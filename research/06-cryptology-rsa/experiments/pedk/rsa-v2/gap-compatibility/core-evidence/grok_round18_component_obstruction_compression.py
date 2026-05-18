#!/usr/bin/env python3
"""Grok co-pilot mirror for Round 18: 12-lane mechanism compression matrix.

This is the independent Grok implementation of the mechanically auditable
12-lane public obstruction compression matrix per the closed Round 00-03
meeting contract.

Contract (verbatim from meeting):
- Build one row per theoretical same-phase lane.
- Compute mechanism_features from public gap/residue/offset/parity/terminal data.
- Derive mechanism_class strictly from those features via an explicit deterministic rule.
- Retain prior_component_law_label (first_zero_stage) only for comparison.
- Report whether the 4 historical component laws compress into fewer derived mechanisms.
- Status discipline: measured matrix on current corpus; theorem_status remains
  hypothesis_not_proved; no factor_found claim.

Grok verification role:
- Independent execution of the identical derivation rule.
- Same output shape and artifacts under output/grok_round18_.../
- Confirmation or objection against Codex's codex_round18 run.

PGS-native frame (per AGENTS.md):
  Lane objects (12 same-phase mod-180 candidates)
  -> Public invariants (rres_o4_o4, at_winner, prev_open_offset_4, prev_d_le4,
     directed_tuple in {even|mid|o4, odd|early|o6}, next_d_le4, next_parity_odd,
     lower-terminal four-slot lift)
  -> Derived mechanism class (computed width/residue/open-offset/parity rule)
  -> Resolved exclusion state or survivor alignment on current evidence surface.

No web search, no Agent Bus, no edits outside this single allowed file.
"""

from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path

from codex_round2_public_trigger_separator import corpus_row_index
from codex_round5_same_phase_boundary_probe import annotated_rows
from codex_round6_sync_chain_table import theoretical_same_phase_lanes
from codex_round9_public_component_obstruction_audit import (
    DIRECTED_TUPLES,
    directed_tuple,
    pipeline,
)
from first_gap_compatibility_check import write_json, write_jsonl
from modulus_gap_grammar_probe import first_open_offset


THIS_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = THIS_DIR / "output" / "grok_round18_component_obstruction_compression"
RULE_ID = "pedk_grok_round18_component_obstruction_compression_v1"
SURVIVOR_LANES = {"43|79", "49|13"}


def parity_name(value_mod2: int) -> str:
    """Return parity label for a mod-2 value."""
    return "even" if value_mod2 == 0 else "odd"


def enriched_state(
    row: dict[str, object],
    row_index: dict[tuple[str, str], dict[str, object]],
) -> dict[str, object]:
    """Compute public width, residue, first-open offset, and next-parity features.

    This is the definition-level extraction used for mechanism_features.
    All values are derived from N, public_n_offset_from_left/right,
    public_previous_gap, public_following_gap, and the first_open_offset table.
    """
    enriched = row_index[(str(row["window"]), str(row["case_id"]))]
    n_value = int(enriched["N"])
    containing_left = n_value - int(enriched["public_n_offset_from_left"])
    containing_right = n_value + int(enriched["public_n_offset_from_right"])
    previous_gap = enriched["public_previous_gap"]
    following_gap = enriched["public_following_gap"]
    previous_gap_width = int(previous_gap["gap_width"])
    previous_left_mod30 = (containing_left % 30 - previous_gap_width) % 30
    computed_prev_open_offset = first_open_offset(previous_left_mod30)
    next_winner_offset = int(following_gap["winner_offset"])
    computed_next_parity = parity_name((containing_right + next_winner_offset) % 2)
    return {
        "public_containing_left_mod30": containing_left % 30,
        "public_containing_right_mod180": containing_right % 180,
        "public_previous_gap_width": previous_gap_width,
        "public_following_gap_width": int(following_gap["gap_width"]),
        "public_previous_winner_offset": int(previous_gap["winner_offset"]),
        "public_following_winner_offset": next_winner_offset,
        "previous_left_mod30_by_width": previous_left_mod30,
        "computed_prev_open_offset": computed_prev_open_offset,
        "computed_next_parity": computed_next_parity,
        "parity_source": (
            "next_parity = parity(public_containing_right_mod180 + "
            "public_following_winner_offset)"
        ),
        "prev_open_source": (
            "computed_prev_open_offset = first_open_offset("
            "public_containing_left_mod30 - public_previous_gap_width mod 30)"
        ),
    }


def rows_for_lane_at_stage(
    rows: list[dict[str, object]],
    lane: str,
) -> tuple[dict[str, object], list[dict[str, object]]]:
    """Walk the Round 9 public predicate pipeline for one lane.

    Returns the cascade summary and the last_nonzero_rows (the representative
    prior surface for feature extraction).
    """
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
    cascade = {
        "stage_counts": stage_counts,
        "first_zero_stage": first_zero_stage,
        "last_nonzero_stage": last_nonzero_stage,
        "final_survives": bool(current),
        "final_survivor_count": len(current),
    }
    return cascade, last_nonzero_rows


def unique_sorted(values: list[object]) -> list[object]:
    """Deterministic unique sort."""
    return sorted({value for value in values}, key=lambda item: str(item))


def summarize_rows(
    rows: list[dict[str, object]],
    row_index: dict[tuple[str, str], dict[str, object]],
) -> dict[str, object]:
    """Aggregate mechanism-relevant features from the representative rows."""
    enriched_rows = [{**row, **enriched_state(row, row_index)} for row in rows]
    if not enriched_rows:
        return {
            "representative_row_status": "representative_prior_surface_empty",
            "representative_row_count": 0,
            "case_ids": [],
            "signatures": [],
            "prev_open_offset_values": [],
            "computed_prev_open_offset_values": [],
            "prev_d_values": [],
            "directed_tuple_values": [],
            "allowed_directed_tuple_values": [],
            "next_d_values": [],
            "next_parity_values": [],
            "computed_next_parity_values": [],
            "public_previous_gap_width_values": [],
            "public_following_gap_width_values": [],
            "public_containing_left_mod30_values": [],
            "public_containing_right_mod180_values": [],
            "previous_left_mod30_by_width_values": [],
            "next_winner_offset_values": [],
            "previous_winner_offset_values": [],
            "phase_width_pair_values": [],
            "lower_predecessor_pair_values": [],
            "lower_predecessor_open_slot_count_values": [],
            "lower_terminal_four_slot_values": [],
            "terminal_image_status": "no_representative_rows",
        }
    tuple_values = ["|".join(directed_tuple(row)) for row in enriched_rows]
    allowed_tuple_values = [
        value
        for value in tuple_values
        if tuple(value.split("|")) in DIRECTED_TUPLES
    ]
    lower_terminal_values = unique_sorted(
        [bool(row["lower_terminal_four_slot"]) for row in enriched_rows]
    )
    if lower_terminal_values == [True]:
        terminal_status = "all_representatives_have_lower_terminal_four_slot"
    elif True in lower_terminal_values:
        terminal_status = "mixed_terminal_image"
    else:
        terminal_status = "no_lower_terminal_four_slot_on_representatives"
    return {
        "representative_row_status": "representative_row_found",
        "representative_row_count": len(enriched_rows),
        "case_ids": unique_sorted([row["case_id"] for row in enriched_rows]),
        "signatures": unique_sorted([row["signature"] for row in enriched_rows]),
        "prev_open_offset_values": unique_sorted(
            [int(row["prev_open_offset"]) for row in enriched_rows]
        ),
        "computed_prev_open_offset_values": unique_sorted(
            [int(row["computed_prev_open_offset"]) for row in enriched_rows]
        ),
        "prev_d_values": unique_sorted([int(row["prev_d"]) for row in enriched_rows]),
        "directed_tuple_values": unique_sorted(tuple_values),
        "allowed_directed_tuple_values": unique_sorted(allowed_tuple_values),
        "next_d_values": unique_sorted([int(row["next_d"]) for row in enriched_rows]),
        "next_parity_values": unique_sorted(
            [str(row["next_parity"]) for row in enriched_rows]
        ),
        "computed_next_parity_values": unique_sorted(
            [str(row["computed_next_parity"]) for row in enriched_rows]
        ),
        "public_previous_gap_width_values": unique_sorted(
            [int(row["public_previous_gap_width"]) for row in enriched_rows]
        ),
        "public_following_gap_width_values": unique_sorted(
            [int(row["public_following_gap_width"]) for row in enriched_rows]
        ),
        "public_containing_left_mod30_values": unique_sorted(
            [int(row["public_containing_left_mod30"]) for row in enriched_rows]
        ),
        "public_containing_right_mod180_values": unique_sorted(
            [int(row["public_containing_right_mod180"]) for row in enriched_rows]
        ),
        "previous_left_mod30_by_width_values": unique_sorted(
            [int(row["previous_left_mod30_by_width"]) for row in enriched_rows]
        ),
        "next_winner_offset_values": unique_sorted(
            [int(row["public_following_winner_offset"]) for row in enriched_rows]
        ),
        "previous_winner_offset_values": unique_sorted(
            [int(row["public_previous_winner_offset"]) for row in enriched_rows]
        ),
        "phase_width_pair_values": unique_sorted(
            [row["phase_width_pair"] for row in enriched_rows]
        ),
        "lower_predecessor_pair_values": unique_sorted(
            [row["lower_predecessor_residue_width_pair"] for row in enriched_rows]
        ),
        "lower_predecessor_open_slot_count_values": unique_sorted(
            [int(row["lower_predecessor_open_slot_count"]) for row in enriched_rows]
        ),
        "lower_terminal_four_slot_values": lower_terminal_values,
        "terminal_image_status": terminal_status,
    }


def a_b_mod6(lane: dict[str, object]) -> dict[str, int]:
    """Phase coordinates a,b in p = p_mod30 + 30a, q = q_mod30 + 30b."""
    return {
        "a_mod6": (int(lane["p_mod180"]) - int(lane["p_mod30"])) // 30,
        "b_mod6": (int(lane["q_mod180"]) - int(lane["q_mod30"])) // 30,
    }


def mechanism_features(
    cascade: dict[str, object],
    summary: dict[str, object],
) -> dict[str, object]:
    """The exact feature vector used for mechanical classification.

    All fields are computed from the enriched public gap data of the
    last_nonzero_rows. No prior Round 10/11 labels are used here.
    """
    prev_open_values = summary["computed_prev_open_offset_values"]
    prev_d_values = summary["prev_d_values"]
    next_d_values = summary["next_d_values"]
    return {
        "final_survives": bool(cascade["final_survives"]),
        "has_prev_open_offset_4": 4 in prev_open_values,
        "has_prev_d_le4": any(int(value) <= 4 for value in prev_d_values),
        "has_allowed_directed_tuple": bool(summary["allowed_directed_tuple_values"]),
        "has_next_d_le4": any(int(value) <= 4 for value in next_d_values),
        "has_next_parity_odd": "odd" in summary["computed_next_parity_values"],
        "has_lower_terminal_four_slot": True in summary["lower_terminal_four_slot_values"],
        "first_zero_stage": cascade["first_zero_stage"],
        "last_nonzero_stage": cascade["last_nonzero_stage"],
    }


def derive_mechanism_class(features: dict[str, object]) -> tuple[str, str]:
    """Explicit, deterministic, auditable classification rule.

    This is the single source of truth for derived_mechanism_class.
    Order and conditions are part of the Round 18 contract.
    """
    if features["final_survives"] and features["has_lower_terminal_four_slot"]:
        return (
            "survivor_terminal_lift_aligned",
            "final_survives and has_lower_terminal_four_slot",
        )
    if not features["has_prev_open_offset_4"]:
        return (
            "entry_width_residue_open_offset_mismatch",
            "computed previous first-open offsets do not include o4",
        )
    if not features["has_prev_d_le4"]:
        return (
            "entry_d_bound_failure",
            "entry reaches o4 but no representative previous d-load is <= 4",
        )
    if not features["has_allowed_directed_tuple"]:
        return (
            "directed_tuple_mismatch",
            "bounded entry exists but no representative tuple is even|mid|o4 or odd|early|o6",
        )
    if features["has_next_d_le4"] and not features["has_next_parity_odd"]:
        return (
            "exit_offset_parity_mismatch",
            "allowed tuple reaches next_d<=4 but computed next parity is never odd",
        )
    return (
        "unclassified_or_requires_separate_component_law",
        "feature vector does not match a compressed rule",
    )


def factor_relevance(payload: dict[str, object]) -> str:
    """Operational factor-relevance (structural alignment only)."""
    if (
        payload["survivor_status"] == "survivor"
        and payload["terminal_image_status"]
        == "all_representatives_have_lower_terminal_four_slot"
    ):
        return (
            "public selector survivor -> terminal image -> lower-terminal "
            "four-slot lift -> candidate factor-side endpoint class"
        )
    return "excluded public selector lane; no factor_found claim"


def falsifier_contract(mechanism_class: str, lane: str) -> str:
    """Per-class falsifier contract (mechanical, not narrative)."""
    if mechanism_class == "entry_width_residue_open_offset_mismatch":
        return (
            f"A valid lane {lane} representative state whose computed previous "
            "first-open offset includes 4 invalidates this mechanism class."
        )
    if mechanism_class == "entry_d_bound_failure":
        return (
            f"A valid lane {lane} representative state with prev_open_offset=4 "
            "and prev_d<=4 invalidates this mechanism class."
        )
    if mechanism_class == "directed_tuple_mismatch":
        return (
            f"A valid lane {lane} representative state with bounded entry and "
            "directed tuple even|mid|o4 or odd|early|o6 invalidates this class."
        )
    if mechanism_class == "exit_offset_parity_mismatch":
        return (
            f"A valid lane {lane} representative state with allowed tuple, "
            "next_d<=4, and computed next_parity=odd invalidates this class."
        )
    if mechanism_class == "survivor_terminal_lift_aligned":
        return (
            f"A valid lane {lane} final survivor without lower-terminal "
            "four-slot lift invalidates this survivor alignment class."
        )
    return f"A valid lane {lane} row requiring no listed mechanism falsifies compression."


def matrix_rows() -> list[dict[str, object]]:
    """Build the 12-lane matrix with mechanically derived classes."""
    rows = annotated_rows()
    row_index = corpus_row_index()
    out = []
    for lane in theoretical_same_phase_lanes():
        lane_value = str(lane["lane"])
        cascade, representative_rows = rows_for_lane_at_stage(rows, lane_value)
        row_summary = summarize_rows(representative_rows, row_index)
        features = mechanism_features(cascade, row_summary)
        mechanism_class, class_rule = derive_mechanism_class(features)
        coords = a_b_mod6(lane)
        payload = {
            "rule_id": RULE_ID,
            "lane": lane_value,
            "orientation": lane["orientation"],
            "phase_mod36": lane["phase_mod36"],
            **coords,
            "survivor_status": (
                "survivor" if cascade["final_survives"] else "excluded"
            ),
            "first_failing_public_predicate": (
                cascade["first_zero_stage"] or "survives"
            ),
            "stage_counts": cascade["stage_counts"],
            **row_summary,
            "mechanism_features": features,
            "derived_mechanism_class": mechanism_class,
            "prior_component_law_label": (
                cascade["first_zero_stage"] or "survivor"
            ),
            "mechanism_class_rule": class_rule,
            "falsifier_contract": falsifier_contract(mechanism_class, lane_value),
            "theorem_status": "hypothesis_not_proved",
            "universal_proof_complete": False,
            "factor_found": False,
        }
        payload["factor_relevance_under_current_operational_definition"] = (
            factor_relevance(payload)
        )
        out.append(payload)
    return out


def mechanism_groups(rows: list[dict[str, object]]) -> dict[str, object]:
    """Groups by the *derived* (not prior) mechanism class."""
    groups: dict[str, list[str]] = defaultdict(list)
    for row in rows:
        groups[str(row["derived_mechanism_class"])].append(str(row["lane"]))
    return {
        "rule_id": RULE_ID,
        "grouping_basis": "derived_mechanism_class computed from mechanism_features",
        "groups": {
            key: sorted(value) for key, value in sorted(groups.items())
        },
        "excluded_groups": {
            key: sorted(
                row["lane"]
                for row in rows
                if row["survivor_status"] == "excluded"
                and row["derived_mechanism_class"] == key
            )
            for key in sorted(groups)
        },
    }


def compression_summary(rows: list[dict[str, object]]) -> dict[str, object]:
    """The Round 18 compression decision surface."""
    excluded = [row for row in rows if row["survivor_status"] == "excluded"]
    survivors = [row for row in rows if row["survivor_status"] == "survivor"]
    first_failure_counts = Counter(
        str(row["first_failing_public_predicate"]) for row in excluded
    )
    mechanism_counts = Counter(
        str(row["derived_mechanism_class"]) for row in excluded
    )
    component_law_count_before = len(first_failure_counts)
    mechanism_law_count_after = len(mechanism_counts)
    compression_success = mechanism_law_count_after < component_law_count_before
    return {
        "rule_id": RULE_ID,
        "status": "measured_component_obstruction_compression_matrix",
        "total_lanes": len(rows),
        "survivor_lanes": sorted(row["lane"] for row in survivors),
        "excluded_lanes": sorted(row["lane"] for row in excluded),
        "first_failure_stage_counts": dict(sorted(first_failure_counts.items())),
        "mechanism_group_counts": dict(sorted(mechanism_counts.items())),
        "component_law_count_before_compression": component_law_count_before,
        "mechanism_law_count_after_compression": mechanism_law_count_after,
        "compression_success": compression_success,
        "candidate_common_invariant": (
            "no smaller shared invariant found in this finite matrix"
            if not compression_success
            else "derived mechanism classes compress prior component labels"
        ),
        "classification_inputs": [
            "computed_prev_open_offset_values",
            "prev_d_values",
            "allowed_directed_tuple_values",
            "next_d_values",
            "computed_next_parity_values",
            "lower_terminal_four_slot_values",
        ],
        "classification_inputs_hash": (
            "computed_prev_open_offset_values|prev_d_values|"
            "allowed_directed_tuple_values|next_d_values|"
            "computed_next_parity_values|lower_terminal_four_slot_values"
        ),
        "theorem_status": "hypothesis_not_proved",
        "universal_proof_complete": False,
        "factor_found_claimed": False,
        "distance_to_final_solution": (
            "the aircraft has climbed back to the 12-lane selector surface; "
            "Round 18 maps the obstruction mechanisms but does not land the "
            "global factor-finding theorem"
        ),
        "grok_mirror_note": (
            "Grok co-pilot independent execution of the identical mechanical "
            "derive_mechanism_class rule on the same annotated corpus. "
            "Result must match Codex codex_round18 output for confirmation."
        ),
    }


def proposed_next_proof_object(rows: list[dict[str, object]]) -> dict[str, object]:
    """Next proof pressure implied by the compression outcome."""
    summary = compression_summary(rows)
    if summary["compression_success"]:
        action = "prove the strongest shared mechanism law first"
    else:
        action = (
            "return to the component-law proof contract, but attach each law to "
            "its extracted width/residue/parity feature vector"
        )
    # Pick a representative derived class for the next-law hint
    excluded = [r for r in rows if r["survivor_status"] == "excluded"]
    recommended = (
        excluded[0]["derived_mechanism_class"] if excluded else "survivor_terminal_lift_aligned"
    )
    return {
        "rule_id": RULE_ID,
        "decision_rule": (
            "if mechanism_group_count < component_law_count, prove the shared "
            "mechanism; otherwise preserve the component-law contract with "
            "extracted mechanisms"
        ),
        "recommended_next_action": action,
        "recommended_next_law": recommended,
        "theorem_status": "hypothesis_not_proved",
        "universal_proof_complete": False,
    }


def main() -> int:
    """Execute the Grok mirror and emit the five artifacts."""
    rows = matrix_rows()
    if len(rows) != 12:
        raise ValueError(f"expected exactly 12 lanes, got {len(rows)}")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    write_jsonl(OUTPUT_DIR / "lane_mechanism_matrix.jsonl", rows)
    write_json(OUTPUT_DIR / "mechanism_groups.json", mechanism_groups(rows))
    write_json(OUTPUT_DIR / "compression_summary.json", compression_summary(rows))
    write_json(
        OUTPUT_DIR / "proposed_next_proof_object.json",
        proposed_next_proof_object(rows),
    )
    write_jsonl(
        OUTPUT_DIR / "falsifier_contracts.jsonl",
        [
            {
                "rule_id": RULE_ID,
                "lane": row["lane"],
                "derived_mechanism_class": row["derived_mechanism_class"],
                "falsifier_contract": row["falsifier_contract"],
            }
            for row in rows
        ],
    )
    payload = compression_summary(rows)
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
