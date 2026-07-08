"""Tests for shipped integer_order_demo.py gap and bridge logic."""

from __future__ import annotations

import importlib.util
import json
import math
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[3]
DEMO_PATH = (
    REPO_ROOT
    / "experiments"
    / "integer-order-before-zeta-whitepaper-2026-07"
    / "integer_order_demo.py"
)
RESULTS_PATH = DEMO_PATH.parent / "output" / "demo_results.json"


def _load_demo():
    spec = importlib.util.spec_from_file_location("integer_order_demo", DEMO_PATH)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules["integer_order_demo"] = module
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="module")
def demo():
    return _load_demo()


def test_gap_23_29_gwr_witness(demo):
    counts = demo.divisor_counts_up_to(29)
    report = demo.analyze_gap(23, 29, counts)
    assert report.gwr_witness == 25
    assert report.interior_min_divisor_count == 3


def test_gap_89_97_gwr_witness(demo):
    counts = demo.divisor_counts_up_to(97)
    report = demo.analyze_gap(89, 97, counts)
    assert report.gwr_witness == 91
    assert report.interior_min_divisor_count == 4


def test_zero_excess_primes_at_zero(demo):
    assert demo.zero_excess(23, 2) == pytest.approx(0.0)
    assert demo.zero_excess(29, 2) == pytest.approx(0.0)


def test_bridge_partial_sums_converge(demo):
    bridge = demo.evaluate_bridge(s=2.5, terms=5000, dps=50)
    assert bridge.divisor_abs_error < 1e-4
    assert bridge.ratio_abs_error < 1e-4


def test_demo_results_json_matches_shipped_gaps():
    assert RESULTS_PATH.is_file()
    payload = json.loads(RESULTS_PATH.read_text(encoding="utf-8"))
    gaps = {(g["p"], g["q"]): g for g in payload["gap_examples"]}
    assert gaps[(23, 29)]["gwr_witness"] == 25
    assert gaps[(89, 97)]["gwr_witness"] == 91
    bridge = payload["bridge"]
    assert bridge["s"] == 2.5
    assert bridge["divisor_abs_error"] < 1e-4
    assert bridge["ratio_abs_error"] < 1e-4