#!/usr/bin/env python3
"""Measure endpoint-pair reduction from survived public-grammar exclusions."""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path

from first_gap_compatibility_check import (
    DEFAULT_MAX_RATIO_DENOMINATOR,
    DEFAULT_MAX_RATIO_NUMERATOR,
    factor_neighborhood,
    ordered_factor_phased_signature,
    semiprime_triples,
    write_json,
    write_jsonl,
)
from public_feature_all_o6_boundary import band_key, parse_bands
from public_grammar_pivot import factor_phase_multiset, factor_residue_multiset, read_jsonl


THIS_DIR = Path(__file__).resolve().parent
DEFAULT_TARGETED_DIR = THIS_DIR / "output" / "public_grammar_targeted_slice_check_5501_7500"
DEFAULT_OUTPUT_DIR = THIS_DIR / "output" / "public_grammar_endpoint_space_reduction_5501_7500"
DEFAULT_BANDS = ((5501, 6500), (6501, 7500))
DEFAULT_RULE_STATUS = "survived_fresh_public_slice"
RULE_ID = "pedk_public_grammar_endpoint_space_reduction_v1"


def endpoint_class_key(
    p_value: int,
    q_value: int,
    neighborhood_cache: dict[int, dict[str, object]],
) -> tuple[str, str]:
    """Return the factor residue and phase class for one endpoint pair."""
    if p_value not in neighborhood_cache:
        neighborhood_cache[p_value] = factor_neighborhood("endpoint", p_value)
    if q_value not in neighborhood_cache:
        neighborhood_cache[q_value] = factor_neighborhood("endpoint", q_value)
    pq_word = ordered_factor_phased_signature(
        neighborhood_cache[p_value],
        neighborhood_cache[q_value],
    )
    return factor_residue_multiset(pq_word), factor_phase_multiset(pq_word)


def load_rules(targeted_dir: Path, rule_status: str) -> list[dict[str, object]]:
    """Return targeted-slice rows with the selected status."""
    rows = read_jsonl(targeted_dir / "targeted_result_rows.jsonl")
    rules = [row for row in rows if str(row["status"]) == rule_status]
    if not rules:
        raise ValueError(f"no targeted rows with status {rule_status!r}")
    return rules


def build_endpoint_space(
    bands: list[tuple[int, int]],
    max_ratio_numerator: int,
    max_ratio_denominator: int,
) -> tuple[list[dict[str, object]], Counter[tuple[str, str]], dict[str, int]]:
    """Return endpoint-pair rows and their factor-class counts."""
    endpoint_rows: list[dict[str, object]] = []
    class_counts: Counter[tuple[str, str]] = Counter()
    semiprime_counts: dict[str, int] = {}
    neighborhood_cache: dict[int, dict[str, object]] = {}

    for min_factor, max_factor in bands:
        band = band_key(min_factor, max_factor)
        triples = semiprime_triples(
            min_factor,
            max_factor,
            max_ratio_numerator,
            max_ratio_denominator,
        )
        semiprime_counts[band] = len(triples)
        for triple in triples:
            residue_key, phase_key = endpoint_class_key(
                triple.p,
                triple.q,
                neighborhood_cache,
            )
            class_counts[(residue_key, phase_key)] += 1
            endpoint_rows.append(
                {
                    "band": band,
                    "case_id": triple.case_id,
                    "p": str(triple.p),
                    "q": str(triple.q),
                    "factor_residue_multiset": residue_key,
                    "factor_phase_multiset": phase_key,
                }
            )

    return endpoint_rows, class_counts, semiprime_counts


def reduction_rows(
    rules: list[dict[str, object]],
    endpoint_rows: list[dict[str, object]],
    class_counts: Counter[tuple[str, str]],
) -> list[dict[str, object]]:
    """Return endpoint-pair reduction rows for each public word."""
    rules_by_public: dict[str, list[dict[str, object]]] = defaultdict(list)
    for rule in rules:
        rules_by_public[str(rule["public_word"])].append(rule)

    total_pair_count = len(endpoint_rows)
    total_endpoint_incident_count = Counter()
    for row in endpoint_rows:
        total_endpoint_incident_count[str(row["p"])] += 1
        total_endpoint_incident_count[str(row["q"])] += 1
    total_endpoint_count = len(total_endpoint_incident_count)
    rows: list[dict[str, object]] = []
    for n_word, public_rules in sorted(rules_by_public.items()):
        excluded_classes = {
            (
                str(rule["factor_residue_multiset"]),
                str(rule["factor_phase_multiset"]),
            )
            for rule in public_rules
        }
        eliminated_pair_count = sum(class_counts[key] for key in excluded_classes)
        fresh_public_hit_count = sum(
            int(rule["fresh_falsification_row_count"])
            for rule in public_rules
        )
        fresh_public_slice_row_count = max(
            int(rule["fresh_public_slice_row_count"])
            for rule in public_rules
        )
        eliminated_endpoint_incident_count = Counter()
        for row in endpoint_rows:
            row_class = (
                str(row["factor_residue_multiset"]),
                str(row["factor_phase_multiset"]),
            )
            if row_class not in excluded_classes:
                continue
            eliminated_endpoint_incident_count[str(row["p"])] += 1
            eliminated_endpoint_incident_count[str(row["q"])] += 1
        touched_endpoint_count = len(eliminated_endpoint_incident_count)
        fully_eliminated_endpoint_count = sum(
            1
            for endpoint, total_count in total_endpoint_incident_count.items()
            if eliminated_endpoint_incident_count[endpoint] == total_count
        )

        survivor_pair_count = total_pair_count - eliminated_pair_count
        rows.append(
            {
                "rule_id": RULE_ID,
                "public_word": n_word,
                "candidate_ranks": [int(rule["candidate_rank"]) for rule in public_rules],
                "excluded_factor_classes": [
                    {
                        "factor_residue_multiset": residue_key,
                        "factor_phase_multiset": phase_key,
                        "endpoint_pair_count": class_counts[(residue_key, phase_key)],
                    }
                    for residue_key, phase_key in sorted(excluded_classes)
                ],
                "endpoint_space_kind": "unordered_endpoint_pair_space",
                "endpoint_pair_count": total_pair_count,
                "eliminated_endpoint_pair_count": eliminated_pair_count,
                "surviving_endpoint_pair_count": survivor_pair_count,
                "endpoint_projection_kind": "individual_endpoint_incidence_projection",
                "endpoint_count": total_endpoint_count,
                "touched_endpoint_count": touched_endpoint_count,
                "touched_endpoint_fraction": (
                    touched_endpoint_count / total_endpoint_count if total_endpoint_count else 0.0
                ),
                "fully_eliminated_endpoint_count": fully_eliminated_endpoint_count,
                "eliminated_endpoint_pair_fraction": (
                    eliminated_pair_count / total_pair_count if total_pair_count else 0.0
                ),
                "surviving_endpoint_pair_fraction": (
                    survivor_pair_count / total_pair_count if total_pair_count else 0.0
                ),
                "reduction_factor": (
                    total_pair_count / survivor_pair_count if survivor_pair_count else None
                ),
                "fresh_public_slice_row_count": fresh_public_slice_row_count,
                "fresh_public_slice_eliminated_actual_count": fresh_public_hit_count,
                "fresh_public_slice_status": (
                    "survived_endpoint_space_audit"
                    if fresh_public_hit_count == 0
                    else "falsified_endpoint_space_audit"
                ),
            }
        )
    return rows


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Measure endpoint-space reduction.")
    parser.add_argument("--targeted-dir", type=Path, default=DEFAULT_TARGETED_DIR)
    parser.add_argument("--rule-status", default=DEFAULT_RULE_STATUS)
    parser.add_argument("--band", action="append")
    parser.add_argument("--max-ratio-numerator", type=int, default=DEFAULT_MAX_RATIO_NUMERATOR)
    parser.add_argument("--max-ratio-denominator", type=int, default=DEFAULT_MAX_RATIO_DENOMINATOR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    """Run endpoint-pair reduction measurement."""
    args = parse_args(argv)
    bands = parse_bands(args.band) if args.band else list(DEFAULT_BANDS)
    rules = load_rules(args.targeted_dir, args.rule_status)
    endpoint_rows, class_counts, semiprime_counts = build_endpoint_space(
        bands,
        args.max_ratio_numerator,
        args.max_ratio_denominator,
    )
    rows = reduction_rows(rules, endpoint_rows, class_counts)
    status_counts = Counter(str(row["fresh_public_slice_status"]) for row in rows)
    total_pair_count = len(endpoint_rows)
    summary = {
        "rule_id": RULE_ID,
        "status": "measured_public_grammar_endpoint_space_reduction",
        "theorem_status": "hypothesis_not_proved",
        "inference_status": "not_live_pedk_inference",
        "endpoint_space_kind": "unordered_endpoint_pair_space",
        "selected_rule_status": args.rule_status,
        "selected_rule_count": len(rules),
        "public_word_count": len(rows),
        "endpoint_pair_count": total_pair_count,
        "status_counts": dict(sorted(status_counts.items())),
        "semiprime_counts_by_band": semiprime_counts,
        "bands": [
            {
                "min_factor": min_factor,
                "max_factor": max_factor,
                "max_factor_ratio": f"{args.max_ratio_numerator}/{args.max_ratio_denominator}",
            }
            for min_factor, max_factor in bands
        ],
        "top_reduction_rows": sorted(
            [
                {
                    "public_word": row["public_word"],
                    "candidate_ranks": row["candidate_ranks"],
                    "eliminated_endpoint_pair_count": row["eliminated_endpoint_pair_count"],
                    "eliminated_endpoint_pair_fraction": row["eliminated_endpoint_pair_fraction"],
                    "surviving_endpoint_pair_fraction": row["surviving_endpoint_pair_fraction"],
                    "endpoint_count": row["endpoint_count"],
                    "touched_endpoint_count": row["touched_endpoint_count"],
                    "fully_eliminated_endpoint_count": row["fully_eliminated_endpoint_count"],
                    "fresh_public_slice_row_count": row["fresh_public_slice_row_count"],
                    "fresh_public_slice_eliminated_actual_count": row[
                        "fresh_public_slice_eliminated_actual_count"
                    ],
                }
                for row in rows
            ],
            key=lambda row: (-float(row["eliminated_endpoint_pair_fraction"]), row["public_word"]),
        ),
    }

    args.output_dir.mkdir(parents=True, exist_ok=True)
    write_jsonl(args.output_dir / "endpoint_space_reduction_rows.jsonl", rows)
    write_json(args.output_dir / "summary.json", summary)
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
