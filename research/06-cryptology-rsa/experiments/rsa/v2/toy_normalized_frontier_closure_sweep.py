#!/usr/bin/env python3
"""Check normalized frontier closure against transported d=4 sidecars."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


THIS_DIR = Path(__file__).resolve().parent
RULE_ID = "toy_normalized_frontier_closure_sweep_v1"
DEFAULT_BUDGET_ROWS = THIS_DIR / "output" / "transported_d4_budget_current" / "budget_rows.jsonl"
DEFAULT_TRACE_ROWS = THIS_DIR / "output" / "transported_d4_budget_trace_current" / "trace_rows.jsonl"
DEFAULT_INFERENCE_ROWS = THIS_DIR / "output" / "inference_rows.jsonl"
DEFAULT_OUTPUT_DIR = THIS_DIR / "output" / "toy_normalized_frontier_closure_sweep_current"
NAMED_TERMINAL_RULES = {
    "typed": "transported_story_ledger_typed_elimination",
    "stale": "transported_story_stale_transport_absorption",
    "recursive_cycle": "transported_story_recursive_cycle_absorption",
}


def read_jsonl(path: Path) -> list[dict[str, object]]:
    """Read LF-delimited JSON rows."""
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def write_json(path: Path, payload: dict[str, object]) -> None:
    """Write one LF-terminated JSON object."""
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_jsonl(path: Path, rows: list[dict[str, object]]) -> None:
    """Write LF-delimited JSON rows."""
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for row in rows:
            handle.write(json.dumps(row, sort_keys=True))
            handle.write("\n")


def case_statuses(rows: list[dict[str, object]]) -> dict[str, str]:
    """Return official inference status by public case id."""
    statuses: dict[str, str] = {}
    for row in rows:
        case_id = str(row["case_id"])
        if str(row["status"]) == "public_endpoint_class_found":
            statuses[case_id] = "public_endpoint_class_found"
        else:
            statuses[case_id] = str(row["unresolved_reason"])
    return statuses


def trace_index(rows: list[dict[str, object]]) -> dict[tuple[str, str], dict[str, object]]:
    """Index strict trace rows by case id and public source anchor."""
    index: dict[tuple[str, str], dict[str, object]] = {}
    for row in rows:
        start = row["start"]
        key = (str(row["case_id"]), str(start["source_anchor"]))
        if key in index:
            raise ValueError(f"duplicate trace row key: {key}")
        index[key] = row
    return index


def named_terminal_rule(terminal_class: str) -> str | None:
    """Return the public invariant name for one terminal class."""
    return NAMED_TERMINAL_RULES.get(terminal_class)


def row_live_after_trace(row: dict[str, object], trace: dict[str, object] | None) -> bool:
    """Return whether one effective row remains live after normalized tracing."""
    if bool(row["strict_budget_frontier_candidate"]):
        if trace is None:
            return True
        return named_terminal_rule(str(trace["terminal_class"])) is None
    return (
        not bool(row["budget_blocks_frontier"])
        and int(row["induced_d4_uncommitted_count"]) > 0
    )


def frontier_projection(
    row: dict[str, object],
    trace: dict[str, object] | None,
) -> dict[str, object]:
    """Return one normalized frontier diagnostic row."""
    terminal_class = None if trace is None else str(trace["terminal_class"])
    terminal_rule = None if terminal_class is None else named_terminal_rule(terminal_class)
    live = row_live_after_trace(row, trace)
    return {
        "rule_id": RULE_ID,
        "case_id": row["case_id"],
        "bits": row["bits"],
        "N": row["N"],
        "source_anchor": row["source_anchor"],
        "induced_anchor": row["induced_anchor"],
        "strict_d4_frontier_candidate": row["strict_budget_frontier_candidate"],
        "budget_blocks_frontier": row["budget_blocks_frontier"],
        "open_d4_carrier": row["open_d4_carrier"],
        "induced_carrier_is_d4": row["induced_carrier_is_d4"],
        "induced_carrier_committed": row["induced_carrier_committed"],
        "induced_d4_uncommitted_count": row["induced_d4_uncommitted_count"],
        "net_frontier_budget": row["net_frontier_budget"],
        "terminal_class": terminal_class,
        "terminal_exit_rule_name": terminal_rule,
        "normalized_live_after_trace": live,
    }


def count_true(rows: list[dict[str, object]], key: str) -> int:
    """Return the number of rows with a true boolean field."""
    return sum(1 for row in rows if bool(row[key]))


def partition(rows: list[dict[str, object]], key: str) -> dict[str, int]:
    """Return stable string counts for one row field."""
    counts: dict[str, int] = {}
    for row in rows:
        value = str(row[key])
        counts[value] = counts.get(value, 0) + 1
    return {key: counts[key] for key in sorted(counts)}


def case_row(
    case_id: str,
    budget_rows: list[dict[str, object]],
    trace_rows: list[dict[str, object]],
    status_before: str,
) -> tuple[dict[str, object], list[dict[str, object]]]:
    """Return one case-level normalized closure row and its frontier projections."""
    traces = trace_index(trace_rows)
    effective_rows = [row for row in budget_rows if bool(row["ledger_effective_survivor"])]
    frontier_rows = [
        frontier_projection(row, traces.get((case_id, str(row["source_anchor"]))))
        for row in effective_rows
    ]
    strict_frontier_rows = [
        row for row in frontier_rows if bool(row["strict_d4_frontier_candidate"])
    ]
    strict_live = [
        row
        for row in strict_frontier_rows
        if bool(row["normalized_live_after_trace"])
    ]
    non_strict_live = [
        row
        for row in frontier_rows
        if not bool(row["strict_d4_frontier_candidate"])
        and bool(row["normalized_live_after_trace"])
    ]
    terminal_rule_names = sorted(
        {
            str(row["terminal_exit_rule_name"])
            for row in strict_frontier_rows
            if row["terminal_exit_rule_name"] is not None
        }
    )
    terminal_without_named_rule = [
        row
        for row in strict_frontier_rows
        if row["terminal_class"] is not None and row["terminal_exit_rule_name"] is None
    ]
    normalized_live_count = len(strict_live) + len(non_strict_live)
    status_after = (
        "sidecar_supported_normalized_frontier_empty"
        if normalized_live_count == 0 and not terminal_without_named_rule
        else "sidecar_blocked_by_live_normalized_frontier"
    )
    summary = {
        "rule_id": RULE_ID,
        "toy_row_id": case_id,
        "case_id": case_id,
        "bits": budget_rows[0]["bits"],
        "N": budget_rows[0]["N"],
        "certificate_status_before": status_before,
        "ledger_effective_survivors": len(effective_rows),
        "strict_d4_frontier_count": len(strict_frontier_rows),
        "strict_d4_live_after_trace": len(strict_live),
        "non_strict_undominated_live_after_trace": len(non_strict_live),
        "stale_cycle_absorption_status": (
            "absorbed"
            if not strict_live and not terminal_without_named_rule
            else "not_absorbed"
        ),
        "terminal_exit_rule_names": terminal_rule_names,
        "terminal_without_named_public_invariant": len(terminal_without_named_rule),
        "normalized_live_frontier_count": normalized_live_count,
        "frontier_empty_but_unresolved": (
            normalized_live_count == 0 and status_before != "public_endpoint_class_found"
        ),
        "frontier_live_but_closed": (
            normalized_live_count > 0 and status_before == "public_endpoint_class_found"
        ),
        "certificate_status_after": status_after,
    }
    return summary, frontier_rows


def run_probe(
    budget_rows_path: Path,
    trace_rows_path: Path,
    inference_rows_path: Path,
) -> tuple[list[dict[str, object]], list[dict[str, object]], dict[str, object]]:
    """Run the normalized frontier closure sweep."""
    budget_rows = read_jsonl(budget_rows_path)
    trace_rows = read_jsonl(trace_rows_path)
    statuses = case_statuses(read_jsonl(inference_rows_path))
    case_ids = sorted({str(row["case_id"]) for row in budget_rows})
    sweep_rows: list[dict[str, object]] = []
    frontier_rows: list[dict[str, object]] = []
    for case_id in case_ids:
        case_budget_rows = [row for row in budget_rows if str(row["case_id"]) == case_id]
        case_trace_rows = [row for row in trace_rows if str(row["case_id"]) == case_id]
        row, projections = case_row(
            case_id,
            case_budget_rows,
            case_trace_rows,
            statuses.get(case_id, "missing_inference_status"),
        )
        sweep_rows.append(row)
        frontier_rows.extend(projections)

    summary = {
        "rule_id": RULE_ID,
        "case_count": len(sweep_rows),
        "frontier_row_count": len(frontier_rows),
        "ledger_effective_survivor_count": sum(
            int(row["ledger_effective_survivors"]) for row in sweep_rows
        ),
        "strict_d4_frontier_count": sum(
            int(row["strict_d4_frontier_count"]) for row in sweep_rows
        ),
        "strict_d4_live_after_trace": sum(
            int(row["strict_d4_live_after_trace"]) for row in sweep_rows
        ),
        "non_strict_undominated_live_after_trace": sum(
            int(row["non_strict_undominated_live_after_trace"]) for row in sweep_rows
        ),
        "normalized_live_frontier_count": sum(
            int(row["normalized_live_frontier_count"]) for row in sweep_rows
        ),
        "frontier_empty_but_unresolved": count_true(
            sweep_rows,
            "frontier_empty_but_unresolved",
        ),
        "frontier_live_but_closed": count_true(sweep_rows, "frontier_live_but_closed"),
        "terminal_without_named_public_invariant": sum(
            int(row["terminal_without_named_public_invariant"]) for row in sweep_rows
        ),
        "certificate_status_after_partition": partition(
            sweep_rows,
            "certificate_status_after",
        ),
    }
    return sweep_rows, frontier_rows, summary


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Sweep normalized frontier closure over transported d=4 sidecars."
    )
    parser.add_argument(
        "--budget-rows",
        type=Path,
        default=DEFAULT_BUDGET_ROWS,
        help="Input budget_rows.jsonl from transported_d4_budget_probe.py.",
    )
    parser.add_argument(
        "--trace-rows",
        type=Path,
        default=DEFAULT_TRACE_ROWS,
        help="Input trace_rows.jsonl from transported_d4_budget_trace.py.",
    )
    parser.add_argument(
        "--inference-rows",
        type=Path,
        default=DEFAULT_INFERENCE_ROWS,
        help="Input inference_rows.jsonl from run_experiment.py.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help="Directory for sweep_rows.jsonl, frontier_rows.jsonl, and summary.json.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    """Run the normalized frontier closure sweep sidecar."""
    args = parse_args(argv)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    sweep_rows, frontier_rows, summary = run_probe(
        args.budget_rows,
        args.trace_rows,
        args.inference_rows,
    )
    write_jsonl(args.output_dir / "sweep_rows.jsonl", sweep_rows)
    write_jsonl(args.output_dir / "frontier_rows.jsonl", frontier_rows)
    write_json(args.output_dir / "summary.json", summary)
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
