#!/usr/bin/env python3
"""Classical validator for the toy PGSPG factorizer."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


TWO_DIGIT_PRIMES = (
    11,
    13,
    17,
    19,
    23,
    29,
    31,
    37,
    41,
    43,
    47,
    53,
    59,
    61,
    67,
    71,
    73,
    79,
    83,
    89,
    97,
)
DEFAULT_MAX_AUDIT_FACTOR = 99
DECISION_KNOBS = (
    "pgs_endpoint_lock",
    "upper_native_width_dominance",
    "endpoint_lock_then_upper_native_width_dominance",
    "reciprocal_floor_boundary_lock",
    "both_chambers_inside",
    "reset_signature_equal",
    "carrier_lock_equal",
)


def is_prime(value: int) -> bool:
    """Return classical primality for validator-only audit surfaces."""
    if value < 2:
        return False
    if value == 2:
        return True
    if value % 2 == 0:
        return False
    divisor = 3
    while divisor * divisor <= value:
        if value % divisor == 0:
            return False
        divisor += 2
    return True


def audit_primes(max_factor: int = DEFAULT_MAX_AUDIT_FACTOR) -> list[int]:
    """Return deterministic validator-only primes on the bounded surface."""
    if max_factor < 11:
        raise ValueError("max_factor must be at least 11")
    return [value for value in range(11, max_factor + 1) if is_prime(value)]


def prime_pairs(max_factor: int = DEFAULT_MAX_AUDIT_FACTOR) -> list[tuple[int, int]]:
    """Return the deterministic bounded semiprime audit surface."""
    primes = audit_primes(max_factor)
    return [
        (p_value, q_value)
        for index, p_value in enumerate(primes)
        for q_value in primes[index:]
    ]


def two_digit_prime_pairs() -> list[tuple[int, int]]:
    """Return the deterministic two-digit semiprime audit surface."""
    return prime_pairs(DEFAULT_MAX_AUDIT_FACTOR)


def read_jsonl(path: Path) -> list[dict[str, object]]:
    """Read LF-delimited JSON rows."""
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    """Write LF-terminated CSV audit rows."""
    fieldnames = [
        "case_id",
        "N",
        "audit_p",
        "audit_q",
        "inference_status",
        "inferred_p",
        "inferred_q",
        "audit_status",
    ]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_decision_knob_csv(path: Path, rows: list[dict[str, object]]) -> None:
    """Write LF-terminated decision-knob audit rows."""
    fieldnames = [
        "knob",
        "valid_for_pgs_factorizer",
        "validity_note",
        "total_cases",
        "resolved",
        "unresolved",
        "ambiguous",
        "no_survivor",
        "audit_pass",
        "audit_fail",
        "resolved_precision",
        "resolution_rate",
    ]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def audit_factors_by_n(
    max_factor: int = DEFAULT_MAX_AUDIT_FACTOR,
) -> dict[int, tuple[int, int]]:
    """Return classical factors indexed by public modulus."""
    factors: dict[int, tuple[int, int]] = {}
    for p_value, q_value in prime_pairs(max_factor):
        factors[p_value * q_value] = (p_value, q_value)
    return factors


def validate_inference_row(
    row: dict[str, object],
    max_factor: int = DEFAULT_MAX_AUDIT_FACTOR,
) -> dict[str, object]:
    """Classically validate one inference row."""
    n_value = int(row["N"])
    factors = audit_factors_by_n(max_factor).get(n_value)
    if factors is None:
        raise ValueError(f"N={n_value} is outside the bounded audit surface")

    p_value, q_value = factors
    inferred_p = row.get("p")
    inferred_q = row.get("q")
    audit_status = "unresolved"
    if row.get("status") == "resolved":
        if (int(inferred_p), int(inferred_q)) == (p_value, q_value):
            audit_status = "audit_pass"
        else:
            audit_status = "audit_fail"

    return {
        "case_id": str(row.get("case_id", "")),
        "N": n_value,
        "audit_p": p_value,
        "audit_q": q_value,
        "inference_status": str(row["status"]),
        "inferred_p": "" if inferred_p is None else int(inferred_p),
        "inferred_q": "" if inferred_q is None else int(inferred_q),
        "audit_status": audit_status,
    }


def validate_inference_rows(
    rows: list[dict[str, object]],
    max_factor: int = DEFAULT_MAX_AUDIT_FACTOR,
) -> list[dict[str, object]]:
    """Classically validate inference rows."""
    return [validate_inference_row(row, max_factor=max_factor) for row in rows]


def decision_knob_validity(knob: str) -> tuple[bool, str]:
    """Return whether one knob is allowed inside the PGS factorizer."""
    if knob == "pgs_endpoint_lock":
        return True, "public mutual reciprocal endpoint lock"
    if knob == "upper_native_width_dominance":
        return False, "candidate public PGSPG invariant, validator-side only"
    if knob == "endpoint_lock_then_upper_native_width_dominance":
        return False, "staged validator-only candidate after endpoint lock"
    if knob == "reciprocal_floor_boundary_lock":
        return False, "divisibility-adjacent reciprocal cell boundary"
    return True, "public PGSPG certificate diagnostic"


def survivor_passes_knob(row: dict[str, object], knob: str) -> bool:
    """Return whether one survivor row passes a decision knob."""
    if knob == "pgs_endpoint_lock":
        return bool(row["mutual_reciprocal_endpoint_lock"])
    if knob == "upper_native_width_dominance":
        return upper_native_width_dominance(row)
    if knob == "endpoint_lock_then_upper_native_width_dominance":
        return upper_native_width_dominance(row)
    if knob == "reciprocal_floor_boundary_lock":
        n_value = int(row["N"])
        lower_endpoint = int(row["lower_reset_endpoint"])
        upper_endpoint = int(row["upper_reset_endpoint"])
        return (n_value - 1) // lower_endpoint < upper_endpoint
    if knob == "both_chambers_inside":
        return (
            bool(row["upper_chamber_inside_lower_image"])
            and bool(row["lower_chamber_inside_upper_image"])
        )
    if knob == "reset_signature_equal":
        return str(row["lower_reset_signature"]) == str(row["upper_reset_signature"])
    if knob == "carrier_lock_equal":
        return str(row["lower_lock_carrier_d"]) == str(row["upper_lock_carrier_d"])
    raise ValueError(f"unknown decision knob: {knob}")


def upper_native_width_dominance(row: dict[str, object]) -> bool:
    """Return the validator-side upper native width dominance candidate."""
    upper_native_width = int(row["upper_reset_deadline_value"]) - int(
        row["upper_anchor"]
    )
    upper_image_width = int(row["upper_chamber_image_max"]) - int(
        row["upper_chamber_image_min"]
    )
    return upper_native_width >= upper_image_width


def summarize_decision_knob(
    inference_rows: list[dict[str, object]],
    survivor_rows: list[dict[str, object]],
    knob: str,
    max_factor: int = DEFAULT_MAX_AUDIT_FACTOR,
) -> dict[str, object]:
    """Return validator-side metrics for one decision knob."""
    factors_by_n = audit_factors_by_n(max_factor)
    survivors_by_case: dict[str, list[dict[str, object]]] = {}
    for survivor in survivor_rows:
        survivors_by_case.setdefault(str(survivor["case_id"]), []).append(survivor)

    resolved = 0
    ambiguous = 0
    no_survivor = 0
    audit_pass = 0
    audit_fail = 0
    for inference in inference_rows:
        case_id = str(inference["case_id"])
        n_value = int(inference["N"])
        case_survivors = survivors_by_case.get(case_id, [])
        if (
            knob == "endpoint_lock_then_upper_native_width_dominance"
            and len(case_survivors) == 1
        ):
            passing = case_survivors
        else:
            passing = [
                survivor
                for survivor in case_survivors
                if survivor_passes_knob(survivor, knob)
            ]
        if len(passing) == 0:
            no_survivor += 1
            continue
        if len(passing) > 1:
            ambiguous += 1
            continue
        resolved += 1
        survivor = passing[0]
        if (
            int(survivor["lower_reset_endpoint"]),
            int(survivor["upper_reset_endpoint"]),
        ) == factors_by_n[n_value]:
            audit_pass += 1
        else:
            audit_fail += 1

    total = len(inference_rows)
    valid, note = decision_knob_validity(knob)
    unresolved = total - resolved
    return {
        "knob": knob,
        "valid_for_pgs_factorizer": valid,
        "validity_note": note,
        "total_cases": total,
        "resolved": resolved,
        "unresolved": unresolved,
        "ambiguous": ambiguous,
        "no_survivor": no_survivor,
        "audit_pass": audit_pass,
        "audit_fail": audit_fail,
        "resolved_precision": 0.0 if resolved == 0 else audit_pass / resolved,
        "resolution_rate": resolved / total,
    }


def decision_knob_rows(
    inference_rows: list[dict[str, object]],
    survivor_rows: list[dict[str, object]],
    max_factor: int = DEFAULT_MAX_AUDIT_FACTOR,
) -> list[dict[str, object]]:
    """Return validator-side decision-knob rows."""
    return [
        summarize_decision_knob(
            inference_rows,
            survivor_rows,
            knob,
            max_factor=max_factor,
        )
        for knob in DECISION_KNOBS
    ]


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Validate toy PGSPG inference rows.")
    parser.add_argument("--inference", type=Path, required=True)
    parser.add_argument("--survivors", type=Path)
    parser.add_argument("--max-audit-factor", type=int, default=DEFAULT_MAX_AUDIT_FACTOR)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--decision-knobs-output", type=Path)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    """Run the classical validator."""
    args = parse_args(argv)
    inference_rows = read_jsonl(args.inference)
    rows = validate_inference_rows(
        inference_rows,
        max_factor=args.max_audit_factor,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    write_csv(args.output, rows)
    if args.survivors is not None and args.decision_knobs_output is not None:
        knob_rows = decision_knob_rows(
            inference_rows,
            read_jsonl(args.survivors),
            max_factor=args.max_audit_factor,
        )
        args.decision_knobs_output.parent.mkdir(parents=True, exist_ok=True)
        write_decision_knob_csv(args.decision_knobs_output, knob_rows)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
