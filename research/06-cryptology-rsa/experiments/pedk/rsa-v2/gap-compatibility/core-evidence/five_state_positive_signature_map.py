#!/usr/bin/env python3
"""Extract positive factor-neighborhood signatures for the five all-o6 states."""

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


THIS_DIR = Path(__file__).resolve().parent
REFINEMENT_PATH = (
    THIS_DIR
    / "output"
    / "five_state_all_o6_refinement_check"
    / "summary.json"
)
ALL_O6_CANDIDATE_PATH = (
    THIS_DIR
    / "output"
    / "five_state_all_o6_refinement_check"
    / "candidate_rule_rows.jsonl"
)
DEFAULT_OUTPUT_DIR = THIS_DIR / "output" / "five_state_positive_signature_map"
RULE_ID = "pedk_five_state_positive_signature_map_v1"
SOURCE_RULE_ID = "pedk_five_state_all_o6_refinement_check_v1"
DEFAULT_BANDS = (
    (601, 1000),
    (1001, 1400),
    (1401, 1800),
    (1801, 2200),
    (2201, 2600),
)


def read_json(path: Path) -> dict[str, object]:
    """Read one JSON object."""
    return json.loads(path.read_text(encoding="utf-8"))


def read_jsonl(path: Path) -> list[dict[str, object]]:
    """Read LF-delimited JSON rows."""
    rows: list[dict[str, object]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def phase_state(row: dict[str, object]) -> str:
    """Return public phase state."""
    return str(row["n_containing_gap_phased_state"])


def factor_signature(row: dict[str, object]) -> str:
    """Return downstream factor-neighborhood label."""
    return str(row["factor_neighborhood_signature"])


def band_key(min_factor: int, max_factor: int) -> str:
    """Return a compact band key."""
    return f"{min_factor}_{max_factor}"


def refinement_states(summary: dict[str, object]) -> set[str]:
    """Return the five public phase states from the refinement result."""
    states = {str(state) for state in summary["survived_public_phase_states"]}
    if len(states) != 5:
        raise ValueError("expected exactly five public phase states")
    return states


def excluded_all_o6_signature(candidate_rows: list[dict[str, object]]) -> str:
    """Return the all-o6 signature excluded by the refined rule."""
    signatures = {
        str(row["excluded_factor_neighborhood_signature"])
        for row in candidate_rows
        if row["candidate_rule"] == "five_state_all_o6_refinement"
    }
    if len(signatures) != 1:
        raise ValueError("expected exactly one refined all-o6 signature")
    return next(iter(signatures))


def parse_bands(raw_bands: list[str] | None) -> list[tuple[int, int]]:
    """Parse deterministic factor bands."""
    if not raw_bands:
        return list(DEFAULT_BANDS)
    bands: list[tuple[int, int]] = []
    for raw in raw_bands:
        left, separator, right = raw.partition(":")
        if separator != ":":
            raise ValueError(f"invalid band: {raw}")
        min_factor = int(left)
        max_factor = int(right)
        if min_factor < 2 or max_factor < min_factor:
            raise ValueError(f"invalid band bounds: {raw}")
        bands.append((min_factor, max_factor))
    return bands


def positive_map_rows(
    states: set[str],
    all_o6_signature: str,
    bands: list[tuple[int, int]],
    max_ratio_numerator: int,
    max_ratio_denominator: int,
) -> tuple[list[dict[str, object]], list[dict[str, object]], list[dict[str, object]], dict[str, object]]:
    """Return positive signature rows across factor bands."""
    state_band_support = Counter()
    signature_counts = Counter()
    signatures_by_state_band: dict[tuple[str, str], set[str]] = defaultdict(set)
    semiprime_counts: dict[str, int] = {}

    for min_factor, max_factor in bands:
        key = band_key(min_factor, max_factor)
        triples = semiprime_triples(
            min_factor,
            max_factor,
            max_ratio_numerator,
            max_ratio_denominator,
        )
        semiprime_counts[key] = len(triples)
        for triple in triples:
            row = corpus_row(triple)
            state = phase_state(row)
            if state not in states:
                continue
            signature = factor_signature(row)
            state_band_support[(state, key)] += 1
            signature_counts[(state, signature, key)] += 1
            signatures_by_state_band[(state, key)].add(signature)

    support_rows = [
        {
            "rule_id": RULE_ID,
            "n_containing_gap_phased_state": state,
            "band": key,
            "forward_row_count": state_band_support[(state, key)],
        }
        for state in sorted(states)
        for key in [band_key(min_factor, max_factor) for min_factor, max_factor in bands]
    ]
    count_rows = [
        {
            "rule_id": RULE_ID,
            "n_containing_gap_phased_state": state,
            "factor_neighborhood_signature": signature,
            "band": key,
            "observed_count": count,
        }
        for (state, signature, key), count in sorted(
            signature_counts.items(),
            key=lambda item: (item[0][0], item[0][1], item[0][2]),
        )
    ]
    positive_rows: list[dict[str, object]] = []
    band_keys = [band_key(min_factor, max_factor) for min_factor, max_factor in bands]
    for state in sorted(states):
        state_signatures = [
            signatures_by_state_band[(state, key)]
            for key in band_keys
            if state_band_support[(state, key)] > 0
        ]
        stable_signatures = set.intersection(*state_signatures) if state_signatures else set()
        for signature in sorted(stable_signatures):
            positive_rows.append(
                {
                    "rule_id": RULE_ID,
                    "source_rule_id": SOURCE_RULE_ID,
                    "candidate_status": "positive_signature_seen_in_every_supported_band",
                    "n_containing_gap_phased_state": state,
                    "factor_neighborhood_signature": signature,
                    "band_count": len(state_signatures),
                    "total_observed_count": sum(
                        signature_counts[(state, signature, key)]
                        for key in band_keys
                    ),
                    "is_excluded_all_o6_signature": signature == all_o6_signature,
                }
            )
    all_o6_observed_count = sum(
        count for (state, signature, _key), count in signature_counts.items()
        if state in states and signature == all_o6_signature
    )
    summary = {
        "rule_id": RULE_ID,
        "source_rule_id": SOURCE_RULE_ID,
        "status": "measured_positive_signature_map",
        "theorem_status": "hypothesis_not_proved",
        "inference_status": "not_live_pedk_inference",
        "public_phase_state_count": len(states),
        "band_count": len(bands),
        "stable_positive_signature_count": len(positive_rows),
        "all_o6_observed_count": all_o6_observed_count,
        "semiprime_counts_by_band": semiprime_counts,
    }
    return support_rows, count_rows, positive_rows, summary


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Extract positive signatures for the five all-o6 public states."
    )
    parser.add_argument("--band", action="append")
    parser.add_argument("--max-ratio-numerator", type=int, default=DEFAULT_MAX_RATIO_NUMERATOR)
    parser.add_argument("--max-ratio-denominator", type=int, default=DEFAULT_MAX_RATIO_DENOMINATOR)
    parser.add_argument("--refinement-summary", type=Path, default=REFINEMENT_PATH)
    parser.add_argument("--candidate-rows", type=Path, default=ALL_O6_CANDIDATE_PATH)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    """Run positive signature extraction."""
    args = parse_args(argv)
    if args.max_ratio_numerator < 1 or args.max_ratio_denominator < 1:
        raise ValueError("ratio terms must be positive")
    if not args.refinement_summary.exists():
        raise FileNotFoundError(f"missing refinement summary: {args.refinement_summary}")
    if not args.candidate_rows.exists():
        raise FileNotFoundError(f"missing candidate rows: {args.candidate_rows}")

    states = refinement_states(read_json(args.refinement_summary))
    all_o6_signature = excluded_all_o6_signature(read_jsonl(args.candidate_rows))
    bands = parse_bands(args.band)
    support_rows, count_rows, positive_rows, summary = positive_map_rows(
        states,
        all_o6_signature,
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
    summary["public_phase_states"] = sorted(states)

    args.output_dir.mkdir(parents=True, exist_ok=True)
    write_jsonl(args.output_dir / "state_band_support_rows.jsonl", support_rows)
    write_jsonl(args.output_dir / "signature_count_rows.jsonl", count_rows)
    write_jsonl(args.output_dir / "stable_positive_signature_rows.jsonl", positive_rows)
    write_json(args.output_dir / "summary.json", summary)
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
