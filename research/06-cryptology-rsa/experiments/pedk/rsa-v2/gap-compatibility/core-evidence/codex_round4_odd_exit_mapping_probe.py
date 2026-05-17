#!/usr/bin/env python3
"""Round 4 odd-exit directed reentry mapping probe."""

from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path

from codex_round3_directed_reentry_lift_probe import annotated_rows
from first_gap_compatibility_check import write_json, write_jsonl


THIS_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = THIS_DIR / "output" / "codex_round4_odd_exit_mapping_probe"
RULE_ID = "pedk_codex_round4_odd_exit_mapping_probe_v1"


def odd_exit_directed_reentry(row: dict[str, object]) -> bool:
    """Return the accepted odd-exit directed reentry predicate."""
    return bool(row["directed_public_reentry2"]) and row["next_parity"] == "odd"


def target_rows(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    """Return rows under OddExit plus Rres=o4|o4."""
    return [
        row
        for row in rows
        if odd_exit_directed_reentry(row) and row["rres_o4_o4"]
    ]


def compact_row(row: dict[str, object]) -> dict[str, object]:
    """Return compact target-row data."""
    signature = (
        f"{row['prev_parity']}|{row['containing_position']}|"
        f"{row['next_open_type']}|{row['next_parity']}"
    )
    return {
        "rule_id": RULE_ID,
        "window": row["window"],
        "case_id": row["case_id"],
        "public_key": row["public_key"],
        "signature": signature,
        "factor_mod180_lane": row["factor_mod180_lane"],
        "p_mod30": row["p_mod30"],
        "q_mod30": row["q_mod30"],
        "p_mod36": row["p_mod36"],
        "q_mod36": row["q_mod36"],
        "phase_width_pair": row["phase_width_pair"],
        "phase_width_complement": row["phase_width_complement"],
        "right_boundary_residues": row["right_boundary_residues"],
        "lower_predecessor_residue_width_pair": row[
            "lower_predecessor_residue_width_pair"
        ],
        "lower_predecessor_open_slot_count": row[
            "lower_predecessor_open_slot_count"
        ],
        "lower_terminal_closure": row["lower_terminal_closure"],
        "lower_terminal_four_slot": row["lower_terminal_four_slot"],
    }


def count_by(rows: list[dict[str, object]], key: str) -> dict[str, int]:
    """Return JSON-safe counts by one field."""
    counts = Counter(str(row[key]) for row in rows)
    return {value: counts[value] for value in sorted(counts)}


def signature_mapping(rows: list[dict[str, object]]) -> dict[str, object]:
    """Return target mapping grouped by active signature."""
    groups: dict[str, list[dict[str, object]]] = defaultdict(list)
    for row in rows:
        groups[str(row["signature"])].append(row)
    out = {}
    for signature, grouped in sorted(groups.items()):
        out[signature] = {
            "row_count": len(grouped),
            "factor_mod180_lane_counts": count_by(grouped, "factor_mod180_lane"),
            "phase_width_pair_counts": count_by(grouped, "phase_width_pair"),
            "lower_predecessor_pair_counts": count_by(
                grouped,
                "lower_predecessor_residue_width_pair",
            ),
            "open_slot_count_counts": count_by(
                grouped,
                "lower_predecessor_open_slot_count",
            ),
            "case_ids": [str(row["case_id"]) for row in grouped],
        }
    return out


def summary(rows: list[dict[str, object]]) -> dict[str, object]:
    """Return Round 4 summary."""
    odd_exit_rows = [
        row for row in rows if odd_exit_directed_reentry(row)
    ]
    targets = [compact_row(row) for row in target_rows(rows)]
    falsifiers = [
        row for row in targets if not row["lower_terminal_four_slot"]
    ]
    return {
        "rule_id": RULE_ID,
        "status": "measured_codex_round4_odd_exit_mapping_probe",
        "theorem_status": "hypothesis_not_proved",
        "high_signal_same_phase_row_count": len(rows),
        "odd_exit_directed_reentry_row_count": len(odd_exit_rows),
        "odd_exit_rres_o4_o4_row_count": len(targets),
        "odd_exit_rres_o4_o4_falsifier_count": len(falsifiers),
        "phase_width_complement_automatic_after_odd_exit_rres": all(
            row["phase_width_complement"] for row in targets
        ),
        "lift_clean_without_phase_width_premise": not falsifiers,
        "target_factor_mod180_lane_counts": count_by(
            targets,
            "factor_mod180_lane",
        ),
        "target_phase_width_pair_counts": count_by(targets, "phase_width_pair"),
        "target_lower_predecessor_pair_counts": count_by(
            targets,
            "lower_predecessor_residue_width_pair",
        ),
        "target_signature_counts": count_by(targets, "signature"),
        "signature_mapping": signature_mapping(targets),
    }


def main() -> int:
    """Run the odd-exit mapping probe."""
    rows = annotated_rows()
    targets = [compact_row(row) for row in target_rows(rows)]
    falsifiers = [
        row for row in targets if not row["lower_terminal_four_slot"]
    ]
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    write_jsonl(OUTPUT_DIR / "target_rows.jsonl", targets)
    write_jsonl(OUTPUT_DIR / "falsifier_rows.jsonl", falsifiers)
    write_json(OUTPUT_DIR / "signature_mapping.json", signature_mapping(targets))
    payload = summary(rows)
    write_json(OUTPUT_DIR / "summary.json", payload)
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
