#!/usr/bin/env python3
"""Probe terminal-twin lift as the shared-load blocked-reentry mechanism."""

from __future__ import annotations

import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

from first_gap_compatibility_check import write_json, write_jsonl
from slot_factor_public_quotient_test import read_jsonl


THIS_DIR = Path(__file__).resolve().parent
if str(THIS_DIR) not in sys.path:
    sys.path.insert(0, str(THIS_DIR))

from directional_boundary_gate_surface import boundary_index_from_pair_key  # noqa: E402
from joint_endpoint_pair_right_boundary_surface import pair_identity_key, public_key  # noqa: E402


INPUT_ROOT = THIS_DIR / "output"
OUTPUT_DIR = INPUT_ROOT / "terminal_twin_lift_probe"
RULE_ID = "pedk_terminal_twin_lift_probe_v1"
SELECTED_D_RE = re.compile(r"_d([0-9]+)_a")
RIGHT_RESIDUE_OFFSET = {"o2": 2, "o4": 4, "o6": 6}
TERMINAL_TWIN_DISTANCE = 2
TERMINAL_TWIN_MIN_BRIDGE_WIDTH = 20


def public_selected_divisor_count(public_containing_exact_type_key: str) -> int:
    """Return the selected divisor count encoded in a containing type key."""
    match = SELECTED_D_RE.search(public_containing_exact_type_key)
    if not match:
        raise ValueError(
            f"cannot parse selected divisor count: {public_containing_exact_type_key}"
        )
    return int(match.group(1))


def endpoint_right_boundary(right_boundary_residues: str) -> int:
    """Return the maximum first right-open endpoint boundary."""
    return max(RIGHT_RESIDUE_OFFSET[value] for value in right_boundary_residues.split("|"))


def ordered_windows() -> list[str]:
    """Return enriched corpus windows in numeric order."""
    return sorted(
        (
            path.name.replace("enriched_multiplication_map_corpus_", "")
            for path in INPUT_ROOT.glob("enriched_multiplication_map_corpus_*")
        ),
        key=lambda value: int(value.split("_", 1)[0]),
    )


def left_bridge_records(row: dict[str, object]) -> list[dict[str, object]]:
    """Return left bridge distance records for p and q."""
    records = []
    for side in ("p", "q"):
        width = int(row[f"{side}_left_gap_width"])
        offset = int(row[f"{side}_left_winner_offset"])
        distance = width - offset
        records.append(
            {
                "side": side,
                "left_bridge_width": width,
                "immediate_left_distance": distance,
                "terminal_twin_lift": (
                    distance == TERMINAL_TWIN_DISTANCE
                    and width >= TERMINAL_TWIN_MIN_BRIDGE_WIDTH
                ),
                "left_phase": row[f"{side}_left_winner_phase"],
                "left_exact_type_key": row[f"{side}_left_exact_type_key"],
            }
        )
    return records


def has_terminal_twin_lift(row: dict[str, object]) -> bool:
    """Return whether one side has terminal twin lift."""
    return any(record["terminal_twin_lift"] for record in left_bridge_records(row))


def load_rows(window: str) -> list[dict[str, object]]:
    """Return enriched rows for one window."""
    return read_jsonl(INPUT_ROOT / f"enriched_multiplication_map_corpus_{window}" / "enriched_rows.jsonl")


def load_match_candidate_rows() -> list[dict[str, object]]:
    """Return load-match candidate rows whose right-boundary cell reentered."""
    rows = []
    for candidate_path in sorted(
        INPUT_ROOT.glob("directional_boundary_gate_surface_*/candidate_rows.jsonl")
    ):
        window = candidate_path.parent.name.replace("directional_boundary_gate_surface_", "")
        for row in read_jsonl(candidate_path):
            if row["boundary_mode"] != "right_residues":
                continue
            if row["status"] == "not_testable_forward":
                continue
            if not row["boundary_index_falsified"]:
                continue
            public_load = public_selected_divisor_count(
                str(row["public_containing_exact_type_key"])
            )
            endpoint_boundary = endpoint_right_boundary(str(row["right_boundary_residues"]))
            if endpoint_boundary != public_load:
                continue
            out = dict(row)
            out["window"] = window
            rows.append(out)
    rows.sort(
        key=lambda row: (
            str(row["window"]),
            str(row["public_key"]),
            str(row["pair_identity_key"]),
        )
    )
    return rows


def prior_windows(forward_window: str, windows: list[str]) -> list[str]:
    """Return the three prior corpus windows used by the sliding surface."""
    index = windows.index(forward_window)
    return windows[index - 3 : index]


def prior_pair_support_rows(
    candidate_rows: list[dict[str, object]],
    windows: list[str],
) -> list[dict[str, object]]:
    """Return prior pair-support rows for the load-match candidate pair classes."""
    pair_keys_by_window: dict[str, set[str]] = defaultdict(set)
    for row in candidate_rows:
        for window in prior_windows(str(row["window"]), windows):
            pair_keys_by_window[window].add(str(row["pair_identity_key"]))

    rows = []
    for window, pair_keys in sorted(pair_keys_by_window.items()):
        for row in load_rows(window):
            pair_key = pair_identity_key(row)
            if pair_key not in pair_keys:
                continue
            records = left_bridge_records(row)
            rows.append(
                {
                    "rule_id": RULE_ID,
                    "window": window,
                    "case_id": row["case_id"],
                    "pair_identity_key": pair_key,
                    "left_bridge_records": records,
                    "has_terminal_twin_lift": any(
                        record["terminal_twin_lift"] for record in records
                    ),
                }
            )
    rows.sort(
        key=lambda row: (
            str(row["window"]),
            str(row["case_id"]),
            str(row["pair_identity_key"]),
        )
    )
    return rows


def observed_replacement_rows(candidate_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    """Return forward exact rows occupying load-match reentered boundary cells."""
    keys_by_window: dict[str, set[tuple[str, str]]] = defaultdict(set)
    for row in candidate_rows:
        keys_by_window[str(row["window"])].add(
            (str(row["public_key"]), str(row["boundary_index_key"]))
        )

    rows = []
    for window, keys in sorted(keys_by_window.items()):
        for row in load_rows(window):
            if row["public_gwr_side"] != "at_winner":
                continue
            pair_key = pair_identity_key(row)
            boundary_key = boundary_index_from_pair_key(pair_key, "right_residues")
            if (public_key(row), boundary_key) not in keys:
                continue
            records = left_bridge_records(row)
            rows.append(
                {
                    "rule_id": RULE_ID,
                    "window": window,
                    "case_id": row["case_id"],
                    "public_key": public_key(row),
                    "pair_identity_key": pair_key,
                    "boundary_index_key": boundary_key,
                    "left_bridge_records": records,
                    "has_terminal_twin_lift": any(
                        record["terminal_twin_lift"] for record in records
                    ),
                }
            )
    rows.sort(
        key=lambda row: (
            str(row["window"]),
            str(row["case_id"]),
            str(row["pair_identity_key"]),
        )
    )
    return rows


def terminal_twin_count(rows: list[dict[str, object]]) -> int:
    """Return count of rows with terminal twin lift."""
    return sum(1 for row in rows if row["has_terminal_twin_lift"])


def bridge_width_distance_counts(records: list[dict[str, object]]) -> dict[str, int]:
    """Return JSON-safe bridge-width and immediate-left-distance counts."""
    counts = Counter(
        (
            record["left_bridge_width"],
            record["immediate_left_distance"],
        )
        for record in records
    )
    return {
        f"width={width}|distance={distance}": count
        for (width, distance), count in sorted(counts.items())
    }


def summary(
    candidate_rows: list[dict[str, object]],
    prior_rows: list[dict[str, object]],
    observed_rows: list[dict[str, object]],
) -> dict[str, object]:
    """Return terminal-twin lift summary."""
    prior_records = [
        record
        for row in prior_rows
        for record in row["left_bridge_records"]
    ]
    observed_records = [
        record
        for row in observed_rows
        for record in row["left_bridge_records"]
    ]
    return {
        "rule_id": RULE_ID,
        "status": "measured_terminal_twin_lift_probe",
        "theorem_status": "hypothesis_not_proved",
        "terminal_twin_distance": TERMINAL_TWIN_DISTANCE,
        "terminal_twin_min_bridge_width": TERMINAL_TWIN_MIN_BRIDGE_WIDTH,
        "candidate_load_match_reentry_rows": len(candidate_rows),
        "prior_pair_support_rows": len(prior_rows),
        "prior_pair_support_rows_with_terminal_twin_lift": terminal_twin_count(prior_rows),
        "observed_replacement_rows": len(observed_rows),
        "observed_replacement_rows_with_terminal_twin_lift": terminal_twin_count(
            observed_rows
        ),
        "prior_left_bridge_width_distance_counts": bridge_width_distance_counts(
            prior_records
        ),
        "observed_left_bridge_width_distance_counts": bridge_width_distance_counts(
            observed_records
        ),
        "sharper_arithmetic_statement": (
            "For load-match reentered boundary cells, the observed forward "
            "replacement rows all contain terminal-twin lift: immediate-left "
            "endpoint distance 2 inside a left bridge of width at least 20."
        ),
    }


def main() -> int:
    """Run the terminal-twin lift probe."""
    windows = ordered_windows()
    candidate_rows = load_match_candidate_rows()
    prior_rows = prior_pair_support_rows(candidate_rows, windows)
    observed_rows = observed_replacement_rows(candidate_rows)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    write_json(OUTPUT_DIR / "summary.json", summary(candidate_rows, prior_rows, observed_rows))
    write_jsonl(OUTPUT_DIR / "candidate_rows.jsonl", candidate_rows)
    write_jsonl(OUTPUT_DIR / "prior_pair_support_rows.jsonl", prior_rows)
    write_jsonl(OUTPUT_DIR / "observed_replacement_rows.jsonl", observed_rows)
    print(
        json.dumps(
            summary(candidate_rows, prior_rows, observed_rows),
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
