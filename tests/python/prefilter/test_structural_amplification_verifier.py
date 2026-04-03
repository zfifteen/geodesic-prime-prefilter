"""Tests for the structural amplification verifier."""

from __future__ import annotations

import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
MODULE_PATH = (
    ROOT
    / "benchmarks"
    / "python"
    / "prefilter"
    / "structural_amplification_verifier.py"
)


def load_module():
    """Load the structural amplification verifier from its file path."""
    spec = importlib.util.spec_from_file_location(
        "structural_amplification_verifier", MODULE_PATH
    )
    if spec is None or spec.loader is None:
        raise RuntimeError("Unable to load structural amplification verifier module")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_parse_schedule_tokens_requires_increasing_even_sizes():
    """The verifier should accept only increasing even RSA bit sizes."""
    module = load_module()

    schedule = module.parse_schedule_tokens(["64:2", "128:1", "256:1"])

    assert schedule == [(64, 2), (128, 1), (256, 1)]


def test_run_verification_writes_full_artifact_set(tmp_path):
    """A small deterministic panel should produce the expected report and plots."""
    module = load_module()

    results = module.run_verification(
        output_dir=tmp_path,
        schedule=[(64, 2), (128, 1), (256, 1)],
        repetitions=2,
        evaluation_min_rsa_bits=64,
        rejection_stability_tolerance=0.50,
        public_exponent=65537,
        namespace="unit-structural-amplification",
    )

    assert [row["rsa_bits"] for row in results["rows"]] == [64, 128, 256]
    assert all(row["repeat_count"] == 2 for row in results["rows"])
    assert all(row["matching_keypairs"] == row["keypair_count"] for row in results["rows"])
    assert results["analysis"]["verdict"] in {"verified", "falsified", "incomplete"}
    assert (tmp_path / "structural_amplification_results.json").exists()
    assert (tmp_path / "structural_amplification_results.csv").exists()
    assert (tmp_path / "STRUCTURAL_AMPLIFICATION_REPORT.md").exists()
    assert (tmp_path / "structural_amplification_speedup.svg").exists()
    assert (tmp_path / "structural_amplification_rejection.svg").exists()
    assert (tmp_path / "structural_amplification_costs.svg").exists()
