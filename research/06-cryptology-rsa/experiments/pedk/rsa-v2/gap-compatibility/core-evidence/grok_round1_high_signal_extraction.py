#!/usr/bin/env python3
"""
Grok Round 1: High-signal surface extraction and cross-tabulation
for the o6_d4_a6_d4_odd + same_mod36 surface.

This is a minimal, self-contained extraction script.
"""

from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

THIS_DIR = Path(__file__).resolve().parent
OUTPUT_ROOT = THIS_DIR / "output" / "grok_round1_high_signal_extraction"

# High-signal filter
HIGH_SIGNAL_CONTAINING = "o6_d4_a6_d4_odd"

# Wheel-open residues mod 30
WHEEL_OPEN = {1, 7, 11, 13, 17, 19, 23, 29}

# The two expected active (p_mod36, public_previous_gap_width_mod30) pairs
EXPECTED_PHASE_WIDTH = {(7, 24), (13, 12)}

# Expected landing pairs under the active surface
EXPECTED_LANDING = {(19, 22), (29, 18)}

# Exact two public triggers (full public_word strings)
EXACT_PUBLIC_TRIGGERS = {
    "prev=o4_d4_even|d<=4|containing=o6_d4_a6_d4_odd@mid|next=o4_d4_odd|d<=4|at_winner",
    "prev=o4_d4_odd|d<=4|containing=o6_d4_a6_d4_odd@early|next=o6_d4_odd|d<=4|at_winner",
}


def load_enriched_rows(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            rows.append(json.loads(line))
    return rows


def compute_flags(row: dict[str, Any]) -> dict[str, Any]:
    """Compute all required boolean and derived fields for a high-signal row."""

    p = int(row["p"])
    q = int(row["q"])
    N = int(row["N"])

    # Basic mod conditions (already filtered, but recompute for clarity)
    p_mod36 = p % 36
    q_mod36 = q % 36
    same_mod36 = (p_mod36 == q_mod36)

    # Public previous gap
    prev_gap = row.get("public_previous_gap", {}) or {}
    public_previous_gap_width = int(prev_gap.get("gap_width", 0))
    public_previous_gap_width_mod30 = public_previous_gap_width % 30

    public_n_offset_from_left = int(row.get("public_n_offset_from_left", 0))
    public_left_endpoint = N - public_n_offset_from_left
    public_left_endpoint_mod30 = public_left_endpoint % 30

    # Public containing
    containing_key = row.get("public_containing_exact_type_key", "")
    public_selected_load = 4 if containing_key == HIGH_SIGNAL_CONTAINING else 0

    # Right boundary balance using first right-open residue labels (o2/o4/o6)
    p_right_reduced = row.get("p_right_reduced_state", "")
    q_right_reduced = row.get("q_right_reduced_state", "")

    def get_residue(s: str) -> str:
        m = re.search(r"^(o[0-9]+)", s)
        return m.group(1) if m else "?"

    def get_residue_num(s: str) -> int:
        m = re.search(r"^(o[0-9]+)", s)
        return int(m.group(1)[1:]) if m else 0

    labels = [get_residue_num(p_right_reduced), get_residue_num(q_right_reduced)]
    endpoint_right_boundary = max(labels) if labels else 0
    endpoint_transport_defect = endpoint_right_boundary - public_selected_load
    boundary_balanced = (public_selected_load == 4 and endpoint_right_boundary == 4)

    right_res_str = f"{get_residue(p_right_reduced)}|{get_residue(q_right_reduced)}"
    right_boundary_o4o4 = (sorted([get_residue(p_right_reduced), get_residue(q_right_reduced)]) == ["o4", "o4"])

    # Terminal-left closure on lower factor (p)
    p_left_gap_width = int(row.get("p_left_gap_width", 0))
    p_left_winner_offset = int(row.get("p_left_winner_offset", 0))
    terminal_distance = p_left_gap_width - p_left_winner_offset
    left_bridge_width = p_left_gap_width
    lower_terminal_closure = (terminal_distance == 2) and (left_bridge_width >= 20)

    # Lower predecessor
    lower_predecessor_width = p_left_winner_offset
    lower_predecessor_left_endpoint = p - p_left_gap_width
    lower_predecessor_left_mod30 = lower_predecessor_left_endpoint % 30
    immediate_left_point = p - terminal_distance
    immediate_left_mod30 = immediate_left_point % 30

    lower_predecessor_pair = (lower_predecessor_left_mod30, lower_predecessor_width)

    # Phase-width complement (candidate for the active surface)
    phase_width_key = (p_mod36, public_previous_gap_width_mod30)
    phase_width_complement = phase_width_key in EXPECTED_PHASE_WIDTH

    # Public left-neighbor gate: previous public gap's left endpoint + first_open == 4
    public_previous_gap = row.get("public_previous_gap", {}) or {}
    public_previous_gap_width = int(public_previous_gap.get("gap_width", 0))
    public_previous_left_endpoint = public_left_endpoint - public_previous_gap_width
    public_previous_left_mod30 = public_previous_left_endpoint % 30
    public_previous_first_open = int(public_previous_gap.get("first_open_offset", 0))

    public_left_neighbor_gate = (
        public_previous_first_open == 4
        and public_previous_left_mod30 in (7, 13, 19)
        and containing_key == HIGH_SIGNAL_CONTAINING
    )

    # Canonical public key used for exact trigger matching
    public_gwr_side = str(row.get("public_gwr_side", ""))
    public_key = f"{row.get('public_word', '')}|{public_gwr_side}"

    # Four-slot open count (strict open interval)
    lower_predecessor_open_slot_residues = []
    start = lower_predecessor_left_endpoint + 1
    end = lower_predecessor_left_endpoint + lower_predecessor_width
    for val in range(start, end):
        res = val % 30
        if res in WHEEL_OPEN:
            lower_predecessor_open_slot_residues.append(res)

    lower_predecessor_open_slot_count = len(lower_predecessor_open_slot_residues)

    lower_terminal_four_slot = (
        lower_terminal_closure and lower_predecessor_open_slot_count == 4
    )

    # Right boundary residues string for the active surface
    right_boundary_residues = right_res_str

    return {
        "band": row.get("band"),
        "case_id": row.get("case_id"),
        "N": N,
        "p": p,
        "q": q,
        "p_mod36": p_mod36,
        "q_mod36": q_mod36,
        "same_mod36": same_mod36,
        "public_containing_exact_type_key": containing_key,
        "public_left_endpoint_mod30": public_left_endpoint_mod30,
        "public_previous_gap_width_mod30": public_previous_gap_width_mod30,
        "public_selected_load": public_selected_load,
        "endpoint_right_boundary": endpoint_right_boundary,
        "endpoint_transport_defect": endpoint_transport_defect,
        "boundary_balanced": boundary_balanced,
        "right_boundary_residues": right_boundary_residues,
        "right_boundary_o4o4": right_boundary_o4o4,
        "phase_width_complement": phase_width_complement,
        "phase_width_key": phase_width_key,
        "lower_terminal_closure": lower_terminal_closure,
        "lower_predecessor_width": lower_predecessor_width,
        "lower_predecessor_left_mod30": lower_predecessor_left_mod30,
        "lower_predecessor_pair": lower_predecessor_pair,
        "lower_predecessor_open_slot_count": lower_predecessor_open_slot_count,
        "lower_predecessor_open_slot_residues": lower_predecessor_open_slot_residues,
        "lower_terminal_four_slot": lower_terminal_four_slot,
        "public_left_neighbor_gate": public_left_neighbor_gate,
        "terminal_distance": terminal_distance,
        "left_bridge_width": left_bridge_width,
        "public_key": public_key,
        "public_gwr_side": public_gwr_side,
        "is_compressed_full_target": (
            public_gwr_side == "at_winner"
            and public_left_neighbor_gate
            and right_boundary_o4o4
            and phase_width_complement
        ),
        "is_exact_two_trigger_boundary_phase": (
            public_key in EXACT_PUBLIC_TRIGGERS
            and right_boundary_o4o4
            and phase_width_complement
        ),
    }


def main() -> None:
    base = Path("research/06-cryptology-rsa/experiments/pedk/rsa-v2/gap-compatibility/core-evidence/output")
    output_dir = base / "grok_round1_high_signal_extraction"
    output_dir.mkdir(parents=True, exist_ok=True)

    # Discover all enriched corpus directories
    pattern = "enriched_multiplication_map_corpus_*"
    corpus_dirs = sorted(base.glob(pattern))

    high_signal_rows: list[dict] = []
    forward_band = "15001_17000"

    for corpus_dir in corpus_dirs:
        jsonl = corpus_dir / "enriched_rows.jsonl"
        if not jsonl.exists():
            continue
        rows = []
        for line in jsonl.read_text(encoding="utf-8").splitlines():
            if line.strip():
                rows.append(json.loads(line))

        for row in rows:
            containing = row.get("public_containing_exact_type_key")
            p = int(row.get("p", 0))
            q = int(row.get("q", 0))
            if containing != HIGH_SIGNAL_CONTAINING:
                continue
            if p % 36 != q % 36:
                continue

            flags = compute_flags(row)
            high_signal_rows.append(flags)

    # Cross-tabs (global across all windows)
    cross1 = Counter()
    cross2 = Counter()
    cross3 = Counter()

    for r in high_signal_rows:
        key1 = (str(r["boundary_balanced"]), str(r["phase_width_complement"]), str(r["lower_terminal_closure"]))
        cross1[key1] += 1

        key2 = (str(r["phase_width_complement"]), str(r["lower_predecessor_pair"]))
        cross2[key2] += 1

        key3 = (str(r["public_left_neighbor_gate"]), str(r["boundary_balanced"]), str(r["lower_terminal_four_slot"]))
        cross3[key3] += 1

    # Global (all-window) checks
    global_phase_but_not_four_slot = sum(
        1 for r in high_signal_rows
        if r["phase_width_complement"] and not r["lower_terminal_four_slot"]
    )

    global_four_slot_without_left_gate = sum(
        1 for r in high_signal_rows
        if r["lower_terminal_four_slot"] and not r["public_left_neighbor_gate"]
    )

    # Exact two public triggers + boundary_balanced + phase_width_complement
    compressed_full_target_count = 0
    compressed_full_target_bad_count = 0
    exact_two_trigger_boundary_phase_count = 0
    exact_two_trigger_boundary_phase_bad_count = 0
    exact_two_trigger_rows = []

    for r in high_signal_rows:
        if r.get("is_compressed_full_target"):
            compressed_full_target_count += 1
            if not r.get("lower_terminal_four_slot"):
                compressed_full_target_bad_count += 1

        if r.get("is_exact_two_trigger_boundary_phase"):
            exact_two_trigger_boundary_phase_count += 1
            if not r.get("lower_terminal_four_slot"):
                exact_two_trigger_boundary_phase_bad_count += 1
            exact_two_trigger_rows.append({
                "band": r.get("band"),
                "case_id": r.get("case_id"),
                "public_key": r.get("public_key"),
                "lower_predecessor_pair": r.get("lower_predecessor_pair"),
                "lower_terminal_four_slot": r.get("lower_terminal_four_slot"),
            })

    # Specific checks on the forward band only (for compatibility with previous reporting)
    forward_rows = [r for r in high_signal_rows if r["band"] == forward_band]

    falsifier_count = sum(
        1 for r in forward_rows
        if r["phase_width_complement"] and not r["lower_terminal_four_slot"]
    )

    missing_gate_count = sum(
        1 for r in forward_rows
        if r["lower_terminal_four_slot"] and not r["public_left_neighbor_gate"]
    )

    expected_pairs_seen = set()
    for r in forward_rows:
        if (
            r["phase_width_complement"]
            and r["lower_terminal_four_slot"]
            and r["public_left_neighbor_gate"]
            and r["boundary_balanced"]
            and r["right_boundary_o4o4"]
        ):
            expected_pairs_seen.add(r["lower_predecessor_pair"])

    expected_unique = len(expected_pairs_seen) == 2 and expected_pairs_seen == EXPECTED_LANDING

    summary = {
        "rule_id": "grok_round1_high_signal_extraction_v1",
        "high_signal_surface_row_count": len(high_signal_rows),
        "forward_band": forward_band,
        "forward_band_high_signal_row_count": len(forward_rows),
        "cross_tab_boundary_x_phase_x_terminal": {str(k): v for k, v in cross1.items()},
        "cross_tab_phase_x_lower_predecessor_pair": {str(k): v for k, v in cross2.items()},
        "cross_tab_public_left_gate_x_boundary_x_four_slot": {str(k): v for k, v in cross3.items()},
        # Global (all windows) versions of the requested checks
        "phase_width_complement_true_but_not_four_slot_all_windows": global_phase_but_not_four_slot,
        "lower_terminal_four_slot_true_without_public_left_gate_all_windows": global_four_slot_without_left_gate,
        "compressed_full_target_count": compressed_full_target_count,
        "compressed_full_target_bad_count": compressed_full_target_bad_count,
        "exact_two_trigger_boundary_phase_count": exact_two_trigger_boundary_phase_count,
        "exact_two_trigger_boundary_phase_bad_count": exact_two_trigger_boundary_phase_bad_count,
        "exact_two_trigger_boundary_phase_rows": exact_two_trigger_rows,
        # Forward-band specific (for continuity)
        "phase_width_complement_true_but_not_four_slot_in_forward": falsifier_count,
        "lower_terminal_four_slot_true_without_public_left_gate_in_forward": missing_gate_count,
        "expected_active_pairs_unique_under_full_conjunction_in_forward": expected_unique,
        "expected_active_pairs_observed": list(expected_pairs_seen),
    }

    (output_dir / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True), encoding="utf-8")

    # Also emit a small JSONL of the forward band high-signal rows for inspection
    forward_jsonl = output_dir / "forward_band_high_signal_rows.jsonl"
    with forward_jsonl.open("w", encoding="utf-8") as f:
        for r in forward_rows:
            f.write(json.dumps(r) + "\n")

    print(json.dumps(summary, indent=2, sort_keys=True))
    print(f"\nWrote summary to {output_dir / 'summary.json'}")
    print(f"Wrote forward-band sample to {forward_jsonl}")


if __name__ == "__main__":
    main()
