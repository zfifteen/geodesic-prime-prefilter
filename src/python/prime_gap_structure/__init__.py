"""Core primitives for prime gap structure."""

from __future__ import annotations

from z_band_prime_invariant import exact_divisor_count as tau
from z_band_prime_predictor import next_prime_after as gap_walk
from . import dni

__all__ = [
    "tau",
    "gap_walk",
    "dni",
]
