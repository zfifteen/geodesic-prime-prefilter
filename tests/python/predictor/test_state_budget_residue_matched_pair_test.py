"""Tests for the state-budget residue-matched pairwise ruler test."""

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
    / "state_budget_residue_matched_pair_test.py"
)


def load_module():
    """Load the residue-matched pairwise test runner from disk."""
    spec = importlib.util.spec_from_file_location(
        "state_budget_residue_matched_pair_test",
        MODULE_PATH,
    )
    if spec is None or spec.loader is None:
        raise RuntimeError("unable to load state_budget_residue_matched_pair_test")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_match_keys_add_residue_context_incrementally():
    """Residue match modes should preserve the base key and add context."""
    module = load_module()
    row = {
        "previous_reduced_state": "o2_odd_semiprime|d<=4",
        "current_winner_parity": "odd",
        "current_carrier_family": "odd_semiprime",
        "current_winner_offset": 2,
        "current_first_open_offset": 4,
        "left_prime_mod30": 17,
        "left_prime_mod210": 107,
        "previous_gap_width": 12,
    }

    base = module.matched_key(row, "base")

    assert module.matched_key(row, "mod30") == (*base, 17)
    assert module.matched_key(row, "mod30_prev_gap") == (*base, 17, 12)
    assert module.matched_key(row, "mod210") == (*base, 107)


def test_retained_surface_residue_results_are_current_readout():
    """The current retained surface keeps positive but unresolved residue results."""
    module = load_module()
    _per_power, summary = module.evaluate_surface(
        module.DEFAULT_DETAIL_CSV,
        min_power=12,
        max_power=18,
        min_class_count=1,
        min_decisive_pairs=100,
        min_control_margin=15,
    )
    by_mode = {row["match_mode"]: row for row in summary["mode_summaries"]}
    mod30_square, mod30_tail = by_mode["mod30"]["measure_summaries"]
    mod30_prev_square, _mod30_prev_tail = by_mode["mod30_prev_gap"]["measure_summaries"]

    assert by_mode["base"]["verdict"] == "unresolved"
    assert by_mode["mod30"]["verdict"] == "unresolved"
    assert mod30_square["decisive_pairs"] == 230
    assert mod30_square["signed_advantage"] == 40
    assert mod30_tail["signed_advantage"] == 33
    assert mod30_square["signed_advantage"] > mod30_tail["signed_advantage"]
    assert by_mode["mod30_prev_gap"]["verdict"] == "unresolved"
    assert mod30_prev_square["decisive_pairs"] < 100


def test_cli_writes_lf_artifacts(tmp_path):
    """The CLI should emit per-power CSV and summary JSON artifacts."""
    module = load_module()

    assert module.main(["--output-dir", str(tmp_path)]) == 0

    per_power_path = tmp_path / "state_budget_residue_matched_pair_per_power.csv"
    summary_path = tmp_path / "state_budget_residue_matched_pair_summary.json"
    assert b"\r\n" not in per_power_path.read_bytes()
    assert b"\r\n" not in summary_path.read_bytes()

    with per_power_path.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    payload = json.loads(summary_path.read_text(encoding="utf-8"))

    assert len(rows) == 56
    assert payload["mode_summaries"][1]["match_mode"] == "mod30"
    assert payload["mode_summaries"][1]["verdict"] == "unresolved"
