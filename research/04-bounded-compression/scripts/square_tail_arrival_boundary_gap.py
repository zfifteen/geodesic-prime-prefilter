#!/usr/bin/env python3
"""Compare unarrived carrier rows with their square-root boundaries."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
DEFAULT_FRONTIER = (
    ROOT
    / "research"
    / "04-bounded-compression"
    / "output"
    / "square_tail_carrier_arrival_frontier_509_1e6.json"
)
DEFAULT_DESCENT = (
    ROOT
    / "research"
    / "04-bounded-compression"
    / "output"
    / "square_tail_dynamic_tail_descent_audit_509.json"
)


def build_parser() -> argparse.ArgumentParser:
    """Build the CLI parser."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--frontier", type=Path, default=DEFAULT_FRONTIER)
    parser.add_argument("--descent", type=Path, default=DEFAULT_DESCENT)
    parser.add_argument("--row-count", type=int, default=7)
    parser.add_argument("--output", type=Path, default=None)
    return parser


def descent_by_m(descent: dict[str, object]) -> dict[int, dict[str, object]]:
    """Return descent rough-tail rows keyed by m."""
    return {
        int(row["m"]): row
        for row in descent["rough_tail_rows"]
    }


def build_boundary_gap(
    frontier_path: Path = DEFAULT_FRONTIER,
    descent_path: Path = DEFAULT_DESCENT,
    row_count: int = 7,
) -> dict[str, object]:
    """Return square-root boundary comparisons for first unarrived rows."""
    frontier = json.loads(frontier_path.read_text(encoding="utf-8"))
    descent = json.loads(descent_path.read_text(encoding="utf-8"))
    root = int(frontier["representative_root"])
    square = root * root
    rows_by_m = descent_by_m(descent)

    rows = []
    for offset in frontier["first_unarrived_offsets"][:row_count]:
        m = int(offset) // 2
        value = square - int(offset)
        sqrt_boundary = math.isqrt(value)
        descent_row = rows_by_m.get(m)
        is_prime = bool(descent_row and descent_row["is_prime"])
        least_factor = (
            int(descent_row["least_factor"])
            if descent_row and descent_row["least_factor"] is not None
            else None
        )
        rows.append(
            {
                "m": m,
                "offset": int(offset),
                "sqrt_boundary": str(sqrt_boundary),
                "sqrt_boundary_digits": len(str(sqrt_boundary)),
                "sqrt_boundary_exceeds_dynamic_cutoff": (
                    sqrt_boundary > int(frontier["dynamic_cutoff"])
                ),
                "actual_status": "prime" if is_prime else "composite",
                "actual_least_factor": least_factor,
                "least_factor_exceeds_arrival_bound": (
                    least_factor is not None
                    and least_factor > int(frontier["arrival_bound"])
                ),
                "no_arrival_to_sqrt_required_for_prime": is_prime,
            }
        )

    return {
        "frontier_path": str(frontier_path.relative_to(ROOT)),
        "descent_path": str(descent_path.relative_to(ROOT)),
        "arrival_bound": frontier["arrival_bound"],
        "dynamic_cutoff": frontier["dynamic_cutoff"],
        "row_count": len(rows),
        "composite_row_count": sum(int(row["actual_status"] == "composite") for row in rows),
        "prime_row_count": sum(int(row["actual_status"] == "prime") for row in rows),
        "rows": rows,
    }


def main(argv: list[str] | None = None) -> int:
    """Run the arrival-boundary gap audit."""
    args = build_parser().parse_args(argv)
    payload = build_boundary_gap(args.frontier, args.descent, args.row_count)
    serialized = json.dumps(payload, indent=2)
    if args.output is not None:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(serialized + "\n", encoding="utf-8")
    print(serialized)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
