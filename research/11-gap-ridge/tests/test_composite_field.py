"""Tests for the exact composite-field interval engine."""

from __future__ import annotations

import math
import sys
from pathlib import Path

import sympy


ROOT = Path(__file__).resolve().parents[3]
SOURCE_DIR = ROOT / "src" / "python"

if str(SOURCE_DIR) not in sys.path:
    sys.path.insert(0, str(SOURCE_DIR))

from z_band_prime_composite_field import (
    INT64_FIELD_MAX,
    divisor_counts_segment,
    divisor_counts_segment_gmp_bounded,
)


def naive_divisor_count(n: int) -> int:
    """Compute the exact divisor count with direct integer enumeration."""
    count = 0
    root = math.isqrt(n)
    for divisor in range(1, root + 1):
        if n % divisor != 0:
            continue
        count += 1 if divisor * divisor == n else 2
    return count


def test_divisor_counts_segment_matches_naive_small_interval():
    """The exact interval engine should match direct counting on a small range."""
    lo = 1
    hi = 64

    observed = divisor_counts_segment(lo, hi)
    expected = [naive_divisor_count(n) for n in range(lo, hi)]

    assert observed.tolist() == expected


def test_divisor_counts_segment_matches_oracle_near_10e18():
    """The exact interval engine should stay correct on a real interval near 10^18."""
    lo = 10**18 - 32
    hi = lo + 16

    observed = divisor_counts_segment(lo, hi)
    expected = [sympy.divisor_count(n) for n in range(lo, hi)]

    assert observed.tolist() == expected


def test_gmp_bounded_backend_matches_small_exact_counts():
    """The bounded GMP-safe backend should close small intervals exactly."""
    lo = 90
    hi = 100

    observed = divisor_counts_segment_gmp_bounded(lo, hi, trial_prime_limit=32)
    expected = [naive_divisor_count(n) for n in range(lo, hi)]

    assert [row.exact_count for row in observed] == expected
    assert all(row.is_exact for row in observed)


def test_gmp_bounded_backend_handles_large_coordinates_without_int64_overflow():
    """The bounded backend should return explicit statuses above int64 range."""
    power = 1 << 80
    lo = power
    hi = lo + 2

    observed = divisor_counts_segment_gmp_bounded(lo, hi, trial_prime_limit=16)

    assert lo > INT64_FIELD_MAX
    assert observed[0].value == power
    assert observed[0].exact_count == 81
    assert observed[0].status == "exact_fully_stripped"
    assert observed[1].value == power + 1
    assert observed[1].exact_count is None
    assert observed[1].status in {
        "bounded_higher_divisor_lower_bound",
        "unresolved_large_residual",
    }


def test_gmp_bounded_backend_reports_proven_higher_divisor_lower_bound():
    """The bounded backend should expose known higher-divisor evidence."""
    value = 3 * 5 * 7 * ((1 << 80) + 13)

    observed = divisor_counts_segment_gmp_bounded(value, value + 1, trial_prime_limit=7)

    assert observed[0].exact_count is None
    assert observed[0].lower_bound_count == 8
    assert observed[0].is_known_higher_divisor
    assert observed[0].status == "bounded_higher_divisor_lower_bound"
