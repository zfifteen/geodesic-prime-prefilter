#!/usr/bin/env python3
"""Measure fixed-N transported candidate reduction from public grammar rules."""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from math import isqrt
from pathlib import Path

from first_gap_compatibility_check import (
    DEFAULT_MAX_RATIO_DENOMINATOR,
    DEFAULT_MAX_RATIO_NUMERATOR,
    factor_neighborhood,
    grammar_around_coordinate,
    ordered_factor_phased_signature,
    pgs_endpoints_through,
    relative_phase_bucket,
    semiprime_triples,
    write_json,
    write_jsonl,
)
from multiplication_map_law_surface import public_word as surface_public_word
from public_feature_all_o6_boundary import band_key, parse_bands
from public_grammar_pivot import factor_phase_multiset, factor_residue_multiset, read_jsonl


THIS_DIR = Path(__file__).resolve().parent
DEFAULT_TARGETED_DIR = THIS_DIR / "output" / "public_grammar_targeted_slice_check_5501_7500"
DEFAULT_OUTPUT_DIR = THIS_DIR / "output" / "public_grammar_transported_candidate_filter_5501_7500"
DEFAULT_BANDS = ((5501, 6500), (6501, 7500))
DEFAULT_RULE_STATUS = "survived_fresh_public_slice"
RULE_ID = "pedk_public_grammar_transported_candidate_filter_v1"


def load_rules(targeted_dir: Path, rule_status: str) -> dict[str, set[tuple[str, str]]]:
    """Return survived exclusion classes keyed by public word."""
    rules_by_public: dict[str, set[tuple[str, str]]] = defaultdict(set)
    rows = read_jsonl(targeted_dir / "targeted_result_rows.jsonl")
    for row in rows:
        if str(row["status"]) != rule_status:
            continue
        rules_by_public[str(row["public_word"])].add(
            (
                str(row["factor_residue_multiset"]),
                str(row["factor_phase_multiset"]),
            )
        )
    if not rules_by_public:
        raise ValueError(f"no targeted rows with status {rule_status!r}")
    return dict(rules_by_public)


def public_word_for_n(n_value: int) -> str:
    """Return public grammar word around N from public coordinate data only."""
    n_gaps = grammar_around_coordinate("n", n_value)
    row = {
        "n_gaps": n_gaps,
        "n_containing_gap_phase_bucket": relative_phase_bucket(n_gaps["containing"]),
    }
    return surface_public_word(row)


def endpoint_pair_class(
    x_value: int,
    y_value: int,
    neighborhood_cache: dict[int, dict[str, object]],
) -> tuple[str, str]:
    """Return endpoint-endpoint factor class for a transported endpoint pair."""
    if x_value not in neighborhood_cache:
        neighborhood_cache[x_value] = factor_neighborhood("x", x_value)
    if y_value not in neighborhood_cache:
        neighborhood_cache[y_value] = factor_neighborhood("y", y_value)
    pair_word = ordered_factor_phased_signature(
        neighborhood_cache[x_value],
        neighborhood_cache[y_value],
    )
    return factor_residue_multiset(pair_word), factor_phase_multiset(pair_word)


def band_endpoint_values(bands: list[tuple[int, int]]) -> list[int]:
    """Return endpoint values in the selected measurement bands."""
    max_factor = max(max_factor for _min_factor, max_factor in bands)
    endpoints = pgs_endpoints_through(max_factor)
    return [
        endpoint
        for endpoint in endpoints
        if any(min_factor <= endpoint <= max_factor for min_factor, max_factor in bands)
    ]


def candidate_x_values(
    n_value: int,
    endpoints: list[int],
    min_factor: int,
    max_factor: int,
    max_ratio_numerator: int,
    max_ratio_denominator: int,
) -> list[tuple[int, int, bool]]:
    """Return public x candidates with their transported y and endpoint status."""
    root = isqrt(n_value)
    endpoint_set = set(endpoints)
    candidates: list[tuple[int, int, bool]] = []
    for x_value in endpoints:
        if x_value > root:
            break
        y_value = n_value // x_value
        if y_value < min_factor or y_value > max_factor:
            continue
        if y_value * max_ratio_denominator > x_value * max_ratio_numerator:
            continue
        candidates.append((x_value, y_value, y_value in endpoint_set))
    return candidates


def measure_band(
    min_factor: int,
    max_factor: int,
    rules_by_public: dict[str, set[tuple[str, str]]],
    endpoints: list[int],
    max_ratio_numerator: int,
    max_ratio_denominator: int,
) -> tuple[list[dict[str, object]], dict[str, object]]:
    """Return fixed-N transported candidate reduction rows for one band."""
    rows: list[dict[str, object]] = []
    triples = semiprime_triples(
        min_factor,
        max_factor,
        max_ratio_numerator,
        max_ratio_denominator,
    )
    neighborhood_cache: dict[int, dict[str, object]] = {}
    band = band_key(min_factor, max_factor)

    for triple in triples:
        n_value = triple.n
        n_word = public_word_for_n(n_value)
        excluded_classes = rules_by_public.get(n_word, set())
        candidates = candidate_x_values(
            n_value,
            endpoints,
            min_factor,
            max_factor,
            max_ratio_numerator,
            max_ratio_denominator,
        )
        transported_endpoint_count = 0
        eliminated_count = 0
        true_p_eliminated = False
        true_p_seen = False

        for x_value, y_value, y_is_endpoint in candidates:
            if x_value == triple.p:
                true_p_seen = True
            if not y_is_endpoint:
                continue
            transported_endpoint_count += 1
            pair_class = endpoint_pair_class(x_value, y_value, neighborhood_cache)
            if pair_class not in excluded_classes:
                continue
            eliminated_count += 1
            if x_value == triple.p:
                true_p_eliminated = True

        candidate_count = len(candidates)
        rows.append(
            {
                "rule_id": RULE_ID,
                "band": band,
                "case_id": triple.case_id,
                "N": str(n_value),
                "public_word": n_word,
                "has_survived_rule": bool(excluded_classes),
                "excluded_class_count": len(excluded_classes),
                "candidate_x_count": candidate_count,
                "transported_endpoint_candidate_count": transported_endpoint_count,
                "compatibility_eliminated_candidate_count": eliminated_count,
                "compatibility_eliminated_fraction_of_all_candidates": (
                    eliminated_count / candidate_count if candidate_count else 0.0
                ),
                "compatibility_eliminated_fraction_of_endpoint_candidates": (
                    eliminated_count / transported_endpoint_count
                    if transported_endpoint_count
                    else 0.0
                ),
                "true_p_seen_in_candidate_space": true_p_seen,
                "true_p_eliminated_by_compatibility": true_p_eliminated,
            }
        )

    summary = {
        "band": band,
        "semiprime_count": len(triples),
    }
    return rows, summary


def aggregate_rows(rows: list[dict[str, object]]) -> dict[str, object]:
    """Return aggregate reduction metrics."""
    public_rows: dict[str, Counter[str]] = defaultdict(Counter)
    for row in rows:
        n_word = str(row["public_word"])
        public_rows[n_word]["row_count"] += 1
        public_rows[n_word]["candidate_x_count"] += int(row["candidate_x_count"])
        public_rows[n_word]["transported_endpoint_candidate_count"] += int(
            row["transported_endpoint_candidate_count"]
        )
        public_rows[n_word]["compatibility_eliminated_candidate_count"] += int(
            row["compatibility_eliminated_candidate_count"]
        )
        public_rows[n_word]["true_p_eliminated_by_compatibility"] += int(
            bool(row["true_p_eliminated_by_compatibility"])
        )
        public_rows[n_word]["has_survived_rule"] += int(bool(row["has_survived_rule"]))

    rule_public_rows = []
    for n_word, counts in sorted(public_rows.items()):
        if not counts["has_survived_rule"]:
            continue
        candidate_count = counts["candidate_x_count"]
        endpoint_candidate_count = counts["transported_endpoint_candidate_count"]
        eliminated_count = counts["compatibility_eliminated_candidate_count"]
        rule_public_rows.append(
            {
                "public_word": n_word,
                "row_count": counts["row_count"],
                "candidate_x_count": candidate_count,
                "transported_endpoint_candidate_count": endpoint_candidate_count,
                "compatibility_eliminated_candidate_count": eliminated_count,
                "compatibility_eliminated_fraction_of_all_candidates": (
                    eliminated_count / candidate_count if candidate_count else 0.0
                ),
                "compatibility_eliminated_fraction_of_endpoint_candidates": (
                    eliminated_count / endpoint_candidate_count
                    if endpoint_candidate_count
                    else 0.0
                ),
                "true_p_eliminated_by_compatibility_count": counts[
                    "true_p_eliminated_by_compatibility"
                ],
            }
        )

    total_candidate_count = sum(int(row["candidate_x_count"]) for row in rows)
    total_endpoint_candidate_count = sum(
        int(row["transported_endpoint_candidate_count"]) for row in rows
    )
    total_eliminated_count = sum(
        int(row["compatibility_eliminated_candidate_count"]) for row in rows
    )
    true_p_eliminated_count = sum(
        int(bool(row["true_p_eliminated_by_compatibility"])) for row in rows
    )

    return {
        "row_count": len(rows),
        "public_word_with_survived_rule_count": len(rule_public_rows),
        "candidate_x_count": total_candidate_count,
        "transported_endpoint_candidate_count": total_endpoint_candidate_count,
        "compatibility_eliminated_candidate_count": total_eliminated_count,
        "compatibility_eliminated_fraction_of_all_candidates": (
            total_eliminated_count / total_candidate_count if total_candidate_count else 0.0
        ),
        "compatibility_eliminated_fraction_of_endpoint_candidates": (
            total_eliminated_count / total_endpoint_candidate_count
            if total_endpoint_candidate_count
            else 0.0
        ),
        "true_p_eliminated_by_compatibility_count": true_p_eliminated_count,
        "survived_rule_public_word_rows": rule_public_rows,
    }


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Measure transported candidate filtering.")
    parser.add_argument("--targeted-dir", type=Path, default=DEFAULT_TARGETED_DIR)
    parser.add_argument("--rule-status", default=DEFAULT_RULE_STATUS)
    parser.add_argument("--band", action="append")
    parser.add_argument("--max-ratio-numerator", type=int, default=DEFAULT_MAX_RATIO_NUMERATOR)
    parser.add_argument("--max-ratio-denominator", type=int, default=DEFAULT_MAX_RATIO_DENOMINATOR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    """Run fixed-N transported candidate filter measurement."""
    args = parse_args(argv)
    bands = parse_bands(args.band) if args.band else list(DEFAULT_BANDS)
    rules_by_public = load_rules(args.targeted_dir, args.rule_status)
    endpoints = band_endpoint_values(bands)
    rows: list[dict[str, object]] = []
    band_summaries = []
    for min_factor, max_factor in bands:
        band_rows, band_summary = measure_band(
            min_factor,
            max_factor,
            rules_by_public,
            endpoints,
            args.max_ratio_numerator,
            args.max_ratio_denominator,
        )
        rows.extend(band_rows)
        band_summaries.append(band_summary)

    summary = {
        "rule_id": RULE_ID,
        "status": "measured_public_grammar_transported_candidate_filter",
        "theorem_status": "hypothesis_not_proved",
        "inference_status": "not_live_pedk_inference",
        "candidate_space_kind": "fixed_N_public_endpoint_x_with_floor_transport_y",
        "transported_class_boundary": "existing_endpoint_endpoint_class_only_when_y_is_endpoint",
        "selected_rule_status": args.rule_status,
        "selected_public_word_count": len(rules_by_public),
        "band_summaries": band_summaries,
        "bands": [
            {
                "min_factor": min_factor,
                "max_factor": max_factor,
                "max_factor_ratio": f"{args.max_ratio_numerator}/{args.max_ratio_denominator}",
            }
            for min_factor, max_factor in bands
        ],
        "aggregate": aggregate_rows(rows),
    }

    args.output_dir.mkdir(parents=True, exist_ok=True)
    write_jsonl(args.output_dir / "transported_candidate_rows.jsonl", rows)
    write_json(args.output_dir / "summary.json", summary)
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
