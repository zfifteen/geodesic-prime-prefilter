#!/usr/bin/env python3
"""Recover Mersenne boundary contracts across prime exponents by divisor count."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

from sympy import divisor_count, factorint, primerange


ROOT = Path(__file__).resolve().parents[3]
DEFAULT_OUTPUT_DIR = ROOT / "experiments" / "exponents" / "output" / "mersenne_boundary_contract_probe"
DEFAULT_MAX_EXPONENT = 127


def build_parser() -> argparse.ArgumentParser:
    """Build the CLI parser."""
    parser = argparse.ArgumentParser(
        description="Compare Mersenne boundary contracts across prime exponents.",
    )
    parser.add_argument("--max-exponent", type=int, default=DEFAULT_MAX_EXPONENT)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    return parser


def tau(n: int) -> int:
    """Return exact divisor count."""
    return int(divisor_count(n))


def factor_signature(n: int) -> str:
    """Return a stable factor signature."""
    if n == 1:
        return "1"
    parts = []
    for prime, exponent in sorted(factorint(n).items()):
        prime = int(prime)
        exponent = int(exponent)
        if exponent == 1:
            parts.append(str(prime))
        else:
            parts.append(f"{prime}^{exponent}")
    return "*".join(parts)


def leftmost_minimizer(left_prime: int, right_prime: int) -> tuple[int, int]:
    """Return the leftmost minimum-divisor interior integer and its divisor count."""
    interiors = range(left_prime + 1, right_prime)
    values = [(value, tau(value)) for value in interiors]
    min_tau = min(value_tau for _value, value_tau in values)
    return min(value for value, value_tau in values if value_tau == min_tau), min_tau


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
    """Recover the right boundary after a known left boundary by divisor count."""
    if tau(left_boundary) != 2:
        raise ValueError("left_boundary must have divisor count 2")
    n = left_boundary + 1
    while True:
        if tau(n) == 2:
            return n
        n += 1


def boundary_row(exponent: int) -> dict[str, object]:
    """Return one prime-exponent boundary-contract row."""
    power = 2**exponent
    candidate = power - 1
    exponent_wall = power
    second_cell = power + 1
    after_one_3 = second_cell // 3 if second_cell % 3 == 0 else second_cell
    recovered_left_boundary = pgs_left_boundary(power)
    recovered_right_boundary = pgs_right_boundary(recovered_left_boundary)
    minimizer, minimizer_tau = leftmost_minimizer(
        recovered_left_boundary,
        recovered_right_boundary,
    )
    candidate_tau = tau(candidate)
    boundary_survives = recovered_left_boundary == candidate
    return {
        "exponent": exponent,
        "candidate": candidate,
        "candidate_tau": candidate_tau,
        "candidate_factor_signature": "prime" if candidate_tau == 2 else factor_signature(candidate),
        "recovered_left_boundary": recovered_left_boundary,
        "boundary_survives": boundary_survives,
        "boundary_distance_from_power": power - recovered_left_boundary,
        "recovered_right_boundary": recovered_right_boundary,
        "recovered_gap_width": recovered_right_boundary - recovered_left_boundary,
        "exponent_wall": exponent_wall,
        "exponent_wall_tau": exponent + 1,
        "second_cell": second_cell,
        "second_cell_tau": tau(second_cell),
        "second_cell_after_one_3": after_one_3,
        "second_cell_after_one_3_signature": factor_signature(after_one_3),
        "second_cell_after_one_3_tau": tau(after_one_3),
        "second_cell_after_one_3_prime": tau(after_one_3) == 2,
        "leftmost_minimizer": minimizer,
        "leftmost_minimizer_offset_from_recovered_boundary": minimizer - recovered_left_boundary,
        "leftmost_minimizer_offset_from_candidate": minimizer - candidate,
        "leftmost_minimizer_tau": minimizer_tau,
        "second_cell_selected": minimizer == second_cell,
    }


def collect_rows(max_exponent: int) -> list[dict[str, object]]:
    """Return boundary-contract rows for prime exponents up to max_exponent."""
    return [boundary_row(exponent) for exponent in primerange(2, max_exponent + 1)]


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


def summarize(rows: list[dict[str, object]], max_exponent: int) -> dict[str, object]:
    """Return compact boundary-contract summary."""
    working = [row for row in rows if int(row["candidate_tau"]) == 2]
    nonworking = [row for row in rows if int(row["candidate_tau"]) != 2]
    boundary_survivors = [row for row in rows if bool(row["boundary_survives"])]
    false_positive_rows = [
        row for row in rows if bool(row["boundary_survives"]) and int(row["candidate_tau"]) != 2
    ]
    false_negative_rows = [
        row for row in rows if int(row["candidate_tau"]) == 2 and not bool(row["boundary_survives"])
    ]
    return {
        "max_exponent": max_exponent,
        "prime_exponent_count": len(rows),
        "mersenne_producing_exponent_count": len(working),
        "nonworking_prime_exponent_count": len(nonworking),
        "boundary_survival_count": len(boundary_survivors),
        "boundary_survival_false_positive_count": len(false_positive_rows),
        "boundary_survival_false_negative_count": len(false_negative_rows),
        "working_second_cell_selected_count": sum(bool(row["second_cell_selected"]) for row in working),
        "nonworking_second_cell_selected_count": sum(
            bool(row["second_cell_selected"]) for row in nonworking
        ),
        "working_after_one_3_prime_count": sum(
            bool(row["second_cell_after_one_3_prime"]) for row in working
        ),
        "nonworking_after_one_3_prime_count": sum(
            bool(row["second_cell_after_one_3_prime"]) for row in nonworking
        ),
        "working_boundary_distance_distribution": grouped_counts(
            working,
            "boundary_distance_from_power",
        ),
        "nonworking_boundary_distance_distribution": grouped_counts(
            nonworking,
            "boundary_distance_from_power",
        ),
        "working_minimizer_offset_from_candidate_distribution": grouped_counts(
            working,
            "leftmost_minimizer_offset_from_candidate",
        ),
        "nonworking_minimizer_offset_from_candidate_distribution": grouped_counts(
            nonworking,
            "leftmost_minimizer_offset_from_candidate",
        ),
    }


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    """Write LF-terminated CSV rows."""
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main(argv: list[str] | None = None) -> int:
    """Run the boundary-contract probe."""
    args = build_parser().parse_args(argv)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    rows = collect_rows(args.max_exponent)
    summary = summarize(rows, args.max_exponent)
    fields = [
        "exponent",
        "candidate",
        "candidate_tau",
        "candidate_factor_signature",
        "recovered_left_boundary",
        "boundary_survives",
        "boundary_distance_from_power",
        "recovered_right_boundary",
        "recovered_gap_width",
        "exponent_wall",
        "exponent_wall_tau",
        "second_cell",
        "second_cell_tau",
        "second_cell_after_one_3",
        "second_cell_after_one_3_signature",
        "second_cell_after_one_3_tau",
        "second_cell_after_one_3_prime",
        "leftmost_minimizer",
        "leftmost_minimizer_offset_from_recovered_boundary",
        "leftmost_minimizer_offset_from_candidate",
        "leftmost_minimizer_tau",
        "second_cell_selected",
    ]
    write_csv(args.output_dir / "boundary_contract_rows.csv", rows, fields)
    write_csv(
        args.output_dir / "boundary_failure_rows.csv",
        [row for row in rows if not bool(row["boundary_survives"])],
        fields,
    )
    (args.output_dir / "summary.json").write_text(
        json.dumps(summary, indent=2) + "\n",
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
