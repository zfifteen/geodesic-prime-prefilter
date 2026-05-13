#!/usr/bin/env python3
"""Audit the selected-square deadline against the dynamic cutoff."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import gmpy2


ROOT = Path(__file__).resolve().parents[3]


def build_parser() -> argparse.ArgumentParser:
    """Build the CLI parser."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=int, action="append", required=True)
    parser.add_argument("--output", type=Path, default=None)
    return parser


def dynamic_cutoff(square: int) -> int:
    """Return C=max(64, ceil(0.5 log(square)^2))."""
    return max(64, math.ceil(0.5 * (math.log(square) ** 2)))


def selected_square_deadline_row(root: int) -> dict[str, object]:
    """Return selected-square deadline data for one prime root."""
    if root < 3 or not gmpy2.is_prime(root):
        raise ValueError("root must be an odd prime")
    previous_root = int(gmpy2.prev_prime(root))
    square = root * root
    previous_prime = int(gmpy2.prev_prime(square))
    actual_offset = square - previous_prime
    cutoff = dynamic_cutoff(square)
    deadline = square - previous_root * previous_root

    return {
        "root": str(root),
        "previous_root": str(previous_root),
        "previous_root_gap": root - previous_root,
        "selected_square_condition": previous_root * previous_root < previous_prime < square,
        "selected_square_deadline_offset": str(deadline),
        "selected_square_deadline_digits": len(str(deadline)),
        "actual_previous_prime_offset": actual_offset,
        "dynamic_cutoff": cutoff,
        "deadline_exceeds_dynamic_cutoff": deadline > cutoff,
        "deadline_to_cutoff_ratio": deadline / cutoff,
    }


def build_deadline_audit(roots: list[int]) -> dict[str, object]:
    """Return selected-square deadline rows for the requested roots."""
    rows = [selected_square_deadline_row(root) for root in roots]
    return {
        "root_count": len(rows),
        "all_selected_square": all(bool(row["selected_square_condition"]) for row in rows),
        "all_deadlines_exceed_dynamic_cutoff": all(
            bool(row["deadline_exceeds_dynamic_cutoff"]) for row in rows
        ),
        "rows": rows,
    }


def main(argv: list[str] | None = None) -> int:
    """Run the selected-square deadline audit."""
    args = build_parser().parse_args(argv)
    payload = build_deadline_audit(args.root)
    serialized = json.dumps(payload, indent=2)
    if args.output is not None:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(serialized + "\n", encoding="utf-8")
    print(serialized)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
