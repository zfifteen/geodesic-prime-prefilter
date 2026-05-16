#!/usr/bin/env python3
"""Check the all-o6 PEDK candidate exclusion rule on a fresh band."""

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
INPUT_PATH = (
    THIS_DIR
    / "output"
    / "symbolic_rule_forward_check"
    / "candidate_rule_rows.jsonl"
)
DEFAULT_OUTPUT_DIR = THIS_DIR / "output" / "all_o6_candidate_rule_check"
RULE_ID = "pedk_all_o6_candidate_rule_check_v1"
SOURCE_RULE_ID = "pedk_symbolic_rule_forward_check_v1"
DEFAULT_MIN_FACTOR = 1801
DEFAULT_MAX_FACTOR = 2200
NARROW_RULE_NAME = "narrow_all_o6_signature_for_six_phase_states"


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


def survived_all_o6_candidate(rows: list[dict[str, object]]) -> dict[str, object]:
    """Return the survived all-o6 candidate row."""
    matches = [
        row for row in rows
        if row["candidate_rule"] == NARROW_RULE_NAME
        and row["candidate_status"] == "survived_fresh_band"
    ]
    if len(matches) != 1:
        raise ValueError("expected exactly one survived all-o6 candidate")
    return matches[0]


def check_candidate(
    candidate: dict[str, object],
    forward_rows: list[dict[str, object]],
) -> tuple[list[dict[str, object]], list[dict[str, object]], list[dict[str, object]], dict[str, object]]:
    """Return candidate check rows for one fresh band."""
    states = {str(state) for state in candidate["public_phase_states"]}
    excluded_signature = str(candidate["excluded_factor_neighborhood_signature"])
    support = Counter(
        phase_state(row) for row in forward_rows
        if phase_state(row) in states
    )
    falsifications = [
        row for row in forward_rows
        if phase_state(row) in states
        and factor_signature(row) == excluded_signature
    ]
    state_falsifications = Counter(phase_state(row) for row in falsifications)
    candidate_rows = [
        {
            "rule_id": RULE_ID,
            "source_rule_id": SOURCE_RULE_ID,
            "candidate_rule": NARROW_RULE_NAME,
            "candidate_status": (
                "survived_fresh_band"
                if not falsifications
                else "falsified_in_fresh_band"
            ),
            "public_phase_state_count": len(states),
            "tested_forward_row_count": sum(support.values()),
            "falsifying_forward_row_count": len(falsifications),
            "excluded_factor_neighborhood_signature": excluded_signature,
            "public_phase_states": sorted(states),
            "falsification_criterion": (
                "A row falsifies this candidate if S(N) is one of the six "
                "public phase states and F(p,q) is the all-o6 "
                "factor-neighborhood signature."
            ),
        }
    ]
    falsification_rows = [
        {
            "rule_id": RULE_ID,
            "candidate_rule": NARROW_RULE_NAME,
            "case_id": row["case_id"],
            "N": row["N"],
            "p": row["p"],
            "q": row["q"],
            "n_containing_gap_phased_state": phase_state(row),
            "factor_neighborhood_signature": factor_signature(row),
        }
        for row in falsifications
    ]
    state_support_rows = [
        {
            "rule_id": RULE_ID,
            "candidate_rule": NARROW_RULE_NAME,
            "candidate_status": (
                "survived_fresh_band"
                if state_falsifications[state] == 0
                else "falsified_in_fresh_band"
            ),
            "n_containing_gap_phased_state": state,
            "forward_row_count": support[state],
            "falsifying_forward_row_count": state_falsifications[state],
        }
        for state in sorted(states)
    ]
    falsified_states = sorted(state for state in states if state_falsifications[state] > 0)
    survived_states = sorted(states - set(falsified_states))
    summary = {
        "rule_id": RULE_ID,
        "source_rule_id": SOURCE_RULE_ID,
        "status": "measured_candidate_rule_check",
        "theorem_status": "hypothesis_not_proved",
        "inference_status": "not_live_pedk_inference",
        "candidate_rule": NARROW_RULE_NAME,
        "tested_forward_row_count": sum(support.values()),
        "falsifying_forward_row_count": len(falsifications),
        "candidate_status": candidate_rows[0]["candidate_status"],
        "survived_public_phase_state_count": len(survived_states),
        "falsified_public_phase_state_count": len(falsified_states),
        "survived_public_phase_states": survived_states,
        "falsified_public_phase_states": falsified_states,
    }
    return candidate_rows, falsification_rows, state_support_rows, summary


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Check the all-o6 PEDK candidate exclusion rule on a fresh band."
    )
    parser.add_argument("--min-factor", type=int, default=DEFAULT_MIN_FACTOR)
    parser.add_argument("--max-factor", type=int, default=DEFAULT_MAX_FACTOR)
    parser.add_argument("--max-ratio-numerator", type=int, default=DEFAULT_MAX_RATIO_NUMERATOR)
    parser.add_argument("--max-ratio-denominator", type=int, default=DEFAULT_MAX_RATIO_DENOMINATOR)
    parser.add_argument("--candidate-rows", type=Path, default=INPUT_PATH)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    """Run the all-o6 candidate rule check."""
    args = parse_args(argv)
    if args.min_factor < 2:
        raise ValueError("min-factor must be at least 2")
    if args.max_factor < args.min_factor:
        raise ValueError("max-factor must be at least min-factor")
    if args.max_ratio_numerator < 1 or args.max_ratio_denominator < 1:
        raise ValueError("ratio terms must be positive")
    if not args.candidate_rows.exists():
        raise FileNotFoundError(f"missing candidate rows: {args.candidate_rows}")

    candidate = survived_all_o6_candidate(read_jsonl(args.candidate_rows))
    triples = semiprime_triples(
        args.min_factor,
        args.max_factor,
        args.max_ratio_numerator,
        args.max_ratio_denominator,
    )
    forward_rows = [corpus_row(triple) for triple in triples]
    candidate_rows, falsification_rows, state_support_rows, summary = check_candidate(
        candidate,
        forward_rows,
    )
    summary["fresh_band"] = {
        "min_factor": args.min_factor,
        "max_factor": args.max_factor,
        "max_factor_ratio": f"{args.max_ratio_numerator}/{args.max_ratio_denominator}",
        "semiprime_triple_count": len(triples),
    }

    args.output_dir.mkdir(parents=True, exist_ok=True)
    write_jsonl(args.output_dir / "candidate_rule_rows.jsonl", candidate_rows)
    write_jsonl(args.output_dir / "falsification_rows.jsonl", falsification_rows)
    write_jsonl(args.output_dir / "state_support_rows.jsonl", state_support_rows)
    write_json(args.output_dir / "summary.json", summary)
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
