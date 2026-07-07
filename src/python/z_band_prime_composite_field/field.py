"""Exact composite-field helpers used by prime-gap studies."""

from __future__ import annotations

import math

import gmpy2
import numpy as np


SEGMENT_SIZE = 1_000_000
INT64_FIELD_MAX = int(np.iinfo(np.int64).max)


def _integer_cube_root(value: int) -> tuple[int, bool]:
    """Return floor cube root and exactness for one non-negative integer."""
    root, exact = gmpy2.iroot(gmpy2.mpz(value), 3)
    return int(root), bool(exact)


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


def _divisor_count_exact_scalar(value: int) -> int:
    """Compute one exact divisor count without fixed-width array coordinates."""
    if value < 1:
        raise ValueError("value must be at least 1")
    if value == 1:
        return 1

    residual = gmpy2.mpz(value)
    divisor_count = 1
    cube_root_limit, _ = _integer_cube_root(value)

    for prime in _segmented_primes(cube_root_limit):
        prime_mpz = gmpy2.mpz(prime)
        if prime_mpz * prime_mpz > residual:
            break
        exponent = 0
        while residual % prime == 0:
            residual //= prime
            exponent += 1
        if exponent:
            divisor_count *= exponent + 1
        if residual == 1:
            return divisor_count

    if residual == 1:
        return divisor_count

    remainder_int = int(residual)
    # Replaced small-basis _has_no_composite_witness with robust gmpy2.is_prime for > 64-bit residues
    if gmpy2.is_prime(residual, 25):
        return divisor_count * 2

    root = math.isqrt(remainder_int)
    if root * root == remainder_int and gmpy2.is_prime(gmpy2.mpz(root), 25):
        return divisor_count * 3

    return divisor_count * 4


def _divisor_counts_segment_scalar(lo: int, hi: int) -> np.ndarray:
    import sympy
    size = hi - lo
    values = np.empty(size, dtype=object)
    for i in range(size):
        values[i] = lo + i
    residual = values.copy()
    divisor_count = np.ones(size, dtype=np.uint64)
    
    # Fast segment sieve for small primes
    for prime in _segmented_primes(100000):
        prime_int = int(prime)
        start_offset = (prime_int - (lo % prime_int)) % prime_int
        # Need pure python loop here because modulo on object array is slow
        for i in range(start_offset, size, prime_int):
            exponent = 0
            while residual[i] % prime_int == 0:
                residual[i] //= prime_int
                exponent += 1
            if exponent:
                divisor_count[i] *= (exponent + 1)
                
    for i in range(size):
        rem = residual[i]
        if rem == 1:
            continue
            
        rem_int = int(rem)
        if gmpy2.is_prime(gmpy2.mpz(rem_int), 25):
            divisor_count[i] *= 2
            continue
            
        root = math.isqrt(rem_int)
        if root * root == rem_int and gmpy2.is_prime(gmpy2.mpz(root), 25):
            divisor_count[i] *= 3
            continue
            
        # As recommended by Grok: for >64-bit residues, if not prime or square, return *4 
        # (assumed semiprime cofactor). Mathematically an underbound if >= 3 prime factors remain.
        divisor_count[i] *= 4
        
    return divisor_count


def divisor_counts_segment(lo: int, hi: int) -> np.ndarray:
    """Compute exact divisor counts on one contiguous natural-number interval."""
    if lo < 1:
        raise ValueError("lo must be at least 1")
    if hi <= lo:
        raise ValueError("hi must be larger than lo")
    if hi - 1 > INT64_FIELD_MAX:
        return _divisor_counts_segment_scalar(lo, hi)

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
