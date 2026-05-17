#!/usr/bin/env python3
"""Extract role-preserving endpoint-pair candidate exclusions."""

from __future__ import annotations

import argparse
import itertools
import json
from pathlib import Path

from first_gap_compatibility_check import write_json, write_jsonl
from slot_factor_public_quotient_test import (
    factor_projection,
    public_projection,
    read_jsonl,
    surface,
)


THIS_DIR = Path(__file__).resolve().parent
DEFAULT_TRAIN_DIR = THIS_DIR / "output" / "enriched_multiplication_map_corpus_11001_13000"
DEFAULT_CALIBRATION_DIR = THIS_DIR / "output" / "enriched_multiplication_map_corpus_13001_15000"
DEFAULT_PRIOR_FORWARD_DIR = THIS_DIR / "output" / "enriched_multiplication_map_corpus_15001_17000"
DEFAULT_FORWARD_DIR = THIS_DIR / "output" / "enriched_multiplication_map_corpus_17001_19000"
DEFAULT_OUTPUT_DIR = THIS_DIR / "output" / "endpoint_pair_candidate_exclusions_17001_19000_rolling"
RULE_ID = "pedk_endpoint_pair_candidate_exclusions_v1"
PUBLIC_MODE = "public_word_gwr_side"
FACTOR_MODE = "unordered_endpoint_pair_residue_phase"
MIN_PUBLIC_SUPPORT = 5
MIN_FACTOR_SUPPORT = 5


def support_counts(
    observed: dict[str, object],
    public_key: str,
    factor_key: str,
) -> dict[str, int]:
    """Return support counts for one public/factor cell."""
    return {
        "public_support": int(observed["public_counts"][public_key]),
        "factor_support": int(observed["factor_counts"][factor_key]),
        "observed_count": int(observed["observed_counts"][(public_key, factor_key)]),
    }


def candidate_rows(
    train_rows: list[dict[str, object]],
    calibration_rows: list[dict[str, object]],
    prior_forward_rows: list[dict[str, object]],
    forward_rows: list[dict[str, object]],
) -> tuple[dict[str, object], list[dict[str, object]]]:
    """Return summary and all candidate endpoint-pair exclusion rows."""
    train = surface(
        train_rows, PUBLIC_MODE, FACTOR_MODE, MIN_PUBLIC_SUPPORT, MIN_FACTOR_SUPPORT
    )
    calibration = surface(
        calibration_rows, PUBLIC_MODE, FACTOR_MODE, MIN_PUBLIC_SUPPORT, MIN_FACTOR_SUPPORT
    )
    prior_forward = surface(
        prior_forward_rows, PUBLIC_MODE, FACTOR_MODE, MIN_PUBLIC_SUPPORT, MIN_FACTOR_SUPPORT
    )
    forward = surface(
        forward_rows, PUBLIC_MODE, FACTOR_MODE, MIN_PUBLIC_SUPPORT, MIN_FACTOR_SUPPORT
    )

    candidate_cells = set(
        itertools.product(train["supported_public"], train["supported_factor"])
    )
    for observed in (train, calibration, prior_forward):
        supported_product = set(
            itertools.product(observed["supported_public"], observed["supported_factor"])
        )
        candidate_cells &= supported_product
        candidate_cells -= observed["observed_supported"]

    forward_product = set(
        itertools.product(forward["supported_public"], forward["supported_factor"])
    )
    testable = candidate_cells & forward_product
    falsified = testable & forward["observed_supported"]

    rows = []
    for public_key, factor_key in sorted(candidate_cells):
        train_counts = support_counts(train, public_key, factor_key)
        calibration_counts = support_counts(calibration, public_key, factor_key)
        prior_counts = support_counts(prior_forward, public_key, factor_key)
        if (public_key, factor_key) in forward_product:
            forward_counts = support_counts(forward, public_key, factor_key)
            status = (
                "falsified_forward"
                if (public_key, factor_key) in falsified
                else "survived_forward"
            )
        else:
            forward_counts = {
                "public_support": int(forward["public_counts"][public_key]),
                "factor_support": int(forward["factor_counts"][factor_key]),
                "observed_count": 0,
            }
            status = "not_testable_forward"
        public_min_support = min(
            train_counts["public_support"],
            calibration_counts["public_support"],
            prior_counts["public_support"],
            forward_counts["public_support"],
        )
        factor_min_support = min(
            train_counts["factor_support"],
            calibration_counts["factor_support"],
            prior_counts["factor_support"],
            forward_counts["factor_support"],
        )
        rows.append(
            {
                "rule_id": RULE_ID,
                "public_mode": PUBLIC_MODE,
                "factor_mode": FACTOR_MODE,
                "public_key": public_key,
                "factor_key": factor_key,
                "train_public_support": train_counts["public_support"],
                "train_factor_support": train_counts["factor_support"],
                "calibration_public_support": calibration_counts["public_support"],
                "calibration_factor_support": calibration_counts["factor_support"],
                "prior_forward_public_support": prior_counts["public_support"],
                "prior_forward_factor_support": prior_counts["factor_support"],
                "forward_public_support": forward_counts["public_support"],
                "forward_factor_support": forward_counts["factor_support"],
                "forward_observed_count": forward_counts["observed_count"],
                "min_public_support_across_bands": public_min_support,
                "min_factor_support_across_bands": factor_min_support,
                "rank_score": public_min_support * factor_min_support,
                "status": status,
            }
        )

    rows.sort(
        key=lambda row: (
            row["status"] != "survived_forward",
            -int(row["rank_score"]),
            -int(row["min_public_support_across_bands"]),
            -int(row["min_factor_support_across_bands"]),
            str(row["public_key"]),
            str(row["factor_key"]),
        )
    )

    status_counts = {
        status: sum(1 for row in rows if row["status"] == status)
        for status in ("survived_forward", "falsified_forward", "not_testable_forward")
    }
    summary = {
        "rule_id": RULE_ID,
        "status": "measured_endpoint_pair_candidate_exclusions",
        "theorem_status": "hypothesis_not_proved",
        "inference_status": "not_live_pedk_inference",
        "public_mode": PUBLIC_MODE,
        "factor_mode": FACTOR_MODE,
        "train_row_count": len(train_rows),
        "calibration_row_count": len(calibration_rows),
        "prior_forward_row_count": len(prior_forward_rows),
        "forward_row_count": len(forward_rows),
        "candidate_clean_absent_cell_count": len(candidate_cells),
        "forward_testable_cell_count": len(testable),
        "survived_forward_cell_count": status_counts["survived_forward"],
        "falsified_forward_cell_count": status_counts["falsified_forward"],
        "not_testable_forward_cell_count": status_counts["not_testable_forward"],
        "strict_falsification_rate_mpermille": (
            status_counts["falsified_forward"] * 1000 // len(testable)
            if testable
            else None
        ),
        "top_survived_candidates": [
            row for row in rows if row["status"] == "survived_forward"
        ][:20],
    }
    return summary, rows


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Extract endpoint-pair candidate exclusions."
    )
    parser.add_argument("--train-dir", type=Path, default=DEFAULT_TRAIN_DIR)
    parser.add_argument("--calibration-dir", type=Path, default=DEFAULT_CALIBRATION_DIR)
    parser.add_argument("--prior-forward-dir", type=Path, default=DEFAULT_PRIOR_FORWARD_DIR)
    parser.add_argument("--forward-dir", type=Path, default=DEFAULT_FORWARD_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    """Run endpoint-pair candidate exclusion extraction."""
    args = parse_args(argv)
    train_rows = read_jsonl(args.train_dir / "enriched_rows.jsonl")
    calibration_rows = read_jsonl(args.calibration_dir / "enriched_rows.jsonl")
    prior_forward_rows = read_jsonl(args.prior_forward_dir / "enriched_rows.jsonl")
    forward_rows = read_jsonl(args.forward_dir / "enriched_rows.jsonl")
    summary, rows = candidate_rows(
        train_rows, calibration_rows, prior_forward_rows, forward_rows
    )

    args.output_dir.mkdir(parents=True, exist_ok=True)
    write_json(args.output_dir / "summary.json", summary)
    write_jsonl(args.output_dir / "candidate_exclusion_rows.jsonl", rows)
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
