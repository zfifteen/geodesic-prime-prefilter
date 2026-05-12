#!/usr/bin/env python3
"""Classical validation for inferred unresolved-pressure rows."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

from sympy import isprime


ROOT = Path(__file__).resolve().parents[3]
DEFAULT_OUTPUT_DIR = (
    ROOT
    / "research"
    / "09-exponents"
    / "output"
    / "exponent_unresolved_pressure_probe"
)
DEFAULT_INPUT = DEFAULT_OUTPUT_DIR / "inferred_after_pressure_rows.csv"


VALIDATION_FIELDNAMES = [
    "exponent",
    "mersenne_number",
    "pgs_mersenne_location_inferred",
    "classical_mersenne_number_is_prime",
    "classical_agreement",
]


def build_parser() -> argparse.ArgumentParser:
    """Build the CLI parser."""
    parser = argparse.ArgumentParser(
        description="Validate PGS-inferred unresolved-pressure rows.",
    )
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    return parser


def read_csv(path: Path) -> list[dict[str, str]]:
    """Read CSV rows."""
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def validation_row(row: dict[str, str]) -> dict[str, object]:
    """Return one validation row."""
    mersenne_number = int(row["mersenne_number"])
    mersenne_is_prime = bool(isprime(mersenne_number))
    return {
        "exponent": int(row["exponent"]),
        "mersenne_number": mersenne_number,
        "pgs_mersenne_location_inferred": True,
        "classical_mersenne_number_is_prime": mersenne_is_prime,
        "classical_agreement": mersenne_is_prime,
    }


def validate_rows(rows: list[dict[str, str]]) -> list[dict[str, object]]:
    """Return validation rows for inferred rows only."""
    return [validation_row(row) for row in rows]


def summarize(rows: list[dict[str, object]]) -> dict[str, object]:
    """Return compact validation summary."""
    return {
        "validated_inferred_count": len(rows),
        "classical_confirmed_count": sum(
            bool(row["classical_mersenne_number_is_prime"]) for row in rows
        ),
        "classical_false_positive_count": sum(
            not bool(row["classical_mersenne_number_is_prime"]) for row in rows
        ),
    }


def write_outputs(output_dir: Path, rows: list[dict[str, object]]) -> None:
    """Write validation outputs."""
    output_dir.mkdir(parents=True, exist_ok=True)
    with (output_dir / "validation_rows.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=VALIDATION_FIELDNAMES, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    (output_dir / "validation_summary.json").write_text(
        json.dumps(summarize(rows), indent=2) + "\n",
        encoding="utf-8",
    )


def main(argv: list[str] | None = None) -> int:
    """Run validation."""
    args = build_parser().parse_args(argv)
    write_outputs(args.output_dir, validate_rows(read_csv(args.input)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
