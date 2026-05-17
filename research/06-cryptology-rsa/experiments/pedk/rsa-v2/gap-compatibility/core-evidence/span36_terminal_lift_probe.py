#!/usr/bin/env python3
"""Probe span-36 plus lower terminal lift in the public o6 trigger surface."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

from first_gap_compatibility_check import write_json, write_jsonl
from slot_factor_public_quotient_test import read_jsonl


THIS_DIR = Path(__file__).resolve().parent
INPUT_ROOT = THIS_DIR / "output"
ORIENTATION_DIR = INPUT_ROOT / "lower_terminal_twin_orientation_probe"
OUTPUT_DIR = INPUT_ROOT / "span36_terminal_lift_probe"
RULE_ID = "pedk_span36_terminal_lift_probe_v1"
WHEEL_OPEN_RESIDUES = {1, 7, 11, 13, 17, 19, 23, 29}


def interior_open_slot_count(left_endpoint: int, width: int) -> int:
    """Return open wheel slots strictly inside a gap."""
    return sum(
        1
        for value in range(left_endpoint + 1, left_endpoint + width)
        if value % 30 in WHEEL_OPEN_RESIDUES
    )


def enriched_rows_for(
    payload_rows: list[dict[str, object]],
) -> dict[tuple[str, str], dict[str, object]]:
    """Return enriched rows keyed by window and case ID."""
    needed_by_window: dict[str, set[str]] = {}
    for row in payload_rows:
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


def with_span_fields(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    """Attach direct factor-span arithmetic to orientation rows."""
    enriched = enriched_rows_for(rows)
    out = []
    for row in rows:
        key = (str(row["window"]), str(row["case_id"]))
        enriched_row = enriched[key]
        p = int(enriched_row["p"])
        q = int(enriched_row["q"])
        span = q - p
        terminal_side = str(row["terminal_side"])
        p_left_width = int(enriched_row["p_left_gap_width"])
        p_left_offset = int(enriched_row["p_left_winner_offset"])
        p_left_distance = p_left_width - p_left_offset
        p_preceding_left_endpoint = p - p_left_width
        p_preceding_open_slots = interior_open_slot_count(
            p_preceding_left_endpoint,
            p_left_offset,
        )
        public_left_endpoint = int(enriched_row["N"]) - int(
            enriched_row["public_n_offset_from_left"]
        )
        full_public_key = (
            row.get("public_key")
            or f"{enriched_row['public_word']}|{enriched_row['public_gwr_side']}"
        )
        out.append(
            {
                "rule_id": RULE_ID,
                "window": row["window"],
                "case_id": row["case_id"],
                "public_key": full_public_key,
                "p_mod30": p % 30,
                "q_mod30": q % 30,
                "p_mod36": p % 36,
                "q_mod36": q % 36,
                "p_mod180": p % 180,
                "q_mod180": q % 180,
                "N_mod60": int(enriched_row["N"]) % 60,
                "public_left_endpoint_mod60": public_left_endpoint % 60,
                "factor_mod180_lane": f"{p % 180}|{q % 180}",
                "same_mod36": p % 36 == q % 36,
                "span": span,
                "span_mod36": span % 36,
                "span_divisible_by_36": span % 36 == 0,
                "p_left_distance": p_left_distance,
                "p_preceding_gap_width": p_left_offset,
                "p_preceding_left_endpoint_mod30": p_preceding_left_endpoint % 30,
                "p_preceding_left_endpoint_mod180": p_preceding_left_endpoint % 180,
                "p_preceding_open_slots": p_preceding_open_slots,
                "p_left_bridge_width": p_left_width,
                "lower_twin_distance": p_left_distance == 2,
                "lower_long_preceding_gap": p_left_offset >= 18,
                "lower_four_slot_preceding_gap": p_preceding_open_slots == 4,
                "terminal_side": terminal_side,
                "lower_terminal_lift": terminal_side == "p",
                "any_terminal_lift": terminal_side != "none",
            }
        )
    return out


def count_by(rows: list[dict[str, object]], key: str) -> dict[str, int]:
    """Return JSON-safe counts for one row key."""
    return {
        str(value): count
        for value, count in sorted(Counter(row[key] for row in rows).items())
    }


def conjunction_count(rows: list[dict[str, object]]) -> int:
    """Return rows with span divisible by 36 and lower terminal lift."""
    return sum(
        1
        for row in rows
        if row["span_divisible_by_36"] and row["lower_terminal_lift"]
    )


def rows_in_lanes(
    rows: list[dict[str, object]],
    lanes: set[str],
) -> list[dict[str, object]]:
    """Return rows occupying one of the supplied mod-180 lanes."""
    return [
        row
        for row in rows
        if str(row["factor_mod180_lane"]) in lanes
    ]


def lower_twin_rows(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    """Return rows where the lower factor is two units after the left endpoint."""
    return [
        row
        for row in rows
        if row["lower_twin_distance"]
    ]


def public_left_31_rows(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    """Return rows whose public left endpoint is 31 modulo 60."""
    return [
        row
        for row in rows
        if row["public_left_endpoint_mod60"] == 31
    ]


def rows_in_public_keys(
    rows: list[dict[str, object]],
    public_keys: set[str],
) -> list[dict[str, object]]:
    """Return rows whose exact public key is in public_keys."""
    return [
        row
        for row in rows
        if str(row["public_key"]) in public_keys
    ]


def max_or_none(values: list[int]) -> int | None:
    """Return max(values), or None for an empty list."""
    return max(values) if values else None


def min_or_none(values: list[int]) -> int | None:
    """Return min(values), or None for an empty list."""
    return min(values) if values else None


def summary(
    trigger_rows: list[dict[str, object]],
    observed_rows: list[dict[str, object]],
    prior_rows: list[dict[str, object]],
) -> dict[str, object]:
    """Return compact span-36 terminal-lift summary."""
    observed_lanes = {
        str(row["factor_mod180_lane"])
        for row in observed_rows
    }
    observed_public_keys = {
        str(row["public_key"])
        for row in observed_rows
    }
    prior_rows_in_observed_lanes = rows_in_lanes(prior_rows, observed_lanes)
    prior_rows_in_observed_public_keys = rows_in_public_keys(
        prior_rows_in_observed_lanes,
        observed_public_keys,
    )
    prior_lane_lower_twins = lower_twin_rows(prior_rows_in_observed_lanes)
    prior_lane_public_left_31 = public_left_31_rows(prior_rows_in_observed_lanes)
    prior_lane_public_left_31_lower_twins = lower_twin_rows(
        prior_lane_public_left_31
    )
    observed_lower_twins = lower_twin_rows(observed_rows)
    observed_public_left_31 = public_left_31_rows(observed_rows)
    observed_public_left_31_lower_twins = lower_twin_rows(observed_public_left_31)
    return {
        "rule_id": RULE_ID,
        "status": "measured_span36_terminal_lift_probe",
        "theorem_status": "hypothesis_not_proved",
        "trigger_row_count": len(trigger_rows),
        "trigger_span_mod36_counts": count_by(trigger_rows, "span_mod36"),
        "trigger_span36_factor_mod180_lane_counts": count_by(
            [
                row
                for row in trigger_rows
                if row["span_divisible_by_36"]
            ],
            "factor_mod180_lane",
        ),
        "trigger_span36_lower_terminal_lift_rows": conjunction_count(trigger_rows),
        "observed_replacement_row_count": len(observed_rows),
        "observed_span_mod36_counts": count_by(observed_rows, "span_mod36"),
        "observed_factor_mod180_lane_counts": count_by(
            observed_rows,
            "factor_mod180_lane",
        ),
        "observed_public_key_counts": count_by(observed_rows, "public_key"),
        "observed_N_mod60_counts": count_by(observed_rows, "N_mod60"),
        "observed_public_left_mod60_counts": count_by(
            observed_rows,
            "public_left_endpoint_mod60",
        ),
        "observed_public_left31_lower_twin_rows": len(
            observed_public_left_31_lower_twins
        ),
        "observed_lower_twin_rows": len(observed_lower_twins),
        "observed_lower_twin_preceding_gap_min": min_or_none(
            [
                int(row["p_preceding_gap_width"])
                for row in observed_lower_twins
            ]
        ),
        "observed_lower_twin_preceding_gap_counts": count_by(
            observed_lower_twins,
            "p_preceding_gap_width",
        ),
        "observed_lower_twin_open_slot_counts": count_by(
            observed_lower_twins,
            "p_preceding_open_slots",
        ),
        "observed_span36_lower_terminal_lift_rows": conjunction_count(observed_rows),
        "prior_pair_support_row_count": len(prior_rows),
        "prior_span_mod36_counts": count_by(prior_rows, "span_mod36"),
        "prior_rows_in_observed_mod180_lanes": len(prior_rows_in_observed_lanes),
        "prior_observed_mod180_lane_counts": count_by(
            prior_rows_in_observed_lanes,
            "factor_mod180_lane",
        ),
        "prior_observed_lane_observed_public_key_rows": len(
            prior_rows_in_observed_public_keys
        ),
        "prior_observed_lane_observed_public_key_lower_twin_rows": len(
            lower_twin_rows(prior_rows_in_observed_public_keys)
        ),
        "prior_observed_lane_N_mod60_counts": count_by(
            prior_rows_in_observed_lanes,
            "N_mod60",
        ),
        "prior_observed_lane_public_left_mod60_counts": count_by(
            prior_rows_in_observed_lanes,
            "public_left_endpoint_mod60",
        ),
        "prior_observed_lane_public_left31_rows": len(prior_lane_public_left_31),
        "prior_observed_lane_public_left31_lower_twin_rows": len(
            prior_lane_public_left_31_lower_twins
        ),
        "prior_observed_lane_lower_twin_rows": len(prior_lane_lower_twins),
        "prior_observed_lane_lower_twin_preceding_gap_max": max_or_none(
            [
                int(row["p_preceding_gap_width"])
                for row in prior_lane_lower_twins
            ]
        ),
        "prior_observed_lane_lower_twin_preceding_gap_counts": count_by(
            prior_lane_lower_twins,
            "p_preceding_gap_width",
        ),
        "prior_observed_lane_lower_twin_open_slot_counts": count_by(
            prior_lane_lower_twins,
            "p_preceding_open_slots",
        ),
        "prior_observed_lane_lower_terminal_lift_rows": conjunction_count(
            prior_rows_in_observed_lanes
        ),
        "prior_span36_lower_terminal_lift_rows": conjunction_count(prior_rows),
        "sharper_arithmetic_statement": (
            "In the current public o6 residue-bridge surface, the observed "
            "supported prior-absent replacements are exactly the rows with "
            "factor span divisible by 36 and lower-factor terminal-twin lift. "
            "Equivalently, after the mod-30 residue bridge has forced 13|19 "
            "or 19|13, the replacement rows are the rows where the two "
            "factors share the same mod-36 phase and then lift through the "
            "lower terminal twin. The mod-180 lanes alone are not enough: "
            "prior support already occupies the observed lanes, but none of "
            "those prior rows has lower terminal lift. Same-lane prior rows "
            "do contain lower twin distance 2, but only after preceding gaps "
            "with at most two interior wheel-open slots; the observed "
            "replacements have four interior wheel-open slots before the "
            "lower twin. Same-lane prior rows also hit public-left 31 mod 60, "
            "but none of those public-left-31 prior rows has lower twin "
            "distance. More sharply, same-lane prior support has no row with "
            "the exact observed public trigger keys."
        ),
    }


def main() -> int:
    """Run the span-36 terminal-lift probe."""
    trigger_rows = with_span_fields(
        read_jsonl(ORIENTATION_DIR / "trigger_orientation_rows.jsonl")
    )
    observed_rows = with_span_fields(
        read_jsonl(ORIENTATION_DIR / "observed_replacement_rows.jsonl")
    )
    prior_rows = with_span_fields(
        read_jsonl(ORIENTATION_DIR / "prior_support_rows.jsonl")
    )

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    payload = summary(trigger_rows, observed_rows, prior_rows)
    write_json(OUTPUT_DIR / "summary.json", payload)
    write_jsonl(OUTPUT_DIR / "trigger_rows.jsonl", trigger_rows)
    write_jsonl(OUTPUT_DIR / "observed_replacement_rows.jsonl", observed_rows)
    write_jsonl(OUTPUT_DIR / "prior_support_rows.jsonl", prior_rows)
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
