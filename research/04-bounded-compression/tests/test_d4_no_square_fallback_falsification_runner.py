"""Tests for the no-square d=4 fallback falsification runner."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
MODULE_PATH = (
    ROOT
    / "research"
    / "04-bounded-compression"
    / "scripts"
    / "d4_no_square_fallback_falsification_runner.py"
)


def load_module():
    """Load the runner from its file path."""
    spec = importlib.util.spec_from_file_location(
        "d4_no_square_fallback_falsification_runner",
        MODULE_PATH,
    )
    if spec is None or spec.loader is None:
        raise RuntimeError("unable to load d4_no_square_fallback_falsification_runner")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_q_113_is_square_present_not_fallback_failure():
    """The q=113 counterexample to the prior-square wording is square-present."""
    module = load_module()
    row = module.row_for_right_prime(113)

    assert row["first_d4_carrier"] == 115
    assert row["first_interior_prime_square"] == 121
    assert row["first_interior_prime_square_root"] == 11
    assert row["has_interior_square"] is True
    assert row["fallback_applicable"] is False
    assert row["fallback_holds"] is None


def test_small_surface_has_no_no_square_fallback_failure():
    """The narrowed no-square fallback should survive a small exact surface."""
    module = load_module()
    summary, first_failure = module.run_scan(11, 10_000)

    assert first_failure is None
    assert summary["first_failure"] is None
    assert summary["tested_gap_count"] > 0
    assert summary["no_square_d4_fallback_cases"] > 0
    assert summary["square_present_cases"] > 0


def test_cli_writes_summary_without_failure(tmp_path):
    """The CLI should emit a summary JSON on a small no-failure surface."""
    module = load_module()

    assert (
        module.main(
            [
                "--min-right-prime",
                "11",
                "--max-right-prime",
                "10000",
                "--output-dir",
                str(tmp_path),
            ]
        )
        == 0
    )

    summary_path = tmp_path / "d4_no_square_fallback_summary.json"
    failure_path = tmp_path / "d4_no_square_fallback_first_failure.json"
    assert summary_path.exists()
    assert not failure_path.exists()

    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    assert summary["first_failure"] is None
    assert summary["no_square_d4_fallback_cases"] > 0
