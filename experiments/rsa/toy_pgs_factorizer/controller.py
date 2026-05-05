#!/usr/bin/env python3
"""Controller for the toy PGSPG factorizer experiment."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from pgs_factorizer import factorize, write_jsonl  # noqa: E402
from validator import (  # noqa: E402
    DEFAULT_MAX_AUDIT_FACTOR,
    decision_knob_rows,
    directed_reset_replay_matrix_rows,
    none_none_replay_alias_rows,
    prime_pairs,
    pgspg_law_matrix_rows,
    rule_audit_matrix_rows,
    structural_candidate_matrix_rows,
    upper_width_failure_artifact,
    upper_width_failure_rows,
    validate_inference_rows,
    write_csv,
    write_decision_knob_csv,
    write_directed_reset_replay_matrix_csv,
    write_none_none_replay_alias_csv,
    write_pgspg_law_matrix_csv,
    write_rule_audit_matrix_csv,
    write_structural_candidate_matrix_csv,
    write_upper_width_failure_csv,
)


DEFAULT_OUTPUT_DIR = SCRIPT_DIR / "output"


def case_id(max_audit_factor: int, p_value: int, q_value: int) -> str:
    """Return one deterministic toy case id."""
    return f"toy_le_{max_audit_factor}_{p_value}_{q_value}"


def write_json(path: Path, row: dict[str, object]) -> None:
    """Write one LF-terminated JSON object."""
    path.write_text(json.dumps(row, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_public_cases(path: Path, rows: list[dict[str, object]]) -> None:
    """Write public case rows without audit factors."""
    write_jsonl(path, rows)


def write_survivors(path: Path, rows: list[dict[str, object]]) -> None:
    """Write survivor rows."""
    write_jsonl(path, rows)


def summary_rows(audit_rows: list[dict[str, object]]) -> dict[str, object]:
    """Return a compact experiment summary."""
    total = len(audit_rows)
    resolved = sum(1 for row in audit_rows if row["inference_status"] == "resolved")
    audit_pass = sum(1 for row in audit_rows if row["audit_status"] == "audit_pass")
    audit_fail = sum(1 for row in audit_rows if row["audit_status"] == "audit_fail")
    return {
        "total_cases": total,
        "resolved": resolved,
        "unresolved": total - resolved,
        "audit_pass": audit_pass,
        "audit_fail": audit_fail,
        "resolution_rate": resolved / total,
        "resolved_precision": 0.0 if resolved == 0 else audit_pass / resolved,
    }


def run_experiment(
    output_dir: Path,
    max_audit_factor: int = DEFAULT_MAX_AUDIT_FACTOR,
    max_candidate_factor: int | None = None,
) -> dict[str, object]:
    """Run the full toy experiment."""
    if max_candidate_factor is None:
        max_candidate_factor = max_audit_factor
    output_dir.mkdir(parents=True, exist_ok=True)
    public_cases: list[dict[str, object]] = []
    inference_rows: list[dict[str, object]] = []
    survivor_rows: list[dict[str, object]] = []

    for p_value, q_value in prime_pairs(max_audit_factor):
        n_value = p_value * q_value
        current_case_id = case_id(max_audit_factor, p_value, q_value)
        public_cases.append({"case_id": current_case_id, "N": n_value})
        inference, survivors = factorize(n_value, max_factor=max_candidate_factor)
        inference["case_id"] = current_case_id
        inference_rows.append(inference)
        for survivor in survivors:
            survivor_row = dict(survivor)
            survivor_row["case_id"] = current_case_id
            survivor_rows.append(survivor_row)

    audit_rows = validate_inference_rows(
        inference_rows,
        max_factor=max_audit_factor,
    )
    knob_rows = decision_knob_rows(
        inference_rows,
        survivor_rows,
        max_factor=max_audit_factor,
    )
    summary = summary_rows(audit_rows)
    write_public_cases(output_dir / "public_cases.jsonl", public_cases)
    write_jsonl(output_dir / "inference_rows.jsonl", inference_rows)
    write_survivors(output_dir / "survivor_rows.jsonl", survivor_rows)
    write_csv(output_dir / "audit_results.csv", audit_rows)
    write_decision_knob_csv(output_dir / "decision_knob_rows.csv", knob_rows)
    write_rule_audit_matrix_csv(
        output_dir / "rule_audit_matrix.csv",
        rule_audit_matrix_rows(
            inference_rows,
            survivor_rows,
            max_factor=max_audit_factor,
        ),
    )
    write_structural_candidate_matrix_csv(
        output_dir / "structural_candidate_matrix.csv",
        structural_candidate_matrix_rows(
            inference_rows,
            survivor_rows,
            max_factor=max_audit_factor,
        ),
    )
    write_pgspg_law_matrix_csv(
        output_dir / "pgspg_law_matrix.csv",
        pgspg_law_matrix_rows(
            inference_rows,
            survivor_rows,
            max_factor=max_audit_factor,
        ),
    )
    write_directed_reset_replay_matrix_csv(
        output_dir / "directed_reset_replay_matrix.csv",
        directed_reset_replay_matrix_rows(
            inference_rows,
            survivor_rows,
            max_factor=max_audit_factor,
        ),
    )
    write_none_none_replay_alias_csv(
        output_dir / "none_none_replay_alias_rows.csv",
        none_none_replay_alias_rows(
            inference_rows,
            survivor_rows,
            max_factor=max_audit_factor,
        ),
    )
    write_upper_width_failure_csv(
        output_dir / "upper_width_failure_rows.csv",
        upper_width_failure_rows(
            inference_rows,
            survivor_rows,
            max_factor=max_audit_factor,
        ),
    )
    write_json(
        output_dir / "upper_width_first_failure.json",
        upper_width_failure_artifact(
            inference_rows,
            survivor_rows,
            max_factor=max_audit_factor,
        ),
    )
    write_json(output_dir / "summary.json", summary)
    return summary


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Run the toy PGSPG experiment.")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--max-audit-factor", type=int, default=DEFAULT_MAX_AUDIT_FACTOR)
    parser.add_argument("--max-candidate-factor", type=int)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    """Run the controller."""
    args = parse_args(argv)
    summary = run_experiment(
        args.output_dir,
        max_audit_factor=args.max_audit_factor,
        max_candidate_factor=args.max_candidate_factor,
    )
    print(json.dumps(summary, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
