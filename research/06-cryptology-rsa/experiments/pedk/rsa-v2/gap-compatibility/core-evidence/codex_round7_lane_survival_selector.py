#!/usr/bin/env python3
"""Round 7 lane-survival selector for the odd-exit same-phase target."""

from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path

from codex_round5_same_phase_boundary_probe import annotated_rows, target_rows
from codex_round6_sync_chain_table import theoretical_same_phase_lanes
from first_gap_compatibility_check import write_json, write_jsonl


THIS_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = THIS_DIR / "output" / "codex_round7_lane_survival_selector"
RULE_ID = "pedk_codex_round7_lane_survival_selector_v1"
EXPECTED_LANES = {"43|79", "49|13"}


def count_by(rows: list[dict[str, object]], key: str) -> dict[str, int]:
    """Return JSON-safe counts by one field."""
    counts = Counter(str(row[key]) for row in rows)
    return {value: counts[value] for value in sorted(counts)}


def compact_surviving_row(row: dict[str, object]) -> dict[str, object]:
    """Return lane-selector fields for one surviving row."""
    return {
        "rule_id": RULE_ID,
        "window": row["window"],
        "case_id": row["case_id"],
        "public_key": row["public_key"],
        "signature": row["signature"],
        "factor_mod180_lane": row["factor_mod180_lane"],
        "p_mod30": row["p_mod30"],
        "q_mod30": row["q_mod30"],
        "p_mod36": row["p_mod36"],
        "q_mod36": row["q_mod36"],
        "phase_width_pair": row["phase_width_pair"],
        "phase_width_complement": row["phase_width_complement"],
        "lower_predecessor_residue_width_pair": row[
            "lower_predecessor_residue_width_pair"
        ],
        "lower_predecessor_open_slot_count": row[
            "lower_predecessor_open_slot_count"
        ],
        "lower_terminal_four_slot": row["lower_terminal_four_slot"],
    }


def signature_lane_map(rows: list[dict[str, object]]) -> dict[str, object]:
    """Return the measured public-signature to lane image."""
    grouped: dict[str, list[dict[str, object]]] = defaultdict(list)
    for row in rows:
        grouped[str(row["signature"])].append(row)

    out = {}
    for signature, signature_rows in sorted(grouped.items()):
        out[signature] = {
            "row_count": len(signature_rows),
            "lanes": sorted({str(row["factor_mod180_lane"]) for row in signature_rows}),
            "phase_width_pairs": count_by(signature_rows, "phase_width_pair"),
            "lower_predecessor_pairs": count_by(
                signature_rows,
                "lower_predecessor_residue_width_pair",
            ),
            "case_ids": [str(row["case_id"]) for row in signature_rows],
        }
    return out


def lane_survival_table(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    """Return one row for each theoretical same-phase lane."""
    target_by_lane: dict[str, list[dict[str, object]]] = defaultdict(list)
    for row in rows:
        target_by_lane[str(row["factor_mod180_lane"])].append(row)

    table = []
    for lane in theoretical_same_phase_lanes():
        lane_value = str(lane["lane"])
        surviving_rows = target_by_lane[lane_value]
        table.append(
            {
                "rule_id": RULE_ID,
                **lane,
                "survives_odd_exit_rres_same_phase": bool(surviving_rows),
                "surviving_row_count": len(surviving_rows),
                "signatures": sorted(
                    {str(row["signature"]) for row in surviving_rows}
                ),
                "phase_width_pairs": count_by(
                    surviving_rows,
                    "phase_width_pair",
                ),
                "lower_predecessor_pairs": count_by(
                    surviving_rows,
                    "lower_predecessor_residue_width_pair",
                ),
                "lower_terminal_four_slot_count": sum(
                    1 for row in surviving_rows if row["lower_terminal_four_slot"]
                ),
            }
        )
    return table


def summary(rows: list[dict[str, object]]) -> dict[str, object]:
    """Return lane-survival selector summary."""
    targets = target_rows(rows)
    same_phase_targets = [row for row in targets if row["same_mod36"]]
    table = lane_survival_table(same_phase_targets)
    surviving = [row for row in table if row["survives_odd_exit_rres_same_phase"]]
    excluded = [row for row in table if not row["survives_odd_exit_rres_same_phase"]]
    observed_lanes = sorted(str(row["lane"]) for row in surviving)
    public_map = signature_lane_map(same_phase_targets)
    return {
        "rule_id": RULE_ID,
        "status": "measured_codex_round7_lane_survival_selector",
        "theorem_status": "hypothesis_not_proved",
        "theoretical_same_phase_lane_count": len(table),
        "same_phase_target_row_count": len(same_phase_targets),
        "observed_same_phase_lane_count": len(observed_lanes),
        "excluded_same_phase_lane_count": len(excluded),
        "observed_same_phase_lanes": observed_lanes,
        "excluded_same_phase_lanes": sorted(str(row["lane"]) for row in excluded),
        "public_signature_lane_map": public_map,
        "signature_to_lane_is_deterministic": all(
            len(data["lanes"]) == 1 for data in public_map.values()
        ),
        "measured_image_exactly_expected_lanes": set(observed_lanes) == EXPECTED_LANES,
        "selected_lanes_lower_predecessor_pairs": count_by(
            same_phase_targets,
            "lower_predecessor_residue_width_pair",
        ),
        "selected_lanes_phase_width_pairs": count_by(
            same_phase_targets,
            "phase_width_pair",
        ),
        "selected_lanes_lift_falsifier_count": sum(
            1 for row in same_phase_targets if not row["lower_terminal_four_slot"]
        ),
    }


def main() -> int:
    """Run the lane-survival selector."""
    rows = annotated_rows()
    same_phase_targets = [
        row for row in target_rows(rows) if row["same_mod36"]
    ]
    table = lane_survival_table(same_phase_targets)
    excluded = [row for row in table if not row["survives_odd_exit_rres_same_phase"]]

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    write_jsonl(OUTPUT_DIR / "same_phase_lane_survival_table.jsonl", table)
    write_json(
        OUTPUT_DIR / "public_signature_lane_map.json",
        signature_lane_map(same_phase_targets),
    )
    write_jsonl(OUTPUT_DIR / "excluded_same_phase_lanes.jsonl", excluded)
    write_jsonl(
        OUTPUT_DIR / "surviving_lane_rows.jsonl",
        [compact_surviving_row(row) for row in same_phase_targets],
    )
    payload = summary(rows)
    write_json(OUTPUT_DIR / "summary.json", payload)
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
