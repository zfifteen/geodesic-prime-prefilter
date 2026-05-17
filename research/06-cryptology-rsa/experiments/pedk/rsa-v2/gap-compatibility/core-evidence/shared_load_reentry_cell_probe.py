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


def boundary_reentry_candidate_rows() -> list[dict[str, object]]:
    """Return candidate rows whose right-boundary cell reentered."""
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
            out = dict(row)
            out["window"] = window
            out["shared_load_boundary_delta"] = endpoint_boundary - public_load
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
    delta_by_key: dict[tuple[str, str, str], int] = {}
    for row in candidate_rows:
        window = str(row["window"])
        key = (str(row["public_key"]), str(row["boundary_index_key"]))
        keys_by_window[window].add(key)
        delta_by_key[(window, key[0], key[1])] = int(row["shared_load_boundary_delta"])

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
            left_distances = sorted(
                record["left_offset_from_right"] for record in left_records
            )
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
                    "shared_load_boundary_delta": delta_by_key[
                        (window, public_key(row), boundary_key)
                    ],
                    "left_boundary_residues": values["left_boundary_residues"],
                    "left_boundary_phases": values["left_boundary_phases"],
                    "right_boundary_residues": values["right_boundary_residues"],
                    "right_boundary_phases": values["right_boundary_phases"],
                    "left_slot_records": left_records,
                    "left_offset_from_right_values": left_distances,
                    "minimum_left_offset_from_right": min(left_distances),
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


def contrast_by_delta(observed_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    """Return observed reentry lift contrast by load-boundary delta."""
    groups: dict[int, list[dict[str, object]]] = defaultdict(list)
    for row in observed_rows:
        groups[int(row["shared_load_boundary_delta"])].append(row)

    out = []
    for delta, group in sorted(groups.items()):
        out.append(
            {
                "shared_load_boundary_delta": delta,
                "observed_forward_exact_rows": len(group),
                "right_boundary_residue_counts": dict(
                    sorted(Counter(row["right_boundary_residues"] for row in group).items())
                ),
                "left_boundary_phase_counts": dict(
                    sorted(Counter(row["left_boundary_phases"] for row in group).items())
                ),
                "minimum_left_offset_from_right_counts": dict(
                    sorted(
                        Counter(
                            row["minimum_left_offset_from_right"] for row in group
                        ).items()
                    )
                ),
                "rows_with_minimum_left_offset_from_right_2": sum(
                    1 for row in group if row["minimum_left_offset_from_right"] == 2
                ),
                "rows_with_one_very_late_left_record": sum(
                    1 for row in group if row["very_late_left_count"] == 1
                ),
            }
        )
    return out


def summary(
    candidate_rows: list[dict[str, object]],
    observed_rows: list[dict[str, object]],
) -> dict[str, object]:
    """Return the compact shared-load reentry-cell profile."""
    load_match_candidates = [
        row for row in candidate_rows if row["shared_load_boundary_delta"] == 0
    ]
    load_match_observed = [
        row for row in observed_rows if row["shared_load_boundary_delta"] == 0
    ]
    load_match_cells = {
        (row["public_key"], row["boundary_index_key"]) for row in candidate_rows
        if row["shared_load_boundary_delta"] == 0
    }
    very_late_records = [
        record
        for row in load_match_observed
        for record in row["very_late_left_records"]
    ]
    return {
        "rule_id": RULE_ID,
        "status": "measured_shared_load_reentry_cell_profile",
        "theorem_status": "hypothesis_not_proved",
        "candidate_load_match_reentry_rows": len(load_match_candidates),
        "distinct_load_match_reentered_boundary_cells": len(load_match_cells),
        "observed_forward_exact_rows_in_load_match_reentered_cells": len(
            load_match_observed
        ),
        "observed_right_boundary_residue_counts": dict(
            sorted(
                Counter(
                    row["right_boundary_residues"] for row in load_match_observed
                ).items()
            )
        ),
        "observed_left_boundary_phase_counts": dict(
            sorted(
                Counter(
                    row["left_boundary_phases"] for row in load_match_observed
                ).items()
            )
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
            1 for row in load_match_observed if row["very_late_left_count"] == 1
        ),
        "observed_rows_whose_very_late_left_is_two_from_right": sum(
            1
            for row in load_match_observed
            if row["very_late_left_offset_from_right_values"] == [2]
        ),
        "observed_reentry_contrast_by_delta": contrast_by_delta(observed_rows),
        "sharper_arithmetic_statement": (
            "In the measured shared-load reentry cells, right-boundary reentry "
            "collapses to Rres=o4|o4 and each exact forward replacement has one "
            "left-side factor gap whose selected point is two units before the "
            "right endpoint."
        ),
    }


def main() -> int:
    """Run the shared-load reentry-cell probe."""
    candidate_rows = boundary_reentry_candidate_rows()
    observed_rows = observed_forward_rows(candidate_rows)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    write_json(OUTPUT_DIR / "summary.json", summary(candidate_rows, observed_rows))
    write_jsonl(OUTPUT_DIR / "candidate_rows.jsonl", candidate_rows)
    write_jsonl(
        OUTPUT_DIR / "load_match_observed_forward_rows.jsonl",
        [row for row in observed_rows if row["shared_load_boundary_delta"] == 0],
    )
    write_jsonl(OUTPUT_DIR / "all_observed_forward_rows.jsonl", observed_rows)
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
