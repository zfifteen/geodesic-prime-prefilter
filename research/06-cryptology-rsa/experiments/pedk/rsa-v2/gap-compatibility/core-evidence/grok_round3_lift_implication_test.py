#!/usr/bin/env python3
"""
Grok Round 3 (corrected): DirectedPublicReentry2 + Rres=o4|o4 => lower-terminal four-slot lift
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

THIS_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = THIS_DIR / "output" / "grok_round3_lift_implication_test"

HIGH_SIGNAL_CONTAINING = "o6_d4_a6_d4_odd"
WHEEL_OPEN = {1, 7, 11, 13, 17, 19, 23, 29}

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
    same_phase = (p_mod36 == q_mod36)

    # Public fields
    prev_gap = row.get("public_previous_gap", {}) or {}
    containing_gap = row.get("public_containing_gap", {}) or {}
    next_gap = row.get("public_following_gap", {}) or {}

    public_word = row.get("public_word", "")
    public_gwr_side = str(row.get("public_gwr_side", ""))
    public_key = f"{public_word}|{public_gwr_side}"

    prev_open_offset = int(prev_gap.get("first_open_offset", 0))
    prev_d = int(prev_gap.get("winner_d", 0))
    prev_exact = prev_gap.get("exact_type_key", "")
    prev_parity = "even" if prev_exact.endswith("_even") else "odd" if prev_exact.endswith("_odd") else "?"

    containing_position = containing_gap.get("phase_bucket", row.get("public_containing_phase_bucket", ""))
    containing_exact_type = row.get("public_containing_exact_type_key", "")

    next_open_offset = int(next_gap.get("first_open_offset", 0))
    next_d = int(next_gap.get("winner_d", 0))
    next_exact = next_gap.get("exact_type_key", "")
    next_parity = "even" if next_exact.endswith("_even") else "odd" if next_exact.endswith("_odd") else "?"
    next_reduced_state = next_gap.get("reduced_state", "")
    next_open_type = get_residue(next_reduced_state)

    # Right boundary (Rres)
    p_right_label = get_residue(row.get("p_right_reduced_state", ""))
    q_right_label = get_residue(row.get("q_right_reduced_state", ""))
    right_labels = sorted([p_right_label, q_right_label])
    rres_o4_o4 = (right_labels == ["o4", "o4"])

    # Lower terminal lift
    p_left_gap_width = int(row.get("p_left_gap_width", 0))
    p_left_winner_offset = int(row.get("p_left_winner_offset", 0))
    terminal_distance = p_left_gap_width - p_left_winner_offset
    left_bridge_width = p_left_gap_width
    lower_terminal_closure = (terminal_distance == 2 and left_bridge_width >= 20)

    lower_predecessor_width = p_left_winner_offset
    lower_predecessor_left_endpoint = p - p_left_gap_width

    # Four-slot open count
    start = lower_predecessor_left_endpoint + 1
    end = lower_predecessor_left_endpoint + lower_predecessor_width
    open_count = sum(1 for v in range(start, end) if v % 30 in WHEEL_OPEN)

    lower_terminal_four_slot = lower_terminal_closure and (open_count == 4)

    # DirectedPublicReentry2
    directed_reentry2 = (
        containing_exact_type == HIGH_SIGNAL_CONTAINING
        and prev_open_offset == 4
        and prev_d <= 4
        and next_d <= 4
        and public_gwr_side == "at_winner"
        and (prev_parity, containing_position, next_open_type) in {("even", "mid", "o4"), ("odd", "early", "o6")}
    )

    # Phase width complement (for reporting)
    prev_gap_width_mod30 = int(prev_gap.get("gap_width", 0)) % 30
    phase_width_complement = (p_mod36, prev_gap_width_mod30) in EXPECTED_PHASE_WIDTH

    return {
        "band": row.get("band"),
        "case_id": row.get("case_id"),
        "public_key": public_key,
        "public_gwr_side": public_gwr_side,
        "p_mod36": p_mod36,
        "q_mod36": q_mod36,
        "same_phase": same_phase,
        "directed_reentry2": directed_reentry2,
        "rres_o4_o4": rres_o4_o4,
        "lower_terminal_four_slot": lower_terminal_four_slot,
        "phase_width_complement": phase_width_complement,
        "factor_mod180_lane": f"{p % 180}|{q % 180}",
        "lower_predecessor_pair": ((p - p_left_gap_width) % 30, lower_predecessor_width),
        "prev_parity": prev_parity,
        "containing_position": containing_position,
        "next_open_type": next_open_type,
        "prev_open_offset": prev_open_offset,
        "prev_d": prev_d,
        "next_d": next_d,
        "next_parity": next_parity,
    }


def main():
    base = Path("research/06-cryptology-rsa/experiments/pedk/rsa-v2/gap-compatibility/core-evidence/output")
    out_dir = base / "grok_round3_lift_implication_test"
    out_dir.mkdir(parents=True, exist_ok=True)

    corpus_dirs = sorted(base.glob("enriched_multiplication_map_corpus_*"))

    high_signal_rows = []
    target_rows = []
    falsifier_rows = []

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

            if flags["directed_reentry2"] and flags["rres_o4_o4"]:
                target_rows.append(flags)
                if not flags["lower_terminal_four_slot"]:
                    falsifier_rows.append(flags)

    summary = {
        "rule_id": "grok_round3_lift_implication_test_v1",
        "high_signal_same_phase_row_count": len(high_signal_rows),
        "directed_public_reentry2_row_count": len([r for r in high_signal_rows if r["directed_reentry2"]]),
        "directed_public_reentry2_rres_o4_o4_row_count": len(target_rows),
        "directed_public_reentry2_rres_o4_o4_falsifier_count": len(falsifier_rows),
        "falsifier_case_ids": [r["case_id"] for r in falsifier_rows],
        "phase_width_complement_target_count": sum(1 for r in target_rows if r["phase_width_complement"]),
        "phase_width_complement_falsifier_count": sum(1 for r in falsifier_rows if r["phase_width_complement"]),
        "next_parity_odd_target_count": sum(1 for r in target_rows if r.get("next_parity") == "odd"),
        "next_parity_odd_falsifier_count": sum(1 for r in falsifier_rows if r.get("next_parity") == "odd"),
    }

    (out_dir / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

    with (out_dir / "target_rows.jsonl").open("w", encoding="utf-8") as f:
        for r in target_rows:
            f.write(json.dumps(r) + "\n")

    with (out_dir / "falsifier_rows.jsonl").open("w", encoding="utf-8") as f:
        for r in falsifier_rows:
            f.write(json.dumps(r) + "\n")

    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()