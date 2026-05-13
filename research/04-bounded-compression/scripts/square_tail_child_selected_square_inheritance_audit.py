#!/usr/bin/env python3
"""Audit selected-square status of rough-defect child roots."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import gmpy2


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from square_tail_dynamic_tail_descent_audit import build_dynamic_tail_descent_audit  # noqa: E402
from square_tail_full_cutoff_crt_model import build_full_cutoff_crt_model  # noqa: E402
from square_tail_rough_defect_audit import build_rough_defect_audit  # noqa: E402


ROOT = Path(__file__).resolve().parents[3]
RECORD_ROOT = 424_171_123
REPRESENTATIVE_SOURCE_ROOT = 509


def build_parser() -> argparse.ArgumentParser:
    """Build the CLI parser."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=None)
    return parser


def selected_square_status(root: int) -> dict[str, object]:
    """Return selected-square status for one prime root."""
    previous_root = int(gmpy2.prev_prime(root)) if root > 3 else 2
    square = root * root
    previous_prime = int(gmpy2.prev_prime(square))
    return {
        "root": root,
        "previous_root": previous_root,
        "previous_prime_offset": square - previous_prime,
        "selected_square_condition": previous_root * previous_root < previous_prime < square,
    }


def summarize_child_roots(label: str, roots: list[int]) -> dict[str, object]:
    """Summarize selected-square status over child roots."""
    rows = [selected_square_status(root) for root in roots]
    not_selected = [row for row in rows if not bool(row["selected_square_condition"])]
    return {
        "label": label,
        "child_root_count": len(rows),
        "selected_square_child_count": len(rows) - len(not_selected),
        "not_selected_square_child_count": len(not_selected),
        "first_child_roots": roots[:20],
        "first_not_selected_square_child_roots": [
            int(row["root"]) for row in not_selected[:20]
        ],
    }


def record_composite_child_roots() -> list[int]:
    """Return composite rough-defect least-factor children for the standing record."""
    audit = build_rough_defect_audit(RECORD_ROOT)
    return [
        int(row["least_factor"])
        for row in audit["rough_rows"]
        if not bool(row["is_prime"])
    ]


def representative_composite_child_roots() -> list[int]:
    """Return composite rough-tail least-factor children for the representative."""
    audit = build_dynamic_tail_descent_audit(REPRESENTATIVE_SOURCE_ROOT)
    return [
        int(row["least_factor"])
        for row in audit["rough_tail_rows"]
        if not bool(row["is_prime"])
    ]


def model_carrier_child_roots() -> list[int]:
    """Return the assigned singleton carriers in the full-cutoff CRT model."""
    model = build_full_cutoff_crt_model(REPRESENTATIVE_SOURCE_ROOT)
    return [int(row["carrier"]) for row in model["carrier_rows"]]


def build_child_selected_square_inheritance_audit() -> dict[str, object]:
    """Return the selected-square child inheritance audit."""
    record_children = record_composite_child_roots()
    representative_children = representative_composite_child_roots()
    model_children = model_carrier_child_roots()
    summaries = [
        summarize_child_roots("standing_record_actual_composite_rough_children", record_children),
        summarize_child_roots(
            "representative_actual_composite_rough_tail_children",
            representative_children,
        ),
        summarize_child_roots(
            "full_cutoff_crt_model_assigned_singleton_carriers",
            model_children,
        ),
    ]
    return {
        "standing_record_root": RECORD_ROOT,
        "representative_source_root": REPRESENTATIVE_SOURCE_ROOT,
        "all_groups_have_only_selected_square_children": all(
            int(summary["not_selected_square_child_count"]) == 0 for summary in summaries
        ),
        "boundary": (
            "child selected-square status is present in actual descent and in the "
            "local CRT singleton-carrier model, so it is not the missing transport law"
        ),
        "summaries": summaries,
    }


def main(argv: list[str] | None = None) -> int:
    """Run the child selected-square inheritance audit."""
    args = build_parser().parse_args(argv)
    payload = build_child_selected_square_inheritance_audit()
    serialized = json.dumps(payload, indent=2)
    if args.output is not None:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(serialized + "\n", encoding="utf-8")
    print(serialized)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
