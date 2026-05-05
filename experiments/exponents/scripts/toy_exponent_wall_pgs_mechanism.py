#!/usr/bin/env python3
"""PGS-only mechanism for toy exponent-wall left-prime recovery."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

from sympy import divisor_count


ROOT = Path(__file__).resolve().parents[3]
DEFAULT_OUTPUT_DIR = ROOT / "experiments" / "exponents" / "output" / "toy_exponent_wall_mechanics_probe"
DEFAULT_MIN_EXPONENT = 2
DEFAULT_MAX_EXPONENT = 31
DEFAULT_CANDIDATE_BOUND = 128
PGS_LEFT_PRIME_RULE_ID = "pgs_left_prime_wheel_open_v1"
LOW_PRIMES = frozenset({2, 3, 5})
WHEEL_OPEN_RESIDUES_MOD30 = frozenset({1, 7, 11, 13, 17, 19, 23, 29})


class PGSLeftPrimeUnresolvedError(RuntimeError):
    """Raised when the PGS left-prime rule does not resolve inside the bound."""


PGS_FIELDNAMES = [
    "exponent",
    "left_prime_rule_id",
    "candidate_bound",
    "candidate_checks",
    "rejected_candidate_offsets_before_left_prime",
    "number_family",
    "power_of_two",
    "power_of_two_divisor_count",
    "mersenne_number",
    "distance_to_left_prime",
    "mersenne_location_inferred",
    "left_prime",
    "right_prime",
    "prime_gap_length",
    "right_neighbor",
    "right_neighbor_divisor_count",
    "least_divisor_count_integer",
    "least_divisor_count_integer_offset_from_left_prime",
    "least_divisor_count_integer_offset_from_power_of_two",
    "least_divisor_count",
]


def build_parser() -> argparse.ArgumentParser:
    """Build the CLI parser."""
    parser = argparse.ArgumentParser(
        description="Run the PGS-only toy exponent-wall mechanism.",
    )
    parser.add_argument("--min-exponent", type=int, default=DEFAULT_MIN_EXPONENT)
    parser.add_argument("--max-exponent", type=int, default=DEFAULT_MAX_EXPONENT)
    parser.add_argument("--candidate-bound", type=int, default=DEFAULT_CANDIDATE_BOUND)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    return parser


def tau(n: int) -> int:
    """Return exact divisor count."""
    return int(divisor_count(n))


def left_prime_candidate_offsets(power_of_two: int, candidate_bound: int) -> list[int]:
    """Return admissible offsets for a left-prime search below a power of two."""
    if candidate_bound < 1:
        raise ValueError("candidate_bound must be positive")
    return [
        offset
        for offset in range(1, candidate_bound + 1)
        if power_of_two - offset in LOW_PRIMES
        or (
            power_of_two - offset > 5
            and (power_of_two - offset) % 30 in WHEEL_OPEN_RESIDUES_MOD30
        )
    ]


def recover_left_prime_record(
    power_of_two: int,
    candidate_bound: int = DEFAULT_CANDIDATE_BOUND,
) -> dict[str, object]:
    """Recover the nearest left prime from bounded PGS candidate state."""
    if power_of_two <= 2:
        raise ValueError("power_of_two must be greater than 2")
    rejected_offsets: list[int] = []
    for offset in left_prime_candidate_offsets(power_of_two, candidate_bound):
        candidate = power_of_two - offset
        if tau(candidate) == 2:
            return {
                "left_prime_rule_id": PGS_LEFT_PRIME_RULE_ID,
                "candidate_bound": candidate_bound,
                "left_prime": candidate,
                "distance_to_left_prime": offset,
                "candidate_checks": len(rejected_offsets) + 1,
                "rejected_candidate_offsets_before_left_prime": ";".join(
                    str(value) for value in rejected_offsets
                ),
            }
        rejected_offsets.append(offset)
    raise PGSLeftPrimeUnresolvedError(
        f"PGS left-prime rule did not resolve n={power_of_two} within bound={candidate_bound}"
    )


def recover_left_prime(
    power_of_two: int,
    candidate_bound: int = DEFAULT_CANDIDATE_BOUND,
) -> int:
    """Recover the nearest left prime by bounded PGS candidate state."""
    return int(recover_left_prime_record(power_of_two, candidate_bound)["left_prime"])


def recover_right_prime(left_prime: int) -> int:
    """Recover the right prime after a recovered left prime."""
    if tau(left_prime) != 2:
        raise ValueError("left_prime must have divisor count 2")
    n = left_prime + 1
    while True:
        if tau(n) == 2:
            return n
        n += 1


def least_divisor_count_integer(left_prime: int, right_prime: int) -> tuple[int, int]:
    """Return the leftmost integer with minimum divisor count between two primes."""
    interiors = range(left_prime + 1, right_prime)
    values = [(value, tau(value)) for value in interiors]
    min_tau = min(value_tau for _value, value_tau in values)
    return min(value for value, value_tau in values if value_tau == min_tau), min_tau


def pgs_row(exponent: int, candidate_bound: int = DEFAULT_CANDIDATE_BOUND) -> dict[str, object]:
    """Return one PGS-only toy exponent-wall row."""
    power_of_two = 2**exponent
    mersenne_number = power_of_two - 1
    right_neighbor = power_of_two + 1
    left_record = recover_left_prime_record(power_of_two, candidate_bound)
    left_prime = int(left_record["left_prime"])
    right_prime = recover_right_prime(left_prime)
    least_integer, least_count = least_divisor_count_integer(left_prime, right_prime)
    distance = int(left_record["distance_to_left_prime"])
    return {
        "exponent": exponent,
        "left_prime_rule_id": PGS_LEFT_PRIME_RULE_ID,
        "candidate_bound": candidate_bound,
        "candidate_checks": left_record["candidate_checks"],
        "rejected_candidate_offsets_before_left_prime": left_record[
            "rejected_candidate_offsets_before_left_prime"
        ],
        "number_family": "power_of_two",
        "power_of_two": power_of_two,
        "power_of_two_divisor_count": tau(power_of_two),
        "mersenne_number": mersenne_number,
        "distance_to_left_prime": distance,
        "mersenne_location_inferred": distance == 1,
        "left_prime": left_prime,
        "right_prime": right_prime,
        "prime_gap_length": right_prime - left_prime,
        "right_neighbor": right_neighbor,
        "right_neighbor_divisor_count": tau(right_neighbor),
        "least_divisor_count_integer": least_integer,
        "least_divisor_count_integer_offset_from_left_prime": least_integer - left_prime,
        "least_divisor_count_integer_offset_from_power_of_two": least_integer - power_of_two,
        "least_divisor_count": least_count,
    }


def collect_rows(
    min_exponent: int,
    max_exponent: int,
    candidate_bound: int = DEFAULT_CANDIDATE_BOUND,
) -> list[dict[str, object]]:
    """Return PGS-only toy exponent-wall rows."""
    if min_exponent < 2:
        raise ValueError("min_exponent must be at least 2")
    if max_exponent < min_exponent:
        raise ValueError("max_exponent must be at least min_exponent")
    return [
        pgs_row(exponent, candidate_bound)
        for exponent in range(min_exponent, max_exponent + 1)
    ]


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


def summarize(
    rows: list[dict[str, object]],
    min_exponent: int,
    max_exponent: int,
    candidate_bound: int,
) -> dict[str, object]:
    """Return compact PGS mechanism summary."""
    inferred = [row for row in rows if bool(row["mersenne_location_inferred"])]
    not_inferred = [row for row in rows if not bool(row["mersenne_location_inferred"])]
    return {
        "min_exponent": min_exponent,
        "max_exponent": max_exponent,
        "candidate_bound": candidate_bound,
        "left_prime_rule_id": PGS_LEFT_PRIME_RULE_ID,
        "number_family": "power_of_two",
        "row_count": len(rows),
        "mersenne_location_inferred_count": len(inferred),
        "mersenne_location_not_inferred_count": len(not_inferred),
        "distance_to_left_prime_distribution": grouped_counts(rows, "distance_to_left_prime"),
        "candidate_checks_distribution": grouped_counts(rows, "candidate_checks"),
        "right_neighbor_divisor_count_distribution": grouped_counts(
            rows,
            "right_neighbor_divisor_count",
        ),
        "least_divisor_count_integer_offset_from_power_of_two_distribution": grouped_counts(
            rows,
            "least_divisor_count_integer_offset_from_power_of_two",
        ),
    }


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    """Write LF-terminated CSV rows."""
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_outputs(output_dir: Path, rows: list[dict[str, object]]) -> None:
    """Write PGS mechanism outputs."""
    output_dir.mkdir(parents=True, exist_ok=True)
    write_csv(output_dir / "pgs_power_of_two_rows.csv", rows, PGS_FIELDNAMES)
    write_csv(
        output_dir / "mersenne_location_inferred_rows.csv",
        [row for row in rows if bool(row["mersenne_location_inferred"])],
        PGS_FIELDNAMES,
    )
    write_csv(
        output_dir / "mersenne_location_not_inferred_rows.csv",
        [row for row in rows if not bool(row["mersenne_location_inferred"])],
        PGS_FIELDNAMES,
    )


def main(argv: list[str] | None = None) -> int:
    """Run the PGS-only toy exponent-wall mechanism."""
    args = build_parser().parse_args(argv)
    rows = collect_rows(args.min_exponent, args.max_exponent, args.candidate_bound)
    write_outputs(args.output_dir, rows)
    (args.output_dir / "pgs_summary.json").write_text(
        json.dumps(
            summarize(rows, args.min_exponent, args.max_exponent, args.candidate_bound),
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
