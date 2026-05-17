#!/usr/bin/env python3
"""
Grok Round 5: Test whether DirectedPublicReentry2OddExit + Rres=o4|o4
forces same_mod36 on the full high-signal public-containing surface
(without the p % 36 == q % 36 pre-filter).
"""

from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path
from typing import Any

THIS_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = THIS_DIR / "output" / "grok_round5_same_phase_boundary_test"

HIGH_SIGNAL_CONTAINING = "o6_d4_a6_d4_odd"
WHEEL_OPEN = {1, 7, 11, 13, 17, 19, 23, 29}


def load_enriched_rows(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def get_residue(s: str) -> str:
    m = re.search(r"^(o[0-9]+)", s or "")
    return m.group(1) if m else "?"


def compute_flags(row: dict[str, Any]) -> dict[str, Any]:
    p = int(row["p"])
    q = int(row["q"])

    p_mod36 = p % 36
    q_mod36 = q % 36
    same_phase = (p_mod36 == q_mod36)

    # Public
    prev_gap = row["public_previous_gap"]
    next_gap = row["public_following_gap"]

    public_word = str(row["public_word"])
    public_gwr_side = str(row["public_gwr_side"])
    public_key = f"{public_word}|{public_gwr_side}"

    prev_open_offset = int(prev_gap["first_open_offset"])
    prev_d = int(prev_gap["winner_d"])
    prev_exact = str(prev_gap["exact_type_key"])
    prev_parity = "even" if prev_exact.endswith("_even") else "odd" if prev_exact.endswith("_odd") else "?"

    containing_position = str(row["public_containing_phase_bucket"])
    containing_exact_type = str(row["public_containing_exact_type_key"])

    next_open_offset = int(next_gap["first_open_offset"])
    next_d = int(next_gap["winner_d"])
    next_exact = str(next_gap["exact_type_key"])
    next_parity = "even" if next_exact.endswith("_even") else "odd" if next_exact.endswith("_odd") else "?"
    next_open_type = get_residue(str(next_gap["reduced_state"]))

    # Right boundary
    p_right_label = get_residue(str(row["p_right_reduced_state"]))
    q_right_label = get_residue(str(row["q_right_reduced_state"]))
    right_labels = sorted([p_right_label, q_right_label])
    rres_o4_o4 = (right_labels == ["o4", "o4"])

    # Lower terminal lift
    p_left_gap_width = int(row["p_left_gap_width"])
    p_left_winner_offset = int(row["p_left_winner_offset"])
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

    return {
        "band": row["band"],
        "case_id": row["case_id"],
        "public_key": public_key,
        "public_gwr_side": public_gwr_side,
        "p_mod36": p_mod36,
        "q_mod36": q_mod36,
        "same_phase": same_phase,
        "directed_reentry2_odd": directed_reentry2_odd,
        "rres_o4_o4": rres_o4_o4,
        "lower_terminal_four_slot": lower_terminal_four_slot,
        "factor_mod180_lane": f"{p % 180}|{q % 180}",
        "lower_predecessor_pair": ((p - p_left_gap_width) % 30, lower_predecessor_width),
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
    out_dir = base / "grok_round5_same_phase_boundary_test"
    out_dir.mkdir(parents=True, exist_ok=True)

    corpus_dirs = sorted(base.glob("enriched_multiplication_map_corpus_*"))

    high_signal_rows = []
    target_rows = []
    falsifier_rows = []
    non_same_target_rows = []
    same_target_rows = []

    for cdir in corpus_dirs:
        for row in load_enriched_rows(cdir / "enriched_rows.jsonl"):
            if row.get("public_containing_exact_type_key") != "o6_d4_a6_d4_odd":
                continue

            flags = compute_flags(row)
            high_signal_rows.append(flags)

            if flags["directed_reentry2_odd"] and flags["rres_o4_o4"]:
                target_rows.append(flags)

                if not flags["lower_terminal_four_slot"]:
                    falsifier_rows.append(flags)

                if flags["same_phase"]:
                    same_target_rows.append(flags)
                else:
                    non_same_target_rows.append(flags)

    # Signature counts (using the 4-tuple)
    def get_signature(r):
        return f"{r['prev_parity']}|{r['containing_position']}|{r['next_open_type']}|{r['next_parity']}"

    target_signature_counts = Counter(get_signature(r) for r in target_rows)
    non_same_signature_counts = Counter(get_signature(r) for r in non_same_target_rows)

    target_lane_counts = Counter(r["factor_mod180_lane"] for r in target_rows)
    non_same_lane_counts = Counter(r["factor_mod180_lane"] for r in non_same_target_rows)

    summary = {
        "rule_id": "grok_round5_same_phase_boundary_test_v1",
        "public_containing_surface_row_count": len(high_signal_rows),
        "odd_exit_rres_o4o4_row_count": len(target_rows),
        "odd_exit_rres_o4o4_same_mod36_count": len(same_target_rows),
        "odd_exit_rres_o4o4_non_same_mod36_count": len(non_same_target_rows),
        "same_phase_derived_on_measured_surface": len(non_same_target_rows) == 0,
        "same_phase_target_lift_falsifier_count": sum(1 for r in same_target_rows if not r["lower_terminal_four_slot"]),
        "non_same_phase_target_lift_falsifier_count": sum(1 for r in non_same_target_rows if not r["lower_terminal_four_slot"]),
        "target_signature_counts": dict(target_signature_counts),
        "non_same_phase_signature_counts": dict(non_same_signature_counts),
        "target_factor_mod180_lane_counts": dict(target_lane_counts),
        "non_same_phase_factor_mod180_lane_counts": dict(non_same_lane_counts),
        "theorem_status": "hypothesis_not_proved",
    }

    (out_dir / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

    with (out_dir / "target_rows.jsonl").open("w", encoding="utf-8") as f:
        for r in target_rows:
            f.write(json.dumps(r) + "\n")

    with (out_dir / "non_same_phase_target_rows.jsonl").open("w", encoding="utf-8") as f:
        for r in non_same_target_rows:
            f.write(json.dumps(r) + "\n")

    with (out_dir / "same_phase_target_rows.jsonl").open("w", encoding="utf-8") as f:
        for r in same_target_rows:
            f.write(json.dumps(r) + "\n")

    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
