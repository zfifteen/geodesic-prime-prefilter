"""Regression tests for defects found in A1 code review.

Each test targets a concrete shipped-path failure mode identified in review.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

V3 = Path(__file__).resolve().parents[1] / "experiments" / "live-solver" / "rsa-v3"
sys.path.insert(0, str(V3))

from gwr_carrier_closure import gwr_first_tail_reciprocal_proximity  # noqa: E402
from residual import build_residual_row  # noqa: E402
from resolver import load_public_cases, resolve_case  # noqa: E402
from structural_certificate import (  # noqa: E402
    ALGORITHM_VERSION,
    RULE_ID,
    build_structural_certificate,
)
from verifier import verify_certificate  # noqa: E402

REGRESSION = V3 / "fixtures" / "regression_cases.jsonl"
GOLDEN = V3 / "fixtures" / "golden_40bit_structural_certificate.json"


def test_issue1_gwr_tail_none_anchor_does_not_crash():
    """ISSUE-1: first-tail predicate must not TypeError when upper.anchor is None."""
    lower = {
        "reset_signature": "carrier_d=4;lock_carrier_d=4;threat=False;deadline=tail",
        "tail_after_reset_offsets": [3],
        "reset_endpoint": 10,
    }
    upper = {"anchor": None}
    result = gwr_first_tail_reciprocal_proximity(100, lower, upper)
    assert result.holds is False
    assert "anchor" in result.detail or "missing" in result.detail


def test_issue2_public_cases_reject_factor_fields(tmp_path: Path):
    """ISSUE-2: inference load must reject audit/factor keys, not only p/q."""
    path = tmp_path / "bad.jsonl"
    path.write_text(
        json.dumps(
            {
                "case_id": "leak",
                "bits": 4,
                "N": "15",
                "factors": [3, 5],
            }
        )
        + "\n",
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="audit|factor|forbidden|public"):
        load_public_cases(path)


def test_issue2_public_cases_reject_private_factor_aliases(tmp_path: Path):
    path = tmp_path / "bad2.jsonl"
    path.write_text(
        json.dumps({"case_id": "x", "bits": 4, "N": "15", "factor": 3}) + "\n",
        encoding="utf-8",
    )
    with pytest.raises(ValueError):
        load_public_cases(path)


def test_issue3_emitted_structural_cert_must_verify():
    """ISSUE-3 happy path: resolver emit is verifier-green on real 40-bit golden path."""
    cases = load_public_cases(REGRESSION)
    case = next(c for c in cases if c.case_id == "rsa_v2_40bit_static_001")
    result = resolve_case(case, commit="review-issue3")
    cert = result["structural_certificate"]
    assert cert is not None
    report = verify_certificate(cert)
    assert report["ok"] is True, report["errors"]


def test_issue3_verify_on_emit_demotes_bad_package(monkeypatch):
    """ISSUE-3 gate: if builder produces an unverifiable package, resolve_case must demote.

    Drives the shipped resolve_case path. Without the verify_certificate gate around
    emit (resolver.py fail-closed block), a deliberately broken package would be
    returned as structural_certificate and this test would fail.
    """
    import resolver as resolver_mod

    cases = load_public_cases(REGRESSION)
    case = next(c for c in cases if c.case_id == "rsa_v2_40bit_static_001")

    real_build = resolver_mod.build_structural_certificate

    def broken_build(**kwargs):
        package = real_build(**kwargs)
        # Break reciprocal floor while keeping a self-consistent content_hash so only
        # semantic verifier (not stale-hash) would catch it — then rehash would pass
        # hash check but fail floor. Force both: corrupt endpoint and rehash.
        package = json.loads(json.dumps(package))
        package["endpoint_class"]["upper"] = str(int(package["endpoint_class"]["upper"]) + 1)
        from structural_certificate import rehash_certificate

        return rehash_certificate(package)

    monkeypatch.setattr(resolver_mod, "build_structural_certificate", broken_build)
    result = resolve_case(case, commit="review-issue3-gate")
    assert result["structural_certificate"] is None
    assert result["summary"]["endpoint_class_emitted"] is False
    assert result["residual"] is not None
    assert result["residual"]["residual_code"] == "unresolved_by_certificate_pair_not_closed"
    assert result["summary"]["closure_status"] == "unresolved_by_certificate_pair_not_closed"
    assert result["inference"].get("endpoint_class") is None


def test_issue3_builder_plus_verify_roundtrip_includes_corrected_transport():
    """ISSUE-3b: deadline packages must carry corrected transport fields used by verifier."""
    if not GOLDEN.is_file():
        pytest.skip("golden missing")
    golden = json.loads(GOLDEN.read_text(encoding="utf-8"))
    # Reconstruct via builder fields from golden pair-like transport
    pair_json = {
        "lower_anchor": golden["lower_certificate"]["anchor"],
        "lower_reset_endpoint": golden["lower_certificate"]["reset_endpoint"],
        "lower_gap_offset": golden["lower_certificate"]["gap_offset"],
        "lower_candidate_bound": golden["lower_certificate"]["candidate_bound"],
        "lower_active_count": golden["lower_certificate"]["active_count"],
        "lower_resolved_count": golden["lower_certificate"]["resolved_count"],
        "lower_unresolved_count": golden["lower_certificate"]["unresolved_count"],
        "lower_closed_offsets_before_q": golden["lower_certificate"][
            "closed_offsets_before_q"
        ],
        "lower_carrier_w": golden["lower_certificate"]["carrier_w"],
        "lower_carrier_d": golden["lower_certificate"]["carrier_d"],
        "lower_lock_carrier_offset": golden["lower_certificate"]["lock_carrier_offset"],
        "lower_lock_carrier_d": golden["lower_certificate"]["lock_carrier_d"],
        "lower_d_threat_offset": golden["lower_certificate"]["lower_d_threat_offset"],
        "lower_tail_after_reset_offsets": golden["lower_certificate"][
            "tail_after_reset_offsets"
        ],
        "lower_reset_deadline_value": golden["lower_certificate"]["reset_deadline_value"],
        "lower_reset_deadline_margin": golden["lower_certificate"][
            "reset_deadline_margin"
        ],
        "lower_reset_signature": golden["lower_certificate"]["reset_signature"],
        "upper_anchor": golden["upper_certificate"]["anchor"],
        "upper_reset_endpoint": golden["upper_certificate"]["reset_endpoint"],
        "upper_gap_offset": golden["upper_certificate"]["gap_offset"],
        "upper_candidate_bound": golden["upper_certificate"]["candidate_bound"],
        "upper_active_count": golden["upper_certificate"]["active_count"],
        "upper_resolved_count": golden["upper_certificate"]["resolved_count"],
        "upper_unresolved_count": golden["upper_certificate"]["unresolved_count"],
        "upper_closed_offsets_before_q": golden["upper_certificate"][
            "closed_offsets_before_q"
        ],
        "upper_carrier_w": golden["upper_certificate"]["carrier_w"],
        "upper_carrier_d": golden["upper_certificate"]["carrier_d"],
        "upper_lock_carrier_offset": golden["upper_certificate"]["lock_carrier_offset"],
        "upper_lock_carrier_d": golden["upper_certificate"]["lock_carrier_d"],
        "upper_d_threat_offset": golden["upper_certificate"]["lower_d_threat_offset"],
        "upper_tail_after_reset_offsets": golden["upper_certificate"][
            "tail_after_reset_offsets"
        ],
        "upper_reset_deadline_value": golden["upper_certificate"]["reset_deadline_value"],
        "upper_reset_deadline_margin": golden["upper_certificate"][
            "reset_deadline_margin"
        ],
        "upper_reset_signature": golden["upper_certificate"]["reset_signature"],
        "corrected_lower_anchor": golden["corrected_lower_certificate"]["anchor"],
        "corrected_lower_reset_endpoint": golden["corrected_lower_certificate"][
            "reset_endpoint"
        ],
        "corrected_lower_gap_offset": golden["corrected_lower_certificate"]["gap_offset"],
        "corrected_lower_candidate_bound": golden["corrected_lower_certificate"][
            "candidate_bound"
        ],
        "corrected_lower_active_count": golden["corrected_lower_certificate"][
            "active_count"
        ],
        "corrected_lower_resolved_count": golden["corrected_lower_certificate"][
            "resolved_count"
        ],
        "corrected_lower_unresolved_count": golden["corrected_lower_certificate"][
            "unresolved_count"
        ],
        "corrected_lower_closed_offsets_before_q": golden["corrected_lower_certificate"][
            "closed_offsets_before_q"
        ],
        "corrected_lower_carrier_w": golden["corrected_lower_certificate"]["carrier_w"],
        "corrected_lower_carrier_d": golden["corrected_lower_certificate"]["carrier_d"],
        "corrected_lower_lock_carrier_offset": golden["corrected_lower_certificate"][
            "lock_carrier_offset"
        ],
        "corrected_lower_lock_carrier_d": golden["corrected_lower_certificate"][
            "lock_carrier_d"
        ],
        "corrected_lower_d_threat_offset": golden["corrected_lower_certificate"][
            "lower_d_threat_offset"
        ],
        "corrected_lower_tail_after_reset_offsets": golden["corrected_lower_certificate"][
            "tail_after_reset_offsets"
        ],
        "corrected_lower_reset_deadline_value": golden["corrected_lower_certificate"][
            "reset_deadline_value"
        ],
        "corrected_lower_reset_deadline_margin": golden["corrected_lower_certificate"][
            "reset_deadline_margin"
        ],
        "corrected_lower_reset_signature": golden["corrected_lower_certificate"][
            "reset_signature"
        ],
        "endpoint_chain_transport_coordinate": golden["transport"][
            "endpoint_chain_transport_coordinate"
        ],
        "transported_upper_endpoint": golden["transport"]["transported_upper_endpoint"],
        "transported_lower_endpoint": golden["transport"]["transported_lower_endpoint"],
        "corrected_lower_endpoint": golden["transport"]["corrected_lower_endpoint"],
        "corrected_upper_endpoint": golden["transport"]["corrected_upper_endpoint"],
        # Required for full deadline transport trace
        "transported_corrected_upper_endpoint": golden["transport"].get(
            "transported_corrected_upper_endpoint"
        )
        or golden["transport"]["corrected_upper_endpoint"],
        "transported_corrected_lower_endpoint": golden["transport"].get(
            "transported_corrected_lower_endpoint"
        )
        or golden["transport"]["corrected_lower_endpoint"],
    }
    built = build_structural_certificate(
        case_id=golden["case_id"],
        bits=golden["bits"],
        n_value=golden["N"],
        center=golden["center"],
        closure_status=golden["closure_status"],
        endpoint_lower=golden["endpoint_class"]["lower"],
        endpoint_upper=golden["endpoint_class"]["upper"],
        pair_json=pair_json,
        gwr_predicate_map=golden["gwr_carrier_closure"],
        step_index=golden.get("step_index"),
        git_commit=golden.get("git_commit"),
    )
    assert "transported_corrected_upper_endpoint" in built["transport"]
    assert "transported_corrected_lower_endpoint" in built["transport"]
    assert verify_certificate(built)["ok"] is True


def test_issue4_unknown_residual_mapped_not_crash():
    """ISSUE-4 helper: coerce maps unknown labels to taxonomy-safe codes."""
    from residual import coerce_residual_code

    code = coerce_residual_code("unresolved_by_future_v2_status_xyz")
    assert code in (
        "unresolved_by_instrumentation_limit",
        "unresolved_by_certificate_pair_not_closed",
    )
    row = build_residual_row(
        case_id="c",
        bits=8,
        n_value="15",
        residual_code=code,
        step_index=0,
        stage="map",
        lower_present=False,
        upper_present=False,
        rule_id=RULE_ID,
        algorithm_version=ALGORITHM_VERSION,
    )
    assert row["residual_code"] == code


def test_issue4_resolve_case_maps_unknown_v2_closure_status(monkeypatch):
    """ISSUE-4 ship path: resolve_case must map unknown v2 closure_status without raising.

    Injects a CertificatePair with a novel residual label through the real
    resolve_case entry. Without coerce_residual_code on the unresolved branch,
    build_residual_row raises ValueError on unknown codes.
    """
    import resolver as resolver_mod
    import gmpy2

    cases = load_public_cases(REGRESSION)
    case = next(c for c in cases if c.case_id == "rsa_v2_40bit_static_001")

    unknown = "unresolved_by_future_v2_status_xyz"
    fake_pair = resolver_mod.v2.CertificatePair(
        lower=None,
        upper=None,
        corrected_lower=None,
        corrected_lower_endpoint=None,
        corrected_upper_endpoint=None,
        transported_upper_endpoint=None,
        transported_lower_endpoint=None,
        transported_corrected_upper_endpoint=None,
        transported_corrected_lower_endpoint=None,
        lower_transported_deadline_width=None,
        upper_transported_deadline_width=None,
        closure_status=unknown,
        endpoint_chain_steps=0,
        endpoint_chain_source_anchor=None,
    )

    def fake_chain(case_arg, diagnostics, start_anchor=None, max_steps=10000):
        diagnostics["previous_endpoint_lookups"] = diagnostics.get(
            "previous_endpoint_lookups", 0
        )
        return fake_pair

    monkeypatch.setattr(resolver_mod.v2, "certificate_pair", fake_chain)
    # Also short-circuit budget wrapper if used
    monkeypatch.setattr(
        resolver_mod,
        "_run_chain_with_budget",
        lambda *a, **k: fake_pair,
    )

    result = resolve_case(case, commit="review-issue4-resolve", force_full_chain=True)
    assert result["structural_certificate"] is None
    assert result["residual"] is not None
    assert result["residual"]["residual_code"] == "unresolved_by_instrumentation_limit"
    assert result["summary"]["residual_code"] == "unresolved_by_instrumentation_limit"
    assert result["summary"]["closure_status"] == "unresolved_by_instrumentation_limit"
    # Must not surface the unknown raw label in residual ledger
    assert result["residual"]["residual_code"] != unknown

