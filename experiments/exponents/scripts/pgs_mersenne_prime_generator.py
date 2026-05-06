#!/usr/bin/env python3
"""PGSMPG v0.1 live generator."""

from __future__ import annotations

from sympy import divisor_count


DEFAULT_CANDIDATE_BOUND = 4096
DEFAULT_MAX_EXPONENT = 127
PGSMPG_VERSION = "0.1.0"
PGSMPG_FREEZE_ID = "pgs_mersenne_prime_generator_v0_1"
PGSMPG_SOURCE = "PGSMPG"
PGSMPG_RULE_ID = "pgsmpg_exponent_successor_v0_1"
PGSMPG_LEFT_BOUNDARY_RULE_ID = "pgsmpg_left_boundary_chamber_reset_v0_1"
WHEEL_OPEN_RESIDUES_MOD30 = frozenset({1, 7, 11, 13, 17, 19, 23, 29})
LOW_PRIMES = frozenset({2, 3, 5})
STATUS_EXPONENT_DIVISOR_COUNT_NOT_TWO = "exponent_divisor_count_not_two"
STATUS_BOUNDARY_REJECTED = "boundary_rejected"
STATUS_BOUNDARY_RESOLVED_SURVIVOR = "boundary_resolved_survivor"
STATUS_BOUNDARY_UNRESOLVED = "boundary_unresolved"
STATUS_MERSENNE_LOCATION_INFERRED = "mersenne_location_inferred"
STATUS_MERSENNE_LOCATION_NOT_INFERRED = "mersenne_location_not_inferred"


class PGSMPGUnresolvedError(RuntimeError):
    """Raised when PGSMPG does not resolve inside the configured surface."""


def tau(n: int) -> int:
    """Return exact divisor count."""
    return int(divisor_count(int(n)))


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
    small_power = 2**exponent if exponent <= 3 else None
    for offset in range(1, candidate_bound + 1):
        if (
            small_power is not None
            and small_power - offset in LOW_PRIMES
        ) or (power_residue_mod30 - offset) % 30 in WHEEL_OPEN_RESIDUES_MOD30:
            yield offset


def admissible_left_offsets(exponent: int, candidate_bound: int) -> list[int]:
    """Return wheel-open offsets to the left of one power of two."""
    return list(iter_admissible_left_offsets(exponent, candidate_bound))


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
    candidate_states: list[dict[str, object]] = []
    rejected_offsets: list[int] = []
    unresolved_offsets: list[int] = []
    carrier_offset: int | None = None
    carrier_d: int | None = None

    for offset in iter_admissible_left_offsets(exponent, candidate_bound):
        n = power_of_two - offset
        divisor_count_n = tau(n)
        if divisor_count_n > 2:
            status = STATUS_BOUNDARY_REJECTED
            rejected_offsets.append(offset)
            if carrier_d is None or divisor_count_n < carrier_d:
                carrier_offset = offset
                carrier_d = divisor_count_n
        else:
            status = STATUS_BOUNDARY_RESOLVED_SURVIVOR
        state = {
            "offset": offset,
            "candidate_bit_length": n.bit_length(),
            "divisor_count": divisor_count_n,
            "divisor_state": divisor_state_label(divisor_count_n),
            "status": status,
            "carrier_offset": carrier_offset,
            "carrier_d": carrier_d,
        }
        candidate_states.append(state)
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
                "candidate_states": candidate_states,
                "closed_offsets_before_boundary": rejected_offsets,
                "unresolved_offsets_before_boundary": unresolved_offsets,
                "active_count": len(candidate_states) - len(rejected_offsets),
                "resolved_count": 1,
                "unresolved_count": len(unresolved_offsets),
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
    exponent_d = tau(exponent)
    if exponent_d != 2:
        return {
            "exponent": exponent,
            "exponent_divisor_count": exponent_d,
            "status": STATUS_EXPONENT_DIVISOR_COUNT_NOT_TWO,
            "boundary_certificate": None,
            "distance_to_left_boundary": "",
            "mersenne_location_inferred": False,
        }

    certificate = left_boundary_state_certificate(exponent, candidate_bound)
    if certificate is None:
        return {
            "exponent": exponent,
            "exponent_divisor_count": exponent_d,
            "status": STATUS_BOUNDARY_UNRESOLVED,
            "boundary_certificate": None,
            "distance_to_left_boundary": "",
            "mersenne_location_inferred": False,
        }

    distance = int(certificate["distance_to_left_boundary"])
    inferred = distance == 1
    return {
        "exponent": exponent,
        "exponent_divisor_count": exponent_d,
        "status": (
            STATUS_MERSENNE_LOCATION_INFERRED
            if inferred
            else STATUS_MERSENNE_LOCATION_NOT_INFERRED
        ),
        "boundary_certificate": certificate,
        "distance_to_left_boundary": distance,
        "mersenne_location_inferred": inferred,
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

    attempts: list[dict[str, object]] = []
    for exponent in range(p + 1, max_exponent + 1):
        attempt = exponent_attempt_row(exponent, candidate_bound)
        attempts.append(attempt)
        if bool(attempt["mersenne_location_inferred"]):
            return {
                "rule_id": PGSMPG_RULE_ID,
                "p": p,
                "q": exponent,
                "max_exponent": max_exponent,
                "candidate_bound": candidate_bound,
                "attempt_count": len(attempts),
                "attempts": attempts,
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
