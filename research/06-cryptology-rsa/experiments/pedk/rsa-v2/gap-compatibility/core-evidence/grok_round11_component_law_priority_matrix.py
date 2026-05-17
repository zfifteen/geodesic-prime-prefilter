#!/usr/bin/env python3
"""Grok Round 11 mirror for component-law proof priority."""

from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path

from first_gap_compatibility_check import write_json, write_jsonl
from slot_factor_public_quotient_test import read_jsonl


THIS_DIR = Path(__file__).resolve().parent
ROUND8_OUTPUT_DIR = THIS_DIR / "output" / "grok_round8_finite_obstruction_table"
ROUND9_OUTPUT_DIR = THIS_DIR / "output" / "grok_round9_public_component_obstruction_audit"
ROUND10_OUTPUT_DIR = THIS_DIR / "output" / "grok_round10_component_law_scaffold"
OUTPUT_DIR = THIS_DIR / "output" / "grok_round11_component_law_priority_matrix"
RULE_ID = "pedk_grok_round11_component_law_priority_matrix_v1"

PROOF_ORDER = {
    "next_parity_odd": 1,
    "prev_d_le4": 2,
    "prev_open_offset_4": 3,
    "directed_tuple": 4,
}

PROOF_ACTIONS = {
    "next_parity_odd": (
        "Attack the lane 163|19 odd-exit law first because it is a "
        "singleton last-stage blocker."
    ),
    "prev_d_le4": (
        "Attack the lane 79|43 bounded-d law second because it is a "
        "singleton bounded-entry blocker."
    ),
    "prev_open_offset_4": (
        "Attack the lane 19|163 offset law third because it is a singleton "
        "entry-offset blocker with more near-miss rows."
    ),
    "directed_tuple": (
        "Attack the seven-lane directed-tuple law last because it is the "
        "broadest grammar law."
    ),
}


def group_by_key(rows: list[dict[str, object]], key: str) -> dict[str, list[dict[str, object]]]:
    """Return rows grouped by one string key."""
    groups: dict[str, list[dict[str, object]]] = defaultdict(list)
    for row in rows:
        groups[str(row[key])].append(row)
    return dict(groups)


def load_jsonl(path: Path) -> list[dict[str, object]]:
    """Return JSONL rows from an existing artifact."""
    return read_jsonl(path)


def lane_coordinates() -> dict[str, dict[str, object]]:
    """Return Grok Round 8 lane coordinates keyed by lane."""
    rows = load_jsonl(ROUND8_OUTPUT_DIR / "finite_lane_obstruction_table.jsonl")
    return {str(row["lane"]): row for row in rows}


def compact_coordinates(row: dict[str, object]) -> dict[str, object]:
    """Return fields needed for proof ordering."""
    return {
        "lane": row["lane"],
        "orientation": row["orientation"],
        "phase_mod36": row["phase_mod36"],
        "a_mod6": row["a_mod6"],
        "b_mod6": row["b_mod6"],
        "same_phase_equation": row["same_phase_equation"],
    }


def signature_counts(rows: list[dict[str, object]]) -> dict[str, int]:
    """Return near-miss signature counts."""
    counts = Counter(str(row["signature"]) for row in rows)
    return dict(sorted(counts.items()))


def component_law_priority_matrix() -> list[dict[str, object]]:
    """Return one priority row per Round 10 component law."""
    laws = load_jsonl(ROUND10_OUTPUT_DIR / "component_law_table.jsonl")
    assignments = group_by_key(
        load_jsonl(ROUND10_OUTPUT_DIR / "excluded_lane_law_assignments.jsonl"),
        "assigned_component_law",
    )
    near_misses = group_by_key(
        load_jsonl(ROUND9_OUTPUT_DIR / "near_miss_rows.jsonl"),
        "lane",
    )
    coords = lane_coordinates()
    rows = []
    for law in laws:
        component = str(law["component_law"])
        assigned = assignments[component]
        lanes = sorted(str(row["lane"]) for row in assigned)
        lane_near_misses = [
            item
            for lane in lanes
            for item in near_misses.get(lane, [])
        ]
        rows.append(
            {
                "rule_id": RULE_ID,
                "component_law": component,
                "priority_rank": PROOF_ORDER[component],
                "covered_lanes": lanes,
                "covered_lane_count": len(lanes),
                "near_miss_row_count": len(lane_near_misses),
                "near_miss_signature_counts": signature_counts(lane_near_misses),
                "lane_coordinates": [
                    compact_coordinates(coords[lane])
                    for lane in lanes
                ],
                "prior_surface": law["prior_surface"],
                "candidate_universal_claim": law["candidate_universal_claim"],
                "falsifier_contract": law["falsifier_contract"],
                "proof_action": PROOF_ACTIONS[component],
                "proof_status": "unproved",
            }
        )
    rows.sort(key=lambda row: int(row["priority_rank"]))
    return rows


def lane_proof_dependency_table() -> list[dict[str, object]]:
    """Return one proof-dependency row per excluded lane."""
    assignments = load_jsonl(ROUND10_OUTPUT_DIR / "excluded_lane_law_assignments.jsonl")
    near_misses = group_by_key(load_jsonl(ROUND9_OUTPUT_DIR / "near_miss_rows.jsonl"), "lane")
    coords = lane_coordinates()
    rows = []
    for assignment in assignments:
        component = str(assignment["assigned_component_law"])
        lane = str(assignment["lane"])
        rows.append(
            {
                "rule_id": RULE_ID,
                "lane": lane,
                "assigned_component_law": component,
                "priority_rank": PROOF_ORDER[component],
                "first_zero_stage": assignment["first_zero_stage"],
                "last_nonzero_stage": assignment["last_nonzero_stage"],
                "near_miss_row_count": len(near_misses.get(lane, [])),
                "near_miss_signature_counts": signature_counts(near_misses.get(lane, [])),
                "lane_coordinates": compact_coordinates(coords[lane]),
                "falsifier_contract": assignment["falsifier_contract"],
                "proof_status": "unproved",
            }
        )
    rows.sort(key=lambda row: (int(row["priority_rank"]), str(row["lane"])))
    return rows


def recommended_proof_order() -> list[dict[str, object]]:
    """Return ordered proof recommendations."""
    return [
        {
            "rule_id": RULE_ID,
            "rank": row["priority_rank"],
            "component_law": row["component_law"],
            "covered_lanes": row["covered_lanes"],
            "proof_action": row["proof_action"],
            "proof_status": "unproved",
        }
        for row in component_law_priority_matrix()
    ]


def remaining_universal_laws() -> list[dict[str, object]]:
    """Return all still-unproved component laws."""
    return [
        {
            "rule_id": RULE_ID,
            "component_law": row["component_law"],
            "candidate_universal_claim": row["candidate_universal_claim"],
            "falsifier_contract": row["falsifier_contract"],
            "proof_status": "unproved",
        }
        for row in component_law_priority_matrix()
    ]


def summary() -> dict[str, object]:
    """Return Grok Round 11 summary."""
    matrix = component_law_priority_matrix()
    lane_rows = lane_proof_dependency_table()
    return {
        "rule_id": RULE_ID,
        "status": "measured_component_law_priority_matrix",
        "component_law_count": len(matrix),
        "excluded_lane_dependency_count": len(lane_rows),
        "singleton_component_law_count": sum(
            1 for row in matrix if int(row["covered_lane_count"]) == 1
        ),
        "broad_component_law_count": sum(
            1 for row in matrix if int(row["covered_lane_count"]) > 1
        ),
        "laws_requiring_public_gap_grammar": len(matrix),
        "laws_with_current_universal_proof": 0,
        "recommended_first_component_law": matrix[0]["component_law"],
        "recommended_first_law_lanes": matrix[0]["covered_lanes"],
        "recommended_first_law_reason": "singleton last-stage blocker",
        "proof_composition_ready": True,
        "universal_proof_complete": False,
        "theorem_status": "hypothesis_not_proved",
        "distance_to_final_solution": (
            "four universal component proofs remain before the lane-survival "
            "theorem can compose with the terminal image"
        ),
        "next_required_proof_object": (
            "universal proof of next_parity_odd for lane 163|19"
        ),
    }


def main() -> int:
    """Run the Grok Round 11 mirror."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    write_jsonl(OUTPUT_DIR / "component_law_priority_matrix.jsonl", component_law_priority_matrix())
    write_jsonl(OUTPUT_DIR / "lane_proof_dependency_table.jsonl", lane_proof_dependency_table())
    write_jsonl(OUTPUT_DIR / "recommended_proof_order.jsonl", recommended_proof_order())
    write_jsonl(OUTPUT_DIR / "remaining_universal_laws.jsonl", remaining_universal_laws())
    payload = summary()
    write_json(OUTPUT_DIR / "summary.json", payload)
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
