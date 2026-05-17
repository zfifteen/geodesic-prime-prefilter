#!/usr/bin/env python3
"""Find structural predicates separating survived endpoint-pair families."""

from __future__ import annotations

import argparse
import itertools
import json
from collections import Counter, defaultdict
from pathlib import Path

from endpoint_pair_family_forward_test import split_family_key
from endpoint_pair_family_profile import parse_endpoint_pair, read_jsonl
from first_gap_compatibility_check import write_json, write_jsonl


THIS_DIR = Path(__file__).resolve().parent
DEFAULT_INPUT = (
    THIS_DIR
    / "output"
    / "endpoint_pair_family_forward_test_19001_21000"
    / "family_forward_rows.jsonl"
)
DEFAULT_OUTPUT_DIR = (
    THIS_DIR
    / "output"
    / "endpoint_pair_family_survival_contrast_19001_21000"
)
RULE_ID = "pedk_endpoint_pair_family_survival_contrast_v1"
DEFAULT_MIN_SURVIVED = 10
DEFAULT_MAX_WIDTH = 3


def parse_public_part(public_part: str) -> dict[str, str]:
    """Return public-side fields from a family public part."""
    fields = {}
    remaining = public_part
    if remaining.startswith("prev="):
        prev_part, remaining = remaining.split("|containing=", 1)
        fields["prev"] = prev_part.removeprefix("prev=")
    elif remaining.startswith("containing="):
        remaining = remaining.removeprefix("containing=")
    else:
        raise ValueError(f"unknown public part: {public_part}")

    if "|next=" in remaining:
        containing_part, rest = remaining.split("|next=", 1)
        next_part, side = rest.rsplit("|", 1)
        fields["next"] = next_part
    else:
        containing_part, side = remaining.rsplit("|", 1)
    fields["containing"] = containing_part
    fields["side"] = side
    if "@" in containing_part:
        containing_type, phase = containing_part.rsplit("@", 1)
        fields["containing_type"] = containing_type
        fields["containing_phase"] = phase
        fields["containing_residue"] = containing_type.split("_", 1)[0]
    return fields


def endpoint_pair_parts(factor_part: str) -> dict[str, str]:
    """Return directed endpoint-pair structural fields."""
    first, second = factor_part.split(" || ", 1)
    pair_a = parse_endpoint_pair(first)
    pair_b = parse_endpoint_pair(second)
    left_values = sorted((pair_a[0], pair_b[0]))
    right_values = sorted((pair_a[1], pair_b[1]))
    return {
        "endpoint_pair_a_left": pair_a[0],
        "endpoint_pair_a_right": pair_a[1],
        "endpoint_pair_b_left": pair_b[0],
        "endpoint_pair_b_right": pair_b[1],
        "endpoint_left_values": "|".join(left_values),
        "endpoint_right_values": "|".join(right_values),
        "endpoint_pairs": factor_part,
    }


def row_features(row: dict[str, object]) -> dict[str, str]:
    """Return structural feature map for one family-forward row."""
    axis = str(row["axis"])
    public_projection, factor_projection = axis.split("__", 1)
    public_part, factor_part = split_family_key(str(row["family_key"]))
    features = {
        "axis": axis,
        "public_projection": public_projection,
        "factor_projection": factor_projection,
    }
    for key, value in parse_public_part(public_part).items():
        features[f"public_{key}"] = value
    for key, value in endpoint_pair_parts(factor_part).items():
        features[f"factor_{key}"] = value
    return features


def predicate_key(items: tuple[tuple[str, str], ...]) -> str:
    """Return stable predicate key."""
    return " && ".join(f"{key}={value}" for key, value in items)


def contrast_rows(
    rows: list[dict[str, object]],
    min_survived: int,
    max_width: int,
) -> list[dict[str, object]]:
    """Return zero-falsified structural predicates."""
    counts: dict[tuple[tuple[str, str], ...], Counter[str]] = defaultdict(Counter)
    examples: dict[tuple[tuple[str, str], ...], dict[str, object]] = {}
    for row in rows:
        features = row_features(row)
        items = sorted(features.items())
        for width in range(1, max_width + 1):
            for combo in itertools.combinations(items, width):
                counts[combo][str(row["status"])] += 1
                examples.setdefault(combo, row)

    out = []
    for combo, status_counts in counts.items():
        survived = status_counts["survived_forward"]
        falsified = status_counts["falsified_forward"]
        not_testable = status_counts["not_testable_forward"]
        if survived < min_survived or falsified:
            continue
        out.append(
            {
                "rule_id": RULE_ID,
                "predicate": predicate_key(combo),
                "width": len(combo),
                "survived_forward_count": survived,
                "falsified_forward_count": falsified,
                "not_testable_forward_count": not_testable,
                "example_family_key": examples[combo]["family_key"],
                "example_axis": examples[combo]["axis"],
                "status": "zero_falsified_structural_predicate",
            }
        )
    out.sort(
        key=lambda row: (
            int(row["width"]),
            -int(row["survived_forward_count"]),
            str(row["predicate"]),
        )
    )
    return out


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Find structural predicates that separate survived families."
    )
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--min-survived", type=int, default=DEFAULT_MIN_SURVIVED)
    parser.add_argument("--max-width", type=int, default=DEFAULT_MAX_WIDTH)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    """Run structural survival contrast."""
    args = parse_args(argv)
    rows = read_jsonl(args.input)
    predicates = contrast_rows(rows, args.min_survived, args.max_width)
    status_counts = Counter(str(row["status"]) for row in rows)
    summary = {
        "rule_id": RULE_ID,
        "status": "measured_endpoint_pair_family_survival_contrast",
        "theorem_status": "hypothesis_not_proved",
        "inference_status": "not_live_pedk_inference",
        "input_row_count": len(rows),
        "input_survived_forward_count": status_counts["survived_forward"],
        "input_falsified_forward_count": status_counts["falsified_forward"],
        "min_survived": args.min_survived,
        "max_width": args.max_width,
        "zero_falsified_predicate_count": len(predicates),
        "top_predicates": predicates[:40],
    }
    args.output_dir.mkdir(parents=True, exist_ok=True)
    write_json(args.output_dir / "summary.json", summary)
    write_jsonl(args.output_dir / "predicate_rows.jsonl", predicates)
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
