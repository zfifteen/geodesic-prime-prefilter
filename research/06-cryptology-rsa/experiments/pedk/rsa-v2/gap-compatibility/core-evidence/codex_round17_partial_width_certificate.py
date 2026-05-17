#!/usr/bin/env python3
"""Round 17 finite-scope landing certificate for the a10 width obstruction."""

from __future__ import annotations

import json
from pathlib import Path

from codex_round16_a10_width_residue_law import (
    RULE_ID as ROUND16_RULE_ID,
    TARGET_LANE,
    a10_width_residue_obstruction,
    flight_transcript as round16_flight_transcript,
    relaxed_rows,
    width_residue_table,
)
from first_gap_compatibility_check import write_json, write_jsonl


THIS_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = THIS_DIR / "output" / "codex_round17_partial_width_certificate"
RULE_ID = "pedk_codex_round17_partial_width_certificate_v1"


def a10_certificate_rows() -> list[dict[str, object]]:
    """Return finite-scope a10 rows with their width-residue certificate."""
    return [
        {
            "rule_id": RULE_ID,
            "source_rule_id": ROUND16_RULE_ID,
            "lane": row["lane"],
            "window": row["window"],
            "case_id": row["case_id"],
            "next_winner_offset": row["next_winner_offset"],
            "public_containing_left_mod30": row["public_containing_left_mod30"],
            "public_previous_gap_width": row["public_previous_gap_width"],
            "previous_left_mod30_by_width": row["previous_left_mod30_by_width"],
            "computed_prev_open_offset": row["computed_prev_open_offset"],
            "observed_prev_open_offset": row["observed_prev_open_offset"],
            "prev_open_offset_4": row["prev_open_offset_4"],
            "certificate_chain": [
                "finite Relaxed163/a10 row has public_previous_gap_width=14",
                "public_containing_left_mod30=1",
                "previous_left_mod30=(1-14) mod 30=17",
                "first_open_offset(17)=2",
                "S_163 requires prev_open_offset=4",
                "a10 is excluded from S_163 in this finite scope",
            ],
            "certificate_status": (
                "finite_scope_landed"
                if not row["prev_open_offset_4"]
                else "finite_scope_falsified"
            ),
        }
        for row in a10_width_residue_obstruction(width_residue_table(relaxed_rows()))
    ]


def finite_scope_contract(rows: list[dict[str, object]]) -> dict[str, object]:
    """Return the exact finite domain of the partial certificate."""
    return {
        "rule_id": RULE_ID,
        "proof_scope": "finite_current_relaxed163_a10_surface",
        "scope_definition": [
            "same_mod36",
            "factor_mod180_lane=163|19",
            "Rres=o4|o4",
            "public_gwr_side=at_winner",
            "prev_d<=4",
            "public_containing_right_mod180=43",
            "next_open_type=o4",
            "next_d<=4",
            "next_winner_offset=10",
        ],
        "scope_row_count": len(rows),
        "scope_width_values": sorted(
            {int(row["public_previous_gap_width"]) for row in rows}
        ),
        "scope_prev_open_values": sorted(
            {int(row["computed_prev_open_offset"]) for row in rows}
        ),
        "scope_complete_for_current_corpus": True,
        "scope_status": "partial_proof_scope_not_universal_theorem",
    }


def partial_proof_certificate(rows: list[dict[str, object]]) -> dict[str, object]:
    """Return the finite-scope proof certificate."""
    falsifiers = [row for row in rows if row["prev_open_offset_4"]]
    return {
        "rule_id": RULE_ID,
        "component_law": "next_parity_odd",
        "target_lane": TARGET_LANE,
        "partial_certificate": (
            "Within the current finite Relaxed163/a10 evidence surface, every "
            "a10 row has public_previous_gap_width=14. The definition-level "
            "width-residue computation then gives previous_left_mod30=17 and "
            "first_open_offset=2, so a10 cannot satisfy the S_163 "
            "prev_open_offset=4 gate."
        ),
        "finite_scope_a10_row_count": len(rows),
        "finite_scope_a10_width_values": sorted(
            {int(row["public_previous_gap_width"]) for row in rows}
        ),
        "finite_scope_a10_prev_open_values": sorted(
            {int(row["computed_prev_open_offset"]) for row in rows}
        ),
        "finite_scope_falsifier_count": len(falsifiers),
        "partial_proof_status": (
            "finite_scope_landed" if not falsifiers else "finite_scope_falsified"
        ),
        "theorem_status": "hypothesis_not_proved",
        "universal_proof_complete": False,
    }


def composition_statement() -> dict[str, object]:
    """Return the finite-scope landing composition."""
    return {
        "rule_id": RULE_ID,
        "component_law": "next_parity_odd",
        "target_lane": TARGET_LANE,
        "composition_scope": "finite_current_relaxed163_a10_surface",
        "local_chain": [
            "Round 15 isolated a10 as the only measured even offset in Relaxed163",
            "Round 16 reduced a10 -> prev_open_offset=2 to width-residue arithmetic",
            "Round 17 certifies the finite Relaxed163/a10 surface has width 14 only",
            "width 14 gives previous_left_mod30=17",
            "first_open_offset(17)=2",
            "a10 cannot satisfy S_163's prev_open_offset=4 gate",
            "S_163 retains only a3 in the current finite surface",
            "a3 plus following-left residue 43 gives next_parity=even",
            "lane 163|19 fails DirectedPublicReentry2OddExit in this partial certificate",
        ],
        "composition_status": "finite_scope_component_landing",
        "theorem_status": "hypothesis_not_proved",
        "universal_proof_complete": False,
    }


def falsifier_contract() -> dict[str, object]:
    """Return the finite and widening falsifier contracts."""
    return {
        "rule_id": RULE_ID,
        "component_law": "next_parity_odd",
        "target_lane": TARGET_LANE,
        "finite_scope_falsifier": (
            "A row inside the current Relaxed163/a10 surface with "
            "public_previous_gap_width != 14 or computed_prev_open_offset=4 "
            "invalidates this partial certificate."
        ),
        "widening_falsifier": (
            "Any later valid Relaxed163/a10 row outside the current corpus "
            "with a previous-gap width that computes first_open_offset=4 "
            "prevents upgrading this partial certificate to a universal law."
        ),
        "current_measured_falsifier_count": 0,
    }


def crew_protocol() -> dict[str, object]:
    """Return the tightened landing-phase crew protocol."""
    return {
        "rule_id": RULE_ID,
        "protocol": "landing_phase_crew_comms_v2",
        "flight_phase": "touchdown_attempt",
        "instructions": [
            "Pilot owns the active artifact and rejects stale co-pilot edits.",
            "Co-pilot communication is read-only unless a clean round-scoped write contract is issued.",
            "First Officer messages are promoted only after ATC accepts the previous round.",
            "Partial landings must declare finite scope and theorem status separately.",
            "Every cockpit summary includes ATC, Pilot, Co-pilot, and First Officer lines.",
        ],
    }


def flight_transcript() -> list[dict[str, str]]:
    """Return the Round 17 flight crew transcript."""
    return [
        {
            "speaker": "ATC",
            "line": "Universal may be too far for this landing. Partial proof is acceptable.",
        },
        {
            "speaker": "Pilot",
            "line": "Copy. Reclassifying target: finite Relaxed163/a10 landing certificate.",
        },
        {
            "speaker": "First Officer",
            "line": "Accepted chain: a10 -> width 14 -> residue 17 -> o2.",
        },
        {
            "speaker": "Co-pilot",
            "line": "Mirror instruments confirm the finite a10 surface has width 14 only.",
        },
        {
            "speaker": "Pilot",
            "line": "Partial touchdown: a10 cannot enter S_163 in the current finite surface.",
        },
        {
            "speaker": "ATC",
            "line": "Landing acknowledged. The global theorem remains open for later traffic.",
        },
    ]


def summary(rows: list[dict[str, object]]) -> dict[str, object]:
    """Return the Round 17 summary."""
    falsifiers = [row for row in rows if row["prev_open_offset_4"]]
    return {
        "rule_id": RULE_ID,
        "status": "finite_scope_component_landing",
        "component_law": "next_parity_odd",
        "target_lane": TARGET_LANE,
        "proof_scope": "finite_current_relaxed163_a10_surface",
        "partial_proof_status": (
            "finite_scope_landed" if not falsifiers else "finite_scope_falsified"
        ),
        "theorem_status": "hypothesis_not_proved",
        "universal_proof_complete": False,
        "finite_scope_a10_row_count": len(rows),
        "finite_scope_a10_width_values": sorted(
            {int(row["public_previous_gap_width"]) for row in rows}
        ),
        "finite_scope_a10_prev_open_values": sorted(
            {int(row["computed_prev_open_offset"]) for row in rows}
        ),
        "finite_scope_falsifier_count": len(falsifiers),
        "landed_chain": (
            "finite a10 -> width 14 -> previous_left_mod30 17 -> "
            "first_open_offset 2 -> not prev_open_offset 4"
        ),
        "distance_to_final_solution": (
            "this flight has landed a finite-scope first-component certificate; "
            "the aircraft is on the runway for the current evidence surface, "
            "while the global theorem remains parked as future work"
        ),
        "next_required_proof_object": (
            "decide whether to broaden the certificate surface or move to the "
            "next component law with this partial obstruction accepted"
        ),
    }


def main() -> int:
    """Run the Round 17 finite-scope landing certificate builder."""
    rows = a10_certificate_rows()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    write_jsonl(OUTPUT_DIR / "a10_certificate_rows.jsonl", rows)
    write_json(OUTPUT_DIR / "finite_scope_contract.json", finite_scope_contract(rows))
    write_json(OUTPUT_DIR / "partial_proof_certificate.json", partial_proof_certificate(rows))
    write_json(OUTPUT_DIR / "composition_statement.json", composition_statement())
    write_json(OUTPUT_DIR / "falsifier_contract.json", falsifier_contract())
    write_json(OUTPUT_DIR / "crew_protocol.json", crew_protocol())
    write_jsonl(OUTPUT_DIR / "flight_transcript.jsonl", flight_transcript())
    write_jsonl(OUTPUT_DIR / "round16_transcript_reference.jsonl", round16_flight_transcript())
    payload = summary(rows)
    write_json(OUTPUT_DIR / "summary.json", payload)
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
