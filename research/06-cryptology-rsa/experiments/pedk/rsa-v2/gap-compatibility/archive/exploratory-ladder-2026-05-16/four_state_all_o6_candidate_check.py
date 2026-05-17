#!/usr/bin/env python3
"""Check the four-state all-o6 PEDK candidate after uniform-corner falsification."""

from __future__ import annotations

import argparse
import json
import re
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
FIVE_STATE_SUMMARY_PATH = (
    THIS_DIR
    / "output"
    / "five_state_all_o6_refinement_check"
    / "summary.json"
)
DEFAULT_OUTPUT_DIR = THIS_DIR / "output" / "four_state_all_o6_candidate_check"
RULE_ID = "pedk_four_state_all_o6_candidate_check_v1"
SOURCE_RULE_ID = "pedk_uniform_corner_test_v1"
DEFAULT_MIN_FACTOR = 4001
DEFAULT_MAX_FACTOR = 4500
REMOVED_MID_STATE = "o4_d4_odd|d<=4@mid"


def read_json(path: Path) -> dict[str, object]:
    """Read one JSON object."""
    return json.loads(path.read_text(encoding="utf-8"))


def phase_state(row: dict[str, object]) -> str:
    """Return public phase state."""
    return str(row["n_containing_gap_phased_state"])


def factor_signature(row: dict[str, object]) -> str:
    """Return downstream factor-neighborhood label."""
    return str(row["factor_neighborhood_signature"])


def is_all_o6(signature: str) -> bool:
    """Return true when all four factor-side residues are o6."""
    residues = tuple(re.findall(r"[LR]=(o[246])_", signature))
    if len(residues) != 4:
        raise ValueError(f"expected four residues in signature: {signature}")
    return all(residue == "o6" for residue in residues)


def four_state_family(summary: dict[str, object]) -> set[str]:
    """Return the four-state family after removing the mid-state exception."""
    states = {str(state) for state in summary["survived_public_phase_states"]}
    states.discard(REMOVED_MID_STATE)
    if len(states) != 4:
        raise ValueError("expected exactly four public phase states")
    return states


def check_candidate(
    states: set[str],
    forward_rows: list[dict[str, object]],
) -> tuple[list[dict[str, object]], list[dict[str, object]], list[dict[str, object]], dict[str, object]]:
    """Return four-state candidate rows for one fresh band."""
    support = Counter(
        phase_state(row) for row in forward_rows
        if phase_state(row) in states
    )
    falsifications = [
        row for row in forward_rows
        if phase_state(row) in states
        and is_all_o6(factor_signature(row))
    ]
    state_falsifications = Counter(phase_state(row) for row in falsifications)
    falsified_states = sorted(state for state in states if state_falsifications[state] > 0)
    survived_states = sorted(states - set(falsified_states))
    candidate_rows = [
        {
            "rule_id": RULE_ID,
            "source_rule_id": SOURCE_RULE_ID,
            "candidate_rule": "four_state_all_o6_exclusion",
            "candidate_status": (
                "survived_fresh_band"
                if not falsifications
                else "falsified_in_fresh_band"
            ),
            "public_phase_state_count": len(states),
            "tested_forward_row_count": sum(support.values()),
            "falsifying_forward_row_count": len(falsifications),
            "public_phase_states": sorted(states),
            "removed_public_phase_state": REMOVED_MID_STATE,
            "falsification_criterion": (
                "A row falsifies this candidate if S(N) is one of the four "
                "public phase states and F(p,q) is the all-o6 "
                "factor-neighborhood signature."
            ),
        }
    ]
    falsification_rows = [
        {
            "rule_id": RULE_ID,
            "candidate_rule": "four_state_all_o6_exclusion",
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
            "candidate_rule": "four_state_all_o6_exclusion",
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
    summary = {
        "rule_id": RULE_ID,
        "source_rule_id": SOURCE_RULE_ID,
        "status": "measured_four_state_candidate_check",
        "theorem_status": "hypothesis_not_proved",
        "inference_status": "not_live_pedk_inference",
        "candidate_rule": "four_state_all_o6_exclusion",
        "candidate_status": candidate_rows[0]["candidate_status"],
        "removed_public_phase_state": REMOVED_MID_STATE,
        "tested_forward_row_count": sum(support.values()),
        "falsifying_forward_row_count": len(falsifications),
        "survived_public_phase_state_count": len(survived_states),
        "falsified_public_phase_state_count": len(falsified_states),
        "survived_public_phase_states": survived_states,
        "falsified_public_phase_states": falsified_states,
    }
    return candidate_rows, falsification_rows, state_support_rows, summary


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Check the four-state all-o6 candidate on a fresh band."
    )
    parser.add_argument("--min-factor", type=int, default=DEFAULT_MIN_FACTOR)
    parser.add_argument("--max-factor", type=int, default=DEFAULT_MAX_FACTOR)
    parser.add_argument("--max-ratio-numerator", type=int, default=DEFAULT_MAX_RATIO_NUMERATOR)
    parser.add_argument("--max-ratio-denominator", type=int, default=DEFAULT_MAX_RATIO_DENOMINATOR)
    parser.add_argument("--five-state-summary", type=Path, default=FIVE_STATE_SUMMARY_PATH)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    """Run the four-state all-o6 candidate check."""
    args = parse_args(argv)
    if args.min_factor < 2:
        raise ValueError("min-factor must be at least 2")
    if args.max_factor < args.min_factor:
        raise ValueError("max-factor must be at least min-factor")
    if args.max_ratio_numerator < 1 or args.max_ratio_denominator < 1:
        raise ValueError("ratio terms must be positive")
    if not args.five_state_summary.exists():
        raise FileNotFoundError(f"missing five-state summary: {args.five_state_summary}")

    states = four_state_family(read_json(args.five_state_summary))
    triples = semiprime_triples(
        args.min_factor,
        args.max_factor,
        args.max_ratio_numerator,
        args.max_ratio_denominator,
    )
    forward_rows = [corpus_row(triple) for triple in triples]
    candidate_rows, falsification_rows, state_support_rows, summary = check_candidate(
        states,
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
