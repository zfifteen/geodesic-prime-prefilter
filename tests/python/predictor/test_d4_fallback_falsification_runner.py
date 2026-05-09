"""Tests for the d=4 fallback falsification runner."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
MODULE_PATH = (
    ROOT / "benchmarks" / "python" / "predictor" / "d4_fallback_falsification_runner.py"
)


def load_module():
    """Load the runner from its file path."""
    spec = importlib.util.spec_from_file_location(
        "d4_fallback_falsification_runner",
        MODULE_PATH,
    )
    if spec is None or spec.loader is None:
        raise RuntimeError("unable to load d4_fallback_falsification_runner")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_first_d4_offset_reads_exact_ladder():
    """The first d=4 carrier is read directly from the exact divisor ladder."""
    module = load_module()

    assert module.first_d4_offset([6, 4, 8]) == 2
    assert module.first_d4_offset([6, 8, 10]) is None


def test_literal_d4_fallback_has_first_failure_at_113():
    """The literal prior-square formulation fails at q=113."""
    module = load_module()
    summary, first_failure = module.run_scan(11, 10_000)

    assert first_failure is not None
    assert summary["first_failure"] == first_failure
    assert summary["last_tested_q"] == 113
    assert first_failure["q"] == 113
    assert first_failure["first_d4_carrier"] == 115
    assert first_failure["first_d4_offset"] == 2
    assert first_failure["prior_prime_square"] is None
    assert first_failure["exact_witness"] == 121
    assert first_failure["exact_witness_is_prime_square"] is True
    assert first_failure["exact_witness_prime_square_root"] == 11
    assert first_failure["fallback_holds"] is False


def test_cli_writes_failure_metadata(tmp_path):
    """The CLI should emit summary and first-failure JSON."""
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

    summary_path = tmp_path / "d4_fallback_falsification_summary.json"
    failure_path = tmp_path / "d4_fallback_first_failure.json"
    assert summary_path.exists()
    assert failure_path.exists()

    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    failure = json.loads(failure_path.read_text(encoding="utf-8"))
    assert summary["first_failure"]["q"] == 113
    assert failure["q"] == 113
    assert failure["exact_witness"] == 121
