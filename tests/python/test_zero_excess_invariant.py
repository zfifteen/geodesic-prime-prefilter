"""Tests for the exact zero-excess DNI coordinate."""

from __future__ import annotations

import math
import sys
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[2]
SOURCE_DIR = ROOT / "src" / "python"

if str(SOURCE_DIR) not in sys.path:
    sys.path.insert(0, str(SOURCE_DIR))

from z_band_prime_invariant import (
    exact_divisor_count,
    exact_z_normalize,
    exact_zero_excess,
)


def test_zero_excess_formula_matches_divisor_count():
    """E(n) is the divisor-count excess measured on the log scale."""
    for n in range(1, 40):
        expected = 0.0
        if n > 1:
            expected = (exact_divisor_count(n) / 2.0 - 1.0) * math.log(n)

        assert exact_zero_excess(n) == pytest.approx(expected)


def test_zero_excess_prime_and_composite_behavior_with_one_guard():
    """For n > 1, primes have zero excess and composites have positive excess."""
    assert exact_zero_excess(1) == 0.0

    for prime in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        assert exact_zero_excess(prime) == pytest.approx(0.0)

    for composite in (4, 6, 8, 9, 10, 12, 16, 18, 21, 25, 27, 36):
        assert exact_zero_excess(composite) > 0.0


def test_zero_excess_is_negative_log_z_when_z_positive():
    """The new coordinate is the negative logarithm of the legacy Z score."""
    for n in range(2, 60):
        z_score = exact_z_normalize(n)

        assert z_score > 0.0
        assert exact_zero_excess(n) == pytest.approx(-math.log(z_score))


def test_local_f_score_is_negative_zero_excess():
    """The local maximizer score F is the sign dual of zero excess."""
    for n in range(2, 60):
        f_score = (1.0 - exact_divisor_count(n) / 2.0) * math.log(n)

        assert f_score == pytest.approx(-exact_zero_excess(n))


def test_zero_excess_rejects_nonpositive_inputs():
    """The semantic zero-excess helper has an explicit positive-integer domain."""
    with pytest.raises(ValueError):
        exact_zero_excess(0)
