#!/usr/bin/env python3
"""Analyze aggregate compensation in the Brocard endpoint-chain tail.

This probe follows the PGS endpoint-chain objects left by the tail-component
budget obstruction:

    c2, c3, c4 = the three endpoint-chain components after e1.

The equal split c2,c3,c4 < a/6 is false. This analyzer tests the next
aggregate bridge:

    max(c2,c3,c4) < a/3
    sum(the other two tail components) < a/6

Together these imply c2 + c3 + c4 < a/2.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
SOURCE_CSV = BASE_DIR / "2026-05-23_tail_component_budget_probe.csv"
OUTPUT_CSV = BASE_DIR / "2026-05-23_aggregate_compensation_probe.csv"
SUMMARY_JSON = BASE_DIR / "2026-05-23_aggregate_compensation_summary.json"


def load_rows() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    with SOURCE_CSV.open(newline="") as handle:
        reader = csv.DictReader(handle)
        for source in reader:
            a = int(source["a"])
            c2 = int(source["c2"])
            c3 = int(source["c3"])
            c4 = int(source["c4"])
            tail_components = [c2, c3, c4]
            dominant_component = max(tail_components)
            dominant_position = tail_components.index(dominant_component) + 2
            residual_pair_sum = sum(tail_components) - dominant_component
            tail_sum = sum(tail_components)
            row = {
                "a": a,
                "u1": int(source["u1"]),
                "u2": int(source["u2"]),
                "u3": int(source["u3"]),
                "u4": int(source["u4"]),
                "c2": c2,
                "c3": c3,
                "c4": c4,
                "dominant_component": dominant_component,
                "dominant_position": dominant_position,
                "residual_pair_sum": residual_pair_sum,
                "tail_sum": tail_sum,
                "dominant_third_slack": a - 3 * dominant_component,
                "residual_pair_sixth_slack": a - 6 * residual_pair_sum,
                "tail_half_slack": a - 2 * tail_sum,
                "dominant_third_status": "pass" if 3 * dominant_component < a else "fail",
                "residual_pair_sixth_status": "pass" if 6 * residual_pair_sum < a else "fail",
                "aggregate_compensation_status": "pass"
                if 3 * dominant_component < a and 6 * residual_pair_sum < a
                else "fail",
                "a_mod_30": int(source["a_mod_30"]),
                "square_mod_30": int(source["square_mod_30"]),
            }
            rows.append(row)
    return rows


def top_rows(rows: list[dict[str, object]], key: str, count: int = 10) -> list[dict[str, object]]:
    return sorted(rows, key=lambda row: (row[key], row["a"]), reverse=True)[:count]


def low_slack_rows(rows: list[dict[str, object]], key: str, count: int = 10) -> list[dict[str, object]]:
    return sorted(rows, key=lambda row: (row[key], row["a"]))[:count]


def main() -> None:
    rows = load_rows()
    dominant_failures = [row for row in rows if row["dominant_third_status"] == "fail"]
    residual_failures = [row for row in rows if row["residual_pair_sixth_status"] == "fail"]
    aggregate_failures = [
        row for row in rows if row["aggregate_compensation_status"] == "fail"
    ]
    tail_half_failures = [row for row in rows if row["tail_half_slack"] <= 0]

    fieldnames = [
        "a",
        "u1",
        "u2",
        "u3",
        "u4",
        "c2",
        "c3",
        "c4",
        "dominant_component",
        "dominant_position",
        "residual_pair_sum",
        "tail_sum",
        "dominant_third_slack",
        "residual_pair_sixth_slack",
        "tail_half_slack",
        "dominant_third_status",
        "residual_pair_sixth_status",
        "aggregate_compensation_status",
        "a_mod_30",
        "square_mod_30",
    ]
    with OUTPUT_CSV.open("w", newline="\n") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    summary = {
        "source_csv": SOURCE_CSV.name,
        "output_csv": OUTPUT_CSV.name,
        "rows_checked": len(rows),
        "root_floor": rows[0]["a"],
        "last_root": rows[-1]["a"],
        "aggregate_compensation_statement": (
            "max(c2,c3,c4) < a/3 and residual_pair_sum < a/6 imply "
            "c2+c3+c4 < a/2"
        ),
        "dominant_third_failures": len(dominant_failures),
        "residual_pair_sixth_failures": len(residual_failures),
        "aggregate_compensation_failures": len(aggregate_failures),
        "tail_half_failures": len(tail_half_failures),
        "min_dominant_third_slack_row": low_slack_rows(rows, "dominant_third_slack", 1)[0],
        "min_residual_pair_sixth_slack_row": low_slack_rows(
            rows, "residual_pair_sixth_slack", 1
        )[0],
        "min_tail_half_slack_row": low_slack_rows(rows, "tail_half_slack", 1)[0],
        "top_dominant_component_rows": top_rows(rows, "dominant_component"),
        "top_residual_pair_sum_rows": top_rows(rows, "residual_pair_sum"),
        "lowest_dominant_third_slack_rows": low_slack_rows(
            rows, "dominant_third_slack"
        ),
        "lowest_residual_pair_sixth_slack_rows": low_slack_rows(
            rows, "residual_pair_sixth_slack"
        ),
        "lowest_tail_half_slack_rows": low_slack_rows(rows, "tail_half_slack"),
        "proof_tree_change": (
            "The live aggregate chain-tail half bridge is reduced to two "
            "sharper PGS endpoint-chain targets: dominant-tail third control "
            "and residual-pair sixth control."
        ),
    }

    with SUMMARY_JSON.open("w", newline="\n") as handle:
        json.dump(summary, handle, indent=2)
        handle.write("\n")

    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
