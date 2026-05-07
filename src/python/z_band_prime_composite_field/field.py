"""Exact composite-field helpers used by prime-gap studies."""

from __future__ import annotations

import math
from dataclasses import dataclass

import gmpy2
import numpy as np


SEGMENT_SIZE = 1_000_000
INT64_FIELD_MAX = int(np.iinfo(np.int64).max)


@dataclass(frozen=True)
class BoundedDivisorCount:
    """One large-coordinate divisor-count measurement with explicit status."""

    value: int
    exact_count: int | None
    lower_bound_count: int
    residual: int
    trial_prime_limit: int
    status: str

    @property
    def is_exact(self) -> bool:
        """Return True when the exact divisor count is known."""
        return self.exact_count is not None

    @property
    def is_known_higher_divisor(self) -> bool:
        """Return True when the value is known to have divisor count above 4."""
        count = self.exact_count if self.exact_count is not None else self.lower_bound_count
        return count > 4

    @property
    def count_or_lower_bound(self) -> int:
        """Return the exact count when known, otherwise the proven lower bound."""
        if self.exact_count is not None:
            return self.exact_count
        return self.lower_bound_count


def _integer_cube_root(value: int) -> tuple[int, bool]:
    """Return floor cube root and exactness for one non-negative integer."""
    root = int(round(value ** (1.0 / 3.0)))
    while (root + 1) ** 3 <= value:
        root += 1
    while root**3 > value:
        root -= 1
    return root, root**3 == value


def _strong_composite_witness(n: int, base: int, odd_part: int, shifts: int) -> bool:
    """Return True when one Miller-Rabin base proves compositeness."""
    value = pow(base, odd_part, n)
    if value == 1 or value == n - 1:
        return False
    for _ in range(shifts - 1):
        value = (value * value) % n
        if value == n - 1:
            return False
    return True


def _has_no_composite_witness(n: int) -> bool:
    """Return True when deterministic bases find no composite witness."""
    if n < 2:
        return False
    small_basis = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37)
    for base in small_basis:
        if n == base:
            return True
        if n % base == 0:
            return False

    odd_part = n - 1
    shifts = 0
    while odd_part % 2 == 0:
        odd_part //= 2
        shifts += 1

    for base in small_basis:
        if _strong_composite_witness(n, base, odd_part, shifts):
            return False
    return True


def _small_primes(limit: int) -> np.ndarray:
    """Return every prime up to one small sieve limit."""
    sieve = np.ones(limit + 1, dtype=bool)
    sieve[:2] = False
    root = int(limit ** 0.5)
    for prime in range(2, root + 1):
        if sieve[prime]:
            sieve[prime * prime : limit + 1 : prime] = False
    return np.flatnonzero(sieve)


def _segmented_primes(limit: int, segment_size: int = SEGMENT_SIZE):
    """Yield primes up to one limit without materializing the full sieve."""
    if limit < 2:
        return

    base_limit = int(math.isqrt(limit))
    base_primes = _small_primes(base_limit)

    for segment_lo in range(2, limit + 1, segment_size):
        segment_hi = min(segment_lo + segment_size - 1, limit)
        sieve = np.ones(segment_hi - segment_lo + 1, dtype=bool)
        for prime in base_primes:
            prime_int = int(prime)
            prime_square = prime_int * prime_int
            if prime_square > segment_hi:
                break
            start = max(prime_square, ((segment_lo + prime_int - 1) // prime_int) * prime_int)
            sieve[start - segment_lo : segment_hi - segment_lo + 1 : prime_int] = False

        for offset in np.flatnonzero(sieve):
            yield segment_lo + int(offset)


def divisor_counts_segment(lo: int, hi: int) -> np.ndarray:
    """Compute exact divisor counts on one contiguous natural-number interval."""
    if lo < 1:
        raise ValueError("lo must be at least 1")
    if hi <= lo:
        raise ValueError("hi must be larger than lo")

    size = hi - lo
    values = np.arange(lo, hi, dtype=np.int64)
    residual = values.copy()
    divisor_count = np.ones(size, dtype=np.uint32)
    cube_root_limit, exact = _integer_cube_root(hi - 1)
    if not exact and (cube_root_limit + 1) ** 3 <= hi - 1:
        cube_root_limit += 1

    for prime in _segmented_primes(cube_root_limit):
        start = ((lo + prime - 1) // prime) * prime
        indices = np.arange(start - lo, size, prime, dtype=np.int64)
        if indices.size == 0:
            continue

        subvalues = residual[indices].copy()
        exponent = np.zeros(indices.size, dtype=np.uint8)
        while True:
            mask = (subvalues % prime) == 0
            if not mask.any():
                break
            subvalues[mask] //= prime
            exponent[mask] += 1

        residual[indices] = subvalues
        nonzero = exponent != 0
        if nonzero.any():
            divisor_count[indices[nonzero]] *= (exponent[nonzero] + 1).astype(np.uint32)

    for index, remainder in enumerate(residual):
        if remainder == 1:
            continue

        remainder_int = int(remainder)
        if _has_no_composite_witness(remainder_int):
            divisor_count[index] *= 2
            continue

        root = math.isqrt(remainder_int)
        if root * root == remainder_int and _has_no_composite_witness(root):
            divisor_count[index] *= 3
            continue

        divisor_count[index] *= 4

    if lo <= 1 < hi:
        divisor_count[1 - lo] = 1
    return divisor_count


def _bounded_divisor_count_with_primes(
    value: int,
    primes: list[int],
    trial_prime_limit: int,
) -> BoundedDivisorCount:
    """Return one GMP-safe bounded divisor-count measurement."""
    if value < 1:
        raise ValueError("value must be at least 1")
    if trial_prime_limit < 2:
        raise ValueError("trial_prime_limit must be at least 2")
    if value == 1:
        return BoundedDivisorCount(
            value=1,
            exact_count=1,
            lower_bound_count=1,
            residual=1,
            trial_prime_limit=trial_prime_limit,
            status="exact_unit",
        )

    residual = gmpy2.mpz(value)
    lower_bound_count = 1
    largest_trial_prime = 1
    for prime in primes:
        largest_trial_prime = prime
        if gmpy2.mpz(prime * prime) > residual:
            break
        exponent = 0
        while residual % prime == 0:
            residual //= prime
            exponent += 1
        if exponent:
            lower_bound_count *= exponent + 1
        if residual == 1:
            return BoundedDivisorCount(
                value=value,
                exact_count=lower_bound_count,
                lower_bound_count=lower_bound_count,
                residual=1,
                trial_prime_limit=largest_trial_prime,
                status="exact_fully_stripped",
            )

    if residual == 1:
        return BoundedDivisorCount(
            value=value,
            exact_count=lower_bound_count,
            lower_bound_count=lower_bound_count,
            residual=1,
            trial_prime_limit=largest_trial_prime,
            status="exact_fully_stripped",
        )

    if gmpy2.mpz(largest_trial_prime * largest_trial_prime) > residual:
        exact_count = lower_bound_count * 2
        return BoundedDivisorCount(
            value=value,
            exact_count=exact_count,
            lower_bound_count=exact_count,
            residual=int(residual),
            trial_prime_limit=largest_trial_prime,
            status="exact_residual_prime_by_trial_bound",
        )

    status = (
        "bounded_higher_divisor_lower_bound"
        if lower_bound_count > 4
        else "unresolved_large_residual"
    )
    return BoundedDivisorCount(
        value=value,
        exact_count=None,
        lower_bound_count=lower_bound_count,
        residual=int(residual),
        trial_prime_limit=largest_trial_prime,
        status=status,
    )


def divisor_counts_segment_gmp_bounded(
    lo: int,
    hi: int,
    trial_prime_limit: int = 1_000_000,
) -> list[BoundedDivisorCount]:
    """Measure bounded divisor-count evidence on a large-coordinate interval.

    This backend is deliberately bounded. It never fabricates exact divisor
    counts for residuals that remain open after the configured trial-prime
    frontier. Exact counts are returned only when the residual closes by
    arithmetic already measured inside the interval backend. Otherwise the row
    carries a lower bound and an explicit unresolved status.
    """
    if lo < 1:
        raise ValueError("lo must be at least 1")
    if hi <= lo:
        raise ValueError("hi must be larger than lo")
    primes = [int(prime) for prime in _segmented_primes(trial_prime_limit)]
    return [
        _bounded_divisor_count_with_primes(value, primes, trial_prime_limit)
        for value in range(lo, hi)
    ]
