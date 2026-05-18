#!/usr/bin/env python3
"""Round 20 public square-fiber probe for the factor-lane bridge."""

from __future__ import annotations

from collections import defaultdict
from pathlib import Path

from codex_round6_sync_chain_table import theoretical_same_phase_lanes
from first_gap_compatibility_check import write_json, write_jsonl


THIS_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = THIS_DIR / "output" / "codex_round20_public_square_fiber_probe"
ROUND18_MATRIX = (
    THIS_DIR
    / "output"
    / "codex_round18_component_obstruction_compression"
    / "lane_mechanism_matrix.jsonl"
)
RULE_ID = "pedk_codex_round20_public_square_fiber_probe_v1"
SURVIVOR_LANES = {"43|79", "49|13"}


def lane_rows() -> list[dict[str, object]]:
    """Return the 12 same-phase lanes enriched with public square-fiber data."""
    rows: list[dict[str, object]] = []
    for lane in theoretical_same_phase_lanes():
        p_mod180 = int(lane["p_mod180"])
        q_mod180 = int(lane["q_mod180"])
        n_mod180 = (p_mod180 * q_mod180) % 180
        n_mod36 = n_mod180 % 36
        lane_name = str(lane["lane"])
        rows.append(
            {
                "rule_id": RULE_ID,
                "lane": lane_name,
                "orientation": lane["orientation"],
                "phase_mod36": lane["phase_mod36"],
                "p_mod180": p_mod180,
                "q_mod180": q_mod180,
                "p_mod36": p_mod180 % 36,
                "q_mod36": q_mod180 % 36,
                "n_mod180": n_mod180,
                "n_mod36": n_mod36,
                "same_phase_square_root": p_mod180 % 36,
                "is_survivor_lane": lane_name in SURVIVOR_LANES,
                "factor_found": False,
                "theorem_status": "hypothesis_not_proved",
                "universal_proof_complete": False,
            }
        )
    return rows


def fiber_rows(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    """Group same-phase lanes by the public N mod 180 fiber."""
    groups: dict[int, list[dict[str, object]]] = defaultdict(list)
    for row in rows:
        groups[int(row["n_mod180"])].append(row)

    out: list[dict[str, object]] = []
    for n_mod180 in sorted(groups):
        group = sorted(groups[n_mod180], key=lambda item: str(item["lane"]))
        survivor_lanes = [
            str(row["lane"]) for row in group if bool(row["is_survivor_lane"])
        ]
        out.append(
            {
                "rule_id": RULE_ID,
                "n_mod180": n_mod180,
                "n_mod36": n_mod180 % 36,
                "lane_count": len(group),
                "lanes": [str(row["lane"]) for row in group],
                "square_roots_mod36": sorted(
                    {int(row["same_phase_square_root"]) for row in group}
                ),
                "survivor_lanes": survivor_lanes,
                "survivor_count": len(survivor_lanes),
                "contains_survivor": bool(survivor_lanes),
            }
        )
    return out


def read_jsonl(path: Path) -> list[dict[str, object]]:
    """Read a JSONL file."""
    import json

    return [json.loads(line) for line in path.read_text().splitlines() if line]


def root_selector_rows(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    """Return Round 18 directed-tuple data inside survivor-bearing fibers."""
    matrix = {str(row["lane"]): row for row in read_jsonl(ROUND18_MATRIX)}
    survivor_fibers = {
        int(row["n_mod180"])
        for row in rows
        if bool(row["is_survivor_lane"])
    }
    out: list[dict[str, object]] = []
    for row in rows:
        n_mod180 = int(row["n_mod180"])
        if n_mod180 not in survivor_fibers:
            continue
        matrix_row = matrix[str(row["lane"])]
        out.append(
            {
                "rule_id": RULE_ID,
                "lane": row["lane"],
                "n_mod180": n_mod180,
                "orientation": row["orientation"],
                "same_phase_square_root": row["same_phase_square_root"],
                "is_survivor_lane": row["is_survivor_lane"],
                "signatures": matrix_row["signatures"],
                "allowed_directed_tuple_values": matrix_row[
                    "allowed_directed_tuple_values"
                ],
                "derived_mechanism_class": matrix_row["derived_mechanism_class"],
                "passes_directed_tuple_selector": bool(
                    matrix_row["allowed_directed_tuple_values"]
                ),
            }
        )
    out.sort(key=lambda item: (int(item["n_mod180"]), str(item["lane"])))
    return out


def summary(
    rows: list[dict[str, object]],
    fibers: list[dict[str, object]],
    selector_rows: list[dict[str, object]],
) -> dict[str, object]:
    """Return the Round 20 probe summary."""
    survivor_rows = [row for row in rows if bool(row["is_survivor_lane"])]
    survivor_fibers = sorted({int(row["n_mod180"]) for row in survivor_rows})
    selector_by_fiber: dict[int, list[dict[str, object]]] = defaultdict(list)
    for row in selector_rows:
        selector_by_fiber[int(row["n_mod180"])].append(row)
    directed_tuple_selector_unique_by_fiber = {}
    for n_mod180 in survivor_fibers:
        passing = [
            str(row["lane"])
            for row in selector_by_fiber[n_mod180]
            if bool(row["passes_directed_tuple_selector"])
        ]
        directed_tuple_selector_unique_by_fiber[str(n_mod180)] = passing
    return {
        "rule_id": RULE_ID,
        "status": "measured_public_square_fiber_probe",
        "round_status": "insight_ooda_round1_and_round2_landed",
        "theorem_status": "hypothesis_not_proved",
        "universal_proof_complete": False,
        "factor_found": False,
        "same_phase_lane_count": len(rows),
        "public_square_fiber_count": len(fibers),
        "fiber_lane_counts": {
            str(fiber["n_mod180"]): int(fiber["lane_count"]) for fiber in fibers
        },
        "survivor_lanes": sorted(SURVIVOR_LANES),
        "survivor_public_square_fibers": survivor_fibers,
        "survivor_fiber_count": len(survivor_fibers),
        "public_square_fiber_reduces_same_phase_lanes": True,
        "public_square_fiber_selects_survivor_lanes": False,
        "directed_tuple_selector_unique_by_survivor_fiber": (
            directed_tuple_selector_unique_by_fiber
        ),
        "directed_tuple_selector_selects_survivors_in_survivor_fibers": all(
            passing
            == [
                str(row["lane"])
                for row in survivor_rows
                if int(row["n_mod180"]) == int(n_mod180)
            ]
            for n_mod180, passing in directed_tuple_selector_unique_by_fiber.items()
        ),
        "strongest_supported_finding": (
            "The hidden same-phase lane table is organized into three public "
            "N mod 180 square fibers of four lanes each. The two survivor "
            "lanes occupy two of those public fibers. N mod 180 alone does "
            "not select the survivor lane inside a fiber, but the allowed "
            "directed public tuple selects exactly the survivor in each "
            "survivor-bearing fiber on the current matrix."
        ),
        "blocker_refinement": (
            "The bridge is not from public grammar directly to all twelve "
            "same-phase lanes. Public N mod 180 first chooses a square fiber; "
            "the unresolved selector is the public rule that chooses the "
            "correct root lane inside that fiber."
        ),
        "next_context": (
            "Test whether the allowed directed public tuple is a root selector "
            "inside each public N mod 180 square fiber, and then determine "
            "why the N mod 180 = 37 fiber carries no survivor."
        ),
        "disconfirmation_condition": (
            "If a survivor lane is not inside the computed public N mod 180 "
            "square fibers, if N mod 180 already selects a unique survivor "
            "lane, or if the allowed directed tuple selects a non-survivor "
            "inside a survivor-bearing fiber, this probe's blocker refinement "
            "is wrong."
        ),
    }


def main() -> None:
    rows = lane_rows()
    fibers = fiber_rows(rows)
    selector_rows = root_selector_rows(rows)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    write_jsonl(OUTPUT_DIR / "lane_square_fiber_rows.jsonl", rows)
    write_jsonl(OUTPUT_DIR / "public_square_fibers.jsonl", fibers)
    write_jsonl(OUTPUT_DIR / "root_selector_rows.jsonl", selector_rows)
    write_json(OUTPUT_DIR / "summary.json", summary(rows, fibers, selector_rows))


if __name__ == "__main__":
    main()
