#!/usr/bin/env python3
"""Trace strict transported d=4 budget frontier candidates."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


THIS_DIR = Path(__file__).resolve().parent
RULE_ID = "transported_d4_budget_trace_v1"
DEFAULT_BUDGET_ROWS = THIS_DIR / "output" / "transported_d4_budget_current" / "budget_rows.jsonl"
DEFAULT_RECURSIVE_BUDGET_ROWS = (
    THIS_DIR / "output" / "transported_d4_budget_current" / "recursive_budget_rows.jsonl"
)
DEFAULT_OUTPUT_DIR = THIS_DIR / "output" / "transported_d4_budget_trace_current"
TERMINAL_CLASSES = (
    "missing",
    "typed",
    "stale",
    "recursive_cycle",
    "budget_blocked",
    "not_recursive_survivor",
    "still_unresolved",
)


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


def row_key(row: dict[str, object]) -> tuple[str, int, str]:
    """Return the unique recursive lookup key for one row."""
    return (
        str(row["case_id"]),
        int(row["recursion_depth"]),
        str(row["source_anchor"]),
    )


def recursive_index(rows: list[dict[str, object]]) -> dict[tuple[str, int, str], dict[str, object]]:
    """Index recursive rows by case, depth, and public source anchor."""
    index: dict[tuple[str, int, str], dict[str, object]] = {}
    for row in rows:
        key = row_key(row)
        if key in index:
            raise ValueError(f"duplicate recursive row key: {key}")
        index[key] = row
    return index


def terminal_class(row: dict[str, object] | None) -> str:
    """Classify one terminal row using the fixed sidecar priority."""
    if row is None:
        return "missing"
    if bool(row["ledger_eliminated"]):
        return "typed"
    if bool(row["ledger_stale_transport_state"]):
        return "stale"
    if bool(row["ledger_recursive_cycle_state"]):
        return "recursive_cycle"
    if bool(row["budget_blocks_frontier"]):
        return "budget_blocked"
    if not bool(row["ledger_recursive_survivor"]):
        return "not_recursive_survivor"
    return "still_unresolved"


def public_projection(row: dict[str, object]) -> dict[str, object]:
    """Return the public trace fields needed to review one row."""
    return {
        "case_id": row["case_id"],
        "bits": row["bits"],
        "source_anchor": row["source_anchor"],
        "induced_anchor": row["induced_anchor"],
        "ledger_eliminated": row["ledger_eliminated"],
        "ledger_effective_survivor": row["ledger_effective_survivor"],
        "ledger_stale_transport_state": row["ledger_stale_transport_state"],
        "budget_blocks_frontier": row["budget_blocks_frontier"],
        "strict_budget_frontier_candidate": row["strict_budget_frontier_candidate"],
        "net_frontier_budget": row["net_frontier_budget"],
        "induced_carrier_symbol": row["induced_carrier_symbol"],
        "induced_carrier_is_d4": row["induced_carrier_is_d4"],
        "open_d4_carrier": row["open_d4_carrier"],
        "opposite_orientation_polarity": row["opposite_orientation_polarity"],
    }


def recursive_projection(row: dict[str, object]) -> dict[str, object]:
    """Return the public trace fields plus recursive state."""
    payload = public_projection(row)
    payload["recursion_depth"] = row["recursion_depth"]
    payload["ledger_recursive_cycle_state"] = row["ledger_recursive_cycle_state"]
    payload["ledger_recursive_survivor"] = row["ledger_recursive_survivor"]
    payload["terminal_class"] = terminal_class(row)
    return payload


def next_recursive_row(
    index: dict[tuple[str, int, str], dict[str, object]],
    case_id: str,
    depth: int,
    source_anchor: object,
) -> dict[str, object] | None:
    """Return the next recursive row for one public anchor transition."""
    if source_anchor is None:
        return None
    return index.get((case_id, depth, str(source_anchor)))


def trace_strict_candidate(
    start: dict[str, object],
    index: dict[tuple[str, int, str], dict[str, object]],
    max_depth: int,
) -> dict[str, object]:
    """Trace one strict direct candidate through the recursive budget surface."""
    case_id = str(start["case_id"])
    path: list[dict[str, object]] = []
    next_anchor = start["induced_anchor"]
    terminal = "still_unresolved"
    terminal_row = None

    for depth in range(1, max_depth + 1):
        row = next_recursive_row(index, case_id, depth, next_anchor)
        terminal = terminal_class(row)
        if row is None:
            break
        terminal_row = row
        path.append(recursive_projection(row))
        if terminal != "still_unresolved":
            break
        next_anchor = row["induced_anchor"]

    return {
        "rule_id": RULE_ID,
        "case_id": start["case_id"],
        "bits": start["bits"],
        "start": public_projection(start),
        "path": path,
        "trace_step_count": len(path),
        "terminal_class": terminal,
        "terminal_depth": None if terminal_row is None else terminal_row["recursion_depth"],
        "terminal_conditions": {} if terminal_row is None else recursive_projection(terminal_row),
    }


def parent_rows(
    rows: list[dict[str, object]],
    survivor: dict[str, object],
) -> list[dict[str, object]]:
    """Return previous-depth rows whose induced anchor feeds one survivor."""
    depth = int(survivor["recursion_depth"])
    return [
        row
        for row in rows
        if str(row["case_id"]) == str(survivor["case_id"])
        and int(row["recursion_depth"]) == depth - 1
        and row["induced_anchor"] == survivor["source_anchor"]
    ]


def inspect_recursive_survivor(
    survivor: dict[str, object],
    rows: list[dict[str, object]],
    index: dict[tuple[str, int, str], dict[str, object]],
) -> dict[str, object]:
    """Inspect one non-depth0 recursive survivor and its immediate child."""
    child = next_recursive_row(
        index,
        str(survivor["case_id"]),
        int(survivor["recursion_depth"]) + 1,
        survivor["induced_anchor"],
    )
    return {
        "rule_id": RULE_ID,
        "case_id": survivor["case_id"],
        "bits": survivor["bits"],
        "survivor": recursive_projection(survivor),
        "parent_count": len(parent_rows(rows, survivor)),
        "parents": [recursive_projection(row) for row in parent_rows(rows, survivor)],
        "child": None if child is None else recursive_projection(child),
        "child_terminal_class": terminal_class(child),
    }


def count_partition(rows: list[dict[str, object]], key: str) -> dict[str, int]:
    """Return counts for one string field with stable keys."""
    counts = {terminal: 0 for terminal in TERMINAL_CLASSES}
    for row in rows:
        value = str(row[key])
        counts[value] = counts.get(value, 0) + 1
    return {key: value for key, value in counts.items() if value}


def summarize(
    trace_rows: list[dict[str, object]],
    survivor_rows: list[dict[str, object]],
    budget_rows: list[dict[str, object]],
    recursive_rows: list[dict[str, object]],
) -> dict[str, object]:
    """Return compact trace summary statistics."""
    return {
        "rule_id": RULE_ID,
        "budget_row_count": len(budget_rows),
        "recursive_budget_row_count": len(recursive_rows),
        "strict_candidate_count": len(trace_rows),
        "terminal_partition": count_partition(trace_rows, "terminal_class"),
        "max_trace_steps": max((int(row["trace_step_count"]) for row in trace_rows), default=0),
        "missing_next_count": sum(1 for row in trace_rows if row["terminal_class"] == "missing"),
        "still_unresolved_count": sum(
            1 for row in trace_rows if row["terminal_class"] == "still_unresolved"
        ),
        "non_depth0_recursive_survivor_count": len(survivor_rows),
        "non_depth0_survivor_child_terminal_partition": count_partition(
            survivor_rows,
            "child_terminal_class",
        ),
    }


def run_probe(
    budget_rows_path: Path,
    recursive_budget_rows_path: Path,
) -> tuple[list[dict[str, object]], list[dict[str, object]], dict[str, object]]:
    """Run the strict d=4 frontier trace over current sidecar rows."""
    budget_rows = read_jsonl(budget_rows_path)
    recursive_rows = read_jsonl(recursive_budget_rows_path)
    index = recursive_index(recursive_rows)
    max_depth = max((int(row["recursion_depth"]) for row in recursive_rows), default=0)
    strict_rows = [row for row in budget_rows if bool(row["strict_budget_frontier_candidate"])]
    trace_rows = [trace_strict_candidate(row, index, max_depth) for row in strict_rows]
    recursive_survivors = [
        row
        for row in recursive_rows
        if int(row["recursion_depth"]) > 0 and bool(row["ledger_recursive_survivor"])
    ]
    survivor_rows = [
        inspect_recursive_survivor(row, recursive_rows, index)
        for row in recursive_survivors
    ]
    return trace_rows, survivor_rows, summarize(
        trace_rows,
        survivor_rows,
        budget_rows,
        recursive_rows,
    )


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Trace strict transported d=4 budget frontier candidates."
    )
    parser.add_argument(
        "--budget-rows",
        type=Path,
        default=DEFAULT_BUDGET_ROWS,
        help="Input budget_rows.jsonl from transported_d4_budget_probe.py.",
    )
    parser.add_argument(
        "--recursive-budget-rows",
        type=Path,
        default=DEFAULT_RECURSIVE_BUDGET_ROWS,
        help="Input recursive_budget_rows.jsonl from transported_d4_budget_probe.py.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help="Directory for trace_rows.jsonl, recursive_survivor_rows.jsonl, and summary.json.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    """Run the strict d=4 budget trace sidecar."""
    args = parse_args(argv)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    trace_rows, survivor_rows, summary = run_probe(
        args.budget_rows,
        args.recursive_budget_rows,
    )
    write_jsonl(args.output_dir / "trace_rows.jsonl", trace_rows)
    write_jsonl(args.output_dir / "recursive_survivor_rows.jsonl", survivor_rows)
    write_json(args.output_dir / "summary.json", summary)
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
