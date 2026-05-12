#!/usr/bin/env python3
"""Audit M-rough defects in a square-tail cutoff window."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import gmpy2
from sympy import factorint, primerange


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


def repeat_capable_cover(root: int, limit: int) -> dict[int, list[int]]:
    """Return positions covered by all repeat-capable prime carriers."""
    covered: dict[int, list[int]] = {}
    for factor in primerange(3, limit + 1):
        factor_int = int(factor)
        residue = (root * root * pow(2, -1, factor_int)) % factor_int
        first = residue if residue != 0 else factor_int
        for m in range(first, limit + 1, factor_int):
            covered.setdefault(m, []).append(factor_int)
    return covered


def rough_row(root: int, m: int) -> dict[str, object]:
    """Return the exact arithmetic row for one M-rough position."""
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


def build_rough_defect_audit(root: int) -> dict[str, object]:
    """Return the M-rough defect audit for one square-tail root."""
    payload = build_payload(root)
    limit = int(payload["full_counterexample_even_count"])
    covered = repeat_capable_cover(root, limit)
    rough_m = [m for m in range(1, limit + 1) if m not in covered]
    rows = [rough_row(root, m) for m in rough_m]
    prime_rows = [row for row in rows if bool(row["is_prime"])]
    composite_rows = [row for row in rows if not bool(row["is_prime"])]
    composite_least_factors = [
        int(row["least_factor"]) for row in composite_rows
    ]

    return {
        "root": root,
        "previous_prime_offset": payload["previous_prime_offset"],
        "dynamic_cutoff": payload["dynamic_cutoff"],
        "full_counterexample_even_count": limit,
        "repeat_capable_prime_count": len(list(primerange(3, limit + 1))),
        "repeat_capable_covered_count": len(covered),
        "rough_defect_count": len(rough_m),
        "rough_defect_offsets": [2 * m for m in rough_m],
        "rough_prime_defect_count": len(prime_rows),
        "rough_prime_defect_offsets": [int(row["offset"]) for row in prime_rows],
        "rough_composite_defect_count": len(composite_rows),
        "rough_composite_least_factors": composite_least_factors,
        "rough_composite_min_least_factor": (
            min(composite_least_factors) if composite_least_factors else None
        ),
        "all_rough_composite_least_factors_exceed_M": all(
            factor > limit for factor in composite_least_factors
        ),
        "all_rough_rows_uncovered_by_repeat_capable_carriers": all(
            m not in covered for m in rough_m
        ),
        "counterexample_equivalent_condition": (
            "all rough defect rows are composite with least factor greater than M"
        ),
        "closed_by_rough_prime_defect": bool(prime_rows),
        "rough_rows": rows,
    }


def main(argv: list[str] | None = None) -> int:
    """Run the M-rough defect audit."""
    args = build_parser().parse_args(argv)
    payload = build_rough_defect_audit(args.root)
    serialized = json.dumps(payload, indent=2)
    if args.output is not None:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(serialized + "\n", encoding="utf-8")
    print(serialized)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
