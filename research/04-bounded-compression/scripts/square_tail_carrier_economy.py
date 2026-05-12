#!/usr/bin/env python3
"""Audit repeat and singleton carrier economy in a square-tail prefix."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from square_tail_cover_audit import covered_positions  # noqa: E402
from square_tail_obstruction_word import build_payload  # noqa: E402


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


def build_carrier_economy(root: int) -> dict[str, object]:
    """Return the repeat and singleton carrier economy for one root."""
    payload = build_payload(root)
    rows = list(payload["obstruction_rows"])
    full_count = int(payload["full_counterexample_even_count"])
    factors = sorted({int(row["least_factor"]) for row in rows})
    repeat_factors = [factor for factor in factors if factor <= full_count]
    singleton_factors = [factor for factor in factors if factor > full_count]
    repeat_covered = covered_positions(root, repeat_factors, full_count)
    all_covered = covered_positions(root, factors, full_count)
    repeat_uncovered = [
        m for m in range(1, full_count + 1) if m not in repeat_covered
    ]
    all_uncovered = [
        m for m in range(1, full_count + 1) if m not in all_covered
    ]
    singleton_rows = [
        row for row in rows if int(row["least_factor"]) > full_count
    ]

    return {
        "root": root,
        "previous_prime_offset": payload["previous_prime_offset"],
        "dynamic_cutoff": payload["dynamic_cutoff"],
        "full_counterexample_even_count": full_count,
        "obstruction_prefix_even_count": payload["obstruction_prefix_even_count"],
        "distinct_factor_count": len(factors),
        "repeat_factor_count": len(repeat_factors),
        "singleton_factor_count": len(singleton_factors),
        "prefix_singleton_row_count": len(singleton_rows),
        "repeat_covered_count": len(repeat_covered),
        "all_prefix_factor_covered_count": len(all_covered),
        "repeat_uncovered_count": len(repeat_uncovered),
        "all_prefix_factor_uncovered_count": len(all_uncovered),
        "repeat_uncovered_offsets": [2 * m for m in repeat_uncovered],
        "all_prefix_factor_uncovered_offsets": [2 * m for m in all_uncovered],
        "singleton_factor_offsets": [int(row["offset"]) for row in singleton_rows],
        "repeat_factors": repeat_factors,
        "singleton_factors": singleton_factors,
    }


def main(argv: list[str] | None = None) -> int:
    """Run the carrier-economy audit."""
    args = build_parser().parse_args(argv)
    payload = build_carrier_economy(args.root)
    serialized = json.dumps(payload, indent=2)
    if args.output is not None:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(serialized + "\n", encoding="utf-8")
    print(serialized)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
