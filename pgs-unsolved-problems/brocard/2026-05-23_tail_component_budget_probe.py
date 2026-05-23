#!/usr/bin/env python3
"""Analyze the Brocard post-first endpoint tail budget.

The live Brocard bridge is the half-wall endpoint lemma:

    e4(a) - a^2 < 2a.

Prior work split the high-root surface into a square-tail quarter budget
and a post-first endpoint-chain half budget. This analyzer tests the natural
componentwise route to the second budget:

    c2 < a/6, c3 < a/6, c4 < a/6

where c2, c3, and c4 are the three endpoint-chain components after e1.
If true, their sum is below a/2. If false, the proof must use aggregate
chain-tail structure or isolate a compensation rule.
"""

from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
SOURCE_CSV = BASE_DIR / "2026-05-20_half_wall_endpoint_probe.csv"
OUTPUT_CSV = BASE_DIR / "2026-05-23_tail_component_budget_probe.csv"
SUMMARY_JSON = BASE_DIR / "2026-05-23_tail_component_budget_summary.json"

HIGH_ROOT_FLOOR = 101
FINITE_COMPENSATION_CEILING = 167


def load_rows() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    with SOURCE_CSV.open(newline="") as handle:
        reader = csv.DictReader(handle)
        for source in reader:
            a = int(source["a"])
            offsets = [int(value) for value in source["endpoint_offsets"].split("|")]
            components = [int(value) for value in source["component_word"].split("|")]
            u1, u2, u3, u4 = offsets
            c1, c2, c3, c4 = components
            tail_components = [c2, c3, c4]
            tail_sum = c2 + c3 + c4
            max_tail_component = max(tail_components)
            max_tail_position = tail_components.index(max_tail_component) + 2
            other_tail_sum = tail_sum - max_tail_component
            row = {
                "a": a,
                "square": int(source["square"]),
                "u1": u1,
                "u2": u2,
                "u3": u3,
                "u4": u4,
                "c1": c1,
                "c2": c2,
                "c3": c3,
                "c4": c4,
                "tail_sum": tail_sum,
                "tail_half_slack": a - 2 * tail_sum,
                "square_tail_quarter_slack": a - 4 * u1,
                "max_tail_component": max_tail_component,
                "max_tail_position": max_tail_position,
                "max_tail_component_sixth_slack": a - 6 * max_tail_component,
                "other_tail_sum_when_max_removed": other_tail_sum,
                "equal_component_budget_status": "pass" if 6 * max_tail_component < a else "fail",
                "chain_tail_half_status": "pass" if 2 * tail_sum < a else "fail",
                "square_tail_quarter_status": "pass" if 4 * u1 < a else "fail",
                "a_mod_30": int(source["a_mod_30"]),
                "square_mod_30": (a * a) % 30,
            }
            rows.append(row)
    return rows


def top_rows(rows: list[dict[str, object]], key: str, count: int = 10) -> list[dict[str, object]]:
    return sorted(rows, key=lambda row: (row[key], row["a"]), reverse=True)[:count]


def main() -> None:
    rows = load_rows()
    high_rows = [row for row in rows if row["a"] >= HIGH_ROOT_FLOOR]
    post_threshold_rows = [row for row in high_rows if row["a"] >= FINITE_COMPENSATION_CEILING]

    equal_component_failures = [
        row for row in high_rows if row["equal_component_budget_status"] == "fail"
    ]
    finite_compensation_rows = [
        row for row in high_rows if row["a"] < FINITE_COMPENSATION_CEILING
    ]
    chain_tail_half_failures = [row for row in high_rows if row["chain_tail_half_status"] == "fail"]
    square_tail_quarter_failures = [
        row for row in high_rows if row["square_tail_quarter_status"] == "fail"
    ]
    post_threshold_equal_component_failures = [
        row
        for row in post_threshold_rows
        if row["equal_component_budget_status"] == "fail"
    ]

    fieldnames = [
        "a",
        "square",
        "u1",
        "u2",
        "u3",
        "u4",
        "c1",
        "c2",
        "c3",
        "c4",
        "tail_sum",
        "tail_half_slack",
        "square_tail_quarter_slack",
        "max_tail_component",
        "max_tail_position",
        "max_tail_component_sixth_slack",
        "other_tail_sum_when_max_removed",
        "equal_component_budget_status",
        "chain_tail_half_status",
        "square_tail_quarter_status",
        "a_mod_30",
        "square_mod_30",
    ]
    with OUTPUT_CSV.open("w", newline="\n") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(high_rows)

    component_failure_positions = Counter(
        row["max_tail_position"] for row in equal_component_failures
    )
    component_failure_square_residues = Counter(
        row["square_mod_30"] for row in equal_component_failures
    )

    summary = {
        "source_csv": SOURCE_CSV.name,
        "output_csv": OUTPUT_CSV.name,
        "high_root_floor": HIGH_ROOT_FLOOR,
        "prime_roots_checked_high": len(high_rows),
        "first_high_root": high_rows[0]["a"],
        "last_high_root": high_rows[-1]["a"],
        "component_budget_bridge": "c2 < a/6, c3 < a/6, c4 < a/6 implies u4 - u1 < a/2",
        "component_budget_status": "invalidated_on_measured_surface",
        "equal_component_budget_failures": len(equal_component_failures),
        "equal_component_failure_rows": equal_component_failures,
        "component_failure_positions": dict(sorted(component_failure_positions.items())),
        "component_failure_square_residues_mod_30": dict(
            sorted(component_failure_square_residues.items())
        ),
        "finite_compensation_ceiling": FINITE_COMPENSATION_CEILING,
        "finite_compensation_rows_checked": len(finite_compensation_rows),
        "finite_compensation_rows": finite_compensation_rows,
        "finite_compensation_chain_tail_half_failures": sum(
            row["chain_tail_half_status"] == "fail" for row in finite_compensation_rows
        ),
        "finite_compensation_square_tail_quarter_failures": sum(
            row["square_tail_quarter_status"] == "fail" for row in finite_compensation_rows
        ),
        "post_threshold_roots_checked": len(post_threshold_rows),
        "post_threshold_equal_component_failures": len(
            post_threshold_equal_component_failures
        ),
        "chain_tail_half_statement": "u4 - u1 < a/2 for a >= 101",
        "chain_tail_half_failures": len(chain_tail_half_failures),
        "square_tail_quarter_statement": "u1 < a/4 for a >= 101",
        "square_tail_quarter_failures": len(square_tail_quarter_failures),
        "max_chain_tail_utilization_row": max(
            high_rows, key=lambda row: (2 * row["tail_sum"] / row["a"], row["a"])
        ),
        "max_tail_component_sixth_utilization_row": max(
            high_rows,
            key=lambda row: (6 * row["max_tail_component"] / row["a"], row["a"]),
        ),
        "max_square_tail_quarter_utilization_row": max(
            high_rows, key=lambda row: (4 * row["u1"] / row["a"], row["a"])
        ),
        "lowest_tail_half_slack_rows": sorted(
            high_rows, key=lambda row: (row["tail_half_slack"], row["a"])
        )[:10],
        "largest_tail_component_rows": top_rows(high_rows, "max_tail_component"),
        "proof_tree_change": (
            "The equal per-component tail-budget branch is false. "
            "A proof of the chain-tail half lemma must either prove the "
            "component budget only after a threshold and directly close the "
            "finite compensation rows, or prove an aggregate endpoint-chain "
            "compensation law."
        ),
    }

    with SUMMARY_JSON.open("w", newline="\n") as handle:
        json.dump(summary, handle, indent=2)
        handle.write("\n")

    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
