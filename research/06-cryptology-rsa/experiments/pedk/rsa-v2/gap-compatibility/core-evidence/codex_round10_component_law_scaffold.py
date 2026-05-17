#!/usr/bin/env python3
"""Round 10 proof-contract scaffold for component obstruction laws."""

from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path

from first_gap_compatibility_check import write_json, write_jsonl
from slot_factor_public_quotient_test import read_jsonl


THIS_DIR = Path(__file__).resolve().parent
ROUND9_OUTPUT_DIR = THIS_DIR / "output" / "codex_round9_public_component_obstruction_audit"
OUTPUT_DIR = THIS_DIR / "output" / "codex_round10_component_law_scaffold"
RULE_ID = "pedk_codex_round10_component_law_scaffold_v1"
SURVIVOR_LANES = ["43|79", "49|13"]
STAGE_PRIORS = {
    "prev_open_offset_4": "same_phase_lane + Rres=o4|o4 + at_winner",
    "prev_d_le4": "same_phase_lane + Rres=o4|o4 + at_winner + prev_open_offset=4",
    "directed_tuple": (
        "same_phase_lane + Rres=o4|o4 + at_winner + "
        "prev_open_offset=4 + prev_d<=4"
    ),
    "next_parity_odd": (
        "same_phase_lane + Rres=o4|o4 + at_winner + "
        "prev_open_offset=4 + prev_d<=4 + allowed directed tuple + next_d<=4"
    ),
}


def load_round9_cascade() -> list[dict[str, object]]:
    """Return Round 9 lane component cascade rows."""
    return read_jsonl(ROUND9_OUTPUT_DIR / "lane_component_cascade.jsonl")


def load_round9_near_misses() -> list[dict[str, object]]:
    """Return Round 9 near-miss rows."""
    return read_jsonl(ROUND9_OUTPUT_DIR / "near_miss_rows.jsonl")


def excluded_cascades() -> list[dict[str, object]]:
    """Return excluded lane cascade rows."""
    return [
        row for row in load_round9_cascade() if not row["final_survives"]
    ]


def stage_lanes(cascades: list[dict[str, object]]) -> dict[str, list[str]]:
    """Return excluded lanes grouped by first-zero stage."""
    groups: dict[str, list[str]] = defaultdict(list)
    for row in cascades:
        groups[str(row["first_zero_stage"])].append(str(row["lane"]))
    return {
        stage: sorted(lanes)
        for stage, lanes in sorted(groups.items())
    }


def law_for_stage(stage: str, lanes: list[str]) -> dict[str, object]:
    """Return one component-law proof contract."""
    if stage == "prev_open_offset_4":
        claim = (
            "Under the prior stages, lane 19|163 never reaches "
            "prev_open_offset=4."
        )
        falsifier = (
            "A row in lane 19|163 satisfying same_phase_lane, Rres=o4|o4, "
            "at_winner, and prev_open_offset=4."
        )
    elif stage == "prev_d_le4":
        claim = (
            "Under the prior stages, lane 79|43 has no previous o4 entry "
            "with prev_d<=4."
        )
        falsifier = (
            "A row in lane 79|43 satisfying same_phase_lane, Rres=o4|o4, "
            "at_winner, prev_open_offset=4, and prev_d<=4."
        )
    elif stage == "directed_tuple":
        claim = (
            "Under the prior stages, the listed lanes never enter either "
            "allowed directed tuple: even|mid|o4 or odd|early|o6."
        )
        falsifier = (
            "A row in any listed lane satisfying the prior stages and "
            "directed_tuple in {even|mid|o4, odd|early|o6}."
        )
    elif stage == "next_parity_odd":
        claim = (
            "Under the prior stages, lane 163|19 reaches the allowed tuple "
            "surface only through non-odd next parity."
        )
        falsifier = (
            "A row in lane 163|19 satisfying all prior stages and "
            "next_parity=odd."
        )
    else:
        raise ValueError(f"unexpected first-zero stage: {stage}")
    return {
        "rule_id": RULE_ID,
        "component_law": stage,
        "covered_lanes": lanes,
        "covered_lane_count": len(lanes),
        "prior_surface": STAGE_PRIORS[stage],
        "candidate_universal_claim": claim,
        "falsifier_contract": falsifier,
        "proof_status": "unproved",
    }


def component_law_table() -> list[dict[str, object]]:
    """Return component-law proof contracts."""
    return [
        law_for_stage(stage, lanes)
        for stage, lanes in stage_lanes(excluded_cascades()).items()
    ]


def lane_law_assignments() -> list[dict[str, object]]:
    """Return one proof-law assignment per excluded lane."""
    laws = {
        str(law["component_law"]): law
        for law in component_law_table()
    }
    near_miss_counts = Counter(str(row["lane"]) for row in load_round9_near_misses())
    assignments = []
    for row in excluded_cascades():
        stage = str(row["first_zero_stage"])
        law = laws[stage]
        assignments.append(
            {
                "rule_id": RULE_ID,
                "lane": row["lane"],
                "orientation": row["orientation"],
                "phase_mod36": row["phase_mod36"],
                "first_zero_stage": stage,
                "assigned_component_law": stage,
                "last_nonzero_stage": row["last_nonzero_stage"],
                "near_miss_row_count": near_miss_counts[str(row["lane"])],
                "stage_counts": row["stage_counts"],
                "falsifier_contract": law["falsifier_contract"],
                "proof_status": "unproved",
            }
        )
    assignments.sort(key=lambda item: (str(item["assigned_component_law"]), str(item["lane"])))
    return assignments


def falsifier_contracts() -> list[dict[str, object]]:
    """Return one falsifier contract per component law."""
    return [
        {
            "rule_id": RULE_ID,
            "component_law": law["component_law"],
            "covered_lanes": law["covered_lanes"],
            "falsifier_contract": law["falsifier_contract"],
            "falsifier_status": "not_observed_in_round9_measured_cascade",
        }
        for law in component_law_table()
    ]


def proof_composition() -> dict[str, object]:
    """Return the proof composition scaffold."""
    return {
        "rule_id": RULE_ID,
        "proof_status": "incomplete",
        "composition": [
            {
                "step": "same-phase lane table",
                "input": "Rres=o4|o4 + same_mod36",
                "output": "12 theoretical ordered mod-180 lanes",
                "status": "finite table emitted in Round 6",
            },
            {
                "step": "component obstruction laws",
                "input": "12 theoretical lanes + ordered public predicate cascade",
                "output": "10 excluded lanes + 2 survivors",
                "status": "measured in Round 9, unproved universally",
            },
            {
                "step": "terminal image",
                "input": "survivor lanes 43|79 and 49|13",
                "output": "lower predecessor pairs 19|22 and 29|18, each with four slots",
                "status": "measured in Rounds 6-8, unproved universally",
            },
        ],
        "theorem_status": "hypothesis_not_proved",
    }


def summary() -> dict[str, object]:
    """Return Round 10 summary."""
    laws = component_law_table()
    assignments = lane_law_assignments()
    covered = sorted({str(item["lane"]) for item in assignments})
    expected = sorted(str(row["lane"]) for row in excluded_cascades())
    return {
        "rule_id": RULE_ID,
        "status": "measured_component_law_scaffold",
        "component_law_count": len(laws),
        "excluded_lane_assignment_count": len(assignments),
        "covered_excluded_lane_count": len(covered),
        "uncovered_excluded_lane_count": len(set(expected) - set(covered)),
        "component_laws_cover_all_excluded_lanes": covered == expected,
        "component_law_lane_counts": {
            str(law["component_law"]): int(law["covered_lane_count"])
            for law in laws
        },
        "survivor_lanes": SURVIVOR_LANES,
        "proof_composition_ready": True,
        "universal_proof_complete": False,
        "theorem_status": "hypothesis_not_proved",
        "next_required_proof_object": (
            "prove the four component obstruction laws universally, then "
            "compose them with the terminal image"
        ),
    }


def main() -> int:
    """Run the component-law scaffold builder."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    write_jsonl(OUTPUT_DIR / "component_law_table.jsonl", component_law_table())
    write_jsonl(
        OUTPUT_DIR / "excluded_lane_law_assignments.jsonl",
        lane_law_assignments(),
    )
    write_jsonl(OUTPUT_DIR / "falsifier_contracts.jsonl", falsifier_contracts())
    write_json(OUTPUT_DIR / "proof_composition.json", proof_composition())
    payload = summary()
    write_json(OUTPUT_DIR / "summary.json", payload)
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
