"""A1 certificate schema/verifier tests (CT).

Fail-closed checks must reject rehashed semantic mutations of real resolved
certificates (deadline-signature path), not only stale content_hash theater.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

V3 = Path(__file__).resolve().parents[1] / "experiments" / "live-solver" / "rsa-v3"
sys.path.insert(0, str(V3))

from residual import is_resolved_status  # noqa: E402
from resolver import load_public_cases, resolve_case  # noqa: E402
from structural_certificate import (  # noqa: E402
    build_structural_certificate,
    content_hash,
    mutate_certificate_for_tests,
    rehash_certificate,
)
from verifier import verify_certificate  # noqa: E402

REGRESSION = V3 / "fixtures" / "regression_cases.jsonl"
GOLDEN_CACHE = V3 / "fixtures" / "golden_40bit_structural_certificate.json"


def _synthetic_mutual_cert():
    """Minimal mutual-path package for unit-level CT smoke (not the deadline golden)."""
    pair_json = {
        "lower_anchor": "9",
        "lower_reset_endpoint": "10",
        "lower_gap_offset": 1,
        "lower_candidate_bound": 128,
        "lower_active_count": 1,
        "lower_resolved_count": 1,
        "lower_unresolved_count": 0,
        "lower_closed_offsets_before_q": [],
        "lower_carrier_w": "10",
        "lower_carrier_d": 4,
        "lower_lock_carrier_offset": 1,
        "lower_lock_carrier_d": 4,
        "lower_d_threat_offset": None,
        "lower_tail_after_reset_offsets": [],
        "lower_reset_deadline_value": "11",
        "lower_reset_deadline_margin": 1,
        "lower_reset_signature": "carrier_d=4;lock_carrier_d=4;threat=False;deadline=bound",
        "upper_anchor": "9",
        "upper_reset_endpoint": "10",
        "upper_gap_offset": 1,
        "upper_candidate_bound": 128,
        "upper_active_count": 1,
        "upper_resolved_count": 1,
        "upper_unresolved_count": 0,
        "upper_closed_offsets_before_q": [],
        "upper_carrier_w": "10",
        "upper_carrier_d": 4,
        "upper_lock_carrier_offset": 1,
        "upper_lock_carrier_d": 4,
        "upper_d_threat_offset": None,
        "upper_tail_after_reset_offsets": [],
        "upper_reset_deadline_value": "11",
        "upper_reset_deadline_margin": 1,
        "upper_reset_signature": "carrier_d=4;lock_carrier_d=4;threat=False;deadline=bound",
        "transported_upper_endpoint": "10",
        "transported_lower_endpoint": "10",
        "endpoint_chain_transport_coordinate": "10",
    }
    # N=100, lower=10, upper=10: floor(100/10)=10 both ways.
    return build_structural_certificate(
        case_id="synthetic_mutual",
        bits=8,
        n_value="100",
        center="10",
        closure_status="endpoint_class_by_mutual_certificate_closure",
        endpoint_lower="10",
        endpoint_upper="10",
        pair_json=pair_json,
        gwr_predicate_map={"gwr_carrier_fields_present": {"holds": True, "detail": "ok"}},
        step_index=0,
        git_commit="test",
    )


@pytest.fixture(scope="module")
def real_deadline_golden():
    """Real 40-bit deadline-signature structural certificate from shipped resolver."""
    if GOLDEN_CACHE.is_file():
        cert = json.loads(GOLDEN_CACHE.read_text(encoding="utf-8"))
        report = verify_certificate(cert)
        if report["ok"]:
            return cert
    cases = load_public_cases(REGRESSION)
    case = next(c for c in cases if c.case_id == "rsa_v2_40bit_static_001")
    result = resolve_case(case, commit="ct-golden")
    assert is_resolved_status(str(result["summary"]["closure_status"]))
    cert = result["structural_certificate"]
    assert cert is not None
    report = verify_certificate(cert)
    assert report["ok"] is True, report["errors"]
    assert cert["closure_status"] == (
        "endpoint_class_by_reciprocal_deadline_signature_correction"
    ) or str(cert["closure_status"]).startswith("endpoint_class_by_")
    GOLDEN_CACHE.write_text(json.dumps(cert, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return cert


def test_tp_ct_001_002_synthetic_mutual_accepts():
    cert = _synthetic_mutual_cert()
    report = verify_certificate(cert)
    assert report["ok"] is True, report["errors"]


def test_tp_ct_001_002_real_deadline_golden_accepts(real_deadline_golden):
    report = verify_certificate(real_deadline_golden)
    assert report["ok"] is True, report["errors"]
    # Hash must be self-consistent
    assert real_deadline_golden["content_hash"] == content_hash(real_deadline_golden)


def test_tp_ct_003_rehashed_floor_mutation_rejects(real_deadline_golden):
    broken = mutate_certificate_for_tests(real_deadline_golden, "floor_equality", rehash=True)
    # Prove hash is valid for the broken body (semantic reject, not stale-hash theater).
    assert broken["content_hash"] == content_hash(broken)
    report = verify_certificate(broken)
    assert report["ok"] is False
    assert any("floor" in e.lower() or "endpoint_class" in e for e in report["errors"]), report[
        "errors"
    ]


def test_tp_ct_003_rehashed_signature_mutation_rejects(real_deadline_golden):
    broken = mutate_certificate_for_tests(real_deadline_golden, "signature", rehash=True)
    assert broken["content_hash"] == content_hash(broken)
    report = verify_certificate(broken)
    assert report["ok"] is False
    assert any("signature" in e.lower() for e in report["errors"]), report["errors"]


def test_tp_ct_003_rehashed_endpoint_class_mutation_rejects(real_deadline_golden):
    broken = mutate_certificate_for_tests(real_deadline_golden, "endpoint_class", rehash=True)
    assert broken["content_hash"] == content_hash(broken)
    report = verify_certificate(broken)
    assert report["ok"] is False
    assert any(
        "endpoint_class" in e or "floor" in e.lower() for e in report["errors"]
    ), report["errors"]


def test_tp_ct_003_missing_field_rejects(real_deadline_golden):
    broken = mutate_certificate_for_tests(real_deadline_golden, "missing_field", rehash=False)
    report = verify_certificate(broken)
    assert report["ok"] is False
    assert any("endpoint_class" in e for e in report["errors"])


def test_tp_ct_003_bad_hash_rejects(real_deadline_golden):
    broken = mutate_certificate_for_tests(real_deadline_golden, "bad_hash", rehash=False)
    report = verify_certificate(broken)
    assert report["ok"] is False
    assert any("content_hash" in e for e in report["errors"])


def test_tp_ct_003_manual_rehash_signature_break_no_magic_strings(real_deadline_golden):
    """Arbitrary rehashed signature break must fail without magic-token lists."""
    broken = json.loads(json.dumps(real_deadline_golden))
    upper = broken["upper_certificate"]
    upper["reset_signature"] = (upper.get("reset_signature") or "") + "#arbitrary"
    broken = rehash_certificate(broken)
    report = verify_certificate(broken)
    assert report["ok"] is False
    assert any("signature" in e.lower() for e in report["errors"])


def test_tp_ct_005_no_audit_fields(real_deadline_golden):
    cert = real_deadline_golden
    assert "confidence" not in cert
    assert "factor" not in cert
    assert "p" not in cert
    assert "q" not in cert
