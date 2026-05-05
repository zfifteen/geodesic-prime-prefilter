#!/usr/bin/env python3
"""PGS-only pressure pass for unresolved exponent-wall rows."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import exponent_decade_ladder_pgs_mechanism as ladder


ROOT = Path(__file__).resolve().parents[3]
DEFAULT_INPUT = (
    ROOT
    / "experiments"
    / "exponents"
    / "output"
    / "exponent_decade_ladder_probe"
    / "pgs_unresolved_rows.csv"
)
DEFAULT_OUTPUT_DIR = (
    ROOT
    / "experiments"
    / "exponents"
    / "output"
    / "exponent_unresolved_pressure_probe"
)
DEFAULT_CANDIDATE_SECONDS_LIMIT = 3.0


PRESSURE_FIELDNAMES = [
    "source_rung_min_exponent",
    "source_rung_max_exponent",
    "exponent",
    "exponent_divisor_count",
    "source_candidate_bound",
    "source_candidate_seconds_limit",
    "source_candidate_checks",
    "source_unresolved_candidate_offset",
    "pressure_candidate_bound",
    "pressure_candidate_seconds_limit",
    "pressure_exponent_status",
    "pressure_candidate_checks",
    "pressure_unresolved_reason",
    "pressure_unresolved_candidate_offset",
    "power_of_two",
    "mersenne_number",
    "distance_to_left_prime",
    "mersenne_location_inferred",
    "left_prime",
]


def build_parser() -> argparse.ArgumentParser:
    """Build the CLI parser."""
    parser = argparse.ArgumentParser(
        description="Pressure unresolved exponent-wall rows with the same PGS rule.",
    )
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--candidate-bound", type=int, default=ladder.DEFAULT_CANDIDATE_BOUND)
    parser.add_argument(
        "--candidate-seconds-limit",
        type=float,
        default=DEFAULT_CANDIDATE_SECONDS_LIMIT,
    )
    return parser


def read_csv(path: Path) -> list[dict[str, str]]:
    """Read CSV rows."""
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def normalize_source_row(row: dict[str, str]) -> dict[str, str]:
    """Return a ladder-unresolved shaped source row."""
    if "rung_min_exponent" in row:
        return row
    return {
        "rung_min_exponent": row["source_rung_min_exponent"],
        "rung_max_exponent": row["source_rung_max_exponent"],
        "exponent": row["exponent"],
        "exponent_divisor_count": row["exponent_divisor_count"],
        "candidate_bound": row["pressure_candidate_bound"],
        "candidate_seconds_limit": row["pressure_candidate_seconds_limit"],
        "candidate_checks": row["pressure_candidate_checks"],
        "unresolved_candidate_offset": row["pressure_unresolved_candidate_offset"],
    }


def pressure_row(
    source: dict[str, str],
    candidate_bound: int,
    candidate_seconds_limit: float,
) -> dict[str, object]:
    """Return one pressure row for a previously unresolved exponent."""
    source = normalize_source_row(source)
    exponent = int(source["exponent"])
    pressure = ladder.pgs_row(
        rung_max_exponent=int(source["rung_max_exponent"]),
        exponent=exponent,
        candidate_bound=candidate_bound,
        candidate_seconds_limit=candidate_seconds_limit,
        rung_min_exponent=int(source["rung_min_exponent"]),
    )
    return {
        "source_rung_min_exponent": source["rung_min_exponent"],
        "source_rung_max_exponent": source["rung_max_exponent"],
        "exponent": exponent,
        "exponent_divisor_count": source["exponent_divisor_count"],
        "source_candidate_bound": source["candidate_bound"],
        "source_candidate_seconds_limit": source["candidate_seconds_limit"],
        "source_candidate_checks": source["candidate_checks"],
        "source_unresolved_candidate_offset": source["unresolved_candidate_offset"],
        "pressure_candidate_bound": candidate_bound,
        "pressure_candidate_seconds_limit": candidate_seconds_limit,
        "pressure_exponent_status": pressure["exponent_status"],
        "pressure_candidate_checks": pressure["candidate_checks"],
        "pressure_unresolved_reason": pressure["unresolved_reason"],
        "pressure_unresolved_candidate_offset": pressure["unresolved_candidate_offset"],
        "power_of_two": pressure["power_of_two"],
        "mersenne_number": pressure["mersenne_number"],
        "distance_to_left_prime": pressure["distance_to_left_prime"],
        "mersenne_location_inferred": pressure["mersenne_location_inferred"],
        "left_prime": pressure["left_prime"],
    }


def collect_rows(
    source_rows: list[dict[str, str]],
    candidate_bound: int,
    candidate_seconds_limit: float,
) -> list[dict[str, object]]:
    """Return pressure rows."""
    return [
        pressure_row(source, candidate_bound, candidate_seconds_limit)
        for source in source_rows
    ]


def summarize(
    rows: list[dict[str, object]],
    source_count: int,
    candidate_bound: int,
    candidate_seconds_limit: float,
) -> dict[str, object]:
    """Return compact pressure summary."""
    resolved = [
        row
        for row in rows
        if row["pressure_exponent_status"] == ladder.STATUS_LEFT_PRIME_RESOLVED
    ]
    still_unresolved = [
        row
        for row in rows
        if row["pressure_exponent_status"] == ladder.STATUS_LEFT_PRIME_UNRESOLVED
    ]
    inferred = [row for row in rows if bool(row["mersenne_location_inferred"])]
    return {
        "source_unresolved_count": source_count,
        "pressure_candidate_bound": candidate_bound,
        "pressure_candidate_seconds_limit": candidate_seconds_limit,
        "pressure_row_count": len(rows),
        "resolved_after_pressure_count": len(resolved),
        "still_unresolved_count": len(still_unresolved),
        "inferred_after_pressure_count": len(inferred),
    }


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    """Write LF-terminated pressure CSV."""
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=PRESSURE_FIELDNAMES, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_outputs(
    output_dir: Path,
    rows: list[dict[str, object]],
    source_count: int,
    candidate_bound: int,
    candidate_seconds_limit: float,
) -> None:
    """Write pressure outputs."""
    output_dir.mkdir(parents=True, exist_ok=True)
    resolved = [
        row
        for row in rows
        if row["pressure_exponent_status"] == ladder.STATUS_LEFT_PRIME_RESOLVED
    ]
    still_unresolved = [
        row
        for row in rows
        if row["pressure_exponent_status"] == ladder.STATUS_LEFT_PRIME_UNRESOLVED
    ]
    inferred = [row for row in rows if bool(row["mersenne_location_inferred"])]
    write_csv(output_dir / "resolved_after_pressure_rows.csv", resolved)
    write_csv(output_dir / "still_unresolved_rows.csv", still_unresolved)
    write_csv(output_dir / "inferred_after_pressure_rows.csv", inferred)
    (output_dir / "pressure_summary.json").write_text(
        json.dumps(
            summarize(rows, source_count, candidate_bound, candidate_seconds_limit),
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )


def main(argv: list[str] | None = None) -> int:
    """Run the unresolved-row pressure pass."""
    args = build_parser().parse_args(argv)
    source_rows = read_csv(args.input)
    rows = collect_rows(source_rows, args.candidate_bound, args.candidate_seconds_limit)
    write_outputs(
        args.output_dir,
        rows,
        len(source_rows),
        args.candidate_bound,
        args.candidate_seconds_limit,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
