#!/usr/bin/env python3
"""Round 6 dependency table for the odd-exit same-phase synchronization chain."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

from codex_round5_same_phase_boundary_probe import (
    annotated_rows,
    target_rows,
)
from first_gap_compatibility_check import write_json, write_jsonl


THIS_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = THIS_DIR / "output" / "codex_round6_sync_chain_table"
RULE_ID = "pedk_codex_round6_sync_chain_table_v1"


def count_by(rows: list[dict[str, object]], key: str) -> dict[str, int]:
    """Return JSON-safe counts by one field."""
    counts = Counter(str(row[key]) for row in rows)
    return {value: counts[value] for value in sorted(counts)}


def theoretical_same_phase_lanes() -> list[dict[str, object]]:
    """Return the 12 ordered mod-180 lanes for factor cores 13|19 and 19|13."""
    lanes = []
    for p_mod30, q_mod30 in ((13, 19), (19, 13)):
        orientation = f"{p_mod30}|{q_mod30}"
        p_residues = [value for value in range(p_mod30, 180, 30)]
        q_residues = [value for value in range(q_mod30, 180, 30)]
        for p_mod180 in p_residues:
            matches = [
                q_mod180
                for q_mod180 in q_residues
                if q_mod180 % 36 == p_mod180 % 36
            ]
            if len(matches) != 1:
                raise ValueError(f"expected one phase match for {p_mod180}")
            q_mod180 = matches[0]
            lanes.append(
                {
                    "rule_id": RULE_ID,
                    "orientation": orientation,
                    "phase_mod36": p_mod180 % 36,
                    "lane": f"{p_mod180}|{q_mod180}",
                    "p_mod180": p_mod180,
                    "q_mod180": q_mod180,
                    "p_mod30": p_mod30,
                    "q_mod30": q_mod30,
                }
            )
    lanes.sort(key=lambda row: (str(row["orientation"]), int(row["phase_mod36"])))
    return lanes


def compact_target_row(row: dict[str, object]) -> dict[str, object]:
    """Return dependency-relevant fields for one full target row."""
    return {
        "rule_id": RULE_ID,
        "window": row["window"],
        "case_id": row["case_id"],
        "public_key": row["public_key"],
        "signature": row["signature"],
        "same_mod36": row["same_mod36"],
        "p_mod36": row["p_mod36"],
        "q_mod36": row["q_mod36"],
        "factor_mod180_lane": row["factor_mod180_lane"],
        "phase_width_pair": row["phase_width_pair"],
        "phase_width_complement": row["phase_width_complement"],
        "lower_predecessor_residue_width_pair": row[
            "lower_predecessor_residue_width_pair"
        ],
        "lower_predecessor_open_slot_count": row[
            "lower_predecessor_open_slot_count"
        ],
        "lower_terminal_closure": row["lower_terminal_closure"],
        "lower_terminal_four_slot": row["lower_terminal_four_slot"],
    }


def dependency_key(row: dict[str, object]) -> str:
    """Return compact truth-state key for the three synchronization predicates."""
    return "|".join(
        (
            f"same={row['same_mod36']}",
            f"phase_width={row['phase_width_complement']}",
            f"lift={row['lower_terminal_four_slot']}",
        )
    )


def summary(rows: list[dict[str, object]]) -> dict[str, object]:
    """Return the Round 6 dependency-chain summary."""
    targets = target_rows(rows)
    same_phase_targets = [row for row in targets if row["same_mod36"]]
    non_same_phase_targets = [row for row in targets if not row["same_mod36"]]
    phase_width_targets = [row for row in targets if row["phase_width_complement"]]
    lift_targets = [row for row in targets if row["lower_terminal_four_slot"]]
    accidental_lifts = [
        row
        for row in targets
        if row["lower_terminal_four_slot"] and not row["same_mod36"]
    ]
    same_phase_lift_falsifiers = [
        row
        for row in same_phase_targets
        if not row["lower_terminal_four_slot"]
    ]
    phase_width_lift_falsifiers = [
        row
        for row in phase_width_targets
        if not row["lower_terminal_four_slot"]
    ]
    same_phase_phase_width_noncomplement = [
        row
        for row in same_phase_targets
        if not row["phase_width_complement"]
    ]
    lanes = theoretical_same_phase_lanes()
    observed_same_phase_lanes = sorted(
        {str(row["factor_mod180_lane"]) for row in same_phase_targets}
    )
    return {
        "rule_id": RULE_ID,
        "status": "measured_codex_round6_sync_chain_table",
        "theorem_status": "hypothesis_not_proved",
        "target_row_count": len(targets),
        "same_phase_target_count": len(same_phase_targets),
        "non_same_phase_target_count": len(non_same_phase_targets),
        "same_phase_phase_width_complement_count": sum(
            1 for row in same_phase_targets if row["phase_width_complement"]
        ),
        "same_phase_phase_width_noncomplement_count": len(
            same_phase_phase_width_noncomplement,
        ),
        "non_same_phase_phase_width_complement_count": sum(
            1 for row in non_same_phase_targets if row["phase_width_complement"]
        ),
        "phase_width_complement_target_count": len(phase_width_targets),
        "phase_width_complement_lift_falsifier_count": len(
            phase_width_lift_falsifiers,
        ),
        "lower_terminal_four_slot_target_count": len(lift_targets),
        "accidental_lift_without_same_phase_count": len(accidental_lifts),
        "same_phase_lift_falsifier_count": len(same_phase_lift_falsifiers),
        "measured_chain_same_phase_to_phase_width_to_lift": (
            not same_phase_phase_width_noncomplement
            and not same_phase_lift_falsifiers
        ),
        "reverse_lift_to_same_phase_holds": not accidental_lifts,
        "dependency_truth_table_counts": dict(
            sorted(Counter(dependency_key(row) for row in targets).items())
        ),
        "same_phase_target_lanes": observed_same_phase_lanes,
        "same_phase_target_signature_counts": count_by(
            same_phase_targets,
            "signature",
        ),
        "same_phase_target_lower_predecessor_pair_counts": count_by(
            same_phase_targets,
            "lower_predecessor_residue_width_pair",
        ),
        "accidental_lift_lanes": sorted(
            {str(row["factor_mod180_lane"]) for row in accidental_lifts}
        ),
        "theoretical_same_phase_lane_count": len(lanes),
        "observed_same_phase_lane_count": len(observed_same_phase_lanes),
    }


def main() -> int:
    """Run the synchronization-chain dependency table."""
    rows = annotated_rows()
    targets = target_rows(rows)
    accidental_lifts = [
        row
        for row in targets
        if row["lower_terminal_four_slot"] and not row["same_mod36"]
    ]
    lanes = theoretical_same_phase_lanes()

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    write_jsonl(
        OUTPUT_DIR / "target_dependency_rows.jsonl",
        [compact_target_row(row) for row in targets],
    )
    write_jsonl(
        OUTPUT_DIR / "theoretical_same_phase_lanes.jsonl",
        lanes,
    )
    write_jsonl(
        OUTPUT_DIR / "accidental_lift_rows.jsonl",
        [compact_target_row(row) for row in accidental_lifts],
    )
    payload = summary(rows)
    write_json(OUTPUT_DIR / "summary.json", payload)
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
