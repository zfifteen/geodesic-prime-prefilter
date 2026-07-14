"""A1 adversarial pre-registered probes (ADV)."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

V3 = Path(__file__).resolve().parents[1] / "experiments" / "live-solver" / "rsa-v3"
sys.path.insert(0, str(V3))

import resolver as resolver_mod  # noqa: E402
from residual import is_resolved_status  # noqa: E402
from resolver import load_public_cases, resolve_case  # noqa: E402
from boundary import scan_inference_tree  # noqa: E402

REGRESSION = V3 / "fixtures" / "regression_cases.jsonl"
ADV_PREREG = V3 / "falsification" / "ADV-001_carrier_misalignment.md"


def test_adv_preregister_artifact_exists():
    assert ADV_PREREG.is_file()
    text = ADV_PREREG.read_text(encoding="utf-8")
    assert "Pre-register" in text


def test_adv_001_known_carrier_misalignment_stays_unresolved():
    cases = load_public_cases(REGRESSION)
    case = next(c for c in cases if c.case_id == "rsa_v2_50bit_static_001")
    result = resolve_case(case, commit="adv")
    assert is_resolved_status(str(result["summary"]["closure_status"])) is False
    assert result["residual"] is not None
    # Must not invent factors via classical gate
    assert "p" not in result["inference"]
    assert "q" not in result["inference"]


def test_phase1_anti_admission_reject_on_resolve_case_emit_path(monkeypatch):
    """Drive shipped resolve_case emit guard against historical false class.

    Forces the resolved-branch path where GWR holds and endpoint pair would be
    (32047651, 32059633). Guard must reject emit. Removing the resolver anti-
    admission block must fail this test (endpoint would emit if verify is green).
    """
    cases = load_public_cases(REGRESSION)
    case = next(c for c in cases if c.case_id == "rsa_v2_50bit_static_001")

    class FakePair:
        closure_status = "endpoint_class_by_mutual_certificate_closure"
        endpoint_chain_steps = 350
        lower = object()
        upper = object()
        corrected_lower = None

    monkeypatch.setattr(
        resolver_mod, "_run_chain_with_budget", lambda *a, **k: FakePair()
    )
    monkeypatch.setattr(
        resolver_mod.v2,
        "pair_to_json",
        lambda c, pair: {
            "case_id": c.case_id,
            "bits": c.bits,
            "N": str(c.n),
            "public_closure_status": "endpoint_class_by_mutual_certificate_closure",
        },
    )
    # GWR stack accepts so emission path is reached (not residual short-circuit).
    monkeypatch.setattr(
        resolver_mod,
        "evaluate_gwr_carrier_transport_closure",
        lambda *a, **k: (True, [], None),
    )
    monkeypatch.setattr(
        resolver_mod,
        "_endpoint_class_from_pair",
        lambda pair: ("32047651", "32059633"),
    )
    # If anti-admission were removed, verify would still allow emit; prove guard
    # is what blocks the false class.
    monkeypatch.setattr(
        resolver_mod,
        "verify_certificate",
        lambda cert: {"ok": True, "errors": []},
    )
    # build_structural_certificate should not be required if guard fires first,
    # but keep it safe if order changes.
    monkeypatch.setattr(
        resolver_mod,
        "build_structural_certificate",
        lambda **kwargs: {"stub": True, **{k: kwargs.get(k) for k in ("case_id",)}},
    )

    result = resolve_case(case, commit="anti-admission-emit-path")

    assert result["summary"]["endpoint_class_emitted"] is False
    assert result["inference"]["endpoint_class"] is None
    assert result["inference"]["public_structure_found"] is False
    assert is_resolved_status(str(result["summary"]["closure_status"])) is False
    assert result["summary"]["residual_code"] == "unresolved_by_certificate_pair_not_closed"
    assert result["structural_certificate"] is None
    anti = result["gwr_carrier_closure"].get("anti_admission")
    assert anti is not None
    assert anti["holds"] is False
    assert anti["detail"] == "historical_false_endpoint_class_50bit"
    assert anti["rejected_lower"] == "32047651"
    assert anti["rejected_upper"] == "32059633"
    assert "p" not in result["inference"]
    assert "q" not in result["inference"]


def test_adv_005_import_boundary_clean():
    assert scan_inference_tree(V3) == []
