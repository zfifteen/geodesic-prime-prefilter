#!/usr/bin/env python3
"""Translate the public left-neighbor gate into residue arithmetic."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

from first_gap_compatibility_check import write_json
from slot_factor_public_quotient_test import read_jsonl


THIS_DIR = Path(__file__).resolve().parent
INPUT_ROOT = THIS_DIR / "output"
SPAN_DIR = INPUT_ROOT / "span36_terminal_lift_probe"
OUTPUT_DIR = INPUT_ROOT / "public_left_gate_arithmetic_probe"
RULE_ID = "pedk_public_left_gate_arithmetic_probe_v1"
TARGET_CONTAINING_TYPE = "o6_d4_a6_d4_odd"
PREVIOUS_FIRST_OPEN_O4_LEFT_RESIDUES = {7, 13, 19}


def public_parts(public_key: str) -> dict[str, str]:
    """Split a public key into public gap-neighborhood parts."""
    before_side, side = public_key.rsplit("|", 1)
    prev_part, rest = before_side.split("|containing=", 1)
    containing, next_part = rest.split("|next=", 1)
    containing_type, containing_phase = containing.rsplit("@", 1)
    prev = prev_part.removeprefix("prev=")
    return {
        "prev": prev,
        "prev_first_open": prev.split("_", 1)[0],
        "containing_type": containing_type,
        "containing_phase": containing_phase,
        "next": next_part,
        "side": side,
    }


def enriched_rows_for(rows: list[dict[str, object]]) -> dict[tuple[str, str], dict[str, object]]:
    """Return enriched rows keyed by window and case ID."""
    needed_by_window: dict[str, set[str]] = {}
    for row in rows:
        needed_by_window.setdefault(str(row["window"]), set()).add(str(row["case_id"]))

    out = {}
    for window, case_ids in sorted(needed_by_window.items()):
        path = (
            INPUT_ROOT
            / f"enriched_multiplication_map_corpus_{window}"
            / "enriched_rows.jsonl"
        )
        for row in read_jsonl(path):
            case_id = str(row["case_id"])
            if case_id in case_ids:
                out[(window, case_id)] = row
    return out


def public_previous_left_mod30(
    row: dict[str, object],
    enriched: dict[tuple[str, str], dict[str, object]],
) -> int:
    """Return the left endpoint residue of the previous public gap."""
    enriched_row = enriched[(str(row["window"]), str(row["case_id"]))]
    public_left = int(enriched_row["N"]) - int(enriched_row["public_n_offset_from_left"])
    previous_width = int(enriched_row["public_previous_gap"]["gap_width"])
    return (public_left - previous_width) % 30


def public_previous_width(
    row: dict[str, object],
    enriched: dict[tuple[str, str], dict[str, object]],
) -> int:
    """Return the width of the previous public gap."""
    enriched_row = enriched[(str(row["window"]), str(row["case_id"]))]
    return int(enriched_row["public_previous_gap"]["gap_width"])


def count_by(rows: list[dict[str, object]], key: str) -> dict[str, int]:
    """Return JSON-safe counts for one row key."""
    return {
        str(value): count
        for value, count in sorted(Counter(row[key] for row in rows).items())
    }


def enriched_public_rows(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    """Return rows with public gate arithmetic attached."""
    enriched = enriched_rows_for(rows)
    out = []
    for row in rows:
        parts = public_parts(str(row["public_key"]))
        prev_left_mod30 = public_previous_left_mod30(row, enriched)
        out.append(
            {
                "case_id": row["case_id"],
                "window": row["window"],
                "factor_mod180_lane": row["factor_mod180_lane"],
                "public_key": row["public_key"],
                "public_containing_type": parts["containing_type"],
                "public_previous_first_open": parts["prev_first_open"],
                "public_previous_left_mod30": prev_left_mod30,
                "public_previous_width": public_previous_width(row, enriched),
                "public_left_neighbor_gate": (
                    parts["containing_type"] == TARGET_CONTAINING_TYPE
                    and prev_left_mod30 in PREVIOUS_FIRST_OPEN_O4_LEFT_RESIDUES
                ),
                "lower_twin_distance": row["lower_twin_distance"],
                "p_preceding_left_endpoint_mod30": row[
                    "p_preceding_left_endpoint_mod30"
                ],
                "p_preceding_gap_width": row["p_preceding_gap_width"],
                "p_left_distance": row["p_left_distance"],
            }
        )
    return out


def same_lane_prior_rows(
    observed_rows: list[dict[str, object]],
    prior_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    """Return prior rows in the same mod-180 factor lanes as observations."""
    lanes = {str(row["factor_mod180_lane"]) for row in observed_rows}
    return [
        row
        for row in prior_rows
        if str(row["factor_mod180_lane"]) in lanes
    ]


def summary(
    observed_rows: list[dict[str, object]],
    prior_rows: list[dict[str, object]],
) -> dict[str, object]:
    """Return the residue translation for the public left-neighbor gate."""
    prior_same_lanes = same_lane_prior_rows(observed_rows, prior_rows)
    observed = enriched_public_rows(observed_rows)
    prior_same = enriched_public_rows(prior_same_lanes)
    prior_target_type = [
        row for row in prior_same
        if row["public_containing_type"] == TARGET_CONTAINING_TYPE
    ]
    prior_previous_o4 = [
        row for row in prior_same
        if row["public_previous_left_mod30"] in PREVIOUS_FIRST_OPEN_O4_LEFT_RESIDUES
    ]
    return {
        "rule_id": RULE_ID,
        "status": "measured_public_left_gate_arithmetic_probe",
        "theorem_status": "hypothesis_not_proved",
        "target_containing_type": TARGET_CONTAINING_TYPE,
        "previous_first_open_o4_left_residues": sorted(
            PREVIOUS_FIRST_OPEN_O4_LEFT_RESIDUES
        ),
        "observed_row_count": len(observed),
        "observed_rows_in_residue_gate": sum(
            1 for row in observed if row["public_left_neighbor_gate"]
        ),
        "observed_public_previous_left_mod30_counts": count_by(
            observed,
            "public_previous_left_mod30",
        ),
        "observed_public_previous_width_counts": count_by(
            observed,
            "public_previous_width",
        ),
        "prior_same_lane_row_count": len(prior_same),
        "prior_same_lane_target_containing_type_rows": len(prior_target_type),
        "prior_same_lane_previous_o4_left_residue_rows": len(prior_previous_o4),
        "prior_same_lane_rows_in_residue_gate": sum(
            1 for row in prior_same if row["public_left_neighbor_gate"]
        ),
        "prior_target_type_public_previous_left_mod30_counts": count_by(
            prior_target_type,
            "public_previous_left_mod30",
        ),
        "prior_target_type_public_previous_width_counts": count_by(
            prior_target_type,
            "public_previous_width",
        ),
        "prior_previous_o4_containing_type_counts": count_by(
            prior_previous_o4,
            "public_containing_type",
        ),
        "sharper_arithmetic_statement": (
            "The public left-neighbor gate is the residue conjunction "
            "public_previous_left_endpoint mod 30 in {7, 13, 19} and "
            "public_containing_exact_type o6_d4_a6_d4_odd. Inside the same "
            "mod-180 factor lanes, prior support reaches the target containing "
            "type and reaches the previous-o4 residue set separately, but it "
            "never reaches their conjunction. The observed replacement rows "
            "both reach that conjunction."
        ),
    }


def main() -> int:
    """Run the public left-gate arithmetic probe."""
    observed_rows = read_jsonl(SPAN_DIR / "observed_replacement_rows.jsonl")
    prior_rows = read_jsonl(SPAN_DIR / "prior_support_rows.jsonl")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    payload = summary(observed_rows, prior_rows)
    write_json(OUTPUT_DIR / "summary.json", payload)
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
