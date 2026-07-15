#!/usr/bin/env python3
"""Pure modular residual partition for chapter 21.

PGS shape:
  carrier w + modulus vector (default M_v1)
    -> wheel W(w) from remainder zeros
    -> residual set R(n, W) for neighbor/endpoint n
    -> modular-closed | residual-open

Decision path is set emptiness only. This module does not trial-divide n by
residual primes and does not call primality to choose the residual state.

Status:
  historical z≥4⇒g=2 claim twin lock remains invalidated (see PROOF.md).
  Residual language is a design object / hypothesis frame, not a theorem.
  Dynamic modulus families beyond M_v1 are optional / hypothesis only.
"""

from __future__ import annotations

from math import isqrt
from typing import FrozenSet, Iterable, List, Sequence, Tuple

# Fixed historical z≥4⇒g=2 claim remainder moduli (PROOF.md M_v1).
M_V1: Tuple[int, ...] = (2, 3, 5, 7, 30, 210, 2310)

# Optional extended family for hypothesis exploration only (not theorem-promoted).
# Adds 11, 13 and primorial 30030 so wheels can deepen past M_v1.
M_DYNAMIC_HYPOTHESIS: Tuple[int, ...] = (
    2,
    3,
    5,
    7,
    11,
    13,
    30,
    210,
    2310,
    30030,
)

STATE_MODULAR_CLOSED = "modular-closed"
STATE_RESIDUAL_OPEN = "residual-open"


def normalize_moduli_family(moduli: Sequence[int]) -> Tuple[int, ...]:
    """Validate and freeze a modulus family (hypothesis path when not M_v1)."""
    if not moduli:
        raise ValueError("moduli family must be non-empty")
    out: list[int] = []
    for m in moduli:
        if int(m) < 2:
            raise ValueError(f"modulus must be >= 2, got {m}")
        out.append(int(m))
    return tuple(out)


def moduli_family_from_primes(primes: Sequence[int]) -> Tuple[int, ...]:
    """Build a dynamic modulus family from primes plus cumulative primorials.

    Status: hypothesis / optional tooling only. Not a proved modulus vector.

    For primes p1..pk returns
      (p1, p2, ..., pk, P1, P2, ..., Pk)
    where Pj = p1*...*pj (primorial prefixes), deduplicated in order.
    """
    cleaned: list[int] = []
    for p in primes:
        pi = int(p)
        if pi < 2:
            raise ValueError(f"prime label must be >= 2, got {p}")
        cleaned.append(pi)
    if not cleaned:
        raise ValueError("primes must be non-empty")
    family: list[int] = []
    seen: set[int] = set()
    primorial = 1
    for p in cleaned:
        if p not in seen:
            family.append(p)
            seen.add(p)
        primorial *= p
        if primorial not in seen:
            family.append(primorial)
            seen.add(primorial)
    return tuple(family)


def remainder_vector(n: int, moduli: Sequence[int] = M_V1) -> List[int]:
    """Return n mod m for each m in moduli."""
    if n < 0:
        raise ValueError("n must be non-negative")
    return [n % m for m in moduli]


def zero_count(n: int, moduli: Sequence[int] = M_V1) -> int:
    """Count remainder zeros of n on moduli."""
    return sum(1 for r in remainder_vector(n, moduli) if r == 0)


def prime_factors(m: int) -> FrozenSet[int]:
    """Prime factors of m (m >= 2). Pure factorization of a modulus label."""
    if m < 2:
        return frozenset()
    factors: set[int] = set()
    x = m
    while x % 2 == 0:
        factors.add(2)
        x //= 2
    d = 3
    while d * d <= x:
        while x % d == 0:
            factors.add(d)
            x //= d
        d += 2
    if x > 1:
        factors.add(x)
    return frozenset(factors)


def wheel_from_carrier(w: int, moduli: Sequence[int] = M_V1) -> FrozenSet[int]:
    """Build wheel W(w) from remainder zeros of carrier w on moduli.

    W(w) = union of prime factors of each m in moduli with m | w.

    Default moduli is M_v1. Passing another family is the optional dynamic-wheel
    path (hypothesis; not theorem-promoted).
    """
    if w < 0:
        raise ValueError("carrier w must be non-negative")
    family = normalize_moduli_family(moduli)
    wheel: set[int] = set()
    for m in family:
        if w % m == 0:
            wheel.update(prime_factors(m))
    return frozenset(wheel)


def primes_upto(limit: int) -> List[int]:
    """Primes in [2, limit] via sieve. Used only to describe residual sets."""
    if limit < 2:
        return []
    sieve = bytearray(b"\x01") * (limit + 1)
    sieve[0:2] = b"\x00\x00"
    for i in range(2, isqrt(limit) + 1):
        if sieve[i]:
            start = i * i
            sieve[start : limit + 1 : i] = b"\x00" * (((limit - start) // i) + 1)
    return [i for i in range(2, limit + 1) if sieve[i]]


def residual_set(n: int, wheel: Iterable[int]) -> FrozenSet[int]:
    """R(n, W) = { primes r <= floor(sqrt(n)) : r not in W }.

    Pure set construction. Does not test whether residual primes divide n.
    """
    if n <= 1:
        return frozenset()
    wheel_set = frozenset(wheel)
    bound = isqrt(n)
    return frozenset(p for p in primes_upto(bound) if p not in wheel_set)


def residual_state(n: int, wheel: Iterable[int]) -> str:
    """Classify n as modular-closed or residual-open under wheel W.

    modular-closed  <=>  n > 1 and R(n, W) is empty
    residual-open    otherwise (including n <= 1)

    No trial division of n. No primality test.
    """
    if n <= 1:
        return STATE_RESIDUAL_OPEN
    if residual_set(n, wheel):
        return STATE_RESIDUAL_OPEN
    return STATE_MODULAR_CLOSED


def classify_neighbor(
    w: int,
    offset: int = 1,
    moduli: Sequence[int] = M_V1,
) -> dict:
    """Classify neighbor n = w + offset under the wheel induced by w.

    Returns a pure record: carrier, neighbor, wheel, residual set, state, z(w).
    Non-default moduli selects the optional dynamic-wheel path (hypothesis).
    """
    if offset == 0:
        raise ValueError("offset must be nonzero")
    family = normalize_moduli_family(moduli)
    n = w + offset
    wheel = wheel_from_carrier(w, family)
    rem = remainder_vector(w, family)
    z = sum(1 for r in rem if r == 0)
    R = residual_set(n, wheel) if n > 1 else frozenset()
    state = residual_state(n, wheel)
    return {
        "carrier": w,
        "offset": offset,
        "neighbor": n,
        "moduli": family,
        "moduli_is_m_v1": family == M_V1,
        "moduli_status": (
            "m_v1_default" if family == M_V1 else "dynamic_hypothesis_optional"
        ),
        "remainder_vector": rem,
        "zero_count": z,
        "wheel": sorted(wheel),
        "residual_set": sorted(R),
        "residual_state": state,
        "modular_closed": state == STATE_MODULAR_CLOSED,
    }
