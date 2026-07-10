"""A1 adversarial pre-registered probes (ADV)."""

from __future__ import annotations

import sys
from pathlib import Path

V3 = Path(__file__).resolve().parents[1] / "experiments" / "live-solver" / "rsa-v3"
sys.path.insert(0, str(V3))

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


def test_adv_005_import_boundary_clean():
    assert scan_inference_tree(V3) == []
