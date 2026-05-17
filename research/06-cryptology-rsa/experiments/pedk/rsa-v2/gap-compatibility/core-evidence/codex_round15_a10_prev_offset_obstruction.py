#!/usr/bin/env python3
"""Round 15 a10 previous-offset obstruction for lane 163|19."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Callable

from codex_round2_public_trigger_separator import corpus_row_index
from codex_round5_same_phase_boundary_probe import annotated_rows
from first_gap_compatibility_check import write_json, write_jsonl


THIS_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = THIS_DIR / "output" / "codex_round15_a10_prev_offset_obstruction"
RULE_ID = "pedk_codex_round15_a10_prev_offset_obstruction_v1"
TARGET_LANE = "163|19"
TARGET_TUPLE = ("even", "mid", "o4")
TARGET_FOLLOWING_LEFT_MOD180 = 43
EVEN_CANDIDATE_OFFSET = 10

StagePredicate = Callable[[dict[str, object]], bool]


def directed_tuple(row: dict[str, object]) -> tuple[str, str, str]:
    """Return the directed public tuple for one annotated row."""
    return (
        str(row["prev_parity"]),
        str(row["containing_position"]),
        str(row["next_open_type"]),
    )


def s163_stage_predicates() -> list[tuple[str, StagePredicate]]:
    """Return the exact prior-surface ladder for the 163|19 component law."""
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


def first_failed_s163_stage(row: dict[str, object]) -> str:
    """Return the first S_163 stage failed by one row."""
    for stage, predicate in s163_stage_predicates():
        if not predicate(row):
            return stage
    return "survives_s163_prior_surface"


def parity_name(value_mod2: int) -> str:
    """Return the parity label for one value mod 2."""
    return "even" if value_mod2 == 0 else "odd"


def enriched_public_state(
    row: dict[str, object],
    row_index: dict[tuple[str, str], dict[str, object]],
) -> dict[str, object]:
    """Return public previous, containing, and following gap state for one row."""
    enriched = row_index[(str(row["window"]), str(row["case_id"]))]
    n_value = int(enriched["N"])
    containing_left = n_value - int(enriched["public_n_offset_from_left"])
    containing_right = n_value + int(enriched["public_n_offset_from_right"])
    previous_gap = enriched["public_previous_gap"]
    containing_gap = enriched["public_containing_gap"]
    following_gap = enriched["public_following_gap"]
    next_winner_offset = int(following_gap["winner_offset"])
    next_winner_value = containing_right + next_winner_offset
    return {
        "public_containing_left_mod180": containing_left % 180,
        "public_containing_right_mod180": containing_right % 180,
        "public_previous_exact_type_key": str(previous_gap["exact_type_key"]),
        "public_previous_first_open_offset": int(previous_gap["first_open_offset"]),
        "public_previous_winner_offset": int(previous_gap["winner_offset"]),
        "public_previous_gap_width": int(previous_gap["gap_width"]),
        "public_containing_exact_type_key": str(containing_gap["exact_type_key"]),
        "public_containing_winner_offset": int(containing_gap["winner_offset"]),
        "public_following_exact_type_key": str(following_gap["exact_type_key"]),
        "public_following_first_open_offset": int(following_gap["first_open_offset"]),
        "public_following_gap_width": int(following_gap["gap_width"]),
        "next_winner_offset": next_winner_offset,
        "next_winner_offset_mod2": next_winner_offset % 2,
        "next_winner_value_mod2_by_lift": next_winner_value % 2,
        "next_parity_by_lift": parity_name(next_winner_value % 2),
    }


def compact_row(
    row: dict[str, object],
    row_index: dict[tuple[str, str], dict[str, object]],
    domain: str,
) -> dict[str, object]:
    """Return one compact public grammar row for the obstruction table."""
    return {
        "rule_id": RULE_ID,
        "domain": domain,
        "window": row["window"],
        "case_id": row["case_id"],
        "lane": row["factor_mod180_lane"],
        "signature": row["signature"],
        "public_key": row["public_key"],
        "p_mod180": row["p_mod180"],
        "q_mod180": row["q_mod180"],
        "p_mod36": row["p_mod36"],
        "q_mod36": row["q_mod36"],
        "same_mod36": row["same_mod36"],
        "right_boundary_residues": row["right_boundary_residues"],
        "public_gwr_side": row["public_gwr_side"],
        "prev_open_offset": int(row["prev_open_offset"]),
        "prev_d": int(row["prev_d"]),
        "prev_parity": row["prev_parity"],
        "containing_position": row["containing_position"],
        "next_open_type": row["next_open_type"],
        "next_d": int(row["next_d"]),
        "next_parity_observed": row["next_parity"],
        "directed_tuple": "|".join(directed_tuple(row)),
        "first_failed_s163_stage": first_failed_s163_stage(row),
        **enriched_public_state(row, row_index),
    }


def relaxed_prior_grammar_rows(
    rows: list[dict[str, object]],
    row_index: dict[tuple[str, str], dict[str, object]],
) -> list[dict[str, object]]:
    """Return the relaxed lane-163|19 prior grammar from Round 14."""
    out = []
    for row in rows:
        state = enriched_public_state(row, row_index)
        if not row["same_mod36"]:
            continue
        if row["factor_mod180_lane"] != TARGET_LANE:
            continue
        if not row["rres_o4_o4"]:
            continue
        if row["public_gwr_side"] != "at_winner":
            continue
        if int(row["prev_d"]) > 4:
            continue
        if state["public_containing_right_mod180"] != TARGET_FOLLOWING_LEFT_MOD180:
            continue
        if row["next_open_type"] != "o4":
            continue
        if int(row["next_d"]) > 4:
            continue
        out.append(compact_row(row, row_index, "relaxed_lane_163_19_prior_grammar"))
    out.sort(
        key=lambda item: (
            int(item["next_winner_offset"]),
            int(item["prev_open_offset"]),
            str(item["window"]),
            str(item["case_id"]),
        )
    )
    return out


def a10_obstruction_rows(relaxed_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    """Return every measured a10 row with the previous-offset obstruction."""
    out = []
    for row in relaxed_rows:
        if int(row["next_winner_offset"]) != EVEN_CANDIDATE_OFFSET:
            continue
        prev_open_offset = int(row["prev_open_offset"])
        out.append(
            {
                "rule_id": RULE_ID,
                "law_id": "a10_prev_open_offset_obstruction",
                "lane": TARGET_LANE,
                "window": row["window"],
                "case_id": row["case_id"],
                "next_winner_offset": row["next_winner_offset"],
                "next_winner_offset_mod2": row["next_winner_offset_mod2"],
                "prev_open_offset": prev_open_offset,
                "prev_open_offset_required_by_s163": 4,
                "prev_open_offset_4": prev_open_offset == 4,
                "first_failed_s163_stage": row["first_failed_s163_stage"],
                "public_previous_exact_type_key": row["public_previous_exact_type_key"],
                "public_following_exact_type_key": row[
                    "public_following_exact_type_key"
                ],
                "signature": row["signature"],
                "obstruction_status": (
                    "a10_blocked_at_prev_open_offset_4"
                    if prev_open_offset != 4
                    else "a10_survives_prev_open_offset_4_falsifier"
                ),
            }
        )
    return out


def offset_pair_table(relaxed_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    """Return the measured offset-to-entry map for the relaxed domain."""
    return [
        {
            "rule_id": RULE_ID,
            "lane": row["lane"],
            "window": row["window"],
            "case_id": row["case_id"],
            "next_winner_offset": row["next_winner_offset"],
            "next_winner_offset_mod2": row["next_winner_offset_mod2"],
            "prev_open_offset": row["prev_open_offset"],
            "prev_parity": row["prev_parity"],
            "signature": row["signature"],
            "public_previous_exact_type_key": row["public_previous_exact_type_key"],
            "public_following_exact_type_key": row["public_following_exact_type_key"],
            "first_failed_s163_stage": row["first_failed_s163_stage"],
            "s163_survival_status": (
                "survives_s163_prior_surface"
                if row["first_failed_s163_stage"] == "survives_s163_prior_surface"
                else "blocked_before_s163"
            ),
        }
        for row in relaxed_rows
    ]


def falsifier_contract() -> dict[str, object]:
    """Return the falsifier contract for the a10 obstruction."""
    return {
        "rule_id": RULE_ID,
        "component_law": "next_parity_odd",
        "target_lane": TARGET_LANE,
        "local_atom": "a10 -> not(prev_open_offset_4)",
        "falsifier_contract": (
            "Any valid relaxed lane-163|19 row with next_winner_offset=10 "
            "and prev_open_offset=4 invalidates the a10 previous-offset "
            "obstruction. Any valid S_163 row with an even next_winner_offset "
            "invalidates the parent odd-offset law."
        ),
        "current_measured_falsifier_count": 0,
        "universal_falsifier_status": "not_proved_absent",
    }


def composition_statement() -> dict[str, object]:
    """Return the Round 15 composition statement."""
    return {
        "rule_id": RULE_ID,
        "component_law": "next_parity_odd",
        "target_lane": TARGET_LANE,
        "local_chain": [
            "Relaxed lane-163|19 prior grammar has measured next-offset domain {a3, a10}",
            "a10 is the only measured even next-offset candidate",
            "a10 carries prev_open_offset=2",
            "S_163 requires prev_open_offset=4",
            "a10 cannot reach S_163 on the measured surface",
            "therefore the measured S_163 surface retains only odd offset a3",
            "a3 with following-left residue 43 gives next_parity=even",
            "lane 163|19 fails DirectedPublicReentry2OddExit",
        ],
        "composition_status": "measured_a10_prev_offset_obstruction",
        "universal_proof_complete": False,
    }


def short_transcript() -> list[dict[str, str]]:
    """Return the requested flight-deck communication transcript."""
    return [
        {
            "speaker": "ATC",
            "line": "Round 15 cleared. Hold premises fixed and identify why a10 misses S_163.",
        },
        {
            "speaker": "Pilot",
            "line": "Copy. We are tracking lane 163|19, same phase, Rres=o4|o4, at_winner.",
        },
        {
            "speaker": "Co-pilot",
            "line": "Grok confirms relaxed offset domain: a3 on glide path, a10 off the entry gate.",
        },
        {
            "speaker": "First Officer",
            "line": "ChatGPT calls the next obstruction: a10 implies prev_open_offset is not 4.",
        },
        {
            "speaker": "Pilot",
            "line": "Measured a10 carries prev_open_offset=2. It cannot cross the S_163 threshold.",
        },
        {
            "speaker": "ATC",
            "line": "Continue approach. Universal proof still required before touchdown.",
        },
    ]


def summary(
    relaxed_rows: list[dict[str, object]],
    a10_rows: list[dict[str, object]],
) -> dict[str, object]:
    """Return the Round 15 summary."""
    offset_values = sorted({int(row["next_winner_offset"]) for row in relaxed_rows})
    even_rows = [
        row for row in relaxed_rows if int(row["next_winner_offset_mod2"]) == 0
    ]
    a10_falsifiers = [row for row in a10_rows if row["prev_open_offset_4"]]
    prev_offset_by_next_offset: dict[str, dict[str, int]] = {}
    for row in relaxed_rows:
        key = f"a{row['next_winner_offset']}"
        prev_offset_by_next_offset.setdefault(key, {})
        prev_key = f"o{row['prev_open_offset']}"
        prev_offset_by_next_offset[key][prev_key] = (
            prev_offset_by_next_offset[key].get(prev_key, 0) + 1
        )
    first_fail_counts = Counter(
        str(row["first_failed_s163_stage"]) for row in even_rows
    )
    return {
        "rule_id": RULE_ID,
        "status": "measured_a10_prev_offset_obstruction",
        "component_law": "next_parity_odd",
        "target_lane": TARGET_LANE,
        "theorem_status": "hypothesis_not_proved",
        "relaxed_prior_grammar_row_count": len(relaxed_rows),
        "relaxed_next_winner_offset_values": offset_values,
        "relaxed_even_offset_values": sorted(
            {int(row["next_winner_offset"]) for row in even_rows}
        ),
        "a10_row_count": len(a10_rows),
        "a10_prev_open_offset_values": sorted(
            {int(row["prev_open_offset"]) for row in a10_rows}
        ),
        "a10_prev_open_offset_4_count": len(a10_falsifiers),
        "a10_first_failed_s163_stage_counts": dict(sorted(first_fail_counts.items())),
        "prev_offset_by_next_offset": prev_offset_by_next_offset,
        "measured_law": "a10 -> prev_open_offset=2, hence not prev_open_offset=4",
        "remaining_universal_atom": (
            "prove a10 -> not(prev_open_offset_4) under the relaxed lane-163|19 prior grammar"
        ),
        "universal_proof_complete": False,
        "distance_to_final_solution": (
            "the first component law is seconds above the runway: a10 is now "
            "isolated as the only measured even offset and it misses the "
            "S_163 entry gate at prev_open_offset_4; touchdown still needs "
            "the universal grammar law behind that miss"
        ),
        "next_required_proof_object": (
            "prove the a10 previous-offset obstruction universally, then "
            "compose it into S_163 -> next_winner_offset odd"
        ),
    }


def main() -> int:
    """Run the Round 15 a10 previous-offset obstruction builder."""
    row_index = corpus_row_index()
    rows = annotated_rows()
    relaxed_rows = relaxed_prior_grammar_rows(rows, row_index)
    a10_rows = a10_obstruction_rows(relaxed_rows)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    write_jsonl(OUTPUT_DIR / "relaxed_prior_grammar_rows.jsonl", relaxed_rows)
    write_jsonl(OUTPUT_DIR / "offset_pair_table.jsonl", offset_pair_table(relaxed_rows))
    write_jsonl(OUTPUT_DIR / "a10_obstruction_table.jsonl", a10_rows)
    write_json(OUTPUT_DIR / "falsifier_contract.json", falsifier_contract())
    write_json(OUTPUT_DIR / "composition_statement.json", composition_statement())
    write_jsonl(OUTPUT_DIR / "flight_transcript.jsonl", short_transcript())
    payload = summary(relaxed_rows, a10_rows)
    write_json(OUTPUT_DIR / "summary.json", payload)
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
