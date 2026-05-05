#!/usr/bin/env python3
"""Measure toy exponent-wall mechanics by exact divisor-count state."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

from sympy import divisor_count, factorint


ROOT = Path(__file__).resolve().parents[3]
DEFAULT_OUTPUT_DIR = ROOT / "experiments" / "exponents" / "output" / "toy_exponent_wall_mechanics_probe"
DEFAULT_MIN_EXPONENT = 2
DEFAULT_MAX_EXPONENT = 31


def build_parser() -> argparse.ArgumentParser:
    """Build the CLI parser."""
    parser = argparse.ArgumentParser(
        description="Measure toy exponent-wall mechanics by divisor-count state.",
    )
    parser.add_argument("--min-exponent", type=int, default=DEFAULT_MIN_EXPONENT)
    parser.add_argument("--max-exponent", type=int, default=DEFAULT_MAX_EXPONENT)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    return parser


def tau(n: int) -> int:
    """Return exact divisor count."""
    return int(divisor_count(n))


def factor_signature(n: int) -> str:
    """Return a stable audit factor signature."""
    parts = []
    for prime, exponent in sorted(factorint(n).items()):
        prime = int(prime)
        exponent = int(exponent)
        if exponent == 1:
            parts.append(str(prime))
        else:
            parts.append(f"{prime}^{exponent}")
    return "*".join(parts)


def pgs_left_boundary(wall: int) -> int:
    """Recover the left boundary before wall by exact divisor-count state."""
    if wall <= 2:
        raise ValueError("wall must be greater than 2")
    n = wall - 1
    while n >= 2:
        if tau(n) == 2:
            return n
        n -= 1
    raise ValueError("no left boundary found")


def pgs_right_boundary(left_boundary: int) -> int:
    """Recover the right boundary after a recovered left boundary."""
    if tau(left_boundary) != 2:
        raise ValueError("left_boundary must have divisor count 2")
    n = left_boundary + 1
    while True:
        if tau(n) == 2:
            return n
        n += 1


def leftmost_minimizer(left_boundary: int, right_boundary: int) -> tuple[int, int]:
    """Return the leftmost minimum-divisor interior integer and divisor count."""
    interiors = range(left_boundary + 1, right_boundary)
    values = [(value, tau(value)) for value in interiors]
    min_tau = min(value_tau for _value, value_tau in values)
    return min(value for value, value_tau in values if value_tau == min_tau), min_tau


def wall_row(exponent: int) -> dict[str, object]:
    """Return one toy exponent-wall mechanics row."""
    wall = 2**exponent
    candidate = wall - 1
    right_neighbor = wall + 1
    recovered_left_boundary = pgs_left_boundary(wall)
    recovered_right_boundary = pgs_right_boundary(recovered_left_boundary)
    minimizer, minimizer_tau = leftmost_minimizer(
        recovered_left_boundary,
        recovered_right_boundary,
    )
    boundary_distance = wall - recovered_left_boundary
    candidate_tau = tau(candidate)
    return {
        "exponent": exponent,
        "wall_family": "power_of_2",
        "wall": wall,
        "wall_tau": tau(wall),
        "candidate": candidate,
        "boundary_distance": boundary_distance,
        "boundary_survives": boundary_distance == 1,
        "recovered_left_boundary": recovered_left_boundary,
        "recovered_right_boundary": recovered_right_boundary,
        "recovered_chamber_width": recovered_right_boundary - recovered_left_boundary,
        "right_neighbor": right_neighbor,
        "right_neighbor_tau": tau(right_neighbor),
        "leftmost_minimizer": minimizer,
        "leftmost_minimizer_offset_from_left_boundary": minimizer - recovered_left_boundary,
        "leftmost_minimizer_offset_from_wall": minimizer - wall,
        "leftmost_minimizer_tau": minimizer_tau,
        "candidate_tau": candidate_tau,
        "candidate_audit_status": "fixed_point" if candidate_tau == 2 else "composite",
        "candidate_factor_signature": "fixed_point" if candidate_tau == 2 else factor_signature(candidate),
    }


def collect_rows(min_exponent: int, max_exponent: int) -> list[dict[str, object]]:
    """Return toy exponent-wall mechanics rows."""
    if min_exponent < 2:
        raise ValueError("min_exponent must be at least 2")
    if max_exponent < min_exponent:
        raise ValueError("max_exponent must be at least min_exponent")
    return [wall_row(exponent) for exponent in range(min_exponent, max_exponent + 1)]


def grouped_counts(rows: list[dict[str, object]], field: str) -> list[dict[str, object]]:
    """Return grouped counts for one field."""
    counts: dict[object, int] = {}
    for row in rows:
        value = row[field]
        counts[value] = counts.get(value, 0) + 1
    return [
        {field: value, "count": count}
        for value, count in sorted(counts.items(), key=lambda item: (-item[1], item[0]))
    ]


def summarize(rows: list[dict[str, object]], min_exponent: int, max_exponent: int) -> dict[str, object]:
    """Return compact toy wall summary."""
    survivors = [row for row in rows if bool(row["boundary_survives"])]
    leaks = [row for row in rows if not bool(row["boundary_survives"])]
    audit_fixed = [row for row in rows if row["candidate_audit_status"] == "fixed_point"]
    audit_composite = [row for row in rows if row["candidate_audit_status"] == "composite"]
    false_positive_rows = [
        row for row in survivors if row["candidate_audit_status"] != "fixed_point"
    ]
    false_negative_rows = [
        row for row in leaks if row["candidate_audit_status"] == "fixed_point"
    ]
    return {
        "min_exponent": min_exponent,
        "max_exponent": max_exponent,
        "wall_family": "power_of_2",
        "wall_count": len(rows),
        "boundary_survival_count": len(survivors),
        "boundary_leak_count": len(leaks),
        "audit_candidate_fixed_point_count": len(audit_fixed),
        "audit_candidate_composite_count": len(audit_composite),
        "audit_false_positive_count": len(false_positive_rows),
        "audit_false_negative_count": len(false_negative_rows),
        "boundary_distance_distribution": grouped_counts(rows, "boundary_distance"),
        "right_neighbor_tau_distribution": grouped_counts(rows, "right_neighbor_tau"),
        "minimizer_offset_from_wall_distribution": grouped_counts(
            rows,
            "leftmost_minimizer_offset_from_wall",
        ),
    }


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    """Write LF-terminated CSV rows."""
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main(argv: list[str] | None = None) -> int:
    """Run the toy exponent-wall mechanics probe."""
    args = build_parser().parse_args(argv)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    rows = collect_rows(args.min_exponent, args.max_exponent)
    fields = [
        "exponent",
        "wall_family",
        "wall",
        "wall_tau",
        "candidate",
        "boundary_distance",
        "boundary_survives",
        "recovered_left_boundary",
        "recovered_right_boundary",
        "recovered_chamber_width",
        "right_neighbor",
        "right_neighbor_tau",
        "leftmost_minimizer",
        "leftmost_minimizer_offset_from_left_boundary",
        "leftmost_minimizer_offset_from_wall",
        "leftmost_minimizer_tau",
        "candidate_tau",
        "candidate_audit_status",
        "candidate_factor_signature",
    ]
    write_csv(args.output_dir / "toy_wall_rows.csv", rows, fields)
    write_csv(
        args.output_dir / "boundary_survival_rows.csv",
        [row for row in rows if bool(row["boundary_survives"])],
        fields,
    )
    write_csv(
        args.output_dir / "boundary_leak_rows.csv",
        [row for row in rows if not bool(row["boundary_survives"])],
        fields,
    )
    (args.output_dir / "summary.json").write_text(
        json.dumps(summarize(rows, args.min_exponent, args.max_exponent), indent=2) + "\n",
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
