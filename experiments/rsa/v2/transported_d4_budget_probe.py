#!/usr/bin/env python3
"""Measure transported d=4 chamber budget on RSA v2 story-law rows."""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
SOURCE_DIR = ROOT / "src" / "python"
if str(SOURCE_DIR) not in sys.path:
    sys.path.insert(0, str(SOURCE_DIR))

from z_band_prime_composite_field import divisor_counts_segment  # noqa: E402


THIS_DIR = Path(__file__).resolve().parent
RULE_ID = "transported_d4_budget_v1"
DEFAULT_STORY_ROWS = THIS_DIR / "output" / "transported_story_law_current" / "story_law_rows.jsonl"
DEFAULT_RECURSIVE_ROWS = THIS_DIR / "output" / "transported_story_law_current" / "recursive_rows.jsonl"
DEFAULT_OUTPUT_DIR = THIS_DIR / "output" / "transported_d4_budget_current"


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


def value(row: dict[str, object], key: str) -> int:
    """Return one integer coordinate from a public row field."""
    return int(str(row[key]))


def optional_value(row: dict[str, object], key: str) -> int | None:
    """Return one optional integer coordinate from a public row field."""
    item = row[key]
    if item is None:
        return None
    return int(str(item))


def d4_values(lo_exclusive: int, hi_inclusive: int) -> list[int]:
    """Return all d=4 coordinates in one public integer interval."""
    if hi_inclusive <= lo_exclusive:
        return []
    start = lo_exclusive + 1
    stop = hi_inclusive + 1
    counts = divisor_counts_segment(start, stop)
    return [
        coordinate
        for coordinate, divisor_count in zip(range(start, stop), counts, strict=True)
        if int(divisor_count) == 4
    ]


def inside(point: int, lo: int, hi: int) -> bool:
    """Return whether one coordinate lies inside a closed interval."""
    return min(lo, hi) <= point <= max(lo, hi)


def transported_symbol(row: dict[str, object], point: int) -> str:
    """Return the prefix/suffix/open symbol for one target-side coordinate."""
    in_prefix = inside(
        point,
        value(row, "transported_prefix_lo"),
        value(row, "transported_prefix_hi"),
    )
    in_suffix = inside(
        point,
        value(row, "transported_suffix_lo"),
        value(row, "transported_suffix_hi"),
    )
    if in_prefix and in_suffix:
        return "B"
    if in_prefix:
        return "P"
    if in_suffix:
        return "S"
    return "O"


def count_symbol(symbols: list[str], candidates: set[str]) -> int:
    """Return the count of symbols in one candidate set."""
    return sum(1 for symbol in symbols if symbol in candidates)


def budget_row(row: dict[str, object], source: str) -> dict[str, object]:
    """Return one transported d=4 budget diagnostic row."""
    source_anchor = value(row, "source_anchor")
    source_deadline = value(row, "source_deadline_event_value")
    source_values = d4_values(source_anchor, source_deadline)
    transported_values = [value(row, "N") // item for item in source_values]
    transported_symbols = [transported_symbol(row, item) for item in transported_values]

    induced_anchor = optional_value(row, "induced_anchor")
    induced_deadline = optional_value(row, "induced_deadline_event_value")
    induced_values = (
        []
        if induced_anchor is None or induced_deadline is None
        else d4_values(induced_anchor, induced_deadline)
    )
    induced_symbols = [transported_symbol(row, item) for item in induced_values]

    source_debt = count_symbol(transported_symbols, {"P", "S", "B"})
    induced_committed = count_symbol(induced_symbols, {"P", "S", "B"})
    induced_uncommitted = count_symbol(induced_symbols, {"O"})
    carrier_value = optional_value(row, "induced_carrier_event_value")
    carrier_symbol = None if carrier_value is None else transported_symbol(row, carrier_value)
    carrier_d4 = carrier_value in induced_values if carrier_value is not None else False
    carrier_committed = carrier_symbol in {"P", "S", "B"} if carrier_symbol is not None else False
    net_budget = induced_uncommitted - source_debt
    opposite_polarity = value(row, "source_transport_reset_image") > math.isqrt(value(row, "N"))
    open_d4_carrier = carrier_d4 and carrier_symbol == "O"

    payload = {
        "case_id": row["case_id"],
        "bits": row["bits"],
        "N": row["N"],
        "rule_id": RULE_ID,
        "source_row_kind": source,
        "source_anchor": row["source_anchor"],
        "induced_anchor": row["induced_anchor"],
        "ledger_eliminated": row["ledger_eliminated"],
        "ledger_effective_survivor": row["ledger_effective_survivor"],
        "ledger_stale_transport_state": row["ledger_stale_transport_state"],
        "source_d4_count": len(source_values),
        "source_d4_values": [str(item) for item in source_values],
        "transported_source_d4_values": [str(item) for item in transported_values],
        "transported_source_d4_symbols": transported_symbols,
        "transported_d4_debt": source_debt,
        "induced_d4_count": len(induced_values),
        "induced_d4_values": [str(item) for item in induced_values],
        "induced_d4_symbols": induced_symbols,
        "induced_d4_committed_count": induced_committed,
        "induced_d4_uncommitted_count": induced_uncommitted,
        "net_frontier_budget": net_budget,
        "induced_carrier_symbol": carrier_symbol,
        "induced_carrier_is_d4": carrier_d4,
        "induced_carrier_committed": carrier_committed,
        "opposite_orientation_polarity": opposite_polarity,
        "open_d4_carrier": open_d4_carrier,
        "budget_blocks_frontier": net_budget <= 0 or (carrier_d4 and carrier_committed),
        "strict_budget_frontier_candidate": (
            opposite_polarity
            and bool(row["ledger_effective_survivor"])
            and open_d4_carrier
        ),
    }
    if "recursion_depth" in row:
        payload["recursion_depth"] = row["recursion_depth"]
        payload["ledger_recursive_cycle_state"] = row["ledger_recursive_cycle_state"]
        payload["ledger_recursive_survivor"] = row["ledger_recursive_survivor"]
    return payload


def count(rows: list[dict[str, object]], key: str) -> int:
    """Return the number of rows with a true boolean field."""
    return sum(1 for row in rows if bool(row[key]))


def partition(rows: list[dict[str, object]], keys: tuple[str, ...]) -> list[dict[str, object]]:
    """Return sorted count partitions for a small set of row fields."""
    grouped: dict[tuple[object, ...], int] = {}
    for row in rows:
        group_key = tuple(row[key] for key in keys)
        grouped[group_key] = grouped.get(group_key, 0) + 1
    return [
        {**{key: group_key[index] for index, key in enumerate(keys)}, "count": grouped[group_key]}
        for group_key in sorted(grouped, key=lambda item: tuple(str(part) for part in item))
    ]


def numeric_summary(rows: list[dict[str, object]], key: str) -> dict[str, object]:
    """Return compact min/max/counts for one integer budget field."""
    values = [int(row[key]) for row in rows]
    if not values:
        return {"min": None, "max": None, "negative": 0, "zero": 0, "positive": 0}
    return {
        "min": min(values),
        "max": max(values),
        "negative": sum(1 for item in values if item < 0),
        "zero": sum(1 for item in values if item == 0),
        "positive": sum(1 for item in values if item > 0),
    }


def summarize(
    budget_rows: list[dict[str, object]],
    recursive_budget_rows: list[dict[str, object]],
) -> dict[str, object]:
    """Return transported d=4 budget partition summaries."""
    typed_rows = [row for row in budget_rows if row["ledger_eliminated"]]
    effective_rows = [row for row in budget_rows if row["ledger_effective_survivor"]]
    stale_rows = [row for row in budget_rows if row["ledger_stale_transport_state"]]
    recursive_survivor_rows = [
        row for row in recursive_budget_rows if row.get("ledger_recursive_survivor")
    ]
    strict_frontier_rows = [
        row for row in budget_rows if row["strict_budget_frontier_candidate"]
    ]
    return {
        "rule_id": RULE_ID,
        "row_count": len(budget_rows),
        "recursive_row_count": len(recursive_budget_rows),
        "ledger_eliminated_count": count(budget_rows, "ledger_eliminated"),
        "ledger_effective_survivor_count": count(budget_rows, "ledger_effective_survivor"),
        "ledger_stale_transport_state_count": count(budget_rows, "ledger_stale_transport_state"),
        "budget_blocks_frontier_count": count(budget_rows, "budget_blocks_frontier"),
        "opposite_orientation_polarity_count": count(
            budget_rows,
            "opposite_orientation_polarity",
        ),
        "open_d4_carrier_count": count(budget_rows, "open_d4_carrier"),
        "strict_budget_frontier_candidate_count": count(
            budget_rows,
            "strict_budget_frontier_candidate",
        ),
        "typed_net_frontier_budget": numeric_summary(typed_rows, "net_frontier_budget"),
        "effective_net_frontier_budget": numeric_summary(effective_rows, "net_frontier_budget"),
        "stale_net_frontier_budget": numeric_summary(stale_rows, "net_frontier_budget"),
        "strict_budget_frontier_candidate_net_budget": numeric_summary(
            strict_frontier_rows,
            "net_frontier_budget",
        ),
        "recursive_survivor_net_frontier_budget": numeric_summary(
            recursive_survivor_rows,
            "net_frontier_budget",
        ),
        "budget_partition": partition(
            budget_rows,
            (
                "ledger_eliminated",
                "ledger_effective_survivor",
                "ledger_stale_transport_state",
                "opposite_orientation_polarity",
                "budget_blocks_frontier",
                "open_d4_carrier",
                "strict_budget_frontier_candidate",
            ),
        ),
        "case_partition": partition(
            budget_rows,
            (
                "case_id",
                "ledger_eliminated",
                "ledger_effective_survivor",
                "opposite_orientation_polarity",
                "open_d4_carrier",
                "budget_blocks_frontier",
            ),
        ),
        "recursive_partition": partition(
            recursive_budget_rows,
            (
                "recursion_depth",
                "ledger_recursive_survivor",
                "budget_blocks_frontier",
                "strict_budget_frontier_candidate",
            ),
        ),
    }


def run_probe(
    story_rows_path: Path,
    recursive_rows_path: Path,
) -> tuple[list[dict[str, object]], list[dict[str, object]], dict[str, object]]:
    """Run the transported d=4 budget probe over story-law sidecar rows."""
    rows = [budget_row(row, "direct") for row in read_jsonl(story_rows_path)]
    recursive_rows = [
        budget_row(row, "recursive")
        for row in read_jsonl(recursive_rows_path)
    ]
    return rows, recursive_rows, summarize(rows, recursive_rows)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Measure transported d=4 budget on RSA v2 story-law rows."
    )
    parser.add_argument(
        "--story-rows",
        type=Path,
        default=DEFAULT_STORY_ROWS,
        help="Input story_law_rows.jsonl from transported_story_law_probe.py.",
    )
    parser.add_argument(
        "--recursive-rows",
        type=Path,
        default=DEFAULT_RECURSIVE_ROWS,
        help="Input recursive_rows.jsonl from transported_story_law_probe.py.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help="Directory for budget_rows.jsonl, recursive_budget_rows.jsonl, and summary.json.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    """Run the sidecar budget probe."""
    args = parse_args(argv)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    rows, recursive_rows, summary = run_probe(args.story_rows, args.recursive_rows)
    write_jsonl(args.output_dir / "budget_rows.jsonl", rows)
    write_jsonl(args.output_dir / "recursive_budget_rows.jsonl", recursive_rows)
    write_json(args.output_dir / "summary.json", summary)
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
