"""Tests for the state-budget forbidden-transition runner."""

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
    / "state_budget_forbidden_transition_test.py"
)


def load_module():
    """Load the forbidden-transition runner from disk."""
    spec = importlib.util.spec_from_file_location(
        "state_budget_forbidden_transition_test",
        MODULE_PATH,
    )
    if spec is None or spec.loader is None:
        raise RuntimeError("unable to load state_budget_forbidden_transition_test")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_match_keys_add_context_incrementally():
    """Match modes should preserve the base PGS chamber cell and add context."""
    module = load_module()
    row = {
        "previous_reduced_state": "o2_odd_semiprime|d<=4",
        "current_winner_parity": "odd",
        "current_carrier_family": "odd_semiprime",
        "current_winner_offset": 2,
        "current_first_open_offset": 4,
        "endpoint_mod30": 17,
        "tail_length": 6,
    }

    base = module.match_key(row, "base")

    assert module.match_key(row, "mod30") == (*base, 17)
    assert module.match_key(row, "exact_tail") == (*base, 6)
    assert module.match_key(row, "mod30_exact_tail") == (*base, 17, 6)


def test_retained_surface_forbidden_transition_result_is_negative():
    """The current retained surface rejects exact next-state exclusion."""
    module = load_module()
    _folds, summary = module.evaluate_surface(
        module.DEFAULT_DETAIL_CSV,
        min_power=12,
        max_power=18,
    )
    by_mode = {row["match_mode"]: row for row in summary["modes"]}

    assert by_mode["base"]["verdict"] == "does_not"
    assert by_mode["base"]["eligible_rows"] == 703
    assert by_mode["base"]["violations"] == 227
    assert by_mode["exact_tail"]["verdict"] == "unresolved"
    assert by_mode["exact_tail"]["eligible_rows"] == 4
    assert by_mode["exact_tail"]["violations"] == 0


def test_cli_writes_lf_artifacts(tmp_path):
    """The CLI should emit per-fold CSV and summary JSON artifacts."""
    module = load_module()

    assert module.main(["--output-dir", str(tmp_path)]) == 0

    fold_path = tmp_path / "state_budget_forbidden_transition_folds.csv"
    summary_path = tmp_path / "state_budget_forbidden_transition_summary.json"
    assert b"\r\n" not in fold_path.read_bytes()
    assert b"\r\n" not in summary_path.read_bytes()

    with fold_path.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    payload = json.loads(summary_path.read_text(encoding="utf-8"))

    assert len(rows) == 28
    assert rows[0]["match_mode"] == "base"
    assert payload["modes"][0]["verdict"] == "does_not"
