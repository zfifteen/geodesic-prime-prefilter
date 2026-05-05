#!/usr/bin/env python3
"""Diagnostic summaries for unresolved exponent pressure rows."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
DEFAULT_INPUT = (
    ROOT
    / "experiments"
    / "exponents"
    / "output"
    / "exponent_unresolved_pressure_probe"
    / "pass_10s"
    / "still_unresolved_rows.csv"
)
DEFAULT_OUTPUT_DIR = (
    ROOT
    / "experiments"
    / "exponents"
    / "output"
    / "exponent_unresolved_pressure_probe"
    / "diagnostic"
)


OFFSET_FIELDNAMES = [
    "pressure_unresolved_candidate_offset",
    "count",
]

CHECK_FIELDNAMES = [
    "pressure_candidate_checks",
    "count",
]


def build_parser() -> argparse.ArgumentParser:
    """Build the CLI parser."""
    parser = argparse.ArgumentParser(description="Summarize unresolved exponent pressure rows.")
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    return parser


def read_csv(path: Path) -> list[dict[str, str]]:
    """Read CSV rows."""
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def grouped_counts(rows: list[dict[str, str]], field: str) -> list[dict[str, object]]:
    """Return grouped counts for one field."""
    counts: dict[str, int] = {}
    for row in rows:
        value = row[field]
        counts[value] = counts.get(value, 0) + 1
    return [
        {field: value, "count": count}
        for value, count in sorted(
            counts.items(),
            key=lambda item: (-item[1], int(item[0]) if item[0] else -1),
        )
    ]


def summarize(rows: list[dict[str, str]]) -> dict[str, object]:
    """Return compact unresolved-surface summary."""
    row_count = len(rows)
    offset_one_count = sum(row["pressure_unresolved_candidate_offset"] == "1" for row in rows)
    first_offset_counts = grouped_counts(rows, "pressure_unresolved_candidate_offset")
    return {
        "row_count": row_count,
        "offset_one_count": offset_one_count,
        "offset_one_share": offset_one_count / row_count if row_count else 0.0,
        "min_exponent": min(int(row["exponent"]) for row in rows) if rows else None,
        "max_exponent": max(int(row["exponent"]) for row in rows) if rows else None,
        "most_common_unresolved_offset": first_offset_counts[0] if first_offset_counts else None,
        "offset_one_stop_rule_triggered": (
            offset_one_count / row_count >= 0.4 if row_count else False
        ),
    }


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    """Write LF-terminated CSV rows."""
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_outputs(output_dir: Path, rows: list[dict[str, str]]) -> None:
    """Write diagnostic outputs."""
    output_dir.mkdir(parents=True, exist_ok=True)
    write_csv(
        output_dir / "unresolved_offset_summary_rows.csv",
        grouped_counts(rows, "pressure_unresolved_candidate_offset"),
        OFFSET_FIELDNAMES,
    )
    write_csv(
        output_dir / "unresolved_candidate_checks_rows.csv",
        grouped_counts(rows, "pressure_candidate_checks"),
        CHECK_FIELDNAMES,
    )
    (output_dir / "diagnostic_summary.json").write_text(
        json.dumps(summarize(rows), indent=2) + "\n",
        encoding="utf-8",
    )


def main(argv: list[str] | None = None) -> int:
    """Run the diagnostic."""
    args = build_parser().parse_args(argv)
    write_outputs(args.output_dir, read_csv(args.input))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
