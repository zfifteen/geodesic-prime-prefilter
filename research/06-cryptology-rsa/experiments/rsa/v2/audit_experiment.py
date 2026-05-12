#!/usr/bin/env python3
"""Audit RSA v2 inference results against physically separate factors."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

import gmpy2


def read_jsonl(path: Path) -> list[dict[str, object]]:
    """Read LF-delimited JSON rows."""
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def rows_by_case(rows: list[dict[str, object]]) -> dict[str, dict[str, object]]:
    """Index rows by case identifier."""
    return {str(row["case_id"]): row for row in rows}


def audit_case(
    case: dict[str, object],
    factors: dict[str, object],
    inference: dict[str, object],
) -> dict[str, object]:
    """Return one audit status row without exposing audit-only endpoints."""
    n_value = gmpy2.mpz(str(case["N"]))
    p_value = gmpy2.mpz(str(factors["p"]))
    q_value = gmpy2.mpz(str(factors["q"]))
    # Audit multiplies the physically separate endpoints to certify the public modulus.
    integrity_pass = p_value * q_value == n_value
    audit_status = "integrity_pass" if integrity_pass else "integrity_fail"

    inference_status = "inference_audit_fail"
    if integrity_pass and str(inference.get("status")) == "resolved":
        inferred_p = gmpy2.mpz(str(inference["p"]))
        inferred_q = gmpy2.mpz(str(inference["q"]))
        if {str(inferred_p), str(inferred_q)} == {str(p_value), str(q_value)}:
            inference_status = "inference_audit_pass"

    return {
        "case_id": str(case["case_id"]),
        "bits": str(case["bits"]),
        "N": str(n_value),
        "audit_integrity_status": audit_status,
        "inference_audit_status": inference_status,
    }


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    """Write LF-terminated CSV status rows."""
    fieldnames = [
        "case_id",
        "bits",
        "N",
        "audit_integrity_status",
        "inference_audit_status",
    ]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def run_audit(
    cases_path: Path,
    factors_path: Path,
    inference_path: Path,
    output_path: Path,
) -> list[dict[str, object]]:
    """Run the audit and write CSV status rows."""
    cases = read_jsonl(cases_path)
    factors_by_case = rows_by_case(read_jsonl(factors_path))
    inference_by_case = rows_by_case(read_jsonl(inference_path))
    rows = [
        audit_case(
            case,
            factors_by_case[str(case["case_id"])],
            inference_by_case[str(case["case_id"])],
        )
        for case in cases
    ]
    output_path.parent.mkdir(parents=True, exist_ok=True)
    write_csv(output_path, rows)
    return rows


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Audit RSA v2 experiment outputs.")
    parser.add_argument(
        "--cases",
        type=Path,
        default=Path(__file__).resolve().parent / "fixtures" / "ladder_cases.jsonl",
        help="Public ladder cases JSONL path.",
    )
    parser.add_argument(
        "--factors",
        type=Path,
        default=Path(__file__).resolve().parent / "fixtures" / "audit_factors.jsonl",
        help="Physically separate audit endpoints JSONL path.",
    )
    parser.add_argument(
        "--inference",
        type=Path,
        default=Path(__file__).resolve().parent / "output" / "inference_rows.jsonl",
        help="Inference rows JSONL path.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(__file__).resolve().parent / "output" / "audit_results.csv",
        help="Audit CSV output path.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    """Run the audit from the command line."""
    args = parse_args(argv)
    run_audit(args.cases, args.factors, args.inference, args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
