#!/usr/bin/env python3
"""Probe square-branch prefix divisor-count floor vs d=4 SDA transfer.

PGS objects:
  - chamber interior I = {p+1, ..., r^2 - 1} before first interior prime square
  - divisor-count field tau(n)
  - backward distance D(r) = r^2 - P(r^2)

This script is audit-only. It does not choose primes or perform PGS inference.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

import gmpy2
from sympy import prevprime

ROOT = Path(__file__).resolve().parents[2]
BENCHMARK_DIR = ROOT / "research" / "02-gwr-dni" / "scripts"
FIELD_DIR = ROOT / "src" / "python"
for path in (BENCHMARK_DIR, FIELD_DIR):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

import gwr_dni_recursive_walk as walk
from z_band_prime_composite_field import divisor_counts_segment


EXTREMAL_ROWS = [
    {"segment": "3e7-1e8", "r": 82_357_433},
    {"segment": "1e8-2e8", "r": 102_017_779},
    {"segment": "2e8-3e8", "r": 251_066_071},
]


def previous_prime_before_square(square: int) -> int:
    candidate = square - 2
    while not gmpy2.is_prime(candidate):
        candidate -= 2
    return int(candidate)


def prefix_tau_values(p: int, square: int) -> list[int]:
    counts = divisor_counts_segment(p + 1, square)
    return [int(value) for value in counts]


def max_tau_le_k_free_prefix(tau_values: list[int], k: int) -> int:
    """Least offset r>=1 where some prefix integer has tau <= k."""
    for offset, value in enumerate(tau_values, start=1):
        if value <= k:
            return offset
    return len(tau_values) + 1


def prefix_tau_summary(tau_values: list[int]) -> dict[str, object]:
    if not tau_values:
        return {
            "prefix_length": 0,
            "prefix_min_tau": None,
            "prefix_max_tau": None,
            "tau4_count": 0,
            "tau5_count": 0,
        }
    return {
        "prefix_length": len(tau_values),
        "prefix_min_tau": min(tau_values),
        "prefix_max_tau": max(tau_values),
        "tau4_count": sum(1 for value in tau_values if value == 4),
        "tau5_count": sum(1 for value in tau_values if value == 5),
    }


def sda_forces_tau_le_k_by_offset(p: int, k: int, max_offset: int) -> int | None:
    """Return first offset where tau<=k is forced by the SDA inequality, or None."""
    for h in range(1, max_offset + 1):
        n = p + h
        lhs = (k + 1) * h
        rhs = h * (math.log(n) + 2.0) + 2.0 * math.sqrt(n)
        if lhs > rhs:
            return h
    return None


def analyze_row(r: int) -> dict[str, object]:
    square = r * r
    p = previous_prime_before_square(square)
    s = int(prevprime(r))
    offset = square - p
    cutoff = walk.dynamic_cutoff(p)
    utilization = offset / cutoff
    selected_square = s * s < p < square
    tau_values = prefix_tau_values(p, square)
    prefix = prefix_tau_summary(tau_values)
    r_sda5 = max_tau_le_k_free_prefix(tau_values, 4)
    r_sda4 = max_tau_le_k_free_prefix(tau_values, 3)
    forced_tau4 = sda_forces_tau_le_k_by_offset(p, 4, offset)
    forced_tau3 = sda_forces_tau_le_k_by_offset(p, 3, offset)
    band_bound = (r - s) * (r + s)
    return {
        "r": r,
        "p": p,
        "s": s,
        "square": square,
        "offset": offset,
        "dynamic_cutoff": cutoff,
        "utilization": utilization,
        "selected_square_branch": selected_square,
        "band_bound_r2_minus_s2": band_bound,
        "prefix": prefix,
        "first_tau4_offset": r_sda5,
        "first_tau3_offset": r_sda4,
        "sda_forces_tau_le_4_by_offset": forced_tau4,
        "sda_forces_tau_le_3_by_offset": forced_tau3,
        "d4_sda_transfers": prefix["prefix_min_tau"] is not None and prefix["prefix_min_tau"] >= 5,
        "tau4_sda_binds_at_observed_offset": (
            forced_tau4 is not None and forced_tau4 <= offset
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Square-branch prefix tau-floor probe.")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(__file__).resolve().parent / "prefix_tau_floor_probe.json",
    )
    args = parser.parse_args()

    results = [analyze_row(row["r"]) | {"segment": row["segment"]} for row in EXTREMAL_ROWS]
    payload = {
        "extremal_rows": results,
        "conclusion": {
            "d4_tau5_sda_route_transfers_to_square_branch": all(
                row["d4_sda_transfers"] for row in results
            ),
            "tau4_sda_binds_observed_offsets": all(
                row["tau4_sda_binds_at_observed_offset"] for row in results
            ),
        },
    }
    args.output.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload["conclusion"], indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())