#!/usr/bin/env python3
"""Probe the simplest right-following residue invariant."""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path

from first_gap_compatibility_check import write_json, write_jsonl
from joint_endpoint_pair_right_boundary_surface import rate_ppm


THIS_DIR = Path(__file__).resolve().parent
DEFAULT_INPUT_ROOT = THIS_DIR / "output"
DEFAULT_OUTPUT_DIR = DEFAULT_INPUT_ROOT / "simple_invariant_probe"
RULE_ID = "pedk_simple_right_residue_invariant_v1"

WINDOWS = (
    ("21001_23000", "directional_boundary_gate_surface_21001_23000"),
    ("23001_25000", "directional_boundary_gate_surface_23001_25000"),
    ("25001_27000", "directional_boundary_gate_surface_25001_27000"),
    ("27001_30000", "directional_boundary_gate_surface_27001_30000"),
)

RESIDUE_RANK = {"o2": 1, "o4": 2, "o6": 3}


def read_jsonl(path: Path) -> list[dict[str, object]]:
    """Read LF-delimited JSON rows."""
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def right_residues(row: dict[str, object]) -> tuple[str, str]:
    """Return the two right-following residue labels."""
    left, right = str(row["right_boundary_residues"]).split("|")
    return left, right


def right_residue_max(row: dict[str, object]) -> str:
    """Return the larger right-following residue label."""
    residues = right_residues(row)
    return max(residues, key=lambda label: RESIDUE_RANK[label])


def right_residue_sum(row: dict[str, object]) -> int:
    """Return the rank sum of the right-following residue pair."""
    return sum(RESIDUE_RANK[label] for label in right_residues(row))


def right_residue_span(row: dict[str, object]) -> int:
    """Return the rank span of the right-following residue pair."""
    ranks = [RESIDUE_RANK[label] for label in right_residues(row)]
    return max(ranks) - min(ranks)


def invariant_values(row: dict[str, object]) -> dict[str, str]:
    """Return simple invariant candidates for one row."""
    residues = right_residues(row)
    max_residue = right_residue_max(row)
    return {
        "right_residue_pair": str(row["right_boundary_residues"]),
        "right_residue_max": max_residue,
        "right_residue_sum": str(right_residue_sum(row)),
        "right_residue_span": str(right_residue_span(row)),
        "right_residue_touches_o6": str("o6" in residues).lower(),
        "right_residue_max_is_o4": str(max_residue == "o4").lower(),
    }


def status_counts(rows: list[dict[str, object]]) -> dict[str, int | None]:
    """Count exact endpoint-pair falsifications among testable rows."""
    testable = [row for row in rows if row["status"] != "not_testable_forward"]
    falsified = [row for row in testable if row["exact_pair_falsified"]]
    return {
        "row_count": len(rows),
        "testable_count": len(testable),
        "survived_count": len(testable) - len(falsified),
        "falsified_count": len(falsified),
        "falsification_rate_ppm": rate_ppm(len(falsified), len(testable)),
    }


def load_rows(input_root: Path) -> list[dict[str, object]]:
    """Load all right-residue candidate rows from measured windows."""
    rows = []
    for window_name, dirname in WINDOWS:
        path = input_root / dirname / "candidate_rows.jsonl"
        for row in read_jsonl(path):
            if row["boundary_mode"] != "right_residues":
                continue
            rows.append({**row, "window": window_name})
    return rows


def grouped_rows(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    """Profile simple invariant values."""
    groups: dict[tuple[str, str], list[dict[str, object]]] = defaultdict(list)
    for row in rows:
        for axis, value in invariant_values(row).items():
            groups[(axis, value)].append(row)

    out = []
    for (axis, value), grouped in groups.items():
        tested_windows = sorted(
            {
                str(row["window"])
                for row in grouped
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
                **status_counts(grouped),
            }
        )
    out.sort(
        key=lambda row: (
            str(row["axis"]),
            int(row["falsified_count"]),
            -int(row["testable_count"]),
            str(row["value"]),
        )
    )
    return out


def window_rows(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    """Profile the candidate invariant in each strict-forward window."""
    out = []
    for window_name, _dirname in WINDOWS:
        window_rows = [row for row in rows if row["window"] == window_name]
        clean = [
            row for row in window_rows
            if right_residue_max(row) == "o4"
        ]
        other = [
            row for row in window_rows
            if right_residue_max(row) != "o4"
        ]
        out.append(
            {
                "rule_id": RULE_ID,
                "window": window_name,
                "right_residue_max_o4": status_counts(clean),
                "right_residue_max_not_o4": status_counts(other),
            }
        )
    return out


def summary(rows: list[dict[str, object]], profiles: list[dict[str, object]]) -> dict[str, object]:
    """Return compact summary for the candidate invariant."""
    clean_rows = [row for row in rows if right_residue_max(row) == "o4"]
    other_rows = [row for row in rows if right_residue_max(row) != "o4"]
    max_rows = [
        row for row in profiles
        if row["axis"] == "right_residue_max"
    ]
    return {
        "rule_id": RULE_ID,
        "status": "measured_simple_invariant_probe",
        "theorem_status": "hypothesis_not_proved",
        "inference_status": "not_live_pedk_inference",
        "candidate_invariant": "under public_at_winner, right_residue_max=o4 is the clean exclusion carrier",
        "window_count": len(WINDOWS),
        "right_residue_max_o4": status_counts(clean_rows),
        "right_residue_max_not_o4": status_counts(other_rows),
        "right_residue_max_profile": max_rows,
    }


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Probe the simplest right-residue invariant.")
    parser.add_argument("--input-root", type=Path, default=DEFAULT_INPUT_ROOT)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    """Run the invariant probe."""
    args = parse_args(argv)
    rows = load_rows(args.input_root)
    profiles = grouped_rows(rows)
    windows = window_rows(rows)
    out_summary = summary(rows, profiles)

    args.output_dir.mkdir(parents=True, exist_ok=True)
    write_json(args.output_dir / "summary.json", out_summary)
    write_jsonl(args.output_dir / "invariant_profile_rows.jsonl", profiles)
    write_jsonl(args.output_dir / "window_rows.jsonl", windows)
    print(json.dumps(out_summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
