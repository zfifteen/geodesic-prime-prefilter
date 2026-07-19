"""Exact DNI coordinate helpers."""

from __future__ import annotations

from z_band_prime_invariant import exact_zero_excess, exact_z_normalize


def E(n: int) -> float:
    """Evaluate the exact zero-excess DNI coordinate."""
    return exact_zero_excess(n)


def Z(n: int) -> float:
    """Evaluate the exact DNI normalization."""
    return exact_z_normalize(n)
