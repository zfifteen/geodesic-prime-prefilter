#!/usr/bin/env python3
"""Round 11 priority matrix for component obstruction laws."""

from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path

from first_gap_compatibility_check import write_json, write_jsonl
from slot_factor_public_quotient_test import read_jsonl


THIS_DIR = Path(__file__).resolve().parent
ROUND8_OUTPUT_DIR = THIS_DIR / "output" / "codex_round8_finite_obstruction_table"
ROUND9_OUTPUT_DIR = THIS_DIR / "output" / "codex_round9_public_component_obstruction_audit"
ROUND10_OUTPUT_DIR = THIS_DIR / "output" / "codex_round10_component_law_scaffold"
OUTPUT_DIR = THIS_DIR / "output" / "codex_round11_component_law_priority_matrix"
RULE_ID = "pedk_codex_round11_component_law_priority_matrix_v1"

PROOF_ACTIONS = {
    "next_parity_odd": (
        "Prove that lane 163|19 reaches the allowed even|mid|o4 tuple "
        "only through even next parity."
    ),
    "prev_d_le4": (
        "Prove that lane 79|43 reaches prev_open_offset=4 only with "
        "prev_d>4."
    ),
    "prev_open_offset_4": (
        "Prove that lane 19|163 reaches at_winner only through "
        "prev_open_offset values other than 4."
    ),
    "directed_tuple": (
        "Prove that the seven assigned lanes reaching bounded entry never "
        "match even|mid|o4 or odd|early|o6."
    ),
}

PROOF_ORDER = {
    "next_parity_odd": 1,
    "prev_d_le4": 2,
    "prev_open_offset_4": 3,
    "directed_tuple": 4,
}


def load_component_laws() -> list[dict[str, object]]:
    """Return Round 10 component-law contracts."""
    return read_jsonl(ROUND10_OUTPUT_DIR / "component_law_table.jsonl")


def load_assignments() -> list[dict[str, object]]:
    """Return Round 10 lane-to-law assignments."""
    return read_jsonl(ROUND10_OUTPUT_DIR / "excluded_lane_law_assignments.jsonl")


def load_near_misses() -> list[dict[str, object]]:
    """Return Round 9 near-miss rows."""
    return read_jsonl(ROUND9_OUTPUT_DIR / "near_miss_rows.jsonl")


def load_lane_coordinates() -> dict[str, dict[str, object]]:
    """Return Round 8 lane-coordinate rows keyed by lane."""
    rows = read_jsonl(ROUND8_OUTPUT_DIR / "finite_lane_obstruction_table.jsonl")
    return {str(row["lane"]): row for row in rows}


def group_by_key(rows: list[dict[str, object]], key: str) -> dict[str, list[dict[str, object]]]:
    """Return rows grouped by one string key."""
    groups: dict[str, list[dict[str, object]]] = defaultdict(list)
    for row in rows:
        groups[str(row[key])].append(row)
    return dict(groups)


def near_miss_signature_counts(rows: list[dict[str, object]]) -> dict[str, int]:
    """Return compact signature counts for near-miss rows."""
    counts = Counter(str(row["signature"]) for row in rows)
    return dict(sorted(counts.items()))


def lane_coordinate_fields(row: dict[str, object]) -> dict[str, object]:
    """Return proof-relevant CRT coordinate fields for one lane."""
    return {
        "lane": row["lane"],
        "orientation": row["orientation"],
        "phase_mod36": row["phase_mod36"],
        "a_mod6": row["a_mod6"],
        "b_mod6": row["b_mod6"],
        "candidate_required_a_mod6": row["candidate_required_a_mod6"],
        "same_phase_equation": row["same_phase_equation"],
    }


def component_priority_matrix() -> list[dict[str, object]]:
    """Return one proof-priority row per component law."""
    laws = load_component_laws()
    assignments_by_law = group_by_key(load_assignments(), "assigned_component_law")
    near_misses_by_lane = group_by_key(load_near_misses(), "lane")
    lane_coordinates = load_lane_coordinates()
    rows = []

    for law in laws:
        name = str(law["component_law"])
        assigned = assignments_by_law.get(name, [])
        lanes = sorted(str(item["lane"]) for item in assigned)
        near_misses = [
            row
            for lane in lanes
            for row in near_misses_by_lane.get(lane, [])
        ]
        lane_fields = [
            lane_coordinate_fields(lane_coordinates[lane])
            for lane in lanes
        ]
        rows.append(
            {
                "rule_id": RULE_ID,
                "component_law": name,
                "priority_rank": PROOF_ORDER[name],
                "covered_lanes": lanes,
                "covered_lane_count": len(lanes),
                "near_miss_row_count": len(near_misses),
                "max_near_miss_rows_for_one_lane": max(
                    (len(near_misses_by_lane.get(lane, [])) for lane in lanes),
                    default=0,
                ),
                "near_miss_signature_counts": near_miss_signature_counts(near_misses),
                "lane_coordinates": lane_fields,
                "prior_surface": law["prior_surface"],
                "candidate_universal_claim": law["candidate_universal_claim"],
                "falsifier_contract": law["falsifier_contract"],
                "proof_dependency": "finite_lane_table_plus_public_gap_grammar",
                "proof_action": PROOF_ACTIONS[name],
                "proof_status": "unproved",
            }
        )

    rows.sort(key=lambda row: int(row["priority_rank"]))
    return rows


def lane_dependency_table() -> list[dict[str, object]]:
    """Return one proof-dependency row per excluded lane."""
    near_misses_by_lane = group_by_key(load_near_misses(), "lane")
    lane_coordinates = load_lane_coordinates()
    rows = []
    for assignment in load_assignments():
        lane = str(assignment["lane"])
        coord = lane_coordinates[lane]
        near_misses = near_misses_by_lane.get(lane, [])
        rows.append(
            {
                "rule_id": RULE_ID,
                "lane": lane,
                "assigned_component_law": assignment["assigned_component_law"],
                "priority_rank": PROOF_ORDER[str(assignment["assigned_component_law"])],
                "first_zero_stage": assignment["first_zero_stage"],
                "last_nonzero_stage": assignment["last_nonzero_stage"],
                "near_miss_row_count": len(near_misses),
                "near_miss_signature_counts": near_miss_signature_counts(near_misses),
                "lane_coordinates": lane_coordinate_fields(coord),
                "falsifier_contract": assignment["falsifier_contract"],
                "proof_dependency": "public_gap_grammar",
                "proof_status": "unproved",
            }
        )
    rows.sort(key=lambda row: (int(row["priority_rank"]), str(row["lane"])))
    return rows


def recommended_proof_order() -> list[dict[str, object]]:
    """Return the recommended attack order for the four laws."""
    matrix = component_priority_matrix()
    return [
        {
            "rule_id": RULE_ID,
            "rank": row["priority_rank"],
            "component_law": row["component_law"],
            "reason": (
                "singleton last-stage blocker"
                if row["component_law"] == "next_parity_odd"
                else "singleton bounded-entry blocker"
                if row["component_law"] == "prev_d_le4"
                else "singleton entry-offset blocker"
                if row["component_law"] == "prev_open_offset_4"
                else "broad seven-lane directed-tuple blocker"
            ),
            "covered_lanes": row["covered_lanes"],
            "proof_action": row["proof_action"],
            "proof_status": row["proof_status"],
        }
        for row in matrix
    ]


def remaining_universal_laws() -> list[dict[str, object]]:
    """Return the still-unproved universal laws."""
    return [
        {
            "rule_id": RULE_ID,
            "component_law": row["component_law"],
            "candidate_universal_claim": row["candidate_universal_claim"],
            "falsifier_contract": row["falsifier_contract"],
            "proof_status": "unproved",
        }
        for row in component_priority_matrix()
    ]


def summary() -> dict[str, object]:
    """Return Round 11 summary."""
    matrix = component_priority_matrix()
    lane_rows = lane_dependency_table()
    singleton_laws = [row for row in matrix if int(row["covered_lane_count"]) == 1]
    broad_laws = [row for row in matrix if int(row["covered_lane_count"]) > 1]
    return {
        "rule_id": RULE_ID,
        "status": "measured_component_law_priority_matrix",
        "component_law_count": len(matrix),
        "excluded_lane_dependency_count": len(lane_rows),
        "singleton_component_law_count": len(singleton_laws),
        "broad_component_law_count": len(broad_laws),
        "laws_requiring_public_gap_grammar": len(matrix),
        "laws_with_current_universal_proof": 0,
        "recommended_first_component_law": matrix[0]["component_law"],
        "recommended_first_law_lanes": matrix[0]["covered_lanes"],
        "recommended_first_law_reason": "singleton last-stage blocker after all prior predicates",
        "proof_composition_ready": True,
        "universal_proof_complete": False,
        "theorem_status": "hypothesis_not_proved",
        "distance_to_final_solution": (
            "proof obligations are prioritized; all four component grammar "
            "laws and the terminal image remain unproved universally"
        ),
        "next_required_proof_object": (
            "prove next_parity_odd for lane 163|19, then continue through "
            "prev_d_le4, prev_open_offset_4, and directed_tuple"
        ),
    }


def main() -> int:
    """Run the Round 11 priority-matrix builder."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    write_jsonl(OUTPUT_DIR / "component_law_priority_matrix.jsonl", component_priority_matrix())
    write_jsonl(OUTPUT_DIR / "lane_proof_dependency_table.jsonl", lane_dependency_table())
    write_jsonl(OUTPUT_DIR / "recommended_proof_order.jsonl", recommended_proof_order())
    write_jsonl(OUTPUT_DIR / "remaining_universal_laws.jsonl", remaining_universal_laws())
    payload = summary()
    write_json(OUTPUT_DIR / "summary.json", payload)
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
