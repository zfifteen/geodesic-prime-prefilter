#!/usr/bin/env python3
"""Forward-test stable PEDK phase-exclusion survivors on a fresh factor band."""

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


THIS_DIR = Path(__file__).resolve().parent
INPUT_PATH = THIS_DIR / "output" / "heldout_phase_exclusion_check" / "stable_survivor_rows.jsonl"
DEFAULT_OUTPUT_DIR = THIS_DIR / "output" / "forward_stable_survivor_prediction"
RULE_ID = "pedk_forward_stable_survivor_prediction_v1"
SOURCE_RULE_ID = "pedk_phase_exclusion_heldout_check_v1"
DEFAULT_MIN_FACTOR = 601
DEFAULT_MAX_FACTOR = 1000


def read_jsonl(path: Path) -> list[dict[str, object]]:
    """Read LF-delimited JSON rows."""
    rows: list[dict[str, object]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def stable_pairs(rows: list[dict[str, object]]) -> set[tuple[str, str]]:
    """Return stable survivor pairs as (public phase state, excluded signature)."""
    return {
        (
            str(row["n_containing_gap_phased_state"]),
            str(row["excluded_factor_neighborhood_signature"]),
        )
        for row in rows
    }


def phase_state(row: dict[str, object]) -> str:
    """Return the public phase state used by the candidate rule."""
    return str(row["n_containing_gap_phased_state"])


def factor_signature(row: dict[str, object]) -> str:
    """Return the downstream factor-neighborhood label."""
    return str(row["factor_neighborhood_signature"])


def prediction_rows(
    pairs: set[tuple[str, str]],
    forward_rows: list[dict[str, object]],
) -> tuple[list[dict[str, object]], list[dict[str, object]], dict[str, object]]:
    """Return per-pair prediction rows, falsification rows, and aggregate counts."""
    state_support = Counter(phase_state(row) for row in forward_rows)
    pair_falsifications = Counter(
        (phase_state(row), factor_signature(row))
        for row in forward_rows
        if (phase_state(row), factor_signature(row)) in pairs
    )
    falsification_rows = [
        {
            "rule_id": RULE_ID,
            "candidate_status": "stable_survivor_falsified_in_fresh_band",
            "case_id": row["case_id"],
            "N": row["N"],
            "p": row["p"],
            "q": row["q"],
            "n_containing_gap_phased_state": phase_state(row),
            "excluded_factor_neighborhood_signature": factor_signature(row),
        }
        for row in forward_rows
        if (phase_state(row), factor_signature(row)) in pairs
    ]

    output_rows: list[dict[str, object]] = []
    for state, signature in sorted(pairs):
        support = state_support[state]
        falsifying_count = pair_falsifications[(state, signature)]
        if support == 0:
            status = "untested_no_forward_rows_for_public_phase_state"
            absence_mpermille = None
        elif falsifying_count == 0:
            status = "survived_fresh_band"
            absence_mpermille = 1000
        else:
            status = "falsified_in_fresh_band"
            absence_mpermille = (support - falsifying_count) * 1000 // support
        output_rows.append(
            {
                "rule_id": RULE_ID,
                "source_rule_id": SOURCE_RULE_ID,
                "candidate_status": status,
                "n_containing_gap_phased_state": state,
                "excluded_factor_neighborhood_signature": signature,
                "forward_state_support": support,
                "falsifying_forward_row_count": falsifying_count,
                "absence_rate_mpermille": absence_mpermille,
            }
        )

    aggregate = {
        "tested_pair_count": sum(
            1 for state, _signature in pairs if state_support[state] > 0
        ),
        "untested_pair_count": sum(
            1 for state, _signature in pairs if state_support[state] == 0
        ),
        "survived_pair_count": sum(
            1
            for state, signature in pairs
            if state_support[state] > 0 and pair_falsifications[(state, signature)] == 0
        ),
        "falsified_pair_count": sum(
            1 for pair in pairs if pair_falsifications[pair] > 0
        ),
        "falsifying_forward_row_count": len(falsification_rows),
    }
    return output_rows, falsification_rows, aggregate


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Forward-test stable PEDK phase-exclusion survivors."
    )
    parser.add_argument("--min-factor", type=int, default=DEFAULT_MIN_FACTOR)
    parser.add_argument("--max-factor", type=int, default=DEFAULT_MAX_FACTOR)
    parser.add_argument("--max-ratio-numerator", type=int, default=DEFAULT_MAX_RATIO_NUMERATOR)
    parser.add_argument("--max-ratio-denominator", type=int, default=DEFAULT_MAX_RATIO_DENOMINATOR)
    parser.add_argument("--stable-survivors", type=Path, default=INPUT_PATH)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    """Run the fresh-band forward stable-survivor prediction check."""
    args = parse_args(argv)
    if args.min_factor < 2:
        raise ValueError("min-factor must be at least 2")
    if args.max_factor < args.min_factor:
        raise ValueError("max-factor must be at least min-factor")
    if args.max_ratio_numerator < 1 or args.max_ratio_denominator < 1:
        raise ValueError("ratio terms must be positive")
    if not args.stable_survivors.exists():
        raise FileNotFoundError(f"missing stable survivor rows: {args.stable_survivors}")

    survivor_rows = read_jsonl(args.stable_survivors)
    pairs = stable_pairs(survivor_rows)
    triples = semiprime_triples(
        args.min_factor,
        args.max_factor,
        args.max_ratio_numerator,
        args.max_ratio_denominator,
    )
    forward_rows = [corpus_row(triple) for triple in triples]
    per_pair_rows, falsification_rows, aggregate = prediction_rows(pairs, forward_rows)
    phase_counts = Counter(phase_state(row) for row in forward_rows)

    args.output_dir.mkdir(parents=True, exist_ok=True)
    write_jsonl(args.output_dir / "stable_pair_forward_rows.jsonl", per_pair_rows)
    write_jsonl(args.output_dir / "falsification_rows.jsonl", falsification_rows)
    write_jsonl(
        args.output_dir / "forward_phase_state_rows.jsonl",
        [
            {
                "rule_id": RULE_ID,
                "n_containing_gap_phased_state": state,
                "forward_row_count": count,
            }
            for state, count in sorted(phase_counts.items())
        ],
    )
    summary = {
        "rule_id": RULE_ID,
        "source_rule_id": SOURCE_RULE_ID,
        "status": "measured_forward_sidecar_check",
        "theorem_status": "hypothesis_not_proved",
        "inference_status": "not_live_pedk_inference",
        "fresh_band": {
            "min_factor": args.min_factor,
            "max_factor": args.max_factor,
            "max_factor_ratio": f"{args.max_ratio_numerator}/{args.max_ratio_denominator}",
            "semiprime_triple_count": len(triples),
        },
        "stable_survivor_count": len(pairs),
        "forward_phase_state_count": len(phase_counts),
        "top_forward_phase_states": [
            {"state": state, "count": count}
            for state, count in phase_counts.most_common(12)
        ],
        **aggregate,
    }
    write_json(args.output_dir / "summary.json", summary)
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
