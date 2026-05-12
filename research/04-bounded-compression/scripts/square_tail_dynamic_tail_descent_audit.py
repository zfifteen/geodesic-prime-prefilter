#!/usr/bin/env python3
"""Project dynamic-tail rough rows to least-factor child squares."""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

import gmpy2
from sympy import factorint


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from square_tail_dynamic_tail_audit import build_dynamic_tail_audit  # noqa: E402


ROOT = Path(__file__).resolve().parents[3]
DEFAULT_OUTPUT_DIR = ROOT / "research" / "04-bounded-compression" / "output"


def build_parser() -> argparse.ArgumentParser:
    """Build the CLI parser."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=int, required=True, help="Root used to seed the CRT model.")
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


def child_projection_row(root: int) -> dict[str, object]:
    """Return the square-tail state for a least-factor child root."""
    square = root * root
    previous_prime = int(gmpy2.prev_prime(square))
    previous_root = int(gmpy2.prev_prime(root)) if root > 3 else 2
    offset = square - previous_prime
    cutoff = dynamic_cutoff(previous_prime)
    return {
        "root": root,
        "previous_prime_offset": offset,
        "dynamic_cutoff": cutoff,
        "cutoff_utilization": offset / cutoff,
        "closed_by_cutoff": offset <= cutoff,
        "selected_square_condition": previous_root * previous_root < previous_prime < square,
        "previous_root_gap": root - previous_root,
    }


def child_prime_parent_residue(parent_root: int, child: dict[str, object]) -> dict[str, object]:
    """Return where the child closing prime would cover the parent, if anywhere."""
    child_root = int(child["root"])
    child_u = int(child["previous_prime_offset"]) // 2
    child_prime = child_root * child_root - 2 * child_u
    residue = (parent_root * parent_root * pow(2, -1, child_prime)) % child_prime
    if residue == 0:
        residue = child_prime
    return {
        "child_prime": str(child_prime),
        "parent_residue_m": residue,
    }


def factor_tail_value(root: int, m: int, parent_m: int | None = None) -> dict[str, object]:
    """Return exact factor data for one dynamic-tail rough row."""
    value = root * root - 2 * m
    if gmpy2.is_prime(value):
        return {
            "m": m,
            "offset": 2 * m,
            "is_prime": True,
            "least_factor": None,
            "factorization": None,
            "child_projection": None,
        }

    factors = factorint(value)
    least_factor = min(int(prime) for prime in factors)
    child = child_projection_row(least_factor)
    parent_residue = child_prime_parent_residue(root, child)
    if parent_m is not None:
        parent_residue["inside_parent_M"] = int(parent_residue["parent_residue_m"]) <= parent_m
    return {
        "m": m,
        "offset": 2 * m,
        "is_prime": False,
        "least_factor": least_factor,
        "factorization": {str(int(prime)): int(power) for prime, power in factors.items()},
        "child_projection": child,
        "child_prime_parent_residue": parent_residue,
    }


def build_dynamic_tail_descent_audit(root: int) -> dict[str, object]:
    """Return exact least-factor descent data for one dynamic-tail audit."""
    tail = build_dynamic_tail_audit(root)
    actual_root = int(tail["actual_root"])
    rows = [
        factor_tail_value(actual_root, int(row["m"]), int(tail["actual_M"]))
        for row in tail["rough_or_prime_rows"]
        if bool(row["actual_rough"])
    ]
    composite_rows = [row for row in rows if not bool(row["is_prime"])]
    prime_rows = [row for row in rows if bool(row["is_prime"])]
    child_rows = [
        row["child_projection"]
        for row in composite_rows
        if row["child_projection"] is not None
    ]

    return {
        "source_root": root,
        "actual_root": tail["actual_root"],
        "actual_M": tail["actual_M"],
        "rough_tail_count": len(rows),
        "prime_rough_tail_count": len(prime_rows),
        "prime_rough_tail_offsets": [int(row["offset"]) for row in prime_rows],
        "composite_rough_tail_count": len(composite_rows),
        "composite_least_factors": [
            int(row["least_factor"]) for row in composite_rows
        ],
        "child_projection_count": len(child_rows),
        "child_projection_closed_count": sum(
            int(bool(row["closed_by_cutoff"])) for row in child_rows
        ),
        "child_projection_selected_square_count": sum(
            int(bool(row["selected_square_condition"])) for row in child_rows
        ),
        "child_prime_parent_residue_inside_M_count": sum(
            int(
                bool(
                    row["child_prime_parent_residue"]
                    and row["child_prime_parent_residue"].get("inside_parent_M")
                )
            )
            for row in composite_rows
        ),
        "rough_tail_rows": rows,
    }


def main(argv: list[str] | None = None) -> int:
    """Run the dynamic-tail descent audit."""
    args = build_parser().parse_args(argv)
    payload = build_dynamic_tail_descent_audit(args.root)
    serialized = json.dumps(payload, indent=2)
    if args.output is not None:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(serialized + "\n", encoding="utf-8")
    print(serialized)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
