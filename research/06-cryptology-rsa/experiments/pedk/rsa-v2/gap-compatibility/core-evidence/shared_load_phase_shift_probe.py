#!/usr/bin/env python3
"""Probe the phase shift behind shared-load blocked exact reentry."""

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
OUTPUT_DIR = INPUT_ROOT / "shared_load_phase_shift_probe"
RULE_ID = "pedk_shared_load_phase_shift_probe_v1"
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


def has_very_late(phase_pair: str) -> bool:
    """Return whether a sorted phase pair contains very_late."""
    return "very_late" in phase_pair.split("|")


def forward_phase_map(forward_dir: Path) -> dict[tuple[str, str], set[str]]:
    """Return observed forward left-phase pairs by public key and right boundary."""
    out: dict[tuple[str, str], set[str]] = defaultdict(set)
    for row in read_jsonl(forward_dir / "enriched_rows.jsonl"):
        if row["public_gwr_side"] != "at_winner":
            continue
        pair_key = pair_identity_key(row)
        boundary_key = boundary_index_from_pair_key(pair_key, "right_residues")
        values = boundary_values(pair_key)
        out[(public_key(row), boundary_key)].add(values["left_boundary_phases"])
    return out


def load_rows() -> list[dict[str, object]]:
    """Load shared-load boundary reentries with candidate and forward phases."""
    rows = []
    for candidate_path in sorted(
        INPUT_ROOT.glob("directional_boundary_gate_surface_*/candidate_rows.jsonl")
    ):
        window = candidate_path.parent.name.replace("directional_boundary_gate_surface_", "")
        forward_dir = INPUT_ROOT / f"enriched_multiplication_map_corpus_{window}"
        phase_map = forward_phase_map(forward_dir)
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
            load_delta = endpoint_boundary - public_load
            candidate_phases = boundary_values(str(row["pair_identity_key"]))[
                "left_boundary_phases"
            ]
            observed_phases = sorted(
                phase_map[(str(row["public_key"]), str(row["boundary_index_key"]))]
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
                    "shared_load_boundary_delta": load_delta,
                    "candidate_left_phases": candidate_phases,
                    "candidate_left_has_very_late": has_very_late(candidate_phases),
                    "observed_left_phase_values": observed_phases,
                    "observed_left_phase_value_count": len(observed_phases),
                    "all_observed_left_phases_have_very_late": all(
                        has_very_late(value) for value in observed_phases
                    ),
                    "candidate_left_phase_reappears": candidate_phases in observed_phases,
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
    """Return phase-shift counts by shared load-boundary delta."""
    groups: dict[int, list[dict[str, object]]] = defaultdict(list)
    for row in rows:
        groups[int(row["shared_load_boundary_delta"])].append(row)

    out = []
    for delta, group in sorted(groups.items()):
        candidate_very_late = [
            row for row in group if row["candidate_left_has_very_late"]
        ]
        observed_all_very_late = [
            row for row in group if row["all_observed_left_phases_have_very_late"]
        ]
        phase_reappears = [
            row for row in group if row["candidate_left_phase_reappears"]
        ]
        observed_values = Counter(
            value
            for row in group
            for value in row["observed_left_phase_values"]
        )
        candidate_values = Counter(str(row["candidate_left_phases"]) for row in group)
        out.append(
            {
                "rule_id": RULE_ID,
                "shared_load_boundary_delta": delta,
                "boundary_reentry_rows": len(group),
                "candidate_left_has_very_late_count": len(candidate_very_late),
                "all_observed_left_phases_have_very_late_count": len(
                    observed_all_very_late
                ),
                "candidate_left_phase_reappears_count": len(phase_reappears),
                "candidate_left_phase_counts": dict(sorted(candidate_values.items())),
                "observed_left_phase_counts": dict(sorted(observed_values.items())),
            }
        )
    return out


def summary(rows: list[dict[str, object]], groups: list[dict[str, object]]) -> dict[str, object]:
    """Return compact phase-shift summary."""
    load_match = next(row for row in groups if row["shared_load_boundary_delta"] == 0)
    return {
        "rule_id": RULE_ID,
        "status": "measured_shared_load_phase_shift_probe",
        "theorem_status": "hypothesis_not_proved",
        "boundary_reentry_row_count": len(rows),
        "grouped_rows": groups,
        "load_match_boundary_reentry_rows": load_match["boundary_reentry_rows"],
        "load_match_candidate_left_has_very_late_count": load_match[
            "candidate_left_has_very_late_count"
        ],
        "load_match_all_observed_left_phases_have_very_late_count": load_match[
            "all_observed_left_phases_have_very_late_count"
        ],
        "load_match_candidate_left_phase_reappears_count": load_match[
            "candidate_left_phase_reappears_count"
        ],
        "sharper_arithmetic_statement": (
            "Under shared load equality, the blocked lift is a phase shift: the "
            "previously absent candidate left phase avoids very_late, while every "
            "observed left phase in the reentered right-boundary cell contains "
            "very_late."
        ),
    }


def main() -> int:
    """Run the shared load phase-shift probe."""
    rows = load_rows()
    groups = grouped_rows(rows)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    write_json(OUTPUT_DIR / "summary.json", summary(rows, groups))
    write_jsonl(OUTPUT_DIR / "phase_shift_rows.jsonl", rows)
    write_jsonl(OUTPUT_DIR / "grouped_rows.jsonl", groups)
    print(json.dumps(summary(rows, groups), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
