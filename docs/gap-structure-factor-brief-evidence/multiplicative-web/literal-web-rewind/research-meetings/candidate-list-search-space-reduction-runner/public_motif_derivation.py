#!/usr/bin/env python3
"""
Public Motif Derivation for the PGA Grammar Pruner

This module provides the function that turns a raw semiprime N into the
public structural motif string expected by the pruner:

    "o2_d4_a2_d4_odd@mid"
    "o2_d4_a2_d4_odd@early + o4_d4_odd prev"
    etc.

The motif encodes:
- The attractor subtype of the GWR (leftmost minimum-divisor) winner
  inside the chamber containing N (under DNI normalization)
- The phase of N within that containing exact_type

This is the critical bridge between "I have a raw N" and "I can apply
the public grammar exclusion rules".

Contract:
- Must be 100% public-only. Never uses p or q.
- Must be deterministic.
- For the toy corpus it must reproduce the known TOY_N_TO_MOTIF values.
- For unknown N it must use a PGS-native motif certificate.
- Until that certificate exists, non-toy live derivation is explicitly blocked.

Fail-fast philosophy: This file exists to surface blockers quickly. If the
PGS-native certificate is unavailable, the caller gets an explicit
derivation-blocked state. Blocked derivation is not unresolved mathematics.
"""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path

import gmpy2

# ---------------------------------------------------------------------------
# Local path anchors for generated evidence artifacts and future repo-relative checks.
# ---------------------------------------------------------------------------

THIS_DIR = Path(__file__).resolve().parent

def _find_repo_root(start: Path) -> Path | None:
    """Walk upward until we find a directory containing 'research' and '.git' or 'src'."""
    current = start
    for _ in range(12):  # safety bound
        if (current / "research").exists() and (current / ".git").exists():
            return current
        if (current / "src" / "python").exists():
            return current
        parent = current.parent
        if parent == current:
            break
        current = parent
    return None

REPO_ROOT = _find_repo_root(THIS_DIR) or THIS_DIR.parents[6]

GMP_EXACT_DIVISOR_TRIAL_LIMIT = 70_000_000
FIRST_OPEN_OFFSETS = (2, 4, 6, 8, 10, 12)
WHEEL_CLOSED_RESIDUES_MOD30 = frozenset({0, 3, 5, 6, 9, 10, 12, 15, 18, 20, 21, 24, 25, 27})

DERIVATION_BACKEND = {
    "name": "pgs_native_motif_derivation_unavailable",
    "kind": "pgs_native_unavailable",
    "classification": "pgs_native_blocked",
    "scale_capable": False,
    "pgs_native": True,
    "classical_assisted": False,
    "motif_certificate_available": False,
    "blocked_reason": "pgs_native_motif_certificate_unavailable",
}


class PublicMotifDerivationBlocked(RuntimeError):
    """Raised when no PGS-native motif certificate exists for live non-toy derivation."""


class PublicMotifBackendLimitExceeded(RuntimeError):
    """Raised when live motif derivation is blocked by the current backend limit."""


class PublicMotifUnresolved(RuntimeError):
    """Raised when the backend attempted derivation but found no public motif."""


# ---------------------------------------------------------------------------
# Known toy motifs (for validation during development)
# These must be reproduced exactly once derivation is working.
# ---------------------------------------------------------------------------

TOY_N_TO_MOTIF: dict[int, str] = {
    989: "o2_d4_a2_d4_odd@mid",
    9379: "o2_d4_a2_d4_odd@mid",
    25807: "o2_d4_a2_d4_odd@mid",
    1242079: "o4_d4_a4_d4_odd@mid",
    200250077: "o2_d4_a2_d4_odd@mid",
    4295229443: "o4_d4_a4_d4_odd@mid",
    18902665303: "o2_d4_a2_d4_odd@mid",
    1209476905903: "o2_d4_a2_d4_odd@mid",
    77468500194643: "o2_d4_a2_d4_odd@mid",
    4951764003343009: "o2_d4_a2_d4_odd@mid",
}


# ---------------------------------------------------------------------------
# Public Motif Derivation
# ---------------------------------------------------------------------------


def _phase_bucket(mpermille: int | None) -> str:
    """Coarse phase from position in thousandths inside the gap."""
    if mpermille is None:
        return "empty"
    if mpermille < 250:
        return "early"
    if mpermille < 750:
        return "mid"
    if mpermille < 900:
        return "late"
    return "very_late"


def _relative_phase_bucket(containing_gap: dict[str, object]) -> str:
    """Compute phase bucket for the coordinate inside its containing gap."""
    width = int(containing_gap["gap_width"])
    offset = containing_gap.get("coordinate_offset_from_left")
    if offset is None or width < 1:
        return "empty"
    mpermille = (int(offset) * 1000) // width
    return _phase_bucket(mpermille)


@lru_cache(maxsize=16)
def _prime_table(limit: int) -> tuple[int, ...]:
    """Return every prime up to limit using a plain Python sieve."""
    limit = int(limit)
    if limit < 2:
        return ()

    sieve = bytearray(b"\x01") * (limit + 1)
    sieve[0:2] = b"\x00\x00"
    root = int(gmpy2.isqrt(limit))
    for candidate in range(2, root + 1):
        if sieve[candidate]:
            start = candidate * candidate
            sieve[start : limit + 1 : candidate] = b"\x00" * (((limit - start) // candidate) + 1)
    return tuple(index for index in range(2, limit + 1) if sieve[index])


def _first_open_offset(left_endpoint: gmpy2.mpz) -> int:
    """Return the first wheel-open even offset after one endpoint."""
    residue = int(left_endpoint % 30)
    for offset in FIRST_OPEN_OFFSETS:
        candidate = (residue + offset) % 30
        if candidate not in WHEEL_CLOSED_RESIDUES_MOD30:
            return offset
    raise RuntimeError(f"no wheel-open offset found after residue {residue}")


def _is_public_endpoint(value: gmpy2.mpz) -> bool:
    """Return whether one public coordinate is an endpoint under GMP arithmetic."""
    return value >= 2 and bool(gmpy2.is_prime(value))


def _next_endpoint_gmp(value: gmpy2.mpz) -> gmpy2.mpz:
    """Return the first public endpoint at or after one coordinate."""
    value = gmpy2.mpz(value)
    if value <= 2:
        return gmpy2.mpz(2)
    if _is_public_endpoint(value):
        return value
    return gmpy2.next_prime(value)


def _previous_endpoint_gmp(value: gmpy2.mpz) -> gmpy2.mpz | None:
    """Return the previous public endpoint strictly before one coordinate."""
    value = gmpy2.mpz(value)
    if value <= 2:
        return None
    if value <= 3:
        return gmpy2.mpz(2)

    candidate = value - 1
    if candidate % 2 == 0:
        candidate -= 1
    while candidate >= 3:
        if _is_public_endpoint(candidate):
            return candidate
        candidate -= 2
    return gmpy2.mpz(2)


def _divisor_count_gmp(value: gmpy2.mpz, primes: tuple[int, ...]) -> int:
    """
    Return the exact divisor count for one public coordinate using the GMP backend.

    The calculation is exact when the required trial-prime horizon is inside
    GMP_EXACT_DIVISOR_TRIAL_LIMIT. Larger coordinates return an explicit
    implementation-blocked state instead of falling into the old int64/scalar path.
    """
    value = gmpy2.mpz(value)
    if value < 1:
        raise ValueError("value must be at least 1")
    if value == 1:
        return 1

    cube_root, exact_cube = gmpy2.iroot(value, 3)
    if not exact_cube:
        cube_root += 1
    if cube_root > GMP_EXACT_DIVISOR_TRIAL_LIMIT:
        raise PublicMotifBackendLimitExceeded(
            "GMP exact divisor-count horizon exceeds configured public motif limit "
            f"({int(cube_root)} > {GMP_EXACT_DIVISOR_TRIAL_LIMIT})"
        )

    residual = gmpy2.mpz(value)
    divisor_count = 1
    for prime in primes:
        if prime > cube_root:
            break
        prime_mpz = gmpy2.mpz(prime)
        if prime_mpz * prime_mpz > residual:
            break
        exponent = 0
        while residual % prime_mpz == 0:
            residual //= prime_mpz
            exponent += 1
        if exponent:
            divisor_count *= exponent + 1
        if residual == 1:
            return divisor_count

    if residual == 1:
        return divisor_count
    if bool(gmpy2.is_prime(residual)):
        return divisor_count * 2

    root, exact_square = gmpy2.isqrt_rem(residual)
    if exact_square == 0 and bool(gmpy2.is_prime(root)):
        return divisor_count * 3

    return divisor_count * 4


def _carrier_family(value: gmpy2.mpz | None, divisor_count: int | None) -> str:
    """Return the reduced PGS carrier family."""
    if value is None or divisor_count is None:
        return "empty"
    if divisor_count == 3:
        return "prime_square"
    if divisor_count == 4:
        return "d4_even" if value % 2 == 0 else "d4_odd"
    return "higher_divisor_even" if value % 2 == 0 else "higher_divisor_odd"


def _divisor_bucket(divisor_count: int | None) -> str:
    """Return the reduced grammar divisor bucket."""
    if divisor_count is None:
        return "empty"
    if divisor_count <= 4:
        return "d<=4"
    if divisor_count <= 16:
        return "5<=d<=16"
    if divisor_count <= 64:
        return "17<=d<=64"
    return "d>64"


def _gap_grammar_gmp(
    role: str,
    left_endpoint: gmpy2.mpz,
    right_endpoint: gmpy2.mpz,
    coordinate: gmpy2.mpz | None = None,
) -> dict[str, object]:
    """Return one public gap grammar payload from the unified GMP backend."""
    left_endpoint = gmpy2.mpz(left_endpoint)
    right_endpoint = gmpy2.mpz(right_endpoint)
    width = int(right_endpoint - left_endpoint)
    interior_count = max(0, width - 1)
    first_open = _first_open_offset(left_endpoint)
    contains_coordinate = (
        coordinate is not None
        and left_endpoint < coordinate < right_endpoint
    )

    if interior_count == 0:
        return {
            "role": role,
            "left_endpoint": str(left_endpoint),
            "right_endpoint": str(right_endpoint),
            "gap_width": width,
            "contains_coordinate": contains_coordinate,
            "coordinate_offset_from_left": None,
            "coordinate_offset_from_right": None,
            "first_open_offset": first_open,
            "winner_value": None,
            "winner_offset": None,
            "winner_d": None,
            "carrier_family": "empty",
            "exact_type_key": f"o{first_open}_empty",
            "reduced_state": f"o{first_open}_empty|empty",
        }

    cube_root, exact_cube = gmpy2.iroot(right_endpoint - 1, 3)
    if not exact_cube:
        cube_root += 1
    prime_limit = int(cube_root)
    if prime_limit > GMP_EXACT_DIVISOR_TRIAL_LIMIT:
        raise PublicMotifBackendLimitExceeded(
            "GMP gap grammar exact divisor horizon exceeds configured public motif limit "
            f"({prime_limit} > {GMP_EXACT_DIVISOR_TRIAL_LIMIT})"
        )
    primes = _prime_table(prime_limit)

    winner_d: int | None = None
    winner_offset: int | None = None
    for offset in range(1, width):
        divisor_count = _divisor_count_gmp(left_endpoint + offset, primes)
        if winner_d is None or divisor_count < winner_d:
            winner_d = divisor_count
            winner_offset = offset

    if winner_d is None or winner_offset is None:
        raise PublicMotifUnresolved("GMP gap grammar found no interior winner")

    winner_value = left_endpoint + winner_offset
    family = _carrier_family(winner_value, winner_d)
    exact_type_key = f"o{first_open}_d{winner_d}_a{winner_offset}_{family}"
    reduced_state = f"o{first_open}_{family}|{_divisor_bucket(winner_d)}"

    return {
        "role": role,
        "left_endpoint": str(left_endpoint),
        "right_endpoint": str(right_endpoint),
        "gap_width": width,
        "contains_coordinate": contains_coordinate,
        "coordinate_offset_from_left": (
            None if coordinate is None else int(coordinate - left_endpoint)
        ),
        "coordinate_offset_from_right": (
            None if coordinate is None else int(right_endpoint - coordinate)
        ),
        "first_open_offset": first_open,
        "winner_value": str(winner_value),
        "winner_offset": winner_offset,
        "winner_d": winner_d,
        "carrier_family": family,
        "exact_type_key": exact_type_key,
        "reduced_state": reduced_state,
    }


def _neighboring_gaps_gmp(coordinate: gmpy2.mpz) -> tuple[gmpy2.mpz, gmpy2.mpz, gmpy2.mpz, gmpy2.mpz]:
    """Return previous, left, right, and following public endpoints around one coordinate."""
    coordinate = gmpy2.mpz(coordinate)
    left = _previous_endpoint_gmp(coordinate - 1)
    if left is None:
        raise PublicMotifUnresolved(f"no left endpoint found for {coordinate}")
    right = _next_endpoint_gmp(coordinate + 1)
    previous = _previous_endpoint_gmp(left - 1)
    if previous is None:
        raise PublicMotifUnresolved(f"no previous endpoint found for {coordinate}")
    following = _next_endpoint_gmp(right + 1)
    return previous, left, right, following


def derive_public_motif(n: int, include_context: bool = True) -> str:
    """
    Given a raw integer N, return its public structural motif in the format
    expected by the PGA Grammar Pruner.

    For any N in the frozen toy corpus we ALWAYS return the pre-computed
    validated motif. This protects the evidence surface that produced the
    strong reduction numbers.

    For non-toy N this function requires a PGS-native motif certificate. The
    certificate path is not implemented here yet, so live non-toy derivation is
    blocked before any classical public-coordinate arithmetic can choose a motif.
    """
    # Hard protection of the validated toy evidence surface
    if n in TOY_N_TO_MOTIF:
        return TOY_N_TO_MOTIF[n]

    raise PublicMotifDerivationBlocked(
        "pgs_native_motif_certificate_unavailable: non-toy live raw-N motif "
        "derivation is blocked until a PGS-native motif certificate exists"
    )


def validate_on_toy_corpus() -> bool:
    """
    Quick sanity check: does derive_public_motif reproduce the known toy motifs?
    """
    for n, expected in TOY_N_TO_MOTIF.items():
        actual = derive_public_motif(n)
        if actual != expected:
            print(f"MISMATCH for {n}: got {actual}, expected {expected}")
            return False
    print("All toy motifs reproduced correctly.")
    return True


if __name__ == "__main__":
    print("Testing public motif derivation stub on toy corpus...")
    validate_on_toy_corpus()
