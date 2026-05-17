#!/usr/bin/env python3
"""Round 2 fieldwise separator for exact public trigger rows."""

from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path

from codex_round1_high_signal_probe import (
    EXACT_PUBLIC_TRIGGERS,
    OUTPUT_DIR as ROUND1_OUTPUT_DIR,
    load_rows as load_round1_rows,
)
from first_gap_compatibility_check import write_json, write_jsonl
from slot_factor_public_quotient_test import read_jsonl


THIS_DIR = Path(__file__).resolve().parent
INPUT_ROOT = THIS_DIR / "output"
OUTPUT_DIR = INPUT_ROOT / "codex_round2_public_trigger_separator"
RULE_ID = "pedk_codex_round2_public_trigger_separator_v1"
FIELD_NAMES = (
    "prev_open_offset",
    "prev_d",
    "prev_parity",
    "containing_position",
    "containing_exact_type",
    "next_open_offset",
    "next_open_type",
    "next_d",
    "next_parity",
    "next_reduced_state",
    "public_gwr_side",
    "public_left_endpoint_mod60",
    "public_previous_left_mod30",
    "right_boundary_residues",
    "p_right_residue",
    "q_right_residue",
    "factor_mod180_lane",
    "phase_width_pair",
    "lower_predecessor_residue_width_pair",
    "lower_predecessor_open_slot_count",
)
PROPOSED_PUBLIC_TUPLES = {
    ("even", "mid", "o4"),
    ("odd", "early", "o6"),
}


def corpus_row_index() -> dict[tuple[str, str], dict[str, object]]:
    """Return enriched rows keyed by window and case ID."""
    out = {}
    for directory in sorted(INPUT_ROOT.glob("enriched_multiplication_map_corpus_*")):
        window = directory.name.removeprefix("enriched_multiplication_map_corpus_")
        for row in read_jsonl(directory / "enriched_rows.jsonl"):
            out[(window, str(row["case_id"]))] = row
    return out


def parity_from_exact_type(value: str) -> str:
    """Return final parity token from an exact type key."""
    match = re.search(r"_(even|odd)$", value)
    return match.group(1) if match else "none"


def containing_position(public_word: str) -> str:
    """Return containing phase label from a public word."""
    match = re.search(r"containing=[^|@]+@([^|]+)", public_word)
    if not match:
        raise ValueError(f"cannot parse containing position: {public_word}")
    return match.group(1)


def leading_open_type(reduced_state: str) -> str:
    """Return leading open token from a reduced state."""
    return reduced_state.split("_", 1)[0]


def comparison_fields(
    round1_row: dict[str, object],
    enriched_row: dict[str, object],
) -> dict[str, object]:
    """Return requested comparison columns for one row."""
    previous_gap = enriched_row["public_previous_gap"]
    following_gap = enriched_row["public_following_gap"]
    p_right_residue, q_right_residue = str(round1_row["right_boundary_residues"]).split("|")
    fields = {
        "prev_open_offset": int(previous_gap["first_open_offset"]),
        "prev_d": int(previous_gap["winner_d"]),
        "prev_parity": parity_from_exact_type(str(previous_gap["exact_type_key"])),
        "containing_position": containing_position(str(enriched_row["public_word"])),
        "containing_exact_type": enriched_row["public_containing_exact_type_key"],
        "next_open_offset": int(following_gap["first_open_offset"]),
        "next_open_type": leading_open_type(str(following_gap["reduced_state"])),
        "next_d": int(following_gap["winner_d"]),
        "next_parity": parity_from_exact_type(str(following_gap["exact_type_key"])),
        "next_reduced_state": following_gap["reduced_state"],
        "public_gwr_side": enriched_row["public_gwr_side"],
        "public_left_endpoint_mod60": round1_row["public_left_endpoint_mod60"],
        "public_previous_left_mod30": round1_row["public_previous_left_mod30"],
        "right_boundary_residues": round1_row["right_boundary_residues"],
        "p_right_residue": p_right_residue,
        "q_right_residue": q_right_residue,
        "factor_mod180_lane": round1_row["factor_mod180_lane"],
        "phase_width_pair": round1_row["phase_width_pair"],
        "lower_predecessor_residue_width_pair": round1_row[
            "lower_predecessor_residue_width_pair"
        ],
        "lower_predecessor_open_slot_count": round1_row[
            "lower_predecessor_open_slot_count"
        ],
    }
    fields["proposed_tuple"] = (
        f"{fields['prev_parity']}|{fields['containing_position']}|"
        f"{fields['next_open_type']}"
    )
    fields["proposed_directed_reentry_condition"] = (
        (
            fields["prev_parity"],
            fields["containing_position"],
            fields["next_open_type"],
        )
        in PROPOSED_PUBLIC_TUPLES
        and fields["prev_open_offset"] == 4
        and fields["prev_d"] <= 4
        and fields["next_d"] <= 4
        and fields["public_gwr_side"] == "at_winner"
    )
    return fields


def selected_rows() -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    """Return good exact-trigger rows and seven projection-collision rows."""
    enriched = corpus_row_index()
    good_rows = []
    bad_rows = []
    for row in load_round1_rows():
        key = (str(row["window"]), str(row["case_id"]))
        payload = {
            "rule_id": RULE_ID,
            "class": "",
            "window": row["window"],
            "case_id": row["case_id"],
            "public_key": row["public_key"],
            **comparison_fields(row, enriched[key]),
        }
        is_good = (
            str(row["public_key"]) in EXACT_PUBLIC_TRIGGERS
            and row["rres_o4_o4"]
            and row["phase_width_complement"]
            and row["lower_terminal_four_slot"]
        )
        is_bad = (
            row["full_target_conjunction"]
            and not row["lower_terminal_four_slot"]
        )
        if is_good:
            payload["class"] = "good_exact_trigger"
            good_rows.append(payload)
        if is_bad:
            payload["class"] = "bad_projection_collision"
            bad_rows.append(payload)
    return good_rows, bad_rows


def value_counts(rows: list[dict[str, object]], field: str) -> dict[str, int]:
    """Return JSON-safe value counts for one field."""
    counts = Counter(str(row[field]) for row in rows)
    return {key: counts[key] for key in sorted(counts)}


def field_comparison(
    good_rows: list[dict[str, object]],
    bad_rows: list[dict[str, object]],
) -> dict[str, object]:
    """Return fieldwise common/absent comparison."""
    out = {}
    for field in FIELD_NAMES:
        good_values = {str(row[field]) for row in good_rows}
        bad_values = {str(row[field]) for row in bad_rows}
        out[field] = {
            "good_counts": value_counts(good_rows, field),
            "bad_counts": value_counts(bad_rows, field),
            "common_to_all_good": sorted(good_values) if len(good_values) == 1 else [],
            "good_values_absent_from_bad": sorted(good_values - bad_values),
            "bad_values_absent_from_good": sorted(bad_values - good_values),
        }
    return out


def summary(
    good_rows: list[dict[str, object]],
    bad_rows: list[dict[str, object]],
) -> dict[str, object]:
    """Return compact separator summary."""
    all_rows = good_rows + bad_rows
    proposed_good_hits = [
        row for row in good_rows if row["proposed_directed_reentry_condition"]
    ]
    proposed_bad_hits = [
        row for row in bad_rows if row["proposed_directed_reentry_condition"]
    ]
    tuple_counts = {
        "good": value_counts(good_rows, "proposed_tuple"),
        "bad": value_counts(bad_rows, "proposed_tuple"),
    }
    exact_public_key_separator = sorted({str(row["public_key"]) for row in good_rows})
    return {
        "rule_id": RULE_ID,
        "status": "measured_codex_round2_public_trigger_separator",
        "theorem_status": "hypothesis_not_proved",
        "good_row_count": len(good_rows),
        "bad_row_count": len(bad_rows),
        "proposed_directed_reentry_good_hits": len(proposed_good_hits),
        "proposed_directed_reentry_bad_hits": len(proposed_bad_hits),
        "proposed_directed_reentry_separates_good_from_bad": (
            len(proposed_good_hits) == len(good_rows)
            and not proposed_bad_hits
        ),
        "proposed_tuple_counts": tuple_counts,
        "exact_public_key_separator": exact_public_key_separator,
        "exact_public_key_separator_good_count": sum(
            1 for row in good_rows if str(row["public_key"]) in exact_public_key_separator
        ),
        "exact_public_key_separator_bad_count": sum(
            1 for row in bad_rows if str(row["public_key"]) in exact_public_key_separator
        ),
        "fields_common_to_all_good_absent_from_bad": {
            field: data["common_to_all_good"]
            for field, data in field_comparison(good_rows, bad_rows).items()
            if data["common_to_all_good"]
            and set(data["common_to_all_good"]).isdisjoint(data["bad_counts"])
        },
        "comparison_set_row_count": len(all_rows),
        "round1_output_source": str(ROUND1_OUTPUT_DIR),
    }


def main() -> int:
    """Run the separator comparison."""
    good_rows, bad_rows = selected_rows()
    comparison = field_comparison(good_rows, bad_rows)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    write_jsonl(OUTPUT_DIR / "good_rows.jsonl", good_rows)
    write_jsonl(OUTPUT_DIR / "bad_rows.jsonl", bad_rows)
    write_json(OUTPUT_DIR / "field_comparison.json", comparison)
    payload = summary(good_rows, bad_rows)
    write_json(OUTPUT_DIR / "summary.json", payload)
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
