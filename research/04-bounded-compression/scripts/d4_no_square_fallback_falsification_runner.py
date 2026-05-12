#!/usr/bin/env python3
"""Falsify or certify the no-square d=4 fallback lemma."""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

import gmpy2
from sympy import nextprime


ROOT = Path(__file__).resolve().parents[3]
BENCHMARK_DIR = ROOT / "research" / "02-gwr-dni" / "scripts"
if str(BENCHMARK_DIR) not in sys.path:
    sys.path.insert(0, str(BENCHMARK_DIR))

import gwr_dni_recursive_walk as walk


DEFAULT_OUTPUT_DIR = ROOT / "research" / "04-bounded-compression" / "output" / "bounded_compression"
DEFAULT_MIN_RIGHT_PRIME = 11
DEFAULT_MAX_RIGHT_PRIME = 10**6


def build_parser() -> argparse.ArgumentParser:
    """Build the CLI parser."""
    parser = argparse.ArgumentParser(
        description="Scan right-prime gaps for the first no-square d=4 fallback failure.",
    )
    parser.add_argument(
        "--min-right-prime",
        type=int,
        default=DEFAULT_MIN_RIGHT_PRIME,
        help="Smallest right prime q to test.",
    )
    parser.add_argument(
        "--max-right-prime",
        type=int,
        default=DEFAULT_MAX_RIGHT_PRIME,
        help="Largest right prime q to test.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help="Directory for JSON artifacts.",
    )
    return parser


def first_tested_right_prime(min_right_prime: int) -> int:
    """Return the first odd prime at or above the requested lower bound."""
    if min_right_prime <= 3:
        return 3
    return int(nextprime(min_right_prime - 1))


def first_d4_offset(divisor_ladder: list[int]) -> int | None:
    """Return the first interior offset whose divisor count is 4."""
    for index, divisor_count in enumerate(divisor_ladder):
        if int(divisor_count) == 4:
            return index + 1
    return None


def first_interior_prime_square(q: int, next_prime: int) -> dict[str, int | None]:
    """Return the first prime square inside one prime gap."""
    first_root = math.isqrt(q) + 1
    last_root = math.isqrt(next_prime - 1)
    for root in range(first_root, last_root + 1):
        if gmpy2.is_prime(root):
            square = root * root
            return {
                "square": square,
                "root": root,
                "offset": square - q,
            }
    return {
        "square": None,
        "root": None,
        "offset": None,
    }


def row_for_right_prime(q: int) -> dict[str, object]:
    """Return the no-square d=4 fallback comparison row for one q."""
    exact = walk.exact_next_gap_profile(q)
    next_prime = int(exact["next_prime"])
    divisor_ladder = [int(value) for value in exact["divisor_ladder"]]
    d4_offset = first_d4_offset(divisor_ladder)
    square = first_interior_prime_square(q, next_prime)
    has_interior_square = square["square"] is not None
    witness_offset = int(exact["next_peak_offset"])
    fallback_applicable = d4_offset is not None and not has_interior_square
    fallback_holds = (
        None
        if not fallback_applicable
        else witness_offset == int(d4_offset) and int(exact["next_dmin"]) == 4
    )

    return {
        "q": q,
        "next_prime": next_prime,
        "gap_width": int(exact["gap_width"]),
        "exact_witness": q + witness_offset,
        "exact_witness_offset": witness_offset,
        "exact_witness_divisor_count": int(exact["next_dmin"]),
        "first_d4_carrier": None if d4_offset is None else q + int(d4_offset),
        "first_d4_offset": d4_offset,
        "first_interior_prime_square": square["square"],
        "first_interior_prime_square_root": square["root"],
        "first_interior_prime_square_offset": square["offset"],
        "has_interior_square": has_interior_square,
        "fallback_applicable": fallback_applicable,
        "fallback_holds": fallback_holds,
    }


def run_scan(
    min_right_prime: int,
    max_right_prime: int,
) -> tuple[dict[str, object], dict[str, object] | None]:
    """Scan right-prime gaps for the first no-square d=4 fallback failure."""
    if min_right_prime < 3:
        raise ValueError("min_right_prime must be at least 3")
    if max_right_prime < min_right_prime:
        raise ValueError("max_right_prime must be at least min_right_prime")

    q = first_tested_right_prime(min_right_prime)
    tested_gap_count = 0
    first_tested_q: int | None = None
    last_tested_q: int | None = None
    no_square_d4_fallback_cases = 0
    square_present_cases = 0
    no_d4_carrier_cases = 0
    first_failure: dict[str, object] | None = None

    while q <= max_right_prime:
        row = row_for_right_prime(q)
        tested_gap_count += 1
        if first_tested_q is None:
            first_tested_q = q
        last_tested_q = q

        if bool(row["has_interior_square"]):
            square_present_cases += 1
        elif row["first_d4_offset"] is None:
            no_d4_carrier_cases += 1
        else:
            no_square_d4_fallback_cases += 1
            if not bool(row["fallback_holds"]):
                first_failure = row
                break

        q = int(nextprime(q))

    summary = {
        "min_right_prime": min_right_prime,
        "max_right_prime": max_right_prime,
        "tested_gap_count": tested_gap_count,
        "first_tested_q": first_tested_q,
        "last_tested_q": last_tested_q,
        "no_square_d4_fallback_cases": no_square_d4_fallback_cases,
        "square_present_cases": square_present_cases,
        "no_d4_carrier_cases": no_d4_carrier_cases,
        "first_failure": first_failure,
    }
    return summary, first_failure


def main(argv: list[str] | None = None) -> int:
    """Run the no-square d=4 fallback falsification scan."""
    args = build_parser().parse_args(argv)
    args.output_dir.mkdir(parents=True, exist_ok=True)

    summary, first_failure = run_scan(args.min_right_prime, args.max_right_prime)

    summary_path = args.output_dir / "d4_no_square_fallback_summary.json"
    summary_path.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")

    if first_failure is not None:
        failure_path = args.output_dir / "d4_no_square_fallback_first_failure.json"
        failure_path.write_text(json.dumps(first_failure, indent=2) + "\n", encoding="utf-8")

    print(
        "d4-no-square-fallback:"
        f" gaps={summary['tested_gap_count']}"
        f" no_square_d4_fallback_cases={summary['no_square_d4_fallback_cases']}"
        f" square_present_cases={summary['square_present_cases']}"
        f" no_d4_carrier_cases={summary['no_d4_carrier_cases']}"
        f" first_failure={'none' if first_failure is None else first_failure['q']}",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
