#!/usr/bin/env python3
"""Unit tests for hourly research delta classification."""

from __future__ import annotations

import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPT_DIR))

from hourly_delta import (  # noqa: E402
    RESEARCH_ADVANCE,
    RESEARCH_FAILED,
    RESEARCH_NO_DELTA,
    RESEARCH_UNRESOLVED,
    classify_deterministic,
    signatures_equal,
    summary_signature,
)


BASELINE = {
    "min_prime": 300000001,
    "max_prime": 400000000,
    "tested_prime_count": 5084001,
    "first_counterexample": None,
    "max_dynamic_cutoff_utilization": 0.7036082474226805,
    "max_p": 358018553,
    "max_offset": 546,
}


def test_replay_of_baseline_is_no_delta() -> None:
    status, delta = classify_deterministic(
        command_ok=True,
        pytest_ok=True,
        current_signature=dict(BASELINE),
        prior_signature=None,
        baseline_signature=dict(BASELINE),
    )
    assert status == RESEARCH_NO_DELTA
    assert "baseline" in delta


def test_new_regime_is_advance() -> None:
    current = dict(BASELINE)
    current["min_prime"] = 400000001
    current["max_prime"] = 500000000
    current["tested_prime_count"] = 5000000
    current["max_p"] = 450000007
    status, delta = classify_deterministic(
        command_ok=True,
        pytest_ok=True,
        current_signature=current,
        prior_signature=dict(BASELINE),
        baseline_signature=dict(BASELINE),
    )
    assert status == RESEARCH_ADVANCE
    assert "max_prime=500000000" in delta


def test_command_failure() -> None:
    status, _ = classify_deterministic(
        command_ok=False,
        pytest_ok=True,
        current_signature=None,
        prior_signature=None,
        baseline_signature=None,
    )
    assert status == RESEARCH_FAILED


def test_missing_summary_is_unresolved() -> None:
    status, _ = classify_deterministic(
        command_ok=True,
        pytest_ok=True,
        current_signature=None,
        prior_signature=None,
        baseline_signature=None,
    )
    assert status == RESEARCH_UNRESOLVED


def test_summary_signature_extracts_max_row() -> None:
    summary = {
        "min_prime": 1,
        "max_prime": 2,
        "tested_prime_count": 3,
        "first_counterexample": None,
        "max_dynamic_cutoff_utilization": 0.5,
        "max_row": {"p": 9, "offset": 8},
    }
    sig = summary_signature(summary)
    assert sig is not None
    assert sig["max_p"] == 9
    assert sig["max_offset"] == 8
    assert signatures_equal(sig, sig)
