#!/usr/bin/env python3
"""Emit the compact zero-to-zero endpoint-space exclusion rule."""

from __future__ import annotations

import json
from pathlib import Path

from first_gap_compatibility_check import write_json, write_jsonl
from joint_endpoint_pair_right_boundary_surface import rate_ppm
from slot_factor_public_quotient_test import read_jsonl


THIS_DIR = Path(__file__).resolve().parent
INPUT_PATH = THIS_DIR / "output" / "public_selected_contrast_probe" / "candidate_rows.jsonl"
OUTPUT_DIR = THIS_DIR / "output" / "zero_to_zero_exclusion_rule"
RULE_ID = "pedk_zero_to_zero_exclusion_rule_v1"


def is_rule_row(row: dict[str, object]) -> bool:
    """Return whether a candidate row satisfies the zero-to-zero rule."""
    return (
        row["public_side"] == "at_winner"
        and int(row["endpoint_transport_defect"]) == 0
        and row["status"] != "not_testable_forward"
    )


def rule_rows(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    """Return exact endpoint-space rows excluded by the zero-to-zero rule."""
    out = []
    for row in rows:
        if not is_rule_row(row):
            continue
        out.append(
            {
                "rule_id": RULE_ID,
                "exclusion_rule": (
                    "public_selected_defect_zero_and_endpoint_transport_defect_zero"
                ),
                "window": row["window"],
                "public_key": row["public_key"],
                "public_containing_exact_type_key": row[
                    "public_containing_exact_type_key"
                ],
                "pair_identity_key": row["pair_identity_key"],
                "right_boundary_residues": row["right_boundary_residues"],
                "public_selected_defect": 0,
                "endpoint_transport_defect": 0,
                "endpoint_residue_predicate": "avoid_{1,23}_and_touch_{7,13,19}",
                "prior_absent_and_supported": True,
                "exact_pair_falsified": row["exact_pair_falsified"],
                "status": row["status"],
            }
        )
    out.sort(
        key=lambda row: (
            str(row["window"]),
            str(row["public_key"]),
            str(row["pair_identity_key"]),
        )
    )
    return out


def summary(rows: list[dict[str, object]], excluded_rows: list[dict[str, object]]) -> dict[str, object]:
    """Return a compact rule summary."""
    falsified = [row for row in excluded_rows if row["exact_pair_falsified"]]
    return {
        "rule_id": RULE_ID,
        "status": "measured_zero_to_zero_exclusion_rule",
        "theorem_status": "hypothesis_not_proved",
        "inference_status": "not_live_pedk_inference",
        "source_candidate_rows": len(rows),
        "excluded_endpoint_cell_count": len(excluded_rows),
        "exact_falsification_count": len(falsified),
        "falsification_rate_ppm": rate_ppm(len(falsified), len(excluded_rows)),
        "public_selected_defect": 0,
        "endpoint_transport_defect": 0,
        "endpoint_residue_predicate": "avoid {1,23} and touch {7,13,19}",
        "rule": (
            "public_selected_defect(W)=0 and prior_absent(W,E) and "
            "supported(E) and endpoint_transport_defect(E)=0 -> exclude E"
        ),
    }


def main() -> int:
    """Write the zero-to-zero exclusion rule output."""
    rows = read_jsonl(INPUT_PATH)
    excluded_rows = rule_rows(rows)
    out_summary = summary(rows, excluded_rows)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    write_json(OUTPUT_DIR / "summary.json", out_summary)
    write_jsonl(OUTPUT_DIR / "excluded_endpoint_cell_rows.jsonl", excluded_rows)
    print(json.dumps(out_summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
