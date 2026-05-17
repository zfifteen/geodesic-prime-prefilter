#!/usr/bin/env python3
"""
Grok Round 4: Test of DirectedPublicReentry2OddExit + Rres=o4|o4 => lower-terminal four-slot lift
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

THIS_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = THIS_DIR / "output" / "grok_round4_odd_exit_lift_test"

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

    # Public
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
    next_open_type = get_residue(next_gap.get("reduced_state", ""))

    # Right boundary
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

    start = lower_predecessor_left_endpoint + 1
    end = lower_predecessor_left_endpoint + lower_predecessor_width
    open_count = sum(1 for v in range(start, end) if v % 30 in WHEEL_OPEN)

    lower_terminal_four_slot = lower_terminal_closure and (open_count == 4)

    # DirectedPublicReentry2OddExit
    directed_reentry2_odd = (
        containing_exact_type == HIGH_SIGNAL_CONTAINING
        and prev_open_offset == 4
        and prev_d <= 4
        and next_d <= 4
        and next_parity == "odd"
        and public_gwr_side == "at_winner"
        and (prev_parity, containing_position, next_open_type) in {("even", "mid", "o4"), ("odd", "early", "o6")}
    )

    # Phase width complement
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
        "directed_reentry2_odd": directed_reentry2_odd,
        "rres_o4_o4": rres_o4_o4,
        "lower_terminal_four_slot": lower_terminal_four_slot,
        "phase_width_complement": phase_width_complement,
        "factor_mod180_lane": f"{p % 180}|{q % 180}",
        "lower_predecessor_pair": ((p - p_left_gap_width) % 30, lower_predecessor_width),
        "phase_width_pair": (p_mod36, prev_gap_width_mod30),
        "prev_parity": prev_parity,
        "containing_position": containing_position,
        "next_open_type": next_open_type,
        "next_parity": next_parity,
        "prev_open_offset": prev_open_offset,
        "prev_d": prev_d,
        "next_d": next_d,
        "lower_predecessor_open_slot_count": open_count,
    }


def main():
    base = Path("research/06-cryptology-rsa/experiments/pedk/rsa-v2/gap-compatibility/core-evidence/output")
    out_dir = base / "grok_round4_odd_exit_lift_test"
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

            if flags["directed_reentry2_odd"] and flags["rres_o4_o4"]:
                target_rows.append(flags)
                if not flags["lower_terminal_four_slot"]:
                    falsifier_rows.append(flags)

    # Signature mapping
    signature_map = {}
    for r in target_rows:
        if r["lower_terminal_four_slot"]:
            key = f"{r['prev_parity']}|{r['containing_position']}|{r['next_open_type']}|{r['next_parity']}"
            if key not in signature_map:
                signature_map[key] = []
            signature_map[key].append({
                "factor_mod180_lane": r["factor_mod180_lane"],
                "phase_width_pair": r.get("phase_width_pair"),
                "lower_predecessor_pair": r["lower_predecessor_pair"],
                "open_slot_count": r["lower_predecessor_open_slot_count"],
            })

    summary = {
        "rule_id": "grok_round4_odd_exit_lift_test_v1",
        "high_signal_same_phase_row_count": len(high_signal_rows),
        "directed_public_reentry2_odd_row_count": len([r for r in high_signal_rows if r["directed_reentry2_odd"]]),
        "directed_public_reentry2_odd_rres_o4o4_row_count": len(target_rows),
        "falsifier_count": len(falsifier_rows),
        "phase_width_complement_automatic_on_target": all(r.get("phase_width_complement", False) for r in target_rows),
    }

    (out_dir / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

    with (out_dir / "target_rows.jsonl").open("w", encoding="utf-8") as f:
        for r in target_rows:
            f.write(json.dumps(r) + "\n")

    with (out_dir / "falsifier_rows.jsonl").open("w", encoding="utf-8") as f:
        for r in falsifier_rows:
            f.write(json.dumps(r) + "\n")

    # Standalone signature_mapping.json in the required clean format
    clean_mapping = {}
    for r in target_rows:
        if r["lower_terminal_four_slot"]:
            key = f"{r['prev_parity']}|{r['containing_position']}|{r['next_open_type']}|{r['next_parity']}"
            if key not in clean_mapping:
                clean_mapping[key] = []
            clean_mapping[key].append({
                "factor_mod180_lane": r["factor_mod180_lane"],
                "phase_width_pair": r.get("phase_width_pair"),
                "lower_predecessor_pair": r["lower_predecessor_pair"],
                "open_slot_count": r["lower_predecessor_open_slot_count"],
            })

    (out_dir / "signature_mapping.json").write_text(json.dumps(clean_mapping, indent=2), encoding="utf-8")

    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()