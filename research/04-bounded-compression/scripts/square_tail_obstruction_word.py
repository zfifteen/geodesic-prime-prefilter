#!/usr/bin/env python3
"""Emit the square-tail obstruction word for one prime-square root."""

from __future__ import annotations

import argparse
import json
import math
from collections import Counter
from pathlib import Path

import gmpy2
from sympy import factorint


ROOT = Path(__file__).resolve().parents[3]
DEFAULT_OUTPUT_DIR = ROOT / "research" / "04-bounded-compression" / "output"


def build_parser() -> argparse.ArgumentParser:
    """Build the CLI parser."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=int, required=True, help="Prime root r of r^2.")
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Optional JSON output path.",
    )
    return parser


def dynamic_cutoff(left_prime: int) -> int:
    """Return C(q)=max(64, ceil(0.5 log(q)^2))."""
    return max(64, math.ceil(0.5 * (math.log(left_prime) ** 2)))


def least_factor_row(root: int, offset: int) -> dict[str, int]:
    """Return one least-factor obstruction row for r^2-offset."""
    square = root * root
    value = square - offset
    factors = factorint(value)
    least_factor = min(int(prime) for prime in factors)
    return {
        "offset": offset,
        "m": offset // 2,
        "value": value,
        "least_factor": least_factor,
        "cofactor": value // least_factor,
        "least_factor_exponent": int(factors[least_factor]),
        "root_mod_least_factor": root % least_factor,
    }


def child_projection_row(root: int) -> dict[str, int | float | bool]:
    """Return the square-tail state for one smaller prime root."""
    square = root * root
    previous_prime = int(gmpy2.prev_prime(square))
    previous_root = int(gmpy2.prev_prime(root)) if root > 3 else 2
    offset = square - previous_prime
    cutoff = dynamic_cutoff(previous_prime)
    prefix_limit = min(offset - 2, cutoff)
    return {
        "root": root,
        "square": square,
        "previous_prime": previous_prime,
        "previous_prime_offset": offset,
        "dynamic_cutoff": cutoff,
        "cutoff_utilization": offset / cutoff,
        "closed_by_cutoff": offset <= cutoff,
        "selected_square_condition": (previous_root * previous_root) < previous_prime < square,
        "obstruction_prefix_even_count": max(0, prefix_limit // 2),
    }


def build_payload(root: int) -> dict[str, object]:
    """Return the square-tail obstruction-word payload."""
    if root < 3 or not gmpy2.is_prime(root):
        raise ValueError("root must be an odd prime")

    square = root * root
    previous_prime = int(gmpy2.prev_prime(square))
    previous_root = int(gmpy2.prev_prime(root))
    offset = square - previous_prime
    cutoff = dynamic_cutoff(previous_prime)
    prefix_limit = min(offset - 2, cutoff)

    rows = []
    for candidate_offset in range(2, prefix_limit + 1, 2):
        value = square - candidate_offset
        if gmpy2.is_prime(value):
            raise RuntimeError("obstruction prefix reached a prime before previous_prime")
        rows.append(least_factor_row(root, candidate_offset))

    least_factor_counts = Counter(int(row["least_factor"]) for row in rows)
    top_least_factors = [
        {
            "least_factor": factor,
            "count": count,
            "first_offset": next(
                int(row["offset"]) for row in rows if int(row["least_factor"]) == factor
            ),
        }
        for factor, count in least_factor_counts.most_common(20)
    ]
    max_least_factor_row = max(rows, key=lambda row: int(row["least_factor"])) if rows else None
    child_rows = [
        child_projection_row(factor)
        for factor in sorted(least_factor_counts)
    ]
    child_closed_count = sum(int(bool(row["closed_by_cutoff"])) for row in child_rows)
    child_selected_count = sum(
        int(bool(row["selected_square_condition"])) for row in child_rows
    )
    max_child_utilization_row = (
        max(child_rows, key=lambda row: float(row["cutoff_utilization"]))
        if child_rows
        else None
    )

    full_counterexample_even_count = cutoff // 2
    obstruction_prefix_even_count = len(rows)
    return {
        "root": root,
        "square": square,
        "previous_prime": previous_prime,
        "previous_prime_offset": offset,
        "dynamic_cutoff": cutoff,
        "closed_by_cutoff": offset <= cutoff,
        "previous_root": previous_root,
        "previous_root_square": previous_root * previous_root,
        "selected_square_condition": (previous_root * previous_root) < previous_prime < square,
        "full_counterexample_even_count": full_counterexample_even_count,
        "obstruction_prefix_even_count": obstruction_prefix_even_count,
        "prefix_fraction_of_counterexample_word": (
            obstruction_prefix_even_count / full_counterexample_even_count
            if full_counterexample_even_count
            else None
        ),
        "distinct_least_factor_count": len(least_factor_counts),
        "top_least_factors": top_least_factors,
        "max_least_factor_row": max_least_factor_row,
        "child_projection_count": len(child_rows),
        "child_projection_closed_count": child_closed_count,
        "child_projection_selected_square_count": child_selected_count,
        "max_child_projection_utilization_row": max_child_utilization_row,
        "child_projection_rows": child_rows,
        "obstruction_rows": rows,
    }


def main(argv: list[str] | None = None) -> int:
    """Run the obstruction-word emitter."""
    args = build_parser().parse_args(argv)
    payload = build_payload(args.root)
    serialized = json.dumps(payload, indent=2)
    if args.output is not None:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(serialized + "\n", encoding="utf-8")
    print(serialized)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
