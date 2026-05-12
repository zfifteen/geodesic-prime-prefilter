#!/usr/bin/env python3
"""Pressure-test the sixth factor strip on the focused nine-row surface."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
DEFAULT_INPUT = (
    ROOT
    / "research"
    / "10-twin-primes"
    / "output"
    / "twin_prime_sixth_layer_normal_form_probe"
    / "sixth_layer_normal_form_rows.csv"
)
DEFAULT_OUTPUT_DIR = (
    ROOT
    / "research"
    / "10-twin-primes"
    / "output"
    / "twin_prime_sixth_strip_pressure_probe"
)
DEFAULT_SCALE = 10**18
LOW_COMPLEXITY_REMAINDER_FAMILIES = frozenset({"fixed_point", "semiprime_distinct"})
PRIME_POWER_TAIL_FAMILIES = frozenset(
    {"prime_square", "prime_cube", "prime_power", "two_prime_power_family"}
)
SIXTH_LAYER_NORMAL_FORMS = frozenset(
    {
        "distinct_3_prime_product",
        "distinct_4_prime_product",
        "one_square_3_distinct_prime_product",
    }
)


def build_parser() -> argparse.ArgumentParser:
    """Build the CLI parser."""
    parser = argparse.ArgumentParser(
        description="Run sixth-strip pressure on the focused nine-row surface.",
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


def factor_signature(factors: list[tuple[int, int]]) -> str:
    """Return a stable factor signature."""
    parts = []
    for prime, exponent in sorted(factors):
        if exponent == 1:
            parts.append(str(prime))
        else:
            parts.append(f"{prime}^{exponent}")
    return "*".join(parts)


def tau_from_factors(factors: list[tuple[int, int]]) -> int:
    """Return divisor count from one factorization."""
    tau = 1
    for _prime, exponent in factors:
        tau *= exponent + 1
    return tau


def decrement_least_factor(factors: list[tuple[int, int]]) -> tuple[int, list[tuple[int, int]]]:
    """Remove one copy of the least factor."""
    least_prime, exponent = factors[0]
    remainder: list[tuple[int, int]] = []
    if exponent > 1:
        remainder.append((least_prime, exponent - 1))
    remainder.extend(factors[1:])
    return least_prime, remainder


def endpoint_family(factors: list[tuple[int, int]], tau_n: int) -> str:
    """Return the factor family relative to the fixed-point locus."""
    if tau_n == 2:
        return "fixed_point"
    if len(factors) == 1:
        exponent = factors[0][1]
        if exponent == 2:
            return "prime_square"
        if exponent == 3:
            return "prime_cube"
        return "prime_power"
    if len(factors) == 2 and all(exponent == 1 for _prime, exponent in factors):
        return "semiprime_distinct"
    if len(factors) == 2:
        return "two_prime_power_family"
    return "multi_prime_family"


def is_prime_power_tail(family: str) -> bool:
    """Return whether the family is prime-power tail material."""
    return family in PRIME_POWER_TAIL_FAMILIES


def sixth_strip_terminal(sixth_remainder_family: str) -> str:
    """Return the terminal class after the sixth strip."""
    if sixth_remainder_family in LOW_COMPLEXITY_REMAINDER_FAMILIES:
        return f"sixth_strip_{sixth_remainder_family}"
    if is_prime_power_tail(sixth_remainder_family):
        return f"sixth_strip_prime_power_tail_{sixth_remainder_family}"
    return "seventh_layer_multi_prime"


def is_sixth_strip_accounted(sixth_remainder_family: str) -> bool:
    """Return whether the sixth strip reaches the known terminal grammar."""
    return (
        sixth_remainder_family in LOW_COMPLEXITY_REMAINDER_FAMILIES
        or is_prime_power_tail(sixth_remainder_family)
    )


def load_normal_form_rows(path: Path, scale: int) -> list[dict[str, str]]:
    """Load and validate the nine-row normal-form surface."""
    rows: list[dict[str, str]] = []
    with path.open(encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            if int(row["scale"]) == int(scale):
                if row["sixth_layer_normal_form"] not in SIXTH_LAYER_NORMAL_FORMS:
                    raise ValueError(f"unexpected sixth-layer normal form for q={row['q']}")
                factors = parse_factor_signature(row["fifth_remainder_signature"])
                if factor_signature(factors) != row["fifth_remainder_signature"]:
                    raise ValueError(f"non-canonical fifth remainder signature for q={row['q']}")
                rows.append(row)
    if not rows:
        raise ValueError(f"no sixth-layer normal-form rows found for scale={scale}")
    return rows


def sixth_strip_row(row: dict[str, str]) -> dict[str, object]:
    """Return one sixth-strip decomposition row."""
    fifth_remainder = int(row["fifth_remainder"])
    factors = parse_factor_signature(row["fifth_remainder_signature"])
    sixth_factor, sixth_remainder_factors = decrement_least_factor(factors)
    sixth_remainder = fifth_remainder // sixth_factor
    sixth_remainder_tau = tau_from_factors(sixth_remainder_factors)
    sixth_remainder_family = endpoint_family(sixth_remainder_factors, sixth_remainder_tau)
    terminal = sixth_strip_terminal(sixth_remainder_family)
    accounted = is_sixth_strip_accounted(sixth_remainder_family)
    return {
        "scale": int(row["scale"]),
        "q": int(row["q"]),
        "candidate": int(row["candidate"]),
        "sixth_layer_normal_form": row["sixth_layer_normal_form"],
        "fifth_remainder": fifth_remainder,
        "fifth_remainder_signature": row["fifth_remainder_signature"],
        "sixth_factor": sixth_factor,
        "sixth_remainder": sixth_remainder,
        "sixth_remainder_tau": sixth_remainder_tau,
        "sixth_remainder_family": sixth_remainder_family,
        "sixth_remainder_signature": factor_signature(sixth_remainder_factors),
        "sixth_strip_terminal": terminal,
        "sixth_strip_accounted": accounted,
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
    """Return summary metrics for sixth-strip pressure."""
    accounted = [row for row in rows if bool(row["sixth_strip_accounted"])]
    seventh_layer = [row for row in rows if not bool(row["sixth_strip_accounted"])]
    low_complexity = [
        row
        for row in rows
        if row["sixth_remainder_family"] in LOW_COMPLEXITY_REMAINDER_FAMILIES
    ]
    prime_power_tail = [
        row for row in rows if is_prime_power_tail(str(row["sixth_remainder_family"]))
    ]
    return {
        "scale": int(rows[0]["scale"]),
        "input_sixth_layer_count": len(rows),
        "sixth_strip_low_complexity_count": len(low_complexity),
        "sixth_strip_prime_power_tail_count": len(prime_power_tail),
        "sixth_strip_accounted_count": len(accounted),
        "seventh_layer_count": len(seventh_layer),
        "sixth_strip_compression_rate": len(accounted) / len(rows),
        "sixth_remainder_family_distribution": count_by(rows, "sixth_remainder_family"),
        "sixth_strip_terminal_distribution": count_by(rows, "sixth_strip_terminal"),
        "seventh_layer_family_distribution": count_by(seventh_layer, "sixth_remainder_family"),
        "grammar_disposition": "CLOSED" if not seventh_layer else "SEVENTH_LAYER_FOUND",
    }


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    """Write LF-terminated CSV rows."""
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main(argv: list[str] | None = None) -> int:
    """Run the focused sixth-strip probe."""
    args = build_parser().parse_args(argv)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    source_rows = load_normal_form_rows(args.input, args.scale)
    rows = [sixth_strip_row(row) for row in source_rows]
    summary = summarize(rows)
    fields = [
        "scale",
        "q",
        "candidate",
        "sixth_layer_normal_form",
        "fifth_remainder",
        "fifth_remainder_signature",
        "sixth_factor",
        "sixth_remainder",
        "sixth_remainder_tau",
        "sixth_remainder_family",
        "sixth_remainder_signature",
        "sixth_strip_terminal",
        "sixth_strip_accounted",
    ]
    seventh_layer_rows = [row for row in rows if not bool(row["sixth_strip_accounted"])]
    write_csv(args.output_dir / "sixth_strip_rows.csv", rows, fields)
    write_csv(args.output_dir / "seventh_layer_rows.csv", seventh_layer_rows, fields)
    (args.output_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
