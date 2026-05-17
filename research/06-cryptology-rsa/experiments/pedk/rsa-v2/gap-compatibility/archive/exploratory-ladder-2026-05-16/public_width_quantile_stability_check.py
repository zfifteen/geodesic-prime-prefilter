#!/usr/bin/env python3
"""Check PEDK survivor stability across state-local public width quantiles."""

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
from forward_stable_survivor_prediction import RULE_ID as FORWARD_RULE_ID


THIS_DIR = Path(__file__).resolve().parent
INPUT_PATH = (
    THIS_DIR
    / "output"
    / "forward_stable_survivor_prediction"
    / "stable_pair_forward_rows.jsonl"
)
DEFAULT_OUTPUT_DIR = THIS_DIR / "output" / "public_width_quantile_stability_check"
RULE_ID = "pedk_public_width_quantile_stability_check_v1"
DEFAULT_MIN_FACTOR = 1001
DEFAULT_MAX_FACTOR = 1400
QUANTILE_LABELS = ("q1_low_width", "q2_midlow_width", "q3_midhigh_width", "q4_high_width")


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


def state_width_thresholds(rows: list[dict[str, object]]) -> dict[str, tuple[int, int, int]]:
    """Return deterministic state-local public width quartile thresholds."""
    widths_by_state: dict[str, list[int]] = defaultdict(list)
    for row in rows:
        widths_by_state[phase_state(row)].append(public_width(row))
    thresholds: dict[str, tuple[int, int, int]] = {}
    for state, widths in widths_by_state.items():
        ordered = sorted(widths)
        count = len(ordered)
        thresholds[state] = (
            ordered[count // 4],
            ordered[count // 2],
            ordered[(3 * count) // 4],
        )
    return thresholds


def quantile_bucket(width: int, thresholds: tuple[int, int, int]) -> str:
    """Return state-local width quantile bucket for one public width."""
    low, mid, high = thresholds
    if width <= low:
        return QUANTILE_LABELS[0]
    if width <= mid:
        return QUANTILE_LABELS[1]
    if width <= high:
        return QUANTILE_LABELS[2]
    return QUANTILE_LABELS[3]


def stability_rows(
    pairs: set[tuple[str, str]],
    forward_rows: list[dict[str, object]],
) -> tuple[
    list[dict[str, object]],
    list[dict[str, object]],
    list[dict[str, object]],
    list[dict[str, object]],
    list[dict[str, object]],
    dict[str, object],
]:
    """Return quantile stability rows and aggregate counts."""
    thresholds = state_width_thresholds(forward_rows)
    state_quantile_support = Counter(
        (
            phase_state(row),
            quantile_bucket(public_width(row), thresholds[phase_state(row)]),
        )
        for row in forward_rows
    )
    pair_quantile_falsifications = Counter(
        (
            phase_state(row),
            factor_signature(row),
            quantile_bucket(public_width(row), thresholds[phase_state(row)]),
        )
        for row in forward_rows
        if (phase_state(row), factor_signature(row)) in pairs
    )

    pair_quantile_rows: list[dict[str, object]] = []
    for state, signature in sorted(pairs):
        for quantile in QUANTILE_LABELS:
            support = state_quantile_support[(state, quantile)]
            falsifications = pair_quantile_falsifications[(state, signature, quantile)]
            if support == 0:
                status = "untested_no_forward_rows_for_state_width_quantile"
                absence_mpermille = None
            elif falsifications == 0:
                status = "survived_state_width_quantile"
                absence_mpermille = 1000
            else:
                status = "falsified_in_state_width_quantile"
                absence_mpermille = (support - falsifications) * 1000 // support
            pair_quantile_rows.append(
                {
                    "rule_id": RULE_ID,
                    "source_rule_id": FORWARD_RULE_ID,
                    "candidate_status": status,
                    "n_containing_gap_phased_state": state,
                    "excluded_factor_neighborhood_signature": signature,
                    "state_width_quantile": quantile,
                    "forward_state_quantile_support": support,
                    "falsifying_forward_row_count": falsifications,
                    "absence_rate_mpermille": absence_mpermille,
                }
            )

    falsification_rows = [
        {
            "rule_id": RULE_ID,
            "candidate_status": "forward_survivor_falsified_in_state_width_quantile",
            "case_id": row["case_id"],
            "N": row["N"],
            "p": row["p"],
            "q": row["q"],
            "n_containing_gap_phased_state": phase_state(row),
            "public_gap_width": public_width(row),
            "state_width_quantile": quantile_bucket(public_width(row), thresholds[phase_state(row)]),
            "excluded_factor_neighborhood_signature": factor_signature(row),
        }
        for row in forward_rows
        if (phase_state(row), factor_signature(row)) in pairs
    ]
    falsified_pairs = {
        (
            str(row["n_containing_gap_phased_state"]),
            str(row["excluded_factor_neighborhood_signature"]),
        )
        for row in pair_quantile_rows
        if row["falsifying_forward_row_count"] > 0
    }
    stable_survivor_rows = [
        {
            "rule_id": RULE_ID,
            "source_rule_id": FORWARD_RULE_ID,
            "candidate_status": "survived_fresh_band_and_state_width_quantiles",
            "n_containing_gap_phased_state": state,
            "excluded_factor_neighborhood_signature": signature,
        }
        for state, signature in sorted(pairs - falsified_pairs)
    ]

    threshold_rows = [
        {
            "rule_id": RULE_ID,
            "n_containing_gap_phased_state": state,
            "q1_max_width": q1,
            "q2_max_width": q2,
            "q3_max_width": q3,
        }
        for state, (q1, q2, q3) in sorted(thresholds.items())
    ]
    quantile_support_rows = [
        {
            "rule_id": RULE_ID,
            "n_containing_gap_phased_state": state,
            "state_width_quantile": quantile,
            "forward_row_count": state_quantile_support[(state, quantile)],
        }
        for state in sorted(thresholds)
        for quantile in QUANTILE_LABELS
    ]
    tested_rows = [
        row for row in pair_quantile_rows if row["forward_state_quantile_support"] > 0
    ]
    aggregate = {
        "forward_survivor_count": len(pairs),
        "state_width_quantile_count": len(QUANTILE_LABELS),
        "pair_quantile_cell_count": len(pair_quantile_rows),
        "tested_pair_quantile_cell_count": len(tested_rows),
        "untested_pair_quantile_cell_count": len(pair_quantile_rows) - len(tested_rows),
        "fully_quantile_covered_pair_count": sum(
            1
            for state, _signature in pairs
            if all(state_quantile_support[(state, quantile)] > 0 for quantile in QUANTILE_LABELS)
        ),
        "falsified_pair_quantile_cell_count": sum(
            1 for row in pair_quantile_rows if row["falsifying_forward_row_count"] > 0
        ),
        "falsified_pair_count": len(
            {
                (
                    row["n_containing_gap_phased_state"],
                    row["excluded_factor_neighborhood_signature"],
                )
                for row in pair_quantile_rows
                if row["falsifying_forward_row_count"] > 0
            }
        ),
        "falsifying_forward_row_count": len(falsification_rows),
    }
    return (
        pair_quantile_rows,
        falsification_rows,
        stable_survivor_rows,
        threshold_rows,
        quantile_support_rows,
        aggregate,
    )


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Check PEDK survivor stability across state-local public width quantiles."
    )
    parser.add_argument("--min-factor", type=int, default=DEFAULT_MIN_FACTOR)
    parser.add_argument("--max-factor", type=int, default=DEFAULT_MAX_FACTOR)
    parser.add_argument("--max-ratio-numerator", type=int, default=DEFAULT_MAX_RATIO_NUMERATOR)
    parser.add_argument("--max-ratio-denominator", type=int, default=DEFAULT_MAX_RATIO_DENOMINATOR)
    parser.add_argument("--forward-pairs", type=Path, default=INPUT_PATH)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    """Run the state-local public width quantile stability check."""
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
    (
        pair_quantile_rows,
        falsification_rows,
        stable_survivor_rows,
        threshold_rows,
        quantile_support_rows,
        aggregate,
    ) = stability_rows(pairs, forward_rows)

    args.output_dir.mkdir(parents=True, exist_ok=True)
    write_jsonl(args.output_dir / "pair_quantile_stability_rows.jsonl", pair_quantile_rows)
    write_jsonl(args.output_dir / "falsification_rows.jsonl", falsification_rows)
    write_jsonl(args.output_dir / "stable_quantile_survivor_rows.jsonl", stable_survivor_rows)
    write_jsonl(args.output_dir / "state_width_threshold_rows.jsonl", threshold_rows)
    write_jsonl(args.output_dir / "state_quantile_support_rows.jsonl", quantile_support_rows)
    summary = {
        "rule_id": RULE_ID,
        "source_rule_id": FORWARD_RULE_ID,
        "status": "measured_public_axis_sidecar_check",
        "theorem_status": "hypothesis_not_proved",
        "inference_status": "not_live_pedk_inference",
        "public_axis": "state_local_n_containing_gap_width_quantile",
        "state_width_quantiles": list(QUANTILE_LABELS),
        "fresh_band": {
            "min_factor": args.min_factor,
            "max_factor": args.max_factor,
            "max_factor_ratio": f"{args.max_ratio_numerator}/{args.max_ratio_denominator}",
            "semiprime_triple_count": len(triples),
        },
        "stable_quantile_survivor_count": len(stable_survivor_rows),
        **aggregate,
    }
    write_json(args.output_dir / "summary.json", summary)
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
