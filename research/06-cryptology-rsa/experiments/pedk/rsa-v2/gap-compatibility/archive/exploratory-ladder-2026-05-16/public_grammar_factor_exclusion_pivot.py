#!/usr/bin/env python3
"""Compress public grammar exclusions by factor residue and phase multisets."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

from first_gap_compatibility_check import write_json, write_jsonl
from public_grammar_pivot import (
    factor_phase_multiset,
    factor_residue_multiset,
    parse_public_word,
    read_json,
    read_jsonl,
    top_rows,
)


THIS_DIR = Path(__file__).resolve().parent
DEFAULT_MAP_DIR = THIS_DIR / "output" / "multiplication_map_law_surface_601_5500"
DEFAULT_OUTPUT_DIR = THIS_DIR / "output" / "public_grammar_factor_exclusion_pivot_601_5500"
RULE_ID = "pedk_public_grammar_factor_exclusion_pivot_v1"


def build_pivot(map_dir: Path) -> tuple[list[dict[str, object]], list[dict[str, object]], dict[str, object]]:
    """Return public-by-factor-class exclusion compression rows."""
    summary = read_json(map_dir / "summary.json")
    public_rows = read_jsonl(map_dir / "public_word_rows.jsonl")
    cell_rows = read_jsonl(map_dir / "map_cell_rows.jsonl")
    supported_public_words = {
        str(row["public_word"])
        for row in public_rows
        if int(row["forward_row_count"]) >= int(summary["min_public_support"])
    }

    public_support = {
        str(row["public_word"]): int(row["forward_row_count"])
        for row in public_rows
        if str(row["public_word"]) in supported_public_words
    }
    observed_word_count = Counter()
    observed_row_count = Counter()
    excluded_word_count = Counter()
    excluded_factor_support = Counter()
    excluded_words: dict[tuple[str, str, str], Counter[str]] = {}

    for row in cell_rows:
        public_word = str(row["public_word"])
        if public_word not in supported_public_words:
            continue
        factor_word = str(row["factor_word"])
        residue_key = factor_residue_multiset(factor_word)
        phase_key = factor_phase_multiset(factor_word)
        key = (public_word, residue_key, phase_key)
        if row.get("status") == "candidate_exclusion_not_observed":
            excluded_word_count[key] += 1
            excluded_factor_support[key] += int(row["factor_word_support"])
            excluded_words.setdefault(key, Counter())[factor_word] += int(row["factor_word_support"])
            continue
        observed_word_count[key] += 1
        observed_row_count[key] += int(row["forward_row_count"])

    keys = sorted(set(observed_word_count) | set(excluded_word_count))
    rows = []
    candidate_rows = []
    for public_word, residue_key, phase_key in keys:
        parsed = parse_public_word(public_word)
        excluded_count = excluded_word_count[(public_word, residue_key, phase_key)]
        observed_count = observed_word_count[(public_word, residue_key, phase_key)]
        row = {
            "rule_id": RULE_ID,
            "public_word": public_word,
            "previous_reduced_state": parsed["prev"],
            "containing_exact_type": parsed["containing"],
            "n_phase": parsed["phase"],
            "next_reduced_state": parsed["next"],
            "factor_residue_multiset": residue_key,
            "factor_phase_multiset": phase_key,
            "public_forward_row_count": public_support[public_word],
            "observed_factor_word_count": observed_count,
            "observed_forward_row_count": observed_row_count[(public_word, residue_key, phase_key)],
            "excluded_factor_word_count": excluded_count,
            "excluded_factor_support_total": excluded_factor_support[(public_word, residue_key, phase_key)],
            "factor_class_status": (
                "candidate_class_exclusion"
                if excluded_count and not observed_count
                else "mixed_or_observed"
            ),
            "is_uniform_residue_class": len(residue_key.split("|")) == 1,
            "is_all_o6_class": residue_key == "o6:4",
            "top_excluded_factor_words": top_rows(excluded_words.get((public_word, residue_key, phase_key), Counter()), 5),
        }
        rows.append(row)
        if row["factor_class_status"] == "candidate_class_exclusion":
            candidate_rows.append(row)

    rows.sort(
        key=lambda row: (
            row["factor_class_status"] != "candidate_class_exclusion",
            -int(row["excluded_factor_word_count"]),
            -int(row["excluded_factor_support_total"]),
            row["public_word"],
            row["factor_residue_multiset"],
            row["factor_phase_multiset"],
        )
    )
    candidate_rows.sort(
        key=lambda row: (
            -int(row["excluded_factor_word_count"]),
            -int(row["excluded_factor_support_total"]),
            row["public_word"],
            row["factor_residue_multiset"],
            row["factor_phase_multiset"],
        )
    )

    candidate_residue_counter = Counter(str(row["factor_residue_multiset"]) for row in candidate_rows)
    summary_row = {
        "rule_id": RULE_ID,
        "status": "measured_public_grammar_factor_exclusion_pivot",
        "theorem_status": "hypothesis_not_proved",
        "inference_status": "not_live_pedk_inference",
        "supported_public_word_count": len(supported_public_words),
        "factor_class_cell_count": len(rows),
        "candidate_class_exclusion_count": len(candidate_rows),
        "candidate_residue_multiset_counts": dict(sorted(candidate_residue_counter.items())),
    }
    return rows, candidate_rows, summary_row


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Compress public grammar factor exclusions.")
    parser.add_argument("--map-dir", type=Path, default=DEFAULT_MAP_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    """Run public grammar factor-exclusion compression."""
    args = parse_args(argv)
    rows, candidate_rows, summary = build_pivot(args.map_dir)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    write_jsonl(args.output_dir / "factor_class_pivot_rows.jsonl", rows)
    write_jsonl(args.output_dir / "candidate_class_exclusion_rows.jsonl", candidate_rows)
    write_json(args.output_dir / "summary.json", summary)
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
