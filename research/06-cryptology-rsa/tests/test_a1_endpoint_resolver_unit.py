"""A1 unit tests: GWR predicates, residual taxonomy, certificate hash (UT)."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

V3 = Path(__file__).resolve().parents[1] / "experiments" / "live-solver" / "rsa-v3"
sys.path.insert(0, str(V3))

from gwr_carrier_closure import (  # noqa: E402
    evaluate_gwr_carrier_transport_closure,
    gwr_carrier_fields_present,
    gwr_carrier_floor_transport_within_gap_bound,
    gwr_dual_gap_carrier_floor_transport_bound,
    gwr_lower_lock_dominance,
    gwr_matched_profile_counts,
    is_historical_false_endpoint_class,
    residual_component_ledger,
)
from residual import TAXONOMY, build_residual_row, is_known_residual  # noqa: E402
from structural_certificate import (  # noqa: E402
    ALGORITHM_VERSION,
    RULE_ID,
    build_structural_certificate,
    content_hash,
)


def test_tp_ut_006_gwr_carrier_fields_present():
    assert gwr_carrier_fields_present(None, {}).holds is False
    lower = {"carrier_w": "10", "carrier_d": 4}
    upper = {"carrier_w": "20", "carrier_d": 4}
    assert gwr_carrier_fields_present(lower, upper).holds is True


def test_tp_ut_006_gwr_carrier_floor_transport_bound():
    lower = {"carrier_w": 100, "carrier_d": 4, "gap_offset": 10}
    upper = {"carrier_w": 100, "carrier_d": 4, "gap_offset": 10}
    ok = gwr_carrier_floor_transport_within_gap_bound(100 * 100, lower, upper)
    assert ok.holds is True
    far = gwr_carrier_floor_transport_within_gap_bound(100 * 1000, lower, upper)
    assert far.holds is False


def test_tp_ut_006_dual_gap_discriminator_d_arithmetic():
    """Pin arithmetic for D: dual-gap bound on the measured 50-bit miss shape."""
    # Synthetic match of live residual geometry: delta=30, g_lo=24, g_up=14.
    # boundD = max(20, (6*(24+14))//5) = 45; 30 <= 45 so D holds.
    lower = {"carrier_w": 1000, "carrier_d": 4, "gap_offset": 24}
    upper = {"carrier_w": 1000, "carrier_d": 4, "gap_offset": 14}
    # floor(N/1000)=1030 => delta=30
    n_value = 1000 * 1030
    dual = gwr_dual_gap_carrier_floor_transport_bound(n_value, lower, upper)
    assert dual.holds is True
    assert "boundD=45" in dual.detail
    assert "delta=30" in dual.detail
    assert "g_lo=24" in dual.detail
    assert "g_up=14" in dual.detail
    legacy = gwr_carrier_floor_transport_within_gap_bound(n_value, lower, upper)
    assert legacy.holds is False
    assert "bound=28" in legacy.detail

    # Dual-gap still fails when miss exceeds dual bound.
    upper_far = {"carrier_w": 1000, "carrier_d": 4, "gap_offset": 14}
    n_far = 1000 * 1100  # delta=100 > boundD=45
    dual_far = gwr_dual_gap_carrier_floor_transport_bound(n_far, lower, upper_far)
    assert dual_far.holds is False


def test_tp_ut_006_lock_and_profile():
    lower = {
        "lock_carrier_offset": 8,
        "gap_offset": 10,
        "active_count": 2,
        "unresolved_count": 1,
    }
    upper = {"active_count": 2, "unresolved_count": 1}
    assert gwr_lower_lock_dominance(lower).holds is True
    assert gwr_matched_profile_counts(lower, upper).holds is True
    upper_bad = {"active_count": 3, "unresolved_count": 1}
    assert gwr_matched_profile_counts(lower, upper_bad).holds is False


def test_tp_ut_006_stack_returns_residual_code():
    lower = {
        "carrier_w": 100,
        "carrier_d": 4,
        "gap_offset": 5,
        "reset_endpoint": 10,
        "anchor": 9,
        "reset_signature": "x",
    }
    upper = {
        "carrier_w": 99999,
        "carrier_d": 4,
        "gap_offset": 5,
        "anchor": 9,
        "reset_endpoint": 20,
        "active_count": 1,
        "unresolved_count": 0,
    }
    holds, results, residual = evaluate_gwr_carrier_transport_closure(
        100 * 100,
        lower,
        upper,
        require_lock_and_profile=False,
    )
    assert holds is False
    assert residual == "unresolved_by_reciprocal_carrier_misalignment"
    assert any(r.name == "gwr_dual_gap_carrier_floor_transport_bound" for r in results)
    assert any(r.name == "gwr_carrier_floor_transport_within_gap_bound" for r in results)


def test_tp_ut_006_stack_migrates_when_dual_gap_holds_but_lock_fails():
    """Outcome-B shape: D holds; lock dominance fails under require_lock."""
    lower = {
        "carrier_w": 1000,
        "carrier_d": 4,
        "gap_offset": 24,
        "lock_carrier_offset": 6,
        "reset_endpoint": 1000,
        "anchor": 999,
        "reset_signature": "carrier_d=4;deadline=tail",
        "tail_after_reset_offsets": [12],
        "active_count": 1,
        "unresolved_count": 1,
    }
    upper = {
        "carrier_w": 1030,
        "carrier_d": 4,
        "gap_offset": 14,
        "anchor": 1020,
        "reset_endpoint": 1034,
        "active_count": 1,
        "unresolved_count": 1,
    }
    n_value = 1000 * 1030  # dual-gap holds (delta=0 after match of transport to 1030)
    # Force exact transport match: floor(N/1000)=1030
    holds, results, residual = evaluate_gwr_carrier_transport_closure(
        n_value,
        lower,
        upper,
        require_lock_and_profile=True,
    )
    assert holds is False
    assert residual == "unresolved_by_lower_lock_misalignment"
    dual = next(r for r in results if r.name == "gwr_dual_gap_carrier_floor_transport_bound")
    assert dual.holds is True
    lock = next(r for r in results if r.name == "gwr_lower_lock_dominance")
    assert lock.holds is False


def test_phase1_joint_diagnostics_50bit_pin_geometry():
    """Phase-1: full component ledger on measured 50-bit residual geometry.

    Decision residual remains first-tail, but lock failure is still visible in
    diagnostics when require_lock is true (co-primary honesty).
    """
    n_value = 1027435935526951
    lower = {
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
    upper = {
        "carrier_w": 32059621,
        "carrier_d": 4,
        "gap_offset": 14,
        "anchor": 32059619,
        "reset_endpoint": 32059633,
        "active_count": 1,
        "unresolved_count": 6,
    }
    holds, results, residual = evaluate_gwr_carrier_transport_closure(
        n_value,
        lower,
        upper,
        require_lock_and_profile=True,
    )
    assert holds is False
    assert residual == "unresolved_by_first_tail_misalignment"
    by_name = {r.name: r for r in results}
    assert by_name["gwr_dual_gap_carrier_floor_transport_bound"].holds is True
    assert "delta=30" in by_name["gwr_dual_gap_carrier_floor_transport_bound"].detail
    assert "boundD=45" in by_name["gwr_dual_gap_carrier_floor_transport_bound"].detail
    assert by_name["gwr_first_tail_reciprocal_proximity"].holds is False
    assert "delta=-22" in by_name["gwr_first_tail_reciprocal_proximity"].detail
    # Lock co-primary: evaluated even though first-tail decided residual.
    assert "gwr_lower_lock_dominance" in by_name
    assert by_name["gwr_lower_lock_dominance"].holds is False
    assert "lock=6" in by_name["gwr_lower_lock_dominance"].detail
    assert "gap=24" in by_name["gwr_lower_lock_dominance"].detail
    assert "gwr_matched_profile_counts" in by_name
    ledger = residual_component_ledger(results, decision_residual=residual)
    assert ledger["decision_residual"] == residual
    comps = ledger["components"]
    assert comps["gwr_dual_gap_carrier_floor_transport_bound"]["holds"] is True
    assert comps["gwr_first_tail_reciprocal_proximity"]["holds"] is False
    assert comps["gwr_lower_lock_dominance"]["holds"] is False


def test_phase1_anti_admission_historical_false_class():
    """Historical false endpoint class must be rejected by pure anti-admission."""
    assert is_historical_false_endpoint_class("32047651", "32059633") is True
    assert is_historical_false_endpoint_class(32047651, 32059633) is True
    # Real factor pair on the same modulus must not be treated as the false class.
    assert is_historical_false_endpoint_class("30729371", "33434981") is False
    assert is_historical_false_endpoint_class("1048559", "1048589") is False
    assert is_historical_false_endpoint_class(None, "32059633") is False


def test_tp_ut_007_residual_encoder_requires_fields():
    row = build_residual_row(
        case_id="c",
        bits=40,
        n_value="11",
        residual_code="unresolved_by_reciprocal_carrier_misalignment",
        step_index=2,
        stage="gwr_carrier_transport_closure",
        lower_present=True,
        upper_present=True,
        diagnostics={"k": 1},
        rule_id=RULE_ID,
        algorithm_version=ALGORITHM_VERSION,
    )
    assert row["residual_code"] in TAXONOMY
    assert row["step_index"] == 2
    assert row["stage"]
    assert is_known_residual(row["residual_code"])


def test_unknown_residual_rejected():
    with pytest.raises(ValueError):
        build_residual_row(
            case_id="c",
            bits=1,
            n_value="3",
            residual_code="not_a_real_code",
            step_index=0,
            stage="x",
            lower_present=False,
            upper_present=False,
            rule_id=RULE_ID,
            algorithm_version=ALGORITHM_VERSION,
        )


def test_content_hash_stable():
    payload = {"a": 1, "b": [2, 3], "schema": "x"}
    h1 = content_hash(payload)
    h2 = content_hash(payload)
    assert h1 == h2
    assert h1.startswith("sha256:")
