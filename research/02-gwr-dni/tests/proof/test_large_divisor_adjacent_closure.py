"""Numeric boundary checks for the large-divisor adjacent closure proof."""

from __future__ import annotations

import math


FINITE_BASE_LEFT_PRIME = 5_000_000_000


def test_large_divisor_closure_constants_hold_at_finite_base():
    """The post-base inequalities used in the proof hold at the boundary."""
    base_log = math.log(FINITE_BASE_LEFT_PRIME)
    beta = (1.0 / math.log(2.0)) - 1.0

    assert beta * base_log - 1.0 > 32.0 / base_log
    assert math.sqrt(FINITE_BASE_LEFT_PRIME) * base_log / 8.0 > 2.0


def test_log_compression_bound_for_short_interval_ratio():
    """The proof's log-ratio bound is strict on the declared interval."""
    for denominator in (5, 8, 16, 128, 1024):
        x = 1.0 / denominator
        assert x < 0.25
        assert -math.log(1.0 - x) < x / (1.0 - x)
        assert x / (1.0 - x) < 2.0 * x
