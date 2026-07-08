"""Tests for shipped zeta_compression_probe.py Layer 3 empiric."""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[3]
PROBE_PATH = (
    REPO_ROOT / "research" / "19-rh-corpus" / "empirics" / "zeta_compression_probe.py"
)
OUTPUT_PATH = PROBE_PATH.parent / "output" / "compression_probe_results.json"


def _load_probe():
    spec = importlib.util.spec_from_file_location("zeta_compression_probe", PROBE_PATH)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules["zeta_compression_probe"] = module
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="module")
def probe():
    return _load_probe()


def test_divisor_counts_tau_values(probe):
    counts = probe.divisor_counts_up_to(12)
    assert counts[1] == 1
    assert counts[2] == 2
    assert counts[4] == 3
    assert counts[6] == 4
    assert counts[12] == 6


def test_probe_at_s25_errors_small(probe):
    counts = probe.divisor_counts_up_to(probe.TERMS)
    point = probe.probe_at(2.5, probe.TERMS, counts, probe.DPS)
    assert point.divisor_abs_error < 1e-4
    assert point.ratio_abs_error < 1e-4


def test_compression_results_artifact_exists():
    assert OUTPUT_PATH.is_file()
    payload = json.loads(OUTPUT_PATH.read_text(encoding="utf-8"))
    assert payload["finding_id"] == "RH-105"
    assert payload["terms"] == 10_000
    assert len(payload["points"]) == 5
    # Match whitepaper demo regime: s=2.5 at N=10k (s=1.5–2.0 need more terms).
    by_s = {p["s"]: p for p in payload["points"]}
    p25 = by_s[2.5]
    assert p25["divisor_abs_error"] < 1e-4
    assert p25["ratio_abs_error"] < 1e-4