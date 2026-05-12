#!/usr/bin/env python3
"""Audit the moving residue cover induced by a square-tail obstruction prefix."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import gmpy2
from sympy import factorint


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from square_tail_obstruction_word import build_payload  # noqa: E402


ROOT = Path(__file__).resolve().parents[3]
DEFAULT_OUTPUT_DIR = ROOT / "research" / "04-bounded-compression" / "output"


def build_parser() -> argparse.ArgumentParser:
    """Build the CLI parser."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=int, required=True, help="Parent prime root.")
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Optional JSON output path.",
    )
    return parser


def residue_for_root(root: int, factor: int) -> int:
    """Return the m-residue where factor divides root^2 - 2m."""
    return (root * root * pow(2, -1, factor)) % factor


def covered_positions(root: int, factors: list[int], limit: int) -> dict[int, list[int]]:
    """Return m positions covered by the observed prefix factor classes."""
    covered: dict[int, list[int]] = {}
    for factor in factors:
        residue = residue_for_root(root, factor)
        first = residue if residue != 0 else factor
        for m in range(first, limit + 1, factor):
            covered.setdefault(m, []).append(factor)
    return covered


def uncovered_row(root: int, m: int) -> dict[str, object]:
    """Return the exact arithmetic row for one uncovered m-position."""
    value = root * root - 2 * m
    if gmpy2.is_prime(value):
        return {
            "m": m,
            "offset": 2 * m,
            "value": value,
            "is_prime": True,
            "least_factor": None,
            "factorization": None,
        }

    factors = factorint(value)
    least_factor = min(int(prime) for prime in factors)
    return {
        "m": m,
        "offset": 2 * m,
        "value": value,
        "is_prime": False,
        "least_factor": least_factor,
        "factorization": {str(int(prime)): int(power) for prime, power in factors.items()},
    }


def build_cover_audit(root: int) -> dict[str, object]:
    """Return the moving-cover audit for one square-tail root."""
    payload = build_payload(root)
    rows = list(payload["obstruction_rows"])
    prefix_factors = sorted({int(row["least_factor"]) for row in rows})
    full_count = int(payload["full_counterexample_even_count"])
    covered = covered_positions(root, prefix_factors, full_count)
    uncovered = [m for m in range(1, full_count + 1) if m not in covered]
    uncovered_rows = [uncovered_row(root, m) for m in uncovered]
    actual_previous_prime_m = int(payload["previous_prime_offset"]) // 2
    uncovered_prime_rows = [row for row in uncovered_rows if bool(row["is_prime"])]
    uncovered_composite_rows = [
        row for row in uncovered_rows if not bool(row["is_prime"])
    ]
    composite_defect_factors = [
        int(row["least_factor"]) for row in uncovered_composite_rows
    ]
    completed_factor_set = sorted(set(prefix_factors + composite_defect_factors))
    completed_cover = covered_positions(root, completed_factor_set, full_count)
    remaining_uncovered = [
        m for m in range(1, full_count + 1) if m not in completed_cover
    ]

    return {
        "root": root,
        "previous_prime_offset": payload["previous_prime_offset"],
        "dynamic_cutoff": payload["dynamic_cutoff"],
        "full_counterexample_even_count": full_count,
        "obstruction_prefix_even_count": payload["obstruction_prefix_even_count"],
        "prefix_factor_count": len(prefix_factors),
        "prefix_factors": prefix_factors,
        "covered_by_prefix_factor_count": len(covered),
        "uncovered_by_prefix_factor_count": len(uncovered),
        "uncovered_m": uncovered,
        "uncovered_offsets": [2 * m for m in uncovered],
        "actual_previous_prime_m": actual_previous_prime_m,
        "actual_previous_prime_uncovered_by_prefix_factors": (
            actual_previous_prime_m in uncovered
        ),
        "uncovered_prime_count": len(uncovered_prime_rows),
        "uncovered_prime_offsets": [
            int(row["offset"]) for row in uncovered_prime_rows
        ],
        "uncovered_composite_count": len(uncovered_composite_rows),
        "uncovered_composite_least_factors": composite_defect_factors,
        "completed_factor_count": len(completed_factor_set),
        "covered_after_composite_defect_factors_count": len(completed_cover),
        "remaining_uncovered_after_composite_defect_factors_m": remaining_uncovered,
        "remaining_uncovered_after_composite_defect_factors_offsets": [
            2 * m for m in remaining_uncovered
        ],
        "uncovered_rows": uncovered_rows,
    }


def main(argv: list[str] | None = None) -> int:
    """Run the moving-cover audit."""
    args = build_parser().parse_args(argv)
    payload = build_cover_audit(args.root)
    serialized = json.dumps(payload, indent=2)
    if args.output is not None:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(serialized + "\n", encoding="utf-8")
    print(serialized)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
