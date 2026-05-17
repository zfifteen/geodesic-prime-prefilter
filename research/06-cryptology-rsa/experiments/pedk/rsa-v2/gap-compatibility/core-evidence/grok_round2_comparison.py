#!/usr/bin/env python3
"""
Grok Round 2: Good vs Bad row comparison on the high-signal surface.
"""

from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

THIS_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = THIS_DIR / "output" / "grok_round2_comparison"

HIGH_SIGNAL_CONTAINING = "o6_d4_a6_d4_odd"

EXACT_PUBLIC_TRIGGERS = {
    "prev=o4_d4_even|d<=4|containing=o6_d4_a6_d4_odd@mid|next=o4_d4_odd|d<=4|at_winner",
    "prev=o4_d4_odd|d<=4|containing=o6_d4_a6_d4_odd@early|next=o6_d4_odd|d<=4|at_winner",
}

EXPECTED_PHASE_WIDTH = {(7, 24), (13, 12)}


def load_enriched_rows(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def get_residue(s: str) -> str:
    m = re.search(r"^(o[0-9]+)", s or "")
    return m.group(1) if m else "?"


def compute_flags(row: dict[str, Any]) -> dict[str, Any]:
    p = int(row.get("p", 0))
    q = int(row.get("q", 0))
    N = int(row.get("N", 0))

    p_mod36 = p % 36
    q_mod36 = q % 36

    prev_gap = row.get("public_previous_gap", {}) or {}
    containing_gap = row.get("public_containing_gap", {}) or {}

    public_previous_gap_width = int(prev_gap.get("gap_width", 0))
    public_previous_gap_width_mod30 = public_previous_gap_width % 30
    public_previous_first_open = int(prev_gap.get("first_open_offset", 0))

    public_n_offset_from_left = int(row.get("public_n_offset_from_left", 0))
    public_left_endpoint = N - public_n_offset_from_left
    public_previous_left_endpoint = public_left_endpoint - public_previous_gap_width
    public_previous_left_mod30 = public_previous_left_endpoint % 30

    containing_key = row.get("public_containing_exact_type_key", "")
    public_selected_load = 4 if containing_key == HIGH_SIGNAL_CONTAINING else 0

    public_word = row.get("public_word", "")
    public_gwr_side = str(row.get("public_gwr_side", ""))
    public_key = f"{public_word}|{public_gwr_side}"

    # Right boundary using residue labels
    p_right_label = get_residue(row.get("p_right_reduced_state", ""))
    q_right_label = get_residue(row.get("q_right_reduced_state", ""))
    endpoint_right_boundary = max([int(x[1:]) for x in [p_right_label, q_right_label] if x.startswith("o")])
    boundary_balanced = (public_selected_load == 4 and endpoint_right_boundary == 4)
    right_boundary_o4o4 = sorted([p_right_label, q_right_label]) == ["o4", "o4"]

    # Terminal left on p
    p_left_gap_width = int(row.get("p_left_gap_width", 0))
    p_left_winner_offset = int(row.get("p_left_winner_offset", 0))
    terminal_distance = p_left_gap_width - p_left_winner_offset
    left_bridge_width = p_left_gap_width
    lower_terminal_closure = (terminal_distance == 2 and left_bridge_width >= 20)

    lower_predecessor_width = p_left_winner_offset
    lower_predecessor_left_endpoint = p - p_left_gap_width
    lower_predecessor_left_mod30 = lower_predecessor_left_endpoint % 30

    # Four slot count
    start = lower_predecessor_left_endpoint + 1
    end = lower_predecessor_left_endpoint + lower_predecessor_width
    open_count = sum(1 for v in range(start, end) if v % 30 in {1,7,11,13,17,19,23,29})
    lower_terminal_four_slot = lower_terminal_closure and open_count == 4

    public_left_neighbor_gate = (
        public_previous_first_open == 4
        and public_previous_left_mod30 in (7, 13, 19)
        and containing_key == HIGH_SIGNAL_CONTAINING
    )

    phase_width_complement = (p_mod36, public_previous_gap_width_mod30) in EXPECTED_PHASE_WIDTH

    lower_predecessor_pair = (lower_predecessor_left_mod30, lower_predecessor_width)

    # Next gap fields
    next_gap = row.get("public_following_gap", {}) or {}
    next_exact = next_gap.get("exact_type_key", "")

    # Prev exact for parity
    prev_exact = prev_gap.get("exact_type_key", "")

    return {
        "band": row.get("band"),
        "case_id": row.get("case_id"),
        "public_key": public_key,
        "public_gwr_side": public_gwr_side,
        "public_word": public_word,
        "p_mod36": p_mod36,
        "q_mod36": q_mod36,
        "phase_width_complement": phase_width_complement,
        "boundary_balanced": boundary_balanced,
        "right_boundary_o4o4": right_boundary_o4o4,
        "lower_terminal_four_slot": lower_terminal_four_slot,
        "public_left_neighbor_gate": public_left_neighbor_gate,
        "lower_predecessor_pair": lower_predecessor_pair,
        "lower_predecessor_open_slot_count": open_count,
        "prev_open_offset": public_previous_first_open,
        "prev_parity": "even" if prev_exact.endswith("_even") else "odd" if prev_exact.endswith("_odd") else "?",
        "prev_d": int(prev_gap.get("winner_d", 0)),
        "containing_position": row.get("public_containing_phase_bucket"),
        "containing_exact_type": containing_key,
        "next_open_offset": int(next_gap.get("first_open_offset", 0)),
        "next_d": int(next_gap.get("winner_d", 0)),
        "next_parity": "even" if next_exact.endswith("_even") else "odd" if next_exact.endswith("_odd") else "?",
        "next_reduced_state": next_gap.get("reduced_state", ""),
        "next_open_type": get_residue(next_gap.get("reduced_state", "")),
        "factor_mod180_lane": f"{p % 180}|{q % 180}",
        "phase_width_pair": (p_mod36, public_previous_gap_width_mod30),
        "lower_predecessor_pair": lower_predecessor_pair,
        "lower_predecessor_open_slot_count": open_count,
    }


def main():
    base = Path("research/06-cryptology-rsa/experiments/pedk/rsa-v2/gap-compatibility/core-evidence/output")
    out_dir = base / "grok_round2_comparison"
    out_dir.mkdir(parents=True, exist_ok=True)

    corpus_dirs = sorted(base.glob("enriched_multiplication_map_corpus_*"))

    high_signal_rows = []
    for cdir in corpus_dirs:
        for row in load_enriched_rows(cdir / "enriched_rows.jsonl"):
            if row.get("public_containing_exact_type_key") != "o6_d4_a6_d4_odd":
                continue
            p = int(row.get("p", 0))
            q = int(row.get("q", 0))
            if p % 36 != q % 36:
                continue
            flags = compute_flags(row)
            high_signal_rows.append(flags)

    good_rows = []
    bad_rows = []

    for r in high_signal_rows:
        is_exact_trigger = r["public_key"] in {
            "prev=o4_d4_even|d<=4|containing=o6_d4_a6_d4_odd@mid|next=o4_d4_odd|d<=4|at_winner",
            "prev=o4_d4_odd|d<=4|containing=o6_d4_a6_d4_odd@early|next=o6_d4_odd|d<=4|at_winner",
        }

        if (is_exact_trigger and r["right_boundary_o4o4"] and r["phase_width_complement"]
                and r["lower_terminal_four_slot"]):
            good_rows.append(r)

        if (r["public_gwr_side"] == "at_winner" and r["public_left_neighbor_gate"]
                and r["right_boundary_o4o4"] and r["phase_width_complement"]
                and not r["lower_terminal_four_slot"]):
            bad_rows.append(r)

    # Field comparison
    comparison_fields = [
        "prev_open_offset", "prev_parity", "containing_position", "containing_exact_type",
        "factor_mod180_lane", "phase_width_pair", "lower_predecessor_pair",
        "lower_predecessor_open_slot_count"
    ]

    good_values = defaultdict(set)
    bad_values = defaultdict(set)

    for r in good_rows:
        for f in comparison_fields:
            good_values[f].add(str(r.get(f)))

    for r in bad_rows:
        for f in comparison_fields:
            bad_values[f].add(str(r.get(f)))

    differentiating = {}
    for f in comparison_fields:
        only_in_good = good_values[f] - bad_values[f]
        if only_in_good:
            differentiating[f] = list(only_in_good)

    # Exact ChatGPT predicate check
    def matches_proposed_predicate(r):
        prev_par = r.get("prev_parity")
        cont_pos = r.get("containing_position")
        next_type = r.get("next_open_type")
        prev_off = r.get("prev_open_offset")
        prev_d = r.get("prev_d", 99)
        next_d = r.get("next_d", 99)
        gwr_side = r.get("public_gwr_side")

        tuple_ok = (prev_par, cont_pos, next_type) in {("even", "mid", "o4"), ("odd", "early", "o6")}
        return (
            tuple_ok
            and prev_off == 4
            and prev_d <= 4
            and next_d <= 4
            and gwr_side == "at_winner"
        )

    good_predicate_hits = sum(1 for r in good_rows if matches_proposed_predicate(r))
    bad_predicate_hits = sum(1 for r in bad_rows if matches_proposed_predicate(r))

    summary = {
        "high_signal_row_count": len(high_signal_rows),
        "good_row_count": len(good_rows),
        "bad_row_count": len(bad_rows),
        "differentiating_fields": differentiating,
        "proposed_directed_reentry_good_hits": good_predicate_hits,
        "proposed_directed_reentry_bad_hits": bad_predicate_hits,
        "proposed_directed_reentry_separates_good_from_bad": (good_predicate_hits == 2 and bad_predicate_hits == 0),
    }

    (out_dir / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

    with (out_dir / "good_rows.jsonl").open("w", encoding="utf-8") as f:
        for r in good_rows:
            f.write(json.dumps(r) + "\n")

    with (out_dir / "bad_rows.jsonl").open("w", encoding="utf-8") as f:
        for r in bad_rows:
            f.write(json.dumps(r) + "\n")

    (out_dir / "field_comparison.json").write_text(json.dumps(differentiating, indent=2), encoding="utf-8")

    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()