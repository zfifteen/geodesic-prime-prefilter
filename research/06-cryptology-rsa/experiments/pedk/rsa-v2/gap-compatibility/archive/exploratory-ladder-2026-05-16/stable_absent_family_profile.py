#!/usr/bin/env python3
"""Profile compact families inside stable PEDK absent cells."""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

from first_gap_compatibility_check import write_json, write_jsonl


THIS_DIR = Path(__file__).resolve().parent
DEFAULT_INPUT = (
    THIS_DIR
    / "output"
    / "absent_cell_forward_stability_9001_11000_to_11001_13000_to_13001_15000_top5000"
    / "forward_stability_rows.jsonl"
)
DEFAULT_OUTPUT_DIR = (
    THIS_DIR
    / "output"
    / "stable_absent_family_profile_9001_11000_to_11001_13000_to_13001_15000_top5000"
)
RULE_ID = "pedk_stable_absent_family_profile_v1"
FACTOR_TOKEN_RE = re.compile(r"o[0-9]+_higher_divisor_(?:odd|even)\|[^@|]+@(?:early|mid|late|very_late)")


def read_jsonl(path: Path) -> list[dict[str, object]]:
    """Read LF-delimited JSON rows."""
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def public_parts(public_key: str) -> dict[str, str]:
    """Return public-key components."""
    before_side, side = public_key.rsplit("|", 1)
    prev_part, rest = before_side.split("|containing=", 1)
    containing_part, next_part = rest.split("|next=", 1)
    return {
        "prev": prev_part.removeprefix("prev="),
        "containing": containing_part,
        "next": next_part,
        "side": side,
    }


def factor_parts(factor_key: str) -> dict[str, str]:
    """Return oriented factor-key components."""
    p_part, q_part = factor_key.split(" || ", 1)
    tokens = FACTOR_TOKEN_RE.findall(factor_key)
    token_counts = Counter(tokens)
    return {
        "p_word": p_part.removeprefix("p="),
        "q_word": q_part.removeprefix("q="),
        "token_multiset": "|".join(
            f"{token}:{count}" for token, count in sorted(token_counts.items())
        ),
    }


def family_values(row: dict[str, object]) -> dict[str, str]:
    """Return candidate compact family keys for one stability row."""
    public = public_parts(str(row["public_key"]))
    factor = factor_parts(str(row["factor_key"]))
    public_containing_side = f"containing={public['containing']}|{public['side']}"
    public_prev_containing_side = (
        f"prev={public['prev']}|containing={public['containing']}|{public['side']}"
    )
    public_containing_next_side = (
        f"containing={public['containing']}|next={public['next']}|{public['side']}"
    )
    return {
        "public_word_gwr_side__factor_token_multiset": (
            f"{row['public_key']} :: factor_tokens={factor['token_multiset']}"
        ),
        "public_containing_side__factor_token_multiset": (
            f"{public_containing_side} :: factor_tokens={factor['token_multiset']}"
        ),
        "public_containing_side__factor_p_word": (
            f"{public_containing_side} :: p={factor['p_word']}"
        ),
        "public_containing_side__factor_q_word": (
            f"{public_containing_side} :: q={factor['q_word']}"
        ),
        "public_prev_containing_side__factor_token_multiset": (
            f"{public_prev_containing_side} :: factor_tokens={factor['token_multiset']}"
        ),
        "public_containing_next_side__factor_token_multiset": (
            f"{public_containing_next_side} :: factor_tokens={factor['token_multiset']}"
        ),
    }


def profile_rows(rows: list[dict[str, object]], min_survived: int) -> list[dict[str, object]]:
    """Return compact family profiles."""
    grouped: dict[tuple[str, str], list[dict[str, object]]] = defaultdict(list)
    for row in rows:
        for axis, value in family_values(row).items():
            grouped[(axis, value)].append(row)

    profiles = []
    for (axis, value), members in grouped.items():
        statuses = Counter(str(member["status"]) for member in members)
        survived = statuses["survived_absent"]
        if survived < min_survived:
            continue
        public_values = {str(member["public_key"]) for member in members}
        factor_values = {str(member["factor_key"]) for member in members}
        profiles.append(
            {
                "rule_id": RULE_ID,
                "axis": axis,
                "family_key": value,
                "row_count": len(members),
                "survived_absent_count": survived,
                "thin_observation_count": statuses["thin_observation"],
                "not_testable_forward_count": statuses["not_testable_forward"],
                "supported_falsification_count": statuses["supported_falsification"],
                "distinct_public_key_count": len(public_values),
                "distinct_factor_key_count": len(factor_values),
                "status": (
                    "clean_proto_family"
                    if statuses["thin_observation"] == 0
                    and statuses["supported_falsification"] == 0
                    else "mixed_proto_family"
                ),
            }
        )
    profiles.sort(
        key=lambda row: (
            str(row["status"]) != "clean_proto_family",
            -int(row["survived_absent_count"]),
            int(row["thin_observation_count"]),
            str(row["axis"]),
            str(row["family_key"]),
        )
    )
    return profiles


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Profile stable absent-cell families.")
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--min-survived", type=int, default=10)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    """Run compact family profile."""
    args = parse_args(argv)
    rows = read_jsonl(args.input)
    profiles = profile_rows(rows, args.min_survived)
    summary = {
        "rule_id": RULE_ID,
        "status": "measured_stable_absent_family_profile",
        "theorem_status": "hypothesis_not_proved",
        "inference_status": "not_live_pedk_inference",
        "input_row_count": len(rows),
        "profile_count": len(profiles),
        "clean_proto_family_count": sum(
            1 for row in profiles if row["status"] == "clean_proto_family"
        ),
        "mixed_proto_family_count": sum(
            1 for row in profiles if row["status"] == "mixed_proto_family"
        ),
        "min_survived": args.min_survived,
        "top_profiles": profiles[:20],
    }
    args.output_dir.mkdir(parents=True, exist_ok=True)
    write_jsonl(args.output_dir / "family_profile_rows.jsonl", profiles)
    write_json(args.output_dir / "summary.json", summary)
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
