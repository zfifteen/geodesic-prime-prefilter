#!/usr/bin/env python3
"""Profile role-preserving families inside endpoint-pair exclusions."""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path

from first_gap_compatibility_check import write_json, write_jsonl


THIS_DIR = Path(__file__).resolve().parent
DEFAULT_INPUT = (
    THIS_DIR
    / "output"
    / "endpoint_pair_candidate_exclusions_17001_19000_rolling"
    / "candidate_exclusion_rows.jsonl"
)
DEFAULT_OUTPUT_DIR = (
    THIS_DIR
    / "output"
    / "endpoint_pair_family_profile_17001_19000_rolling"
)
RULE_ID = "pedk_endpoint_pair_family_profile_v1"
DEFAULT_MIN_SURVIVED = 20


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


def parse_endpoint_pair(pair: str) -> tuple[str, str]:
    """Return directed left/right slot labels from one endpoint pair."""
    left, right = pair.split("|R=", 1)
    return left.removeprefix("L="), right


def parse_factor_key(factor_key: str) -> tuple[tuple[str, str], tuple[str, str]]:
    """Return the two unordered directed endpoint pairs."""
    first, second = factor_key.split(" || ", 1)
    return parse_endpoint_pair(first), parse_endpoint_pair(second)


def slot_residue(slot: str) -> str:
    """Return the residue label from a slot value such as o4@mid."""
    return slot.split("@", 1)[0]


def slot_phase(slot: str) -> str:
    """Return the phase label from a slot value such as o4@mid."""
    return slot.split("@", 1)[1]


def endpoint_pair_key(
    pairs: tuple[tuple[str, str], tuple[str, str]],
    projection: str,
) -> str:
    """Return a role-preserving endpoint-pair projection."""
    out = []
    for left, right in pairs:
        if projection == "exact":
            out.append(f"L={left}|R={right}")
        elif projection == "residue":
            out.append(f"L={slot_residue(left)}|R={slot_residue(right)}")
        elif projection == "phase":
            out.append(f"L={slot_phase(left)}|R={slot_phase(right)}")
        elif projection == "left_residue_right_phase":
            out.append(f"L={slot_residue(left)}|R={slot_phase(right)}")
        elif projection == "left_phase_right_residue":
            out.append(f"L={slot_phase(left)}|R={slot_residue(right)}")
        else:
            raise ValueError(f"unknown endpoint-pair projection: {projection}")
    return " || ".join(sorted(out))


def public_key(public: dict[str, str], projection: str) -> str:
    """Return a public-side projection."""
    if projection == "word_side":
        return (
            f"prev={public['prev']}|containing={public['containing']}|"
            f"next={public['next']}|{public['side']}"
        )
    if projection == "containing_side":
        return f"containing={public['containing']}|{public['side']}"
    if projection == "prev_containing_side":
        return f"prev={public['prev']}|containing={public['containing']}|{public['side']}"
    if projection == "containing_next_side":
        return f"containing={public['containing']}|next={public['next']}|{public['side']}"
    raise ValueError(f"unknown public projection: {projection}")


def family_values(row: dict[str, object]) -> dict[str, str]:
    """Return role-preserving family keys for one candidate row."""
    public = public_parts(str(row["public_key"]))
    pairs = parse_factor_key(str(row["factor_key"]))
    values = {}
    for public_projection in (
        "word_side",
        "containing_side",
        "prev_containing_side",
        "containing_next_side",
    ):
        for factor_projection in (
            "exact",
            "residue",
            "phase",
            "left_residue_right_phase",
            "left_phase_right_residue",
        ):
            axis = f"{public_projection}__endpoint_pair_{factor_projection}"
            values[axis] = (
                f"{public_key(public, public_projection)} :: "
                f"endpoint_pairs={endpoint_pair_key(pairs, factor_projection)}"
            )
    return values


def profile_rows(rows: list[dict[str, object]], min_survived: int) -> list[dict[str, object]]:
    """Return role-preserving family profiles."""
    grouped: dict[tuple[str, str], list[dict[str, object]]] = defaultdict(list)
    for row in rows:
        for axis, value in family_values(row).items():
            grouped[(axis, value)].append(row)

    profiles = []
    for (axis, value), members in grouped.items():
        statuses = Counter(str(member["status"]) for member in members)
        survived = statuses["survived_forward"]
        if survived < min_survived:
            continue
        public_values = {str(member["public_key"]) for member in members}
        factor_values = {str(member["factor_key"]) for member in members}
        rank_score = sum(int(member["rank_score"]) for member in members)
        if statuses["falsified_forward"] == 0 and statuses["not_testable_forward"] == 0:
            status = "clean_fully_tested_role_family"
        elif statuses["falsified_forward"] == 0:
            status = "clean_partially_tested_role_family"
        else:
            status = "mixed_falsified_role_family"
        profiles.append(
            {
                "rule_id": RULE_ID,
                "axis": axis,
                "family_key": value,
                "row_count": len(members),
                "survived_forward_count": survived,
                "falsified_forward_count": statuses["falsified_forward"],
                "not_testable_forward_count": statuses["not_testable_forward"],
                "distinct_public_key_count": len(public_values),
                "distinct_factor_key_count": len(factor_values),
                "rank_score_sum": rank_score,
                "status": status,
            }
        )
    profiles.sort(
        key=lambda row: (
            str(row["status"]) != "clean_fully_tested_role_family",
            str(row["status"]) != "clean_partially_tested_role_family",
            -int(row["survived_forward_count"]),
            int(row["falsified_forward_count"]),
            int(row["not_testable_forward_count"]),
            str(row["axis"]),
            str(row["family_key"]),
        )
    )
    return profiles


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Profile role-preserving endpoint-pair families."
    )
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--min-survived", type=int, default=DEFAULT_MIN_SURVIVED)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    """Run endpoint-pair family profiling."""
    args = parse_args(argv)
    rows = read_jsonl(args.input)
    profiles = profile_rows(rows, args.min_survived)
    summary = {
        "rule_id": RULE_ID,
        "status": "measured_endpoint_pair_family_profile",
        "theorem_status": "hypothesis_not_proved",
        "inference_status": "not_live_pedk_inference",
        "input_row_count": len(rows),
        "profile_count": len(profiles),
        "clean_fully_tested_role_family_count": sum(
            1 for row in profiles if row["status"] == "clean_fully_tested_role_family"
        ),
        "clean_partially_tested_role_family_count": sum(
            1 for row in profiles if row["status"] == "clean_partially_tested_role_family"
        ),
        "mixed_falsified_role_family_count": sum(
            1 for row in profiles if row["status"] == "mixed_falsified_role_family"
        ),
        "min_survived": args.min_survived,
        "top_profiles": profiles[:30],
    }
    args.output_dir.mkdir(parents=True, exist_ok=True)
    write_jsonl(args.output_dir / "family_profile_rows.jsonl", profiles)
    write_json(args.output_dir / "summary.json", summary)
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
