#!/usr/bin/env python3
"""Brocard square-wall endpoint probe.

This probe stays on the PGS object surface:

    exact divisor-count field -> endpoint arrivals -> square-wall margin.

For each prime root a <= ROOT_LIMIT, it starts at a^2 and records the first
four later integers with exact divisor count 2. It then tests the prior
minimal square-wall bridge

    e4(a) - a^2 < 4a

and the stronger half-wall candidate

    e4(a) - a^2 < 2a    for a >= 11.
"""

from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path


ROOT_LIMIT = 100_000
HALF_WALL_ROOT_FLOOR = 11
FIXED_WALL = 256

BASE_DIR = Path(__file__).resolve().parent
CSV_PATH = BASE_DIR / "2026-05-20_half_wall_endpoint_probe.csv"
SUMMARY_PATH = BASE_DIR / "2026-05-20_half_wall_endpoint_summary.json"


def divisor_counts_up_to(limit: int) -> list[int]:
    counts = [0] * (limit + 1)
    for divisor in range(1, limit + 1):
        for multiple in range(divisor, limit + 1, divisor):
            counts[multiple] += 1
    return counts


def exact_divisor_count(n: int, primes: list[int]) -> int:
    remaining = n
    total = 1
    for prime in primes:
        if prime * prime > remaining:
            break
        if remaining % prime == 0:
            exponent = 0
            while remaining % prime == 0:
                remaining //= prime
                exponent += 1
            total *= exponent + 1
        if remaining == 1:
            break
    if remaining > 1:
        total *= 2
    return total


def first_four_endpoint_offsets(a: int, primes: list[int]) -> list[int]:
    square = a * a
    offsets: list[int] = []
    for offset in range(1, 4 * a):
        if exact_divisor_count(square + offset, primes) == 2:
            offsets.append(offset)
            if len(offsets) == 4:
                return offsets
    return offsets


def component_word(offsets: list[int]) -> str:
    components = [offsets[0]]
    for previous, current in zip(offsets, offsets[1:]):
        components.append(current - previous)
    return "|".join(str(component) for component in components)


def top_rows(rows: list[dict[str, object]], key: str, count: int = 10) -> list[dict[str, object]]:
    return sorted(rows, key=lambda row: (row[key], row["a"]), reverse=True)[:count]


def main() -> None:
    root_counts = divisor_counts_up_to(ROOT_LIMIT + 2)
    primes = [n for n in range(2, ROOT_LIMIT + 3) if root_counts[n] == 2]
    roots = [n for n in primes if 3 <= n <= ROOT_LIMIT]

    rows: list[dict[str, object]] = []
    four_wall_failures: list[dict[str, object]] = []
    half_wall_failures: list[dict[str, object]] = []
    small_half_wall_exceptions: list[dict[str, object]] = []
    fixed_wall_failures: list[dict[str, object]] = []

    for a in roots:
        offsets = first_four_endpoint_offsets(a, primes)
        if len(offsets) < 4:
            row = {
                "a": a,
                "square": a * a,
                "endpoint_offsets": "|".join(str(offset) for offset in offsets),
                "component_word": component_word(offsets) if offsets else "",
                "s4": "",
                "slack_4a": "",
                "slack_2a": "",
                "utilization_4a": "",
                "utilization_2a": "",
                "half_wall_status": "unresolved_before_4a",
                "fixed_256_status": "unresolved_before_4a",
                "a_mod_30": a % 30,
            }
            rows.append(row)
            four_wall_failures.append(row)
            continue

        s4 = offsets[3]
        slack_4a = 4 * a - s4
        slack_2a = 2 * a - s4
        half_status = "not_applicable_small_root"
        if a >= HALF_WALL_ROOT_FLOOR:
            half_status = "pass" if slack_2a > 0 else "fail"

        row = {
            "a": a,
            "square": a * a,
            "endpoint_offsets": "|".join(str(offset) for offset in offsets),
            "component_word": component_word(offsets),
            "s4": s4,
            "slack_4a": slack_4a,
            "slack_2a": slack_2a,
            "utilization_4a": round(s4 / (4 * a), 12),
            "utilization_2a": round(s4 / (2 * a), 12),
            "half_wall_status": half_status,
            "fixed_256_status": "pass" if s4 <= FIXED_WALL else "fail",
            "a_mod_30": a % 30,
        }
        rows.append(row)

        if slack_4a <= 0:
            four_wall_failures.append(row)
        if a >= HALF_WALL_ROOT_FLOOR and slack_2a <= 0:
            half_wall_failures.append(row)
        if a < HALF_WALL_ROOT_FLOOR and slack_2a <= 0:
            small_half_wall_exceptions.append(row)
        if s4 > FIXED_WALL:
            fixed_wall_failures.append(row)

    threshold_summaries = []
    for floor in (11, 101, 1_009, 10_007, 50_021):
        subset = [row for row in rows if row["s4"] != "" and row["a"] >= floor]
        max_s4_row = max(subset, key=lambda row: (row["s4"], row["a"]))
        max_util_row = max(subset, key=lambda row: (row["utilization_2a"], row["a"]))
        threshold_summaries.append(
            {
                "floor": floor,
                "roots": len(subset),
                "max_s4": max_s4_row["s4"],
                "max_s4_at_a": max_s4_row["a"],
                "max_utilization_2a": max_util_row["utilization_2a"],
                "max_utilization_2a_at_a": max_util_row["a"],
                "min_slack_2a": min(row["slack_2a"] for row in subset),
            }
        )

    with CSV_PATH.open("w", newline="\n") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "a",
                "square",
                "endpoint_offsets",
                "component_word",
                "s4",
                "slack_4a",
                "slack_2a",
                "utilization_4a",
                "utilization_2a",
                "half_wall_status",
                "fixed_256_status",
                "a_mod_30",
            ],
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(rows)

    resolved_rows = [row for row in rows if row["s4"] != ""]
    half_rows = [row for row in resolved_rows if row["a"] >= HALF_WALL_ROOT_FLOOR]
    component_counter = Counter(row["component_word"] for row in resolved_rows)
    fixed_failure_residues = Counter(row["a_mod_30"] for row in fixed_wall_failures)

    summary = {
        "root_limit": ROOT_LIMIT,
        "prime_roots_checked": len(roots),
        "first_root": roots[0],
        "last_root": roots[-1],
        "four_wall_statement": "e4(a) - a^2 < 4a",
        "four_wall_failures": len(four_wall_failures),
        "half_wall_statement": "e4(a) - a^2 < 2a for a >= 11",
        "half_wall_root_floor": HALF_WALL_ROOT_FLOOR,
        "half_wall_failures": len(half_wall_failures),
        "small_half_wall_exception_count": len(small_half_wall_exceptions),
        "small_half_wall_exceptions": small_half_wall_exceptions,
        "fixed_wall_statement": f"e4(a) - a^2 <= {FIXED_WALL}",
        "fixed_wall_failures": len(fixed_wall_failures),
        "first_fixed_wall_failure": fixed_wall_failures[0] if fixed_wall_failures else None,
        "fixed_wall_failure_residues_mod_30": dict(sorted(fixed_failure_residues.items())),
        "max_s4_row": max(resolved_rows, key=lambda row: (row["s4"], row["a"])),
        "max_utilization_4a_row": max(resolved_rows, key=lambda row: (row["utilization_4a"], row["a"])),
        "max_utilization_2a_row_a_ge_11": max(
            half_rows, key=lambda row: (row["utilization_2a"], row["a"])
        ),
        "threshold_summaries": threshold_summaries,
        "top_s4_rows": top_rows(resolved_rows, "s4"),
        "top_half_wall_utilization_rows": top_rows(half_rows, "utilization_2a"),
        "dominant_component_words": component_counter.most_common(10),
        "csv": CSV_PATH.name,
    }

    with SUMMARY_PATH.open("w", newline="\n") as handle:
        json.dump(summary, handle, indent=2)
        handle.write("\n")

    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
