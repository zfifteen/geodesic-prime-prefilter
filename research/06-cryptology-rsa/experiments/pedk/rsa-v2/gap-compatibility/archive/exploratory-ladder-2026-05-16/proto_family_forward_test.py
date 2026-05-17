#!/usr/bin/env python3
"""Forward-test clean PEDK proto-family exclusions on a new band."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

from absent_cell_forward_stability import FACTOR_MODE, PUBLIC_MODE
from first_gap_compatibility_check import write_json, write_jsonl
from intermediate_projection_surface import factor_key, public_key
from stable_absent_family_profile import family_values, read_jsonl


THIS_DIR = Path(__file__).resolve().parent
DEFAULT_PROFILE_DIR = (
    THIS_DIR
    / "output"
    / "stable_absent_family_profile_9001_11000_to_11001_13000_to_13001_15000_top5000"
)
DEFAULT_FORWARD_DIR = THIS_DIR / "output" / "enriched_multiplication_map_corpus_15001_17000"
DEFAULT_OUTPUT_DIR = (
    THIS_DIR
    / "output"
    / "proto_family_forward_test_15001_17000"
)
RULE_ID = "pedk_proto_family_forward_test_v1"


def split_family_key(family_key: str) -> tuple[str, str]:
    """Split a compact family key into public and factor conditions."""
    public_condition, factor_condition = family_key.split(" :: ", 1)
    return public_condition, factor_condition


def row_family_values(row: dict[str, object]) -> dict[str, str]:
    """Return family values for one enriched corpus row."""
    projected = {
        "public_key": public_key(row, PUBLIC_MODE),
        "factor_key": factor_key(row, FACTOR_MODE),
    }
    return family_values(projected)


def forward_counts(rows: list[dict[str, object]]) -> dict[str, Counter[object]]:
    """Return family, public-condition, and factor-condition counts."""
    family_counter: Counter[tuple[str, str]] = Counter()
    public_condition_counter: Counter[tuple[str, str]] = Counter()
    factor_condition_counter: Counter[tuple[str, str]] = Counter()
    for row in rows:
        for axis, value in row_family_values(row).items():
            public_condition, factor_condition = split_family_key(value)
            family_counter[(axis, value)] += 1
            public_condition_counter[(axis, public_condition)] += 1
            factor_condition_counter[(axis, factor_condition)] += 1
    return {
        "family": family_counter,
        "public_condition": public_condition_counter,
        "factor_condition": factor_condition_counter,
    }


def selected_profiles(
    profile_rows: list[dict[str, object]],
    profile_status: str,
    axes: set[str],
    max_profiles: int | None,
) -> list[dict[str, object]]:
    """Return selected proto-family profiles."""
    rows = [
        row
        for row in profile_rows
        if str(row["status"]) == profile_status
        and (not axes or str(row["axis"]) in axes)
    ]
    rows.sort(
        key=lambda row: (
            -int(row["survived_absent_count"]),
            int(row["thin_observation_count"]),
            str(row["axis"]),
            str(row["family_key"]),
        )
    )
    if max_profiles is not None:
        return rows[:max_profiles]
    return rows


def evaluate_profiles(
    profiles: list[dict[str, object]],
    counts: dict[str, Counter[object]],
    observation_threshold: int,
) -> list[dict[str, object]]:
    """Evaluate selected proto-family profiles against forward rows."""
    rows = []
    for rank, profile in enumerate(profiles, start=1):
        axis = str(profile["axis"])
        family_key = str(profile["family_key"])
        public_condition, factor_condition = split_family_key(family_key)
        observed_count = counts["family"][(axis, family_key)]
        public_support = counts["public_condition"][(axis, public_condition)]
        factor_support = counts["factor_condition"][(axis, factor_condition)]
        forward_testable = public_support > 0 and factor_support > 0
        if not forward_testable:
            status = "not_testable_forward"
        elif observed_count >= observation_threshold:
            status = "falsified_forward"
        else:
            status = "survived_forward"
        rows.append(
            {
                "rule_id": RULE_ID,
                "rank": rank,
                "axis": axis,
                "family_key": family_key,
                "public_condition": public_condition,
                "factor_condition": factor_condition,
                "profile_row_count": profile["row_count"],
                "profile_survived_absent_count": profile["survived_absent_count"],
                "profile_distinct_public_key_count": profile["distinct_public_key_count"],
                "profile_distinct_factor_key_count": profile["distinct_factor_key_count"],
                "forward_public_condition_support": public_support,
                "forward_factor_condition_support": factor_support,
                "forward_observed_family_count": observed_count,
                "forward_testable": forward_testable,
                "observation_threshold": observation_threshold,
                "status": status,
            }
        )
    return rows


def summarize(
    rows: list[dict[str, object]],
    profile_input_count: int,
    forward_row_count: int,
    profile_status: str,
    observation_threshold: int,
) -> dict[str, object]:
    """Summarize proto-family forward rows."""
    status_counts = Counter(str(row["status"]) for row in rows)
    testable_count = sum(1 for row in rows if row["forward_testable"])
    return {
        "rule_id": RULE_ID,
        "status": "measured_proto_family_forward_test",
        "theorem_status": "hypothesis_not_proved",
        "inference_status": "not_live_pedk_inference",
        "profile_status_filter": profile_status,
        "profile_input_count": profile_input_count,
        "selected_profile_count": len(rows),
        "forward_row_count": forward_row_count,
        "observation_threshold": observation_threshold,
        "forward_testable_family_count": testable_count,
        "survived_forward_family_count": status_counts["survived_forward"],
        "falsified_forward_family_count": status_counts["falsified_forward"],
        "not_testable_forward_family_count": status_counts["not_testable_forward"],
        "falsification_rate_mpermille": (
            status_counts["falsified_forward"] * 1000 // testable_count
            if testable_count
            else 0
        ),
        "falsification_boundary": (
            "a proto-family exclusion is falsified by any forward row matching "
            "both its public condition and its factor condition"
        ),
        "top_rows": rows[:20],
    }


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Forward-test clean PEDK proto-families.")
    parser.add_argument("--profile-dir", type=Path, default=DEFAULT_PROFILE_DIR)
    parser.add_argument("--forward-dir", type=Path, default=DEFAULT_FORWARD_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--profile-status", default="clean_proto_family")
    parser.add_argument("--axis", action="append", default=[])
    parser.add_argument("--observation-threshold", type=int, default=1)
    parser.add_argument("--max-profiles", type=int)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    """Run proto-family forward test."""
    args = parse_args(argv)
    profile_rows = read_jsonl(args.profile_dir / "family_profile_rows.jsonl")
    forward_rows = read_jsonl(args.forward_dir / "enriched_rows.jsonl")
    profiles = selected_profiles(
        profile_rows,
        args.profile_status,
        set(args.axis),
        args.max_profiles,
    )
    counts = forward_counts(forward_rows)
    result_rows = evaluate_profiles(profiles, counts, args.observation_threshold)
    summary = summarize(
        result_rows,
        len(profile_rows),
        len(forward_rows),
        args.profile_status,
        args.observation_threshold,
    )
    args.output_dir.mkdir(parents=True, exist_ok=True)
    write_jsonl(args.output_dir / "proto_family_forward_rows.jsonl", result_rows)
    write_json(args.output_dir / "summary.json", summary)
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
