#!/usr/bin/env python3
"""Controller for unresolved exponent pressure passes."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import exponent_unresolved_pressure_pgs_mechanism as pgs_mechanism
import exponent_unresolved_pressure_validator as validator


def build_parser() -> argparse.ArgumentParser:
    """Build the CLI parser."""
    parser = argparse.ArgumentParser(description="Run unresolved exponent pressure probe.")
    parser.add_argument("--input", type=Path, default=pgs_mechanism.DEFAULT_INPUT)
    parser.add_argument("--output-dir", type=Path, default=pgs_mechanism.DEFAULT_OUTPUT_DIR)
    parser.add_argument("--candidate-bound", type=int, default=4096)
    parser.add_argument("--candidate-seconds-limit", type=float, default=3.0)
    return parser


def run_controller(
    *,
    input_path: Path,
    output_dir: Path,
    candidate_bound: int,
    candidate_seconds_limit: float,
) -> dict[str, object]:
    """Run PGS pressure first, then validation for inferred rows."""
    source_rows = pgs_mechanism.read_csv(input_path)
    pgs_rows = pgs_mechanism.collect_rows(
        source_rows,
        candidate_bound,
        candidate_seconds_limit,
    )
    pgs_mechanism.write_outputs(
        output_dir,
        pgs_rows,
        len(source_rows),
        candidate_bound,
        candidate_seconds_limit,
    )
    inferred_rows = [
        {key: str(value) for key, value in row.items()}
        for row in pgs_rows
        if bool(row["mersenne_location_inferred"])
    ]
    validation_rows = validator.validate_rows(inferred_rows)
    validator.write_outputs(output_dir, validation_rows)
    summary = {
        "pgs_pressure": pgs_mechanism.summarize(
            pgs_rows,
            len(source_rows),
            candidate_bound,
            candidate_seconds_limit,
        ),
        "classical_validation": validator.summarize(validation_rows),
        "controller_order": "pgs_pressure_then_classical_validation",
    }
    (output_dir / "summary.json").write_text(
        json.dumps(summary, indent=2) + "\n",
        encoding="utf-8",
    )
    return summary


def main(argv: list[str] | None = None) -> int:
    """Run the pressure controller."""
    args = build_parser().parse_args(argv)
    run_controller(
        input_path=args.input,
        output_dir=args.output_dir,
        candidate_bound=args.candidate_bound,
        candidate_seconds_limit=args.candidate_seconds_limit,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
