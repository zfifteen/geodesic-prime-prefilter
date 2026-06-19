"""Replay Rule X selection at sufficient bound; record selection-time semantics."""

from __future__ import annotations

from z_band_prime_composite_field import divisor_counts_segment
from z_band_prime_predictor.simple_pgs_generator import (
    STATUS_REJECTED,
    STATUS_RESOLVED_SURVIVOR,
    STATUS_UNRESOLVED,
    WHEEL_OPEN_RESIDUES_MOD30,
    admissible_offsets,
)


def composite_witness(divisor_count: int) -> bool:
    return divisor_count > 2


def replay_selection_at_bound(p: int, bound: int) -> dict[str, object] | None:
    """Replay production Rule X; return selection record at resolved offset."""
    p = int(p)
    bound = int(bound)
    counts = [int(v) for v in divisor_counts_segment(p + 1, p + bound + 1)]
    offset_set = set(admissible_offsets(p, bound))
    carrier_offset: int | None = None
    carrier_d: int | None = None
    unresolved_count = 0
    selection_records: list[dict[str, object]] = []

    for offset, divisor_count in enumerate(counts, start=1):
        if offset in offset_set:
            if composite_witness(divisor_count):
                status = STATUS_REJECTED
            elif unresolved_count > 0:
                status = STATUS_UNRESOLVED
            else:
                status = STATUS_RESOLVED_SURVIVOR
            selection_records.append(
                {
                    "offset": offset,
                    "status": status,
                    "composite_witness_at_selection": composite_witness(divisor_count),
                    "unresolved_wheel_open_before": unresolved_count,
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
    for record in selection_records:
        if (
            record["status"] == STATUS_RESOLVED_SURVIVOR
            and carrier_offset is not None
        ):
            lock_carrier_offset = carrier_offset
            lock_carrier_d = carrier_d
            break

    threat_offset: int | None = None
    if lock_carrier_offset is not None and lock_carrier_d is not None:
        for offset in range(lock_carrier_offset + 1, bound + 1):
            divisor_count = counts[offset - 1]
            if composite_witness(divisor_count) and divisor_count < lock_carrier_d:
                threat_offset = offset
                break

    resolved: list[dict[str, object]] = []
    for record in selection_records:
        offset = int(record["offset"])
        final_status = str(record["status"])
        if threat_offset is not None and offset > threat_offset:
            final_status = STATUS_REJECTED
        if final_status == STATUS_RESOLVED_SURVIVOR:
            resolved.append({**record, "final_status": final_status})

    if not resolved:
        return None

    first = resolved[0]
    return {
        "gap_offset": int(first["offset"]),
        "q": p + int(first["offset"]),
        "resolved_count": len(resolved),
        "selection_record": first,
        "lock_carrier_offset": lock_carrier_offset,
        "lower_d_threat_offset": threat_offset,
        "used_composite_witness_only": not bool(first["composite_witness_at_selection"]),
        "wheel_open": (p + int(first["offset"])) % 30 in WHEEL_OPEN_RESIDUES_MOD30,
    }