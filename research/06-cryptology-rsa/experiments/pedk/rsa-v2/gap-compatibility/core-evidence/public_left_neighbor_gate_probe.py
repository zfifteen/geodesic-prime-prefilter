#!/usr/bin/env python3
"""Compress the exact public trigger to its minimal left-neighbor gate."""

from __future__ import annotations

import json
from pathlib import Path

from first_gap_compatibility_check import write_json
from slot_factor_public_quotient_test import read_jsonl


THIS_DIR = Path(__file__).resolve().parent
INPUT_DIR = THIS_DIR / "output" / "span36_terminal_lift_probe"
OUTPUT_DIR = THIS_DIR / "output" / "public_left_neighbor_gate_probe"
RULE_ID = "pedk_public_left_neighbor_gate_probe_v1"


def public_parts(public_key: str) -> dict[str, str]:
    """Split a public key into public gap-neighborhood parts."""
    before_side, side = public_key.rsplit("|", 1)
    prev_part, rest = before_side.split("|containing=", 1)
    containing, next_part = rest.split("|next=", 1)
    containing_type, containing_phase = containing.rsplit("@", 1)
    return {
        "prev": prev_part.removeprefix("prev="),
        "prev_first_open": prev_part.removeprefix("prev=").split("_", 1)[0],
        "containing": containing,
        "containing_type": containing_type,
        "containing_phase": containing_phase,
        "next": next_part,
        "next_first_open": next_part.split("_", 1)[0],
        "side": side,
    }


def gate_key(row: dict[str, object]) -> tuple[str, str]:
    """Return the two-part public left-neighbor gate."""
    parts = public_parts(str(row["public_key"]))
    return (parts["prev_first_open"], parts["containing_type"])


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


def row_count_in_keys(
    rows: list[dict[str, object]],
    keys: set[tuple[str, str]],
) -> int:
    """Return row count whose two-part public gate is in keys."""
    return sum(1 for row in rows if gate_key(row) in keys)


def count_single_part(
    rows: list[dict[str, object]],
    field: str,
    values: set[str],
) -> int:
    """Return row count whose public part field is in values."""
    return sum(
        1
        for row in rows
        if public_parts(str(row["public_key"]))[field] in values
    )


def summary(
    observed_rows: list[dict[str, object]],
    prior_rows: list[dict[str, object]],
) -> dict[str, object]:
    """Return the minimal public gate compression summary."""
    prior_same_lanes = same_lane_prior_rows(observed_rows, prior_rows)
    observed_gate_keys = {gate_key(row) for row in observed_rows}
    observed_containing_types = {
        public_parts(str(row["public_key"]))["containing_type"]
        for row in observed_rows
    }
    observed_prev_first_opens = {
        public_parts(str(row["public_key"]))["prev_first_open"]
        for row in observed_rows
    }
    return {
        "rule_id": RULE_ID,
        "status": "measured_public_left_neighbor_gate_probe",
        "theorem_status": "hypothesis_not_proved",
        "observed_row_count": len(observed_rows),
        "prior_same_lane_row_count": len(prior_same_lanes),
        "observed_gate_keys": [
            "|".join(key)
            for key in sorted(observed_gate_keys)
        ],
        "observed_rows_in_gate": row_count_in_keys(
            observed_rows,
            observed_gate_keys,
        ),
        "prior_same_lane_rows_in_gate": row_count_in_keys(
            prior_same_lanes,
            observed_gate_keys,
        ),
        "prior_same_lane_rows_with_observed_containing_type": count_single_part(
            prior_same_lanes,
            "containing_type",
            observed_containing_types,
        ),
        "prior_same_lane_rows_with_observed_prev_first_open": count_single_part(
            prior_same_lanes,
            "prev_first_open",
            observed_prev_first_opens,
        ),
        "sharper_arithmetic_statement": (
            "Inside the observed mod-180 factor lanes, the full exact public "
            "trigger compresses to a two-part public gate: previous public "
            "first-open offset o4 and containing public exact type "
            "o6_d4_a6_d4_odd. The containing type alone has prior support, "
            "and the previous first-open offset alone has prior support, but "
            "their conjunction has no prior support and contains both "
            "observed replacement rows."
        ),
    }


def main() -> int:
    """Run the public left-neighbor gate probe."""
    observed_rows = read_jsonl(INPUT_DIR / "observed_replacement_rows.jsonl")
    prior_rows = read_jsonl(INPUT_DIR / "prior_support_rows.jsonl")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    payload = summary(observed_rows, prior_rows)
    write_json(OUTPUT_DIR / "summary.json", payload)
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
