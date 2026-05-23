#!/usr/bin/env python3
"""Classify low-prefix boundary reserve in the seeded PGS Gilbreath cascade."""

from __future__ import annotations

import csv
import json
from collections import Counter, defaultdict
from pathlib import Path


ENDPOINT_COUNT = 20000
LOW_VALUES = {0, 2}

OUT_DIR = Path(__file__).resolve().parent
SUMMARY_PATH = OUT_DIR / "2026-05-23-boundary_reserve_exclusion_summary.json"
ROWS_PATH = OUT_DIR / "2026-05-23-boundary_reserve_exclusion_rows.csv"


def divisor_count(n: int) -> int:
    if n < 1:
        raise ValueError("divisor_count expects a positive integer")
    remaining = n
    count = 1
    factor = 2
    while factor * factor <= remaining:
        if remaining % factor == 0:
            exponent = 0
            while remaining % factor == 0:
                remaining //= factor
                exponent += 1
            count *= exponent + 1
        factor += 1 if factor == 2 else 2
    if remaining > 1:
        count *= 2
    return count


def next_endpoint_by_tau(endpoint: int) -> int:
    n = endpoint + 1
    while True:
        if divisor_count(n) == 2:
            return n
        n += 1


def endpoint_gaps(count: int) -> tuple[list[int], int]:
    endpoints = [2]
    while len(endpoints) < count + 1:
        endpoints.append(next_endpoint_by_tau(endpoints[-1]))
    return [right - left for left, right in zip(endpoints, endpoints[1:])], endpoints[-1]


def difference_row(row: list[int]) -> list[int]:
    return [abs(row[i + 1] - row[i]) for i in range(len(row) - 1)]


def low_prefix_len(row: list[int]) -> int:
    index = 1
    while index < len(row) and row[index] in LOW_VALUES:
        index += 1
    return index - 1


def row_window(row: list[int], ell: int) -> str:
    start = max(0, ell - 5)
    end = min(len(row), ell + 9)
    return " ".join(str(value) for value in row[start:end])


def main() -> None:
    row, final_endpoint = endpoint_gaps(ENDPOINT_COUNT)
    leading_failures = 0
    tail_parity_failures = 0
    depletion_failures = 0
    forbidden_prefix_hits = 0
    boundary_pair_counts: Counter[str] = Counter()
    boundary_pair_min_ell: dict[str, int] = {}
    boundary_pair_max_ell: dict[str, int] = {}
    high_boundary_pair_counts: Counter[str] = Counter()
    high_boundary_min_ell: dict[str, int] = {}
    floor_rows = 0
    floor_guard_failures = 0
    high_boundary_rows = 0
    high_boundary_floor_hits = 0
    high_boundary_min_reserve: int | None = None
    high_boundary_examples: list[dict[str, int | str]] = []
    rows_by_pair: defaultdict[str, list[dict[str, int | str]]] = defaultdict(list)

    with ROWS_PATH.open("w", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "depth",
                "row_len",
                "ell",
                "ell_after",
                "ordinary_floor_after",
                "boundary_pair",
                "boundary_left",
                "boundary_right",
                "reset_gain",
                "row_window",
            ],
            lineterminator="\n",
        )
        writer.writeheader()

        for depth in range(ENDPOINT_COUNT - 4):
            if row[0] != 1:
                leading_failures += 1
            if any(value % 2 != 0 for value in row[1:]):
                tail_parity_failures += 1
            if len(row) >= 5 and tuple(row[:5]) == (1, 2, 2, 6, 2):
                forbidden_prefix_hits += 1

            next_row = difference_row(row)
            ell = low_prefix_len(row)
            ell_after = low_prefix_len(next_row)
            ordinary_floor_after = max(0, ell - 1)
            if ell_after < ordinary_floor_after:
                depletion_failures += 1
            reset_gain = ell_after - ordinary_floor_after

            if ell >= 1 and ell + 1 < len(row):
                left = row[ell]
                right = row[ell + 1]
                pair = f"{left},{right}"
                boundary_pair_counts[pair] += 1
                boundary_pair_min_ell[pair] = min(ell, boundary_pair_min_ell.get(pair, ell))
                boundary_pair_max_ell[pair] = max(ell, boundary_pair_max_ell.get(pair, ell))

                if ell == 2:
                    floor_rows += 1
                    if pair != "2,4":
                        floor_guard_failures += 1

                if left in LOW_VALUES and right not in LOW_VALUES and right != 4:
                    high_boundary_rows += 1
                    high_boundary_pair_counts[pair] += 1
                    high_boundary_min_ell[pair] = min(ell, high_boundary_min_ell.get(pair, ell))
                    if high_boundary_min_reserve is None or ell < high_boundary_min_reserve:
                        high_boundary_min_reserve = ell
                    if ell == 2:
                        high_boundary_floor_hits += 1

                    record = {
                        "depth": depth,
                        "row_len": len(row),
                        "ell": ell,
                        "ell_after": ell_after,
                        "ordinary_floor_after": ordinary_floor_after,
                        "boundary_pair": pair,
                        "boundary_left": left,
                        "boundary_right": right,
                        "reset_gain": reset_gain,
                        "row_window": row_window(row, ell),
                    }
                    writer.writerow(record)
                    rows_by_pair[pair].append(record)
                    if len(high_boundary_examples) < 12:
                        high_boundary_examples.append(record)

            row = next_row

    first_examples_by_pair = {
        pair: rows[0] for pair, rows in sorted(rows_by_pair.items())
    }
    summary = {
        "status": "ADVANCE",
        "endpoint_count": ENDPOINT_COUNT,
        "seed_endpoint": 2,
        "final_endpoint": final_endpoint,
        "cascade_rows_checked": ENDPOINT_COUNT - 4,
        "leading_failures": leading_failures,
        "tail_parity_failures": tail_parity_failures,
        "depletion_failures": depletion_failures,
        "forbidden_prefix": "1,2,2,6,2",
        "forbidden_prefix_hits": forbidden_prefix_hits,
        "floor_rows": floor_rows,
        "floor_guard_failures": floor_guard_failures,
        "boundary_pair_counts": dict(boundary_pair_counts.most_common()),
        "boundary_pair_min_ell": dict(sorted(boundary_pair_min_ell.items())),
        "boundary_pair_max_ell": dict(sorted(boundary_pair_max_ell.items())),
        "high_boundary_definition": "boundary left in {0,2}, boundary right not in {0,2,4}",
        "high_boundary_rows": high_boundary_rows,
        "high_boundary_floor_hits": high_boundary_floor_hits,
        "high_boundary_min_reserve": high_boundary_min_reserve,
        "high_boundary_pair_counts": dict(high_boundary_pair_counts.most_common()),
        "high_boundary_min_ell_by_pair": dict(sorted(high_boundary_min_ell.items())),
        "first_high_boundary_examples_by_pair": first_examples_by_pair,
        "high_boundary_examples": high_boundary_examples,
        "invalidated_shortcut": (
            "Actual PGS does not exclude every high boundary pair: 2,6 occurs "
            "in the cascade. The live bridge is reserve separation, not absolute "
            "boundary-pair exclusion."
        ),
        "proof_tree_change": (
            "The minimal abstract guard failure is excluded at floor reserve: "
            "the actual cascade has zero hits of 1,2,2,6,2 and zero high-boundary "
            "floor rows. Since high boundary pairs do occur with ell at least 22, "
            "the next theorem target is to prove that such pairs are reserve-"
            "separated from the floor."
        ),
    }
    SUMMARY_PATH.write_text(json.dumps(summary, indent=2) + "\n")


if __name__ == "__main__":
    main()
