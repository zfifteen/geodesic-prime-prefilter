#!/usr/bin/env python3
"""Round 16 width-residue reduction for the a10 previous-offset obstruction."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

from codex_round2_public_trigger_separator import corpus_row_index
from codex_round15_a10_prev_offset_obstruction import (
    EVEN_CANDIDATE_OFFSET,
    TARGET_LANE,
    relaxed_prior_grammar_rows,
)
from codex_round5_same_phase_boundary_probe import annotated_rows
from first_gap_compatibility_check import write_json, write_jsonl
from modulus_gap_grammar_probe import first_open_offset


THIS_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = THIS_DIR / "output" / "codex_round16_a10_width_residue_law"
RULE_ID = "pedk_codex_round16_a10_width_residue_law_v1"


def relaxed_rows() -> list[dict[str, object]]:
    """Return the Round 15 relaxed lane-163|19 prior grammar rows."""
    return relaxed_prior_grammar_rows(annotated_rows(), corpus_row_index())


def width_residue_row(row: dict[str, object]) -> dict[str, object]:
    """Return the previous-gap width and residue mechanism for one row."""
    containing_left_mod30 = int(row["public_containing_left_mod180"]) % 30
    previous_gap_width = int(row["public_previous_gap_width"])
    previous_left_mod30 = (containing_left_mod30 - previous_gap_width) % 30
    computed_prev_open_offset = first_open_offset(previous_left_mod30)
    return {
        "rule_id": RULE_ID,
        "lane": row["lane"],
        "window": row["window"],
        "case_id": row["case_id"],
        "next_winner_offset": row["next_winner_offset"],
        "next_winner_offset_mod2": row["next_winner_offset_mod2"],
        "public_containing_left_mod180": row["public_containing_left_mod180"],
        "public_containing_left_mod30": containing_left_mod30,
        "public_previous_gap_width": previous_gap_width,
        "public_previous_gap_width_mod30": previous_gap_width % 30,
        "previous_left_mod30_by_width": previous_left_mod30,
        "computed_prev_open_offset": computed_prev_open_offset,
        "observed_prev_open_offset": row["prev_open_offset"],
        "computed_matches_observed": computed_prev_open_offset == row["prev_open_offset"],
        "public_previous_exact_type_key": row["public_previous_exact_type_key"],
        "public_following_exact_type_key": row["public_following_exact_type_key"],
        "first_failed_s163_stage": row["first_failed_s163_stage"],
        "s163_survival_status": (
            "survives_s163_prior_surface"
            if row["first_failed_s163_stage"] == "survives_s163_prior_surface"
            else "blocked_before_s163"
        ),
    }


def width_residue_table(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    """Return width-residue rows for the full relaxed domain."""
    return [width_residue_row(row) for row in rows]


def first_open_residue_table() -> list[dict[str, object]]:
    """Return the mod-30 first-open map used by the a10 obstruction."""
    residues = sorted({17, 19})
    return [
        {
            "rule_id": RULE_ID,
            "previous_left_mod30": residue,
            "first_open_offset": first_open_offset(residue),
            "open_residue": (residue + first_open_offset(residue)) % 30,
        }
        for residue in residues
    ]


def a10_width_residue_obstruction(
    rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    """Return the measured a10 width-residue obstruction rows."""
    out = []
    for row in rows:
        if int(row["next_winner_offset"]) != EVEN_CANDIDATE_OFFSET:
            continue
        previous_gap_width = int(row["public_previous_gap_width"])
        previous_left_mod30 = int(row["previous_left_mod30_by_width"])
        computed_prev_open_offset = int(row["computed_prev_open_offset"])
        out.append(
            {
                "rule_id": RULE_ID,
                "law_id": "a10_width_residue_prev_open_obstruction",
                "lane": TARGET_LANE,
                "window": row["window"],
                "case_id": row["case_id"],
                "next_winner_offset": row["next_winner_offset"],
                "public_containing_left_mod30": row["public_containing_left_mod30"],
                "public_previous_gap_width": previous_gap_width,
                "previous_left_mod30_by_width": previous_left_mod30,
                "computed_prev_open_offset": computed_prev_open_offset,
                "observed_prev_open_offset": row["observed_prev_open_offset"],
                "prev_open_offset_4": computed_prev_open_offset == 4,
                "obstruction_chain": (
                    "a10 -> previous_gap_width=14 -> previous_left_mod30=17 "
                    "-> first_open_offset=2"
                ),
                "obstruction_status": (
                    "a10_width_residue_blocks_prev_open_offset_4"
                    if computed_prev_open_offset != 4
                    else "a10_width_residue_falsifier"
                ),
            }
        )
    return out


def falsifier_contract() -> dict[str, object]:
    """Return the falsifier contract for the width-residue reduction."""
    return {
        "rule_id": RULE_ID,
        "component_law": "next_parity_odd",
        "target_lane": TARGET_LANE,
        "local_atom": "a10 -> previous_gap_width=14",
        "falsifier_contract": (
            "Any valid relaxed lane-163|19 row with next_winner_offset=10 "
            "and a previous-gap width whose computed first_open_offset is 4 "
            "invalidates this width-residue obstruction. Equivalently, an "
            "a10 row with prev_open_offset=4 invalidates the parent a10 "
            "previous-offset law."
        ),
        "current_measured_falsifier_count": 0,
        "universal_falsifier_status": "not_proved_absent",
    }


def composition_statement() -> dict[str, object]:
    """Return the Round 16 composition statement."""
    return {
        "rule_id": RULE_ID,
        "component_law": "next_parity_odd",
        "target_lane": TARGET_LANE,
        "local_chain": [
            "Relaxed lane-163|19 prior grammar has measured next-offset domain {a3, a10}",
            "a10 is the only measured even next-offset candidate",
            "a10 carries public_previous_gap_width=14",
            "public_containing_left_mod30=1, so previous_left_mod30=(1-14) mod 30=17",
            "first_open_offset(17)=2",
            "S_163 requires prev_open_offset=4",
            "a10 cannot reach S_163 on the measured surface",
            "remaining universal atom: prove a10 -> public_previous_gap_width=14",
        ],
        "composition_status": "measured_width_residue_reduction",
        "universal_proof_complete": False,
    }


def flight_transcript() -> list[dict[str, str]]:
    """Return the tightened flight crew transcript for Round 16."""
    return [
        {
            "speaker": "ATC",
            "line": "Round 16 cleared. No broad selector work. Derive why a10 carries o2.",
        },
        {
            "speaker": "Pilot",
            "line": "Copy. We are below decision altitude on the first component law, holding premises fixed.",
        },
        {
            "speaker": "First Officer",
            "line": "Definition check: prev_open_offset is first_open_offset(previous_left_endpoint).",
        },
        {
            "speaker": "Co-pilot",
            "line": "Width-residue table reads a10 -> previous_gap_width 14 -> previous_left_mod30 17.",
        },
        {
            "speaker": "Pilot",
            "line": "And first_open_offset(17)=2. a10 cannot enter the o4 gate.",
        },
        {
            "speaker": "ATC",
            "line": "Continue. Touchdown requires proving a10 forces width 14 universally.",
        },
    ]


def crew_protocol() -> dict[str, object]:
    """Return the tightened flight crew communication protocol."""
    return {
        "rule_id": RULE_ID,
        "protocol": "landing_phase_crew_comms",
        "flight_phase": "final_approach",
        "instructions": [
            "Use clean, round-scoped prompts for co-pilot checks.",
            "Do not let stale Grok sessions edit tracked artifacts during landing-phase proof work.",
            "Treat ChatGPT as First Officer: promote only accepted proof targets into the next round.",
            "Treat the user as ATC: preserve premise locks and report theorem status plainly.",
            "Every round must include a falsifier contract, theorem status, and distance-to-touchdown statement.",
        ],
    }


def summary(rows: list[dict[str, object]], a10_rows: list[dict[str, object]]) -> dict[str, object]:
    """Return the Round 16 summary."""
    by_offset: dict[str, dict[str, int]] = {}
    for row in rows:
        offset_key = f"a{row['next_winner_offset']}"
        by_offset.setdefault(offset_key, {})
        prev_open_key = f"o{row['computed_prev_open_offset']}"
        by_offset[offset_key][prev_open_key] = by_offset[offset_key].get(prev_open_key, 0) + 1
    a10_falsifiers = [row for row in a10_rows if row["prev_open_offset_4"]]
    width_counts = Counter(
        int(row["public_previous_gap_width"]) for row in a10_rows
    )
    residue_counts = Counter(
        int(row["previous_left_mod30_by_width"]) for row in a10_rows
    )
    return {
        "rule_id": RULE_ID,
        "status": "measured_width_residue_reduction",
        "component_law": "next_parity_odd",
        "target_lane": TARGET_LANE,
        "theorem_status": "hypothesis_not_proved",
        "relaxed_prior_grammar_row_count": len(rows),
        "offset_to_computed_prev_open_offset": by_offset,
        "a10_row_count": len(a10_rows),
        "a10_previous_gap_width_counts": {
            str(key): width_counts[key] for key in sorted(width_counts)
        },
        "a10_previous_left_mod30_counts": {
            str(key): residue_counts[key] for key in sorted(residue_counts)
        },
        "a10_computed_prev_open_offset_values": sorted(
            {int(row["computed_prev_open_offset"]) for row in a10_rows}
        ),
        "a10_prev_open_offset_4_count": len(a10_falsifiers),
        "measured_law": (
            "a10 -> previous_gap_width=14 -> previous_left_mod30=17 "
            "-> first_open_offset=2"
        ),
        "remaining_universal_atom": (
            "prove a10 -> public_previous_gap_width=14 under Relaxed163"
        ),
        "universal_proof_complete": False,
        "distance_to_final_solution": (
            "we are in the landing flare: the a10 obstruction has descended "
            "from previous-open offset to a width-residue equation; touchdown "
            "requires the universal grammar law a10 -> previous_gap_width=14"
        ),
        "next_required_proof_object": (
            "derive public_previous_gap_width=14 from a10 inside Relaxed163"
        ),
    }


def main() -> int:
    """Run the Round 16 width-residue reduction."""
    rows = width_residue_table(relaxed_rows())
    a10_rows = a10_width_residue_obstruction(rows)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    write_jsonl(OUTPUT_DIR / "width_residue_table.jsonl", rows)
    write_jsonl(OUTPUT_DIR / "first_open_residue_table.jsonl", first_open_residue_table())
    write_jsonl(OUTPUT_DIR / "a10_width_residue_obstruction.jsonl", a10_rows)
    write_json(OUTPUT_DIR / "falsifier_contract.json", falsifier_contract())
    write_json(OUTPUT_DIR / "composition_statement.json", composition_statement())
    write_json(OUTPUT_DIR / "crew_protocol.json", crew_protocol())
    write_jsonl(OUTPUT_DIR / "flight_transcript.jsonl", flight_transcript())
    payload = summary(rows, a10_rows)
    write_json(OUTPUT_DIR / "summary.json", payload)
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
