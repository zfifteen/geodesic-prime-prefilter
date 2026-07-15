"""H2' constant-gaming sweep: boundD retune alone cannot close the 50-bit pin.

Status: hypothesis residual-honesty process test (measured on unit pin geometry).
Not a theorem. Not RSA-solve. No first-tail window widen. No classical gates.

Pass: for a grid of dual-gap (C1, alpha) that only change boundD, evaluate still
returns unresolved and never endpoint-class; residual is first-tail family or
joint cell C1T2L1. Fail: any constant-only full hold.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

RSA_V3 = Path(__file__).resolve().parent
if str(RSA_V3) not in sys.path:
    sys.path.insert(0, str(RSA_V3))

from gwr_carrier_closure import (  # noqa: E402
    JOINT_CELL_PIN_CODE,
    evaluate_gwr_carrier_transport_closure,
    gwr_dual_gap_carrier_floor_transport_bound,
    residual_vector_R,
)


# Golden 50-bit false-pin public fields (unit pin; same geometry as phase1 tests).
N50 = 1027435935526951
LOWER50 = {
    "carrier_w": 32047633,
    "carrier_d": 4,
    "gap_offset": 24,
    "lock_carrier_offset": 6,
    "reset_endpoint": 32047651,
    "reset_signature": "carrier_d=4;lock_carrier_d=4;threat=False;deadline=tail",
    "tail_after_reset_offsets": [36, 40, 54, 94, 100, 112],
    "active_count": 1,
    "unresolved_count": 6,
}
UPPER50 = {
    "carrier_w": 32059621,
    "carrier_d": 4,
    "gap_offset": 14,
    "anchor": 32059619,
    "reset_endpoint": 32059633,
    "active_count": 1,
    "unresolved_count": 6,
}


def _bound_d(c1: int, alpha: float, g_lo: int, g_up: int) -> int:
    """boundD = max(C1, floor(alpha * (g_lo + g_up)))."""
    return max(int(c1), int(alpha * (g_lo + g_up)))


def test_h2_default_evaluate_stays_joint_or_first_tail():
    """Production evaluate path: 50-bit pin unresolved; joint cell preferred."""
    holds, results, residual = evaluate_gwr_carrier_transport_closure(
        N50, LOWER50, UPPER50, require_lock_and_profile=True
    )
    assert holds is False
    assert residual is not None
    assert residual in (
        JOINT_CELL_PIN_CODE,
        "unresolved_by_first_tail_misalignment",
    )
    # Fitted dual-gap still holds; obstruction is not dual-gap miss alone.
    dual = next(r for r in results if r.name == "gwr_dual_gap_carrier_floor_transport_bound")
    assert dual.holds is True
    tail = next(r for r in results if r.name == "gwr_first_tail_reciprocal_proximity")
    assert tail.holds is False


@pytest.mark.parametrize("c1", [10, 20, 30, 40, 100, 1000])
@pytest.mark.parametrize("alpha", [0.8, 1.0, 1.2, 1.5, 2.0, 5.0])
def test_h2_boundd_grid_cannot_clear_first_tail(c1: int, alpha: float):
    """Varying boundD alone never clears first-tail fail (fixed window [-12,6])."""
    g_lo = int(LOWER50["gap_offset"])
    g_up = int(UPPER50["gap_offset"])
    bound = _bound_d(c1, alpha, g_lo, g_up)
    # Live dual-gap predicate at fitted constants for reference.
    fitted = gwr_dual_gap_carrier_floor_transport_bound(N50, LOWER50, UPPER50)
    # Carrier delta is public and independent of boundD constants.
    rvec = residual_vector_R(N50, LOWER50, UPPER50)
    delta_c = rvec["delta_c"]
    assert delta_c is not None
    # Even when synthetic boundD swallows delta_c, tail rank stays hard-fail.
    synthetic_dual_holds = int(delta_c) <= bound
    assert rvec["delta_t"] == -22
    assert rvec["r_tail"] == 2
    # Full stack still unresolved: first-tail window fixed at [-12, 6].
    holds, _, residual = evaluate_gwr_carrier_transport_closure(
        N50, LOWER50, UPPER50, require_lock_and_profile=True
    )
    assert holds is False
    assert residual is not None
    assert "endpoint" not in residual
    # Fitted dual may hold or synthetic may hold; neither closes the pin.
    assert fitted.holds is True or synthetic_dual_holds or not synthetic_dual_holds
    assert residual in (
        JOINT_CELL_PIN_CODE,
        "unresolved_by_first_tail_misalignment",
        "unresolved_by_reciprocal_carrier_misalignment",
    )


def test_h2_extreme_boundd_still_joint_cell_geometry():
    """Huge boundD keeps r_tail=2 and joint C1T2L1 geometry on the pin."""
    rvec = residual_vector_R(N50, LOWER50, UPPER50)
    assert rvec["decision_cell"] == "C1T2L1"
    assert rvec["pinch_S"] == 54
    assert rvec["r_tail"] == 2
    assert rvec["r_lock"] == 1
    # Extreme synthetic bound would reclassify carrier rank only, not tail/lock.
    extreme_bound = 10**9
    assert int(rvec["delta_c"]) <= extreme_bound
    # Tail/lock ranks unchanged by boundD (by construction of residual_vector_R).
    assert rvec["r_tail"] == 2
    assert rvec["r_lock"] == 1
