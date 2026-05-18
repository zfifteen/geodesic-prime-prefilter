#!/usr/bin/env python3
"""Round 21 public square-fiber root selector probe."""

from __future__ import annotations

import json
from pathlib import Path

from first_gap_compatibility_check import write_json, write_jsonl


THIS_DIR = Path(__file__).resolve().parent
ROUND18_MATRIX = (
    THIS_DIR
    / "output"
    / "codex_round18_component_obstruction_compression"
    / "lane_mechanism_matrix.jsonl"
)
OUTPUT_DIR = THIS_DIR / "output" / "codex_round21_public_square_fiber_root_selector"
RULE_ID = "pedk_codex_round21_public_square_fiber_root_selector_v1"


def read_jsonl(path: Path) -> list[dict[str, object]]:
    """Read JSONL rows."""
    return [json.loads(line) for line in path.read_text().splitlines() if line]


def candidate_lanes_by_public_fiber() -> dict[int, list[str]]:
    """Enumerate same-phase candidate lanes from public N mod 180 fibers."""
    by_fiber: dict[int, list[str]] = {}
    for p_core, q_core in ((13, 19), (19, 13)):
        for p_mod180 in range(p_core, 180, 30):
            for q_mod180 in range(q_core, 180, 30):
                if p_mod180 % 36 != q_mod180 % 36:
                    continue
                n_mod180 = (p_mod180 * q_mod180) % 180
                by_fiber.setdefault(n_mod180, []).append(f"{p_mod180}|{q_mod180}")
    return {key: sorted(value) for key, value in sorted(by_fiber.items())}


def matrix_by_lane() -> dict[str, dict[str, object]]:
    """Return Round 18 lane matrix rows keyed by lane."""
    return {str(row["lane"]): row for row in read_jsonl(ROUND18_MATRIX)}


def candidate_rows() -> list[dict[str, object]]:
    """Return candidate root rows with public gate co-landing status."""
    matrix = matrix_by_lane()
    rows: list[dict[str, object]] = []
    for n_mod180, lanes in candidate_lanes_by_public_fiber().items():
        for lane in lanes:
            row = matrix[lane]
            has_entry_open_4 = 4 in [int(value) for value in row["computed_prev_open_offset_values"]]
            has_prev_d_le4 = any(int(value) <= 4 for value in row["prev_d_values"])
            has_directed_tuple = bool(row["allowed_directed_tuple_values"])
            has_next_d_le4 = any(int(value) <= 4 for value in row["next_d_values"])
            has_exit_odd = "odd" in [str(value) for value in row["computed_next_parity_values"]]
            selector_pass = (
                has_entry_open_4
                and has_prev_d_le4
                and has_directed_tuple
                and has_next_d_le4
                and has_exit_odd
            )
            rows.append(
                {
                    "rule_id": RULE_ID,
                    "n_mod180": n_mod180,
                    "lane": lane,
                    "orientation": row["orientation"],
                    "same_phase_square_root": int(lane.split("|")[0]) % 36,
                    "has_entry_open_4": has_entry_open_4,
                    "has_prev_d_le4": has_prev_d_le4,
                    "has_directed_tuple": has_directed_tuple,
                    "allowed_directed_tuple_values": row["allowed_directed_tuple_values"],
                    "has_next_d_le4": has_next_d_le4,
                    "has_exit_odd": has_exit_odd,
                    "selector_pass": selector_pass,
                    "survivor_status": row["survivor_status"],
                    "derived_mechanism_class": row["derived_mechanism_class"],
                    "lower_terminal_four_slot_values": row["lower_terminal_four_slot_values"],
                    "factor_found": False,
                    "theorem_status": "hypothesis_not_proved",
                    "universal_proof_complete": False,
                }
            )
    return rows


def fiber_rows(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    """Return one selector summary row per public fiber."""
    out: list[dict[str, object]] = []
    for n_mod180 in sorted({int(row["n_mod180"]) for row in rows}):
        group = [row for row in rows if int(row["n_mod180"]) == n_mod180]
        selector_pass_lanes = [str(row["lane"]) for row in group if bool(row["selector_pass"])]
        survivor_lanes = [
            str(row["lane"]) for row in group if str(row["survivor_status"]) == "survivor"
        ]
        out.append(
            {
                "rule_id": RULE_ID,
                "n_mod180": n_mod180,
                "candidate_lanes": [str(row["lane"]) for row in group],
                "selector_pass_lanes": selector_pass_lanes,
                "survivor_lanes": survivor_lanes,
                "selector_matches_survivors": selector_pass_lanes == survivor_lanes,
                "selector_pass_count": len(selector_pass_lanes),
                "survivor_count": len(survivor_lanes),
            }
        )
    return out


def summary(fibers: list[dict[str, object]]) -> dict[str, object]:
    """Return probe summary."""
    return {
        "rule_id": RULE_ID,
        "status": "measured_public_square_fiber_root_selector",
        "theorem_status": "hypothesis_not_proved",
        "universal_proof_complete": False,
        "factor_found": False,
        "public_fiber_count": len(fibers),
        "selector_matches_survivors_all_fibers": all(
            bool(row["selector_matches_survivors"]) for row in fibers
        ),
        "fiber_selector_results": {
            str(row["n_mod180"]): row["selector_pass_lanes"] for row in fibers
        },
        "fiber_survivor_results": {
            str(row["n_mod180"]): row["survivor_lanes"] for row in fibers
        },
        "strongest_supported_finding": (
            "Within the current same-phase/core-orientation surface, public "
            "N mod 180 enumerates four candidate root lanes per fiber, and "
            "public gate co-landing selects exactly the terminal-lift survivor "
            "lanes: none for 37, 49|13 for 97, and 43|79 for 157."
        ),
        "next_context": (
            "Promote the selector from lane-matrix measurement to a public "
            "candidate procedure by deriving the co-landing gates directly "
            "from public neighboring-gap rows."
        ),
    }


def main() -> None:
    rows = candidate_rows()
    fibers = fiber_rows(rows)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    write_jsonl(OUTPUT_DIR / "candidate_root_selector_rows.jsonl", rows)
    write_jsonl(OUTPUT_DIR / "fiber_selector_rows.jsonl", fibers)
    write_json(OUTPUT_DIR / "summary.json", summary(fibers))


if __name__ == "__main__":
    main()
