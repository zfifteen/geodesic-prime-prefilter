#!/usr/bin/env python3
"""Profile the exact forward cells behind shared-load boundary reentry."""

from __future__ import annotations

import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

from first_gap_compatibility_check import write_json, write_jsonl
from slot_factor_public_quotient_test import read_jsonl


THIS_DIR = Path(__file__).resolve().parent
if str(THIS_DIR) not in sys.path:
    sys.path.insert(0, str(THIS_DIR))

from directional_boundary_gate_surface import (  # noqa: E402
    boundary_index_from_pair_key,
    boundary_values,
)
from joint_endpoint_pair_right_boundary_surface import (  # noqa: E402
    pair_identity_key,
    public_key,
)


INPUT_ROOT = THIS_DIR / "output"
OUTPUT_DIR = INPUT_ROOT / "shared_load_reentry_cell_probe"
RULE_ID = "pedk_shared_load_reentry_cell_probe_v1"
SELECTED_D_RE = re.compile(r"_d([0-9]+)_a")
RIGHT_RESIDUE_OFFSET = {"o2": 2, "o4": 4, "o6": 6}


def public_selected_divisor_count(public_containing_exact_type_key: str) -> int:
    """Return the selected divisor count encoded in a containing type key."""
    match = SELECTED_D_RE.search(public_containing_exact_type_key)
    if not match:
        raise ValueError(
            f"cannot parse selected divisor count: {public_containing_exact_type_key}"
        )
    return int(match.group(1))


def endpoint_right_boundary(right_boundary_residues: str) -> int:
    """Return the maximum first right-open endpoint boundary."""
    return max(RIGHT_RESIDUE_OFFSET[value] for value in right_boundary_residues.split("|"))


def shared_load_candidate_rows() -> list[dict[str, object]]:
    """Return load-match candidate rows whose right-boundary cell reentered."""
    rows = []
    for candidate_path in sorted(
        INPUT_ROOT.glob("directional_boundary_gate_surface_*/candidate_rows.jsonl")
    ):
        window = candidate_path.parent.name.replace("directional_boundary_gate_surface_", "")
        for row in read_jsonl(candidate_path):
            if row["boundary_mode"] != "right_residues":
                continue
            if row["status"] == "not_testable_forward":
                continue
            if not row["boundary_index_falsified"]:
                continue
            public_load = public_selected_divisor_count(
                str(row["public_containing_exact_type_key"])
            )
            endpoint_boundary = endpoint_right_boundary(str(row["right_boundary_residues"]))
            if endpoint_boundary != public_load:
                continue
            out = dict(row)
            out["window"] = window
            rows.append(out)
    rows.sort(
        key=lambda row: (
            str(row["window"]),
            str(row["public_key"]),
            str(row["pair_identity_key"]),
        )
    )
    return rows


def left_slot_records(row: dict[str, object]) -> list[dict[str, object]]:
    """Return concrete left-side gap records for p and q."""
    records = []
    for side in ("p", "q"):
        offset = int(row[f"{side}_left_winner_offset"])
        width = int(row[f"{side}_left_gap_width"])
        records.append(
            {
                "side": side,
                "left_exact_type_key": row[f"{side}_left_exact_type_key"],
                "left_reduced_state": row[f"{side}_left_reduced_state"],
                "left_winner_offset": offset,
                "left_gap_width": width,
                "left_offset_from_right": width - offset,
                "left_phase": row[f"{side}_left_winner_phase"],
                "right_exact_type_key": row[f"{side}_right_exact_type_key"],
                "right_winner_offset": row[f"{side}_right_winner_offset"],
                "right_gap_width": row[f"{side}_right_gap_width"],
                "right_phase": row[f"{side}_right_winner_phase"],
            }
        )
    return records


def observed_forward_rows(
    candidate_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    """Return exact forward rows occupying the reentered load-match boundary cells."""
    keys_by_window: dict[str, set[tuple[str, str]]] = defaultdict(set)
    for row in candidate_rows:
        keys_by_window[str(row["window"])].add(
            (str(row["public_key"]), str(row["boundary_index_key"]))
        )

    rows = []
    for window, keys in sorted(keys_by_window.items()):
        forward_path = INPUT_ROOT / f"enriched_multiplication_map_corpus_{window}"
        for row in read_jsonl(forward_path / "enriched_rows.jsonl"):
            if row["public_gwr_side"] != "at_winner":
                continue
            pair_key = pair_identity_key(row)
            boundary_key = boundary_index_from_pair_key(pair_key, "right_residues")
            if (public_key(row), boundary_key) not in keys:
                continue
            values = boundary_values(pair_key)
            left_records = left_slot_records(row)
            very_late_left_records = [
                record for record in left_records if record["left_phase"] == "very_late"
            ]
            rows.append(
                {
                    "rule_id": RULE_ID,
                    "window": window,
                    "case_id": row["case_id"],
                    "public_key": public_key(row),
                    "public_containing_exact_type_key": row[
                        "public_containing_exact_type_key"
                    ],
                    "pair_identity_key": pair_key,
                    "boundary_index_key": boundary_key,
                    "left_boundary_residues": values["left_boundary_residues"],
                    "left_boundary_phases": values["left_boundary_phases"],
                    "right_boundary_residues": values["right_boundary_residues"],
                    "right_boundary_phases": values["right_boundary_phases"],
                    "left_slot_records": left_records,
                    "very_late_left_records": very_late_left_records,
                    "very_late_left_count": len(very_late_left_records),
                    "very_late_left_offset_from_right_values": sorted(
                        record["left_offset_from_right"]
                        for record in very_late_left_records
                    ),
                }
            )
    rows.sort(
        key=lambda row: (
            str(row["window"]),
            str(row["public_key"]),
            str(row["pair_identity_key"]),
        )
    )
    return rows


def summary(
    candidate_rows: list[dict[str, object]],
    observed_rows: list[dict[str, object]],
) -> dict[str, object]:
    """Return the compact shared-load reentry-cell profile."""
    candidate_cells = {
        (row["public_key"], row["boundary_index_key"]) for row in candidate_rows
    }
    very_late_records = [
        record
        for row in observed_rows
        for record in row["very_late_left_records"]
    ]
    return {
        "rule_id": RULE_ID,
        "status": "measured_shared_load_reentry_cell_profile",
        "theorem_status": "hypothesis_not_proved",
        "candidate_load_match_reentry_rows": len(candidate_rows),
        "distinct_reentered_boundary_cells": len(candidate_cells),
        "observed_forward_exact_rows_in_reentered_cells": len(observed_rows),
        "observed_right_boundary_residue_counts": dict(
            sorted(Counter(row["right_boundary_residues"] for row in observed_rows).items())
        ),
        "observed_left_boundary_phase_counts": dict(
            sorted(Counter(row["left_boundary_phases"] for row in observed_rows).items())
        ),
        "observed_very_late_left_record_count": len(very_late_records),
        "observed_very_late_left_offset_from_right_counts": dict(
            sorted(
                Counter(
                    record["left_offset_from_right"] for record in very_late_records
                ).items()
            )
        ),
        "observed_rows_with_one_very_late_left_record": sum(
            1 for row in observed_rows if row["very_late_left_count"] == 1
        ),
        "observed_rows_whose_very_late_left_is_two_from_right": sum(
            1
            for row in observed_rows
            if row["very_late_left_offset_from_right_values"] == [2]
        ),
        "sharper_arithmetic_statement": (
            "In the measured shared-load reentry cells, right-boundary reentry "
            "collapses to Rres=o4|o4 and each exact forward replacement has one "
            "left-side factor gap whose selected point is two units before the "
            "right endpoint."
        ),
    }


def main() -> int:
    """Run the shared-load reentry-cell probe."""
    candidate_rows = shared_load_candidate_rows()
    observed_rows = observed_forward_rows(candidate_rows)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    write_json(OUTPUT_DIR / "summary.json", summary(candidate_rows, observed_rows))
    write_jsonl(OUTPUT_DIR / "candidate_rows.jsonl", candidate_rows)
    write_jsonl(OUTPUT_DIR / "observed_forward_rows.jsonl", observed_rows)
    print(
        json.dumps(
            summary(candidate_rows, observed_rows),
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
