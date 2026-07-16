#!/usr/bin/env python3
"""PGSMPG v0.1 live generator."""

from __future__ import annotations

import math

from sympy import divisor_count


DEFAULT_CANDIDATE_BOUND = 4096
DEFAULT_MAX_EXPONENT = 127
PGSMPG_VERSION = "0.1.1"
PGSMPG_FREEZE_ID = "pgs_mersenne_prime_generator_v0_1"
PGSMPG_SOURCE = "PGSMPG"
PGSMPG_RULE_ID = "pgsmpg_exponent_successor_v0_1"
PGSMPG_LEFT_BOUNDARY_RULE_ID = "pgsmpg_left_boundary_chamber_reset_v0_1"
PGSMPG_RESIDUE_RETURN_RULE_ID = "pgsmpg_residue_return_pressure_v0_3"
# Bounded small-divisor scan for thresholded divisor-state checks. Full exact
# tau is used only when this bound does not settle the cell.
SMALL_DIVISOR_SCAN_LIMIT = 50_000
# Additional scan band for algebraic factor candidates of 2^e - 1 (form 2*k*e + 1).
MERSENNE_FORM_DIVISOR_SCAN_LIMIT = 2_000_000
# Known-composite lower bound written when exact tau is not computed.
DEFERRED_DIVISOR_COUNT_LOWER_BOUND = 3
WHEEL_OPEN_RESIDUES_MOD30 = frozenset({1, 7, 11, 13, 17, 19, 23, 29})
LOW_PRIMES = frozenset({2, 3, 5})
STATUS_EXPONENT_DIVISOR_COUNT_NOT_TWO = "exponent_divisor_count_not_two"
STATUS_BOUNDARY_REJECTED = "boundary_rejected"
STATUS_BOUNDARY_RESOLVED_SURVIVOR = "boundary_resolved_survivor"
STATUS_BOUNDARY_UNRESOLVED = "boundary_unresolved"
STATUS_MERSENNE_LOCATION_INFERRED = "mersenne_location_inferred"
STATUS_MERSENNE_LOCATION_NOT_INFERRED = "mersenne_location_not_inferred"
STATUS_RESIDUE_RETURN_DEFERRED = "residue_return_deferred"
STATUS_RESIDUE_RETURN_RESOLVED_SURVIVOR = "residue_return_resolved_survivor"


class PGSMPGUnresolvedError(RuntimeError):
    """Raised when PGSMPG does not resolve inside the configured surface."""


def tau(n: int) -> int:
    """Return exact divisor count."""
    return int(divisor_count(int(n)))


def _small_divisor_scan_finds_proper_divisor(
    n: int,
    factor_limit: int = SMALL_DIVISOR_SCAN_LIMIT,
) -> bool:
    """Return True when a proper divisor is found by a bounded odd factor scan."""
    n = int(n)
    factor_limit = int(factor_limit)
    if n < 2:
        return True
    if n == 2:
        return False
    if n % 2 == 0:
        return True
    root = math.isqrt(n)
    limit = root if root <= factor_limit else factor_limit
    factor = 3
    while factor <= limit:
        if n % factor == 0:
            return True
        factor += 2
    return False


def _mersenne_form_divisor_scan_finds_proper_divisor(
    exponent: int,
    candidate: int,
    factor_limit: int = MERSENNE_FORM_DIVISOR_SCAN_LIMIT,
) -> bool:
    """Return True when a proper divisor of form 2*k*e+1 is found under the band.

    This is divisor-state measurement on the offset-1 cell 2^e - 1, using the
    algebraic shape of that cell. It is not a classical primality decision rule.
    """
    exponent = int(exponent)
    candidate = int(candidate)
    factor_limit = int(factor_limit)
    if exponent < 2 or candidate < 2:
        return True
    # q = 2*k*e + 1, with q <= factor_limit and q < candidate.
    max_q = min(factor_limit, candidate - 1)
    if max_q < 3:
        return False
    k_max = (max_q - 1) // (2 * exponent)
    for k in range(1, k_max + 1):
        q = 2 * k * exponent + 1
        if q >= 3 and candidate % q == 0:
            return True
    return False


def _offset1_has_threshold_proper_divisor(exponent: int, candidate: int) -> bool:
    """Return True when thresholded scans prove the offset-1 cell is composite."""
    # General odd scan is useful on small cells. On large Mersenne cells the
    # algebraic form scan is the high-leverage bounded check.
    if int(candidate).bit_length() <= 40:
        if _small_divisor_scan_finds_proper_divisor(candidate):
            return True
    return _mersenne_form_divisor_scan_finds_proper_divisor(exponent, candidate)


def tau_equals_two(n: int, factor_limit: int = SMALL_DIVISOR_SCAN_LIMIT) -> bool:
    """Return True iff n has exact divisor count 2 (PGS survivor state).

    Uses a bounded small-divisor scan first. A proper divisor found in that
    band settles the cell as non-survivor without a full exact tau inventory.
    When the band does not settle the cell, exact tau finishes the proof.
    """
    n = int(n)
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    root = math.isqrt(n)
    limit = root if root <= int(factor_limit) else int(factor_limit)
    factor = 3
    while factor <= limit:
        if n % factor == 0:
            return False
        factor += 2
    if limit >= root:
        return True
    return tau(n) == 2


def divisor_state_label(divisor_state: int) -> str:
    """Return a compact label for one thresholded divisor-count state."""
    return "2" if int(divisor_state) == 2 else ">2"


def iter_admissible_left_offsets(exponent: int, candidate_bound: int):
    """Yield wheel-open offsets to the left of one power of two."""
    exponent = int(exponent)
    candidate_bound = int(candidate_bound)
    if candidate_bound < 1:
        raise ValueError("candidate_bound must be positive")
    power_residue_mod30 = pow(2, exponent, 30)
    open_offset_residues = tuple(
        offset_residue
        for offset_residue in range(1, 31)
        if (power_residue_mod30 - offset_residue) % 30 in WHEEL_OPEN_RESIDUES_MOD30
    )
    small_prime_offsets = (
        sorted(
            {
                2**exponent - prime
                for prime in LOW_PRIMES
                if 1 <= 2**exponent - prime <= candidate_bound
            }
        )
        if exponent <= 3
        else []
    )

    small_index = 0
    for block_start in range(0, candidate_bound, 30):
        block_end = min(candidate_bound, block_start + 30)
        block_small_offsets = []
        while (
            small_index < len(small_prime_offsets)
            and small_prime_offsets[small_index] <= block_end
        ):
            block_small_offsets.append(small_prime_offsets[small_index])
            small_index += 1

        block_small_index = 0
        for offset_residue in open_offset_residues:
            offset = block_start + offset_residue
            if offset > candidate_bound:
                break
            while (
                block_small_index < len(block_small_offsets)
                and block_small_offsets[block_small_index] < offset
            ):
                yield block_small_offsets[block_small_index]
                block_small_index += 1
            if (
                block_small_index < len(block_small_offsets)
                and block_small_offsets[block_small_index] == offset
            ):
                block_small_index += 1
            yield offset

        while block_small_index < len(block_small_offsets):
            yield block_small_offsets[block_small_index]
            block_small_index += 1


def admissible_left_offsets(exponent: int, candidate_bound: int) -> list[int]:
    """Return wheel-open offsets to the left of one power of two."""
    return list(iter_admissible_left_offsets(exponent, candidate_bound))


def residue_return_pressure(exponent: int) -> dict[str, object]:
    """Return the offset-1 chamber pressure below one exponent wall.

    Live succession only needs pressure == 0 versus pressure > 0. Deferred
    cells may stop once a proper divisor is known (thresholded divisor state).
    Survivors still require a complete tau == 2 proof.
    """
    exponent = int(exponent)
    if exponent < 2:
        raise ValueError("exponent must be at least 2")

    candidate = (1 << exponent) - 1
    bit_length = exponent
    root = math.isqrt(candidate)

    # Fast deferred path: proper divisor from bounded divisor-state scans.
    if _offset1_has_threshold_proper_divisor(exponent, candidate):
        return {
            "rule_id": PGSMPG_RESIDUE_RETURN_RULE_ID,
            "exponent": exponent,
            "offset_from_power_of_two": 1,
            "candidate_bit_length": bit_length,
            "candidate_divisor_count": DEFERRED_DIVISOR_COUNT_LOWER_BOUND,
            "pressure": 1,
            "exact_divisor_count": False,
            "status": STATUS_RESIDUE_RETURN_DEFERRED,
            "used_forbidden_tool": False,
        }

    # Bounded scan already covered every factor candidate through isqrt(n).
    if root <= SMALL_DIVISOR_SCAN_LIMIT:
        return {
            "rule_id": PGSMPG_RESIDUE_RETURN_RULE_ID,
            "exponent": exponent,
            "offset_from_power_of_two": 1,
            "candidate_bit_length": bit_length,
            "candidate_divisor_count": 2,
            "pressure": 0,
            "exact_divisor_count": True,
            "status": STATUS_RESIDUE_RETURN_RESOLVED_SURVIVOR,
            "used_forbidden_tool": False,
        }

    # Remaining hard cell: one exact tau settles survivor versus deferred.
    divisor_count_candidate = tau(candidate)
    pressure = divisor_count_candidate - 2
    return {
        "rule_id": PGSMPG_RESIDUE_RETURN_RULE_ID,
        "exponent": exponent,
        "offset_from_power_of_two": 1,
        "candidate_bit_length": bit_length,
        "candidate_divisor_count": divisor_count_candidate,
        "pressure": pressure,
        "exact_divisor_count": True,
        "status": (
            STATUS_RESIDUE_RETURN_RESOLVED_SURVIVOR
            if pressure == 0
            else STATUS_RESIDUE_RETURN_DEFERRED
        ),
        "used_forbidden_tool": False,
    }


def residue_return_boundary_certificate(
    pressure: dict[str, object],
    candidate_bound: int,
) -> dict[str, object]:
    """Return a boundary-shaped certificate from offset-1 pressure."""
    exponent = int(pressure["exponent"])
    candidate_bound = int(candidate_bound)
    if candidate_bound < 1:
        raise ValueError("candidate_bound must be positive")
    return {
        "rule_id": PGSMPG_LEFT_BOUNDARY_RULE_ID,
        "exponent": exponent,
        "power_of_two_exponent": exponent,
        "power_of_two_bit_length": exponent + 1,
        "candidate_bound": candidate_bound,
        "left_boundary_offset_from_power_of_two": 1,
        "left_boundary_bit_length": int(pressure["candidate_bit_length"]),
        "distance_to_left_boundary": 1,
        "candidate_state_count": 1,
        "closed_offset_count_before_boundary": 0,
        "active_count": 1,
        "resolved_count": 1,
        "unresolved_count": 0,
        "carrier_offset_from_power_of_two": None,
        "carrier_d": None,
        "lock_carrier_offset": None,
        "lock_carrier_d": None,
        "lower_d_threat_offset": None,
        "counted_prefix_length": 1,
        "residue_return_pressure": pressure,
        "used_forbidden_tool": False,
    }


def left_boundary_state_certificate(
    exponent: int,
    candidate_bound: int = DEFAULT_CANDIDATE_BOUND,
) -> dict[str, object] | None:
    """Return the first resolved survivor to the left of one exponent wall."""
    exponent = int(exponent)
    candidate_bound = int(candidate_bound)
    if exponent < 2:
        raise ValueError("exponent must be at least 2")
    if candidate_bound < 1:
        raise ValueError("candidate_bound must be positive")

    power_of_two = 2**exponent
    scanned_count = 0
    rejected_count = 0
    carrier_offset: int | None = None
    carrier_d: int | None = None

    for offset in iter_admissible_left_offsets(exponent, candidate_bound):
        scanned_count += 1
        n = power_of_two - offset
        divisor_count_n = tau(n)
        if divisor_count_n > 2:
            status = STATUS_BOUNDARY_REJECTED
            rejected_count += 1
            if carrier_d is None or divisor_count_n < carrier_d:
                carrier_offset = offset
                carrier_d = divisor_count_n
        else:
            status = STATUS_BOUNDARY_RESOLVED_SURVIVOR
        if status == STATUS_BOUNDARY_RESOLVED_SURVIVOR:
            return {
                "rule_id": PGSMPG_LEFT_BOUNDARY_RULE_ID,
                "exponent": exponent,
                "power_of_two_exponent": exponent,
                "power_of_two_bit_length": exponent + 1,
                "candidate_bound": candidate_bound,
                "left_boundary_offset_from_power_of_two": offset,
                "left_boundary_bit_length": n.bit_length(),
                "distance_to_left_boundary": offset,
                "candidate_state_count": scanned_count,
                "closed_offset_count_before_boundary": rejected_count,
                "active_count": scanned_count - rejected_count,
                "resolved_count": 1,
                "unresolved_count": 0,
                "carrier_offset_from_power_of_two": carrier_offset,
                "carrier_d": carrier_d,
                "lock_carrier_offset": carrier_offset,
                "lock_carrier_d": carrier_d,
                "lower_d_threat_offset": None,
                "counted_prefix_length": offset,
                "used_forbidden_tool": False,
            }

    return None


def exponent_attempt_row(
    exponent: int,
    candidate_bound: int = DEFAULT_CANDIDATE_BOUND,
) -> dict[str, object]:
    """Return one candidate-exponent attempt row."""
    exponent = int(exponent)
    if not tau_equals_two(exponent):
        # Exponents in the live scan are small; exact tau is cheap diagnostics.
        return {
            "exponent": exponent,
            "exponent_divisor_count": tau(exponent),
            "status": STATUS_EXPONENT_DIVISOR_COUNT_NOT_TWO,
            "boundary_certificate": None,
            "residue_return_pressure": None,
            "distance_to_left_boundary": "",
            "mersenne_location_inferred": False,
        }

    pressure = residue_return_pressure(exponent)
    if pressure["status"] == STATUS_RESIDUE_RETURN_DEFERRED:
        return {
            "exponent": exponent,
            "exponent_divisor_count": 2,
            "status": STATUS_RESIDUE_RETURN_DEFERRED,
            "boundary_certificate": None,
            "residue_return_pressure": pressure,
            "distance_to_left_boundary": "",
            "mersenne_location_inferred": False,
        }

    certificate = residue_return_boundary_certificate(pressure, candidate_bound)
    return {
        "exponent": exponent,
        "exponent_divisor_count": 2,
        "status": STATUS_MERSENNE_LOCATION_INFERRED,
        "boundary_certificate": certificate,
        "residue_return_pressure": pressure,
        "distance_to_left_boundary": 1,
        "mersenne_location_inferred": True,
    }


def pgs_mersenne_prime_certificate(
    p: int,
    max_exponent: int = DEFAULT_MAX_EXPONENT,
    candidate_bound: int = DEFAULT_CANDIDATE_BOUND,
) -> dict[str, object] | None:
    """Return the first PGSMPG successor certificate."""
    p = int(p)
    max_exponent = int(max_exponent)
    candidate_bound = int(candidate_bound)
    if max_exponent <= p:
        raise ValueError("max_exponent must be larger than p")
    if candidate_bound < 1:
        raise ValueError("candidate_bound must be positive")

    attempt_count = 0
    for exponent in range(p + 1, max_exponent + 1):
        attempt_count += 1
        if not tau_equals_two(exponent):
            continue
        pressure = residue_return_pressure(exponent)
        if pressure["status"] == STATUS_RESIDUE_RETURN_DEFERRED:
            continue
        certificate = residue_return_boundary_certificate(pressure, candidate_bound)
        return {
            "rule_id": PGSMPG_RULE_ID,
            "p": p,
            "q": exponent,
            "max_exponent": max_exponent,
            "candidate_bound": candidate_bound,
            "attempt_count": attempt_count,
            "boundary_certificate": certificate,
            "used_forbidden_tool": False,
        }
    return None


def resolve_q(
    p: int,
    max_exponent: int = DEFAULT_MAX_EXPONENT,
    candidate_bound: int = DEFAULT_CANDIDATE_BOUND,
) -> tuple[int, str, dict[str, object]]:
    """Resolve the next PGSMPG exponent."""
    certificate = pgs_mersenne_prime_certificate(p, max_exponent, candidate_bound)
    if certificate is None:
        raise PGSMPGUnresolvedError(
            f"PGSMPG did not resolve p={int(p)} within max_exponent={int(max_exponent)}"
        )
    return int(certificate["q"]), PGSMPG_SOURCE, certificate


def emit_record(
    p: int,
    max_exponent: int = DEFAULT_MAX_EXPONENT,
    candidate_bound: int = DEFAULT_CANDIDATE_BOUND,
) -> dict[str, int]:
    """Emit one minimal PGSMPG record."""
    q, _source, _certificate = resolve_q(int(p), max_exponent, candidate_bound)
    return {
        "p": int(p),
        "q": q,
    }


def emit_records(
    anchors: list[int],
    max_exponent: int = DEFAULT_MAX_EXPONENT,
    candidate_bound: int = DEFAULT_CANDIDATE_BOUND,
) -> list[dict[str, int]]:
    """Emit one minimal record per accepted exponent."""
    return [
        emit_record(anchor, max_exponent, candidate_bound)
        for anchor in anchors
    ]
