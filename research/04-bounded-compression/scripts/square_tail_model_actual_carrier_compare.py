#!/usr/bin/env python3
"""Compare modeled singleton carriers with actual least factors."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
DEFAULT_MODEL = (
    ROOT
    / "research"
    / "04-bounded-compression"
    / "output"
    / "square_tail_full_cutoff_crt_model_509.json"
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
    parser.add_argument("--model", type=Path, default=DEFAULT_MODEL)
    parser.add_argument("--descent", type=Path, default=DEFAULT_DESCENT)
    parser.add_argument("--output", type=Path, default=None)
    return parser


def build_comparison(model_path: Path = DEFAULT_MODEL, descent_path: Path = DEFAULT_DESCENT) -> dict[str, object]:
    """Return exact carrier comparison rows for the model and actual descent."""
    model = json.loads(model_path.read_text(encoding="utf-8"))
    descent = json.loads(descent_path.read_text(encoding="utf-8"))
    carrier_by_m = {
        int(row["m"]): int(row["carrier"])
        for row in model["carrier_rows"]
    }
    carrier_positions = {
        int(row["carrier"]): int(row["m"])
        for row in model["carrier_rows"]
    }

    rows = []
    for row in descent["rough_tail_rows"]:
        if bool(row["is_prime"]):
            continue
        m = int(row["m"])
        least_factor = int(row["least_factor"])
        assigned = carrier_by_m.get(m)
        rows.append(
            {
                "m": m,
                "offset": 2 * m,
                "actual_least_factor": least_factor,
                "assigned_carrier_same_m": assigned,
                "same_position_match": least_factor == assigned,
                "assigned_elsewhere_m": carrier_positions.get(least_factor),
                "any_assigned_match": least_factor in carrier_positions,
            }
        )

    return {
        "model_path": str(model_path.relative_to(ROOT)),
        "descent_path": str(descent_path.relative_to(ROOT)),
        "actual_composite_row_count": len(rows),
        "same_position_match_count": sum(int(bool(row["same_position_match"])) for row in rows),
        "any_assigned_match_count": sum(int(bool(row["any_assigned_match"])) for row in rows),
        "rows": rows,
    }


def main(argv: list[str] | None = None) -> int:
    """Run the carrier comparison."""
    args = build_parser().parse_args(argv)
    payload = build_comparison(args.model, args.descent)
    serialized = json.dumps(payload, indent=2)
    if args.output is not None:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(serialized + "\n", encoding="utf-8")
    print(serialized)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
