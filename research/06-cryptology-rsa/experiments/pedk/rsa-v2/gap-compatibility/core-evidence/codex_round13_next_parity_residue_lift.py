#!/usr/bin/env python3
"""Round 13 residue-lift equation for the lane 163|19 next-parity obstruction."""

from __future__ import annotations

import json
from pathlib import Path

from first_gap_compatibility_check import write_json, write_jsonl
from slot_factor_public_quotient_test import read_jsonl


THIS_DIR = Path(__file__).resolve().parent
ROUND12_OUTPUT_DIR = THIS_DIR / "output" / "codex_round12_next_parity_obstruction"
OUTPUT_DIR = THIS_DIR / "output" / "codex_round13_next_parity_residue_lift"
RULE_ID = "pedk_codex_round13_next_parity_residue_lift_v1"
TARGET_LANE = "163|19"


def load_micro_rows() -> list[dict[str, object]]:
    """Return Round 12 prior-surface micro rows."""
    return read_jsonl(ROUND12_OUTPUT_DIR / "next_parity_micro_state_rows.jsonl")


def parity_name(value_mod2: int) -> str:
    """Return the parity label for one value mod 2."""
    return "even" if value_mod2 == 0 else "odd"


def next_parity_definition() -> dict[str, object]:
    """Return the source-level definition of next parity."""
    return {
        "rule_id": RULE_ID,
        "definition_status": "source_defined",
        "source_file": (
            "research/06-cryptology-rsa/experiments/modulus-recursive-catalogs/"
            "rsa-v2/modulus_gap_grammar_probe.py"
        ),
        "definition": (
            "For a non-empty gap, gap_grammar selects the first minimum "
            "divisor-count interior value. The exact_type_key suffix is the "
            "carrier_family of that winner_value. For d=4 winners, "
            "carrier_family is d4_even when winner_value % 2 == 0 and "
            "d4_odd when winner_value % 2 == 1."
        ),
        "next_parity_equation": (
            "next_parity = parity(following_left_endpoint + next_winner_offset)"
        ),
    }


def residue_lift_rows() -> list[dict[str, object]]:
    """Return one residue-lift row per Round 12 prior-surface state."""
    rows = []
    for row in load_micro_rows():
        following_left_mod180 = int(row["public_containing_right_mod180"])
        winner_offset = int(row["next_winner_offset"])
        winner_value_mod2 = (following_left_mod180 + winner_offset) % 2
        rows.append(
            {
                "rule_id": RULE_ID,
                "case_id": row["case_id"],
                "lane": row["lane"],
                "p_mod180": row["p_mod180"],
                "q_mod180": row["q_mod180"],
                "n_mod180": row["n_mod180"],
                "public_containing_left_mod180": row["public_containing_left_mod180"],
                "public_containing_right_mod180": following_left_mod180,
                "public_following_exact_type_key": row[
                    "public_following_exact_type_key"
                ],
                "next_winner_offset": winner_offset,
                "next_winner_offset_mod2": winner_offset % 2,
                "winner_value_mod2_by_lift": winner_value_mod2,
                "next_parity_by_lift": parity_name(winner_value_mod2),
                "next_parity_observed": row["next_parity"],
                "residue_lift_matches_observed_parity": (
                    parity_name(winner_value_mod2) == row["next_parity"]
                ),
            }
        )
    return rows


def symbolic_parity_table() -> list[dict[str, object]]:
    """Return the finite parity table over the two offset parities."""
    following_left_mod180 = int(load_micro_rows()[0]["public_containing_right_mod180"])
    rows = []
    for offset_mod2 in (0, 1):
        winner_value_mod2 = (following_left_mod180 + offset_mod2) % 2
        rows.append(
            {
                "rule_id": RULE_ID,
                "target_lane": TARGET_LANE,
                "following_left_mod180": following_left_mod180,
                "following_left_mod2": following_left_mod180 % 2,
                "next_winner_offset_mod2": offset_mod2,
                "winner_value_mod2": winner_value_mod2,
                "next_parity": parity_name(winner_value_mod2),
                "status_under_round12_surface": (
                    "measured_admissible_offset_class"
                    if offset_mod2 == 1
                    else "falsifier_offset_class_if_admissible"
                ),
            }
        )
    return rows


def falsifier_contract() -> dict[str, object]:
    """Return the falsifier contract for the component law."""
    return {
        "rule_id": RULE_ID,
        "component_law": "next_parity_odd",
        "target_lane": TARGET_LANE,
        "falsifier_contract": (
            "Any valid row on the 163|19 prior surface with "
            "next_winner_offset even, equivalently next_parity=odd, "
            "invalidates this component law."
        ),
        "current_measured_falsifier_count": 0,
        "universal_falsifier_status": "not_proved_absent",
    }


def composition_statement() -> dict[str, object]:
    """Return the local composition statement."""
    return {
        "rule_id": RULE_ID,
        "component_law": "next_parity_odd",
        "local_chain": [
            "S_163 fixes public_containing_right_mod180=43 on the measured prior surface",
            "Round 12 reduces S_163 to following exact state o4_d4_a3_d4_even",
            "a3 gives next_winner_offset=3, so 43 + 3 is even",
            "next_parity=even",
            "DirectedPublicReentry2OddExit requires next_parity=odd",
            "lane 163|19 is excluded by the odd-exit predicate",
        ],
        "composition_status": "measured_local_reduction",
        "universal_proof_complete": False,
    }


def summary() -> dict[str, object]:
    """Return Round 13 summary."""
    lift_rows = residue_lift_rows()
    symbolic = symbolic_parity_table()
    measured_even = [
        row for row in lift_rows if row["next_parity_by_lift"] == "even"
    ]
    measured_odd = [
        row for row in lift_rows if row["next_parity_by_lift"] == "odd"
    ]
    return {
        "rule_id": RULE_ID,
        "status": "measured_next_parity_residue_lift",
        "component_law": "next_parity_odd",
        "target_lane": TARGET_LANE,
        "theorem_status": "hypothesis_not_proved",
        "prior_surface_row_count": len(lift_rows),
        "residue_lift_matches_observed_parity": all(
            row["residue_lift_matches_observed_parity"] for row in lift_rows
        ),
        "measured_even_lift_count": len(measured_even),
        "measured_odd_lift_count": len(measured_odd),
        "following_left_mod180_values": sorted(
            {int(row["public_containing_right_mod180"]) for row in lift_rows}
        ),
        "measured_next_winner_offset_values": sorted(
            {int(row["next_winner_offset"]) for row in lift_rows}
        ),
        "candidate_local_equation": (
            "next_parity = parity(public_containing_right + next_winner_offset)"
        ),
        "remaining_universal_atom": (
            "prove S_163 -> next_winner_offset is odd, measured here as a3"
        ),
        "falsifier_offset_classes": [
            row for row in symbolic if row["next_parity"] == "odd"
        ],
        "universal_proof_complete": False,
        "distance_to_final_solution": (
            "the first component law has descended to a parity equation; "
            "touchdown still requires proving the odd offset class universally"
        ),
    }


def main() -> int:
    """Run the Round 13 residue-lift builder."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    write_json(OUTPUT_DIR / "next_parity_definition.json", next_parity_definition())
    write_jsonl(OUTPUT_DIR / "residue_lift_table.jsonl", residue_lift_rows())
    write_jsonl(OUTPUT_DIR / "symbolic_parity_table.jsonl", symbolic_parity_table())
    write_json(OUTPUT_DIR / "falsifier_contract.json", falsifier_contract())
    write_json(OUTPUT_DIR / "composition_statement.json", composition_statement())
    payload = summary()
    write_json(OUTPUT_DIR / "summary.json", payload)
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
