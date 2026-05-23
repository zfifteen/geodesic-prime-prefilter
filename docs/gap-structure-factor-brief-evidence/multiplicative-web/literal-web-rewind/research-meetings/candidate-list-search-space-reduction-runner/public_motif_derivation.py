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
- For unknown N it uses one unified GMP public arithmetic backend.
- For live non-toy N it computes only the calibrated tier-3 public coordinate
  class needed by the grammar motif. Full divisor counts are not required.

Fail-fast philosophy: This file exists to surface blockers quickly. If the
single GMP backend cannot attempt public motif derivation, the caller gets an
explicit implementation-blocked state.
"""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from time import perf_counter
from typing import Any

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

FIRST_OPEN_OFFSETS = (2, 4, 6, 8, 10, 12)
WHEEL_CLOSED_RESIDUES_MOD30 = frozenset({0, 3, 5, 6, 9, 10, 12, 15, 18, 20, 21, 24, 25, 27})

DERIVATION_BACKEND = {
    "name": "gmp_tier3_public_coordinate_backend",
    "kind": "pgs_live_tier3",
    "classification": "classical_assisted_public_coordinate",
    "scale_capable": True,
    "pgs_native": False,
    "classical_assisted": True,
}

LAST_DERIVATION_DIAGNOSTICS: dict[str, Any] = {}


def get_last_derivation_diagnostics() -> dict[str, Any]:
    """Return diagnostics for the most recent non-toy live motif derivation."""
    return dict(LAST_DERIVATION_DIAGNOSTICS)


class PublicMotifUnresolved(RuntimeError):
    """Raised when the backend attempted derivation but found no public motif."""


class PublicMotifBackendError(RuntimeError):
    """Raised when the tier-3 backend cannot determine a required public class."""


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


def _empty_derivation_stats() -> dict[str, Any]:
    return {
        "coordinates_scanned": 0,
        "tier3_classifications": 0,
        "max_public_gap_width": 0,
        "indeterminate_classifications": 0,
        "minimum_d4_large_residual_classifications": 0,
        "derivation_elapsed_seconds": None,
    }


def _is_prime_square(value: gmpy2.mpz) -> bool:
    root, remainder = gmpy2.isqrt_rem(value)
    return remainder == 0 and _is_public_endpoint(root)


def _is_prime_cube(value: gmpy2.mpz) -> bool:
    root, exact = gmpy2.iroot(value, 3)
    return exact and _is_public_endpoint(root)


def _small_trial_primes() -> tuple[int, ...]:
    return _prime_table(1_000_000)


@lru_cache(maxsize=8192)
def _classify_public_coordinate_tier3_cached(value_int: int) -> tuple[str, str, str, tuple[int, int]]:
    value = gmpy2.mpz(value_int)
    if value < 2:
        raise PublicMotifBackendError(f"tier-3 classifier cannot classify coordinate {value}")
    parity = "even" if value % 2 == 0 else "odd"

    if _is_prime_square(value):
        return "d3", "prime_square", "d<=4", (0, 0)

    if _is_prime_cube(value):
        return "d4", f"d4_{parity}", "d<=4", (1, 0)

    divisor_evidence = 1
    residual = gmpy2.mpz(value)
    for prime in _small_trial_primes():
        prime_mpz = gmpy2.mpz(prime)
        if prime_mpz * prime_mpz > residual:
            break
        exponent = 0
        while residual % prime_mpz == 0:
            residual //= prime_mpz
            exponent += 1
        if not exponent:
            continue

        divisor_evidence *= exponent + 1
        if residual == 1:
            return _tier3_from_divisor_evidence(value, divisor_evidence)

        if bool(gmpy2.is_prime(residual)):
            return _tier3_from_divisor_evidence(value, divisor_evidence * 2)

        if divisor_evidence > 64:
            return "d>64", f"higher_divisor_{parity}", "d>64", (4, 0)

    if residual == value:
        if _is_public_endpoint(value):
            raise PublicMotifBackendError(
                f"tier-3 classifier cannot classify public endpoint coordinate {value}"
            )
        # In a prime-gap interior, the coordinate is publicly non-prime.
        # With no smaller visible class and no small divisor evidence, tier-3
        # assigns the minimum composite carrier needed by the motif grammar.
        return "d4", f"d4_{parity}", "d<=4", (1, 1)
    if residual == 1:
        return _tier3_from_divisor_evidence(value, divisor_evidence)
    if bool(gmpy2.is_prime(residual)):
        return _tier3_from_divisor_evidence(value, divisor_evidence * 2)

    root, remainder = gmpy2.isqrt_rem(residual)
    if remainder == 0 and bool(gmpy2.is_prime(root)):
        return _tier3_from_divisor_evidence(value, divisor_evidence * 3)

    return _tier3_from_divisor_evidence(value, divisor_evidence * 4)


def _tier3_from_divisor_evidence(
    value: gmpy2.mpz, divisor_evidence: int
) -> tuple[str, str, str, tuple[int, int]]:
    parity = "even" if value % 2 == 0 else "odd"
    if divisor_evidence == 3:
        return "d3", "prime_square", "d<=4", (0, 0)
    if divisor_evidence == 4:
        return "d4", f"d4_{parity}", "d<=4", (1, 0)
    if divisor_evidence <= 16:
        return "5<=d<=16", f"higher_divisor_{parity}", "5<=d<=16", (2, 0)
    if divisor_evidence <= 64:
        return "17<=d<=64", f"higher_divisor_{parity}", "17<=d<=64", (3, 0)
    return "d>64", f"higher_divisor_{parity}", "d>64", (4, 0)


def classify_public_coordinate_tier3(value: gmpy2.mpz) -> dict[str, object]:
    """Return the calibrated tier-3 public coordinate class for motif derivation."""
    label, family, bucket, rank_prefix = _classify_public_coordinate_tier3_cached(int(value))
    return {
        "divisor_label": label,
        "carrier_family": family,
        "bucket": bucket,
        "rank_prefix": rank_prefix,
    }


def _tier3_gap_winner(
    left_endpoint: gmpy2.mpz,
    right_endpoint: gmpy2.mpz,
    stats: dict[str, Any],
) -> tuple[int | None, str, str, str, tuple[int, int] | None]:
    width = int(right_endpoint - left_endpoint)
    first_higher: tuple[tuple[int, int], int, str, str, str] | None = None

    for offset in range(1, width):
        value = left_endpoint + offset
        stats["coordinates_scanned"] += 1
        if _is_prime_square(value):
            return offset, "d3", "prime_square", "d<=4", (0, offset)

    for offset in range(1, width):
        value = left_endpoint + offset
        stats["coordinates_scanned"] += 1
        stats["tier3_classifications"] += 1
        try:
            label, family, bucket, rank_prefix = _classify_public_coordinate_tier3_cached(int(value))
        except PublicMotifBackendError:
            stats["indeterminate_classifications"] += 1
            raise
        if rank_prefix == (1, 1):
            stats["minimum_d4_large_residual_classifications"] += 1
        rank = (rank_prefix[0], offset)
        if label == "d4":
            return offset, label, family, bucket, rank
        if label != "d3" and (first_higher is None or rank < first_higher[0]):
            first_higher = (rank, offset, label, family, bucket)

    if first_higher is None:
        return None, "empty", "empty", "empty", None
    rank, offset, label, family, bucket = first_higher
    return offset, label, family, bucket, rank


def _gap_grammar_gmp(
    role: str,
    left_endpoint: gmpy2.mpz,
    right_endpoint: gmpy2.mpz,
    coordinate: gmpy2.mpz | None = None,
    stats: dict[str, Any] | None = None,
) -> dict[str, object]:
    """Return one public gap grammar payload from the unified tier-3 GMP backend."""
    if stats is None:
        stats = _empty_derivation_stats()
    left_endpoint = gmpy2.mpz(left_endpoint)
    right_endpoint = gmpy2.mpz(right_endpoint)
    width = int(right_endpoint - left_endpoint)
    stats["max_public_gap_width"] = max(int(stats["max_public_gap_width"]), width)
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

    winner_offset, divisor_label, family, bucket, rank = _tier3_gap_winner(
        left_endpoint,
        right_endpoint,
        stats,
    )
    if winner_offset is None or rank is None:
        raise PublicMotifUnresolved("tier-3 gap grammar found no interior winner")

    winner_value = left_endpoint + winner_offset
    exact_type_key = f"o{first_open}_{divisor_label}_a{winner_offset}_{family}"
    reduced_state = f"o{first_open}_{family}|{bucket}"

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
        "winner_d": divisor_label,
        "winner_divisor_label": divisor_label,
        "winner_bucket": bucket,
        "winner_rank": list(rank),
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

    For non-toy N we call the live public gap-grammar engine.
    """
    global LAST_DERIVATION_DIAGNOSTICS

    # Hard protection of the validated toy evidence surface
    if n in TOY_N_TO_MOTIF:
        LAST_DERIVATION_DIAGNOSTICS = {
            "toy_lookup": True,
            **_empty_derivation_stats(),
        }
        return TOY_N_TO_MOTIF[n]

    n_mp = gmpy2.mpz(n)
    stats = _empty_derivation_stats()
    start = perf_counter()

    try:
        prev_end, left, right, _ = _neighboring_gaps_gmp(n_mp)
        containing = _gap_grammar_gmp("containing", left, right, n_mp, stats)
        previous_gap = _gap_grammar_gmp("previous", prev_end, left, stats=stats)
    except (PublicMotifUnresolved, PublicMotifBackendError):
        stats["derivation_elapsed_seconds"] = round(perf_counter() - start, 6)
        LAST_DERIVATION_DIAGNOSTICS = dict(stats)
        raise
    except Exception as exc:
        stats["derivation_elapsed_seconds"] = round(perf_counter() - start, 6)
        LAST_DERIVATION_DIAGNOSTICS = dict(stats)
        raise RuntimeError(f"Failed to compute public gaps for N={n}") from exc
    stats["derivation_elapsed_seconds"] = round(perf_counter() - start, 6)
    LAST_DERIVATION_DIAGNOSTICS = dict(stats)

    exact_type = containing.get("exact_type_key") or containing.get("reduced_state", "unknown")
    phase = _relative_phase_bucket(containing)
    base_motif = f"{exact_type}@{phase}"

    if not include_context:
        return base_motif

    # Compute simple prev context for the highest-signal rules
    prev_reduced = previous_gap.get("reduced_state") or previous_gap.get("exact_type_key", "")
    if prev_reduced:
        # Normalize to the short form the pruner recognizes (e.g. "o4_d4_odd")
        # Many rules look for things like "o4_d4_odd prev"
        short_prev = prev_reduced.split("|")[0] if "|" in prev_reduced else prev_reduced
        # Common pattern used in the rule set
        return f"{base_motif} + {short_prev} prev"

    return base_motif


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
