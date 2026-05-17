#!/usr/bin/env python3
"""Profile the simple forward-boundary law candidate across measured windows."""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path

from first_gap_compatibility_check import write_json, write_jsonl
from joint_endpoint_pair_right_boundary_surface import rate_mpermille, rate_ppm


THIS_DIR = Path(__file__).resolve().parent
DEFAULT_OUTPUT_DIR = THIS_DIR / "output" / "forward_boundary_law_profile"
RULE_ID = "pedk_forward_boundary_law_profile_v1"

WINDOWS = (
    ("21001_23000", "directional_boundary_gate_surface_21001_23000"),
    ("23001_25000", "directional_boundary_gate_surface_23001_25000"),
    ("25001_27000", "directional_boundary_gate_surface_25001_27000"),
    ("27001_30000", "directional_boundary_gate_surface_27001_30000"),
)

PROFILE_AXES = (
    "public_containing_exact_type_key",
    "boundary_index_key",
    "left_boundary_residues",
    "left_boundary_phases",
    "right_boundary_phases",
    "left_right_residue_pair",
    "right_residue_phase_pair",
)


def read_jsonl(path: Path) -> list[dict[str, object]]:
    """Read LF-delimited JSON rows."""
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def profile_value(row: dict[str, object], axis: str) -> str:
    """Return one profiling value for a right-residue gated row."""
    if axis == "left_right_residue_pair":
        return (
            f"L={row['left_boundary_residues']}|"
            f"R={row['right_boundary_residues']}"
        )
    if axis == "right_residue_phase_pair":
        return (
            f"R={row['right_boundary_residues']}|"
            f"Rphase={row['right_boundary_phases']}"
        )
    return str(row[axis])


def status_counts(rows: list[dict[str, object]]) -> dict[str, int | None]:
    """Return exact-pair falsification counts for testable rows."""
    testable = [
        row for row in rows
        if row["status"] != "not_testable_forward"
    ]
    falsified = [
        row for row in testable
        if row["exact_pair_falsified"]
    ]
    return {
        "row_count": len(rows),
        "testable_count": len(testable),
        "survived_count": len(testable) - len(falsified),
        "falsified_count": len(falsified),
        "falsification_rate_mpermille": rate_mpermille(
            len(falsified),
            len(testable),
        ),
        "falsification_rate_ppm": rate_ppm(len(falsified), len(testable)),
    }


def load_window(base: Path, window_name: str, dirname: str) -> dict[str, object]:
    """Load one directional-boundary window and keep right-residue rows."""
    summary = json.loads((base / dirname / "summary.json").read_text(encoding="utf-8"))
    surface = next(
        row for row in summary["top_surfaces"]
        if row["boundary_mode"] == "right_residues"
    )
    rows = [
        row for row in read_jsonl(base / dirname / "candidate_rows.jsonl")
        if row["boundary_mode"] == "right_residues"
    ]
    return {
        "window": window_name,
        "surface": surface,
        "rows": rows,
    }


def window_rows(windows: list[dict[str, object]]) -> list[dict[str, object]]:
    """Return summary rows for each forward window."""
    out = []
    total_rows = []
    for window in windows:
        surface = window["surface"]
        rows = window["rows"]
        total_rows.extend(rows)
        out.append(
            {
                "rule_id": RULE_ID,
                "window": window["window"],
                "joint_candidate_cell_count": surface["joint_candidate_cell_count"],
                "forward_testable_cell_count": surface["forward_testable_cell_count"],
                "falsified_forward_cell_count": surface["falsified_forward_cell_count"],
                "strict_falsification_rate_ppm": surface["strict_falsification_rate_ppm"],
                "right_boundary_absent_cell_count": surface["boundary_absent_cell_count"],
                "top_1000_falsified_count": surface["top_k_metrics"]["top_1000"][
                    "falsified_count"
                ],
                "top_1000_testable_count": surface["top_k_metrics"]["top_1000"][
                    "testable_count"
                ],
                "materialized_row_count": len(rows),
            }
        )
    totals = status_counts(total_rows)
    out.append(
        {
            "rule_id": RULE_ID,
            "window": "all_windows",
            "joint_candidate_cell_count": sum(
                int(row["joint_candidate_cell_count"])
                for row in out
                if row["window"] != "all_windows"
            ),
            "forward_testable_cell_count": totals["testable_count"],
            "falsified_forward_cell_count": totals["falsified_count"],
            "strict_falsification_rate_ppm": totals["falsification_rate_ppm"],
            "right_boundary_absent_cell_count": None,
            "top_1000_falsified_count": None,
            "top_1000_testable_count": None,
            "materialized_row_count": len(total_rows),
        }
    )
    return out


def axis_profile_rows(windows: list[dict[str, object]]) -> list[dict[str, object]]:
    """Return falsification profiles by simple feature axes."""
    grouped: dict[tuple[str, str], list[dict[str, object]]] = defaultdict(list)
    for window in windows:
        for row in window["rows"]:
            row = dict(row)
            row["window"] = window["window"]
            for axis in PROFILE_AXES:
                grouped[(axis, profile_value(row, axis))].append(row)

    out = []
    for (axis, value), rows in grouped.items():
        counts = status_counts(rows)
        tested_windows = sorted(
            {
                str(row["window"])
                for row in rows
                if row["status"] != "not_testable_forward"
            }
        )
        out.append(
            {
                "rule_id": RULE_ID,
                "axis": axis,
                "value": value,
                "tested_window_count": len(tested_windows),
                "tested_windows": tested_windows,
                **counts,
            }
        )
    out.sort(
        key=lambda row: (
            int(row["falsified_count"]),
            -int(row["testable_count"]),
            str(row["axis"]),
            str(row["value"]),
        )
    )
    return out


def cross_window_pair_rows(windows: list[dict[str, object]]) -> list[dict[str, object]]:
    """Return exact endpoint-pair rows that recur across windows."""
    grouped: dict[str, list[dict[str, object]]] = defaultdict(list)
    for window in windows:
        for row in window["rows"]:
            if row["status"] == "not_testable_forward":
                continue
            grouped[str(row["pair_identity_key"])].append({**row, "window": window["window"]})

    out = []
    for pair_key, rows in grouped.items():
        counts = status_counts(rows)
        if int(counts["testable_count"]) < 2:
            continue
        windows_seen = sorted({str(row["window"]) for row in rows})
        exemplar = rows[0]
        out.append(
            {
                "rule_id": RULE_ID,
                "pair_identity_key": pair_key,
                "windows_seen": windows_seen,
                "right_boundary_residues": exemplar["right_boundary_residues"],
                "right_boundary_phases": exemplar["right_boundary_phases"],
                "left_boundary_residues": exemplar["left_boundary_residues"],
                "left_boundary_phases": exemplar["left_boundary_phases"],
                **counts,
            }
        )
    out.sort(
        key=lambda row: (
            int(row["falsified_count"]),
            -int(row["testable_count"]),
            str(row["pair_identity_key"]),
        )
    )
    return out


def summary(
    windows: list[dict[str, object]],
    windows_out: list[dict[str, object]],
    axis_rows: list[dict[str, object]],
    pair_rows: list[dict[str, object]],
) -> dict[str, object]:
    """Return compact profile summary."""
    all_row = next(row for row in windows_out if row["window"] == "all_windows")
    clean_axes = [
        row for row in axis_rows
        if row["falsified_count"] == 0 and row["testable_count"] >= 100
    ][:20]
    fragile_axes = sorted(
        [
            row for row in axis_rows
            if row["testable_count"] >= 100
        ],
        key=lambda row: (
            -(int(row["falsification_rate_ppm"]) if row["falsification_rate_ppm"] else 0),
            -int(row["testable_count"]),
        ),
    )[:20]
    recurring_clean_pairs = [
        row for row in pair_rows
        if row["falsified_count"] == 0
    ][:10]
    recurring_fragile_pairs = sorted(
        [
            row for row in pair_rows
            if row["falsified_count"] > 0
        ],
        key=lambda row: (-int(row["falsified_count"]), str(row["pair_identity_key"])),
    )[:10]
    return {
        "rule_id": RULE_ID,
        "status": "measured_forward_boundary_law_profile",
        "theorem_status": "hypothesis_not_proved",
        "inference_status": "not_live_pedk_inference",
        "window_count": len(windows),
        "total_testable_right_gated_exact_cells": all_row["forward_testable_cell_count"],
        "total_falsified_right_gated_exact_cells": all_row["falsified_forward_cell_count"],
        "total_falsification_rate_ppm": all_row["strict_falsification_rate_ppm"],
        "profile_axis_count": len(axis_rows),
        "recurring_pair_count": len(pair_rows),
        "clean_axis_examples": clean_axes,
        "fragile_axis_examples": fragile_axes,
        "recurring_clean_pair_examples": recurring_clean_pairs,
        "recurring_fragile_pair_examples": recurring_fragile_pairs,
    }


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Profile the forward-boundary law candidate.")
    parser.add_argument(
        "--input-root",
        type=Path,
        default=THIS_DIR / "output",
    )
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    """Run the profile."""
    args = parse_args(argv)
    windows = [
        load_window(args.input_root, window_name, dirname)
        for window_name, dirname in WINDOWS
    ]
    w_rows = window_rows(windows)
    a_rows = axis_profile_rows(windows)
    p_rows = cross_window_pair_rows(windows)
    out_summary = summary(windows, w_rows, a_rows, p_rows)

    args.output_dir.mkdir(parents=True, exist_ok=True)
    write_json(args.output_dir / "summary.json", out_summary)
    write_jsonl(args.output_dir / "window_rows.jsonl", w_rows)
    write_jsonl(args.output_dir / "axis_profile_rows.jsonl", a_rows)
    write_jsonl(args.output_dir / "recurring_pair_rows.jsonl", p_rows)
    print(json.dumps(out_summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
