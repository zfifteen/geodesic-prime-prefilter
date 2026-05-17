#!/usr/bin/env python3
"""Check forward-stable PEDK exclusions across public gap-width buckets."""

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
from forward_stable_survivor_prediction import (
    DEFAULT_MAX_FACTOR,
    DEFAULT_MIN_FACTOR,
    RULE_ID as FORWARD_RULE_ID,
)


THIS_DIR = Path(__file__).resolve().parent
INPUT_PATH = (
    THIS_DIR
    / "output"
    / "forward_stable_survivor_prediction"
    / "stable_pair_forward_rows.jsonl"
)
DEFAULT_OUTPUT_DIR = THIS_DIR / "output" / "public_axis_stability_check"
RULE_ID = "pedk_public_gap_width_stability_check_v1"


def read_jsonl(path: Path) -> list[dict[str, object]]:
    """Read LF-delimited JSON rows."""
    rows: list[dict[str, object]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def survivor_pairs(rows: list[dict[str, object]]) -> set[tuple[str, str]]:
    """Return forward-stable survivor pairs."""
    return {
        (
            str(row["n_containing_gap_phased_state"]),
            str(row["excluded_factor_neighborhood_signature"]),
        )
        for row in rows
        if row["candidate_status"] == "survived_fresh_band"
    }


def phase_state(row: dict[str, object]) -> str:
    """Return public phase state."""
    return str(row["n_containing_gap_phased_state"])


def factor_signature(row: dict[str, object]) -> str:
    """Return downstream factor-neighborhood label."""
    return str(row["factor_neighborhood_signature"])


def public_width(row: dict[str, object]) -> int:
    """Return public gap width of the gap containing N."""
    return int(str(row["n_containing_gap_width"]))


def width_bucket(width: int) -> str:
    """Return a fixed public gap-width bucket."""
    if width <= 16:
        return "width_006_016"
    if width <= 32:
        return "width_018_032"
    if width <= 48:
        return "width_034_048"
    return "width_050_plus"


def stability_rows(
    pairs: set[tuple[str, str]],
    forward_rows: list[dict[str, object]],
) -> tuple[list[dict[str, object]], list[dict[str, object]], list[dict[str, object]], dict[str, object]]:
    """Return pair-by-width rows, falsifications, bucket rows, and aggregate counts."""
    width_buckets = ("width_006_016", "width_018_032", "width_034_048", "width_050_plus")
    state_bucket_support = Counter(
        (phase_state(row), width_bucket(public_width(row)))
        for row in forward_rows
    )
    bucket_support = Counter(width_bucket(public_width(row)) for row in forward_rows)
    pair_bucket_falsifications = Counter(
        (phase_state(row), factor_signature(row), width_bucket(public_width(row)))
        for row in forward_rows
        if (phase_state(row), factor_signature(row)) in pairs
    )

    pair_width_rows: list[dict[str, object]] = []
    falsification_rows: list[dict[str, object]] = []
    for state, signature in sorted(pairs):
        for bucket in width_buckets:
            support = state_bucket_support[(state, bucket)]
            falsifications = pair_bucket_falsifications[(state, signature, bucket)]
            if support == 0:
                status = "untested_no_forward_rows_for_state_width_bucket"
                absence_mpermille = None
            elif falsifications == 0:
                status = "survived_public_width_bucket"
                absence_mpermille = 1000
            else:
                status = "falsified_in_public_width_bucket"
                absence_mpermille = (support - falsifications) * 1000 // support
            pair_width_rows.append(
                {
                    "rule_id": RULE_ID,
                    "source_rule_id": FORWARD_RULE_ID,
                    "candidate_status": status,
                    "n_containing_gap_phased_state": state,
                    "excluded_factor_neighborhood_signature": signature,
                    "public_width_bucket": bucket,
                    "forward_state_width_support": support,
                    "falsifying_forward_row_count": falsifications,
                    "absence_rate_mpermille": absence_mpermille,
                }
            )

    for row in forward_rows:
        pair = (phase_state(row), factor_signature(row))
        if pair not in pairs:
            continue
        falsification_rows.append(
            {
                "rule_id": RULE_ID,
                "candidate_status": "forward_survivor_falsified_in_public_width_bucket",
                "case_id": row["case_id"],
                "N": row["N"],
                "p": row["p"],
                "q": row["q"],
                "n_containing_gap_phased_state": phase_state(row),
                "public_gap_width": public_width(row),
                "public_width_bucket": width_bucket(public_width(row)),
                "excluded_factor_neighborhood_signature": factor_signature(row),
            }
        )

    bucket_rows = [
        {
            "rule_id": RULE_ID,
            "public_width_bucket": bucket,
            "forward_row_count": bucket_support[bucket],
        }
        for bucket in width_buckets
    ]
    tested_rows = [row for row in pair_width_rows if row["forward_state_width_support"] > 0]
    fully_covered_pairs = sum(
        1
        for state, signature in pairs
        if all(
            state_bucket_support[(state, bucket)] > 0
            for bucket in width_buckets
        )
    )
    aggregate = {
        "forward_survivor_count": len(pairs),
        "public_width_bucket_count": len(width_buckets),
        "pair_width_cell_count": len(pair_width_rows),
        "tested_pair_width_cell_count": len(tested_rows),
        "untested_pair_width_cell_count": len(pair_width_rows) - len(tested_rows),
        "fully_width_covered_pair_count": fully_covered_pairs,
        "falsified_pair_width_cell_count": sum(
            1 for row in pair_width_rows if row["falsifying_forward_row_count"] > 0
        ),
        "falsifying_forward_row_count": len(falsification_rows),
    }
    return pair_width_rows, falsification_rows, bucket_rows, aggregate


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Check forward-stable PEDK exclusions across public gap-width buckets."
    )
    parser.add_argument("--min-factor", type=int, default=DEFAULT_MIN_FACTOR)
    parser.add_argument("--max-factor", type=int, default=DEFAULT_MAX_FACTOR)
    parser.add_argument("--max-ratio-numerator", type=int, default=DEFAULT_MAX_RATIO_NUMERATOR)
    parser.add_argument("--max-ratio-denominator", type=int, default=DEFAULT_MAX_RATIO_DENOMINATOR)
    parser.add_argument("--forward-pairs", type=Path, default=INPUT_PATH)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    """Run the public gap-width stability check."""
    args = parse_args(argv)
    if args.min_factor < 2:
        raise ValueError("min-factor must be at least 2")
    if args.max_factor < args.min_factor:
        raise ValueError("max-factor must be at least min-factor")
    if args.max_ratio_numerator < 1 or args.max_ratio_denominator < 1:
        raise ValueError("ratio terms must be positive")
    if not args.forward_pairs.exists():
        raise FileNotFoundError(f"missing forward survivor rows: {args.forward_pairs}")

    pairs = survivor_pairs(read_jsonl(args.forward_pairs))
    triples = semiprime_triples(
        args.min_factor,
        args.max_factor,
        args.max_ratio_numerator,
        args.max_ratio_denominator,
    )
    forward_rows = [corpus_row(triple) for triple in triples]
    pair_width_rows, falsification_rows, bucket_rows, aggregate = stability_rows(
        pairs,
        forward_rows,
    )

    args.output_dir.mkdir(parents=True, exist_ok=True)
    write_jsonl(args.output_dir / "pair_width_stability_rows.jsonl", pair_width_rows)
    write_jsonl(args.output_dir / "falsification_rows.jsonl", falsification_rows)
    write_jsonl(args.output_dir / "public_width_bucket_rows.jsonl", bucket_rows)
    summary = {
        "rule_id": RULE_ID,
        "source_rule_id": FORWARD_RULE_ID,
        "status": "measured_public_axis_sidecar_check",
        "theorem_status": "hypothesis_not_proved",
        "inference_status": "not_live_pedk_inference",
        "public_axis": "n_containing_gap_width",
        "public_width_buckets": [
            "width_006_016",
            "width_018_032",
            "width_034_048",
            "width_050_plus",
        ],
        "fresh_band": {
            "min_factor": args.min_factor,
            "max_factor": args.max_factor,
            "max_factor_ratio": f"{args.max_ratio_numerator}/{args.max_ratio_denominator}",
            "semiprime_triple_count": len(triples),
        },
        **aggregate,
    }
    write_json(args.output_dir / "summary.json", summary)
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
