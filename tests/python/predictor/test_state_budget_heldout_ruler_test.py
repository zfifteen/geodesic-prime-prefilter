"""Tests for the state-budget held-out ruler test."""

from __future__ import annotations

import csv
import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
MODULE_PATH = (
    ROOT
    / "benchmarks"
    / "python"
    / "predictor"
    / "state_budget_heldout_ruler_test.py"
)


def load_module():
    """Load the held-out ruler test runner from disk."""
    spec = importlib.util.spec_from_file_location(
        "state_budget_heldout_ruler_test",
        MODULE_PATH,
    )
    if spec is None or spec.loader is None:
        raise RuntimeError("unable to load state_budget_heldout_ruler_test")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_median_by_cell_keeps_only_cells_with_both_classes():
    """A training cell must split into real low and high classes."""
    module = load_module()
    split_key_rows = [
        {
            "current_next_dmin": 4,
            "previous_reduced_state": "prev",
            "current_winner_parity": "odd",
            "current_carrier_family": "odd_semiprime",
            "current_winner_offset": 2,
            "current_first_open_offset": 4,
            "square_budget": 0.1,
        },
        {
            "current_next_dmin": 4,
            "previous_reduced_state": "prev",
            "current_winner_parity": "odd",
            "current_carrier_family": "odd_semiprime",
            "current_winner_offset": 2,
            "current_first_open_offset": 4,
            "square_budget": 0.4,
        },
        {
            "current_next_dmin": 4,
            "previous_reduced_state": "prev",
            "current_winner_parity": "odd",
            "current_carrier_family": "odd_semiprime",
            "current_winner_offset": 2,
            "current_first_open_offset": 4,
            "square_budget": 0.9,
        },
    ]
    single_key_rows = [
        {
            "current_next_dmin": 4,
            "previous_reduced_state": "single",
            "current_winner_parity": "odd",
            "current_carrier_family": "odd_semiprime",
            "current_winner_offset": 2,
            "current_first_open_offset": 4,
            "square_budget": 0.2,
        }
    ]

    medians = module.median_by_cell(split_key_rows + single_key_rows, "square_budget")

    assert len(medians) == 1
    assert medians[
        (
            "prev",
            "odd",
            "odd_semiprime",
            2,
            4,
        )
    ] == 0.4


def test_retained_surface_has_hard_balance_and_does_not_verdicts():
    """The current retained surface should not promote under the hard gate."""
    module = load_module()

    rows = module.evaluate_surface(
        module.DEFAULT_DETAIL_CSV,
        min_power=12,
        max_power=18,
        balance_floor=0.10,
        min_scored_rows=20,
    )
    by_power = {row["heldout_power"]: row for row in rows}

    assert len(rows) == 7
    assert by_power[12]["verdict"] == "unresolved"
    assert by_power[12]["min_class_share"] < 0.10
    assert by_power[13]["verdict"] == "does_not"
    assert by_power[14]["verdict"] == "does_not"
    assert by_power[17]["verdict"] == "does_not"
    assert by_power[18]["verdict"] == "unresolved"
    assert by_power[18]["high_count"] == 0
    assert all(row["verdict"] != "does" for row in rows)


def test_cli_writes_one_lf_csv_table(tmp_path):
    """The CLI should emit the requested single decision table."""
    module = load_module()

    assert module.main(["--output-dir", str(tmp_path)]) == 0

    path = tmp_path / "state_budget_heldout_ruler_test.csv"
    raw = path.read_bytes()
    assert b"\r\n" not in raw

    with path.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))

    assert len(rows) == 7
    assert list(rows[0]) == list(module.OUTPUT_FIELDS)
    assert rows[0]["heldout_power"] == "12"
    assert rows[-1]["heldout_power"] == "18"
