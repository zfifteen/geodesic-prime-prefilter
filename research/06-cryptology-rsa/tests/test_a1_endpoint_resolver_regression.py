"""A1 regression + determinism on fixed public goldens (RG/IT)."""

from __future__ import annotations

import json
import sys
from pathlib import Path

V3 = Path(__file__).resolve().parents[1] / "experiments" / "live-solver" / "rsa-v3"
sys.path.insert(0, str(V3))

from residual import is_resolved_status  # noqa: E402
from resolver import load_public_cases, resolve_case  # noqa: E402
from structural_certificate import RULE_ID  # noqa: E402
from verifier import verify_certificate  # noqa: E402

REGRESSION = V3 / "fixtures" / "regression_cases.jsonl"


def _by_id(case_id: str):
    cases = load_public_cases(REGRESSION)
    for case in cases:
        if case.case_id == case_id:
            return case
    raise AssertionError(f"missing {case_id}")


def test_tp_rg_001_known_resolved_40bit():
    case = _by_id("rsa_v2_40bit_static_001")
    result = resolve_case(case, commit="test-commit")
    summary = result["summary"]
    assert is_resolved_status(str(summary["closure_status"]))
    assert summary["endpoint_class_emitted"] is True
    assert summary["rule_id"] == RULE_ID
    assert summary["algorithm_version"]
    assert result["structural_certificate"] is not None
    report = verify_certificate(result["structural_certificate"])
    assert report["ok"] is True, report["errors"]
    assert result["inference"]["endpoint_class"]["lower"]
    assert result["inference"]["endpoint_class"]["upper"]
    # Public class record has no audit fields
    assert "confidence" not in result["inference"]
    assert "p" not in result["inference"]


def test_tp_rg_002_known_unresolved_50bit_carrier_misalignment():
    case = _by_id("rsa_v2_50bit_static_001")
    result = resolve_case(case, commit="test-commit")
    summary = result["summary"]
    assert is_resolved_status(str(summary["closure_status"])) is False
    assert summary["residual_code"] is not None
    assert result["residual"] is not None
    assert result["residual"]["residual_code"] == summary["residual_code"]
    assert result["residual"]["step_index"] is not None or result["residual"]["stage"]
    assert result["residual"]["diagnostics"]
    # Carrier misalignment family remains unresolved (honest residual)
    code = summary["residual_code"]
    assert "unresolved" in code
    assert result["structural_certificate"] is None


def test_tp_rg_003_determinism_double_run_40bit():
    case = _by_id("rsa_v2_40bit_static_001")
    r1 = resolve_case(case, commit="fixed")
    r2 = resolve_case(case, commit="fixed")
    s1, s2 = r1["summary"], r2["summary"]
    assert s1["closure_status"] == s2["closure_status"]
    assert s1["rule_id"] == s2["rule_id"]
    assert s1["residual_code"] == s2["residual_code"]
    assert r1["inference"].get("endpoint_class") == r2["inference"].get("endpoint_class")
    if r1["structural_certificate"] and r2["structural_certificate"]:
        assert (
            r1["structural_certificate"]["content_hash"]
            == r2["structural_certificate"]["content_hash"]
        )
        # transport coordinates match
        assert (
            r1["structural_certificate"]["transport"]
            == r2["structural_certificate"]["transport"]
        )


def test_tp_it_001_summary_required_fields():
    case = _by_id("rsa_v2_40bit_static_001")
    result = resolve_case(case, commit="it")
    s = result["summary"]
    for key in (
        "case_id",
        "bits",
        "N",
        "center",
        "algorithm_version",
        "git_commit",
        "closure_status",
        "rule_id",
        "lower_certificate_present",
        "upper_certificate_present",
    ):
        assert key in s
