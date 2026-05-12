#!/usr/bin/env python3
"""Falsify or certify one finite surface for the bounded GWR/DNI cutoff."""

from __future__ import annotations

import argparse
import csv
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
FRONTIER_FIELDS = [
    "q",
    "next_prime",
    "gap_width",
    "witness",
    "witness_offset",
    "witness_divisor_count",
    "cutoff",
    "cutoff_utilization",
    "first_interior_prime_square",
    "first_interior_prime_square_root",
    "first_interior_prime_square_offset",
    "selected_witness_is_prime_square",
    "square_offset_minus_witness_offset",
]


def build_parser() -> argparse.ArgumentParser:
    """Build the CLI parser."""
    parser = argparse.ArgumentParser(
        description="Compare exact unbounded GWR/DNI witnesses against the dynamic cutoff.",
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
        help="Directory for JSON and CSV artifacts.",
    )
    return parser


def first_tested_right_prime(min_right_prime: int) -> int:
    """Return the first odd prime at or above the requested lower bound."""
    if min_right_prime <= 3:
        return 3
    return int(nextprime(min_right_prime - 1))


def first_interior_prime_square(q: int, next_prime: int) -> dict[str, int | None]:
    """Return the first prime-square obstruction inside one prime gap."""
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
    """Return the exact bounded-compression comparison row for one q."""
    exact = walk.exact_next_gap_profile(q)
    next_prime = int(exact["next_prime"])
    witness_offset = int(exact["next_peak_offset"])
    witness = q + witness_offset
    cutoff = walk.dynamic_cutoff(q)
    square = first_interior_prime_square(q, next_prime)
    square_offset = square["offset"]
    selected_witness_is_prime_square = square_offset == witness_offset

    return {
        "q": q,
        "next_prime": next_prime,
        "gap_width": int(exact["gap_width"]),
        "witness": witness,
        "witness_offset": witness_offset,
        "witness_divisor_count": int(exact["next_dmin"]),
        "cutoff": cutoff,
        "cutoff_utilization": witness_offset / cutoff,
        "first_interior_prime_square": square["square"],
        "first_interior_prime_square_root": square["root"],
        "first_interior_prime_square_offset": square_offset,
        "selected_witness_is_prime_square": selected_witness_is_prime_square,
        "square_offset_minus_witness_offset": (
            None if square_offset is None else int(square_offset) - witness_offset
        ),
    }


def run_scan(
    min_right_prime: int,
    max_right_prime: int,
) -> tuple[list[dict[str, object]], dict[str, object], dict[str, object] | None]:
    """Scan right primes until the first dynamic-cutoff failure or range end."""
    if min_right_prime < 3:
        raise ValueError("min_right_prime must be at least 3")
    if max_right_prime < min_right_prime:
        raise ValueError("max_right_prime must be at least min_right_prime")

    q = first_tested_right_prime(min_right_prime)
    frontier_rows: list[dict[str, object]] = []
    first_failure: dict[str, object] | None = None
    tested_gap_count = 0
    first_tested_q: int | None = None
    last_tested_q: int | None = None
    max_witness_offset = 0
    max_cutoff_utilization = 0.0
    extremal_q: int | None = None
    extremal_row: dict[str, object] | None = None

    while q <= max_right_prime:
        row = row_for_right_prime(q)
        tested_gap_count += 1
        if first_tested_q is None:
            first_tested_q = q
        last_tested_q = q

        witness_offset = int(row["witness_offset"])
        cutoff_utilization = float(row["cutoff_utilization"])
        if witness_offset > max_witness_offset:
            max_witness_offset = witness_offset
        if cutoff_utilization > max_cutoff_utilization:
            max_cutoff_utilization = cutoff_utilization
            extremal_q = q
            extremal_row = row
            frontier_rows.append(row)

        if witness_offset > int(row["cutoff"]):
            first_failure = row
            break

        q = int(nextprime(q))

    summary = {
        "min_right_prime": min_right_prime,
        "max_right_prime": max_right_prime,
        "tested_gap_count": tested_gap_count,
        "first_tested_q": first_tested_q,
        "last_tested_q": last_tested_q,
        "first_failure": first_failure,
        "max_witness_offset": max_witness_offset,
        "max_cutoff_utilization": max_cutoff_utilization,
        "extremal_q": extremal_q,
        "extremal_row": extremal_row,
    }
    return frontier_rows, summary, first_failure


def write_frontier_csv(path: Path, rows: list[dict[str, object]]) -> None:
    """Write the extremal frontier as an LF-terminated CSV."""
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FRONTIER_FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main(argv: list[str] | None = None) -> int:
    """Run the bounded-compression falsification scan."""
    args = build_parser().parse_args(argv)
    args.output_dir.mkdir(parents=True, exist_ok=True)

    frontier_rows, summary, first_failure = run_scan(
        args.min_right_prime,
        args.max_right_prime,
    )

    summary_path = args.output_dir / "bounded_compression_falsification_summary.json"
    frontier_path = args.output_dir / "bounded_compression_falsification_frontier.csv"
    summary_path.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    write_frontier_csv(frontier_path, frontier_rows)

    if first_failure is not None:
        failure_path = args.output_dir / "bounded_compression_first_failure.json"
        failure_path.write_text(json.dumps(first_failure, indent=2) + "\n", encoding="utf-8")

    print(
        "bounded-compression-falsification:"
        f" gaps={summary['tested_gap_count']}"
        f" first_failure={'none' if first_failure is None else first_failure['q']}"
        f" max_witness_offset={summary['max_witness_offset']}"
        f" max_cutoff_utilization={summary['max_cutoff_utilization']}"
        f" extremal_q={summary['extremal_q']}",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
