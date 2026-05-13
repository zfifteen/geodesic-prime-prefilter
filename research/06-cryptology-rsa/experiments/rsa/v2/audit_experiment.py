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

    public_lower = inference.get("endpoint_class_lower")
    public_upper = inference.get("endpoint_class_upper")
    public_structure_found = public_lower is not None and public_upper is not None
    factor_found = False
    if integrity_pass and public_structure_found:
        inferred_lower = gmpy2.mpz(str(public_lower))
        inferred_upper = gmpy2.mpz(str(public_upper))
        factor_found = {str(inferred_lower), str(inferred_upper)} == {
            str(p_value),
            str(q_value),
        }
    inference_status = "inference_audit_pass" if factor_found else "inference_audit_fail"

    return {
        "case_id": str(case["case_id"]),
        "bits": str(case["bits"]),
        "N": str(n_value),
        "audit_integrity_status": audit_status,
        "inference_audit_status": inference_status,
        "factor_found": str(factor_found).lower(),
        "public_structure_found": str(public_structure_found).lower(),
        "public_endpoint_class_lower": "" if public_lower is None else str(public_lower),
        "public_endpoint_class_upper": "" if public_upper is None else str(public_upper),
        "factor_endpoint_lower": str(p_value),
        "factor_endpoint_upper": str(q_value),
    }


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    """Write LF-terminated CSV status rows."""
    fieldnames = [
        "case_id",
        "bits",
        "N",
        "factor_found",
        "audit_integrity_status",
        "inference_audit_status",
    ]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n", extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def run_audit(
    cases_path: Path,
    factors_path: Path,
    inference_path: Path,
    output_path: Path,
    factor_results_path: Path,
) -> list[dict[str, object]]:
    """Run the audit and write CSV plus merged factor-result rows."""
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
    write_factor_results_jsonl(factor_results_path, rows)
    return rows


def write_factor_results_jsonl(path: Path, rows: list[dict[str, object]]) -> None:
    """Write user-facing factor verdict rows."""
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = [
        "case_id",
        "bits",
        "N",
        "factor_found",
        "audit_integrity_status",
        "public_structure_found",
        "public_endpoint_class_lower",
        "public_endpoint_class_upper",
        "factor_endpoint_lower",
        "factor_endpoint_upper",
    ]
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for row in rows:
            payload = {field: row[field] for field in fields}
            payload["bits"] = int(str(payload["bits"]))
            payload["factor_found"] = payload["factor_found"] == "true"
            payload["public_structure_found"] = payload["public_structure_found"] == "true"
            handle.write(json.dumps(payload))
            handle.write("\n")


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
    parser.add_argument(
        "--factor-results",
        type=Path,
        default=Path(__file__).resolve().parent / "output" / "factor_result_rows.jsonl",
        help="User-facing factor result JSONL output path.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    """Run the audit from the command line."""
    args = parse_args(argv)
    run_audit(args.cases, args.factors, args.inference, args.output, args.factor_results)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
