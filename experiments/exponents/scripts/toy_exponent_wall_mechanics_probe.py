#!/usr/bin/env python3
"""Controller for toy exponent-wall PGS mechanism and validation."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import toy_exponent_wall_pgs_mechanism as pgs_mechanism
import toy_exponent_wall_validator as validator


ROOT = Path(__file__).resolve().parents[3]
DEFAULT_OUTPUT_DIR = ROOT / "experiments" / "exponents" / "output" / "toy_exponent_wall_mechanics_probe"


def build_parser() -> argparse.ArgumentParser:
    """Build the CLI parser."""
    parser = argparse.ArgumentParser(
        description="Run toy exponent-wall PGS mechanism followed by validation.",
    )
    parser.add_argument("--min-exponent", type=int, default=pgs_mechanism.DEFAULT_MIN_EXPONENT)
    parser.add_argument("--max-exponent", type=int, default=pgs_mechanism.DEFAULT_MAX_EXPONENT)
    parser.add_argument("--candidate-bound", type=int, default=pgs_mechanism.DEFAULT_CANDIDATE_BOUND)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    return parser


def run_controller(
    *,
    min_exponent: int,
    max_exponent: int,
    candidate_bound: int,
    output_dir: Path,
) -> dict[str, object]:
    """Run PGS mechanism first, then classical validation."""
    output_dir.mkdir(parents=True, exist_ok=True)
    pgs_rows = pgs_mechanism.collect_rows(min_exponent, max_exponent, candidate_bound)
    pgs_mechanism.write_outputs(output_dir, pgs_rows)
    pgs_summary = pgs_mechanism.summarize(
        pgs_rows,
        min_exponent,
        max_exponent,
        candidate_bound,
    )
    (output_dir / "pgs_summary.json").write_text(
        json.dumps(pgs_summary, indent=2) + "\n",
        encoding="utf-8",
    )

    validation_rows = validator.validate_rows(
        [
            {key: str(value) for key, value in row.items()}
            for row in pgs_rows
        ]
    )
    validator.write_outputs(output_dir, validation_rows)
    validation_summary = validator.summarize(validation_rows)
    summary = {
        "pgs_mechanism": pgs_summary,
        "classical_validation": validation_summary,
        "controller_order": "pgs_mechanism_then_classical_validation",
    }
    (output_dir / "summary.json").write_text(
        json.dumps(summary, indent=2) + "\n",
        encoding="utf-8",
    )
    return summary


def main(argv: list[str] | None = None) -> int:
    """Run the controller."""
    args = build_parser().parse_args(argv)
    run_controller(
        min_exponent=args.min_exponent,
        max_exponent=args.max_exponent,
        candidate_bound=args.candidate_bound,
        output_dir=args.output_dir,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
