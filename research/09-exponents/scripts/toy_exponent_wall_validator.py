#!/usr/bin/env python3
"""Classical validation for toy exponent-wall PGS rows."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

from sympy import factorint, isprime


ROOT = Path(__file__).resolve().parents[3]
DEFAULT_OUTPUT_DIR = ROOT / "research" / "09-exponents" / "output" / "toy_exponent_wall_mechanics_probe"
DEFAULT_INPUT = DEFAULT_OUTPUT_DIR / "pgs_power_of_two_rows.csv"


VALIDATION_FIELDNAMES = [
    "exponent",
    "power_of_two",
    "mersenne_number",
    "pgs_left_prime",
    "pgs_distance_to_left_prime",
    "pgs_mersenne_location_inferred",
    "classical_left_prime_is_prime",
    "classical_mersenne_number_is_prime",
    "classical_agreement",
    "mersenne_number_factor_signature",
]


def build_parser() -> argparse.ArgumentParser:
    """Build the CLI parser."""
    parser = argparse.ArgumentParser(
        description="Validate toy exponent-wall PGS rows with classical checks.",
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


def factor_signature(n: int) -> str:
    """Return a stable factor signature."""
    parts = []
    for prime, exponent in sorted(factorint(n).items()):
        prime = int(prime)
        exponent = int(exponent)
        if exponent == 1:
            parts.append(str(prime))
        else:
            parts.append(f"{prime}^{exponent}")
    return "*".join(parts)


def read_csv(path: Path) -> list[dict[str, str]]:
    """Read CSV rows from a path."""
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def validation_row(row: dict[str, str]) -> dict[str, object]:
    """Return one classical validation row."""
    mersenne_number = int(row["mersenne_number"])
    pgs_inferred = parse_bool(row["mersenne_location_inferred"])
    mersenne_is_prime = bool(isprime(mersenne_number))
    return {
        "exponent": int(row["exponent"]),
        "power_of_two": int(row["power_of_two"]),
        "mersenne_number": mersenne_number,
        "pgs_left_prime": int(row["left_prime"]),
        "pgs_distance_to_left_prime": int(row["distance_to_left_prime"]),
        "pgs_mersenne_location_inferred": pgs_inferred,
        "classical_left_prime_is_prime": bool(isprime(int(row["left_prime"]))),
        "classical_mersenne_number_is_prime": mersenne_is_prime,
        "classical_agreement": pgs_inferred == mersenne_is_prime,
        "mersenne_number_factor_signature": (
            "prime" if mersenne_is_prime else factor_signature(mersenne_number)
        ),
    }


def validate_rows(rows: list[dict[str, str]]) -> list[dict[str, object]]:
    """Return classical validation rows for PGS output rows."""
    return [validation_row(row) for row in rows]


def summarize(rows: list[dict[str, object]]) -> dict[str, object]:
    """Return compact validation summary."""
    inferred = [row for row in rows if bool(row["pgs_mersenne_location_inferred"])]
    not_inferred = [row for row in rows if not bool(row["pgs_mersenne_location_inferred"])]
    actual_prime = [row for row in rows if bool(row["classical_mersenne_number_is_prime"])]
    actual_composite = [row for row in rows if not bool(row["classical_mersenne_number_is_prime"])]
    false_positive_rows = [
        row
        for row in rows
        if bool(row["pgs_mersenne_location_inferred"])
        and not bool(row["classical_mersenne_number_is_prime"])
    ]
    false_negative_rows = [
        row
        for row in rows
        if not bool(row["pgs_mersenne_location_inferred"])
        and bool(row["classical_mersenne_number_is_prime"])
    ]
    return {
        "validated_row_count": len(rows),
        "pgs_mersenne_location_inferred_count": len(inferred),
        "pgs_mersenne_location_not_inferred_count": len(not_inferred),
        "classical_mersenne_prime_count": len(actual_prime),
        "classical_mersenne_composite_count": len(actual_composite),
        "classical_agreement_count": sum(bool(row["classical_agreement"]) for row in rows),
        "classical_false_positive_count": len(false_positive_rows),
        "classical_false_negative_count": len(false_negative_rows),
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
    """Run classical validation for PGS rows."""
    args = build_parser().parse_args(argv)
    rows = validate_rows(read_csv(args.input))
    write_outputs(args.output_dir, rows)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
