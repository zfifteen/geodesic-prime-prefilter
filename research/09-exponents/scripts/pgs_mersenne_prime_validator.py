#!/usr/bin/env python3
"""Classical validation for PGSMPG v0.1 records."""

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
    / "pgs_mersenne_prime_generator_v0_1"
)
DEFAULT_INPUT = DEFAULT_OUTPUT_DIR / "records.jsonl"
KNOWN_MERSENNE_EXPONENTS = (
    2,
    3,
    5,
    7,
    13,
    17,
    19,
    31,
    61,
    89,
    107,
    127,
    521,
    607,
    1279,
    2203,
    2281,
    3217,
    4253,
    4423,
    9689,
    9941,
    11213,
    19937,
    21701,
    23209,
    44497,
    86243,
    110503,
    132049,
    216091,
    756839,
    859433,
    1257787,
    1398269,
    2976221,
    3021377,
    6972593,
    13466917,
    20996011,
    24036583,
    25964951,
    30402457,
    32582657,
    37156667,
    43112609,
    57885161,
    74207281,
    77232917,
    82589933,
    136279841,
)


VALIDATION_FIELDNAMES = [
    "p",
    "q",
    "classical_next_known_mersenne_exponent",
    "classical_q_is_known_mersenne_exponent",
    "classical_mersenne_number_is_prime",
    "classical_agreement",
]


def build_parser() -> argparse.ArgumentParser:
    """Build the validation CLI."""
    parser = argparse.ArgumentParser(description="Validate PGSMPG v0.1 records.")
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    return parser


def read_jsonl(path: Path) -> list[dict[str, int]]:
    """Read minimal JSONL records."""
    rows: list[dict[str, int]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            payload = json.loads(line)
            rows.append({"p": int(payload["p"]), "q": int(payload["q"])})
    return rows


def next_known_exponent(p: int) -> int | None:
    """Return the next listed Mersenne exponent after p."""
    for exponent in KNOWN_MERSENNE_EXPONENTS:
        if exponent > p:
            return exponent
    return None


def validation_row(record: dict[str, int]) -> dict[str, object]:
    """Return one validation row."""
    p = int(record["p"])
    q = int(record["q"])
    expected = next_known_exponent(p)
    endpoint_is_prime = bool(isprime(2**q - 1))
    return {
        "p": p,
        "q": q,
        "classical_next_known_mersenne_exponent": "" if expected is None else expected,
        "classical_q_is_known_mersenne_exponent": q in KNOWN_MERSENNE_EXPONENTS,
        "classical_mersenne_number_is_prime": endpoint_is_prime,
        "classical_agreement": q == expected and endpoint_is_prime,
    }


def validate_records(records: list[dict[str, int]]) -> list[dict[str, object]]:
    """Return validation rows."""
    return [validation_row(record) for record in records]


def summarize(rows: list[dict[str, object]]) -> dict[str, object]:
    """Return compact validation summary."""
    return {
        "validated_record_count": len(rows),
        "classical_agreement_count": sum(bool(row["classical_agreement"]) for row in rows),
        "classical_disagreement_count": sum(
            not bool(row["classical_agreement"]) for row in rows
        ),
    }


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    """Write LF-terminated validation CSV."""
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=VALIDATION_FIELDNAMES, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_outputs(output_dir: Path, rows: list[dict[str, object]]) -> None:
    """Write validation outputs."""
    output_dir.mkdir(parents=True, exist_ok=True)
    write_csv(output_dir / "validation_rows.csv", rows)
    (output_dir / "validation_summary.json").write_text(
        json.dumps(summarize(rows), indent=2) + "\n",
        encoding="utf-8",
    )


def main(argv: list[str] | None = None) -> int:
    """Run validation."""
    args = build_parser().parse_args(argv)
    rows = validate_records(read_jsonl(args.input))
    write_outputs(args.output_dir, rows)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
