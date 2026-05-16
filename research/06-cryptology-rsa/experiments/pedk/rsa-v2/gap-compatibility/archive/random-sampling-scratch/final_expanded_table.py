#!/usr/bin/env python3
"""
Final Expanded Gap Compatibility Table

This script combines:
- The 3 official rungs
- The 6 toy cases from previous expansion
- 4 additional randomly sampled cases from the large pre-computed corpus (gap_compatibility_search/corpus_rows.jsonl)

It produces one clean table using the position-bucketed classification.
"""

import json
import random
from pathlib import Path


def load_corpus(path):
    with open(path) as f:
        return [json.loads(line) for line in f if line.strip()]


def main():
    base = Path(__file__).parent

    # 1. Official + previously expanded cases (from fourth script)
    previous = load_corpus(base / "output" / "gap_compatibility_expanded_corpus.jsonl")

    # 2. Sample 4 more from the large search corpus
    large_corpus = load_corpus(base / "output" / "gap_compatibility_search" / "corpus_rows.jsonl")

    # Prefer cases around 40-60 bits if available
    candidates = [r for r in large_corpus if 38 <= r.get("bits", 0) <= 55]
    random.seed(42)
    if len(candidates) >= 4:
        additional = random.sample(candidates, 4)
    else:
        additional = random.sample(large_corpus, 4)

    # Build final table
    print("Final Expanded Gap Compatibility Corpus (13 cases)")
    print("=" * 110)
    print(f"{'case_id':<35} {'bits':>4} {'gap(N) State':<28} {'gap(N) Bucket':<12} {'rel_pos':>7}")
    print("-" * 110)

    all_cases = previous + additional

    for r in all_cases:
        state = r.get("n_containing_gap_reduced_state") or r.get("gap_N_state", "N/A")
        bucket = r.get("n_containing_gap_position_bucket") or r.get("gap_N_bucket", "N/A")
        rel_pos = r.get("n_containing_gap_position_mpermille")
        if rel_pos is not None:
            rel_pos = round(rel_pos / 1000, 3)
        else:
            rel_pos = r.get("gap_N_rel_pos", "?")

        print(f"{r['case_id']:<35} {r['bits']:>4} {state:<28} {bucket:<12} {rel_pos:>7}")

    print("\nNote: Additional 4 cases sampled from gap_compatibility_search/corpus_rows.jsonl")


if __name__ == "__main__":
    main()
