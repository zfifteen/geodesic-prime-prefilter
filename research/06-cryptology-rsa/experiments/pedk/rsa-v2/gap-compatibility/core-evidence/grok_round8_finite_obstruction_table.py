#!/usr/bin/env python3
"""Grok Round 8 finite obstruction workbench for lane survival."""

from __future__ import annotations

import json
from pathlib import Path

from codex_round5_same_phase_boundary_probe import annotated_rows, target_rows
from codex_round6_sync_chain_table import theoretical_same_phase_lanes
from first_gap_compatibility_check import write_json, write_jsonl


THIS_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = THIS_DIR / "output" / "grok_round8_finite_obstruction_table"
RULE_ID = "grok_round8_finite_obstruction_table_v1"
SIGNATURE_EQUATIONS = {
    "13|19": {
        "signature": "even|mid|o4|odd",
        "required_a_mod6": 1,
        "surviving_lane": "43|79",
    },
    "19|13": {
        "signature": "odd|early|o6|odd",
        "required_a_mod6": 1,
        "surviving_lane": "49|13",
    },
}
EXPECTED_LANES = {"43|79", "49|13"}


def lane_coordinates(lane: dict[str, object]) -> dict[str, object]:
    """Return Z/6Z coordinates for one theoretical lane."""
    p_mod30 = int(lane["p_mod30"])
    q_mod30 = int(lane["q_mod30"])
    p_mod180 = int(lane["p_mod180"])
    q_mod180 = int(lane["q_mod180"])
    a_mod6 = (p_mod180 - p_mod30) // 30
    b_mod6 = (q_mod180 - q_mod30) // 30
    orientation = str(lane["orientation"])
    expected_difference = 5 if orientation == "13|19" else 1
    if (a_mod6 - b_mod6) % 6 != expected_difference:
        raise ValueError(f"bad same-phase coordinates: {lane['lane']}")
    return {
        "a_mod6": a_mod6,
        "b_mod6": b_mod6,
        "same_phase_equation": f"a-b={expected_difference} mod 6",
    }


def measured_surviving_rows() -> list[dict[str, object]]:
    """Return measured same-phase target rows from the current corpus."""
    return [row for row in target_rows(annotated_rows()) if row["same_mod36"]]


def measured_lane_map() -> dict[str, dict[str, object]]:
    """Return measured survivor rows keyed by lane."""
    return {
        str(row["factor_mod180_lane"]): row
        for row in measured_surviving_rows()
    }


def obstruction_for_lane(
    lane: dict[str, object],
    coordinates: dict[str, object],
    measured_map: dict[str, dict[str, object]],
) -> dict[str, object]:
    """Return finite candidate obstruction data for one lane."""
    lane_value = str(lane["lane"])
    orientation = str(lane["orientation"])
    equation = SIGNATURE_EQUATIONS[orientation]
    candidate_survives = int(coordinates["a_mod6"]) == int(
        equation["required_a_mod6"],
    )
    measured_survives = lane_value in measured_map
    if candidate_survives:
        obstruction = "survives_candidate_signature_phase_equation"
    else:
        obstruction = (
            f"{orientation} selector requires a=1 mod 6; "
            f"lane has a={coordinates['a_mod6']} mod 6"
        )
    return {
        **lane,
        "rule_id": RULE_ID,
        **coordinates,
        "candidate_matching_signature": equation["signature"],
        "candidate_required_a_mod6": equation["required_a_mod6"],
        "candidate_survives": candidate_survives,
        "measured_survives_round7": measured_survives,
        "candidate_matches_measured": candidate_survives == measured_survives,
        "candidate_obstruction": obstruction,
        "orientation_incompatible_signature": (
            "odd|early|o6|odd"
            if orientation == "13|19"
            else "even|mid|o4|odd"
        ),
    }


def finite_lane_obstruction_table() -> list[dict[str, object]]:
    """Return all 12 candidate obstruction rows."""
    measured_map = measured_lane_map()
    return [
        obstruction_for_lane(lane, lane_coordinates(lane), measured_map)
        for lane in theoretical_same_phase_lanes()
    ]


def terminal_image_table() -> list[dict[str, object]]:
    """Return measured terminal image rows for the two survivors."""
    rows = []
    for row in measured_surviving_rows():
        lane = str(row["factor_mod180_lane"])
        if lane not in EXPECTED_LANES:
            raise ValueError(f"unexpected measured survivor: {lane}")
        rows.append(
            {
                "rule_id": RULE_ID,
                "lane": lane,
                "signature": row["signature"],
                "phase_width_pair": row["phase_width_pair"],
                "phase_width_complement": row["phase_width_complement"],
                "lower_predecessor_pair": row[
                    "lower_predecessor_residue_width_pair"
                ],
                "strict_interior_open_slot_count": row[
                    "lower_predecessor_open_slot_count"
                ],
                "terminal_closure": row["lower_terminal_closure"],
                "lower_terminal_four_slot": row["lower_terminal_four_slot"],
            }
        )
    rows.sort(key=lambda item: str(item["lane"]))
    return rows


def public_signature_phase_equation() -> dict[str, object]:
    """Return the candidate finite public signature equation."""
    return {
        "rule_id": RULE_ID,
        "status": "candidate_finite_state_equation_not_proved",
        "equations": [
            {
                "public_signature": "even|mid|o4|odd",
                "orientation": "13|19",
                "required_a_mod6": 1,
                "surviving_lane": "43|79",
            },
            {
                "public_signature": "odd|early|o6|odd",
                "orientation": "19|13",
                "required_a_mod6": 1,
                "surviving_lane": "49|13",
            },
        ],
        "interpretation": (
            "The measured public signature chooses the factor-core orientation "
            "and fixes the p-lift coordinate a to 1 mod 6."
        ),
        "theorem_status": "hypothesis_not_proved",
    }


def proof_obligations() -> dict[str, object]:
    """Return remaining proof obligations."""
    return {
        "rule_id": RULE_ID,
        "proof_status": "incomplete",
        "obligations": [
            {
                "name": "same-phase lane table",
                "status": "finite_algebra_table_emitted",
                "claim": "same_mod36 expands the two factor-core orientations into exactly 12 ordered mod-180 lanes.",
            },
            {
                "name": "public signature phase equation",
                "status": "unproved_main_obligation",
                "claim": "DirectedPublicReentry2OddExit forces the matching orientation and a=1 mod 6.",
            },
            {
                "name": "terminal image",
                "status": "measured_on_selected_lanes",
                "claim": "The selected lanes land in lower predecessor pairs 19|22 and 29|18 with four slots.",
            },
        ],
    }


def summary() -> dict[str, object]:
    """Return Grok Round 8 summary."""
    table = finite_lane_obstruction_table()
    terminal_rows = terminal_image_table()
    candidate_survivors = [row for row in table if row["candidate_survives"]]
    candidate_excluded = [row for row in table if not row["candidate_survives"]]
    measured_survivors = [row for row in table if row["measured_survives_round7"]]
    measured_excluded = [row for row in table if not row["measured_survives_round7"]]
    return {
        "rule_id": RULE_ID,
        "theoretical_same_phase_lane_count": len(table),
        "candidate_signature_equation_count": len(SIGNATURE_EQUATIONS),
        "candidate_survivor_count": len(candidate_survivors),
        "candidate_excluded_count": len(candidate_excluded),
        "measured_survivor_count": len(measured_survivors),
        "measured_excluded_count": len(measured_excluded),
        "candidate_matches_measured_round7_image": all(
            row["candidate_matches_measured"] for row in table
        ),
        "candidate_surviving_lanes": sorted(str(row["lane"]) for row in candidate_survivors),
        "candidate_excluded_lanes": sorted(str(row["lane"]) for row in candidate_excluded),
        "terminal_image_four_slot_count_clean": all(
            row["lower_terminal_four_slot"]
            and row["strict_interior_open_slot_count"] == 4
            for row in terminal_rows
        ),
        "universal_proof_complete": False,
        "theorem_status": "hypothesis_not_proved",
        "next_required_proof_object": (
            "prove that the public odd-exit reentry grammar enforces the "
            "orientation plus a=1 mod 6 signature-phase equation universally"
        ),
    }


def main() -> int:
    """Run the Grok Round 8 obstruction workbench."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    write_jsonl(
        OUTPUT_DIR / "finite_lane_obstruction_table.jsonl",
        finite_lane_obstruction_table(),
    )
    write_json(
        OUTPUT_DIR / "public_signature_phase_equation.json",
        public_signature_phase_equation(),
    )
    write_jsonl(
        OUTPUT_DIR / "terminal_image_table.jsonl",
        terminal_image_table(),
    )
    write_json(OUTPUT_DIR / "proof_obligations.json", proof_obligations())
    payload = summary()
    write_json(OUTPUT_DIR / "summary.json", payload)
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
