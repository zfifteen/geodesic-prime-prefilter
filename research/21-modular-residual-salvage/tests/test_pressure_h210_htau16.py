"""Tests for H-210 / H-tau16 CE pressure predicates and entry module."""

from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts" / "pressure_h210_htau16.py"


def load_module():
    spec = importlib.util.spec_from_file_location("pressure_h210_htau16_ch21", MODULE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"unable to load {MODULE_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="module")
def pressure():
    return load_module()


def test_h210_antecedent_and_ce_logic(pressure):
    assert pressure.is_h210_antecedent(210) is True
    assert pressure.is_h210_antecedent(30) is False
    # antecedent + gap>2 falsifies implication
    assert pressure.is_hypothesis_ce(gap=8, antecedent=True) is True
    assert pressure.is_hypothesis_ce(gap=2, antecedent=True) is False
    assert pressure.is_hypothesis_ce(gap=8, antecedent=False) is False


def test_htau16_antecedent_logic(pressure):
    assert pressure.is_htau16_antecedent(w=210, tau_w=32, z=6) is True
    assert pressure.is_htau16_antecedent(w=30, tau_w=8, z=4) is False  # tau not > 16
    assert pressure.is_htau16_antecedent(w=30, tau_w=32, z=3) is False  # z < 4


def test_run_pressure_small_regime_returns_hypothesis_labels(pressure):
    """Drive shipped run_pressure on a tiny regime (real entry path)."""
    result = pressure.run_pressure(11, 5_000)
    assert result["status"] == "hypothesis_measured_pressure_only"
    assert result["z4_universal_status_lock"] == "invalidated"
    assert "proved" not in result["claim_language"].lower()
    assert result["regime"]["p_min"] == 11
    assert result["regime"]["p_max"] == 5_000
    assert result["control"]["gaps_scanned"] > 0
    for key in ("H-210", "H-tau16"):
        h = result["hypotheses"][key]
        assert h["status_label"] == "hypothesis / measured"
        assert h["verdict"] in ("falsified", "not_falsified_in_tested_regime")
        assert h["counterexample_count"] == len(h["counterexample_examples"]) or (
            h["counterexample_count"] >= len(h["counterexample_examples"])
        )
        if h["verdict"] == "falsified":
            assert h["counterexample_count"] >= 1
            assert h["counterexample_examples"]
            assert h["counterexample_examples"][0]["gap"] > 2
        else:
            assert h["counterexample_count"] == 0
