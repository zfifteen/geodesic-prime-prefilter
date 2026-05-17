#!/usr/bin/env python3
"""Run fresh targeted checks for public-grammar factor exclusion candidates."""

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
from multiplication_map_law_surface import factor_word, public_word
from public_feature_all_o6_boundary import band_key, parse_bands
from public_grammar_pivot import factor_phase_multiset, factor_residue_multiset, read_jsonl


THIS_DIR = Path(__file__).resolve().parent
DEFAULT_CANDIDATE_PATH = (
    THIS_DIR
    / "output"
    / "public_grammar_factor_exclusion_pivot_601_5500"
    / "candidate_class_exclusion_rows.jsonl"
)
DEFAULT_OUTPUT_DIR = THIS_DIR / "output" / "public_grammar_targeted_slice_check_5501_6500"
RULE_ID = "pedk_public_grammar_targeted_slice_check_v1"
DEFAULT_BANDS = ((5501, 6500),)
DEFAULT_TOP_N = 5


def selected_candidates(candidate_path: Path, top_n: int) -> list[dict[str, object]]:
    """Return top candidate rows in existing deterministic order."""
    rows = read_jsonl(candidate_path)
    if top_n < 1:
        raise ValueError("top_n must be positive")
    selected = rows[:top_n]
    for index, row in enumerate(selected, 1):
        row["candidate_rank"] = index
    return selected


def check_candidates(
    candidates: list[dict[str, object]],
    bands: list[tuple[int, int]],
    max_ratio_numerator: int,
    max_ratio_denominator: int,
) -> tuple[list[dict[str, object]], list[dict[str, object]], dict[str, object]]:
    """Run fresh public-slice checks for selected candidates."""
    public_to_indices: dict[str, list[int]] = defaultdict(list)
    for index, candidate in enumerate(candidates):
        public_to_indices[str(candidate["public_word"])].append(index)

    public_slice_counts = Counter()
    factor_class_hits = Counter()
    observed_factor_classes: dict[int, Counter[str]] = defaultdict(Counter)
    falsification_rows: list[dict[str, object]] = []
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
            candidate_indices = public_to_indices.get(n_word)
            if not candidate_indices:
                continue
            pq_word = factor_word(row)
            residue_key = factor_residue_multiset(pq_word)
            phase_key = factor_phase_multiset(pq_word)
            class_key = f"{residue_key} || {phase_key}"
            for index in candidate_indices:
                candidate = candidates[index]
                public_slice_counts[index] += 1
                observed_factor_classes[index][class_key] += 1
                if (
                    residue_key == str(candidate["factor_residue_multiset"])
                    and phase_key == str(candidate["factor_phase_multiset"])
                ):
                    factor_class_hits[index] += 1
                    falsification_rows.append(
                        {
                            "rule_id": RULE_ID,
                            "candidate_rank": candidate["candidate_rank"],
                            "case_id": row["case_id"],
                            "band": band,
                            "N": row["N"],
                            "p": row["p"],
                            "q": row["q"],
                            "public_word": n_word,
                            "factor_word": pq_word,
                            "factor_residue_multiset": residue_key,
                            "factor_phase_multiset": phase_key,
                        }
                    )

    result_rows = []
    for index, candidate in enumerate(candidates):
        public_count = public_slice_counts[index]
        hit_count = factor_class_hits[index]
        if public_count == 0:
            status = "untested_no_fresh_public_slice"
        elif hit_count == 0:
            status = "survived_fresh_public_slice"
        else:
            status = "falsified_fresh_public_slice"
        result_rows.append(
            {
                "rule_id": RULE_ID,
                "candidate_rank": candidate["candidate_rank"],
                "status": status,
                "public_word": candidate["public_word"],
                "factor_residue_multiset": candidate["factor_residue_multiset"],
                "factor_phase_multiset": candidate["factor_phase_multiset"],
                "training_public_forward_row_count": candidate["public_forward_row_count"],
                "training_excluded_factor_word_count": candidate["excluded_factor_word_count"],
                "training_excluded_factor_support_total": candidate["excluded_factor_support_total"],
                "fresh_public_slice_row_count": public_count,
                "fresh_falsification_row_count": hit_count,
                "fresh_observed_factor_class_count": len(observed_factor_classes[index]),
                "top_fresh_factor_classes": [
                    {"value": value, "count": count}
                    for value, count in sorted(
                        observed_factor_classes[index].items(),
                        key=lambda item: (-item[1], item[0]),
                    )[:8]
                ],
            }
        )

    status_counts = Counter(str(row["status"]) for row in result_rows)
    summary = {
        "rule_id": RULE_ID,
        "status": "measured_public_grammar_targeted_slice_check",
        "theorem_status": "hypothesis_not_proved",
        "inference_status": "not_live_pedk_inference",
        "candidate_count": len(candidates),
        "status_counts": dict(sorted(status_counts.items())),
        "falsification_row_count": len(falsification_rows),
        "semiprime_counts_by_band": semiprime_counts,
    }
    return result_rows, falsification_rows, summary


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Run targeted public-grammar slice checks.")
    parser.add_argument("--candidate-path", type=Path, default=DEFAULT_CANDIDATE_PATH)
    parser.add_argument("--top-n", type=int, default=DEFAULT_TOP_N)
    parser.add_argument("--band", action="append")
    parser.add_argument("--max-ratio-numerator", type=int, default=DEFAULT_MAX_RATIO_NUMERATOR)
    parser.add_argument("--max-ratio-denominator", type=int, default=DEFAULT_MAX_RATIO_DENOMINATOR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    """Run fresh targeted slice check."""
    args = parse_args(argv)
    bands = parse_bands(args.band) if args.band else list(DEFAULT_BANDS)
    candidates = selected_candidates(args.candidate_path, args.top_n)
    result_rows, falsification_rows, summary = check_candidates(
        candidates,
        bands,
        args.max_ratio_numerator,
        args.max_ratio_denominator,
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
    write_jsonl(args.output_dir / "selected_candidate_rows.jsonl", candidates)
    write_jsonl(args.output_dir / "targeted_result_rows.jsonl", result_rows)
    write_jsonl(args.output_dir / "falsification_rows.jsonl", falsification_rows)
    write_json(args.output_dir / "summary.json", summary)
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
