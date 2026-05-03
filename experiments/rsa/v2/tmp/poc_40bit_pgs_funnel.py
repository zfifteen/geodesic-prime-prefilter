#!/usr/bin/env python3
"""Temporary 40-bit PGS factorizer funnel prototype."""

from __future__ import annotations

import json
import sys
from dataclasses import dataclass
from pathlib import Path

import gmpy2


ROOT = Path(__file__).resolve().parents[4]
SOURCE_DIR = ROOT / "src" / "python"
if str(SOURCE_DIR) not in sys.path:
    sys.path.insert(0, str(SOURCE_DIR))

from z_band_prime_composite_field import divisor_counts_segment  # noqa: E402
from z_band_prime_predictor.simple_pgs_generator import (  # noqa: E402
    pgs_chamber_reset_state_certificate,
)


CASE_ID = "rsa_v2_40bit_static_001"
PUBLIC_N = gmpy2.mpz(1099507433251)
BITS = 40
RADIUS = gmpy2.mpz(1024)
BALANCE_BAND = gmpy2.mpz(2)
PGS_ENDPOINT_RADIUS = 16
RULE_X_CANDIDATE_BOUND = 128
RECURSIVE_DEPTH = 4
WHEEL_OPEN_RESIDUES_MOD30 = frozenset({1, 7, 11, 13, 17, 19, 23, 29})


@dataclass(frozen=True)
class CandidateRow:
    """One lower-side candidate and its public reciprocal coordinate."""

    x: gmpy2.mpz
    y: gmpy2.mpz


@dataclass(frozen=True)
class LocalLock:
    """One local PGSPG endpoint lock result."""

    value: gmpy2.mpz
    nearest_endpoint: gmpy2.mpz | None
    nearest_endpoint_distance: int | None
    previous_endpoint: gmpy2.mpz | None
    reset_endpoint: gmpy2.mpz | None
    reset_gap_offset: int | None
    active_count: int | None
    resolved_count: int | None
    unresolved_count: int | None
    carrier_w: gmpy2.mpz | None
    carrier_d: int | None
    lock_carrier_offset: int | None
    lock_carrier_d: int | None
    lower_d_threat_offset: int | None
    tail_after_reset_offsets: tuple[int, ...]
    reset_deadline_kind: str | None
    reset_deadline_offset: int | None
    reset_deadline_value: gmpy2.mpz | None
    reset_deadline_margin: int | None
    reset_signature: str | None
    locked: bool


@dataclass(frozen=True)
class SurvivorRow:
    """One survivor after local PGS checks and recursive reciprocal lock."""

    rank: int
    x: gmpy2.mpz
    y: gmpy2.mpz
    lower_lock: LocalLock
    upper_lock: LocalLock
    recursive_rounds_locked: int
    deadline_locked: bool
    deadline_lock_reason: str
    lower_transported_deadline_width: int | None
    upper_transported_deadline_width: int | None
    product_closed: bool
    product_error: gmpy2.mpz


def mpz_to_int(value: gmpy2.mpz) -> int:
    """Convert one GMP integer to a Python integer for existing PGSPG helpers."""
    return int(value)


def write_json(path: Path, payload: dict[str, object]) -> None:
    """Write one LF-terminated JSON object."""
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")


def write_jsonl(path: Path, rows: list[dict[str, object]]) -> None:
    """Write LF-delimited JSON rows."""
    with path.open("w", newline="\n") as handle:
        for row in rows:
            handle.write(json.dumps(row, sort_keys=True))
            handle.write("\n")


def wheel_open(value: gmpy2.mpz) -> bool:
    """Return whether one integer sits in a residue class open to primes."""
    return int(value % 30) in WHEEL_OPEN_RESIDUES_MOD30


def candidate_band(n_value: gmpy2.mpz, radius: gmpy2.mpz) -> list[gmpy2.mpz]:
    """Return the full public chamber around the integer square root of `N`."""
    # The integer square root gives the public center of the semiprime chamber.
    center = gmpy2.isqrt(n_value)
    # The radius defines the lower side of the public search interval.
    lower = center - radius
    # The same radius defines the upper side of the public search interval.
    upper = center + radius
    return [lower + offset for offset in range(mpz_to_int(upper - lower) + 1)]


def balance_bounds(center: gmpy2.mpz, band: gmpy2.mpz) -> tuple[gmpy2.mpz, gmpy2.mpz]:
    """Return the public balance interval around the square-root center."""
    # Division by the balance band gives the smallest accepted balanced factor.
    lower = center // band
    # Multiplication by the balance band gives the largest accepted balanced factor.
    upper = center * band
    return lower, upper


def reciprocal_floor(n_value: gmpy2.mpz, x_value: gmpy2.mpz) -> gmpy2.mpz:
    """Return the public upper coordinate implied by one lower candidate."""
    # The reciprocal floor maps a lower candidate to its public cofactor side.
    return n_value // x_value


def public_candidate_funnel(n_value: gmpy2.mpz) -> tuple[list[CandidateRow], dict[str, int]]:
    """Apply public balance, wheel, and reciprocal-window filters."""
    # The integer square root fixes the center used by both balance and chamber checks.
    center = gmpy2.isqrt(n_value)
    lower_balance, upper_balance = balance_bounds(center, BALANCE_BAND)
    candidates = candidate_band(n_value, RADIUS)
    post_balance: list[gmpy2.mpz] = []
    post_wheel: list[CandidateRow] = []
    reciprocal_window: list[CandidateRow] = []

    for x_value in candidates:
        if not lower_balance <= x_value <= upper_balance:
            continue
        post_balance.append(x_value)

        if not wheel_open(x_value):
            continue

        y_value = reciprocal_floor(n_value, x_value)
        if not lower_balance <= y_value <= upper_balance:
            continue

        if not wheel_open(y_value):
            continue
        post_wheel.append(CandidateRow(x_value, y_value))

        if center - RADIUS <= y_value <= center + RADIUS:
            reciprocal_window.append(CandidateRow(x_value, y_value))

    return reciprocal_window, {
        "initial_candidate_integers": len(candidates),
        "post_balance_candidates": len(post_balance),
        "post_wheel_candidates": len(post_wheel),
        "reciprocal_window_candidates": len(reciprocal_window),
    }


def nearest_endpoint(value: gmpy2.mpz, radius: int) -> tuple[gmpy2.mpz | None, int | None]:
    """Return the nearest divisor-count endpoint in a small local chamber."""
    # The local chamber starts a fixed distance to the left of the candidate.
    lo = max(2, mpz_to_int(value) - radius)
    # The local chamber ends a fixed distance to the right of the candidate.
    hi = mpz_to_int(value) + radius + 1
    counts = divisor_counts_segment(lo, hi)
    endpoints = [
        gmpy2.mpz(lo + offset)
        for offset, divisor_count in enumerate(counts)
        if int(divisor_count) == 2
    ]
    if not endpoints:
        return None, None
    # The nearest endpoint checks whether the candidate is itself locally endpoint-stable.
    endpoint = min(endpoints, key=lambda item: (abs(mpz_to_int(item - value)), mpz_to_int(item)))
    return endpoint, abs(mpz_to_int(endpoint - value))


def previous_endpoint(value: gmpy2.mpz, chamber_bound: int) -> gmpy2.mpz | None:
    """Return the nearest previous divisor-count endpoint below one value."""
    hi = mpz_to_int(value)
    while hi > 2:
        # The backward chunk asks for the previous endpoint without using `N`.
        lo = max(2, hi - chamber_bound)
        counts = divisor_counts_segment(lo, hi)
        for offset in range(len(counts) - 1, -1, -1):
            if int(counts[offset]) == 2:
                return gmpy2.mpz(lo + offset)
        hi = lo
    return None


def chamber_reset_certificate(anchor: gmpy2.mpz) -> dict[str, object] | None:
    """Return the PGSPG chamber-reset certificate after one previous endpoint."""
    certificate = pgs_chamber_reset_state_certificate(
        mpz_to_int(anchor),
        RULE_X_CANDIDATE_BOUND,
    )
    if certificate is None:
        return None
    return certificate


def local_lock(value: gmpy2.mpz) -> LocalLock:
    """Return whether one value is stable under local PGSPG chamber logic."""
    endpoint, distance = nearest_endpoint(value, PGS_ENDPOINT_RADIUS)
    anchor = previous_endpoint(value, RULE_X_CANDIDATE_BOUND)
    certificate = None if anchor is None else chamber_reset_certificate(anchor)
    reset = None if certificate is None else gmpy2.mpz(int(certificate["q"]))
    locked = endpoint == value and distance == 0 and reset == value
    carrier_w = None
    if certificate is not None and certificate["carrier_w"] is not None:
        carrier_w = gmpy2.mpz(int(certificate["carrier_w"]))
    tail_offsets = (
        ()
        if certificate is None
        else tuple(int(offset) for offset in certificate["tail_after_reset_offsets"])
    )
    reset_gap = None if certificate is None else int(certificate["gap_offset"])
    threat_offset = (
        None
        if certificate is None or certificate["lower_d_threat_offset"] is None
        else int(certificate["lower_d_threat_offset"])
    )
    deadline_options: list[tuple[int, str]] = []
    if tail_offsets:
        deadline_options.append((tail_offsets[0], "tail"))
    if threat_offset is not None:
        deadline_options.append((threat_offset, "threat"))
    if not deadline_options and reset_gap is not None:
        deadline_options.append((RULE_X_CANDIDATE_BOUND, "bound"))
    deadline_offset = None
    deadline_kind = None
    if deadline_options:
        deadline_offset, deadline_kind = min(deadline_options)
    deadline_value = None
    if anchor is not None and deadline_offset is not None:
        # The reset deadline value is the first local state boundary after the reset endpoint.
        deadline_value = anchor + deadline_offset
    deadline_margin = None
    if reset_gap is not None and deadline_offset is not None:
        # The reset margin is the local distance from the reset endpoint to the next state boundary.
        deadline_margin = deadline_offset - reset_gap
    signature = None
    if certificate is not None:
        signature = (
            f"carrier_d={certificate['carrier_d']};"
            f"lock_carrier_d={certificate['lock_carrier_d']};"
            f"threat={threat_offset is not None};"
            f"deadline={deadline_kind}"
        )
    return LocalLock(
        value=value,
        nearest_endpoint=endpoint,
        nearest_endpoint_distance=distance,
        previous_endpoint=anchor,
        reset_endpoint=reset,
        reset_gap_offset=reset_gap,
        active_count=None if certificate is None else int(certificate["active_count"]),
        resolved_count=None if certificate is None else int(certificate["resolved_count"]),
        unresolved_count=None if certificate is None else int(certificate["unresolved_count"]),
        carrier_w=carrier_w,
        carrier_d=None if certificate is None or certificate["carrier_d"] is None else int(certificate["carrier_d"]),
        lock_carrier_offset=None if certificate is None or certificate["lock_carrier_offset"] is None else int(certificate["lock_carrier_offset"]),
        lock_carrier_d=None if certificate is None or certificate["lock_carrier_d"] is None else int(certificate["lock_carrier_d"]),
        lower_d_threat_offset=threat_offset,
        tail_after_reset_offsets=tail_offsets,
        reset_deadline_kind=deadline_kind,
        reset_deadline_offset=deadline_offset,
        reset_deadline_value=deadline_value,
        reset_deadline_margin=deadline_margin,
        reset_signature=signature,
        locked=bool(locked),
    )


def recursive_lock_rounds(n_value: gmpy2.mpz, x_value: gmpy2.mpz, y_value: gmpy2.mpz) -> int:
    """Return how many reciprocal PGSPG lock rounds one pair survives."""
    rounds_locked = 0
    current_x = x_value
    current_y = y_value

    for _round_index in range(1, RECURSIVE_DEPTH + 1):
        lower = local_lock(current_x)
        upper = local_lock(current_y)
        if not (lower.locked and upper.locked):
            break

        # The lower side transported through the upper endpoint must return to the lower endpoint.
        transported_x = n_value // upper.reset_endpoint
        # The upper side transported through the lower endpoint must return to the upper endpoint.
        transported_y = n_value // lower.reset_endpoint
        if transported_x != lower.reset_endpoint or transported_y != upper.reset_endpoint:
            break

        rounds_locked += 1
        current_x = lower.reset_endpoint
        current_y = upper.reset_endpoint

    return rounds_locked


def transported_deadline_width(n_value: gmpy2.mpz, lock: LocalLock) -> int | None:
    """Return how wide one reset interval becomes under the reciprocal map."""
    if lock.reset_endpoint is None or lock.reset_deadline_value is None:
        return None
    # The reciprocal map sends the reset endpoint to the opposite-side candidate.
    reset_image = n_value // lock.reset_endpoint
    # The reciprocal map sends the reset deadline to the opposite-side deadline image.
    deadline_image = n_value // lock.reset_deadline_value
    return abs(mpz_to_int(reset_image - deadline_image))


def deadline_lock(
    n_value: gmpy2.mpz,
    lower: LocalLock,
    upper: LocalLock,
) -> tuple[bool, str, int | None, int | None]:
    """Return whether two local reset states form a reciprocal deadline lock."""
    lower_width = transported_deadline_width(n_value, lower)
    upper_width = transported_deadline_width(n_value, upper)
    if lower.reset_signature != upper.reset_signature:
        return False, "reset_signature_mismatch", lower_width, upper_width
    if lower.reset_deadline_margin != upper.reset_deadline_margin:
        return False, "reset_deadline_margin_mismatch", lower_width, upper_width
    if lower_width is None or upper_width is None:
        return False, "transported_deadline_missing", lower_width, upper_width
    if abs(lower_width - upper_width) > 1:
        return False, "transported_deadline_width_mismatch", lower_width, upper_width
    return True, "reciprocal_deadline_lock", lower_width, upper_width


def survivor_rows(n_value: gmpy2.mpz) -> tuple[list[SurvivorRow], dict[str, int]]:
    """Return survivor rows and public funnel counts for the 40-bit probe."""
    candidates, counts = public_candidate_funnel(n_value)
    survivors: list[SurvivorRow] = []

    for row in candidates:
        lower = local_lock(row.x)
        upper = local_lock(row.y)
        if not (lower.locked and upper.locked):
            continue

        rounds = recursive_lock_rounds(n_value, row.x, row.y)
        if rounds != RECURSIVE_DEPTH:
            continue

        deadline_ok, deadline_reason, lower_width, upper_width = deadline_lock(
            n_value,
            lower,
            upper,
        )
        # Product closure is evaluated only after the pair survived PGS contraction.
        product = row.x * row.y
        # Product error measures the remaining distance from public certification.
        product_error = abs(n_value - product)
        survivors.append(
            SurvivorRow(
                rank=0,
                x=row.x,
                y=row.y,
                lower_lock=lower,
                upper_lock=upper,
                recursive_rounds_locked=rounds,
                deadline_locked=deadline_ok,
                deadline_lock_reason=deadline_reason,
                lower_transported_deadline_width=lower_width,
                upper_transported_deadline_width=upper_width,
                product_closed=product == n_value,
                product_error=product_error,
            )
        )

    # The square-root distance ranking keeps the survivor ordering deterministic.
    center = gmpy2.isqrt(n_value)
    ranked = sorted(survivors, key=lambda item: (abs(mpz_to_int(item.x - center)), mpz_to_int(item.x)))
    ranked = [
        SurvivorRow(
            rank=index,
            x=row.x,
            y=row.y,
            lower_lock=row.lower_lock,
            upper_lock=row.upper_lock,
            recursive_rounds_locked=row.recursive_rounds_locked,
            deadline_locked=row.deadline_locked,
            deadline_lock_reason=row.deadline_lock_reason,
            lower_transported_deadline_width=row.lower_transported_deadline_width,
            upper_transported_deadline_width=row.upper_transported_deadline_width,
            product_closed=row.product_closed,
            product_error=row.product_error,
        )
        for index, row in enumerate(ranked, start=1)
    ]
    return ranked, counts


def survivor_to_json(row: SurvivorRow) -> dict[str, object]:
    """Return one survivor row as plain JSON values."""
    # Product closure is reported here after PGS contraction, not used to admit the survivor.
    product_closed = row.product_closed
    return {
        "case_id": CASE_ID,
        "rank": row.rank,
        "x": str(row.x),
        "y": str(row.y),
        "lower_previous_endpoint": None if row.lower_lock.previous_endpoint is None else str(row.lower_lock.previous_endpoint),
        "lower_reset_endpoint": None if row.lower_lock.reset_endpoint is None else str(row.lower_lock.reset_endpoint),
        "lower_reset_gap_offset": row.lower_lock.reset_gap_offset,
        "lower_active_count": row.lower_lock.active_count,
        "lower_resolved_count": row.lower_lock.resolved_count,
        "lower_unresolved_count": row.lower_lock.unresolved_count,
        "lower_carrier_w": None if row.lower_lock.carrier_w is None else str(row.lower_lock.carrier_w),
        "lower_carrier_d": row.lower_lock.carrier_d,
        "lower_lock_carrier_offset": row.lower_lock.lock_carrier_offset,
        "lower_lock_carrier_d": row.lower_lock.lock_carrier_d,
        "lower_d_threat_offset": row.lower_lock.lower_d_threat_offset,
        "lower_tail_after_reset_offsets": list(row.lower_lock.tail_after_reset_offsets),
        "lower_reset_deadline_kind": row.lower_lock.reset_deadline_kind,
        "lower_reset_deadline_offset": row.lower_lock.reset_deadline_offset,
        "lower_reset_deadline_value": None if row.lower_lock.reset_deadline_value is None else str(row.lower_lock.reset_deadline_value),
        "lower_reset_deadline_margin": row.lower_lock.reset_deadline_margin,
        "lower_reset_signature": row.lower_lock.reset_signature,
        "lower_transported_deadline_width": row.lower_transported_deadline_width,
        "upper_previous_endpoint": None if row.upper_lock.previous_endpoint is None else str(row.upper_lock.previous_endpoint),
        "upper_reset_endpoint": None if row.upper_lock.reset_endpoint is None else str(row.upper_lock.reset_endpoint),
        "upper_reset_gap_offset": row.upper_lock.reset_gap_offset,
        "upper_active_count": row.upper_lock.active_count,
        "upper_resolved_count": row.upper_lock.resolved_count,
        "upper_unresolved_count": row.upper_lock.unresolved_count,
        "upper_carrier_w": None if row.upper_lock.carrier_w is None else str(row.upper_lock.carrier_w),
        "upper_carrier_d": row.upper_lock.carrier_d,
        "upper_lock_carrier_offset": row.upper_lock.lock_carrier_offset,
        "upper_lock_carrier_d": row.upper_lock.lock_carrier_d,
        "upper_d_threat_offset": row.upper_lock.lower_d_threat_offset,
        "upper_tail_after_reset_offsets": list(row.upper_lock.tail_after_reset_offsets),
        "upper_reset_deadline_kind": row.upper_lock.reset_deadline_kind,
        "upper_reset_deadline_offset": row.upper_lock.reset_deadline_offset,
        "upper_reset_deadline_value": None if row.upper_lock.reset_deadline_value is None else str(row.upper_lock.reset_deadline_value),
        "upper_reset_deadline_margin": row.upper_lock.reset_deadline_margin,
        "upper_reset_signature": row.upper_lock.reset_signature,
        "upper_transported_deadline_width": row.upper_transported_deadline_width,
        "recursive_rounds_locked": row.recursive_rounds_locked,
        "deadline_locked": row.deadline_locked,
        "deadline_lock_reason": row.deadline_lock_reason,
        "product_closed": product_closed,
        "product_error": str(row.product_error),
    }


def main() -> int:
    """Run the temporary 40-bit PGS funnel prototype."""
    output_dir = Path(__file__).resolve().parent / "output_40bit_pgs_funnel"
    output_dir.mkdir(parents=True, exist_ok=True)

    survivors, counts = survivor_rows(PUBLIC_N)
    deadline_locked = [row for row in survivors if row.deadline_locked]
    deadline_locked_pairs = {tuple(sorted((str(row.x), str(row.y)))) for row in deadline_locked}
    product_closed = [row for row in survivors if row.product_closed]
    product_closed_pairs = {tuple(sorted((str(row.x), str(row.y)))) for row in product_closed}
    unordered_survivor_pairs = {tuple(sorted((str(row.x), str(row.y)))) for row in survivors}
    summary = {
        "case_id": CASE_ID,
        "bits": BITS,
        "N": str(PUBLIC_N),
        "radius": str(RADIUS),
        "balance_band": str(BALANCE_BAND),
        **counts,
        "pgs_chamber_survivors": len(survivors),
        "recursive_lock_survivors": len(survivors),
        "deadline_lock_ordered_rows": len(deadline_locked),
        "deadline_lock_pairs": len(deadline_locked_pairs),
        "ordered_survivors": len(survivors),
        "unordered_survivors": len(unordered_survivor_pairs),
        "product_closed_ordered_rows": len(product_closed),
        "product_closed_pairs": len(product_closed_pairs),
        "status": "resolved" if len(deadline_locked_pairs) == 1 else "unresolved",
    }

    write_json(output_dir / "summary.json", summary)
    write_jsonl(output_dir / "survivor_rows.jsonl", [survivor_to_json(row) for row in survivors])
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
