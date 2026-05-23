#!/usr/bin/env python3
"""
Calibrate how much divisor-count information is needed to reproduce current motifs.

This diagnostic script reads already-measured real-probe artifacts, recomputes
their public gap records under the exact baseline path, then projects those same
records into weaker divisor-information tiers. It does not modify production
motif derivation, the pruner, or the ladder runner.
"""

from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone
from functools import lru_cache
from pathlib import Path
from typing import Any

import gmpy2
from sympy.ntheory import factorint

from pga_grammar_pruner import prune_factor_space
from public_motif_derivation import (
    _divisor_bucket,
    _first_open_offset,
    _neighboring_gaps_gmp,
    _phase_bucket,
)


ROOT = Path(__file__).resolve().parent
DEFAULT_OUTPUT = ROOT / "output" / "divisor_classifier_calibration"
BASELINE_INPUTS = (
    ROOT / "output" / "ladder" / "real_semiprime_64_72_samples_5_gmp_backend" / "ladder_summary.json",
    ROOT / "output" / "ladder" / "real_semiprime_64_80_samples_3_gmp_backend" / "ladder_summary.json",
    ROOT / "output" / "ladder" / "real_semiprime_64_80_samples_3_replay" / "ladder_summary.json",
)
TIERS = ("tier_0", "tier_1", "tier_2", "tier_3", "tier_exact")


@dataclass(frozen=True)
class CoordinateRecord:
    offset: int
    value: gmpy2.mpz


@dataclass(frozen=True)
class TierGap:
    first_open_offset: int
    winner_offset: int | None
    winner_divisor_label: str
    carrier_family: str
    exact_type_key: str
    reduced_state: str
    rank: tuple[int, int]


def phase_for_coordinate(left_endpoint: gmpy2.mpz, right_endpoint: gmpy2.mpz, coordinate: gmpy2.mpz) -> str:
    width = int(right_endpoint - left_endpoint)
    offset = int(coordinate - left_endpoint)
    if width < 1:
        return "empty"
    return _phase_bucket((offset * 1000) // width)


@lru_cache(maxsize=128)
def exact_gap_records_cached(left_endpoint_int: int, right_endpoint_int: int) -> tuple[CoordinateRecord, ...]:
    left_endpoint = gmpy2.mpz(left_endpoint_int)
    right_endpoint = gmpy2.mpz(right_endpoint_int)
    width = int(right_endpoint - left_endpoint)
    if width <= 1:
        return ()

    return tuple(
        CoordinateRecord(
            offset=offset,
            value=left_endpoint + offset,
        )
        for offset in range(1, width)
    )


def exact_gap_records(left_endpoint: gmpy2.mpz, right_endpoint: gmpy2.mpz) -> tuple[CoordinateRecord, ...]:
    return exact_gap_records_cached(int(left_endpoint), int(right_endpoint))


def family_for_count(value: gmpy2.mpz, divisor_count: int) -> str:
    if divisor_count == 3:
        return "prime_square"
    if divisor_count == 4:
        return "d4_even" if value % 2 == 0 else "d4_odd"
    return "higher_divisor_even" if value % 2 == 0 else "higher_divisor_odd"


@lru_cache(maxsize=4096)
def divisor_count_public_coordinate(value: int) -> int:
    factors = factorint(value)
    total = 1
    for exponent in factors.values():
        total *= int(exponent) + 1
    return total


def is_prime_square(value: gmpy2.mpz) -> bool:
    root, remainder = gmpy2.isqrt_rem(value)
    return remainder == 0 and bool(gmpy2.is_prime(root))


def record_payload(first_open: int, record: CoordinateRecord, divisor_label: str, family: str, bucket: str, rank: tuple[int, int]) -> TierGap:
    exact_type_key = f"o{first_open}_{divisor_label}_a{record.offset}_{family}"
    reduced_state = f"o{first_open}_{family}|{bucket}"
    return TierGap(
        first_open_offset=first_open,
        winner_offset=record.offset,
        winner_divisor_label=divisor_label,
        carrier_family=family,
        exact_type_key=exact_type_key,
        reduced_state=reduced_state,
        rank=rank,
    )


def tier_gap(left_endpoint: gmpy2.mpz, right_endpoint: gmpy2.mpz, records: list[CoordinateRecord], tier: str) -> TierGap:
    first_open = _first_open_offset(left_endpoint)
    if not records:
        return TierGap(
            first_open_offset=first_open,
            winner_offset=None,
            winner_divisor_label="empty",
            carrier_family="empty",
            exact_type_key=f"o{first_open}_empty",
            reduced_state=f"o{first_open}_empty|empty",
            rank=(0, 0),
        )

    if tier == "tier_0":
        winner = records[0]
        parity = "even" if winner.value % 2 == 0 else "odd"
        return record_payload(first_open, winner, "unknown", f"parity_{parity}", "unknown", (0, winner.offset))

    for record in records:
        if is_prime_square(record.value):
            return record_payload(first_open, record, "d3", "prime_square", "d<=4", (0, record.offset))

    if tier == "tier_1":
        winner = records[0]
        parity = "even" if winner.value % 2 == 0 else "odd"
        return record_payload(first_open, winner, "unknown", f"non_prime_square_{parity}", "unknown", (1, winner.offset))

    for record in records:
        divisor_count = divisor_count_public_coordinate(int(record.value))
        if divisor_count == 4:
            parity = "even" if record.value % 2 == 0 else "odd"
            return record_payload(first_open, record, "d4", f"d4_{parity}", "d<=4", (1, record.offset))

    if tier == "tier_2":
        winner = records[0]
        parity = "even" if winner.value % 2 == 0 else "odd"
        return record_payload(first_open, winner, "higher", f"higher_divisor_{parity}", "higher", (2, winner.offset))

    if tier == "tier_3":
        ranked: list[tuple[tuple[int, int], str, str, str, CoordinateRecord]] = []
        for record in records:
            divisor_count = divisor_count_public_coordinate(int(record.value))
            bucket = _divisor_bucket(divisor_count)
            bucket_rank = {"5<=d<=16": 2, "17<=d<=64": 3, "d>64": 4}.get(bucket, 5)
            parity = "even" if record.value % 2 == 0 else "odd"
            ranked.append(((bucket_rank, record.offset), bucket, f"higher_divisor_{parity}", bucket, record))
        rank, divisor_label, family, bucket, winner = min(ranked, key=lambda item: item[0])
        return record_payload(first_open, winner, divisor_label, family, bucket, rank)

    raise ValueError(f"unknown non-exact tier: {tier}")


@lru_cache(maxsize=128)
def derive_all_tier_payloads(n_value: int) -> dict[str, dict[str, Any]]:
    n_mpz = gmpy2.mpz(n_value)
    previous_endpoint, left_endpoint, right_endpoint, _ = _neighboring_gaps_gmp(n_mpz)

    containing_records = exact_gap_records(left_endpoint, right_endpoint)
    previous_records = exact_gap_records(previous_endpoint, left_endpoint)

    payloads: dict[str, dict[str, Any]] = {}
    for tier in TIERS:
        if tier == "tier_exact":
            continue
        containing = tier_gap(left_endpoint, right_endpoint, list(containing_records), tier)
        previous = tier_gap(previous_endpoint, left_endpoint, list(previous_records), tier)
        phase = phase_for_coordinate(left_endpoint, right_endpoint, n_mpz)
        prev_short = previous.reduced_state.split("|")[0]
        motif = f"{containing.exact_type_key}@{phase}"
        if prev_short:
            motif = f"{motif} + {prev_short} prev"

        pruned = prune_factor_space(motif)
        payloads[tier] = {
            "motif": motif,
            "rules_fired": pruned["rules_fired"],
            "reduction_percent": pruned["reduction_percent"],
            "winner_offset": containing.winner_offset,
            "carrier_family": containing.carrier_family,
            "previous_reduced_state": prev_short,
            "containing_rank": list(containing.rank),
            "previous_rank": list(previous.rank),
            "divisor_label": containing.winner_divisor_label,
        }
    return payloads



def parse_baseline_components(motif: str) -> dict[str, Any]:
    winner_match = re.search(r"_a(\d+)_", motif)
    carrier_match = re.search(r"_a\d+_([^@+]+)@", motif)
    previous = None
    if " + " in motif:
        previous = motif.split(" + ", 1)[1].removesuffix(" prev")
    return {
        "winner_offset": int(winner_match.group(1)) if winner_match else None,
        "carrier_family": carrier_match.group(1) if carrier_match else None,
        "previous_reduced_state": previous,
    }


def first_failure(baseline: dict[str, Any], candidate: dict[str, Any]) -> str | None:
    for key in ("winner_offset", "carrier_family", "previous_reduced_state"):
        if baseline.get(key) != candidate.get(key):
            return key
    if baseline["motif"] != candidate["motif"]:
        return "motif"
    if set(baseline["rules_fired"]) != set(candidate["rules_fired"]):
        return "rules_fired"
    if float(baseline["reduction_percent"]) != float(candidate["reduction_percent"]):
        return "reduction_percent"
    return None


def baseline_cases(input_path: Path) -> list[dict[str, Any]]:
    source = json.loads(input_path.read_text(encoding="utf-8"))
    rows: list[dict[str, Any]] = []
    for bits, level in sorted(source["levels"].items(), key=lambda item: int(item[0])):
        for case in level.get("per_case", []):
            if case.get("status") != "resolved" or case.get("unresolved_flag"):
                continue
            motif = str(case["derived_motif"])
            components = parse_baseline_components(motif)
            rows.append(
                {
                    "source": str(input_path.relative_to(ROOT)),
                    "bit_length": int(bits),
                    "case_id": case["case_id"],
                    "N": int(case["N"]),
                    "motif": motif,
                    "rules_fired": case["rules_fired"],
                    "reduction_percent": case["reduction_percent"],
                    **components,
                }
            )
    return rows


def minimum_successful_tier(tier_results: dict[str, dict[str, Any]]) -> str | None:
    for tier in TIERS:
        if tier_results[tier]["status"] == "reproduced":
            return tier
    return None


def calibrate(inputs: tuple[Path, ...]) -> dict[str, Any]:
    per_source_expected_counts = {
        "output/ladder/real_semiprime_64_72_samples_5_gmp_backend/ladder_summary.json": 10,
        "output/ladder/real_semiprime_64_80_samples_3_gmp_backend/ladder_summary.json": 9,
        "output/ladder/real_semiprime_64_80_samples_3_replay/ladder_summary.json": 9,
    }
    cases: list[dict[str, Any]] = []
    for input_path in inputs:
        cases.extend(baseline_cases(input_path))

    per_case: list[dict[str, Any]] = []
    tier_totals = {tier: Counter() for tier in TIERS}
    motif_totals: dict[str, dict[str, Counter[str]]] = defaultdict(lambda: {tier: Counter() for tier in TIERS})

    for baseline in cases:
        tier_results: dict[str, dict[str, Any]] = {}
        candidate_payloads = derive_all_tier_payloads(baseline["N"])
        for tier in TIERS:
            if tier == "tier_exact":
                candidate = {
                    "motif": baseline["motif"],
                    "rules_fired": baseline["rules_fired"],
                    "reduction_percent": baseline["reduction_percent"],
                    "winner_offset": baseline["winner_offset"],
                    "carrier_family": baseline["carrier_family"],
                    "previous_reduced_state": baseline["previous_reduced_state"],
                    "containing_rank": ["baseline_exact"],
                    "previous_rank": ["baseline_exact"],
                    "divisor_label": "baseline_exact",
                }
            else:
                candidate = candidate_payloads[tier]
            failure = first_failure(baseline, candidate)
            reproduced = failure is None
            tier_results[tier] = {
                **candidate,
                "status": "reproduced" if reproduced else "mismatched",
                "first_failing_component": failure,
            }
            tier_totals[tier]["reproduced" if reproduced else "mismatched"] += 1
            motif_totals[baseline["motif"]][tier]["reproduced" if reproduced else "mismatched"] += 1

        per_case.append(
            {
                "source": baseline["source"],
                "bit_length": baseline["bit_length"],
                "case_id": baseline["case_id"],
                "N": baseline["N"],
                "baseline": {
                    "motif": baseline["motif"],
                    "rules_fired": baseline["rules_fired"],
                    "reduction_percent": baseline["reduction_percent"],
                    "winner_offset": baseline["winner_offset"],
                    "carrier_family": baseline["carrier_family"],
                    "previous_reduced_state": baseline["previous_reduced_state"],
                },
                "minimum_successful_tier": minimum_successful_tier(tier_results),
                "tiers": tier_results,
            }
        )

    source_counts = Counter(case["source"] for case in cases)
    reproduction_by_tier = {
        tier: {
            "reproduced": tier_totals[tier]["reproduced"],
            "mismatched": tier_totals[tier]["mismatched"],
            "total": sum(tier_totals[tier].values()),
            "reproduction_rate_percent": round(
                (tier_totals[tier]["reproduced"] / sum(tier_totals[tier].values())) * 100, 2
            )
            if sum(tier_totals[tier].values())
            else 0.0,
        }
        for tier in TIERS
    }
    full_surface_tier = next(
        (
            tier
            for tier in TIERS
            if reproduction_by_tier[tier]["reproduced"] == reproduction_by_tier[tier]["total"]
        ),
        None,
    )

    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "artifact_type": "diagnostic_divisor_classifier_calibration",
        "not_reduction_evidence_surface": True,
        "header": "This is a diagnostic calibration report. It is not a reduction evidence surface.",
        "baseline_inputs": [str(path.relative_to(ROOT)) for path in inputs],
        "baseline_source": "original committed/pre-exact-bit fixture artifacts",
        "classifier_computation_note": (
            "Non-exact tiers compute only the class they report. Public-coordinate "
            "factorization is used inside the diagnostic to classify d4 and coarse "
            "higher buckets; exact tau values are not emitted for non-exact tiers."
        ),
        "expected_case_counts": per_source_expected_counts,
        "observed_case_counts": dict(sorted(source_counts.items())),
        "total_cases": len(cases),
        "tiers": {
            "tier_0": "parity and gap position only; no divisor-family detection",
            "tier_1": "prime_square vs non-prime_square; withholds d4 vs higher_divisor",
            "tier_2": "prime_square, d4, higher_divisor; no exact tau(n) when tau(n) > 4",
            "tier_3": "prime_square, d4, and coarse higher buckets; no exact tau(n) inside buckets",
            "tier_exact": "exact divisor count control",
        },
        "aggregate": {
            "reproduction_by_tier": reproduction_by_tier,
            "lowest_full_surface_success_tier": full_surface_tier,
            "reproduction_by_motif": {
                motif: {
                    tier: {
                        "reproduced": counts["reproduced"],
                        "mismatched": counts["mismatched"],
                        "total": sum(counts.values()),
                    }
                    for tier, counts in tier_map.items()
                }
                for motif, tier_map in sorted(motif_totals.items())
            },
        },
        "per_case": per_case,
    }


def write_reports(result: dict[str, Any], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "calibration_summary.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    lines = [
        "# Divisor Classifier Calibration",
        "",
        result["header"],
        "",
        f"- artifact_type: `{result['artifact_type']}`",
        f"- baseline_source: `{result['baseline_source']}`",
        f"- total_cases: `{result['total_cases']}`",
        f"- lowest_full_surface_success_tier: `{result['aggregate']['lowest_full_surface_success_tier']}`",
        f"- classifier_computation_note: {result['classifier_computation_note']}",
        "",
        "## Baseline Inputs",
        "",
    ]
    for source, expected in result["expected_case_counts"].items():
        observed = result["observed_case_counts"].get(source, 0)
        lines.append(f"- `{source}`: observed `{observed}`, expected `{expected}`")

    lines += [
        "",
        "## Tier Definitions",
        "",
    ]
    for tier, definition in result["tiers"].items():
        lines.append(f"- `{tier}`: {definition}")

    lines += [
        "",
        "## Reproduction By Tier",
        "",
        "| tier | reproduced | mismatched | total | rate |",
        "|------|------------|------------|-------|------|",
    ]
    for tier in TIERS:
        item = result["aggregate"]["reproduction_by_tier"][tier]
        lines.append(
            f"| `{tier}` | {item['reproduced']} | {item['mismatched']} | "
            f"{item['total']} | {item['reproduction_rate_percent']:.2f}% |"
        )

    lines += [
        "",
        "## Per-Case Minimum Tier",
        "",
        "| source | case_id | bits | baseline motif | minimum successful tier | first non-exact failure |",
        "|--------|---------|------|----------------|-------------------------|-------------------------|",
    ]
    for case in result["per_case"]:
        first_non_exact_failure = "-"
        for tier in TIERS:
            if tier == "tier_exact":
                continue
            failure = case["tiers"][tier]["first_failing_component"]
            if failure:
                first_non_exact_failure = f"{tier}:{failure}"
                break
        lines.append(
            f"| `{case['source']}` | `{case['case_id']}` | {case['bit_length']} | "
            f"`{case['baseline']['motif']}` | `{case['minimum_successful_tier']}` | "
            f"`{first_non_exact_failure}` |"
        )

    lines += [
        "",
        "## Motif Reproduction Summary",
        "",
        "| motif | tier_0 | tier_1 | tier_2 | tier_3 | tier_exact |",
        "|-------|--------|--------|--------|--------|------------|",
    ]
    for motif, tier_map in result["aggregate"]["reproduction_by_motif"].items():
        cells = []
        for tier in TIERS:
            item = tier_map[tier]
            cells.append(f"{item['reproduced']}/{item['total']}")
        lines.append(f"| `{motif}` | " + " | ".join(cells) + " |")

    lines.append("")
    lines.append("This calibration uses public coordinates from already-measured baseline rows. It does not modify production motif derivation or publish a new reduction surface.")
    (output_dir / "calibration_summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def validate_result(result: dict[str, Any]) -> None:
    for source, expected in result["expected_case_counts"].items():
        observed = result["observed_case_counts"].get(source, 0)
        if observed != expected:
            raise RuntimeError(f"{source} expected {expected} cases but observed {observed}")

    exact = result["aggregate"]["reproduction_by_tier"]["tier_exact"]
    if exact["reproduced"] != exact["total"] or exact["mismatched"] != 0:
        raise RuntimeError("tier_exact did not reproduce every baseline row")


def main() -> None:
    result = calibrate(BASELINE_INPUTS)
    validate_result(result)
    write_reports(result, DEFAULT_OUTPUT)
    print(json.dumps(result["aggregate"]["reproduction_by_tier"], indent=2, sort_keys=True))
    print(f"Calibration written to: {DEFAULT_OUTPUT}")


if __name__ == "__main__":
    main()
