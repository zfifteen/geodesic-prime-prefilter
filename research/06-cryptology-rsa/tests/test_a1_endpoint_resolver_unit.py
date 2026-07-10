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
    gwr_lower_lock_dominance,
    gwr_matched_profile_counts,
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
    upper = {"carrier_w": 100, "carrier_d": 4}
    ok = gwr_carrier_floor_transport_within_gap_bound(100 * 100, lower, upper)
    assert ok.holds is True
    far = gwr_carrier_floor_transport_within_gap_bound(100 * 1000, lower, upper)
    assert far.holds is False


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
    lower = {"carrier_w": 100, "carrier_d": 4, "gap_offset": 5, "reset_endpoint": 10, "anchor": 9, "reset_signature": "x"}
    upper = {"carrier_w": 99999, "carrier_d": 4, "anchor": 9, "reset_endpoint": 20, "active_count": 1, "unresolved_count": 0}
    holds, results, residual = evaluate_gwr_carrier_transport_closure(
        100 * 100,
        lower,
        upper,
        require_lock_and_profile=False,
    )
    assert holds is False
    assert residual == "unresolved_by_reciprocal_carrier_misalignment"
    assert any(r.name == "gwr_carrier_floor_transport_within_gap_bound" for r in results)


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
