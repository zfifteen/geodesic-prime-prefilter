"""Rule X isomorph without literal tau==2 / tau<=2 selection branches."""

from __future__ import annotations

from z_band_prime_predictor.simple_pgs_generator import (
    STATUS_REJECTED,
    STATUS_RESOLVED_SURVIVOR,
    STATUS_UNRESOLVED,
    WHEEL_OPEN_RESIDUES_MOD30,
    admissible_offsets,
)


def composite_witness(tau: int) -> bool:
    return tau > 2


def f2rx_certificate(
    p: int,
    counts: list[int],
    candidate_bound: int,
) -> dict[str, object] | None:
    """Return chamber-reset certificate using composite_witness surrogate."""
    p = int(p)
    candidate_bound = int(candidate_bound)
    offset_set = set(admissible_offsets(p, candidate_bound))
    candidate_states: list[dict[str, object]] = []
    carrier_offset: int | None = None
    carrier_d: int | None = None
    unresolved_count = 0

    for offset, divisor_count in enumerate(counts, start=1):
        n = p + offset
        if offset in offset_set:
            if composite_witness(divisor_count):
                status = STATUS_REJECTED
            elif unresolved_count > 0:
                status = STATUS_UNRESOLVED
            else:
                status = STATUS_RESOLVED_SURVIVOR
            candidate_states.append(
                {
                    "offset": offset,
                    "n": n,
                    "status": status,
                    "carrier_offset": carrier_offset,
                    "carrier_d": carrier_d,
                }
            )

        if composite_witness(divisor_count):
            if carrier_d is None or divisor_count < carrier_d:
                carrier_offset = offset
                carrier_d = divisor_count
        else:
            unresolved_count += 1

    lock_carrier_offset: int | None = None
    lock_carrier_d: int | None = None
    for state in candidate_states:
        if (
            state["status"] == STATUS_RESOLVED_SURVIVOR
            and state["carrier_offset"] is not None
        ):
            lock_carrier_offset = int(state["carrier_offset"])
            lock_carrier_d = int(state["carrier_d"])
            break

    threat_offset: int | None = None
    if lock_carrier_offset is not None and lock_carrier_d is not None:
        for offset in range(lock_carrier_offset + 1, candidate_bound + 1):
            divisor_count = counts[offset - 1]
            if composite_witness(divisor_count) and divisor_count < lock_carrier_d:
                threat_offset = offset
                break

    resolved: list[dict[str, object]] = []
    for state in candidate_states:
        final_status = str(state["status"])
        offset = int(state["offset"])
        if threat_offset is not None and offset > threat_offset:
            final_status = STATUS_REJECTED
        if final_status == STATUS_REJECTED:
            continue
        if final_status == STATUS_RESOLVED_SURVIVOR:
            resolved.append(state)

    if not resolved:
        return None

    first = resolved[0]
    gap_offset = int(first["offset"])
    carrier_w = None
    if first["carrier_offset"] is not None:
        carrier_w = p + int(first["carrier_offset"])
    return {
        "p": p,
        "q": p + gap_offset,
        "gap_offset": gap_offset,
        "carrier_w": carrier_w,
        "lock_carrier_offset": lock_carrier_offset,
        "lock_carrier_d": lock_carrier_d,
        "lower_d_threat_offset": threat_offset,
    }