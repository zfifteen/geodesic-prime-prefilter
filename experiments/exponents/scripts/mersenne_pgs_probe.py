#!/usr/bin/env python3
"""Measure PGS chamber structure next to Mersenne prime endpoints."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

from sympy import divisor_count, factorint, nextprime


ROOT = Path(__file__).resolve().parents[3]
DEFAULT_OUTPUT_DIR = ROOT / "experiments" / "exponents" / "output" / "mersenne_pgs_probe"
DEFAULT_SCALE_LIMIT = 10**18
KNOWN_MERSENNE_PRIME_EXPONENTS_THROUGH_SCALE = (2, 3, 5, 7, 13, 17, 19, 31, 61)


def build_parser() -> argparse.ArgumentParser:
    """Build the CLI parser."""
    parser = argparse.ArgumentParser(
        description="Measure PGS chamber structure next to Mersenne prime endpoints.",
    )
    parser.add_argument("--scale-limit", type=int, default=DEFAULT_SCALE_LIMIT)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    return parser


def tau(n: int) -> int:
    """Return the exact divisor count."""
    return int(divisor_count(n))


def factor_signature(n: int) -> str:
    """Return a stable prime-power factor signature."""
    parts = []
    for prime, exponent in sorted(factorint(n).items()):
        prime = int(prime)
        exponent = int(exponent)
        if exponent == 1:
            parts.append(str(prime))
        else:
            parts.append(f"{prime}^{exponent}")
    return "*".join(parts)


def scale_ceiling(n: int) -> int:
    """Return the smallest power of ten at least n."""
    scale = 1
    while scale < n:
        scale *= 10
    return scale


def mersenne_exponents_through(limit: int) -> list[int]:
    """Return known Mersenne-prime exponents whose endpoint is within limit."""
    return [
        exponent
        for exponent in KNOWN_MERSENNE_PRIME_EXPONENTS_THROUGH_SCALE
        if 2**exponent - 1 <= limit
    ]


def chamber_row(exponent: int) -> dict[str, object]:
    """Return one Mersenne endpoint chamber row."""
    mersenne_prime = 2**exponent - 1
    right_power = mersenne_prime + 1
    second_cell = mersenne_prime + 2
    right_prime = int(nextprime(mersenne_prime))
    interior_values = list(range(mersenne_prime + 1, right_prime))
    interior_taus = [(value, tau(value)) for value in interior_values]
    min_tau = min(value_tau for _value, value_tau in interior_taus)
    leftmost_minimizer = min(value for value, value_tau in interior_taus if value_tau == min_tau)
    power_tau = tau(right_power)
    second_cell_tau = tau(second_cell)
    return {
        "exponent": exponent,
        "mersenne_prime": mersenne_prime,
        "scale_ceiling": scale_ceiling(mersenne_prime),
        "right_power": right_power,
        "right_power_signature": f"2^{exponent}",
        "right_power_tau": power_tau,
        "second_cell": second_cell,
        "second_cell_signature": factor_signature(second_cell),
        "second_cell_tau": second_cell_tau,
        "second_cell_divisible_by_3": second_cell % 3 == 0,
        "right_prime": right_prime,
        "gap_width": right_prime - mersenne_prime,
        "interior_count": len(interior_values),
        "leftmost_minimizer": leftmost_minimizer,
        "leftmost_minimizer_offset": leftmost_minimizer - mersenne_prime,
        "leftmost_minimizer_tau": min_tau,
        "right_power_selected": leftmost_minimizer == right_power,
        "second_cell_selected": leftmost_minimizer == second_cell,
        "right_power_tau_excess": power_tau - min_tau,
        "right_power_tau_over_min_tau": power_tau / min_tau,
    }


def collect_rows(scale_limit: int) -> list[dict[str, object]]:
    """Return Mersenne endpoint chamber rows through the configured limit."""
    return [chamber_row(exponent) for exponent in mersenne_exponents_through(scale_limit)]


def summarize(rows: list[dict[str, object]], scale_limit: int) -> dict[str, object]:
    """Return compact summary metrics."""
    nontrivial_rows = [row for row in rows if int(row["exponent"]) > 2]
    return {
        "scale_limit": scale_limit,
        "mersenne_prime_count": len(rows),
        "nontrivial_mersenne_prime_count": len(nontrivial_rows),
        "max_mersenne_exponent": max(int(row["exponent"]) for row in rows) if rows else 0,
        "max_mersenne_prime": max(int(row["mersenne_prime"]) for row in rows) if rows else 0,
        "right_power_selected_count": sum(bool(row["right_power_selected"]) for row in rows),
        "nontrivial_right_power_selected_count": sum(
            bool(row["right_power_selected"]) for row in nontrivial_rows
        ),
        "nontrivial_second_cell_selected_count": sum(
            bool(row["second_cell_selected"]) for row in nontrivial_rows
        ),
        "nontrivial_second_cell_selected_rate": (
            sum(bool(row["second_cell_selected"]) for row in nontrivial_rows) / len(nontrivial_rows)
            if nontrivial_rows
            else 0.0
        ),
        "nontrivial_second_cell_divisible_by_3_count": sum(
            bool(row["second_cell_divisible_by_3"]) for row in nontrivial_rows
        ),
        "nontrivial_minimizer_offset_distribution": grouped_counts(
            nontrivial_rows,
            "leftmost_minimizer_offset",
        ),
        "nontrivial_second_cell_signature_distribution": grouped_counts(
            nontrivial_rows,
            "second_cell_signature",
        ),
    }


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


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    """Write LF-terminated CSV rows."""
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main(argv: list[str] | None = None) -> int:
    """Run the Mersenne PGS probe."""
    args = build_parser().parse_args(argv)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    rows = collect_rows(args.scale_limit)
    summary = summarize(rows, args.scale_limit)
    write_csv(
        args.output_dir / "mersenne_chamber_rows.csv",
        rows,
        [
            "exponent",
            "mersenne_prime",
            "scale_ceiling",
            "right_power",
            "right_power_signature",
            "right_power_tau",
            "second_cell",
            "second_cell_signature",
            "second_cell_tau",
            "second_cell_divisible_by_3",
            "right_prime",
            "gap_width",
            "interior_count",
            "leftmost_minimizer",
            "leftmost_minimizer_offset",
            "leftmost_minimizer_tau",
            "right_power_selected",
            "second_cell_selected",
            "right_power_tau_excess",
            "right_power_tau_over_min_tau",
        ],
    )
    (args.output_dir / "summary.json").write_text(
        json.dumps(summary, indent=2) + "\n",
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
