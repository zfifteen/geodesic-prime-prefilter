#!/usr/bin/env python3
"""Test high-signal public-word transported filters on a fresh band."""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path

from first_gap_compatibility_check import (
    DEFAULT_MAX_RATIO_DENOMINATOR,
    DEFAULT_MAX_RATIO_NUMERATOR,
    write_json,
    write_jsonl,
)
from public_feature_all_o6_boundary import parse_bands
from public_grammar_transported_candidate_filter import (
    DEFAULT_RULE_STATUS,
    DEFAULT_TARGETED_DIR,
    aggregate_rows,
    band_endpoint_values,
    load_rules,
    measure_band,
)


THIS_DIR = Path(__file__).resolve().parent
RULE_ID = "pedk_public_grammar_word_conditioned_transported_filter_v1"
DEFAULT_BASELINE_BANDS = ((5501, 6500), (6501, 7500))
DEFAULT_FRESH_BANDS = ((7501, 9000),)
DEFAULT_OUTPUT_DIR = THIS_DIR / "output" / "public_grammar_word_conditioned_transported_filter_7501_9000"
DEFAULT_CONTINUE_THRESHOLD = 0.025
DEFAULT_DEPRIORITIZE_THRESHOLD = 0.015


def measure_bands(
    bands: list[tuple[int, int]],
    rules_by_public: dict[str, set[tuple[str, str]]],
    max_ratio_numerator: int,
    max_ratio_denominator: int,
) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    """Return transported-candidate rows and band summaries for a set of bands."""
    endpoints = band_endpoint_values(bands)
    rows: list[dict[str, object]] = []
    band_summaries: list[dict[str, object]] = []
    for min_factor, max_factor in bands:
        band_rows, band_summary = measure_band(
            min_factor,
            max_factor,
            rules_by_public,
            endpoints,
            max_ratio_numerator,
            max_ratio_denominator,
        )
        rows.extend(band_rows)
        band_summaries.append(band_summary)
    return rows, band_summaries


def public_word_stats(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    """Return per-public-word reduction stats for rows that have survived rules."""
    counters: dict[str, Counter[str]] = defaultdict(Counter)
    for row in rows:
        if not bool(row["has_survived_rule"]):
            continue
        public_word = str(row["public_word"])
        counters[public_word]["row_count"] += 1
        counters[public_word]["candidate_x_count"] += int(row["candidate_x_count"])
        counters[public_word]["transported_endpoint_candidate_count"] += int(
            row["transported_endpoint_candidate_count"]
        )
        counters[public_word]["compatibility_eliminated_candidate_count"] += int(
            row["compatibility_eliminated_candidate_count"]
        )
        counters[public_word]["true_p_eliminated_by_compatibility_count"] += int(
            bool(row["true_p_eliminated_by_compatibility"])
        )

    stats = []
    for public_word, counts in counters.items():
        candidate_count = counts["candidate_x_count"]
        endpoint_candidate_count = counts["transported_endpoint_candidate_count"]
        eliminated_count = counts["compatibility_eliminated_candidate_count"]
        stats.append(
            {
                "rule_id": RULE_ID,
                "public_word": public_word,
                "row_count": counts["row_count"],
                "candidate_x_count": candidate_count,
                "transported_endpoint_candidate_count": endpoint_candidate_count,
                "compatibility_eliminated_candidate_count": eliminated_count,
                "compatibility_eliminated_fraction_of_all_candidates": (
                    eliminated_count / candidate_count if candidate_count else 0.0
                ),
                "compatibility_eliminated_fraction_of_endpoint_candidates": (
                    eliminated_count / endpoint_candidate_count if endpoint_candidate_count else 0.0
                ),
                "true_p_eliminated_by_compatibility_count": counts[
                    "true_p_eliminated_by_compatibility_count"
                ],
            }
        )

    stats.sort(
        key=lambda row: (
            -float(row["compatibility_eliminated_fraction_of_endpoint_candidates"]),
            -int(row["compatibility_eliminated_candidate_count"]),
            row["public_word"],
        )
    )
    return stats


def select_public_words(
    baseline_stats: list[dict[str, object]],
    max_selected_public_words: int,
) -> list[dict[str, object]]:
    """Return high-signal public words from baseline stats."""
    selected = [
        row
        for row in baseline_stats
        if int(row["compatibility_eliminated_candidate_count"]) > 0
        and int(row["true_p_eliminated_by_compatibility_count"]) == 0
    ]
    if max_selected_public_words > 0:
        selected = selected[:max_selected_public_words]
    if not selected:
        raise ValueError("no high-signal public words selected from baseline")
    return selected


def aggregate_selected_rows(
    rows: list[dict[str, object]],
    selected_public_words: set[str],
) -> dict[str, object]:
    """Return aggregate metrics for selected public words only."""
    selected_rows = [
        row
        for row in rows
        if str(row["public_word"]) in selected_public_words
    ]
    aggregate = aggregate_rows(selected_rows)
    aggregate["selected_row_count"] = len(selected_rows)
    return aggregate


def outcome_status(
    fresh_aggregate: dict[str, object],
    continue_threshold: float,
    deprioritize_threshold: float,
) -> str:
    """Return deterministic status for the fresh word-conditioned run."""
    true_p_eliminated = int(fresh_aggregate["true_p_eliminated_by_compatibility_count"])
    fraction = float(fresh_aggregate["compatibility_eliminated_fraction_of_endpoint_candidates"])
    if true_p_eliminated:
        return "falsified_true_p_eliminated"
    if fraction >= continue_threshold:
        return "continue_condition_met"
    if fraction < deprioritize_threshold:
        return "deprioritize_condition_met"
    return "inconclusive_between_thresholds"


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Run word-conditioned transported filter.")
    parser.add_argument("--targeted-dir", type=Path, default=DEFAULT_TARGETED_DIR)
    parser.add_argument("--rule-status", default=DEFAULT_RULE_STATUS)
    parser.add_argument("--baseline-band", action="append")
    parser.add_argument("--fresh-band", action="append")
    parser.add_argument("--max-selected-public-words", type=int, default=0)
    parser.add_argument("--continue-threshold", type=float, default=DEFAULT_CONTINUE_THRESHOLD)
    parser.add_argument("--deprioritize-threshold", type=float, default=DEFAULT_DEPRIORITIZE_THRESHOLD)
    parser.add_argument("--max-ratio-numerator", type=int, default=DEFAULT_MAX_RATIO_NUMERATOR)
    parser.add_argument("--max-ratio-denominator", type=int, default=DEFAULT_MAX_RATIO_DENOMINATOR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    """Run baseline selection and fresh word-conditioned measurement."""
    args = parse_args(argv)
    baseline_bands = (
        parse_bands(args.baseline_band)
        if args.baseline_band
        else list(DEFAULT_BASELINE_BANDS)
    )
    fresh_bands = (
        parse_bands(args.fresh_band)
        if args.fresh_band
        else list(DEFAULT_FRESH_BANDS)
    )
    rules_by_public = load_rules(args.targeted_dir, args.rule_status)

    baseline_rows, baseline_band_summaries = measure_bands(
        baseline_bands,
        rules_by_public,
        args.max_ratio_numerator,
        args.max_ratio_denominator,
    )
    baseline_stats = public_word_stats(baseline_rows)
    selected_rows = select_public_words(
        baseline_stats,
        args.max_selected_public_words,
    )
    selected_public_words = {str(row["public_word"]) for row in selected_rows}

    fresh_rows, fresh_band_summaries = measure_bands(
        fresh_bands,
        rules_by_public,
        args.max_ratio_numerator,
        args.max_ratio_denominator,
    )
    fresh_stats = [
        row
        for row in public_word_stats(fresh_rows)
        if str(row["public_word"]) in selected_public_words
    ]
    baseline_aggregate = aggregate_selected_rows(baseline_rows, selected_public_words)
    fresh_aggregate = aggregate_selected_rows(fresh_rows, selected_public_words)

    summary = {
        "rule_id": RULE_ID,
        "status": "measured_public_grammar_word_conditioned_transported_filter",
        "theorem_status": "hypothesis_not_proved",
        "inference_status": "not_live_pedk_inference",
        "candidate_space_kind": "fixed_N_public_endpoint_x_with_floor_transport_y",
        "transported_class_boundary": "existing_endpoint_endpoint_class_only_when_y_is_endpoint",
        "selection_basis": "baseline_public_words_with_positive_elimination_and_zero_true_p_loss",
        "selected_rule_status": args.rule_status,
        "selected_public_word_count": len(selected_public_words),
        "selected_public_words": sorted(selected_public_words),
        "baseline_band_summaries": baseline_band_summaries,
        "fresh_band_summaries": fresh_band_summaries,
        "baseline_aggregate": baseline_aggregate,
        "fresh_aggregate": fresh_aggregate,
        "continue_threshold": args.continue_threshold,
        "deprioritize_threshold": args.deprioritize_threshold,
        "outcome_status": outcome_status(
            fresh_aggregate,
            args.continue_threshold,
            args.deprioritize_threshold,
        ),
    }

    args.output_dir.mkdir(parents=True, exist_ok=True)
    write_jsonl(args.output_dir / "baseline_public_word_stats.jsonl", baseline_stats)
    write_jsonl(args.output_dir / "selected_public_word_rows.jsonl", selected_rows)
    write_jsonl(args.output_dir / "fresh_public_word_stats.jsonl", fresh_stats)
    write_jsonl(
        args.output_dir / "fresh_selected_candidate_rows.jsonl",
        [
            row
            for row in fresh_rows
            if str(row["public_word"]) in selected_public_words
        ],
    )
    write_json(args.output_dir / "summary.json", summary)
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
