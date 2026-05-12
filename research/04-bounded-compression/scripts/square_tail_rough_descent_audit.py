#!/usr/bin/env python3
"""Audit rough-defect descent through composite least-factor children."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from square_tail_rough_defect_audit import build_rough_defect_audit  # noqa: E402


ROOT = Path(__file__).resolve().parents[3]
DEFAULT_OUTPUT_DIR = ROOT / "research" / "04-bounded-compression" / "output"


def build_parser() -> argparse.ArgumentParser:
    """Build the CLI parser."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=int, required=True, help="Parent prime root.")
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Optional JSON output path.",
    )
    return parser


def child_summary(root: int) -> dict[str, object]:
    """Return the rough-defect summary for one child root."""
    payload = build_rough_defect_audit(root)
    return {
        "root": root,
        "M": payload["full_counterexample_even_count"],
        "rough_defect_count": payload["rough_defect_count"],
        "rough_prime_defect_count": payload["rough_prime_defect_count"],
        "rough_prime_defect_offsets": payload["rough_prime_defect_offsets"],
        "rough_composite_defect_count": payload["rough_composite_defect_count"],
        "closed_by_rough_prime_defect": payload["closed_by_rough_prime_defect"],
    }


def build_descent_audit(root: int) -> dict[str, object]:
    """Return the rough-defect descent audit for one parent root."""
    parent = build_rough_defect_audit(root)
    child_roots = sorted(set(int(factor) for factor in parent["rough_composite_least_factors"]))
    child_rows = [child_summary(child) for child in child_roots]
    open_rows = [
        row for row in child_rows if not bool(row["closed_by_rough_prime_defect"])
    ]

    return {
        "root": root,
        "parent_M": parent["full_counterexample_even_count"],
        "parent_rough_defect_count": parent["rough_defect_count"],
        "parent_rough_prime_defect_count": parent["rough_prime_defect_count"],
        "parent_rough_composite_defect_count": parent["rough_composite_defect_count"],
        "child_count": len(child_rows),
        "all_child_roots_strictly_decrease": all(child < root for child in child_roots),
        "all_children_closed_by_rough_prime_defect": not open_rows,
        "open_child_roots": [int(row["root"]) for row in open_rows],
        "max_child_M_row": max(child_rows, key=lambda row: int(row["M"])) if child_rows else None,
        "max_child_rough_defect_row": (
            max(child_rows, key=lambda row: int(row["rough_defect_count"]))
            if child_rows
            else None
        ),
        "child_rows": child_rows,
    }


def main(argv: list[str] | None = None) -> int:
    """Run the rough-defect descent audit."""
    args = build_parser().parse_args(argv)
    payload = build_descent_audit(args.root)
    serialized = json.dumps(payload, indent=2)
    if args.output is not None:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(serialized + "\n", encoding="utf-8")
    print(serialized)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
