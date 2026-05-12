#!/usr/bin/env python3
"""Classical validation for exponent-decade ladder rows."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

from sympy import isprime


ROOT = Path(__file__).resolve().parents[3]
DEFAULT_OUTPUT_DIR = ROOT / "research" / "09-exponents" / "output" / "exponent_decade_ladder_probe"
DEFAULT_INPUT = DEFAULT_OUTPUT_DIR / "pgs_ladder_rows.csv"


VALIDATION_FIELDNAMES = [
    "rung_min_exponent",
    "rung_max_exponent",
    "exponent",
    "exponent_status",
    "pgs_mersenne_location_inferred",
    "classical_mersenne_number_is_prime",
    "classical_validation_reason",
    "classical_agreement",
]


def build_parser() -> argparse.ArgumentParser:
    """Build the CLI parser."""
    parser = argparse.ArgumentParser(
        description="Validate exponent-decade ladder PGS rows.",
    )
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    return parser


def parse_bool(value: object) -> bool:
    """Parse a CSV boolean field."""
    if value is True:
        return True
    if value is False:
        return False
    if str(value) == "True":
        return True
    if str(value) == "False":
        return False
    raise ValueError(f"invalid boolean value: {value!r}")


def read_csv(path: Path) -> list[dict[str, str]]:
    """Read CSV rows from a path."""
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def validation_row(row: dict[str, str]) -> dict[str, object]:
    """Return one validation row."""
    pgs_inferred = parse_bool(row["mersenne_location_inferred"])
    if row["exponent_status"] == "exponent_divisor_count_not_two":
        mersenne_is_prime = False
        reason = "composite_exponent"
    elif row["mersenne_number"]:
        mersenne_is_prime = bool(isprime(int(row["mersenne_number"])))
        reason = "classical_endpoint_check"
    else:
        mersenne_is_prime = False
        reason = "no_endpoint_emitted"
    return {
        "rung_min_exponent": int(row["rung_min_exponent"]),
        "rung_max_exponent": int(row["rung_max_exponent"]),
        "exponent": int(row["exponent"]),
        "exponent_status": row["exponent_status"],
        "pgs_mersenne_location_inferred": pgs_inferred,
        "classical_mersenne_number_is_prime": mersenne_is_prime,
        "classical_validation_reason": reason,
        "classical_agreement": pgs_inferred == mersenne_is_prime,
    }


def validate_rows(rows: list[dict[str, str]]) -> list[dict[str, object]]:
    """Return validation rows."""
    return [validation_row(row) for row in rows]


def summarize(rows: list[dict[str, object]]) -> dict[str, object]:
    """Return compact validation summary."""
    return {
        "validated_row_count": len(rows),
        "pgs_mersenne_location_inferred_count": sum(
            bool(row["pgs_mersenne_location_inferred"]) for row in rows
        ),
        "classical_mersenne_prime_count": sum(
            bool(row["classical_mersenne_number_is_prime"]) for row in rows
        ),
        "classical_agreement_count": sum(bool(row["classical_agreement"]) for row in rows),
        "classical_false_positive_count": sum(
            bool(row["pgs_mersenne_location_inferred"])
            and not bool(row["classical_mersenne_number_is_prime"])
            for row in rows
        ),
        "classical_false_negative_count": sum(
            not bool(row["pgs_mersenne_location_inferred"])
            and bool(row["classical_mersenne_number_is_prime"])
            for row in rows
        ),
    }


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    """Write LF-terminated CSV rows."""
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_outputs(output_dir: Path, rows: list[dict[str, object]]) -> None:
    """Write validation outputs."""
    output_dir.mkdir(parents=True, exist_ok=True)
    write_csv(output_dir / "validation_rows.csv", rows, VALIDATION_FIELDNAMES)
    (output_dir / "validation_summary.json").write_text(
        json.dumps(summarize(rows), indent=2) + "\n",
        encoding="utf-8",
    )


def main(argv: list[str] | None = None) -> int:
    """Run validation for PGS ladder rows."""
    args = build_parser().parse_args(argv)
    rows = validate_rows(read_csv(args.input))
    write_outputs(args.output_dir, rows)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
