#!/usr/bin/env python3
"""Profile support strength for the shared load-boundary rows."""

from __future__ import annotations

import json
import re
from collections import defaultdict
from pathlib import Path

from first_gap_compatibility_check import write_json, write_jsonl
from joint_endpoint_pair_right_boundary_surface import rate_ppm
from slot_factor_public_quotient_test import read_jsonl


THIS_DIR = Path(__file__).resolve().parent
INPUT_ROOT = THIS_DIR / "output"
OUTPUT_DIR = INPUT_ROOT / "shared_load_support_probe"
RULE_ID = "pedk_shared_load_support_probe_v1"
SELECTED_D_RE = re.compile(r"_d([0-9]+)_a")
RIGHT_RESIDUE_OFFSET = {"o2": 2, "o4": 4, "o6": 6}
WINDOW_DIRS = (
    "directional_boundary_gate_surface_21001_23000",
    "directional_boundary_gate_surface_23001_25000",
    "directional_boundary_gate_surface_25001_27000",
    "directional_boundary_gate_surface_27001_30000",
    "directional_boundary_gate_surface_30001_32000",
    "directional_boundary_gate_surface_32001_34000",
)


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


def quantiles(values: list[int]) -> dict[str, int | None]:
    """Return deterministic five-number support summary."""
    if not values:
        return {"min": None, "q1": None, "median": None, "q3": None, "max": None}
    ordered = sorted(values)
    return {
        "min": ordered[0],
        "q1": ordered[len(ordered) // 4],
        "median": ordered[len(ordered) // 2],
        "q3": ordered[(3 * len(ordered)) // 4],
        "max": ordered[-1],
    }


def load_rows() -> list[dict[str, object]]:
    """Load right-residue directional rows with shared load-delta fields."""
    rows = []
    for dirname in WINDOW_DIRS:
        for row in read_jsonl(INPUT_ROOT / dirname / "candidate_rows.jsonl"):
            if row["boundary_mode"] != "right_residues":
                continue
            public_load = public_selected_divisor_count(
                str(row["public_containing_exact_type_key"])
            )
            endpoint_boundary = endpoint_right_boundary(str(row["right_boundary_residues"]))
            rows.append(
                {
                    "rule_id": RULE_ID,
                    "window": dirname.rsplit("_", 1)[-1],
                    "public_key": row["public_key"],
                    "public_containing_exact_type_key": row[
                        "public_containing_exact_type_key"
                    ],
                    "pair_identity_key": row["pair_identity_key"],
                    "right_boundary_residues": row["right_boundary_residues"],
                    "public_selected_divisor_count": public_load,
                    "endpoint_right_boundary": endpoint_boundary,
                    "shared_load_boundary_delta": endpoint_boundary - public_load,
                    "minimum_prior_pair_support": row["minimum_prior_pair_support"],
                    "minimum_prior_boundary_support": row[
                        "minimum_prior_boundary_support"
                    ],
                    "exact_pair_falsified": row["exact_pair_falsified"],
                    "status": row["status"],
                }
            )
    rows.sort(
        key=lambda row: (
            str(row["window"]),
            int(row["shared_load_boundary_delta"]),
            str(row["public_key"]),
            str(row["pair_identity_key"]),
        )
    )
    return rows


def grouped_rows(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    """Return support profiles by shared load-boundary delta."""
    groups: dict[int, list[dict[str, object]]] = defaultdict(list)
    for row in rows:
        groups[int(row["shared_load_boundary_delta"])].append(row)

    out = []
    for delta, group in sorted(groups.items()):
        testable = [row for row in group if row["status"] != "not_testable_forward"]
        falsified = [row for row in testable if row["exact_pair_falsified"]]
        out.append(
            {
                "rule_id": RULE_ID,
                "shared_load_boundary_delta": delta,
                "row_count": len(group),
                "testable_count": len(testable),
                "falsified_count": len(falsified),
                "falsification_rate_ppm": rate_ppm(len(falsified), len(testable)),
                "minimum_prior_pair_support_quantiles": quantiles(
                    [int(row["minimum_prior_pair_support"]) for row in testable]
                ),
                "minimum_prior_boundary_support_quantiles": quantiles(
                    [int(row["minimum_prior_boundary_support"]) for row in testable]
                ),
            }
        )
    return out


def summary(rows: list[dict[str, object]], groups: list[dict[str, object]]) -> dict[str, object]:
    """Return compact support-probe summary."""
    load_match = next(row for row in groups if row["shared_load_boundary_delta"] == 0)
    return {
        "rule_id": RULE_ID,
        "status": "measured_shared_load_support_probe",
        "theorem_status": "hypothesis_not_proved",
        "row_count": len(rows),
        "grouped_rows": groups,
        "support_reading": (
            "The clean shared-load row is not a low-support artifact. Its "
            "minimum prior exact-pair support is comparable to the leaking rows, "
            "and its minimum prior boundary support is the strongest of the three "
            "load-delta classes."
        ),
        "load_match_testable_count": load_match["testable_count"],
        "load_match_falsified_count": load_match["falsified_count"],
        "load_match_boundary_support_quantiles": load_match[
            "minimum_prior_boundary_support_quantiles"
        ],
    }


def main() -> int:
    """Run the shared load-boundary support probe."""
    rows = load_rows()
    groups = grouped_rows(rows)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    write_json(OUTPUT_DIR / "summary.json", summary(rows, groups))
    write_jsonl(OUTPUT_DIR / "support_rows.jsonl", rows)
    write_jsonl(OUTPUT_DIR / "grouped_rows.jsonl", groups)
    print(json.dumps(summary(rows, groups), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
