#!/usr/bin/env python3
"""Round 19 shadow-surface compression test for the same-phase lanes."""

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
)
from first_gap_compatibility_check import write_json, write_jsonl
from modulus_gap_grammar_probe import first_open_offset


THIS_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = THIS_DIR / "output" / "codex_round19_shadow_surface_compression"
RULE_ID = "pedk_codex_round19_shadow_surface_compression_v1"
SURVIVOR_LANES = {"43|79", "49|13"}
SYMMETRIC_PAIR = ("163|19", "19|163")


def parity_name(value_mod2: int) -> str:
    """Return a parity label."""
    return "even" if value_mod2 == 0 else "odd"


def enriched_state(
    row: dict[str, object],
    row_index: dict[tuple[str, str], dict[str, object]],
) -> dict[str, object]:
    """Return public width, residue, first-open, and parity-lift features."""
    enriched = row_index[(str(row["window"]), str(row["case_id"]))]
    n_value = int(enriched["N"])
    containing_left = n_value - int(enriched["public_n_offset_from_left"])
    containing_right = n_value + int(enriched["public_n_offset_from_right"])
    previous_gap = enriched["public_previous_gap"]
    following_gap = enriched["public_following_gap"]
    previous_gap_width = int(previous_gap["gap_width"])
    previous_left_mod30 = (containing_left % 30 - previous_gap_width) % 30
    next_winner_offset = int(following_gap["winner_offset"])
    return {
        "public_containing_left_mod30": containing_left % 30,
        "public_containing_right_mod180": containing_right % 180,
        "public_previous_gap_width": previous_gap_width,
        "public_following_gap_width": int(following_gap["gap_width"]),
        "public_previous_winner_offset": int(previous_gap["winner_offset"]),
        "public_following_winner_offset": next_winner_offset,
        "previous_left_mod30_by_width": previous_left_mod30,
        "computed_prev_open_offset": first_open_offset(previous_left_mod30),
        "computed_next_parity": parity_name((containing_right + next_winner_offset) % 2),
    }


def public_prefix(row: dict[str, object]) -> bool:
    """Return whether a row reaches the shared shadow prefix."""
    return bool(row["same_mod36"]) and bool(row["rres_o4_o4"]) and (
        row["public_gwr_side"] == "at_winner"
    )


def gate_vector(row: dict[str, object], state: dict[str, object]) -> dict[str, bool]:
    """Return the five post-prefix public gates using computed transport fields."""
    return {
        "prev_open_offset_4": int(state["computed_prev_open_offset"]) == 4,
        "prev_d_le4": int(row["prev_d"]) <= 4,
        "directed_tuple_allowed": directed_tuple(row) in DIRECTED_TUPLES,
        "next_d_le4": int(row["next_d"]) <= 4,
        "next_parity_odd": state["computed_next_parity"] == "odd",
    }


def passes_full_chain(gates: dict[str, bool]) -> bool:
    """Return whether all post-prefix gates pass."""
    return all(gates.values())


def shadow_row_for_lane(
    row: dict[str, object],
    lane: str,
    row_index: dict[tuple[str, str], dict[str, object]],
) -> dict[str, object] | None:
    """Return one shadow row, or None if row is outside the lane shadow."""
    if str(row["factor_mod180_lane"]) != lane or not public_prefix(row):
        return None
    state = enriched_state(row, row_index)
    gates = gate_vector(row, state)
    if passes_full_chain(gates):
        return None
    row_class, class_rule = derive_shadow_row_class(gates)
    tuple_value = "|".join(directed_tuple(row))
    return {
        "rule_id": RULE_ID,
        "lane": lane,
        "window": row["window"],
        "case_id": row["case_id"],
        "signature": row["signature"],
        "directed_tuple": tuple_value,
        "prev_open_offset_observed": int(row["prev_open_offset"]),
        "computed_prev_open_offset": int(state["computed_prev_open_offset"]),
        "prev_d": int(row["prev_d"]),
        "next_d": int(row["next_d"]),
        "next_parity_observed": row["next_parity"],
        "computed_next_parity": state["computed_next_parity"],
        "public_previous_gap_width": state["public_previous_gap_width"],
        "public_following_gap_width": state["public_following_gap_width"],
        "public_containing_left_mod30": state["public_containing_left_mod30"],
        "public_containing_right_mod180": state["public_containing_right_mod180"],
        "previous_left_mod30_by_width": state["previous_left_mod30_by_width"],
        "next_winner_offset": state["public_following_winner_offset"],
        "previous_winner_offset": state["public_previous_winner_offset"],
        "phase_width_pair": row["phase_width_pair"],
        "lower_predecessor_pair": row["lower_predecessor_residue_width_pair"],
        "lower_predecessor_open_slot_count": int(
            row["lower_predecessor_open_slot_count"]
        ),
        "lower_terminal_four_slot": bool(row["lower_terminal_four_slot"]),
        "gate_vector": gates,
        "shadow_row_class": row_class,
        "shadow_row_class_rule": class_rule,
        "shadow_failure_signature": shadow_failure_signature(row, state, gates, row_class),
        "theorem_status": "hypothesis_not_proved",
        "universal_proof_complete": False,
        "factor_found": False,
    }


def derive_shadow_row_class(gates: dict[str, bool]) -> tuple[str, str]:
    """Return the first-failing shadow row class and its fixed rule."""
    if not gates["prev_open_offset_4"]:
        return (
            "entry_width_residue_open_offset_shadow_defect",
            "computed_prev_open_offset != 4",
        )
    if not gates["prev_d_le4"]:
        return ("entry_d_bound_shadow_defect", "computed_prev_open_offset=4 and prev_d>4")
    if not gates["directed_tuple_allowed"]:
        return (
            "directed_tuple_shadow_defect",
            "entry gates pass and directed_tuple not in allowed set",
        )
    if not gates["next_d_le4"]:
        return ("exit_d_bound_shadow_defect", "allowed tuple passes and next_d>4")
    if not gates["next_parity_odd"]:
        return (
            "exit_offset_parity_shadow_defect",
            "allowed tuple and next_d pass but computed_next_parity != odd",
        )
    return ("unclassified_shadow_defect", "row failed shadow selection unexpectedly")


def shadow_failure_signature(
    row: dict[str, object],
    state: dict[str, object],
    gates: dict[str, bool],
    row_class: str,
) -> str:
    """Return a compact mechanical signature for one shadow row."""
    failed = [name for name, value in gates.items() if not value]
    return "|".join(
        [
            row_class,
            f"failed={','.join(failed)}",
            f"prev_width={state['public_previous_gap_width']}",
            f"prev_left30={state['previous_left_mod30_by_width']}",
            f"prev_open={state['computed_prev_open_offset']}",
            f"right180={state['public_containing_right_mod180']}",
            f"next_offset={state['public_following_winner_offset']}",
            f"next_parity={state['computed_next_parity']}",
            f"tuple={'|'.join(directed_tuple(row))}",
        ]
    )


def shadow_rows() -> list[dict[str, object]]:
    """Return every one-gate-or-more shadow row for the 12 lanes."""
    rows = annotated_rows()
    row_index = corpus_row_index()
    out = []
    for lane in theoretical_same_phase_lanes():
        lane_value = str(lane["lane"])
        for row in rows:
            shadow = shadow_row_for_lane(row, lane_value, row_index)
            if shadow is not None:
                out.append(shadow)
    out.sort(key=lambda item: (str(item["lane"]), str(item["case_id"])))
    return out


def failure_count(row: dict[str, object]) -> int:
    """Return number of failed gates in one shadow row."""
    return sum(1 for value in dict(row["gate_vector"]).values() if not value)


def primary_shadow_class(rows: list[dict[str, object]]) -> tuple[str, str]:
    """Return the dominant class by count with deterministic tie-break."""
    if not rows:
        return ("no_shadow_rows", "no rows reached the shadow prefix")
    counts = Counter(str(row["shadow_row_class"]) for row in rows)
    count, row_class = max((count, row_class) for row_class, count in counts.items())
    return (row_class, f"most frequent shadow_row_class with count {count}")


def lane_shadow_profiles(
    rows: list[dict[str, object]],
    profile_scope: str,
) -> list[dict[str, object]]:
    """Return one profile per theoretical same-phase lane."""
    by_lane: dict[str, list[dict[str, object]]] = defaultdict(list)
    for row in rows:
        by_lane[str(row["lane"])].append(row)
    profiles = []
    for lane in theoretical_same_phase_lanes():
        lane_value = str(lane["lane"])
        lane_rows = by_lane[lane_value]
        primary, primary_rule = primary_shadow_class(lane_rows)
        class_counts = Counter(str(row["shadow_row_class"]) for row in lane_rows)
        signature_counts = Counter(str(row["shadow_failure_signature"]) for row in lane_rows)
        gate_fail_counts = Counter()
        for row in lane_rows:
            for gate, passed in dict(row["gate_vector"]).items():
                if not passed:
                    gate_fail_counts[gate] += 1
        profiles.append(
            {
                "rule_id": RULE_ID,
                "profile_scope": profile_scope,
                "lane": lane_value,
                "orientation": lane["orientation"],
                "phase_mod36": lane["phase_mod36"],
                "shadow_row_count": len(lane_rows),
                "primary_shadow_mechanism_class": primary,
                "primary_shadow_mechanism_rule": primary_rule,
                "shadow_class_counts": dict(sorted(class_counts.items())),
                "gate_failure_counts": dict(sorted(gate_fail_counts.items())),
                "top_shadow_failure_signatures": [
                    {"signature": signature, "count": count}
                    for signature, count in sorted(
                        signature_counts.items(),
                        key=lambda item: (-item[1], item[0]),
                    )[:3]
                ],
                "contains_entry_width_residue_shadow_defect": (
                    "entry_width_residue_open_offset_shadow_defect" in class_counts
                ),
                "theorem_status": "hypothesis_not_proved",
                "universal_proof_complete": False,
                "factor_found": False,
            }
        )
    return profiles


def mechanism_groups(profiles: list[dict[str, object]]) -> dict[str, object]:
    """Return lanes grouped by dominant shadow mechanism class."""
    groups: dict[str, list[str]] = defaultdict(list)
    for profile in profiles:
        groups[str(profile["primary_shadow_mechanism_class"])].append(str(profile["lane"]))
    return {
        "rule_id": RULE_ID,
        "grouping_basis": "primary_shadow_mechanism_class from shadow row features",
        "groups": {key: sorted(value) for key, value in sorted(groups.items())},
        "theorem_status": "hypothesis_not_proved",
        "universal_proof_complete": False,
        "factor_found_claimed": False,
    }


def shadow_derivation_rules() -> list[dict[str, object]]:
    """Return the fixed rules used before count inspection."""
    return [
        {
            "class": "entry_width_residue_open_offset_shadow_defect",
            "rule": "computed_prev_open_offset != 4",
        },
        {
            "class": "entry_d_bound_shadow_defect",
            "rule": "computed_prev_open_offset=4 and prev_d>4",
        },
        {
            "class": "directed_tuple_shadow_defect",
            "rule": "entry gates pass and directed_tuple not in allowed set",
        },
        {
            "class": "exit_d_bound_shadow_defect",
            "rule": "allowed tuple passes and next_d>4",
        },
        {
            "class": "exit_offset_parity_shadow_defect",
            "rule": "allowed tuple and next_d pass but computed_next_parity != odd",
        },
    ]


def lane_blind_boundary(rows: list[dict[str, object]]) -> dict[str, object]:
    """Return the lane-conditioning boundary requested by Grok."""
    class_counts = Counter(str(row["shadow_row_class"]) for row in rows)
    signature_counts = Counter(str(row["shadow_failure_signature"]) for row in rows)
    return {
        "rule_id": RULE_ID,
        "boundary": "shadow rows are lane-conditioned by same_mod36 and factor_mod180_lane",
        "lane_blind_claim_status": "not_tested_as_public_factor_selector",
        "all_shadow_row_class_counts": dict(sorted(class_counts.items())),
        "top_lane_conditioned_shadow_signatures": [
            {"signature": signature, "count": count}
            for signature, count in sorted(
                signature_counts.items(),
                key=lambda item: (-item[1], item[0]),
            )[:10]
        ],
    }


def compression_summary(
    rows: list[dict[str, object]],
    profiles: list[dict[str, object]],
    exact_one_profiles: list[dict[str, object]],
) -> dict[str, object]:
    """Return the shadow-compression summary."""
    profile_by_lane = {str(row["lane"]): row for row in profiles}
    exact_profile_by_lane = {str(row["lane"]): row for row in exact_one_profiles}
    groups = mechanism_groups(profiles)["groups"]
    pair_collapsed = (
        profile_by_lane[SYMMETRIC_PAIR[0]]["primary_shadow_mechanism_class"]
        == profile_by_lane[SYMMETRIC_PAIR[1]]["primary_shadow_mechanism_class"]
    )
    pair_class = profile_by_lane[SYMMETRIC_PAIR[0]][
        "primary_shadow_mechanism_class"
    ]
    survivor_classes = {
        lane: profile_by_lane[lane]["primary_shadow_mechanism_class"]
        for lane in sorted(SURVIVOR_LANES)
    }
    survivor_contamination = pair_class in survivor_classes.values()
    exact_pair_classes = {
        lane: exact_profile_by_lane[lane]["primary_shadow_mechanism_class"]
        for lane in SYMMETRIC_PAIR
    }
    exact_pair_collapsed = exact_pair_classes[SYMMETRIC_PAIR[0]] == exact_pair_classes[
        SYMMETRIC_PAIR[1]
    ]
    mechanism_class_count = len(groups)
    return {
        "rule_id": RULE_ID,
        "status": "measured_shadow_surface_compression",
        "shadow_row_count": len(rows),
        "total_lanes": len(profiles),
        "survivor_lanes": sorted(SURVIVOR_LANES),
        "primary_shadow_mechanism_group_count": mechanism_class_count,
        "shadow_mechanism_groups": groups,
        "symmetric_pair": list(SYMMETRIC_PAIR),
        "symmetric_pair_primary_classes": {
            lane: profile_by_lane[lane]["primary_shadow_mechanism_class"]
            for lane in SYMMETRIC_PAIR
        },
        "symmetric_pair_collapsed": pair_collapsed,
        "symmetric_pair_collapsed_into_entry_width_residue": (
            pair_collapsed
            and pair_class == "entry_width_residue_open_offset_shadow_defect"
        ),
        "survivor_primary_shadow_classes": survivor_classes,
        "survivor_shadow_contamination": survivor_contamination,
        "exact_one_gate_symmetric_pair_primary_classes": exact_pair_classes,
        "exact_one_gate_symmetric_pair_collapsed": exact_pair_collapsed,
        "broad_shadow_pair_collapse_signal": (
            pair_collapsed
            and pair_class == "entry_width_residue_open_offset_shadow_defect"
        ),
        "shadow_compression_success": (
            pair_collapsed
            and pair_class == "entry_width_residue_open_offset_shadow_defect"
            and not survivor_contamination
            and exact_pair_collapsed
        ),
        "shadow_insight_status": (
            "weakened_by_survivor_contamination_or_exact_one_gate_failure"
            if survivor_contamination or not exact_pair_collapsed
            else "supported_on_shadow_surface"
        ),
        "falsifier_for_shadow_insight": (
            "Falsified if 163|19 and 19|163 do not share an entry-side "
            "width/residue/open-offset primary shadow class, or if survivor "
            "lanes carry the same contradictory primary shadow class."
        ),
        "theorem_status": "hypothesis_not_proved",
        "universal_proof_complete": False,
        "factor_found_claimed": False,
        "distance_to_final_solution": (
            "Round 19 tests whether Round 18 missed compression by using "
            "last-nonzero representatives; it remains lane-conditioned and "
            "does not prove a public factor selector."
        ),
    }


def main() -> int:
    """Run the Round 19 shadow-surface compression test."""
    rows = shadow_rows()
    profiles = lane_shadow_profiles(rows, "all_shadow_rows")
    exact_one_rows = [row for row in rows if failure_count(row) == 1]
    exact_one_profiles = lane_shadow_profiles(exact_one_rows, "exact_one_gate_shadow_rows")
    if len(profiles) != 12:
        raise ValueError(f"expected 12 lane profiles, got {len(profiles)}")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    write_jsonl(OUTPUT_DIR / "shadow_rows.jsonl", rows)
    write_jsonl(OUTPUT_DIR / "exact_one_gate_shadow_rows.jsonl", exact_one_rows)
    write_jsonl(OUTPUT_DIR / "lane_shadow_profiles.jsonl", profiles)
    write_jsonl(
        OUTPUT_DIR / "exact_one_gate_lane_shadow_profiles.jsonl",
        exact_one_profiles,
    )
    write_json(OUTPUT_DIR / "shadow_mechanism_groups.json", mechanism_groups(profiles))
    write_json(OUTPUT_DIR / "shadow_derivation_rules.json", shadow_derivation_rules())
    write_json(OUTPUT_DIR / "lane_blind_boundary.json", lane_blind_boundary(rows))
    payload = compression_summary(rows, profiles, exact_one_profiles)
    write_json(OUTPUT_DIR / "shadow_compression_summary.json", payload)
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
