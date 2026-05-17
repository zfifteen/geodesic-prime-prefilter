#!/usr/bin/env python3
"""Forward-test clean role-preserving endpoint-pair families."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

from endpoint_pair_family_profile import family_values, read_jsonl
from first_gap_compatibility_check import write_json, write_jsonl
from slot_factor_public_quotient_test import factor_projection, public_projection


THIS_DIR = Path(__file__).resolve().parent
DEFAULT_PROFILE = (
    THIS_DIR
    / "output"
    / "endpoint_pair_family_profile_17001_19000_rolling"
    / "family_profile_rows.jsonl"
)
DEFAULT_FORWARD_DIR = THIS_DIR / "output" / "enriched_multiplication_map_corpus_19001_21000"
DEFAULT_OUTPUT_DIR = THIS_DIR / "output" / "endpoint_pair_family_forward_test_19001_21000"
RULE_ID = "pedk_endpoint_pair_family_forward_test_v1"
PUBLIC_MODE = "public_word_gwr_side"
FACTOR_MODE = "unordered_endpoint_pair_residue_phase"
DEFAULT_STATUS = "clean_fully_tested_role_family"


def split_family_key(family_key: str) -> tuple[str, str]:
    """Return public and endpoint-pair parts of a family key."""
    public_part, factor_part = family_key.split(" :: endpoint_pairs=", 1)
    return public_part, factor_part


def selected_profiles(rows: list[dict[str, object]], status: str) -> list[dict[str, object]]:
    """Return selected family profiles for forward testing."""
    return [row for row in rows if row["status"] == status]


def forward_indexes(
    rows: list[dict[str, object]],
) -> tuple[
    Counter[tuple[str, str]],
    Counter[tuple[str, str]],
    set[tuple[str, str]],
]:
    """Return public/factor/family indexes for fresh rows."""
    public_counts: Counter[tuple[str, str]] = Counter()
    factor_counts: Counter[tuple[str, str]] = Counter()
    observed_family_keys: set[tuple[str, str]] = set()
    for row in rows:
        public_key = public_projection(row, PUBLIC_MODE)
        factor_key = factor_projection(row, FACTOR_MODE)
        cell_row = {
            "public_key": public_key,
            "factor_key": factor_key,
        }
        for axis, family_key in family_values(cell_row).items():
            public_part, factor_part = split_family_key(family_key)
            public_counts[(axis, public_part)] += 1
            factor_counts[(axis, factor_part)] += 1
            observed_family_keys.add((axis, family_key))
    return public_counts, factor_counts, observed_family_keys


def forward_test(
    profiles: list[dict[str, object]],
    rows: list[dict[str, object]],
) -> tuple[dict[str, object], list[dict[str, object]]]:
    """Return forward-test summary and rows."""
    public_counts, factor_counts, observed_family_keys = forward_indexes(rows)
    result_rows = []
    for profile in profiles:
        axis = str(profile["axis"])
        family_key = str(profile["family_key"])
        key = (axis, family_key)
        public_part, factor_part = split_family_key(family_key)
        public_support = public_counts[(axis, public_part)]
        factor_support = factor_counts[(axis, factor_part)]
        if key in observed_family_keys:
            status = "falsified_forward"
            observed_count = 1
        elif public_support and factor_support:
            status = "survived_forward"
            observed_count = 0
        else:
            status = "not_testable_forward"
            observed_count = 0
        result_rows.append(
            {
                "rule_id": RULE_ID,
                "source_rule_id": profile["rule_id"],
                "axis": profile["axis"],
                "family_key": profile["family_key"],
                "source_survived_forward_count": profile["survived_forward_count"],
                "source_distinct_public_key_count": profile["distinct_public_key_count"],
                "source_distinct_factor_key_count": profile["distinct_factor_key_count"],
                "source_rank_score_sum": profile["rank_score_sum"],
                "fresh_public_support_floor": public_support,
                "fresh_factor_support_floor": factor_support,
                "fresh_observed_family_count": observed_count,
                "status": status,
            }
        )
    status_counts = Counter(str(row["status"]) for row in result_rows)
    result_rows.sort(
        key=lambda row: (
            row["status"] != "survived_forward",
            -int(row["source_survived_forward_count"]),
            str(row["axis"]),
            str(row["family_key"]),
        )
    )
    summary = {
        "rule_id": RULE_ID,
        "status": "measured_endpoint_pair_family_forward_test",
        "theorem_status": "hypothesis_not_proved",
        "inference_status": "not_live_pedk_inference",
        "forward_row_count": len(rows),
        "selected_profile_count": len(profiles),
        "survived_forward_family_count": status_counts["survived_forward"],
        "falsified_forward_family_count": status_counts["falsified_forward"],
        "not_testable_forward_family_count": status_counts["not_testable_forward"],
        "strict_falsification_rate_mpermille": (
            status_counts["falsified_forward"]
            * 1000
            // (status_counts["survived_forward"] + status_counts["falsified_forward"])
            if status_counts["survived_forward"] + status_counts["falsified_forward"]
            else None
        ),
        "top_survived_families": [
            row for row in result_rows if row["status"] == "survived_forward"
        ][:20],
        "top_falsified_families": [
            row for row in result_rows if row["status"] == "falsified_forward"
        ][:20],
    }
    return summary, result_rows


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Forward-test endpoint-pair family profiles."
    )
    parser.add_argument("--profile", type=Path, default=DEFAULT_PROFILE)
    parser.add_argument("--forward-dir", type=Path, default=DEFAULT_FORWARD_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--status", default=DEFAULT_STATUS)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    """Run endpoint-pair family forward test."""
    args = parse_args(argv)
    profiles = selected_profiles(read_jsonl(args.profile), args.status)
    rows = read_jsonl(args.forward_dir / "enriched_rows.jsonl")
    summary, result_rows = forward_test(profiles, rows)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    write_json(args.output_dir / "summary.json", summary)
    write_jsonl(args.output_dir / "family_forward_rows.jsonl", result_rows)
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
