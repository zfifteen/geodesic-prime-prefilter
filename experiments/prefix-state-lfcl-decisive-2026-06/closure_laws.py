"""Pre-registered L_FCL closure laws L0–L4 (no q_ref / gap imports)."""

from __future__ import annotations

import math
from dataclasses import dataclass

from prefix_state import PrefixSnapshot, PrefixStateTracker


@dataclass(frozen=True)
class ClosureFire:
    law_id: str
    B_declare: int
    r_declare: int


LAW_IDS = ("L0", "L1", "L2", "L3", "L4")


def _try_l0(p: int, snap: PrefixSnapshot) -> ClosureFire | None:
    if snap.gwr_offset is None:
        return None
    return ClosureFire("L0", snap.B, p + snap.gwr_offset)


def _try_l1(p: int, snap: PrefixSnapshot) -> ClosureFire | None:
    if snap.threat_offset is None:
        return None
    if snap.threat_offset > snap.B:
        return None
    return ClosureFire("L1", snap.B, p + snap.threat_offset)


def _try_l2(p: int, snap: PrefixSnapshot) -> ClosureFire | None:
    if len(snap.admissible) != 1:
        return None
    return ClosureFire("L2", snap.B, p + snap.admissible[0])


def _try_l3(p: int, snap: PrefixSnapshot, gated: list[int]) -> ClosureFire | None:
    if snap.threat_offset is None:
        return None
    if len(gated) != 1:
        return None
    return ClosureFire("L3", snap.B, p + gated[0])


def _try_l4(p: int, snap: PrefixSnapshot) -> ClosureFire | None:
    if snap.gwr_offset is None or snap.gwr_tau is None:
        return None
    if snap.threat_offset is None:
        return None
    threshold = snap.gwr_tau * math.log(p + snap.gwr_offset)
    if snap.partial_budget < threshold:
        return None
    return ClosureFire("L4", snap.B, p + snap.threat_offset)


_LAW_TRY = {
    "L0": lambda p, snap, gated: _try_l0(p, snap),
    "L1": lambda p, snap, gated: _try_l1(p, snap),
    "L2": lambda p, snap, gated: _try_l2(p, snap),
    "L3": lambda p, snap, gated: _try_l3(p, snap, gated),
    "L4": lambda p, snap, gated: _try_l4(p, snap),
}


def first_fire_for_law(
    law_id: str,
    p: int,
    tau: list[int],
    prefix_bounds: list[int],
) -> ClosureFire | None:
    """Return first forced closure along ordered prefix bounds."""
    tracker = PrefixStateTracker(p, tau)
    try_fn = _LAW_TRY[law_id]
    for bound in prefix_bounds:
        snap = tracker.advance_to(bound)
        gated = tracker.threat_gated_admissible(bound)
        fire = try_fn(p, snap, gated)
        if fire is not None:
            return fire
    return None


def scan_all_laws(
    p: int,
    tau: list[int],
    prefix_bounds: list[int],
) -> dict[str, ClosureFire | None]:
    return {
        law_id: first_fire_for_law(law_id, p, tau, prefix_bounds)
        for law_id in LAW_IDS
    }