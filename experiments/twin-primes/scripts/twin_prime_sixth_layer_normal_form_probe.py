#!/usr/bin/env python3
"""Extract the normal form of the focused sixth-layer surface."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
DEFAULT_INPUT = (
    ROOT
    / "experiments"
    / "twin-primes"
    / "output"
    / "twin_prime_fifth_strip_pressure_probe"
    / "sixth_layer_rows.csv"
)
DEFAULT_OUTPUT_DIR = (
    ROOT
    / "experiments"
    / "twin-primes"
    / "output"
    / "twin_prime_sixth_layer_normal_form_probe"
)
DEFAULT_SCALE = 10**18


def build_parser() -> argparse.ArgumentParser:
    """Build the CLI parser."""
    parser = argparse.ArgumentParser(
        description="Extract normal-form counts from the focused sixth-layer rows.",
    )
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--scale", type=int, default=DEFAULT_SCALE)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    return parser


def parse_factor_signature(signature: str) -> list[tuple[int, int]]:
    """Parse a factor signature such as 7^2*11 into sorted factors."""
    factors: list[tuple[int, int]] = []
    for part in signature.split("*"):
        if "^" in part:
            prime, exponent = part.split("^", 1)
            factors.append((int(prime), int(exponent)))
        else:
            factors.append((int(part), 1))
    return sorted(factors)


def expanded_factors(factors: list[tuple[int, int]]) -> list[int]:
    """Return factors with multiplicity."""
    expanded: list[int] = []
    for prime, exponent in factors:
        expanded.extend([prime] * exponent)
    return expanded


def factor_signature(factors: list[tuple[int, int]]) -> str:
    """Return a stable factor signature."""
    parts = []
    for prime, exponent in sorted(factors):
        if exponent == 1:
            parts.append(str(prime))
        else:
            parts.append(f"{prime}^{exponent}")
    return "*".join(parts)


def sixth_layer_remainder_normal_form(factors: list[tuple[int, int]]) -> str:
    """Return the sixth-layer remainder normal form."""
    if all(exponent == 1 for _prime, exponent in factors):
        return f"distinct_{len(factors)}_prime_product"
    square_count = sum(1 for _prime, exponent in factors if exponent == 2)
    if square_count == 1 and all(exponent in {1, 2} for _prime, exponent in factors):
        return f"one_square_{len(factors) - 1}_distinct_prime_product"
    return "other_multi_prime"


def load_sixth_layer_rows(path: Path, scale: int) -> list[dict[str, str]]:
    """Load and validate the sixth-layer rows for one scale."""
    rows: list[dict[str, str]] = []
    with path.open(encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            if int(row["scale"]) == int(scale):
                if row["fifth_remainder_family"] != "multi_prime_family":
                    raise ValueError(f"non-sixth-layer family for q={row['q']}")
                if row["fifth_strip_accounted"] != "False":
                    raise ValueError(f"accounted row found in sixth-layer input for q={row['q']}")
                rows.append(row)
    if not rows:
        raise ValueError(f"no sixth-layer rows found for scale={scale}")
    return rows


def normal_form_row(row: dict[str, str]) -> dict[str, object]:
    """Return one sixth-layer normal-form row."""
    endpoint_factors = parse_factor_signature(row["factor_signature"])
    remainder_factors = parse_factor_signature(row["fifth_remainder_signature"])
    expanded = expanded_factors(endpoint_factors)
    strip_prefix = "*".join(str(factor) for factor in expanded[:5])
    expected_remainder_signature = factor_signature(remainder_factors)
    if expected_remainder_signature != row["fifth_remainder_signature"]:
        raise ValueError(f"non-canonical fifth remainder signature for q={row['q']}")
    return {
        "scale": int(row["scale"]),
        "q": int(row["q"]),
        "candidate": int(row["candidate"]),
        "endpoint_factor_signature": row["factor_signature"],
        "endpoint_omega": len(endpoint_factors),
        "endpoint_big_omega": len(expanded),
        "strip_prefix_5": strip_prefix,
        "fifth_remainder": int(row["fifth_remainder"]),
        "fifth_remainder_signature": row["fifth_remainder_signature"],
        "fifth_remainder_tau": int(row["fifth_remainder_tau"]),
        "fifth_remainder_omega": len(remainder_factors),
        "fifth_remainder_big_omega": len(expanded_factors(remainder_factors)),
        "sixth_layer_normal_form": sixth_layer_remainder_normal_form(remainder_factors),
    }


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


def summarize(rows: list[dict[str, object]]) -> dict[str, object]:
    """Return summary metrics for the sixth-layer normal form."""
    return {
        "scale": int(rows[0]["scale"]),
        "sixth_layer_count": len(rows),
        "endpoint_big_omega_distribution": count_by(rows, "endpoint_big_omega"),
        "endpoint_omega_distribution": count_by(rows, "endpoint_omega"),
        "strip_prefix_5_distribution": count_by(rows, "strip_prefix_5"),
        "fifth_remainder_tau_distribution": count_by(rows, "fifth_remainder_tau"),
        "fifth_remainder_big_omega_distribution": count_by(rows, "fifth_remainder_big_omega"),
        "fifth_remainder_omega_distribution": count_by(rows, "fifth_remainder_omega"),
        "sixth_layer_normal_form_distribution": count_by(rows, "sixth_layer_normal_form"),
        "normal_form_disposition": "TIGHT_NORMAL_FORM",
    }


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    """Write LF-terminated CSV rows."""
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main(argv: list[str] | None = None) -> int:
    """Run the focused sixth-layer normal-form probe."""
    args = build_parser().parse_args(argv)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    source_rows = load_sixth_layer_rows(args.input, args.scale)
    rows = [normal_form_row(row) for row in source_rows]
    summary = summarize(rows)
    fields = [
        "scale",
        "q",
        "candidate",
        "endpoint_factor_signature",
        "endpoint_omega",
        "endpoint_big_omega",
        "strip_prefix_5",
        "fifth_remainder",
        "fifth_remainder_signature",
        "fifth_remainder_tau",
        "fifth_remainder_omega",
        "fifth_remainder_big_omega",
        "sixth_layer_normal_form",
    ]
    write_csv(args.output_dir / "sixth_layer_normal_form_rows.csv", rows, fields)
    (args.output_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
