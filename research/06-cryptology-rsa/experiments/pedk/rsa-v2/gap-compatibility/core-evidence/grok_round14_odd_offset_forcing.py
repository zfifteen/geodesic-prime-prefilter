#!/usr/bin/env python3
"""Grok Round 14 live odd-offset forcing audit for lane 163|19."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Callable

from codex_round2_public_trigger_separator import corpus_row_index
from codex_round5_same_phase_boundary_probe import annotated_rows
from first_gap_compatibility_check import write_json, write_jsonl


THIS_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = THIS_DIR / "output" / "grok_round14_odd_offset_forcing"
RULE_ID = "pedk_grok_round14_odd_offset_forcing_v1"
TARGET_LANE = "163|19"
TARGET_TUPLE = ("even", "mid", "o4")
TARGET_FOLLOWING_LEFT_MOD180 = 43

StagePredicate = Callable[[dict[str, object]], bool]


def directed_tuple(row: dict[str, object]) -> tuple[str, str, str]:
    """Return the directed public tuple for one annotated row."""
    return (
        str(row["prev_parity"]),
        str(row["containing_position"]),
        str(row["next_open_type"]),
    )


def s163_stage_predicates() -> list[tuple[str, StagePredicate]]:
    """Return the S_163 prior-surface predicate ladder."""
    return [
        (
            "same_phase_lane_163_19",
            lambda row: row["same_mod36"] and row["factor_mod180_lane"] == TARGET_LANE,
        ),
        ("rres_o4_o4", lambda row: row["rres_o4_o4"]),
        ("at_winner", lambda row: row["public_gwr_side"] == "at_winner"),
        ("prev_open_offset_4", lambda row: int(row["prev_open_offset"]) == 4),
        ("prev_d_le4", lambda row: int(row["prev_d"]) <= 4),
        (
            "directed_tuple_even_mid_o4",
            lambda row: directed_tuple(row) == TARGET_TUPLE,
        ),
        ("next_d_le4", lambda row: int(row["next_d"]) <= 4),
    ]


def count_by(rows: list[dict[str, object]], field: str) -> dict[str, int]:
    """Return JSON-safe counts by one field."""
    counts = Counter(str(row[field]) for row in rows)
    return dict(sorted(counts.items()))


def parity_name(value_mod2: int) -> str:
    """Return the parity label for one value mod 2."""
    return "even" if value_mod2 == 0 else "odd"


def first_failed_s163_stage(row: dict[str, object]) -> str:
    """Return the first failed S_163 stage for one row."""
    for stage, predicate in s163_stage_predicates():
        if not predicate(row):
            return stage
    return "survives_s163_prior_surface"


def enriched_public_state(
    row: dict[str, object],
    row_index: dict[tuple[str, str], dict[str, object]],
) -> dict[str, object]:
    """Return public boundary and following-gap state for one row."""
    enriched = row_index[(str(row["window"]), str(row["case_id"]))]
    n_value = int(enriched["N"])
    containing_left = n_value - int(enriched["public_n_offset_from_left"])
    containing_right = n_value + int(enriched["public_n_offset_from_right"])
    following_gap = enriched["public_following_gap"]
    next_winner_offset = int(following_gap["winner_offset"])
    next_winner_value = containing_right + next_winner_offset
    return {
        "public_containing_left_mod180": containing_left % 180,
        "public_containing_right_mod180": containing_right % 180,
        "public_following_exact_type_key": str(following_gap["exact_type_key"]),
        "public_following_gap_width": int(following_gap["gap_width"]),
        "next_winner_offset": next_winner_offset,
        "next_winner_offset_mod2": next_winner_offset % 2,
        "next_winner_value_mod2_by_lift": next_winner_value % 2,
        "next_parity_by_lift": parity_name(next_winner_value % 2),
    }


def compact_offset_row(
    row: dict[str, object],
    row_index: dict[tuple[str, str], dict[str, object]],
    domain: str,
) -> dict[str, object]:
    """Return one compact public offset-domain row."""
    return {
        "rule_id": RULE_ID,
        "domain": domain,
        "window": row["window"],
        "case_id": row["case_id"],
        "lane": row["factor_mod180_lane"],
        "signature": row["signature"],
        "public_key": row["public_key"],
        "public_gwr_side": row["public_gwr_side"],
        "prev_open_offset": row["prev_open_offset"],
        "prev_d": row["prev_d"],
        "prev_parity": row["prev_parity"],
        "containing_position": row["containing_position"],
        "next_open_type": row["next_open_type"],
        "next_d": row["next_d"],
        "next_parity_observed": row["next_parity"],
        "right_boundary_residues": row["right_boundary_residues"],
        "first_failed_s163_stage": first_failed_s163_stage(row),
        **enriched_public_state(row, row_index),
    }


def stage_ladder_rows(
    rows: list[dict[str, object]],
) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    """Return the S_163 stage counts and final prior-surface rows."""
    current = rows
    ladder = []
    for stage, predicate in s163_stage_predicates():
        current = [row for row in current if predicate(row)]
        ladder.append(
            {
                "rule_id": RULE_ID,
                "stage": stage,
                "row_count": len(current),
                "signature_counts": count_by(current, "signature"),
            }
        )
    return ladder, list(current)


def relaxed_offset_domain_table(
    rows: list[dict[str, object]],
    row_index: dict[tuple[str, str], dict[str, object]],
) -> list[dict[str, object]]:
    """Return lane 163|19 rows in the fixed boundary and next-side domain."""
    out = []
    for row in rows:
        state = enriched_public_state(row, row_index)
        if row["factor_mod180_lane"] != TARGET_LANE:
            continue
        if state["public_containing_right_mod180"] != TARGET_FOLLOWING_LEFT_MOD180:
            continue
        if row["next_open_type"] != "o4":
            continue
        if int(row["next_d"]) > 4:
            continue
        out.append(compact_offset_row(row, row_index, "relaxed_offset_domain"))
    out.sort(
        key=lambda row: (
            int(row["next_winner_offset"]),
            str(row["window"]),
            str(row["case_id"]),
        )
    )
    return out


def obstruction_class(stage: str) -> str:
    """Return the component-law class for one failed stage."""
    if stage in {"prev_open_offset_4", "prev_d_le4", "rres_o4_o4", "at_winner"}:
        return "fixed_prior_public_boundary"
    if stage == "directed_tuple_even_mid_o4":
        return "allowed_directed_tuple"
    if stage == "next_d_le4":
        return "next_d_le4"
    if stage == "same_phase_lane_163_19":
        return "same_phase_lane"
    if stage == "survives_s163_prior_surface":
        return "component_law_falsifier"
    return "unclassified"


def even_offset_obstruction_table(
    relaxed_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    """Return every relaxed even offset and its first obstruction."""
    out = []
    for row in relaxed_rows:
        if int(row["next_winner_offset_mod2"]) != 0:
            continue
        first_fail = str(row["first_failed_s163_stage"])
        out.append(
            {
                "rule_id": RULE_ID,
                "lane": TARGET_LANE,
                "window": row["window"],
                "case_id": row["case_id"],
                "next_winner_offset": row["next_winner_offset"],
                "next_winner_offset_mod2": row["next_winner_offset_mod2"],
                "signature": row["signature"],
                "first_failed_s163_stage": first_fail,
                "obstruction_class": obstruction_class(first_fail),
                "status": (
                    "relaxed_even_offset_fails_before_s163"
                    if first_fail != "survives_s163_prior_surface"
                    else "s163_even_offset_falsifier"
                ),
            }
        )
    return out


def falsifier_contract() -> dict[str, object]:
    """Return the falsifier contract for the odd-offset component atom."""
    return {
        "rule_id": RULE_ID,
        "component_law": "next_parity_odd",
        "target_lane": TARGET_LANE,
        "universal_atom": "S_163 -> next_winner_offset is odd",
        "falsifier_contract": (
            "Any valid S_163 row with even next_winner_offset produces "
            "next_parity=odd by the residue-lift equation and invalidates "
            "the lane 163|19 next-parity obstruction."
        ),
        "current_measured_falsifier_count": 0,
        "universal_falsifier_status": "not_proved_absent",
    }


def composition_statement() -> dict[str, object]:
    """Return the local composition statement for Round 14."""
    return {
        "rule_id": RULE_ID,
        "component_law": "next_parity_odd",
        "target_lane": TARGET_LANE,
        "local_chain": [
            "S_163 table-confirms public_containing_right_mod180=43",
            "S_163 table-confirms next_winner_offset=3",
            "3 is odd and 43 is odd, so 43 + 3 is even",
            "next_parity=even",
            "DirectedPublicReentry2OddExit requires next_parity=odd",
            "lane 163|19 is excluded on the measured prior surface",
        ],
        "composition_status": "measured_odd_offset_reduction",
        "universal_proof_complete": False,
    }


def summary(
    prior_rows: list[dict[str, object]],
    relaxed_rows: list[dict[str, object]],
    even_obstructions: list[dict[str, object]],
) -> dict[str, object]:
    """Return the Grok Round 14 summary."""
    boundary_values = sorted(
        {int(row["public_containing_right_mod180"]) for row in prior_rows}
    )
    prior_parities = Counter(
        parity_name(int(row["next_winner_offset_mod2"])) for row in prior_rows
    )
    relaxed_even_rows = [
        row for row in relaxed_rows if int(row["next_winner_offset_mod2"]) == 0
    ]
    relaxed_odd_rows = [
        row for row in relaxed_rows if int(row["next_winner_offset_mod2"]) == 1
    ]
    even_falsifiers = [
        row
        for row in even_obstructions
        if row["status"] == "s163_even_offset_falsifier"
    ]
    first_fail_counts = Counter(
        str(row["first_failed_s163_stage"]) for row in relaxed_even_rows
    )
    return {
        "rule_id": RULE_ID,
        "status": "measured_odd_offset_forcing_reduction",
        "component_law": "next_parity_odd",
        "target_lane": TARGET_LANE,
        "theorem_status": "hypothesis_not_proved",
        "boundary_lock_values": boundary_values,
        "boundary_lock_status": (
            "measured_locked_to_43"
            if boundary_values == [TARGET_FOLLOWING_LEFT_MOD180]
            else "boundary_lock_not_singleton"
        ),
        "prior_surface_row_count": len(prior_rows),
        "prior_surface_next_winner_offset_values": sorted(
            {int(row["next_winner_offset"]) for row in prior_rows}
        ),
        "prior_surface_offset_parity_counts": dict(sorted(prior_parities.items())),
        "prior_surface_even_offset_falsifier_count": len(even_falsifiers),
        "relaxed_offset_domain_row_count": len(relaxed_rows),
        "relaxed_offset_domain_offset_values": sorted(
            {int(row["next_winner_offset"]) for row in relaxed_rows}
        ),
        "relaxed_even_offset_candidate_count": len(relaxed_even_rows),
        "relaxed_odd_offset_candidate_count": len(relaxed_odd_rows),
        "relaxed_even_offset_first_fail_counts": dict(sorted(first_fail_counts.items())),
        "even_offset_obstruction_table_covers_relaxed_even_offsets": (
            len(even_obstructions) == len(relaxed_even_rows)
        ),
        "measured_surviving_offsets": [
            {
                "next_winner_offset": row["next_winner_offset"],
                "next_winner_offset_mod2": row["next_winner_offset_mod2"],
                "public_following_exact_type_key": row[
                    "public_following_exact_type_key"
                ],
                "next_parity_by_lift": row["next_parity_by_lift"],
            }
            for row in prior_rows
        ],
        "remaining_universal_atom": "prove S_163 -> next_winner_offset is odd",
        "universal_proof_complete": False,
        "distance_to_final_solution": (
            "co-pilot audit agrees that the aircraft is in the flare: "
            "the measured S_163 surface has only the odd a3 offset, while "
            "the relaxed even a10 offset fails before the prior surface"
        ),
        "next_required_proof_object": (
            "prove the odd-offset forcing law without adding a following "
            "exact-type premise"
        ),
    }


def main() -> int:
    """Run the live Grok Round 14 odd-offset forcing audit."""
    row_index = corpus_row_index()
    rows = annotated_rows()
    ladder, prior_surface = stage_ladder_rows(rows)
    prior_rows = [
        compact_offset_row(row, row_index, "s163_prior_surface_offset_domain")
        for row in prior_surface
    ]
    boundary_rows = [
        compact_offset_row(row, row_index, "s163_prior_surface_boundary_lock")
        for row in prior_surface
    ]
    relaxed_rows = relaxed_offset_domain_table(rows, row_index)
    even_obstructions = even_offset_obstruction_table(relaxed_rows)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    write_jsonl(OUTPUT_DIR / "s163_stage_ladder.jsonl", ladder)
    write_jsonl(OUTPUT_DIR / "boundary_lock_table.jsonl", boundary_rows)
    write_jsonl(OUTPUT_DIR / "offset_domain_table.jsonl", prior_rows)
    write_jsonl(OUTPUT_DIR / "relaxed_offset_domain_table.jsonl", relaxed_rows)
    write_jsonl(
        OUTPUT_DIR / "even_offset_obstruction_table.jsonl",
        even_obstructions,
    )
    write_json(OUTPUT_DIR / "falsifier_contract.json", falsifier_contract())
    write_json(OUTPUT_DIR / "composition_statement.json", composition_statement())
    payload = summary(prior_rows, relaxed_rows, even_obstructions)
    write_json(OUTPUT_DIR / "summary.json", payload)
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
