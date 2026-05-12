#!/usr/bin/env python3
"""Run a high-scale decade-window certificate for width-2 chambers."""

from __future__ import annotations

import argparse
import csv
import importlib.util
import json
from pathlib import Path

from sympy import factorint, prevprime


ROOT = Path(__file__).resolve().parents[3]
WIDTH2_PROBE_PATH = Path(__file__).with_name("twin_prime_width2_pgs_generator_probe.py")
ENDPOINT_PROBE_PATH = Path(__file__).with_name("twin_prime_endpoint_fixed_point_decomposition_probe.py")
DEFAULT_OUTPUT_DIR = ROOT / "research" / "10-twin-primes" / "output" / "twin_prime_decade_ladder_probe"
DEFAULT_SAMPLE_SIZE = 4096
DEFAULT_MIN_EXPONENT = 6
DEFAULT_MAX_EXPONENT = 18


def load_module(path: Path, name: str):
    """Load one experiment-local module."""
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"unable to load {name} module")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


WIDTH2_PROBE = load_module(WIDTH2_PROBE_PATH, "twin_prime_width2_pgs_generator_probe")
ENDPOINT_PROBE = load_module(
    ENDPOINT_PROBE_PATH,
    "twin_prime_endpoint_fixed_point_decomposition_probe",
)


def build_parser() -> argparse.ArgumentParser:
    """Build the CLI parser."""
    parser = argparse.ArgumentParser(
        description="Run the twin-prime width-2 decade-window ladder.",
    )
    parser.add_argument("--sample-size", type=int, default=DEFAULT_SAMPLE_SIZE)
    parser.add_argument("--min-exponent", type=int, default=DEFAULT_MIN_EXPONENT)
    parser.add_argument("--max-exponent", type=int, default=DEFAULT_MAX_EXPONENT)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    return parser


def factorization(n: int) -> list[tuple[int, int]]:
    """Return exact prime-power factorization using post-decision factorization."""
    return [(int(prime), int(exp)) for prime, exp in sorted(factorint(int(n)).items())]


def sampled_eligible_anchors_near(scale: int, sample_size: int) -> list[int]:
    """Return deterministic eligible prime anchors immediately below one scale."""
    anchors: list[int] = []
    cursor = int(scale)
    while len(anchors) < int(sample_size):
        q = int(prevprime(cursor))
        if q % 30 in WIDTH2_PROBE.ELIGIBLE_RESIDUES:
            anchors.append(q)
        cursor = q
    return anchors


def generated_contract_record(q: int) -> dict[str, object]:
    """Return the PGS width-2 generator record before audit or decomposition."""
    return WIDTH2_PROBE.width2_record(int(q))


def strip_row(record: dict[str, object], scale: int) -> dict[str, object]:
    """Return one audited and decomposed high-scale row after PGS status exists."""
    q = int(record["q"])
    candidate = int(record["candidate"])
    factors = factorization(candidate)
    tau_candidate = ENDPOINT_PROBE.tau_from_factors(factors)
    endpoint_family = ENDPOINT_PROBE.endpoint_family(factors, tau_candidate)
    endpoint_fixed_point = tau_candidate == 2
    endpoint_class = (
        WIDTH2_PROBE.ENDPOINT_PRIME_CLOSURE
        if endpoint_fixed_point
        else WIDTH2_PROBE.ENDPOINT_COMPOSITE_OBSTRUCTION
    )
    status = str(record["status"])
    false_exclusion = status == WIDTH2_PROBE.STATUS_EXCLUDED and endpoint_fixed_point
    unresolved_composite = status == WIDTH2_PROBE.STATUS_UNRESOLVED and not endpoint_fixed_point

    first_family = None
    second_family = None
    third_family = None
    terminal_family = endpoint_family
    grammar_accounted = endpoint_fixed_point
    grammar_terminal = "endpoint_fixed_point_closure" if endpoint_fixed_point else None
    least_factor = None
    cofactor = None
    second_factor = None
    second_remainder = None
    third_factor = None
    third_remainder = None

    if not endpoint_fixed_point:
        least_factor = factors[0][0]
        cofactor = candidate // least_factor
        cofactor_factors = factorization(cofactor)
        cofactor_tau = ENDPOINT_PROBE.tau_from_factors(cofactor_factors)
        first_family = ENDPOINT_PROBE.endpoint_family(cofactor_factors, cofactor_tau)
        terminal_family = first_family
        if first_family in ENDPOINT_PROBE.LOW_COMPLEXITY_COFACTOR_FAMILIES:
            grammar_accounted = True
            grammar_terminal = f"first_strip_{first_family}"
        else:
            second_factor = cofactor_factors[0][0]
            second_remainder = cofactor // second_factor
            second_factors = factorization(second_remainder)
            second_tau = ENDPOINT_PROBE.tau_from_factors(second_factors)
            second_family = ENDPOINT_PROBE.endpoint_family(second_factors, second_tau)
            terminal_family = second_family
            if second_family in ENDPOINT_PROBE.LOW_COMPLEXITY_COFACTOR_FAMILIES:
                grammar_accounted = True
                grammar_terminal = f"second_strip_{second_family}"
            else:
                third_factor = second_factors[0][0]
                third_remainder = second_remainder // third_factor
                third_factors = factorization(third_remainder)
                third_tau = ENDPOINT_PROBE.tau_from_factors(third_factors)
                third_family = ENDPOINT_PROBE.endpoint_family(third_factors, third_tau)
                terminal_family = third_family
                if third_family in ENDPOINT_PROBE.LOW_COMPLEXITY_COFACTOR_FAMILIES:
                    grammar_accounted = True
                    grammar_terminal = f"third_strip_{third_family}"
                elif ENDPOINT_PROBE.is_prime_power_tail(third_family):
                    grammar_accounted = True
                    grammar_terminal = f"third_strip_prime_power_tail_{third_family}"

    return {
        "scale": int(scale),
        "q": q,
        "q_mod30": q % 30,
        "candidate": candidate,
        "candidate_mod30": candidate % 30,
        "status": status,
        "endpoint_class": endpoint_class,
        "tau_candidate": tau_candidate,
        "endpoint_family": endpoint_family,
        "factor_signature": ENDPOINT_PROBE.factor_signature(factors),
        "false_exclusion": false_exclusion,
        "unresolved_composite": unresolved_composite,
        "least_factor": least_factor,
        "cofactor": cofactor,
        "first_remainder_family": first_family,
        "second_factor": second_factor,
        "second_remainder": second_remainder,
        "second_remainder_family": second_family,
        "third_factor": third_factor,
        "third_remainder": third_remainder,
        "third_remainder_family": third_family,
        "grammar_terminal": grammar_terminal,
        "terminal_family": terminal_family,
        "grammar_accounted": grammar_accounted,
    }


def scale_rows(scale: int, sample_size: int) -> list[dict[str, object]]:
    """Return high-scale rows for one deterministic window."""
    rows = []
    for q in sampled_eligible_anchors_near(int(scale), int(sample_size)):
        record = generated_contract_record(q)
        rows.append(strip_row(record, int(scale)))
    return rows


def count_by(rows: list[dict[str, object]], field: str) -> list[dict[str, object]]:
    """Return grouped counts for one field."""
    counts: dict[object, int] = {}
    for row in rows:
        value = row[field]
        counts[value] = counts.get(value, 0) + 1
    return [
        {field: value, "count": count}
        for value, count in sorted(counts.items(), key=lambda item: (-item[1], str(item[0])))
    ]


def summarize_scale(scale: int, rows: list[dict[str, object]]) -> dict[str, object]:
    """Return one scale summary."""
    closures = [row for row in rows if row["endpoint_class"] == WIDTH2_PROBE.ENDPOINT_PRIME_CLOSURE]
    obstructions = [
        row for row in rows if row["endpoint_class"] == WIDTH2_PROBE.ENDPOINT_COMPOSITE_OBSTRUCTION
    ]
    next_layer = [row for row in obstructions if not bool(row["grammar_accounted"])]
    false_exclusions = [row for row in rows if bool(row["false_exclusion"])]
    unresolved_composites = [row for row in rows if bool(row["unresolved_composite"])]
    return {
        "scale": int(scale),
        "eligible_anchor_count": len(rows),
        "prime_closure_count": len(closures),
        "endpoint_obstruction_count": len(obstructions),
        "low_scale_grammar_accounted_obstruction_count": len(obstructions) - len(next_layer),
        "next_layer_count": len(next_layer),
        "false_exclusion_count": len(false_exclusions),
        "unresolved_composite_count": len(unresolved_composites),
        "low_scale_grammar_coverage_rate": (len(obstructions) - len(next_layer)) / len(obstructions)
        if obstructions
        else 1.0,
        "audit_status": "PASS" if not false_exclusions and not unresolved_composites else "FAIL",
        "grammar_disposition": "CLOSED" if not next_layer else "NEXT_LAYER_FOUND",
    }


def summarize_ladder(scale_summaries: list[dict[str, object]], next_layer_rows: list[dict[str, object]]) -> dict[str, object]:
    """Return pooled ladder summary."""
    total_anchors = sum(int(row["eligible_anchor_count"]) for row in scale_summaries)
    total_closures = sum(int(row["prime_closure_count"]) for row in scale_summaries)
    total_obstructions = sum(int(row["endpoint_obstruction_count"]) for row in scale_summaries)
    total_accounted = sum(int(row["low_scale_grammar_accounted_obstruction_count"]) for row in scale_summaries)
    false_exclusions = sum(int(row["false_exclusion_count"]) for row in scale_summaries)
    unresolved_composites = sum(int(row["unresolved_composite_count"]) for row in scale_summaries)
    return {
        "scale_count": len(scale_summaries),
        "eligible_anchor_count": total_anchors,
        "prime_closure_count": total_closures,
        "endpoint_obstruction_count": total_obstructions,
        "low_scale_grammar_accounted_obstruction_count": total_accounted,
        "next_layer_count": len(next_layer_rows),
        "low_scale_grammar_coverage_rate": total_accounted / total_obstructions if total_obstructions else 1.0,
        "false_exclusion_count": false_exclusions,
        "unresolved_composite_count": unresolved_composites,
        "audit_status": "PASS" if false_exclusions == 0 and unresolved_composites == 0 else "FAIL",
        "grammar_disposition": "CLOSED" if not next_layer_rows else "NEXT_LAYER_FOUND",
        "scale_summaries": scale_summaries,
        "next_layer_terminal_family_distribution": count_by(next_layer_rows, "terminal_family"),
    }


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    """Write LF-terminated CSV rows."""
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def run_ladder(min_exponent: int, max_exponent: int, sample_size: int) -> tuple[dict[str, object], list[dict[str, object]], list[dict[str, object]]]:
    """Run all decade windows and return summary artifacts."""
    scale_summaries: list[dict[str, object]] = []
    next_layer_rows: list[dict[str, object]] = []
    for exponent in range(int(min_exponent), int(max_exponent) + 1):
        scale = 10**exponent
        rows = scale_rows(scale, int(sample_size))
        scale_summaries.append(summarize_scale(scale, rows))
        next_layer_rows.extend(
            row
            for row in rows
            if row["endpoint_class"] == WIDTH2_PROBE.ENDPOINT_COMPOSITE_OBSTRUCTION
            and not bool(row["grammar_accounted"])
        )
    return summarize_ladder(scale_summaries, next_layer_rows), scale_summaries, next_layer_rows


def main(argv: list[str] | None = None) -> int:
    """Run the decade ladder probe."""
    args = build_parser().parse_args(argv)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    summary, scale_summaries, next_layer_rows = run_ladder(
        args.min_exponent,
        args.max_exponent,
        args.sample_size,
    )
    (args.output_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    write_csv(
        args.output_dir / "scale_summary_rows.csv",
        scale_summaries,
        [
            "scale",
            "eligible_anchor_count",
            "prime_closure_count",
            "endpoint_obstruction_count",
            "low_scale_grammar_accounted_obstruction_count",
            "next_layer_count",
            "false_exclusion_count",
            "unresolved_composite_count",
            "low_scale_grammar_coverage_rate",
            "audit_status",
            "grammar_disposition",
        ],
    )
    write_csv(
        args.output_dir / "next_layer_rows.csv",
        next_layer_rows,
        [
            "scale",
            "q",
            "q_mod30",
            "candidate",
            "candidate_mod30",
            "status",
            "endpoint_class",
            "tau_candidate",
            "endpoint_family",
            "factor_signature",
            "false_exclusion",
            "unresolved_composite",
            "least_factor",
            "cofactor",
            "first_remainder_family",
            "second_factor",
            "second_remainder",
            "second_remainder_family",
            "third_factor",
            "third_remainder",
            "third_remainder_family",
            "grammar_terminal",
            "terminal_family",
            "grammar_accounted",
        ],
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
