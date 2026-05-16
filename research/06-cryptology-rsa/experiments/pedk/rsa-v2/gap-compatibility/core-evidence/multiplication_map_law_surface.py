#!/usr/bin/env python3
"""Build the observed PEDK multiplication map between N and factor gap words."""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path

from first_gap_compatibility_check import (
    DEFAULT_MAX_RATIO_DENOMINATOR,
    DEFAULT_MAX_RATIO_NUMERATOR,
    corpus_row,
    semiprime_triples,
    write_json,
    write_jsonl,
)
from public_feature_all_o6_boundary import band_key, parse_bands


THIS_DIR = Path(__file__).resolve().parent
DEFAULT_OUTPUT_DIR = THIS_DIR / "output" / "multiplication_map_law_surface_601_5500"
RULE_ID = "pedk_multiplication_map_law_surface_v1"
DEFAULT_BANDS = (
    (601, 1000),
    (1001, 1400),
    (1401, 1800),
    (1801, 2200),
    (2201, 2600),
    (2601, 3000),
    (3001, 3500),
    (3501, 4000),
    (4001, 4500),
    (4501, 5000),
    (5001, 5500),
)
DEFAULT_MIN_PUBLIC_SUPPORT = 50
DEFAULT_MIN_FACTOR_SUPPORT = 20


def containing_word(row: dict[str, object]) -> str:
    """Return exact containing-gap type with N phase."""
    containing = row["n_gaps"]["containing"]
    return f"{containing['exact_type_key']}@{row['n_containing_gap_phase_bucket']}"


def public_word(row: dict[str, object]) -> str:
    """Return the local public word around N."""
    gaps = row["n_gaps"]
    return "|".join(
        (
            f"prev={gaps['previous']['reduced_state']}",
            f"containing={containing_word(row)}",
            f"next={gaps['following']['reduced_state']}",
        )
    )


def factor_word(row: dict[str, object]) -> str:
    """Return unordered factor-neighborhood word."""
    return str(row["factor_phased_neighborhood_signature"])


def top_rows(counter: Counter[str], limit: int) -> list[dict[str, object]]:
    """Return top counter entries in deterministic order."""
    return [
        {"value": value, "count": count}
        for value, count in sorted(counter.items(), key=lambda item: (-item[1], item[0]))[:limit]
    ]


def build_surface(
    bands: list[tuple[int, int]],
    max_ratio_numerator: int,
    max_ratio_denominator: int,
    min_public_support: int,
    min_factor_support: int,
) -> tuple[list[dict[str, object]], list[dict[str, object]], list[dict[str, object]], dict[str, object]]:
    """Return observed compatibility cells and candidate exclusion cells."""
    public_counts = Counter()
    factor_counts = Counter()
    cell_counts = Counter()
    public_to_factor: dict[str, Counter[str]] = defaultdict(Counter)
    semiprime_counts: dict[str, int] = {}

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
            row = corpus_row(triple)
            n_word = public_word(row)
            pq_word = factor_word(row)
            public_counts[n_word] += 1
            factor_counts[pq_word] += 1
            cell_counts[(n_word, pq_word)] += 1
            public_to_factor[n_word][pq_word] += 1

    public_rows = [
        {
            "rule_id": RULE_ID,
            "public_word": word,
            "forward_row_count": count,
            "observed_factor_word_count": len(public_to_factor[word]),
            "top_factor_words": top_rows(public_to_factor[word], 5),
        }
        for word, count in sorted(public_counts.items(), key=lambda item: (-item[1], item[0]))
    ]
    factor_rows = [
        {
            "rule_id": RULE_ID,
            "factor_word": word,
            "forward_row_count": count,
        }
        for word, count in sorted(factor_counts.items(), key=lambda item: (-item[1], item[0]))
    ]
    cell_rows = [
        {
            "rule_id": RULE_ID,
            "public_word": n_word,
            "factor_word": pq_word,
            "forward_row_count": count,
        }
        for (n_word, pq_word), count in sorted(
            cell_counts.items(),
            key=lambda item: (-item[1], item[0][0], item[0][1]),
        )
    ]

    supported_public_words = [
        word
        for word, count in public_counts.items()
        if count >= min_public_support
    ]
    supported_factor_words = [
        word
        for word, count in factor_counts.items()
        if count >= min_factor_support
    ]
    exclusion_rows = []
    for n_word in sorted(supported_public_words):
        for pq_word in sorted(supported_factor_words):
            if cell_counts[(n_word, pq_word)]:
                continue
            exclusion_rows.append(
                {
                    "rule_id": RULE_ID,
                    "public_word": n_word,
                    "factor_word": pq_word,
                    "public_word_support": public_counts[n_word],
                    "factor_word_support": factor_counts[pq_word],
                    "status": "candidate_exclusion_not_observed",
                }
            )

    summary = {
        "rule_id": RULE_ID,
        "status": "measured_multiplication_map_surface",
        "theorem_status": "hypothesis_not_proved",
        "inference_status": "not_live_pedk_inference",
        "public_word_count": len(public_counts),
        "factor_word_count": len(factor_counts),
        "observed_cell_count": len(cell_counts),
        "supported_public_word_count": len(supported_public_words),
        "supported_factor_word_count": len(supported_factor_words),
        "candidate_exclusion_count": len(exclusion_rows),
        "min_public_support": min_public_support,
        "min_factor_support": min_factor_support,
        "semiprime_counts_by_band": semiprime_counts,
    }
    return public_rows, factor_rows, cell_rows + exclusion_rows, summary


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Build PEDK multiplication-map surface.")
    parser.add_argument("--band", action="append")
    parser.add_argument("--max-ratio-numerator", type=int, default=DEFAULT_MAX_RATIO_NUMERATOR)
    parser.add_argument("--max-ratio-denominator", type=int, default=DEFAULT_MAX_RATIO_DENOMINATOR)
    parser.add_argument("--min-public-support", type=int, default=DEFAULT_MIN_PUBLIC_SUPPORT)
    parser.add_argument("--min-factor-support", type=int, default=DEFAULT_MIN_FACTOR_SUPPORT)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    """Run multiplication-map extraction."""
    args = parse_args(argv)
    bands = parse_bands(args.band) if args.band else list(DEFAULT_BANDS)
    public_rows, factor_rows, cell_rows, summary = build_surface(
        bands,
        args.max_ratio_numerator,
        args.max_ratio_denominator,
        args.min_public_support,
        args.min_factor_support,
    )
    summary["bands"] = [
        {
            "min_factor": min_factor,
            "max_factor": max_factor,
            "max_factor_ratio": f"{args.max_ratio_numerator}/{args.max_ratio_denominator}",
        }
        for min_factor, max_factor in bands
    ]

    args.output_dir.mkdir(parents=True, exist_ok=True)
    write_jsonl(args.output_dir / "public_word_rows.jsonl", public_rows)
    write_jsonl(args.output_dir / "factor_word_rows.jsonl", factor_rows)
    write_jsonl(args.output_dir / "map_cell_rows.jsonl", cell_rows)
    write_json(args.output_dir / "summary.json", summary)
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
