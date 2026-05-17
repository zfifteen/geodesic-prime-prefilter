#!/usr/bin/env python3
"""Run fresh targeted checks for one public-grammar factor-class family."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

from first_gap_compatibility_check import (
    DEFAULT_MAX_RATIO_DENOMINATOR,
    DEFAULT_MAX_RATIO_NUMERATOR,
    write_json,
    write_jsonl,
)
from public_feature_all_o6_boundary import parse_bands
from public_grammar_pivot import read_jsonl
from public_grammar_targeted_slice_check import check_candidates


THIS_DIR = Path(__file__).resolve().parent
DEFAULT_CANDIDATE_PATH = (
    THIS_DIR
    / "output"
    / "public_grammar_factor_exclusion_pivot_601_5500"
    / "candidate_class_exclusion_rows.jsonl"
)
DEFAULT_OUTPUT_DIR = THIS_DIR / "output" / "public_grammar_family_o2o4_midlate_9001_11000"
DEFAULT_BANDS = ((9001, 11000),)
DEFAULT_FACTOR_RESIDUE_MULTISET = "o2:2|o4:2"
DEFAULT_FACTOR_PHASE_MULTISET = "mid:3|late:1"
RULE_ID = "pedk_public_grammar_family_targeted_slice_check_v1"


def selected_family_candidates(
    candidate_path: Path,
    factor_residue_multiset: str,
    factor_phase_multiset: str,
    public_word: str | None,
) -> list[dict[str, object]]:
    """Return candidates matching one residue and phase family."""
    rows = read_jsonl(candidate_path)
    selected = []
    for candidate_rank, row in enumerate(rows, 1):
        if str(row["factor_residue_multiset"]) != factor_residue_multiset:
            continue
        if str(row["factor_phase_multiset"]) != factor_phase_multiset:
            continue
        if public_word is not None and str(row["public_word"]) != public_word:
            continue
        selected_row = dict(row)
        selected_row["candidate_rank"] = candidate_rank
        selected.append(selected_row)
    if not selected:
        raise ValueError("no candidate rows matched the requested factor family")
    for index, row in enumerate(selected, 1):
        row["family_candidate_rank"] = index
    return selected


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Run targeted check for one factor family.")
    parser.add_argument("--candidate-path", type=Path, default=DEFAULT_CANDIDATE_PATH)
    parser.add_argument("--factor-residue-multiset", default=DEFAULT_FACTOR_RESIDUE_MULTISET)
    parser.add_argument("--factor-phase-multiset", default=DEFAULT_FACTOR_PHASE_MULTISET)
    parser.add_argument("--public-word")
    parser.add_argument("--band", action="append")
    parser.add_argument("--max-ratio-numerator", type=int, default=DEFAULT_MAX_RATIO_NUMERATOR)
    parser.add_argument("--max-ratio-denominator", type=int, default=DEFAULT_MAX_RATIO_DENOMINATOR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    """Run family-specific targeted slice check."""
    args = parse_args(argv)
    bands = parse_bands(args.band) if args.band else list(DEFAULT_BANDS)
    candidates = selected_family_candidates(
        args.candidate_path,
        args.factor_residue_multiset,
        args.factor_phase_multiset,
        args.public_word,
    )
    result_rows, falsification_rows, summary = check_candidates(
        candidates,
        bands,
        args.max_ratio_numerator,
        args.max_ratio_denominator,
    )
    status_counts = Counter(str(row["status"]) for row in result_rows)
    summary.update(
        {
            "rule_id": RULE_ID,
            "status": "measured_public_grammar_family_targeted_slice_check",
            "factor_residue_multiset": args.factor_residue_multiset,
            "factor_phase_multiset": args.factor_phase_multiset,
            "public_word_filter": args.public_word,
            "candidate_count": len(candidates),
            "status_counts": dict(sorted(status_counts.items())),
            "falsification_row_count": len(falsification_rows),
            "bands": [
                {
                    "min_factor": min_factor,
                    "max_factor": max_factor,
                    "max_factor_ratio": f"{args.max_ratio_numerator}/{args.max_ratio_denominator}",
                }
                for min_factor, max_factor in bands
            ],
        }
    )

    args.output_dir.mkdir(parents=True, exist_ok=True)
    write_jsonl(args.output_dir / "selected_family_candidate_rows.jsonl", candidates)
    write_jsonl(args.output_dir / "family_targeted_result_rows.jsonl", result_rows)
    write_jsonl(args.output_dir / "family_falsification_rows.jsonl", falsification_rows)
    write_json(args.output_dir / "summary.json", summary)
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
