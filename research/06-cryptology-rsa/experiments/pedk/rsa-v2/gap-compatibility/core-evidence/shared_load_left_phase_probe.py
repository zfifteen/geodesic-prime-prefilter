#!/usr/bin/env python3
"""Probe left-phase obstruction inside shared-load right-boundary reentry."""

from __future__ import annotations

import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

from first_gap_compatibility_check import write_json, write_jsonl
from joint_endpoint_pair_right_boundary_surface import (
    pair_identity_key,
    public_key,
    rate_ppm,
)
from slot_factor_public_quotient_test import read_jsonl


THIS_DIR = Path(__file__).resolve().parent
if str(THIS_DIR) not in sys.path:
    sys.path.insert(0, str(THIS_DIR))

from directional_boundary_gate_surface import (  # noqa: E402
    boundary_index_from_pair_key,
    boundary_values,
)


INPUT_ROOT = THIS_DIR / "output"
OUTPUT_DIR = INPUT_ROOT / "shared_load_left_phase_probe"
RULE_ID = "pedk_shared_load_left_phase_probe_v1"
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


def forward_boundary_map(forward_dir: Path) -> dict[tuple[str, str], list[dict[str, str]]]:
    """Return observed forward exact pairs by public key and right-residue boundary."""
    out: dict[tuple[str, str], list[dict[str, str]]] = defaultdict(list)
    for row in read_jsonl(forward_dir / "enriched_rows.jsonl"):
        if row["public_gwr_side"] != "at_winner":
            continue
        pair_key = pair_identity_key(row)
        boundary_key = boundary_index_from_pair_key(pair_key, "right_residues")
        values = boundary_values(pair_key)
        out[(public_key(row), boundary_key)].append(
            {
                "pair_identity_key": pair_key,
                "left_boundary_residues": values["left_boundary_residues"],
                "left_boundary_phases": values["left_boundary_phases"],
            }
        )
    return out


def load_rows() -> list[dict[str, object]]:
    """Load boundary-reentry rows and compare old exact pairs with forward pairs."""
    rows = []
    for candidate_path in sorted(
        INPUT_ROOT.glob("directional_boundary_gate_surface_*/candidate_rows.jsonl")
    ):
        surface_name = candidate_path.parent.name
        window = surface_name.replace("directional_boundary_gate_surface_", "")
        forward_dir = INPUT_ROOT / f"enriched_multiplication_map_corpus_{window}"
        forward_map = forward_boundary_map(forward_dir)
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
            values = boundary_values(str(row["pair_identity_key"]))
            observed = forward_map[(str(row["public_key"]), str(row["boundary_index_key"]))]
            left_residue_reappears = any(
                item["left_boundary_residues"] == values["left_boundary_residues"]
                for item in observed
            )
            left_phase_reappears = any(
                item["left_boundary_phases"] == values["left_boundary_phases"]
                for item in observed
            )
            exact_pair_reappears = any(
                item["pair_identity_key"] == row["pair_identity_key"]
                for item in observed
            )
            rows.append(
                {
                    "rule_id": RULE_ID,
                    "window": window,
                    "public_key": row["public_key"],
                    "public_containing_exact_type_key": row[
                        "public_containing_exact_type_key"
                    ],
                    "pair_identity_key": row["pair_identity_key"],
                    "boundary_index_key": row["boundary_index_key"],
                    "right_boundary_residues": row["right_boundary_residues"],
                    "left_boundary_residues": values["left_boundary_residues"],
                    "left_boundary_phases": values["left_boundary_phases"],
                    "public_selected_divisor_count": public_load,
                    "endpoint_right_boundary": endpoint_boundary,
                    "shared_load_boundary_delta": endpoint_boundary - public_load,
                    "forward_observed_pair_count_in_boundary": len(observed),
                    "left_residue_reappears": left_residue_reappears,
                    "left_phase_reappears": left_phase_reappears,
                    "exact_pair_reappears": exact_pair_reappears,
                }
            )
    rows.sort(
        key=lambda row: (
            int(row["shared_load_boundary_delta"]),
            str(row["window"]),
            str(row["public_key"]),
            str(row["pair_identity_key"]),
        )
    )
    return rows


def grouped_rows(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    """Return reappearance counts by shared load-boundary delta."""
    groups: dict[int, list[dict[str, object]]] = defaultdict(list)
    for row in rows:
        groups[int(row["shared_load_boundary_delta"])].append(row)

    out = []
    for delta, group in sorted(groups.items()):
        left_residue = [row for row in group if row["left_residue_reappears"]]
        left_phase = [row for row in group if row["left_phase_reappears"]]
        exact = [row for row in group if row["exact_pair_reappears"]]
        out.append(
            {
                "rule_id": RULE_ID,
                "shared_load_boundary_delta": delta,
                "boundary_reentry_rows": len(group),
                "left_residue_reappears": len(left_residue),
                "left_phase_reappears": len(left_phase),
                "exact_pair_reappears": len(exact),
                "left_phase_reappearance_rate_ppm": rate_ppm(
                    len(left_phase), len(group)
                ),
                "exact_pair_reappearance_rate_ppm": rate_ppm(len(exact), len(group)),
            }
        )
    return out


def summary(rows: list[dict[str, object]], groups: list[dict[str, object]]) -> dict[str, object]:
    """Return compact left-phase obstruction summary."""
    load_match = next(row for row in groups if row["shared_load_boundary_delta"] == 0)
    return {
        "rule_id": RULE_ID,
        "status": "measured_shared_load_left_phase_probe",
        "theorem_status": "hypothesis_not_proved",
        "boundary_reentry_row_count": len(rows),
        "grouped_rows": groups,
        "load_match_boundary_reentry_rows": load_match["boundary_reentry_rows"],
        "load_match_left_residue_reappears": load_match["left_residue_reappears"],
        "load_match_left_phase_reappears": load_match["left_phase_reappears"],
        "load_match_exact_pair_reappears": load_match["exact_pair_reappears"],
        "sharper_arithmetic_statement": (
            "Under shared load equality, right-boundary reentry can preserve coarse "
            "left residues, but it never preserves the left phase arrangement of the "
            "previously absent exact endpoint pair. Off-load rows do allow left-phase "
            "reentry, and exact reentry occurs only there."
        ),
    }


def main() -> int:
    """Run the shared load left-phase obstruction probe."""
    rows = load_rows()
    groups = grouped_rows(rows)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    write_json(OUTPUT_DIR / "summary.json", summary(rows, groups))
    write_jsonl(OUTPUT_DIR / "left_phase_rows.jsonl", rows)
    write_jsonl(OUTPUT_DIR / "grouped_rows.jsonl", groups)
    print(json.dumps(summary(rows, groups), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
