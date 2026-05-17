#!/usr/bin/env python3
"""Round 1 high-signal extraction for the PEDK synchronization target."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

from first_gap_compatibility_check import write_json, write_jsonl
from slot_factor_public_quotient_test import read_jsonl


THIS_DIR = Path(__file__).resolve().parent
INPUT_ROOT = THIS_DIR / "output"
OUTPUT_DIR = INPUT_ROOT / "codex_round1_high_signal_probe"
RULE_ID = "pedk_codex_round1_high_signal_probe_v1"
TARGET_CONTAINING_TYPE = "o6_d4_a6_d4_odd"
WHEEL_OPEN_RESIDUES = {1, 7, 11, 13, 17, 19, 23, 29}
PUBLIC_LEFT_NEIGHBOR_RESIDUES = {7, 13, 19}
PHASE_WIDTH_COMPLEMENT_PAIRS = {(7, 24), (13, 12)}
EXACT_PUBLIC_TRIGGERS = {
    (
        "prev=o4_d4_even|d<=4|containing=o6_d4_a6_d4_odd@mid|"
        "next=o4_d4_odd|d<=4|at_winner"
    ),
    (
        "prev=o4_d4_odd|d<=4|containing=o6_d4_a6_d4_odd@early|"
        "next=o6_d4_odd|d<=4|at_winner"
    ),
}


def corpus_dirs() -> list[Path]:
    """Return enriched corpus directories in numeric order."""
    return sorted(
        INPUT_ROOT.glob("enriched_multiplication_map_corpus_*"),
        key=lambda path: int(path.name.removeprefix("enriched_multiplication_map_corpus_").split("_", 1)[0]),
    )


def right_open_label(row: dict[str, object], side: str) -> str:
    """Return the first right-open label for one factor side."""
    value = str(row[f"{side}_right_reduced_state"]).split("_", 1)[0]
    if value not in {"o2", "o4", "o6"}:
        raise ValueError(f"unknown right-open label: {value}")
    return value


def open_offset(label: str) -> int:
    """Return the numeric offset encoded by an open label."""
    return int(label[1:])


def interior_open_slot_count(left_endpoint: int, width: int) -> int:
    """Return mod-30 wheel-open slots strictly inside a gap."""
    return sum(
        1
        for value in range(left_endpoint + 1, left_endpoint + width)
        if value % 30 in WHEEL_OPEN_RESIDUES
    )


def public_key(row: dict[str, object]) -> str:
    """Return full public word with GWR side."""
    return f"{row['public_word']}|{row['public_gwr_side']}"


def reduced_row(row: dict[str, object], window: str) -> dict[str, object] | None:
    """Return one extracted high-signal row, or None outside the surface."""
    p = int(row["p"])
    q = int(row["q"])
    if str(row["public_containing_exact_type_key"]) != TARGET_CONTAINING_TYPE:
        return None
    if p % 36 != q % 36:
        return None

    n_value = int(row["N"])
    public_left_endpoint = n_value - int(row["public_n_offset_from_left"])
    public_previous_width = int(row["public_previous_gap"]["gap_width"])
    public_previous_left_endpoint = public_left_endpoint - public_previous_width
    public_previous_left_mod30 = public_previous_left_endpoint % 30
    public_previous_first_open = int(row["public_previous_gap"]["first_open_offset"])
    p_left_gap_width = int(row["p_left_gap_width"])
    p_left_winner_offset = int(row["p_left_winner_offset"])
    lower_predecessor_left_endpoint = p - p_left_gap_width
    lower_predecessor_open_slots = interior_open_slot_count(
        lower_predecessor_left_endpoint,
        p_left_winner_offset,
    )
    p_right_label = right_open_label(row, "p")
    q_right_label = right_open_label(row, "q")
    right_labels = "|".join(sorted((p_right_label, q_right_label)))
    endpoint_right_boundary = max(open_offset(p_right_label), open_offset(q_right_label))
    public_selected_load = int(row["public_containing_gap"]["winner_d"])
    lower_terminal_closure = (
        p_left_gap_width - p_left_winner_offset == 2
        and p_left_gap_width >= 20
    )
    lower_terminal_four_slot = (
        lower_terminal_closure
        and lower_predecessor_open_slots == 4
    )
    phase_width_pair = (p % 36, public_previous_width % 30)
    return {
        "rule_id": RULE_ID,
        "window": window,
        "case_id": row["case_id"],
        "public_key": public_key(row),
        "public_gwr_side": row["public_gwr_side"],
        "public_containing_exact_type_key": row["public_containing_exact_type_key"],
        "public_selected_load": public_selected_load,
        "public_left_endpoint_mod60": public_left_endpoint % 60,
        "public_previous_first_open": public_previous_first_open,
        "public_previous_gap_width": public_previous_width,
        "public_previous_gap_width_mod30": public_previous_width % 30,
        "public_previous_left_mod30": public_previous_left_mod30,
        "public_left_neighbor_gate": (
            public_previous_left_mod30 in PUBLIC_LEFT_NEIGHBOR_RESIDUES
            and public_previous_first_open == 4
        ),
        "p_mod30": p % 30,
        "q_mod30": q % 30,
        "p_mod36": p % 36,
        "q_mod36": q % 36,
        "p_mod180": p % 180,
        "q_mod180": q % 180,
        "factor_mod180_lane": f"{p % 180}|{q % 180}",
        "right_boundary_residues": right_labels,
        "endpoint_right_boundary": endpoint_right_boundary,
        "boundary_balanced": (
            public_selected_load == 4
            and endpoint_right_boundary == 4
        ),
        "rres_o4_o4": right_labels == "o4|o4",
        "phase_width_pair": f"{phase_width_pair[0]}|{phase_width_pair[1]}",
        "phase_width_complement": phase_width_pair in PHASE_WIDTH_COMPLEMENT_PAIRS,
        "p_left_gap_width": p_left_gap_width,
        "p_left_winner_offset": p_left_winner_offset,
        "lower_terminal_closure": lower_terminal_closure,
        "lower_predecessor_left_mod30": lower_predecessor_left_endpoint % 30,
        "lower_predecessor_gap_width": p_left_winner_offset,
        "lower_predecessor_open_slot_count": lower_predecessor_open_slots,
        "lower_predecessor_residue_width_pair": (
            f"{lower_predecessor_left_endpoint % 30}|{p_left_winner_offset}"
        ),
        "lower_terminal_four_slot": lower_terminal_four_slot,
        "full_target_conjunction": (
            str(row["public_gwr_side"]) == "at_winner"
            and public_previous_first_open == 4
            and public_previous_left_mod30 in PUBLIC_LEFT_NEIGHBOR_RESIDUES
            and public_selected_load == 4
            and right_labels == "o4|o4"
            and phase_width_pair in PHASE_WIDTH_COMPLEMENT_PAIRS
        ),
    }


def load_rows() -> list[dict[str, object]]:
    """Load every high-signal row from the current enriched output tree."""
    rows = []
    for directory in corpus_dirs():
        window = directory.name.removeprefix("enriched_multiplication_map_corpus_")
        for row in read_jsonl(directory / "enriched_rows.jsonl"):
            extracted = reduced_row(row, window)
            if extracted is not None:
                rows.append(extracted)
    rows.sort(key=lambda row: (str(row["window"]), str(row["case_id"])))
    return rows


def count_by(rows: list[dict[str, object]], *keys: str) -> dict[str, int]:
    """Return counts by one or more boolean/string row keys."""
    counts = Counter(
        "|".join(f"{key}={row[key]}" for key in keys)
        for row in rows
    )
    return {key: counts[key] for key in sorted(counts)}


def sample(rows: list[dict[str, object]], limit: int = 12) -> list[dict[str, object]]:
    """Return compact sample rows for inspection."""
    return [
        {
            "window": row["window"],
            "case_id": row["case_id"],
            "public_key": row["public_key"],
            "factor_mod180_lane": row["factor_mod180_lane"],
            "phase_width_pair": row["phase_width_pair"],
            "public_previous_left_mod30": row["public_previous_left_mod30"],
            "right_boundary_residues": row["right_boundary_residues"],
            "lower_predecessor_residue_width_pair": row[
                "lower_predecessor_residue_width_pair"
            ],
            "lower_predecessor_open_slot_count": row[
                "lower_predecessor_open_slot_count"
            ],
        }
        for row in rows[:limit]
    ]


def summary(rows: list[dict[str, object]]) -> dict[str, object]:
    """Return Round 1 summary."""
    phase_width_without_four_slot = [
        row
        for row in rows
        if row["phase_width_complement"] and not row["lower_terminal_four_slot"]
    ]
    four_slot_without_public_gate = [
        row
        for row in rows
        if row["lower_terminal_four_slot"] and not row["public_left_neighbor_gate"]
    ]
    full_target_rows = [
        row for row in rows if row["full_target_conjunction"]
    ]
    full_target_bad_rows = [
        row for row in full_target_rows if not row["lower_terminal_four_slot"]
    ]
    full_target_pairs = sorted(
        {
            str(row["lower_predecessor_residue_width_pair"])
            for row in full_target_rows
        }
    )
    exact_trigger_boundary_phase_rows = [
        row
        for row in rows
        if str(row["public_key"]) in EXACT_PUBLIC_TRIGGERS
        and row["rres_o4_o4"]
        and row["phase_width_complement"]
    ]
    exact_trigger_boundary_phase_bad_rows = [
        row
        for row in exact_trigger_boundary_phase_rows
        if not row["lower_terminal_four_slot"]
    ]
    return {
        "rule_id": RULE_ID,
        "status": "measured_codex_round1_high_signal_probe",
        "theorem_status": "hypothesis_not_proved",
        "high_signal_row_count": len(rows),
        "boundary_balanced_x_phase_width_complement_x_lower_terminal_closure": count_by(
            rows,
            "boundary_balanced",
            "phase_width_complement",
            "lower_terminal_closure",
        ),
        "phase_width_complement_x_lower_predecessor_residue_width_pair": count_by(
            rows,
            "phase_width_complement",
            "lower_predecessor_residue_width_pair",
        ),
        "public_left_neighbor_gate_x_boundary_balanced_x_lower_terminal_four_slot": count_by(
            rows,
            "public_left_neighbor_gate",
            "boundary_balanced",
            "lower_terminal_four_slot",
        ),
        "phase_width_without_four_slot_count": len(phase_width_without_four_slot),
        "phase_width_without_four_slot_examples": sample(
            phase_width_without_four_slot,
        ),
        "four_slot_without_public_gate_count": len(four_slot_without_public_gate),
        "four_slot_without_public_gate_examples": sample(
            four_slot_without_public_gate,
        ),
        "full_target_conjunction_count": len(full_target_rows),
        "full_target_conjunction_bad_count": len(full_target_bad_rows),
        "full_target_lower_predecessor_pairs": full_target_pairs,
        "full_target_rows": sample(full_target_rows, limit=20),
        "exact_two_trigger_boundary_phase_count": len(
            exact_trigger_boundary_phase_rows,
        ),
        "exact_two_trigger_boundary_phase_bad_count": len(
            exact_trigger_boundary_phase_bad_rows,
        ),
        "exact_two_trigger_boundary_phase_rows": sample(
            exact_trigger_boundary_phase_rows,
            limit=20,
        ),
    }


def main() -> int:
    """Run the high-signal extraction."""
    rows = load_rows()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    write_jsonl(OUTPUT_DIR / "rows.jsonl", rows)
    payload = summary(rows)
    write_json(OUTPUT_DIR / "summary.json", payload)
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
