#!/usr/bin/env python3
"""Audit direct parent-to-child containment for square-tail obstruction words."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from square_tail_obstruction_word import build_payload  # noqa: E402


ROOT = Path(__file__).resolve().parents[3]
DEFAULT_OUTPUT_DIR = ROOT / "research" / "04-bounded-compression" / "output"


def build_parser() -> argparse.ArgumentParser:
    """Build the CLI parser."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--parent-root", type=int, required=True, help="Parent prime root.")
    parser.add_argument("--child-root", type=int, required=True, help="Projected child root.")
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Optional JSON output path.",
    )
    return parser


def build_audit(parent_root: int, child_root: int) -> dict[str, object]:
    """Return the direct recursive-containment audit for one parent and child."""
    parent = build_payload(parent_root)
    child = build_payload(child_root)

    parent_rows = list(parent["obstruction_rows"])
    child_rows = list(child["obstruction_rows"])
    parent_factors = {int(row["least_factor"]) for row in parent_rows}
    child_factors = {int(row["least_factor"]) for row in child_rows}
    parent_child_rows = [
        row for row in parent_rows if int(row["least_factor"]) == child_root
    ]

    child_factor_subset = child_factors.issubset(parent_factors)
    child_occurrence_count = len(parent_child_rows)
    child_prefix_count = int(child["obstruction_prefix_even_count"])
    child_full_count = int(child["full_counterexample_even_count"])

    return {
        "parent_root": parent_root,
        "child_root": child_root,
        "parent_previous_prime_offset": parent["previous_prime_offset"],
        "parent_dynamic_cutoff": parent["dynamic_cutoff"],
        "parent_obstruction_prefix_even_count": parent[
            "obstruction_prefix_even_count"
        ],
        "parent_full_counterexample_even_count": parent[
            "full_counterexample_even_count"
        ],
        "child_previous_prime_offset": child["previous_prime_offset"],
        "child_dynamic_cutoff": child["dynamic_cutoff"],
        "child_closed_by_cutoff": child["closed_by_cutoff"],
        "child_selected_square_condition": child["selected_square_condition"],
        "child_obstruction_prefix_even_count": child_prefix_count,
        "child_full_counterexample_even_count": child_full_count,
        "child_root_occurs_in_parent_word": child_root in parent_factors,
        "parent_child_occurrence_count": child_occurrence_count,
        "parent_child_occurrence_offsets": [
            int(row["offset"]) for row in parent_child_rows
        ],
        "child_distinct_least_factor_count": len(child_factors),
        "child_word_factors_subset_of_parent_word": child_factor_subset,
        "missing_child_factors_from_parent_word": sorted(child_factors - parent_factors),
        "parent_child_occurrences_cover_child_prefix": (
            child_occurrence_count >= child_prefix_count
        ),
        "parent_child_occurrences_cover_child_full_word": (
            child_occurrence_count >= child_full_count
        ),
        "direct_recursive_containment_holds": (
            child_factor_subset
            and child_occurrence_count >= child_prefix_count
        ),
    }


def main(argv: list[str] | None = None) -> int:
    """Run the direct recursive-containment audit."""
    args = build_parser().parse_args(argv)
    payload = build_audit(args.parent_root, args.child_root)
    serialized = json.dumps(payload, indent=2)
    if args.output is not None:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(serialized + "\n", encoding="utf-8")
    print(serialized)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
