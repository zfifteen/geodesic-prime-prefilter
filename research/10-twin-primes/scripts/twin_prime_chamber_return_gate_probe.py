#!/usr/bin/env python3
"""Test whether completed chamber state predicts the next twin-prime gap."""

from __future__ import annotations

import argparse
import csv
import importlib.util
import json
import sys
import time
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
SOURCE_DIR = ROOT / "src" / "python"
if str(SOURCE_DIR) not in sys.path:
    sys.path.insert(0, str(SOURCE_DIR))

DEFAULT_OUTPUT_DIR = ROOT / "research" / "10-twin-primes" / "output" / "twin_prime_chamber_return_gate_probe"
DEFAULT_MAX_RIGHT_PRIME = 1_000_000
DEFAULT_TRAIN_MAX_RIGHT_PRIME = 100_000
GAP_TYPE_PROBE_PATH = Path(__file__).with_name("gwr_dni_gap_type_probe.py")
SIGNATURE_TIERS = ("exact", "type_pair", "family_width", "current_type")


def load_gap_type_probe():
    """Load the experiment-local gap-type probe."""
    spec = importlib.util.spec_from_file_location("gwr_dni_gap_type_probe", GAP_TYPE_PROBE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("unable to load gwr_dni_gap_type_probe module")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


GAP_TYPE_PROBE = load_gap_type_probe()


def build_parser() -> argparse.ArgumentParser:
    """Build the CLI parser."""
    parser = argparse.ArgumentParser(
        description="Measure PGS chamber signatures as twin-prime return gates.",
    )
    parser.add_argument(
        "--max-right-prime",
        type=int,
        default=DEFAULT_MAX_RIGHT_PRIME,
        help="Largest current prime q included in the labeled prediction surface.",
    )
    parser.add_argument(
        "--train-max-right-prime",
        type=int,
        default=DEFAULT_TRAIN_MAX_RIGHT_PRIME,
        help="Largest current prime q included in the train split.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help="Directory for summary and signature rows.",
    )
    parser.add_argument(
        "--min-train-count",
        type=int,
        default=50,
        help="Minimum train support for candidate return gates.",
    )
    parser.add_argument(
        "--min-test-count",
        type=int,
        default=50,
        help="Minimum test support for candidate return gates.",
    )
    parser.add_argument(
        "--min-train-lift",
        type=float,
        default=1.5,
        help="Minimum train lift for candidate return gates.",
    )
    parser.add_argument(
        "--min-test-lift",
        type=float,
        default=1.25,
        help="Minimum test lift for candidate return gates.",
    )
    return parser


def split_name(current_prime: int, train_max_right_prime: int) -> str:
    """Return the chronological split for one current prime."""
    if current_prime <= train_max_right_prime:
        return "train"
    return "test"


def tier_signature_key(row: dict[str, object], tier: str) -> str:
    """Return one deterministic chamber signature for one support-density tier."""
    residue = f"qmod30={int(row['current_prime_mod30'])}"
    if tier == "exact":
        return "|".join(
            (
                str(row["previous_type_key"]),
                str(row["current_type_key"]),
                residue,
                f"g={int(row['current_gap_width'])}",
                f"fam={row['current_carrier_family']}",
                f"a={int(row['current_peak_offset'])}",
            )
        )
    if tier == "type_pair":
        return "|".join((str(row["previous_type_key"]), str(row["current_type_key"]), residue))
    if tier == "family_width":
        return "|".join(
            (
                f"prevfam={row['previous_carrier_family']}",
                f"currfam={row['current_carrier_family']}",
                f"g={int(row['current_gap_width'])}",
                residue,
            )
        )
    if tier == "current_type":
        return "|".join((str(row["current_type_key"]), residue))
    raise ValueError(f"unknown signature tier: {tier}")


def labeled_rows(max_right_prime: int, train_max_right_prime: int) -> list[dict[str, object]]:
    """Return no-leakage chamber rows with the future twin event as label."""
    if max_right_prime <= train_max_right_prime:
        raise ValueError("max_right_prime must be greater than train_max_right_prime")

    gap_rows = GAP_TYPE_PROBE.type_rows(max_right_prime)
    if len(gap_rows) < 3:
        raise ValueError("gap surface must contain at least three rows")

    rows: list[dict[str, object]] = []
    for index in range(2, len(gap_rows)):
        previous_gap = gap_rows[index - 2]
        current_gap = gap_rows[index - 1]
        next_gap = gap_rows[index]
        current_prime = int(next_gap["current_right_prime"])
        if current_prime > max_right_prime:
            continue

        row = {
            "split": split_name(current_prime, train_max_right_prime),
            "current_prime": current_prime,
            "current_prime_mod30": current_prime % 30,
            "previous_type_key": str(previous_gap["type_key"]),
            "previous_gap_width": int(previous_gap["next_gap_width"]),
            "previous_carrier_family": str(previous_gap["carrier_family"]),
            "previous_peak_offset": int(previous_gap["next_peak_offset"]),
            "current_type_key": str(current_gap["type_key"]),
            "current_gap_width": int(current_gap["next_gap_width"]),
            "current_carrier_family": str(current_gap["carrier_family"]),
            "current_peak_offset": int(current_gap["next_peak_offset"]),
            "next_gap_is_twin": int(int(next_gap["next_gap_width"]) == 2),
        }
        row["signature"] = tier_signature_key(row, "exact")
        rows.append(row)

    return rows


def rate(count: int, total: int) -> float:
    """Return count divided by total."""
    return count / total if total else 0.0


def lift(local_rate: float, baseline_rate: float) -> float | None:
    """Return local rate divided by baseline rate."""
    if baseline_rate == 0.0:
        return None
    return local_rate / baseline_rate


def summarize_split(rows: list[dict[str, object]], split: str) -> dict[str, object]:
    """Return split-level twin return counts and residue baselines."""
    split_rows = [row for row in rows if row["split"] == split]
    twin_count = sum(int(row["next_gap_is_twin"]) for row in split_rows)
    residue_totals = Counter(int(row["current_prime_mod30"]) for row in split_rows)
    residue_twins = Counter(
        int(row["current_prime_mod30"]) for row in split_rows if int(row["next_gap_is_twin"])
    )
    return {
        "row_count": len(split_rows),
        "twin_return_count": twin_count,
        "twin_return_rate": rate(twin_count, len(split_rows)),
        "residue_baselines": {
            str(residue): {
                "row_count": int(residue_totals[residue]),
                "twin_return_count": int(residue_twins[residue]),
                "twin_return_rate": rate(int(residue_twins[residue]), int(residue_totals[residue])),
            }
            for residue in sorted(residue_totals)
        },
    }


def signature_rows(rows: list[dict[str, object]], tier: str = "exact") -> list[dict[str, object]]:
    """Aggregate chamber signatures across train and test splits."""
    if tier not in SIGNATURE_TIERS:
        raise ValueError(f"unknown signature tier: {tier}")
    split_summaries = {
        "train": summarize_split(rows, "train"),
        "test": summarize_split(rows, "test"),
    }
    by_signature: dict[str, dict[str, object]] = {}
    split_counts: dict[str, Counter[str]] = {
        "train": Counter(),
        "test": Counter(),
    }
    split_twins: dict[str, Counter[str]] = {
        "train": Counter(),
        "test": Counter(),
    }
    for row in rows:
        signature = tier_signature_key(row, tier)
        by_signature.setdefault(signature, row)
        split = str(row["split"])
        split_counts[split][signature] += 1
        split_twins[split][signature] += int(row["next_gap_is_twin"])

    output_rows: list[dict[str, object]] = []
    for signature in sorted(by_signature):
        first_row = by_signature[signature]
        out: dict[str, object] = {
            "tier": tier,
            "signature": signature,
            "previous_type_key": first_row["previous_type_key"],
            "current_type_key": first_row["current_type_key"],
            "current_prime_mod30": int(first_row["current_prime_mod30"]),
            "current_gap_width": int(first_row["current_gap_width"]),
            "current_carrier_family": first_row["current_carrier_family"],
            "current_peak_offset": int(first_row["current_peak_offset"]),
        }
        for split in ("train", "test"):
            count = int(split_counts[split][signature])
            twin_count = int(split_twins[split][signature])
            local_rate = rate(twin_count, count)
            baseline = split_summaries[split]["residue_baselines"].get(str(out["current_prime_mod30"]))
            baseline_rate = 0.0 if baseline is None else float(baseline["twin_return_rate"])
            out[f"{split}_count"] = count
            out[f"{split}_twin_return_count"] = twin_count
            out[f"{split}_twin_return_rate"] = local_rate
            out[f"{split}_residue_baseline_rate"] = baseline_rate
            out[f"{split}_lift"] = lift(local_rate, baseline_rate)
        output_rows.append(out)

    output_rows.sort(
        key=lambda row: (
            float(row["train_lift"] or 0.0),
            int(row["train_count"]),
            float(row["test_lift"] or 0.0),
        ),
        reverse=True,
    )
    return output_rows


def candidate_gate_rows(
    rows: list[dict[str, object]],
    min_train_count: int,
    min_test_count: int,
    min_train_lift: float,
    min_test_lift: float,
) -> list[dict[str, object]]:
    """Return signatures that satisfy the candidate return-gate rule."""
    candidates = []
    for row in rows:
        train_lift = row["train_lift"]
        test_lift = row["test_lift"]
        if train_lift is None or test_lift is None:
            continue
        if int(row["train_count"]) < min_train_count:
            continue
        if int(row["test_count"]) < min_test_count:
            continue
        if float(train_lift) < min_train_lift:
            continue
        if float(test_lift) < min_test_lift:
            continue
        candidates.append(row)
    return candidates


def summarize_tier(
    signatures: list[dict[str, object]],
    candidates: list[dict[str, object]],
) -> dict[str, object]:
    """Return one compact summary for one signature tier."""
    supported_train = [row for row in signatures if int(row["train_count"]) >= 50]
    supported_test = [row for row in signatures if int(row["test_count"]) >= 50]
    supported_both = [
        row
        for row in signatures
        if int(row["train_count"]) >= 50 and int(row["test_count"]) >= 50
    ]
    return {
        "distinct_signature_count": len(signatures),
        "supported_train_signature_count": len(supported_train),
        "supported_test_signature_count": len(supported_test),
        "supported_both_signature_count": len(supported_both),
        "candidate_gate_count": len(candidates),
        "top_train_lift_signatures": signatures[:20],
        "candidate_gates": candidates[:50],
    }


def first_signal_tier(tier_payload: dict[str, dict[str, object]]) -> str | None:
    """Return the first tier with a candidate gate under the fixed tier order."""
    for tier in SIGNATURE_TIERS:
        if int(tier_payload[tier]["candidate_gate_count"]) > 0:
            return tier
    return None


def summarize(
    rows: list[dict[str, object]],
    tier_payload: dict[str, dict[str, object]],
    max_right_prime: int,
    train_max_right_prime: int,
    runtime_seconds: float,
) -> dict[str, object]:
    """Return the compact summary payload."""
    exact_summary = tier_payload["exact"]
    return {
        "max_right_prime": max_right_prime,
        "train_max_right_prime": train_max_right_prime,
        "row_count": len(rows),
        "signature_tiers": list(SIGNATURE_TIERS),
        "distinct_signature_count": exact_summary["distinct_signature_count"],
        "split_summaries": {
            "train": summarize_split(rows, "train"),
            "test": summarize_split(rows, "test"),
        },
        "candidate_gate_count": exact_summary["candidate_gate_count"],
        "top_train_lift_signatures": exact_summary["top_train_lift_signatures"],
        "candidate_gates": exact_summary["candidate_gates"],
        "tier_summaries": tier_payload,
        "first_signal_tier": first_signal_tier(tier_payload),
        "no_leakage_contract": {
            "signature_tiers": {
                "exact": [
                    "previous_type_key",
                    "current_type_key",
                    "current_prime_mod30",
                    "current_gap_width",
                    "current_carrier_family",
                    "current_peak_offset",
                ],
                "type_pair": [
                    "previous_type_key",
                    "current_type_key",
                    "current_prime_mod30",
                ],
                "family_width": [
                    "previous_carrier_family",
                    "current_carrier_family",
                    "current_gap_width",
                    "current_prime_mod30",
                ],
                "current_type": [
                    "current_type_key",
                    "current_prime_mod30",
                ],
            },
            "label_field": "next_gap_is_twin",
            "forbidden_input_fields": [
                "next_right_prime",
                "next_gap_width",
                "next_gap_type",
                "next_gap_interior",
            ],
        },
        "runtime_seconds": runtime_seconds,
    }


def write_signature_rows(path: Path, rows: list[dict[str, object]]) -> None:
    """Write signature rows as LF-terminated CSV."""
    fieldnames = [
        "tier",
        "signature",
        "previous_type_key",
        "current_type_key",
        "current_prime_mod30",
        "current_gap_width",
        "current_carrier_family",
        "current_peak_offset",
        "train_count",
        "train_twin_return_count",
        "train_twin_return_rate",
        "train_residue_baseline_rate",
        "train_lift",
        "test_count",
        "test_twin_return_count",
        "test_twin_return_rate",
        "test_residue_baseline_rate",
        "test_lift",
    ]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main(argv: list[str] | None = None) -> int:
    """Run the deterministic return-gate probe."""
    args = build_parser().parse_args(argv)
    args.output_dir.mkdir(parents=True, exist_ok=True)

    started = time.perf_counter()
    rows = labeled_rows(args.max_right_prime, args.train_max_right_prime)
    tier_rows: dict[str, list[dict[str, object]]] = {}
    tier_payload: dict[str, dict[str, object]] = {}
    for tier in SIGNATURE_TIERS:
        signatures = signature_rows(rows, tier=tier)
        candidates = candidate_gate_rows(
            signatures,
            min_train_count=args.min_train_count,
            min_test_count=args.min_test_count,
            min_train_lift=args.min_train_lift,
            min_test_lift=args.min_test_lift,
        )
        tier_rows[tier] = signatures
        tier_payload[tier] = summarize_tier(signatures, candidates)
    summary = summarize(
        rows,
        tier_payload,
        max_right_prime=args.max_right_prime,
        train_max_right_prime=args.train_max_right_prime,
        runtime_seconds=time.perf_counter() - started,
    )

    summary_path = args.output_dir / "summary.json"
    summary_path.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    for tier, signatures in tier_rows.items():
        write_signature_rows(args.output_dir / f"{tier}_signature_rows.csv", signatures)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
