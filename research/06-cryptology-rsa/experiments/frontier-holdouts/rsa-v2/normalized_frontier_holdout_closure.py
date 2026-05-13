"""Hold out normalized frontier closure as a public PGS sidecar.

This sidecar consumes the public rows emitted by
toy_normalized_frontier_closure_sweep.py. It pre-registers one normalized
frontier invariant, applies it without fitting thresholds or branching by rung,
and reports resolved only when no public survivor remains.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


BASE_DIR = Path(__file__).resolve().parent
DEFAULT_FRONTIER_ROWS = (
    BASE_DIR
    / "output"
    / "toy_normalized_frontier_closure_sweep_current"
    / "frontier_rows.jsonl"
)
DEFAULT_SWEEP_ROWS = (
    BASE_DIR
    / "output"
    / "toy_normalized_frontier_closure_sweep_current"
    / "sweep_rows.jsonl"
)
DEFAULT_OUTPUT_DIR = (
    BASE_DIR / "output" / "normalized_frontier_holdout_closure_current"
)

RULE_ID = "normalized_frontier_holdout_closure_v1"
INVARIANT_NAME = "Normalized Frontier Dominance Invariant"
EXPECTED_PUBLIC_STATE = {
    "ledger_effective_survivor_count": 202,
    "strict_d4_frontier_count": 50,
    "strict_d4_collapse_count": 50,
    "strict_d4_live_after_trace": 0,
    "non_strict_live_after_trace": 2,
    "normalized_live_frontier_count": 2,
}
ALLOWED_FRONTIER_KEYS = {
    "N",
    "bits",
    "budget_blocks_frontier",
    "case_id",
    "induced_anchor",
    "induced_carrier_committed",
    "induced_carrier_is_d4",
    "induced_d4_uncommitted_count",
    "net_frontier_budget",
    "normalized_live_after_trace",
    "open_d4_carrier",
    "rule_id",
    "source_anchor",
    "strict_d4_frontier_candidate",
    "terminal_class",
    "terminal_exit_rule_name",
}
ALLOWED_SWEEP_KEYS = {
    "N",
    "bits",
    "case_id",
    "certificate_status_after",
    "certificate_status_before",
    "frontier_empty_but_unresolved",
    "frontier_live_but_closed",
    "ledger_effective_survivors",
    "non_strict_undominated_live_after_trace",
    "normalized_live_frontier_count",
    "rule_id",
    "stale_cycle_absorption_status",
    "strict_d4_frontier_count",
    "strict_d4_live_after_trace",
    "terminal_exit_rule_names",
    "terminal_without_named_public_invariant",
    "toy_row_id",
}
LIVE_ROW_AUDIT_KEYS = (
    "rule_id",
    "case_id",
    "bits",
    "N",
    "source_anchor",
    "induced_anchor",
    "strict_d4_frontier_candidate",
    "open_d4_carrier",
    "induced_carrier_is_d4",
    "induced_carrier_committed",
    "induced_d4_uncommitted_count",
    "net_frontier_budget",
    "budget_blocks_frontier",
    "terminal_class",
    "terminal_exit_rule_name",
    "normalized_live_after_trace",
)
FORBIDDEN_MECHANISM_MANIFEST = [
    "hidden factor labels",
    "audit factor labels",
    "divisibility gates",
    "gcd gates",
    "product closure",
    "factor APIs",
    "primality APIs",
    "fixed-radius chambers",
    "endpoint-budget resolver rules",
    "per-rung special cases",
    "randomness",
    "fallback paths",
]


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    """Read newline-delimited JSON rows."""
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]


def write_json(path: Path, payload: Any) -> None:
    """Write one LF-terminated JSON artifact."""
    path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    """Write LF-terminated JSONL rows."""
    text = "\n".join(json.dumps(row, sort_keys=True) for row in rows)
    path.write_text(text + "\n", encoding="utf-8")


def count_true(rows: list[dict[str, Any]], key: str) -> int:
    """Count rows with a truthy public field."""
    return sum(1 for row in rows if row[key])


def public_state(frontier_rows: list[dict[str, Any]]) -> dict[str, int]:
    """Compute the frozen public state from frontier rows only."""
    strict_count = count_true(frontier_rows, "strict_d4_frontier_candidate")
    strict_live = sum(
        1
        for row in frontier_rows
        if row["strict_d4_frontier_candidate"] and row["normalized_live_after_trace"]
    )
    return {
        "ledger_effective_survivor_count": len(frontier_rows),
        "strict_d4_frontier_count": strict_count,
        "strict_d4_collapse_count": strict_count - strict_live,
        "strict_d4_live_after_trace": strict_live,
        "non_strict_live_after_trace": sum(
            1
            for row in frontier_rows
            if row["normalized_live_after_trace"]
            and not row["strict_d4_frontier_candidate"]
        ),
        "normalized_live_frontier_count": count_true(
            frontier_rows, "normalized_live_after_trace"
        ),
    }


def key_violations(
    rows: list[dict[str, Any]], allowed_keys: set[str], source_name: str
) -> list[dict[str, Any]]:
    """Return public-input key violations for one row family."""
    violations = []
    for index, row in enumerate(rows):
        keys = set(row)
        if keys != allowed_keys:
            violations.append(
                {
                    "source": source_name,
                    "row_index": index,
                    "extra_keys": sorted(keys - allowed_keys),
                    "missing_keys": sorted(allowed_keys - keys),
                }
            )
    return violations


def registered_invariant() -> dict[str, Any]:
    """Return the pre-registered invariant before holdout application."""
    return {
        "name": INVARIANT_NAME,
        "rule_id": RULE_ID,
        "registration_status": "pre_registered_before_holdout_application",
        "public_coordinates": [
            "strict_d4_frontier_candidate",
            "open_d4_carrier",
            "induced_carrier_is_d4",
            "induced_carrier_committed",
            "induced_d4_uncommitted_count",
            "net_frontier_budget",
            "terminal_class",
            "terminal_exit_rule_name",
        ],
        "decision_rule": (
            "A normalized frontier row is eliminated only when the public row "
            "is a strict d=4 frontier candidate and carries a named public "
            "terminal exit from the strict d=4 collapse trace."
        ),
        "non_strict_clause": (
            "A non-strict live row remains live unless the same public "
            "normalized frontier witness eliminates it."
        ),
        "threshold_policy": "no fitted threshold",
        "rung_policy": "one rule for every rung",
        "resolver_policy": "sidecar evidence only",
    }


def holdout_action(row: dict[str, Any]) -> tuple[str, bool]:
    """Apply the pre-registered invariant to one public frontier row."""
    if not row["normalized_live_after_trace"]:
        return "already_not_live_after_public_frontier_sweep", False
    if row["strict_d4_frontier_candidate"] and row["terminal_exit_rule_name"]:
        return "eliminated_by_public_strict_d4_terminal_witness", False
    return "remains_live_no_public_normalized_frontier_witness", True


def ledger_row(row: dict[str, Any]) -> dict[str, Any]:
    """Build one before-after holdout ledger row from public fields."""
    action, live_after = holdout_action(row)
    return {
        "rule_id": RULE_ID,
        "case_id": row["case_id"],
        "bits": row["bits"],
        "N": row["N"],
        "source_anchor": row["source_anchor"],
        "induced_anchor": row["induced_anchor"],
        "strict_d4_frontier_candidate": row["strict_d4_frontier_candidate"],
        "public_terminal_exit_rule_name": row["terminal_exit_rule_name"],
        "before_holdout_live": row["normalized_live_after_trace"],
        "holdout_action": action,
        "after_holdout_live": live_after,
    }


def live_audit_row(row: dict[str, Any]) -> dict[str, Any]:
    """Build one public live-row audit entry."""
    audit_row = {key: row[key] for key in LIVE_ROW_AUDIT_KEYS}
    audit_row["holdout_survivor_reason"] = (
        "no_public_normalized_frontier_witness_for_non_strict_row"
    )
    return audit_row


def checker_report(
    frontier_rows: list[dict[str, Any]],
    sweep_rows: list[dict[str, Any]],
    state: dict[str, int],
) -> dict[str, Any]:
    """Report whether the sidecar input contract stayed public."""
    violations = []
    violations.extend(
        key_violations(frontier_rows, ALLOWED_FRONTIER_KEYS, "frontier_rows")
    )
    violations.extend(key_violations(sweep_rows, ALLOWED_SWEEP_KEYS, "sweep_rows"))
    if state != EXPECTED_PUBLIC_STATE:
        violations.append(
            {
                "source": "public_state",
                "expected": EXPECTED_PUBLIC_STATE,
                "observed": state,
            }
        )
    return {
        "rule_id": RULE_ID,
        "status": "passed" if not violations else "failed",
        "violations": violations,
        "allowed_frontier_keys": sorted(ALLOWED_FRONTIER_KEYS),
        "allowed_sweep_keys": sorted(ALLOWED_SWEEP_KEYS),
        "forbidden_mechanism_manifest": FORBIDDEN_MECHANISM_MANIFEST,
    }


def run_probe(
    frontier_rows_path: Path,
    sweep_rows_path: Path,
) -> tuple[
    dict[str, Any],
    dict[str, Any],
    dict[str, Any],
    list[dict[str, Any]],
    list[dict[str, Any]],
    dict[str, Any],
]:
    """Run holdout closure over public normalized frontier rows."""
    frontier_rows = read_jsonl(frontier_rows_path)
    sweep_rows = read_jsonl(sweep_rows_path)
    state = public_state(frontier_rows)
    invariant = registered_invariant()
    before_after_rows = [ledger_row(row) for row in frontier_rows]
    live_rows = [
        live_audit_row(row)
        for row in frontier_rows
        if row["normalized_live_after_trace"]
    ]
    live_after_count = sum(1 for row in before_after_rows if row["after_holdout_live"])
    checker = checker_report(frontier_rows, sweep_rows, state)
    case_live_actions = sorted(
        {
            (row["case_id"], row["holdout_action"])
            for row in before_after_rows
            if row["before_holdout_live"]
        }
    )
    action_shapes = {action for _, action in case_live_actions}
    falsification_reasons = []
    if live_after_count:
        falsification_reasons.append("survivor_remains_after_holdout")
    if len(action_shapes) > 1:
        falsification_reasons.append("different_live_row_logic_by_rung")
    if checker["status"] != "passed":
        falsification_reasons.append("forbidden_or_non_public_mechanism_detected")

    summary = {
        "rule_id": RULE_ID,
        "invariant_name": INVARIANT_NAME,
        "frontier_rows_path": str(frontier_rows_path),
        "sweep_rows_path": str(sweep_rows_path),
        "frozen_public_state": state,
        "expected_public_state": EXPECTED_PUBLIC_STATE,
        "public_state_matches_expected": state == EXPECTED_PUBLIC_STATE,
        "pre_registered_invariant_applied": True,
        "threshold_fitted_from_holdout_rows": False,
        "case_specific_logic_used": len(action_shapes) > 1,
        "forbidden_mechanism_entered": checker["status"] != "passed",
        "before_holdout_live_count": count_true(
            frontier_rows, "normalized_live_after_trace"
        ),
        "after_holdout_live_count": live_after_count,
        "resolved": not falsification_reasons,
        "status": (
            "resolved_by_normalized_frontier_holdout"
            if not falsification_reasons
            else "unresolved_by_holdout_survivors"
        ),
        "falsified": bool(falsification_reasons),
        "falsification_reasons": falsification_reasons,
        "case_live_actions": [
            {"case_id": case_id, "holdout_action": action}
            for case_id, action in case_live_actions
        ],
    }
    manifest = {
        "rule_id": RULE_ID,
        "source_artifacts": {
            "frontier_rows": str(frontier_rows_path),
            "sweep_rows": str(sweep_rows_path),
        },
        "frozen_public_state": state,
        "expected_public_state": EXPECTED_PUBLIC_STATE,
        "public_state_matches_expected": state == EXPECTED_PUBLIC_STATE,
        "forbidden_mechanism_manifest": FORBIDDEN_MECHANISM_MANIFEST,
    }
    return manifest, invariant, checker, before_after_rows, live_rows, summary


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Hold out normalized frontier closure against public rows."
    )
    parser.add_argument(
        "--frontier-rows",
        type=Path,
        default=DEFAULT_FRONTIER_ROWS,
        help="Public frontier_rows.jsonl from toy_normalized_frontier_closure_sweep.py.",
    )
    parser.add_argument(
        "--sweep-rows",
        type=Path,
        default=DEFAULT_SWEEP_ROWS,
        help="Public sweep_rows.jsonl from toy_normalized_frontier_closure_sweep.py.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help="Directory for holdout sidecar artifacts.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    """Run the normalized frontier holdout closure sidecar."""
    args = parse_args(argv)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    manifest, invariant, checker, ledger_rows, live_rows, summary = run_probe(
        args.frontier_rows,
        args.sweep_rows,
    )
    write_json(args.output_dir / "input_manifest.json", manifest)
    write_json(args.output_dir / "pre_registered_invariant.json", invariant)
    write_json(args.output_dir / "checker_report.json", checker)
    write_jsonl(args.output_dir / "before_after_ledger.jsonl", ledger_rows)
    write_json(args.output_dir / "live_rows_audit.json", live_rows)
    write_json(args.output_dir / "summary.json", summary)
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
