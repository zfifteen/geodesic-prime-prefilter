#!/usr/bin/env python3
"""Tabulate all-o6 support by public exact subtype."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

from first_gap_compatibility_check import (
    DEFAULT_MAX_RATIO_DENOMINATOR,
    DEFAULT_MAX_RATIO_NUMERATOR,
    corpus_row,
    semiprime_triples,
    write_json,
    write_jsonl,
)
from public_feature_all_o6_boundary import TARGET_STATES, band_key, is_all_o6, parse_bands


THIS_DIR = Path(__file__).resolve().parent
DEFAULT_OUTPUT_DIR = THIS_DIR / "output" / "exact_subtype_all_o6_boundary_601_5500"
RULE_ID = "pedk_exact_subtype_all_o6_boundary_v1"
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


def phase_state(row: dict[str, object]) -> str:
    """Return public phase state."""
    return str(row["n_containing_gap_phased_state"])


def subtype_rows(
    bands: list[tuple[int, int]],
    max_ratio_numerator: int,
    max_ratio_denominator: int,
) -> tuple[list[dict[str, object]], list[dict[str, object]], dict[str, object]]:
    """Return exact-subtype support rows and all-o6 observation rows."""
    target_states = set(TARGET_STATES)
    support = Counter()
    all_o6_support = Counter()
    observation_rows: list[dict[str, object]] = []
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
            state = phase_state(row)
            if state not in target_states:
                continue
            exact_type = str(row["n_gaps"]["containing"]["exact_type_key"])
            key = (state, exact_type)
            support[key] += 1
            if is_all_o6(str(row["factor_neighborhood_signature"])):
                all_o6_support[key] += 1
                observation_rows.append(
                    {
                        "rule_id": RULE_ID,
                        "case_id": row["case_id"],
                        "band": band,
                        "N": row["N"],
                        "p": row["p"],
                        "q": row["q"],
                        "n_containing_gap_phased_state": state,
                        "n_containing_gap_exact_type_key": exact_type,
                        "n_containing_gap_width": row["n_containing_gap_width"],
                        "n_offset_from_left": row["n_offset_from_left"],
                        "n_offset_from_right": row["n_offset_from_right"],
                        "n_position_mpermille": row["n_containing_gap_position_mpermille"],
                        "factor_neighborhood_signature": row["factor_neighborhood_signature"],
                    }
                )

    rows = []
    for state, exact_type in sorted(support):
        count = support[(state, exact_type)]
        all_o6_count = all_o6_support[(state, exact_type)]
        rows.append(
            {
                "rule_id": RULE_ID,
                "n_containing_gap_phased_state": state,
                "n_containing_gap_exact_type_key": exact_type,
                "forward_row_count": count,
                "all_o6_observation_count": all_o6_count,
                "all_o6_rate_mpermille": all_o6_count * 1000 // count,
                "all_o6_status": (
                    "all_o6_compatible_observed"
                    if all_o6_count
                    else "all_o6_not_observed"
                ),
            }
        )

    zero_all_o6 = [row for row in rows if row["all_o6_observation_count"] == 0]
    summary = {
        "rule_id": RULE_ID,
        "status": "measured_exact_subtype_all_o6_boundary",
        "theorem_status": "hypothesis_not_proved",
        "inference_status": "not_live_pedk_inference",
        "exact_subtype_cell_count": len(rows),
        "all_o6_compatible_cell_count": len(rows) - len(zero_all_o6),
        "all_o6_not_observed_cell_count": len(zero_all_o6),
        "all_o6_observation_count": len(observation_rows),
        "semiprime_counts_by_band": semiprime_counts,
    }
    return rows, observation_rows, summary


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Tabulate all-o6 support by exact subtype.")
    parser.add_argument("--band", action="append")
    parser.add_argument("--max-ratio-numerator", type=int, default=DEFAULT_MAX_RATIO_NUMERATOR)
    parser.add_argument("--max-ratio-denominator", type=int, default=DEFAULT_MAX_RATIO_DENOMINATOR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    """Run exact-subtype all-o6 tabulation."""
    args = parse_args(argv)
    bands = parse_bands(args.band) if args.band else list(DEFAULT_BANDS)
    rows, observation_rows, summary = subtype_rows(
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
    write_jsonl(args.output_dir / "exact_subtype_rows.jsonl", rows)
    write_jsonl(args.output_dir / "all_o6_observation_rows.jsonl", observation_rows)
    write_json(args.output_dir / "summary.json", summary)
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
