#!/usr/bin/env python3
"""Round 12 next-parity obstruction reducer for lane 163|19."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

from codex_round2_public_trigger_separator import corpus_row_index
from codex_round5_same_phase_boundary_probe import annotated_rows
from first_gap_compatibility_check import write_json, write_jsonl


THIS_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = THIS_DIR / "output" / "codex_round12_next_parity_obstruction"
RULE_ID = "pedk_codex_round12_next_parity_obstruction_v1"
TARGET_LANE = "163|19"
TARGET_TUPLE = ("even", "mid", "o4")
EXPECTED_EXACT_FOLLOWING_TYPE = "o4_d4_a3_d4_even"


def directed_tuple(row: dict[str, object]) -> tuple[str, str, str]:
    """Return the directed public tuple for one annotated row."""
    return (
        str(row["prev_parity"]),
        str(row["containing_position"]),
        str(row["next_open_type"]),
    )


def stage_predicates() -> list[tuple[str, object]]:
    """Return the lane 163|19 next-parity obstruction ladder."""
    return [
        ("public_containing_o6", lambda row: True),
        ("same_phase_lane_163_19", lambda row: row["factor_mod180_lane"] == TARGET_LANE),
        ("rres_o4_o4", lambda row: row["rres_o4_o4"]),
        ("at_winner", lambda row: row["public_gwr_side"] == "at_winner"),
        ("prev_open_offset_4", lambda row: int(row["prev_open_offset"]) == 4),
        ("prev_d_le4", lambda row: int(row["prev_d"]) <= 4),
        ("directed_tuple_even_mid_o4", lambda row: directed_tuple(row) == TARGET_TUPLE),
        ("next_d_le4", lambda row: int(row["next_d"]) <= 4),
        ("next_parity_odd", lambda row: row["next_parity"] == "odd"),
    ]


def cascade_rows() -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    """Return stage counts and the final pre-parity prior-surface rows."""
    current = annotated_rows()
    rows = []
    prior_surface = []
    for stage, predicate in stage_predicates():
        current = [row for row in current if predicate(row)]
        rows.append(
            {
                "rule_id": RULE_ID,
                "stage": stage,
                "row_count": len(current),
                "target_lane_count": sum(
                    1 for row in current if row["factor_mod180_lane"] == TARGET_LANE
                ),
                "top_signature_counts": top_counts_by(current, "signature"),
                "target_lane_signature_counts": count_by(
                    [
                        row
                        for row in current
                        if row["factor_mod180_lane"] == TARGET_LANE
                    ],
                    "signature",
                ),
            }
        )
        if stage == "next_d_le4":
            prior_surface = list(current)
    return rows, prior_surface


def count_by(rows: list[dict[str, object]], field: str) -> dict[str, int]:
    """Return JSON-safe value counts for one field."""
    counts = Counter(str(row[field]) for row in rows)
    return dict(sorted(counts.items()))


def top_counts_by(
    rows: list[dict[str, object]],
    field: str,
    limit: int = 12,
) -> dict[str, int]:
    """Return compact top counts for one field."""
    counts = Counter(str(row[field]) for row in rows)
    return {
        value: count
        for value, count in sorted(
            counts.items(),
            key=lambda item: (-item[1], item[0]),
        )[:limit]
    }


def parity_from_exact_type(exact_type: str) -> str:
    """Return the final parity token from an exact type key."""
    if exact_type.endswith("_even"):
        return "even"
    if exact_type.endswith("_odd"):
        return "odd"
    return "none"


def enriched_for(row: dict[str, object]) -> dict[str, object]:
    """Return the enriched source row for one annotated row."""
    return corpus_row_index()[(str(row["window"]), str(row["case_id"]))]


def micro_state_rows(prior_surface: list[dict[str, object]]) -> list[dict[str, object]]:
    """Return exact following-gap state rows for the prior surface."""
    out = []
    for row in prior_surface:
        enriched = enriched_for(row)
        n_value = int(enriched["N"])
        containing_left = n_value - int(enriched["public_n_offset_from_left"])
        containing_right = n_value + int(enriched["public_n_offset_from_right"])
        following_gap = enriched["public_following_gap"]
        next_winner_offset = int(following_gap["winner_offset"])
        next_winner_value = containing_right + next_winner_offset
        next_exact_type = str(following_gap["exact_type_key"])
        out.append(
            {
                "rule_id": RULE_ID,
                "window": row["window"],
                "case_id": row["case_id"],
                "lane": row["factor_mod180_lane"],
                "signature": row["signature"],
                "public_key": row["public_key"],
                "p_mod180": row["p_mod180"],
                "q_mod180": row["q_mod180"],
                "p_mod36": row["p_mod36"],
                "q_mod36": row["q_mod36"],
                "n_mod180": n_value % 180,
                "public_containing_left_mod180": containing_left % 180,
                "public_containing_right_mod180": containing_right % 180,
                "public_containing_exact_type_key": row["public_containing_exact_type_key"],
                "public_following_exact_type_key": next_exact_type,
                "public_following_gap_width": following_gap["gap_width"],
                "next_open_offset": row["next_open_offset"],
                "next_open_type": row["next_open_type"],
                "next_d": row["next_d"],
                "next_winner_offset": next_winner_offset,
                "next_winner_value_mod2": next_winner_value % 2,
                "next_parity": row["next_parity"],
                "parity_from_exact_type": parity_from_exact_type(next_exact_type),
                "matches_expected_exact_following_type": (
                    next_exact_type == EXPECTED_EXACT_FOLLOWING_TYPE
                ),
            }
        )
    return out


def proof_reduction(prior_surface: list[dict[str, object]]) -> dict[str, object]:
    """Return the exact-state reduction of the next-parity obstruction."""
    states = micro_state_rows(prior_surface)
    exact_type_counts = Counter(str(row["public_following_exact_type_key"]) for row in states)
    return {
        "rule_id": RULE_ID,
        "proof_status": "incomplete",
        "component_law": "next_parity_odd",
        "target_lane": TARGET_LANE,
        "prior_surface": (
            "lane 163|19 + Rres=o4|o4 + at_winner + prev_open_offset=4 + "
            "prev_d<=4 + directed_tuple=even|mid|o4 + next_d<=4"
        ),
        "round11_law": (
            "prior surface -> next_parity=even, so DirectedPublicReentry2OddExit fails"
        ),
        "round12_exact_state_reduction": (
            "prior surface -> public_following_gap.exact_type_key="
            f"{EXPECTED_EXACT_FOLLOWING_TYPE}"
        ),
        "exact_state_implies_next_parity_even": (
            EXPECTED_EXACT_FOLLOWING_TYPE.endswith("_even")
        ),
        "measured_prior_surface_row_count": len(prior_surface),
        "measured_exact_following_type_counts": dict(sorted(exact_type_counts.items())),
        "candidate_exact_state_matches_measured_surface": (
            set(exact_type_counts) == {EXPECTED_EXACT_FOLLOWING_TYPE}
        ),
        "universal_proof_complete": False,
        "next_required_proof_object": (
            "prove that the 163|19 prior surface forces the following-gap "
            f"exact type {EXPECTED_EXACT_FOLLOWING_TYPE}"
        ),
    }


def summary() -> dict[str, object]:
    """Return Round 12 summary."""
    ladder, prior_surface = cascade_rows()
    states = micro_state_rows(prior_surface)
    parity_counts = Counter(str(row["next_parity"]) for row in states)
    exact_type_counts = Counter(str(row["public_following_exact_type_key"]) for row in states)
    odd_exit_count = parity_counts.get("odd", 0)
    return {
        "rule_id": RULE_ID,
        "status": "measured_next_parity_micro_obstruction",
        "component_law": "next_parity_odd",
        "target_lane": TARGET_LANE,
        "theorem_status": "hypothesis_not_proved",
        "prior_surface_row_count": len(prior_surface),
        "prior_surface_next_parity_counts": dict(sorted(parity_counts.items())),
        "odd_exit_counterexample_count": odd_exit_count,
        "micro_exact_following_type_counts": dict(sorted(exact_type_counts.items())),
        "candidate_micro_law": (
            "prior surface -> public_following_gap.exact_type_key="
            f"{EXPECTED_EXACT_FOLLOWING_TYPE}"
        ),
        "candidate_micro_law_matches_measured_surface": (
            set(exact_type_counts) == {EXPECTED_EXACT_FOLLOWING_TYPE}
        ),
        "stage_ladder_final_count": ladder[-1]["row_count"],
        "universal_proof_complete": False,
        "distance_to_final_solution": (
            "first component law is reduced to an exact following-gap state; "
            "the exact-state law remains unproved universally"
        ),
        "next_required_proof_object": (
            "prove the 163|19 exact following-gap state "
            f"{EXPECTED_EXACT_FOLLOWING_TYPE}"
        ),
    }


def main() -> int:
    """Run the Round 12 next-parity obstruction reducer."""
    ladder, prior_surface = cascade_rows()
    states = micro_state_rows(prior_surface)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    write_jsonl(OUTPUT_DIR / "next_parity_stage_ladder.jsonl", ladder)
    write_jsonl(OUTPUT_DIR / "next_parity_micro_state_rows.jsonl", states)
    write_json(OUTPUT_DIR / "proof_reduction.json", proof_reduction(prior_surface))
    payload = summary()
    write_json(OUTPUT_DIR / "summary.json", payload)
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
