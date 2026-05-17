#!/usr/bin/env python3
"""Round 5 test of whether odd-exit public reentry derives same mod-36 phase."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

from codex_round1_high_signal_probe import (
    PHASE_WIDTH_COMPLEMENT_PAIRS,
    TARGET_CONTAINING_TYPE,
    corpus_dirs,
    interior_open_slot_count,
    open_offset,
    public_key,
    right_open_label,
)
from codex_round2_public_trigger_separator import comparison_fields
from first_gap_compatibility_check import write_json, write_jsonl
from slot_factor_public_quotient_test import read_jsonl


THIS_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = THIS_DIR / "output" / "codex_round5_same_phase_boundary_probe"
RULE_ID = "pedk_codex_round5_same_phase_boundary_probe_v1"
DIRECTED_REENTRY_TUPLES = {
    ("even", "mid", "o4"),
    ("odd", "early", "o6"),
}


def reduced_row(row: dict[str, object], window: str) -> dict[str, object] | None:
    """Return one public-containing row without filtering by factor phase."""
    if str(row["public_containing_exact_type_key"]) != TARGET_CONTAINING_TYPE:
        return None

    p = int(row["p"])
    q = int(row["q"])
    n_value = int(row["N"])
    public_left_endpoint = n_value - int(row["public_n_offset_from_left"])
    public_previous_width = int(row["public_previous_gap"]["gap_width"])
    public_previous_left_endpoint = public_left_endpoint - public_previous_width
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
        "public_previous_gap_width": public_previous_width,
        "public_previous_gap_width_mod30": public_previous_width % 30,
        "public_previous_left_mod30": public_previous_left_endpoint % 30,
        "p_mod30": p % 30,
        "q_mod30": q % 30,
        "p_mod36": p % 36,
        "q_mod36": q % 36,
        "same_mod36": p % 36 == q % 36,
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
    }


def directed_public_reentry2_odd_exit(fields: dict[str, object]) -> bool:
    """Return the Round 4 odd-exit directed public reentry predicate."""
    return (
        fields["containing_exact_type"] == TARGET_CONTAINING_TYPE
        and fields["prev_open_offset"] == 4
        and int(fields["prev_d"]) <= 4
        and int(fields["next_d"]) <= 4
        and fields["next_parity"] == "odd"
        and fields["public_gwr_side"] == "at_winner"
        and (
            fields["prev_parity"],
            fields["containing_position"],
            fields["next_open_type"],
        )
        in DIRECTED_REENTRY_TUPLES
    )


def annotated_rows() -> list[dict[str, object]]:
    """Return public-containing rows with directed reentry fields."""
    out = []
    for directory in corpus_dirs():
        window = directory.name.removeprefix("enriched_multiplication_map_corpus_")
        for enriched_row in read_jsonl(directory / "enriched_rows.jsonl"):
            base_row = reduced_row(enriched_row, window)
            if base_row is None:
                continue
            fields = comparison_fields(base_row, enriched_row)
            signature = (
                f"{fields['prev_parity']}|{fields['containing_position']}|"
                f"{fields['next_open_type']}|{fields['next_parity']}"
            )
            out.append(
                {
                    **base_row,
                    **fields,
                    "signature": signature,
                    "directed_public_reentry2_odd_exit": (
                        directed_public_reentry2_odd_exit(fields)
                    ),
                }
            )
    out.sort(key=lambda row: (str(row["window"]), str(row["case_id"])))
    return out


def count_by(rows: list[dict[str, object]], key: str) -> dict[str, int]:
    """Return JSON-safe counts by one field."""
    counts = Counter(str(row[key]) for row in rows)
    return {value: counts[value] for value in sorted(counts)}


def compact_rows(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    """Return compact rows for target inspection."""
    return [
        {
            "rule_id": RULE_ID,
            "window": row["window"],
            "case_id": row["case_id"],
            "public_key": row["public_key"],
            "signature": row["signature"],
            "same_mod36": row["same_mod36"],
            "p_mod36": row["p_mod36"],
            "q_mod36": row["q_mod36"],
            "factor_mod180_lane": row["factor_mod180_lane"],
            "right_boundary_residues": row["right_boundary_residues"],
            "phase_width_pair": row["phase_width_pair"],
            "phase_width_complement": row["phase_width_complement"],
            "lower_predecessor_residue_width_pair": row[
                "lower_predecessor_residue_width_pair"
            ],
            "lower_predecessor_open_slot_count": row[
                "lower_predecessor_open_slot_count"
            ],
            "lower_terminal_closure": row["lower_terminal_closure"],
            "lower_terminal_four_slot": row["lower_terminal_four_slot"],
        }
        for row in rows
    ]


def target_rows(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    """Return OddExitDirectedPublicReentry plus Rres=o4|o4 target rows."""
    return [
        row
        for row in rows
        if row["directed_public_reentry2_odd_exit"] and row["rres_o4_o4"]
    ]


def summary(rows: list[dict[str, object]]) -> dict[str, object]:
    """Return Round 5 same-phase boundary summary."""
    targets = target_rows(rows)
    same_phase_targets = [row for row in targets if row["same_mod36"]]
    non_same_phase_targets = [row for row in targets if not row["same_mod36"]]
    same_phase_lift_falsifiers = [
        row for row in same_phase_targets if not row["lower_terminal_four_slot"]
    ]
    non_same_phase_lift_falsifiers = [
        row for row in non_same_phase_targets if not row["lower_terminal_four_slot"]
    ]
    return {
        "rule_id": RULE_ID,
        "status": "measured_codex_round5_same_phase_boundary_probe",
        "theorem_status": "hypothesis_not_proved",
        "public_containing_surface_row_count": len(rows),
        "odd_exit_rres_o4_o4_row_count": len(targets),
        "odd_exit_rres_o4_o4_same_mod36_count": len(same_phase_targets),
        "odd_exit_rres_o4_o4_non_same_mod36_count": len(non_same_phase_targets),
        "same_phase_derived_on_measured_surface": not non_same_phase_targets,
        "same_phase_target_lift_falsifier_count": len(same_phase_lift_falsifiers),
        "non_same_phase_target_lift_falsifier_count": len(
            non_same_phase_lift_falsifiers,
        ),
        "phase_width_complement_automatic_on_same_phase_target": all(
            row["phase_width_complement"] for row in same_phase_targets
        ),
        "phase_width_complement_automatic_on_full_target": all(
            row["phase_width_complement"] for row in targets
        ),
        "target_signature_counts": count_by(targets, "signature"),
        "non_same_phase_signature_counts": count_by(
            non_same_phase_targets,
            "signature",
        ),
        "target_factor_mod180_lane_counts": count_by(
            targets,
            "factor_mod180_lane",
        ),
        "non_same_phase_factor_mod180_lane_counts": count_by(
            non_same_phase_targets,
            "factor_mod180_lane",
        ),
        "non_same_phase_target_rows": compact_rows(non_same_phase_targets),
    }


def main() -> int:
    """Run the full-surface same-phase boundary probe."""
    rows = annotated_rows()
    targets = target_rows(rows)
    same_phase_targets = [row for row in targets if row["same_mod36"]]
    non_same_phase_targets = [row for row in targets if not row["same_mod36"]]

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    write_jsonl(OUTPUT_DIR / "target_rows.jsonl", compact_rows(targets))
    write_jsonl(
        OUTPUT_DIR / "same_phase_target_rows.jsonl",
        compact_rows(same_phase_targets),
    )
    write_jsonl(
        OUTPUT_DIR / "non_same_phase_target_rows.jsonl",
        compact_rows(non_same_phase_targets),
    )
    payload = summary(rows)
    write_json(OUTPUT_DIR / "summary.json", payload)
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
