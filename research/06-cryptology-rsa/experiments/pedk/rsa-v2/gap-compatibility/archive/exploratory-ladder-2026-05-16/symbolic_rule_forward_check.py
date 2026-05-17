#!/usr/bin/env python3
"""Forward-test symbolic PEDK incompatibility rule candidates."""

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
SYMBOLIC_ROWS_PATH = (
    THIS_DIR
    / "output"
    / "symbolic_survivor_compression"
    / "symbolic_survivor_rows.jsonl"
)
DEFAULT_OUTPUT_DIR = THIS_DIR / "output" / "symbolic_rule_forward_check"
RULE_ID = "pedk_symbolic_rule_forward_check_v1"
SOURCE_RULE_ID = "pedk_symbolic_survivor_compression_v1"
DEFAULT_MIN_FACTOR = 1401
DEFAULT_MAX_FACTOR = 1800


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


def residue_count(signature: str, residue: str) -> int:
    """Count factor-side residue labels in a factor-neighborhood signature."""
    return re.findall(r"[LR]=(o[246])_", signature).count(residue)


def narrow_all_o6_rule(rows: list[dict[str, object]]) -> tuple[str, set[str]]:
    """Return all-o6 signature and public phase states from symbolic survivors."""
    all_o6_rows = [
        row for row in rows
        if row["is_all_o6_signature"] is True
    ]
    signatures = {
        str(row["excluded_factor_neighborhood_signature"])
        for row in all_o6_rows
    }
    if len(signatures) != 1:
        raise ValueError("expected exactly one all-o6 factor-neighborhood signature")
    states = {
        str(row["n_containing_gap_phased_state"])
        for row in all_o6_rows
    }
    return next(iter(signatures)), states


def broad_o6_envelope_states(rows: list[dict[str, object]]) -> set[str]:
    """Return phase states covered by the symbolic survivor surface."""
    return {
        str(row["n_containing_gap_phased_state"])
        for row in rows
    }


def evaluate_rules(
    symbolic_rows: list[dict[str, object]],
    forward_rows: list[dict[str, object]],
) -> tuple[list[dict[str, object]], list[dict[str, object]], list[dict[str, object]], dict[str, object]]:
    """Evaluate narrow and broad symbolic rule candidates on forward rows."""
    all_o6_signature, all_o6_states = narrow_all_o6_rule(symbolic_rows)
    broad_states = broad_o6_envelope_states(symbolic_rows)
    narrow_state_support = Counter(
        phase_state(row) for row in forward_rows
        if phase_state(row) in all_o6_states
    )
    broad_state_support = Counter(
        phase_state(row) for row in forward_rows
        if phase_state(row) in broad_states
    )

    narrow_falsifications = [
        row for row in forward_rows
        if phase_state(row) in all_o6_states
        and factor_signature(row) == all_o6_signature
    ]
    broad_falsifications = [
        row for row in forward_rows
        if phase_state(row) in broad_states
        and residue_count(factor_signature(row), "o6") >= 2
    ]

    rule_rows = [
        {
            "rule_id": RULE_ID,
            "candidate_rule": "narrow_all_o6_signature_for_six_phase_states",
            "candidate_status": (
                "survived_fresh_band"
                if not narrow_falsifications
                else "falsified_in_fresh_band"
            ),
            "public_phase_state_count": len(all_o6_states),
            "tested_forward_row_count": sum(narrow_state_support.values()),
            "falsifying_forward_row_count": len(narrow_falsifications),
            "excluded_factor_neighborhood_signature": all_o6_signature,
            "public_phase_states": sorted(all_o6_states),
            "falsification_criterion": (
                "A row falsifies this candidate if S(N) is one of the six "
                "surviving all-o6 public phase states and F(p,q) is the "
                "all-o6 factor-neighborhood signature."
            ),
        },
        {
            "rule_id": RULE_ID,
            "candidate_rule": "broad_at_least_two_o6_residues_for_survivor_phase_states",
            "candidate_status": (
                "survived_fresh_band"
                if not broad_falsifications
                else "falsified_in_fresh_band"
            ),
            "public_phase_state_count": len(broad_states),
            "tested_forward_row_count": sum(broad_state_support.values()),
            "falsifying_forward_row_count": len(broad_falsifications),
            "public_phase_states": sorted(broad_states),
            "falsification_criterion": (
                "A row falsifies this broad envelope if S(N) is one of the "
                "current survivor phase states and F(p,q) contains at least "
                "two o6 factor-side residues."
            ),
        },
    ]
    falsification_rows = [
        {
            "rule_id": RULE_ID,
            "candidate_rule": "narrow_all_o6_signature_for_six_phase_states",
            "case_id": row["case_id"],
            "N": row["N"],
            "p": row["p"],
            "q": row["q"],
            "n_containing_gap_phased_state": phase_state(row),
            "factor_neighborhood_signature": factor_signature(row),
        }
        for row in narrow_falsifications
    ] + [
        {
            "rule_id": RULE_ID,
            "candidate_rule": "broad_at_least_two_o6_residues_for_survivor_phase_states",
            "case_id": row["case_id"],
            "N": row["N"],
            "p": row["p"],
            "q": row["q"],
            "n_containing_gap_phased_state": phase_state(row),
            "factor_neighborhood_signature": factor_signature(row),
            "o6_residue_count": residue_count(factor_signature(row), "o6"),
        }
        for row in broad_falsifications
    ]
    state_support_rows = [
        {
            "rule_id": RULE_ID,
            "candidate_rule": "narrow_all_o6_signature_for_six_phase_states",
            "n_containing_gap_phased_state": state,
            "forward_row_count": narrow_state_support[state],
        }
        for state in sorted(all_o6_states)
    ] + [
        {
            "rule_id": RULE_ID,
            "candidate_rule": "broad_at_least_two_o6_residues_for_survivor_phase_states",
            "n_containing_gap_phased_state": state,
            "forward_row_count": broad_state_support[state],
        }
        for state in sorted(broad_states)
    ]
    summary = {
        "rule_id": RULE_ID,
        "source_rule_id": SOURCE_RULE_ID,
        "status": "measured_symbolic_rule_forward_check",
        "theorem_status": "hypothesis_not_proved",
        "inference_status": "not_live_pedk_inference",
        "candidate_rule_count": len(rule_rows),
        "survived_candidate_rule_count": sum(
            1 for row in rule_rows if row["candidate_status"] == "survived_fresh_band"
        ),
        "falsified_candidate_rule_count": sum(
            1 for row in rule_rows if row["candidate_status"] == "falsified_in_fresh_band"
        ),
        "narrow_all_o6_falsifying_row_count": len(narrow_falsifications),
        "broad_two_o6_falsifying_row_count": len(broad_falsifications),
    }
    return rule_rows, falsification_rows, state_support_rows, summary


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Forward-test symbolic PEDK incompatibility rule candidates."
    )
    parser.add_argument("--min-factor", type=int, default=DEFAULT_MIN_FACTOR)
    parser.add_argument("--max-factor", type=int, default=DEFAULT_MAX_FACTOR)
    parser.add_argument("--max-ratio-numerator", type=int, default=DEFAULT_MAX_RATIO_NUMERATOR)
    parser.add_argument("--max-ratio-denominator", type=int, default=DEFAULT_MAX_RATIO_DENOMINATOR)
    parser.add_argument("--symbolic-rows", type=Path, default=SYMBOLIC_ROWS_PATH)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    """Run symbolic rule candidates on a third fresh factor band."""
    args = parse_args(argv)
    if args.min_factor < 2:
        raise ValueError("min-factor must be at least 2")
    if args.max_factor < args.min_factor:
        raise ValueError("max-factor must be at least min-factor")
    if args.max_ratio_numerator < 1 or args.max_ratio_denominator < 1:
        raise ValueError("ratio terms must be positive")
    if not args.symbolic_rows.exists():
        raise FileNotFoundError(f"missing symbolic rows: {args.symbolic_rows}")

    symbolic_rows = read_jsonl(args.symbolic_rows)
    triples = semiprime_triples(
        args.min_factor,
        args.max_factor,
        args.max_ratio_numerator,
        args.max_ratio_denominator,
    )
    forward_rows = [corpus_row(triple) for triple in triples]
    rule_rows, falsification_rows, state_support_rows, summary = evaluate_rules(
        symbolic_rows,
        forward_rows,
    )
    summary["fresh_band"] = {
        "min_factor": args.min_factor,
        "max_factor": args.max_factor,
        "max_factor_ratio": f"{args.max_ratio_numerator}/{args.max_ratio_denominator}",
        "semiprime_triple_count": len(triples),
    }

    args.output_dir.mkdir(parents=True, exist_ok=True)
    write_jsonl(args.output_dir / "candidate_rule_rows.jsonl", rule_rows)
    write_jsonl(args.output_dir / "falsification_rows.jsonl", falsification_rows)
    write_jsonl(args.output_dir / "state_support_rows.jsonl", state_support_rows)
    write_json(args.output_dir / "summary.json", summary)
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
