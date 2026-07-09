"""Tests for chamber_compression + zeta_compression_probe (RH-105)."""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[3]
SRC = REPO_ROOT / "src" / "python"
EMP = REPO_ROOT / "research" / "19-rh-corpus" / "empirics"
for path in (SRC, EMP):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from chamber_compression import (
    analyze_chamber_gap,
    chamber_dirichlet_increments,
    compression_bound_c,
    f18_branch_label,
)

OUTPUT_PATH = EMP / "output" / "compression_probe_results.json"


def test_chamber_gap_23_29():
    report = analyze_chamber_gap(23, 29)
    assert report.w == 25
    assert report.tau_w == 3
    assert report.f18_branch == "prime_square"


def test_compression_bound_c():
    assert compression_bound_c(29) == 64


def test_f18_max_case_square_branch():
    summary_path = REPO_ROOT / "research" / "18-derived-half-coefficient" / "output" / "near_maximal_audit_results_40M.json"
    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    case = summary["max_case"]
    report = analyze_chamber_gap(case["p"], case["q"])
    assert report.f18_branch == "prime_square"
    assert report.offset_ratio == pytest.approx(case["ratio"], rel=1e-4)


def test_chamber_dirichlet_increments_at_s25():
    inc = chamber_dirichlet_increments(2.5, 23, 29, 10_000)
    assert inc.delta_d > 0
    assert inc.rho_chamber > 0
    assert inc.global_r_error < 1e-4


def test_compression_results_artifact_exists():
    assert OUTPUT_PATH.is_file()
    payload = json.loads(OUTPUT_PATH.read_text(encoding="utf-8"))
    assert payload["finding_id"] == "RH-105"
    assert payload["probe"] == "gwr_chamber_zeta_compression"
    assert len(payload["example_chambers"]) == 2
    assert payload["f18_max_case"]["chamber"]["f18_branch"] == "prime_square"
    assert payload["global_bridge"]["normalized_ratio_error"] < 1e-4


def test_multi_s_bridge_fields_in_artifact():
    """RH-105 claims five s-values; artifact must carry that measured surface."""
    payload = json.loads(OUTPUT_PATH.read_text(encoding="utf-8"))
    s_values = payload["s_values"]
    assert len(s_values) == 5
    assert all(s > 1.0 for s in s_values)
    by_s = payload["global_bridge_by_s"]
    assert len(by_s) == 5
    # Primary s=2.5 is tight at N=10^4; s=2.0 is coarser but still measured.
    for row in by_s:
        assert row["normalized_ratio_error"] < 5e-3
        assert row["mangoldt_series_error"] < 5e-3
    multi = payload["example_increments_multi_s"]
    assert len(multi) == 5 * 2  # five s × two example gaps
    assert all(row["delta_d"] > 0 and row["rho_chamber"] > 0 for row in multi)


def test_multi_s_probe_module_constants():
    """Ship constants match the RH-105 measured regime, not a reimplementation."""
    import zeta_compression_probe as probe

    assert len(probe.PROBE_S_VALUES) == 5
    assert probe.PRIMARY_S in probe.PROBE_S_VALUES
    assert probe.PROBE_TERMS == 10_000