#!/usr/bin/env python3
"""Compare intermediate PEDK multiplication-map projections across fresh bands."""

from __future__ import annotations

import argparse
import itertools
import json
from collections import Counter, defaultdict
from pathlib import Path

from first_gap_compatibility_check import write_json, write_jsonl


THIS_DIR = Path(__file__).resolve().parent
DEFAULT_TRAIN_DIR = THIS_DIR / "output" / "enriched_multiplication_map_corpus_7501_9000"
DEFAULT_FRESH_DIR = THIS_DIR / "output" / "enriched_multiplication_map_corpus_9001_11000"
DEFAULT_OUTPUT_DIR = THIS_DIR / "output" / "intermediate_projection_surface_7501_9000_to_9001_11000"
RULE_ID = "pedk_intermediate_projection_surface_v1"
DEFAULT_MIN_PUBLIC_SUPPORT = 3
DEFAULT_MIN_FACTOR_SUPPORT = 3


PUBLIC_MODES = (
    "public_word",
    "public_word_gwr_side",
    "public_word_gwr_bucket",
    "public_word_gwr_distance",
)
FACTOR_MODES = (
    "residue_phase",
    "factor_phased_word",
    "oriented_factor_phase_word",
)


def read_jsonl(path: Path) -> list[dict[str, object]]:
    """Read LF-delimited JSON rows."""
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def gwr_distance_bucket(distance: int) -> str:
    """Return a signed GWR-distance bucket."""
    if distance == 0:
        return "gwr=0"
    side = "before" if distance < 0 else "after"
    value = abs(distance)
    if value <= 4:
        band = "abs<=4"
    elif value <= 16:
        band = "5<=abs<=16"
    elif value <= 64:
        band = "17<=abs<=64"
    else:
        band = "abs>64"
    return f"gwr={side}_{band}"


def public_key(row: dict[str, object], mode: str) -> str:
    """Return the public-side projection key."""
    word = str(row["public_word"])
    if mode == "public_word":
        return word
    if mode == "public_word_gwr_side":
        return f"{word}|{row['public_gwr_side']}"
    if mode == "public_word_gwr_bucket":
        return f"{word}|{gwr_distance_bucket(int(row['public_gwr_signed_distance']))}"
    if mode == "public_word_gwr_distance":
        return f"{word}|gwr={row['public_gwr_signed_distance']}"
    raise ValueError(f"unknown public mode: {mode}")


def factor_key(row: dict[str, object], mode: str) -> str:
    """Return the factor-side projection key."""
    if mode == "residue_phase":
        return " || ".join(
            (
                str(row["factor_residue_multiset"]),
                str(row["factor_phase_multiset"]),
            )
        )
    if mode == "factor_phased_word":
        return str(row["factor_phased_word"])
    if mode == "oriented_factor_phase_word":
        return str(row["oriented_factor_phase_word"])
    raise ValueError(f"unknown factor mode: {mode}")


def surface(
    rows: list[dict[str, object]],
    public_mode: str,
    factor_mode: str,
    min_public_support: int,
    min_factor_support: int,
) -> dict[str, object]:
    """Return supported keys and observed cells for one projection."""
    public_counts = Counter(public_key(row, public_mode) for row in rows)
    factor_counts = Counter(factor_key(row, factor_mode) for row in rows)
    observed_counts = Counter(
        (public_key(row, public_mode), factor_key(row, factor_mode))
        for row in rows
    )
    supported_public = {
        key for key, count in public_counts.items() if count >= min_public_support
    }
    supported_factor = {
        key for key, count in factor_counts.items() if count >= min_factor_support
    }
    observed_supported = {
        key
        for key in observed_counts
        if key[0] in supported_public and key[1] in supported_factor
    }
    return {
        "public_counts": public_counts,
        "factor_counts": factor_counts,
        "observed_counts": observed_counts,
        "supported_public": supported_public,
        "supported_factor": supported_factor,
        "observed_supported": observed_supported,
    }


def top_counter(counter: Counter[object], limit: int) -> list[dict[str, object]]:
    """Return top counter entries."""
    return [
        {"value": str(value), "count": count}
        for value, count in sorted(counter.items(), key=lambda item: (-item[1], str(item[0])))[:limit]
    ]


def analyze_projection(
    train_rows: list[dict[str, object]],
    fresh_rows: list[dict[str, object]],
    public_mode: str,
    factor_mode: str,
    min_public_support: int,
    min_factor_support: int,
) -> tuple[dict[str, object], list[dict[str, object]]]:
    """Return summary and sample rows for one projection pair."""
    train = surface(
        train_rows,
        public_mode,
        factor_mode,
        min_public_support,
        min_factor_support,
    )
    fresh = surface(
        fresh_rows,
        public_mode,
        factor_mode,
        min_public_support,
        min_factor_support,
    )
    supported_product = set(
        itertools.product(train["supported_public"], train["supported_factor"])
    )
    train_candidates = supported_product - train["observed_supported"]
    fresh_testable_product = set(
        itertools.product(fresh["supported_public"], fresh["supported_factor"])
    )
    testable = train_candidates & fresh_testable_product
    falsified = testable & fresh["observed_supported"]
    survived = testable - falsified

    sample_rows = []
    for status, cells in (("falsified", falsified), ("survived", survived)):
        for public_value, factor_value in sorted(cells)[:25]:
            sample_rows.append(
                {
                    "rule_id": RULE_ID,
                    "public_mode": public_mode,
                    "factor_mode": factor_mode,
                    "status": status,
                    "public_key": public_value,
                    "factor_key": factor_value,
                    "train_public_support": train["public_counts"][public_value],
                    "train_factor_support": train["factor_counts"][factor_value],
                    "fresh_public_support": fresh["public_counts"][public_value],
                    "fresh_factor_support": fresh["factor_counts"][factor_value],
                    "fresh_observed_count": fresh["observed_counts"][
                        (public_value, factor_value)
                    ],
                }
            )

    summary = {
        "rule_id": RULE_ID,
        "public_mode": public_mode,
        "factor_mode": factor_mode,
        "min_public_support": min_public_support,
        "min_factor_support": min_factor_support,
        "train_public_key_count": len(train["public_counts"]),
        "train_factor_key_count": len(train["factor_counts"]),
        "train_supported_public_key_count": len(train["supported_public"]),
        "train_supported_factor_key_count": len(train["supported_factor"]),
        "train_observed_supported_cell_count": len(train["observed_supported"]),
        "train_candidate_absent_cell_count": len(train_candidates),
        "fresh_supported_public_key_count": len(fresh["supported_public"]),
        "fresh_supported_factor_key_count": len(fresh["supported_factor"]),
        "fresh_observed_supported_cell_count": len(fresh["observed_supported"]),
        "testable_candidate_absent_cell_count": len(testable),
        "falsified_candidate_absent_cell_count": len(falsified),
        "survived_candidate_absent_cell_count": len(survived),
        "falsification_rate_mpermille": (
            len(falsified) * 1000 // len(testable) if testable else 0
        ),
        "top_train_public_keys": top_counter(train["public_counts"], 5),
        "top_train_factor_keys": top_counter(train["factor_counts"], 5),
    }
    return summary, sample_rows


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Compare intermediate projection surfaces.")
    parser.add_argument("--train-dir", type=Path, default=DEFAULT_TRAIN_DIR)
    parser.add_argument("--fresh-dir", type=Path, default=DEFAULT_FRESH_DIR)
    parser.add_argument("--min-public-support", type=int, default=DEFAULT_MIN_PUBLIC_SUPPORT)
    parser.add_argument("--min-factor-support", type=int, default=DEFAULT_MIN_FACTOR_SUPPORT)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    """Run intermediate projection-surface comparison."""
    args = parse_args(argv)
    train_rows = read_jsonl(args.train_dir / "enriched_rows.jsonl")
    fresh_rows = read_jsonl(args.fresh_dir / "enriched_rows.jsonl")
    projection_rows = []
    sample_rows = []
    for public_mode in PUBLIC_MODES:
        for factor_mode in FACTOR_MODES:
            summary, samples = analyze_projection(
                train_rows,
                fresh_rows,
                public_mode,
                factor_mode,
                args.min_public_support,
                args.min_factor_support,
            )
            projection_rows.append(summary)
            sample_rows.extend(samples)

    projection_rows.sort(
        key=lambda row: (
            -int(row["testable_candidate_absent_cell_count"]),
            int(row["falsification_rate_mpermille"]),
            row["public_mode"],
            row["factor_mode"],
        )
    )
    summary = {
        "rule_id": RULE_ID,
        "status": "measured_intermediate_projection_surface",
        "theorem_status": "hypothesis_not_proved",
        "inference_status": "not_live_pedk_inference",
        "train_row_count": len(train_rows),
        "fresh_row_count": len(fresh_rows),
        "min_public_support": args.min_public_support,
        "min_factor_support": args.min_factor_support,
        "projection_count": len(projection_rows),
        "top_projection_rows": projection_rows[:5],
    }

    args.output_dir.mkdir(parents=True, exist_ok=True)
    write_jsonl(args.output_dir / "projection_surface_rows.jsonl", projection_rows)
    write_jsonl(args.output_dir / "projection_sample_rows.jsonl", sample_rows)
    write_json(args.output_dir / "summary.json", summary)
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
