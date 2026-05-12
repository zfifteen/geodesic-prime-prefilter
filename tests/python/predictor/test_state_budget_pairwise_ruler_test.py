"""Tests for the state-budget pairwise ruler test."""

from __future__ import annotations

import csv
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
MODULE_PATH = (
    ROOT
    / "benchmarks"
    / "python"
    / "predictor"
    / "state_budget_pairwise_ruler_test.py"
)


def load_module():
    """Load the pairwise ruler test runner from disk."""
    spec = importlib.util.spec_from_file_location(
        "state_budget_pairwise_ruler_test",
        MODULE_PATH,
    )
    if spec is None or spec.loader is None:
        raise RuntimeError("unable to load state_budget_pairwise_ruler_test")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_compare_pairs_counts_lower_target_values_as_positive():
    """Target rows below non-target rows on the ruler produce positive signed wins."""
    module = load_module()
    targets = [{"square_ruler": 0.1}, {"square_ruler": 0.4}]
    non_targets = [{"square_ruler": 0.3}, {"square_ruler": 0.5}]

    pairs, signed_advantage, ties = module.compare_pairs(
        targets,
        non_targets,
        value_field="square_ruler",
    )

    assert pairs == 4
    assert signed_advantage == 2
    assert ties == 0


def test_retained_surface_pairwise_result_is_current_lab_readout():
    """The current surface has positive but not separated square-ruler advantage."""
    module = load_module()

    _per_power, summary = module.evaluate_surface(
        module.DEFAULT_DETAIL_CSV,
        min_power=12,
        max_power=18,
        min_class_count=1,
        min_decisive_pairs=100,
        min_control_margin=15,
    )
    square, tail = summary["measure_summaries"]

    assert summary["verdict"] == "unresolved"
    assert square["measure"] == "square_ruler"
    assert square["eligible_cells"] == 152
    assert square["decisive_pairs"] == 589
    assert square["signed_advantage"] == 73
    assert tail["measure"] == "tail_length"
    assert tail["signed_advantage"] == 70
    assert square["signed_advantage"] > tail["signed_advantage"]


def test_cli_writes_lf_artifacts(tmp_path):
    """The CLI should emit per-power CSV and summary JSON artifacts."""
    module = load_module()

    assert module.main(["--output-dir", str(tmp_path)]) == 0

    per_power_path = tmp_path / "state_budget_pairwise_ruler_per_power.csv"
    summary_path = tmp_path / "state_budget_pairwise_ruler_summary.json"
    assert b"\r\n" not in per_power_path.read_bytes()
    assert b"\r\n" not in summary_path.read_bytes()

    with per_power_path.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    payload = json.loads(summary_path.read_text(encoding="utf-8"))

    assert len(rows) == 14
    assert rows[0]["measure"] == "square_ruler"
    assert rows[-1]["measure"] == "tail_length"
    assert payload["verdict"] == "unresolved"
