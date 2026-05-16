#!/usr/bin/env python3
"""Characterize public gap features around all-o6 compatibility boundaries."""

from __future__ import annotations

import argparse
import json
import re
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
DEFAULT_OUTPUT_DIR = THIS_DIR / "output" / "public_feature_all_o6_boundary"
RULE_ID = "pedk_public_feature_all_o6_boundary_v1"
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
)
TARGET_STATES = (
    "o2_d4_odd|d<=4@late",
    "o4_d4_even|d<=4@mid",
    "o4_d4_odd|d<=4@early",
    "o4_d4_odd|d<=4@late",
    "o4_d4_odd|d<=4@mid",
    "o6_d4_odd|d<=4@late",
)


def factor_residues(signature: str) -> tuple[str, ...]:
    """Return the four factor-side residue labels."""
    residues = tuple(re.findall(r"[LR]=(o[246])_", signature))
    if len(residues) != 4:
        raise ValueError(f"expected four residues in signature: {signature}")
    return residues


def is_all_o6(signature: str) -> bool:
    """Return true when all four factor-side residues are o6."""
    return all(residue == "o6" for residue in factor_residues(signature))


def phase_state(row: dict[str, object]) -> str:
    """Return public phase state."""
    return str(row["n_containing_gap_phased_state"])


def band_key(min_factor: int, max_factor: int) -> str:
    """Return a compact band key."""
    return f"{min_factor}_{max_factor}"


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


def median(values: list[int]) -> int | None:
    """Return deterministic median for integer values."""
    if not values:
        return None
    ordered = sorted(values)
    return ordered[len(ordered) // 2]


def top_counter_rows(counter: Counter[str], limit: int) -> list[dict[str, object]]:
    """Return top counter rows in deterministic order."""
    return [
        {"value": value, "count": count}
        for value, count in sorted(counter.items(), key=lambda item: (-item[1], item[0]))[:limit]
    ]


def state_features(
    bands: list[tuple[int, int]],
    target_states: set[str],
    max_ratio_numerator: int,
    max_ratio_denominator: int,
) -> tuple[list[dict[str, object]], list[dict[str, object]], list[dict[str, object]], dict[str, object]]:
    """Return public feature rows for target public phase states."""
    support = Counter()
    all_o6 = Counter()
    exact_types: dict[str, Counter[str]] = defaultdict(Counter)
    previous_states: dict[str, Counter[str]] = defaultdict(Counter)
    following_states: dict[str, Counter[str]] = defaultdict(Counter)
    widths: dict[str, list[int]] = defaultdict(list)
    offsets_left: dict[str, list[int]] = defaultdict(list)
    offsets_right: dict[str, list[int]] = defaultdict(list)
    position_mpermille: dict[str, list[int]] = defaultdict(list)
    winner_offsets: dict[str, list[int]] = defaultdict(list)
    band_support = Counter()
    all_o6_rows: list[dict[str, object]] = []
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
            if state not in target_states:
                continue
            containing = row["n_gaps"]["containing"]
            support[state] += 1
            band_support[(state, key)] += 1
            exact_types[state][str(containing["exact_type_key"])] += 1
            previous_states[state][str(row["n_previous_gap_reduced_state"])] += 1
            following_states[state][str(row["n_following_gap_reduced_state"])] += 1
            widths[state].append(int(str(row["n_containing_gap_width"])))
            offsets_left[state].append(int(str(row["n_offset_from_left"])))
            offsets_right[state].append(int(str(row["n_offset_from_right"])))
            position_mpermille[state].append(int(str(row["n_containing_gap_position_mpermille"])))
            winner_offsets[state].append(int(str(containing["winner_offset"])))
            if is_all_o6(str(row["factor_neighborhood_signature"])):
                all_o6[state] += 1
                all_o6_rows.append(
                    {
                        "rule_id": RULE_ID,
                        "case_id": row["case_id"],
                        "band": key,
                        "N": row["N"],
                        "p": row["p"],
                        "q": row["q"],
                        "n_containing_gap_phased_state": state,
                        "n_containing_gap_exact_type_key": containing["exact_type_key"],
                        "n_containing_gap_width": row["n_containing_gap_width"],
                        "n_offset_from_left": row["n_offset_from_left"],
                        "n_offset_from_right": row["n_offset_from_right"],
                        "n_position_mpermille": row["n_containing_gap_position_mpermille"],
                        "factor_neighborhood_signature": row["factor_neighborhood_signature"],
                    }
                )

    state_rows: list[dict[str, object]] = []
    for state in sorted(target_states):
        count = support[state]
        state_rows.append(
            {
                "rule_id": RULE_ID,
                "n_containing_gap_phased_state": state,
                "all_o6_status": (
                    "all_o6_compatible_observed"
                    if all_o6[state] > 0
                    else "all_o6_not_observed"
                ),
                "forward_row_count": count,
                "all_o6_observation_count": all_o6[state],
                "all_o6_rate_mpermille": None if count == 0 else all_o6[state] * 1000 // count,
                "width_min": min(widths[state]) if widths[state] else None,
                "width_median": median(widths[state]),
                "width_max": max(widths[state]) if widths[state] else None,
                "offset_left_median": median(offsets_left[state]),
                "offset_right_median": median(offsets_right[state]),
                "position_mpermille_median": median(position_mpermille[state]),
                "winner_offset_median": median(winner_offsets[state]),
                "top_exact_type_keys": top_counter_rows(exact_types[state], 5),
                "top_previous_gap_states": top_counter_rows(previous_states[state], 5),
                "top_following_gap_states": top_counter_rows(following_states[state], 5),
            }
        )

    band_rows = [
        {
            "rule_id": RULE_ID,
            "n_containing_gap_phased_state": state,
            "band": key,
            "forward_row_count": band_support[(state, key)],
        }
        for state in sorted(target_states)
        for key in [band_key(min_factor, max_factor) for min_factor, max_factor in bands]
    ]
    compatible_states = sorted(state for state in target_states if all_o6[state] > 0)
    not_observed_states = sorted(state for state in target_states if all_o6[state] == 0)
    summary = {
        "rule_id": RULE_ID,
        "status": "measured_public_feature_all_o6_boundary",
        "theorem_status": "hypothesis_not_proved",
        "inference_status": "not_live_pedk_inference",
        "target_state_count": len(target_states),
        "all_o6_compatible_state_count": len(compatible_states),
        "all_o6_not_observed_state_count": len(not_observed_states),
        "all_o6_compatible_states": compatible_states,
        "all_o6_not_observed_states": not_observed_states,
        "all_o6_observation_count": sum(all_o6.values()),
        "semiprime_counts_by_band": semiprime_counts,
    }
    return state_rows, band_rows, all_o6_rows, summary


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Characterize public gap features around all-o6 boundaries."
    )
    parser.add_argument("--band", action="append")
    parser.add_argument("--max-ratio-numerator", type=int, default=DEFAULT_MAX_RATIO_NUMERATOR)
    parser.add_argument("--max-ratio-denominator", type=int, default=DEFAULT_MAX_RATIO_DENOMINATOR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    """Run public feature characterization."""
    args = parse_args(argv)
    if args.max_ratio_numerator < 1 or args.max_ratio_denominator < 1:
        raise ValueError("ratio terms must be positive")

    bands = parse_bands(args.band)
    state_rows, band_rows, all_o6_rows, summary = state_features(
        bands,
        set(TARGET_STATES),
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
    write_jsonl(args.output_dir / "state_feature_rows.jsonl", state_rows)
    write_jsonl(args.output_dir / "state_band_support_rows.jsonl", band_rows)
    write_jsonl(args.output_dir / "all_o6_observation_rows.jsonl", all_o6_rows)
    write_json(args.output_dir / "summary.json", summary)
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
