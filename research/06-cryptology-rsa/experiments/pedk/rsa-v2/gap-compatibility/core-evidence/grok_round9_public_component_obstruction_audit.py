#!/usr/bin/env python3
"""Grok Round 9 component audit for the public signature phase obstruction."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Callable

from codex_round5_same_phase_boundary_probe import annotated_rows
from codex_round6_sync_chain_table import theoretical_same_phase_lanes
from first_gap_compatibility_check import write_json, write_jsonl


THIS_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = THIS_DIR / "output" / "grok_round9_public_component_obstruction_audit"
RULE_ID = "pedk_grok_round9_public_component_obstruction_audit_v1"
DIRECTED_TUPLES = {
    ("even", "mid", "o4"),
    ("odd", "early", "o6"),
}


StagePredicate = Callable[[dict[str, object]], bool]


def directed_tuple(row: dict[str, object]) -> tuple[str, str, str]:
    """Return the three-symbol directed tuple."""
    return (
        str(row["prev_parity"]),
        str(row["containing_position"]),
        str(row["next_open_type"]),
    )


def pipeline(lane: str) -> list[tuple[str, StagePredicate]]:
    """Return the ordered public-predicate cascade for one lane."""
    return [
        (
            "same_phase_lane",
            lambda row: row["same_mod36"] and row["factor_mod180_lane"] == lane,
        ),
        ("rres_o4_o4", lambda row: row["rres_o4_o4"]),
        ("at_winner", lambda row: row["public_gwr_side"] == "at_winner"),
        ("prev_open_offset_4", lambda row: int(row["prev_open_offset"]) == 4),
        ("prev_d_le4", lambda row: int(row["prev_d"]) <= 4),
        (
            "directed_tuple",
            lambda row: directed_tuple(row) in DIRECTED_TUPLES,
        ),
        ("next_d_le4", lambda row: int(row["next_d"]) <= 4),
        ("next_parity_odd", lambda row: row["next_parity"] == "odd"),
    ]


def compact_row(row: dict[str, object], lane: str, stage: str) -> dict[str, object]:
    """Return component-audit fields for one row."""
    return {
        "rule_id": RULE_ID,
        "lane": lane,
        "stage": stage,
        "window": row["window"],
        "case_id": row["case_id"],
        "public_key": row["public_key"],
        "signature": row["signature"],
        "factor_mod180_lane": row["factor_mod180_lane"],
        "p_mod36": row["p_mod36"],
        "q_mod36": row["q_mod36"],
        "prev_open_offset": row["prev_open_offset"],
        "prev_d": row["prev_d"],
        "prev_parity": row["prev_parity"],
        "containing_position": row["containing_position"],
        "next_open_type": row["next_open_type"],
        "next_d": row["next_d"],
        "next_parity": row["next_parity"],
        "public_gwr_side": row["public_gwr_side"],
        "phase_width_pair": row["phase_width_pair"],
        "lower_predecessor_residue_width_pair": row[
            "lower_predecessor_residue_width_pair"
        ],
        "lower_terminal_four_slot": row["lower_terminal_four_slot"],
    }


def cascade_for_lane(
    rows: list[dict[str, object]],
    lane: str,
) -> tuple[dict[str, object], list[dict[str, object]], list[dict[str, object]]]:
    """Return cascade row, near misses, and final survivors for one lane."""
    current = rows
    stage_counts: dict[str, int] = {}
    last_nonzero_stage = ""
    last_nonzero_rows: list[dict[str, object]] = []
    first_zero_stage = ""

    for stage, predicate in pipeline(lane):
        current = [row for row in current if predicate(row)]
        stage_counts[stage] = len(current)
        if current:
            last_nonzero_stage = stage
            last_nonzero_rows = list(current)
        elif not first_zero_stage:
            first_zero_stage = stage

    final_survives = bool(current)
    near_misses = []
    if not final_survives and last_nonzero_stage:
        near_misses = [
            compact_row(row, lane, last_nonzero_stage)
            for row in last_nonzero_rows
        ]
    final_rows = [
        compact_row(row, lane, "next_parity_odd")
        for row in current
    ]
    return (
        {
            "rule_id": RULE_ID,
            "lane": lane,
            "stage_counts": stage_counts,
            "first_zero_stage": first_zero_stage,
            "last_nonzero_stage": last_nonzero_stage,
            "final_survives": final_survives,
            "final_survivor_count": len(current),
        },
        near_misses,
        final_rows,
    )


def lane_component_cascade() -> tuple[
    list[dict[str, object]],
    list[dict[str, object]],
    list[dict[str, object]],
]:
    """Return cascades, near misses, and final survivors for all 12 lanes."""
    rows = annotated_rows()
    cascades = []
    near_misses = []
    final_rows = []
    for lane in theoretical_same_phase_lanes():
        lane_value = str(lane["lane"])
        cascade, lane_near_misses, lane_final_rows = cascade_for_lane(rows, lane_value)
        cascades.append({**lane, **cascade})
        near_misses.extend(lane_near_misses)
        final_rows.extend(lane_final_rows)
    return cascades, near_misses, final_rows


def proof_pressure(cascades: list[dict[str, object]]) -> dict[str, object]:
    """Return proof-pressure notes derived from the component cascade."""
    excluded = [row for row in cascades if not row["final_survives"]]
    return {
        "rule_id": RULE_ID,
        "proof_status": "incomplete",
        "main_obligation": (
            "prove that the ordered public predicate cascade excludes every "
            "same-phase lane except 43|79 and 49|13"
        ),
        "component_obligations": [
            {
                "stage": stage,
                "excluded_lane_count": sum(
                    1 for row in excluded if row["first_zero_stage"] == stage
                ),
            }
            for stage in (
                "prev_open_offset_4",
                "prev_d_le4",
                "directed_tuple",
                "next_parity_odd",
            )
        ],
        "near_miss_warning": (
            "The public signature phase equation is not proved by the "
            "four-symbol signature alone; bounded entry and odd exit are part "
            "of the measured obstruction."
        ),
    }


def summary(cascades: list[dict[str, object]]) -> dict[str, object]:
    """Return Round 9 summary."""
    final = [row for row in cascades if row["final_survives"]]
    excluded = [row for row in cascades if not row["final_survives"]]
    first_zero_counts = Counter(str(row["first_zero_stage"]) for row in excluded)
    by_lane = {str(row["lane"]): row for row in cascades}
    return {
        "rule_id": RULE_ID,
        "status": "measured_grok_public_component_obstruction_audit",
        "theorem_status": "hypothesis_not_proved",
        "theoretical_same_phase_lane_count": len(cascades),
        "final_survivor_count": len(final),
        "final_surviving_lanes": sorted(str(row["lane"]) for row in final),
        "excluded_lane_count": len(excluded),
        "first_zero_stage_counts": dict(sorted(first_zero_counts.items())),
        "lane_163_19_block_stage": by_lane["163|19"]["first_zero_stage"],
        "lane_19_163_block_stage": by_lane["19|163"]["first_zero_stage"],
        "all_excluded_lanes_have_component_obstruction": all(
            bool(row["first_zero_stage"]) for row in excluded
        ),
        "universal_proof_complete": False,
        "next_required_proof_object": (
            "prove the public predicate component exclusions over the finite "
            "same-phase lane table, with bounded entry and odd exit included"
        ),
    }


def main() -> int:
    """Run the public component obstruction audit."""
    cascades, near_misses, final_rows = lane_component_cascade()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    write_jsonl(OUTPUT_DIR / "lane_component_cascade.jsonl", cascades)
    write_jsonl(OUTPUT_DIR / "near_miss_rows.jsonl", near_misses)
    write_jsonl(OUTPUT_DIR / "final_survivor_rows.jsonl", final_rows)
    write_json(OUTPUT_DIR / "proof_pressure.json", proof_pressure(cascades))
    payload = summary(cascades)
    write_json(OUTPUT_DIR / "summary.json", payload)
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
