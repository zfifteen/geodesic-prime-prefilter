#!/usr/bin/env python3
"""Test fully uniform factor-neighborhood corners for PEDK gap states."""

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
EXCEPTION_SUMMARY_PATH = (
    THIS_DIR
    / "output"
    / "all_o6_candidate_rule_check"
    / "summary.json"
)
DEFAULT_OUTPUT_DIR = THIS_DIR / "output" / "uniform_corner_test"
RULE_ID = "pedk_uniform_corner_test_v1"
SOURCE_RULE_ID = "pedk_five_state_all_o6_refinement_check_v1"
DEFAULT_BANDS = (
    (3001, 3500),
    (3501, 4000),
)


def read_json(path: Path) -> dict[str, object]:
    """Read one JSON object."""
    return json.loads(path.read_text(encoding="utf-8"))


def factor_residues(signature: str) -> tuple[str, ...]:
    """Return the four factor-side residue labels."""
    residues = tuple(re.findall(r"[LR]=(o[246])_", signature))
    if len(residues) != 4:
        raise ValueError(f"expected four residues in signature: {signature}")
    return residues


def uniform_residue(signature: str) -> str | None:
    """Return the residue when all four factor-side residues match."""
    residues = factor_residues(signature)
    if len(set(residues)) == 1:
        return residues[0]
    return None


def phase_state(row: dict[str, object]) -> str:
    """Return public phase state."""
    return str(row["n_containing_gap_phased_state"])


def factor_signature(row: dict[str, object]) -> str:
    """Return downstream factor-neighborhood label."""
    return str(row["factor_neighborhood_signature"])


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


def five_state_family(summary: dict[str, object]) -> set[str]:
    """Return the five public states from the refined all-o6 rule."""
    states = {str(state) for state in summary["survived_public_phase_states"]}
    if len(states) != 5:
        raise ValueError("expected exactly five public phase states")
    return states


def exception_states(summary: dict[str, object]) -> set[str]:
    """Return the public states that falsified the six-state all-o6 rule."""
    states = {str(state) for state in summary["falsified_public_phase_states"]}
    if not states:
        raise ValueError("expected at least one exception state")
    return states


def group_name(state: str, five_states: set[str], exceptions: set[str]) -> str | None:
    """Return the analysis group for a public phase state."""
    if state in five_states:
        return "five_state_survivor_family"
    if state in exceptions:
        return "even_mid_exception_family"
    return None


def uniform_corner_rows(
    five_states: set[str],
    exceptions: set[str],
    bands: list[tuple[int, int]],
    max_ratio_numerator: int,
    max_ratio_denominator: int,
) -> tuple[list[dict[str, object]], list[dict[str, object]], dict[str, object]]:
    """Return uniform-corner observations and group summaries."""
    support = Counter()
    uniform_counts = Counter()
    semiprime_counts: dict[str, int] = {}
    observation_rows: list[dict[str, object]] = []

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
            group = group_name(state, five_states, exceptions)
            if group is None:
                continue
            support[(group, state, key)] += 1
            residue = uniform_residue(factor_signature(row))
            if residue is None:
                continue
            uniform_counts[(group, state, key, residue)] += 1
            observation_rows.append(
                {
                    "rule_id": RULE_ID,
                    "analysis_group": group,
                    "band": key,
                    "uniform_residue": residue,
                    "case_id": row["case_id"],
                    "N": row["N"],
                    "p": row["p"],
                    "q": row["q"],
                    "n_containing_gap_phased_state": state,
                    "factor_neighborhood_signature": factor_signature(row),
                }
            )

    states_by_group = {
        "five_state_survivor_family": sorted(five_states),
        "even_mid_exception_family": sorted(exceptions),
    }
    band_keys = [band_key(min_factor, max_factor) for min_factor, max_factor in bands]
    summary_rows: list[dict[str, object]] = []
    for group, states in states_by_group.items():
        for state in states:
            for key in band_keys:
                total_uniform = sum(
                    uniform_counts[(group, state, key, residue)]
                    for residue in ("o2", "o4", "o6")
                )
                summary_rows.append(
                    {
                        "rule_id": RULE_ID,
                        "analysis_group": group,
                        "band": key,
                        "n_containing_gap_phased_state": state,
                        "forward_row_count": support[(group, state, key)],
                        "uniform_factor_neighborhood_count": total_uniform,
                        "all_o2_count": uniform_counts[(group, state, key, "o2")],
                        "all_o4_count": uniform_counts[(group, state, key, "o4")],
                        "all_o6_count": uniform_counts[(group, state, key, "o6")],
                    }
                )

    five_uniform_count = sum(
        row["uniform_factor_neighborhood_count"]
        for row in summary_rows
        if row["analysis_group"] == "five_state_survivor_family"
    )
    exception_uniform_count = sum(
        row["uniform_factor_neighborhood_count"]
        for row in summary_rows
        if row["analysis_group"] == "even_mid_exception_family"
    )
    summary = {
        "rule_id": RULE_ID,
        "source_rule_id": SOURCE_RULE_ID,
        "status": "measured_uniform_corner_test",
        "theorem_status": "hypothesis_not_proved",
        "inference_status": "not_live_pedk_inference",
        "band_count": len(bands),
        "five_state_public_phase_states": sorted(five_states),
        "exception_public_phase_states": sorted(exceptions),
        "five_state_forward_row_count": sum(
            row["forward_row_count"]
            for row in summary_rows
            if row["analysis_group"] == "five_state_survivor_family"
        ),
        "exception_forward_row_count": sum(
            row["forward_row_count"]
            for row in summary_rows
            if row["analysis_group"] == "even_mid_exception_family"
        ),
        "five_state_uniform_observation_count": five_uniform_count,
        "exception_uniform_observation_count": exception_uniform_count,
        "five_state_uniform_corner_status": (
            "survived_no_uniform_observations"
            if five_uniform_count == 0
            else "falsified_uniform_observation_present"
        ),
        "exception_uniform_corner_status": (
            "exception_supported_uniform_observation_present"
            if exception_uniform_count > 0
            else "exception_not_observed_in_test_bands"
        ),
        "semiprime_counts_by_band": semiprime_counts,
    }
    return observation_rows, summary_rows, summary


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Test fully uniform factor-neighborhood corners for PEDK gap states."
    )
    parser.add_argument("--band", action="append")
    parser.add_argument("--max-ratio-numerator", type=int, default=DEFAULT_MAX_RATIO_NUMERATOR)
    parser.add_argument("--max-ratio-denominator", type=int, default=DEFAULT_MAX_RATIO_DENOMINATOR)
    parser.add_argument("--five-state-summary", type=Path, default=FIVE_STATE_SUMMARY_PATH)
    parser.add_argument("--exception-summary", type=Path, default=EXCEPTION_SUMMARY_PATH)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    """Run the uniform corner test."""
    args = parse_args(argv)
    if args.max_ratio_numerator < 1 or args.max_ratio_denominator < 1:
        raise ValueError("ratio terms must be positive")
    if not args.five_state_summary.exists():
        raise FileNotFoundError(f"missing five-state summary: {args.five_state_summary}")
    if not args.exception_summary.exists():
        raise FileNotFoundError(f"missing exception summary: {args.exception_summary}")

    bands = parse_bands(args.band)
    observation_rows, summary_rows, summary = uniform_corner_rows(
        five_state_family(read_json(args.five_state_summary)),
        exception_states(read_json(args.exception_summary)),
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
    write_jsonl(args.output_dir / "uniform_observation_rows.jsonl", observation_rows)
    write_jsonl(args.output_dir / "group_band_summary_rows.jsonl", summary_rows)
    write_json(args.output_dir / "summary.json", summary)
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
