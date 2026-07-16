#!/usr/bin/env python3
"""Controller for the exponent-decade ladder."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import exponent_decade_ladder_pgs_mechanism as pgs_mechanism
import exponent_decade_ladder_validator as validator


ROOT = Path(__file__).resolve().parents[3]
DEFAULT_OUTPUT_DIR = ROOT / "research" / "09-exponents" / "output" / "exponent_decade_ladder_probe"


def build_parser() -> argparse.ArgumentParser:
    """Build the CLI parser."""
    parser = argparse.ArgumentParser(description="Run the exponent-decade ladder.")
    parser.add_argument(
        "--rungs",
        default=",".join(str(value) for value in pgs_mechanism.DEFAULT_RUNG_MAX_EXPONENTS),
    )
    parser.add_argument("--candidate-bound", type=int, default=pgs_mechanism.DEFAULT_CANDIDATE_BOUND)
    parser.add_argument(
        "--candidate-seconds-limit",
        type=float,
        default=pgs_mechanism.DEFAULT_CANDIDATE_SECONDS_LIMIT,
    )
    parser.add_argument(
        "--mersenne-inference",
        choices=sorted(pgs_mechanism.VALID_MERSENNE_INFERENCE_MODES),
        default=pgs_mechanism.DEFAULT_MERSENNE_INFERENCE,
    )
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    return parser


def run_controller(
    *,
    rungs: list[int],
    candidate_bound: int,
    candidate_seconds_limit: float,
    output_dir: Path,
    mersenne_inference: str = pgs_mechanism.DEFAULT_MERSENNE_INFERENCE,
) -> dict[str, object]:
    """Run the PGS ladder first, then validation."""
    output_dir.mkdir(parents=True, exist_ok=True)
    pgs_rows = pgs_mechanism.collect_rows(
        rungs,
        candidate_bound,
        candidate_seconds_limit,
        mersenne_inference,
    )
    pgs_mechanism.write_outputs(
        output_dir,
        pgs_rows,
        rungs,
        candidate_bound,
        candidate_seconds_limit,
        mersenne_inference,
    )
    pgs_summary = pgs_mechanism.summarize(
        pgs_rows,
        rungs,
        candidate_bound,
        candidate_seconds_limit,
        mersenne_inference,
    )

    validation_rows = validator.validate_rows(
        [{key: str(value) for key, value in row.items()} for row in pgs_rows]
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
        rungs=pgs_mechanism.parse_rungs(args.rungs),
        candidate_bound=args.candidate_bound,
        candidate_seconds_limit=args.candidate_seconds_limit,
        output_dir=args.output_dir,
        mersenne_inference=args.mersenne_inference,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
