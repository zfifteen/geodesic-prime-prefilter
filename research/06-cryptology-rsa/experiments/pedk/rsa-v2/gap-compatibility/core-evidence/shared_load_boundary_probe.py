#!/usr/bin/env python3
"""Restate the endpoint balance rule as a shared load-boundary rule."""

from __future__ import annotations

import json
import re
from collections import defaultdict
from pathlib import Path

from first_gap_compatibility_check import write_json, write_jsonl
from joint_endpoint_pair_right_boundary_surface import rate_ppm
from slot_factor_public_quotient_test import read_jsonl


THIS_DIR = Path(__file__).resolve().parent
INPUT_PATH = THIS_DIR / "output" / "public_selected_contrast_probe" / "candidate_rows.jsonl"
OUTPUT_DIR = THIS_DIR / "output" / "shared_load_boundary_probe"
RULE_ID = "pedk_shared_load_boundary_probe_v1"
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


def endpoint_right_boundary(row: dict[str, object]) -> int:
    """Return the maximum first right-open endpoint boundary."""
    residues = str(row["right_boundary_residues"]).split("|")
    return max(RIGHT_RESIDUE_OFFSET[value] for value in residues)


def load_boundary_row(row: dict[str, object]) -> dict[str, object]:
    """Return one candidate row in shared load-boundary coordinates."""
    public_load = public_selected_divisor_count(
        str(row["public_containing_exact_type_key"])
    )
    endpoint_boundary = endpoint_right_boundary(row)
    load_delta = endpoint_boundary - public_load
    endpoint_transport_defect = int(row["endpoint_transport_defect"])
    return {
        "rule_id": RULE_ID,
        "window": row["window"],
        "public_side": row["public_side"],
        "public_key": row["public_key"],
        "public_containing_exact_type_key": row["public_containing_exact_type_key"],
        "pair_identity_key": row["pair_identity_key"],
        "right_boundary_residues": row["right_boundary_residues"],
        "public_selected_divisor_count": public_load,
        "endpoint_right_boundary": endpoint_boundary,
        "shared_load_boundary_delta": load_delta,
        "endpoint_transport_defect": endpoint_transport_defect,
        "load_delta_matches_endpoint_defect": load_delta == 2 * endpoint_transport_defect,
        "endpoint_matches_public_load": endpoint_boundary == public_load,
        "exact_pair_falsified": row["exact_pair_falsified"],
        "status": row["status"],
    }


def status_counts(rows: list[dict[str, object]]) -> dict[str, int | None]:
    """Return exact endpoint-pair falsification counts."""
    testable = [row for row in rows if row["status"] != "not_testable_forward"]
    falsified = [row for row in testable if row["exact_pair_falsified"]]
    return {
        "row_count": len(rows),
        "testable_count": len(testable),
        "survived_count": len(testable) - len(falsified),
        "falsified_count": len(falsified),
        "falsification_rate_ppm": rate_ppm(len(falsified), len(testable)),
    }


def grouped_summary(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    """Return public-side by shared-boundary-delta summary rows."""
    groups: dict[tuple[str, int], list[dict[str, object]]] = defaultdict(list)
    for row in rows:
        groups[(str(row["public_side"]), int(row["shared_load_boundary_delta"]))].append(row)
    out = []
    for (public_side, delta), group in groups.items():
        out.append(
            {
                "rule_id": RULE_ID,
                "public_side": public_side,
                "shared_load_boundary_delta": delta,
                "endpoint_matches_public_load": delta == 0,
                **status_counts(group),
            }
        )
    out.sort(
        key=lambda row: (
            str(row["public_side"]),
            int(row["shared_load_boundary_delta"]),
        )
    )
    return out


def local_summary(rows: list[dict[str, object]], public_axis: str) -> list[dict[str, object]]:
    """Return at-selected local summaries by one public axis."""
    groups: dict[str, list[dict[str, object]]] = defaultdict(list)
    for row in rows:
        if row["public_side"] != "at_winner":
            continue
        groups[str(row[public_axis])].append(row)

    out = []
    for public_value, group in groups.items():
        load_match = [row for row in group if row["endpoint_matches_public_load"]]
        load_mismatch = [row for row in group if not row["endpoint_matches_public_load"]]
        out.append(
            {
                "rule_id": RULE_ID,
                "public_axis": public_axis,
                "public_value": public_value,
                "load_match": status_counts(load_match),
                "load_mismatch": status_counts(load_mismatch),
            }
        )
    out.sort(
        key=lambda row: (
            int(row["load_match"]["falsified_count"]),
            -int(row["load_match"]["testable_count"]),
            str(row["public_value"]),
        )
    )
    return out


def local_summary_index(local_rows: list[dict[str, object]], public_axis: str) -> dict[str, int | str]:
    """Return compact locality counts for one public axis."""
    load_match_testable = [
        row for row in local_rows
        if int(row["load_match"]["testable_count"]) > 0
    ]
    load_match_falsified = [
        row for row in load_match_testable
        if int(row["load_match"]["falsified_count"]) > 0
    ]
    load_mismatch_testable = [
        row for row in local_rows
        if int(row["load_mismatch"]["testable_count"]) > 0
    ]
    load_mismatch_falsified = [
        row for row in load_mismatch_testable
        if int(row["load_mismatch"]["falsified_count"]) > 0
    ]
    return {
        "rule_id": RULE_ID,
        "public_axis": public_axis,
        "public_value_count": len(local_rows),
        "load_match_testable_public_value_count": len(load_match_testable),
        "load_match_falsified_public_value_count": len(load_match_falsified),
        "load_mismatch_testable_public_value_count": len(load_mismatch_testable),
        "load_mismatch_falsified_public_value_count": len(load_mismatch_falsified),
    }


def summary(
    rows: list[dict[str, object]],
    grouped_rows: list[dict[str, object]],
    local_type_rows: list[dict[str, object]],
    local_word_rows: list[dict[str, object]],
) -> dict[str, object]:
    """Return compact shared load-boundary summary."""
    selected = [
        row for row in rows
        if row["public_side"] == "at_winner"
        and row["endpoint_matches_public_load"]
        and row["status"] != "not_testable_forward"
    ]
    falsified = [row for row in selected if row["exact_pair_falsified"]]
    public_loads = sorted({row["public_selected_divisor_count"] for row in rows})
    load_delta_mismatches = [
        row for row in rows if not row["load_delta_matches_endpoint_defect"]
    ]
    return {
        "rule_id": RULE_ID,
        "status": "measured_shared_load_boundary_probe",
        "theorem_status": "hypothesis_not_proved",
        "candidate_row_count": len(rows),
        "public_selected_divisor_counts": public_loads,
        "load_delta_endpoint_defect_mismatch_count": len(load_delta_mismatches),
        "selected_public_and_endpoint_matches_load_count": len(selected),
        "selected_public_and_endpoint_matches_load_falsification_count": len(falsified),
        "selected_public_and_endpoint_matches_load_rate_ppm": rate_ppm(
            len(falsified), len(selected)
        ),
        "grouped_rows": grouped_rows,
        "locality_summary": [
            local_summary_index(local_type_rows, "public_containing_exact_type_key"),
            local_summary_index(local_word_rows, "public_key"),
        ],
        "sharper_arithmetic_statement": (
            "On the active candidate surface, endpoint transport defect zero is exactly "
            "endpoint_right_boundary == public_selected_divisor_count. The signed "
            "load delta equals twice the old endpoint transport defect with zero "
            "mismatches, so the defect language can be replaced by the arithmetic "
            "condition endpoint boundary minus public load equals 0."
        ),
    }


def main() -> int:
    """Run the shared load-boundary probe."""
    rows = [load_boundary_row(row) for row in read_jsonl(INPUT_PATH)]
    groups = grouped_summary(rows)
    local_type_rows = local_summary(rows, "public_containing_exact_type_key")
    local_word_rows = local_summary(rows, "public_key")
    out_summary = summary(rows, groups, local_type_rows, local_word_rows)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    write_json(OUTPUT_DIR / "summary.json", out_summary)
    write_jsonl(OUTPUT_DIR / "shared_load_boundary_rows.jsonl", rows)
    write_jsonl(OUTPUT_DIR / "grouped_rows.jsonl", groups)
    write_jsonl(OUTPUT_DIR / "public_containing_type_rows.jsonl", local_type_rows)
    write_jsonl(OUTPUT_DIR / "public_word_rows.jsonl", local_word_rows)
    write_jsonl(
        OUTPUT_DIR / "load_delta_mismatch_rows.jsonl",
        [row for row in rows if not row["load_delta_matches_endpoint_defect"]],
    )
    print(json.dumps(out_summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
