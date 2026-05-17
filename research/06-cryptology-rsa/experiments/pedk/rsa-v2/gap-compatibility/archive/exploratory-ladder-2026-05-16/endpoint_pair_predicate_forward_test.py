#!/usr/bin/env python3
"""Forward-test structural predicates over endpoint-pair families."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

from endpoint_pair_family_forward_test import forward_indexes, split_family_key
from endpoint_pair_family_profile import read_jsonl
from endpoint_pair_family_survival_contrast import row_features
from first_gap_compatibility_check import write_json, write_jsonl


THIS_DIR = Path(__file__).resolve().parent
DEFAULT_PREDICATES = (
    THIS_DIR
    / "output"
    / "endpoint_pair_family_survival_contrast_19001_21000"
    / "predicate_rows.jsonl"
)
DEFAULT_PROFILE = (
    THIS_DIR
    / "output"
    / "endpoint_pair_family_profile_17001_19000_rolling"
    / "family_profile_rows.jsonl"
)
DEFAULT_FORWARD_DIR = THIS_DIR / "output" / "enriched_multiplication_map_corpus_21001_23000"
DEFAULT_OUTPUT_DIR = THIS_DIR / "output" / "endpoint_pair_predicate_forward_test_21001_23000"
RULE_ID = "pedk_endpoint_pair_predicate_forward_test_v1"
DEFAULT_PROFILE_STATUS = "clean_fully_tested_role_family"


def parse_predicate(predicate: str) -> tuple[tuple[str, str], ...]:
    """Return predicate feature conditions."""
    conditions = []
    for part in predicate.split(" && "):
        key, value = part.split("=", 1)
        conditions.append((key, value))
    return tuple(conditions)


def matches(profile: dict[str, object], conditions: tuple[tuple[str, str], ...]) -> bool:
    """Return whether a profile matches all structural conditions."""
    features = row_features(
        {
            "axis": profile["axis"],
            "family_key": profile["family_key"],
            "status": profile["status"],
        }
    )
    return all(features.get(key) == value for key, value in conditions)


def test_profile(profile: dict[str, object], observed_family_keys: set[tuple[str, str]]) -> str:
    """Return strict forward status for one profile."""
    key = (str(profile["axis"]), str(profile["family_key"]))
    if key in observed_family_keys:
        return "falsified_forward"
    return "survived_forward"


def forward_test(
    predicates: list[dict[str, object]],
    profiles: list[dict[str, object]],
    forward_rows: list[dict[str, object]],
    profile_status: str,
) -> tuple[dict[str, object], list[dict[str, object]]]:
    """Return predicate forward-test summary and rows."""
    selected_profiles = [
        profile for profile in profiles if str(profile["status"]) == profile_status
    ]
    _, _, observed_family_keys = forward_indexes(forward_rows)
    rows = []
    for predicate_row in predicates:
        predicate = str(predicate_row["predicate"])
        conditions = parse_predicate(predicate)
        matched = [
            profile for profile in selected_profiles if matches(profile, conditions)
        ]
        status_counts = Counter(test_profile(profile, observed_family_keys) for profile in matched)
        testable = status_counts["survived_forward"] + status_counts["falsified_forward"]
        status = (
            "survived_forward"
            if matched and status_counts["falsified_forward"] == 0
            else "falsified_forward"
            if status_counts["falsified_forward"]
            else "not_testable_forward"
        )
        rows.append(
            {
                "rule_id": RULE_ID,
                "source_rule_id": predicate_row["rule_id"],
                "predicate": predicate,
                "source_survived_forward_count": predicate_row["survived_forward_count"],
                "source_falsified_forward_count": predicate_row["falsified_forward_count"],
                "matched_profile_count": len(matched),
                "survived_forward_family_count": status_counts["survived_forward"],
                "falsified_forward_family_count": status_counts["falsified_forward"],
                "strict_falsification_rate_mpermille": (
                    status_counts["falsified_forward"] * 1000 // testable
                    if testable
                    else None
                ),
                "status": status,
            }
        )
    rows.sort(
        key=lambda row: (
            row["status"] != "survived_forward",
            -int(row["survived_forward_family_count"]),
            str(row["predicate"]),
        )
    )
    status_counts = Counter(str(row["status"]) for row in rows)
    summary = {
        "rule_id": RULE_ID,
        "status": "measured_endpoint_pair_predicate_forward_test",
        "theorem_status": "hypothesis_not_proved",
        "inference_status": "not_live_pedk_inference",
        "forward_row_count": len(forward_rows),
        "input_predicate_count": len(predicates),
        "profile_status": profile_status,
        "survived_forward_predicate_count": status_counts["survived_forward"],
        "falsified_forward_predicate_count": status_counts["falsified_forward"],
        "not_testable_forward_predicate_count": status_counts["not_testable_forward"],
        "top_predicates": rows[:40],
    }
    return summary, rows


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Forward-test structural endpoint-pair predicates."
    )
    parser.add_argument("--predicates", type=Path, default=DEFAULT_PREDICATES)
    parser.add_argument("--profile", type=Path, default=DEFAULT_PROFILE)
    parser.add_argument("--forward-dir", type=Path, default=DEFAULT_FORWARD_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--profile-status", default=DEFAULT_PROFILE_STATUS)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    """Run predicate forward test."""
    args = parse_args(argv)
    predicates = read_jsonl(args.predicates)
    profiles = read_jsonl(args.profile)
    forward_rows = read_jsonl(args.forward_dir / "enriched_rows.jsonl")
    summary, rows = forward_test(
        predicates, profiles, forward_rows, args.profile_status
    )
    args.output_dir.mkdir(parents=True, exist_ok=True)
    write_json(args.output_dir / "summary.json", summary)
    write_jsonl(args.output_dir / "predicate_forward_rows.jsonl", rows)
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
