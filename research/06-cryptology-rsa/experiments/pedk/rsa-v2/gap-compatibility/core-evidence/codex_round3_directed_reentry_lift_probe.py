#!/usr/bin/env python3
"""Round 3 test of directed public reentry forcing lower-terminal lift."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

from codex_round1_high_signal_probe import load_rows as load_round1_rows
from codex_round2_public_trigger_separator import (
    comparison_fields,
    corpus_row_index,
)
from first_gap_compatibility_check import write_json, write_jsonl


THIS_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = THIS_DIR / "output" / "codex_round3_directed_reentry_lift_probe"
RULE_ID = "pedk_codex_round3_directed_reentry_lift_probe_v1"
DIRECTED_REENTRY_TUPLES = {
    ("even", "mid", "o4"),
    ("odd", "early", "o6"),
}


def directed_public_reentry2(fields: dict[str, object]) -> bool:
    """Return the sharpened directed public reentry predicate."""
    return (
        fields["containing_exact_type"] == "o6_d4_a6_d4_odd"
        and fields["prev_open_offset"] == 4
        and int(fields["prev_d"]) <= 4
        and int(fields["next_d"]) <= 4
        and fields["public_gwr_side"] == "at_winner"
        and (
            fields["prev_parity"],
            fields["containing_position"],
            fields["next_open_type"],
        )
        in DIRECTED_REENTRY_TUPLES
    )


def annotated_rows() -> list[dict[str, object]]:
    """Return high-signal same-phase rows with directed reentry fields."""
    enriched = corpus_row_index()
    out = []
    for row in load_round1_rows():
        key = (str(row["window"]), str(row["case_id"]))
        fields = comparison_fields(row, enriched[key])
        payload = {
            "rule_id": RULE_ID,
            "window": row["window"],
            "case_id": row["case_id"],
            "public_key": row["public_key"],
            "directed_public_reentry2": directed_public_reentry2(fields),
            "rres_o4_o4": row["rres_o4_o4"],
            "same_mod36": True,
            "phase_width_complement": row["phase_width_complement"],
            "lower_terminal_four_slot": row["lower_terminal_four_slot"],
            "lower_terminal_closure": row["lower_terminal_closure"],
            "lower_predecessor_residue_width_pair": row[
                "lower_predecessor_residue_width_pair"
            ],
            "lower_predecessor_open_slot_count": row[
                "lower_predecessor_open_slot_count"
            ],
            "factor_mod180_lane": row["factor_mod180_lane"],
            "p_mod30": row["p_mod30"],
            "q_mod30": row["q_mod30"],
            "p_mod36": row["p_mod36"],
            "q_mod36": row["q_mod36"],
            "phase_width_pair": row["phase_width_pair"],
            "right_boundary_residues": row["right_boundary_residues"],
            **fields,
        }
        payload["directed_tuple"] = (
            f"{payload['prev_parity']}|{payload['containing_position']}|"
            f"{payload['next_open_type']}"
        )
        out.append(payload)
    return out


def count_by(rows: list[dict[str, object]], key: str) -> dict[str, int]:
    """Return JSON-safe counts by one row field."""
    counts = Counter(str(row[key]) for row in rows)
    return {value: counts[value] for value in sorted(counts)}


def compact_rows(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    """Return compact rows for summary output."""
    return [
        {
            "window": row["window"],
            "case_id": row["case_id"],
            "public_key": row["public_key"],
            "directed_tuple": row["directed_tuple"],
            "factor_mod180_lane": row["factor_mod180_lane"],
            "phase_width_pair": row["phase_width_pair"],
            "phase_width_complement": row["phase_width_complement"],
            "right_boundary_residues": row["right_boundary_residues"],
            "lower_predecessor_residue_width_pair": row[
                "lower_predecessor_residue_width_pair"
            ],
            "lower_predecessor_open_slot_count": row[
                "lower_predecessor_open_slot_count"
            ],
            "lower_terminal_four_slot": row["lower_terminal_four_slot"],
        }
        for row in rows
    ]


def summary(rows: list[dict[str, object]]) -> dict[str, object]:
    """Return the directed reentry lift summary."""
    directed_rows = [
        row for row in rows if row["directed_public_reentry2"]
    ]
    target_rows = [
        row for row in directed_rows if row["rres_o4_o4"]
    ]
    falsifier_rows = [
        row for row in target_rows if not row["lower_terminal_four_slot"]
    ]
    next_parity_odd_rows = [
        row for row in target_rows if row["next_parity"] == "odd"
    ]
    next_parity_odd_falsifier_rows = [
        row for row in next_parity_odd_rows if not row["lower_terminal_four_slot"]
    ]
    phase_width_rows = [
        row for row in target_rows if row["phase_width_complement"]
    ]
    phase_width_falsifier_rows = [
        row for row in phase_width_rows if not row["lower_terminal_four_slot"]
    ]
    return {
        "rule_id": RULE_ID,
        "status": "measured_codex_round3_directed_reentry_lift_probe",
        "theorem_status": "hypothesis_not_proved",
        "high_signal_same_phase_row_count": len(rows),
        "directed_public_reentry2_row_count": len(directed_rows),
        "directed_public_reentry2_rres_o4_o4_row_count": len(target_rows),
        "directed_public_reentry2_rres_o4_o4_falsifier_count": len(falsifier_rows),
        "next_parity_odd_target_count": len(next_parity_odd_rows),
        "next_parity_odd_falsifier_count": len(next_parity_odd_falsifier_rows),
        "phase_width_complement_target_count": len(phase_width_rows),
        "phase_width_complement_falsifier_count": len(phase_width_falsifier_rows),
        "phase_width_complement_automatic_on_target": all(
            row["phase_width_complement"] for row in target_rows
        ),
        "smallest_public_added_premise": "next_parity == odd",
        "round3_status": "NEEDS_EXTRA_PREMISE",
        "target_factor_mod180_lane_counts": count_by(
            target_rows,
            "factor_mod180_lane",
        ),
        "target_lower_predecessor_pair_counts": count_by(
            target_rows,
            "lower_predecessor_residue_width_pair",
        ),
        "target_directed_tuple_counts": count_by(target_rows, "directed_tuple"),
        "target_rows": compact_rows(target_rows),
        "falsifier_rows": compact_rows(falsifier_rows),
    }


def main() -> int:
    """Run Round 3 implication probe."""
    rows = annotated_rows()
    target_rows = [
        row
        for row in rows
        if row["directed_public_reentry2"] and row["rres_o4_o4"]
    ]
    falsifier_rows = [
        row for row in target_rows if not row["lower_terminal_four_slot"]
    ]
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    write_jsonl(OUTPUT_DIR / "target_rows.jsonl", target_rows)
    write_jsonl(OUTPUT_DIR / "falsifier_rows.jsonl", falsifier_rows)
    payload = summary(rows)
    write_json(OUTPUT_DIR / "summary.json", payload)
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
