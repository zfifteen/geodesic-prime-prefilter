#!/usr/bin/env python3
"""Classify reset stop-walls in the seeded PGS Gilbreath cascade."""

from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path


ENDPOINT_COUNT = 16384
LOW_VALUES = {0, 2}
OUT_DIR = Path(__file__).resolve().parent
SUMMARY_PATH = OUT_DIR / "2026-05-20-reset_stop_wall_summary.json"
ROWS_PATH = OUT_DIR / "2026-05-20-reset_stop_wall_rows.csv"


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


def low_prefix_len(row: list[int]) -> int:
    i = 1
    while i < len(row) and row[i] in LOW_VALUES:
        i += 1
    return i - 1


def difference_row(row: list[int]) -> list[int]:
    return [abs(row[i + 1] - row[i]) for i in range(len(row) - 1)]


def reset_extension(row: list[int], ell: int) -> tuple[int, str, int | None, int | None, int | None]:
    j = ell
    while j + 1 < len(row) and abs(row[j + 1] - row[j]) in LOW_VALUES:
        j += 1
    if j + 1 == len(row):
        return j - ell, "finite_edge_truncated", None, None, None
    left = row[j]
    right = row[j + 1]
    stop_diff = abs(right - left)
    return j - ell, "closed", left, right, stop_diff


def row_window(row: list[int], ell: int) -> str:
    start = max(0, ell - 3)
    end = min(len(row), ell + 9)
    return " ".join(str(value) for value in row[start:end])


def main() -> None:
    row, final_endpoint = endpoint_gaps(ENDPOINT_COUNT)
    leading_failures = 0
    tail_parity_failures = 0
    depletion_failures = 0
    positive_reset_rows = 0
    closed_positive_resets = 0
    finite_edge_truncated_resets = 0
    boundary_pair_failures = 0
    stop_diff_counts: Counter[int] = Counter()
    stop_pair_counts: Counter[str] = Counter()
    extension_edge_counts: Counter[int] = Counter()
    boundary_pair_counts: Counter[str] = Counter()
    examples: list[dict[str, int | str | None]] = []

    with ROWS_PATH.open("w", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "depth",
                "row_len",
                "ell_before",
                "ell_after",
                "reset_gain",
                "boundary_left",
                "boundary_right",
                "extension_edges",
                "closure",
                "stop_left",
                "stop_right",
                "stop_diff",
                "row_window",
            ],
            lineterminator="\n",
        )
        writer.writeheader()

        for depth in range(ENDPOINT_COUNT - 1):
            if row[0] != 1:
                leading_failures += 1
            if any(value % 2 != 0 for value in row[1:]):
                tail_parity_failures += 1

            next_row = difference_row(row)
            ell_before = low_prefix_len(row)
            ell_after = low_prefix_len(next_row)
            floor_after = max(0, ell_before - 1)

            if ell_after < floor_after:
                depletion_failures += 1

            reset_gain = ell_after - floor_after
            has_boundary_pair = ell_before >= 1 and ell_before + 1 < len(row)
            if reset_gain > 0 and has_boundary_pair:
                positive_reset_rows += 1
                boundary_left = row[ell_before]
                boundary_right = row[ell_before + 1]
                boundary_pair = f"{boundary_left},{boundary_right}"
                boundary_pair_counts[boundary_pair] += 1
                if boundary_pair != "2,4":
                    boundary_pair_failures += 1

                extension_edges, closure, stop_left, stop_right, stop_diff = reset_extension(
                    row, ell_before
                )
                extension_edge_counts[extension_edges] += 1
                if closure == "closed":
                    closed_positive_resets += 1
                    assert stop_diff is not None
                    assert stop_left is not None
                    assert stop_right is not None
                    stop_diff_counts[stop_diff] += 1
                    stop_pair_counts[f"{stop_left},{stop_right}"] += 1
                else:
                    finite_edge_truncated_resets += 1

                record = {
                    "depth": depth,
                    "row_len": len(row),
                    "ell_before": ell_before,
                    "ell_after": ell_after,
                    "reset_gain": reset_gain,
                    "boundary_left": boundary_left,
                    "boundary_right": boundary_right,
                    "extension_edges": extension_edges,
                    "closure": closure,
                    "stop_left": stop_left,
                    "stop_right": stop_right,
                    "stop_diff": stop_diff,
                    "row_window": row_window(row, ell_before),
                }
                writer.writerow(record)
                if len(examples) < 12:
                    examples.append(record)

            row = next_row

    summary = {
        "endpoint_count": ENDPOINT_COUNT,
        "seed_endpoint": 2,
        "final_endpoint": final_endpoint,
        "cascade_transitions": ENDPOINT_COUNT - 1,
        "leading_failures": leading_failures,
        "tail_parity_failures": tail_parity_failures,
        "depletion_failures": depletion_failures,
        "positive_reset_rows": positive_reset_rows,
        "closed_positive_resets": closed_positive_resets,
        "finite_edge_truncated_resets": finite_edge_truncated_resets,
        "boundary_pair_failures": boundary_pair_failures,
        "boundary_pair_counts": dict(sorted(boundary_pair_counts.items())),
        "stop_diff_counts": dict(sorted(stop_diff_counts.items())),
        "stop_pair_counts": dict(sorted(stop_pair_counts.items())),
        "extension_edge_counts": dict(sorted(extension_edge_counts.items())),
        "invalidated_shortcut": "Closed positive reset stop-walls are not confined to absolute difference 4.",
        "next_theorem_obligation": "Derive the broader closed stop-wall alphabet from seeded ordered endpoint-gap grammar after the 2,4 reset admission pair.",
        "examples": examples,
        "status": "ADVANCE",
    }
    SUMMARY_PATH.write_text(json.dumps(summary, indent=2) + "\n")


if __name__ == "__main__":
    main()
