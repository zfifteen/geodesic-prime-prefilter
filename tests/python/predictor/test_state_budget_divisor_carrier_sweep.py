"""Tests for the state-budget divisor-carrier sweep."""

from __future__ import annotations

import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
MODULE_PATH = (
    ROOT
    / "benchmarks"
    / "python"
    / "predictor"
    / "state_budget_divisor_carrier_sweep.py"
)


def load_module():
    """Load the divisor-carrier sweep runner from disk."""
    spec = importlib.util.spec_from_file_location(
        "state_budget_divisor_carrier_sweep",
        MODULE_PATH,
    )
    if spec is None or spec.loader is None:
        raise RuntimeError("unable to load state_budget_divisor_carrier_sweep")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_match_keys_add_required_controls_incrementally():
    """Match modes should preserve current PGS facts and add residue/gap controls."""
    module = load_module()
    row = {
        "previous_reduced_state": "o2_odd_semiprime|d<=4",
        "current_winner_parity": "odd",
        "current_carrier_family": "odd_semiprime",
        "current_winner_offset": 2,
        "current_first_open_offset": 4,
        "endpoint_mod30": 17,
        "previous_gap_bin": "8_12",
        "previous_gap_width": 12,
    }

    mod30 = module.match_key(row, "mod30")

    assert mod30 == module.base_key(row) + (17,)
    assert module.match_key(row, "mod30_prev_gap_bin") == (*mod30, "8_12")
    assert module.match_key(row, "mod30_prev_gap_exact") == (*mod30, 12)


def test_score_rows_counts_pairwise_ordering_inside_cells():
    """Pairwise scoring should compare target and non-target rows only within cells."""
    module = load_module()
    base = {
        "previous_reduced_state": "s",
        "current_winner_parity": "odd",
        "current_carrier_family": "odd_semiprime",
        "current_winner_offset": 2,
        "current_first_open_offset": 4,
        "endpoint_mod30": 17,
        "previous_gap_bin": "8_12",
        "previous_gap_width": 12,
    }
    rows = [
        {**base, "next_is_triad": 1, "d4_count": 2},
        {**base, "next_is_triad": 1, "d4_count": 5},
        {**base, "next_is_triad": 0, "d4_count": 4},
        {**base, "next_is_triad": 0, "d4_count": 6},
    ]

    eligible_cells, pairs, signed, ties = module.score_rows(
        rows,
        match_mode="mod30_prev_gap_exact",
        measure="d4_count",
    )

    assert eligible_cells == 1
    assert pairs == 4
    assert signed == 2
    assert ties == 0


def test_summarize_measure_keeps_direction_and_support_counts():
    """Fold summaries should expose support and directional fold counts."""
    module = load_module()
    rows = [
        {
            "match_mode": "mod30",
            "measure": "d4_count",
            "measure_role": "candidate",
            "decisive_pairs": 120,
            "oriented_signed_advantage": 10,
            "eligible_cells": 3,
            "tie_pairs": 1,
        },
        {
            "match_mode": "mod30",
            "measure": "d4_count",
            "measure_role": "candidate",
            "decisive_pairs": 90,
            "oriented_signed_advantage": -4,
            "eligible_cells": 2,
            "tie_pairs": 0,
        },
    ]

    summary = module.summarize_measure(rows)

    assert summary["folds_with_min_support"] == 1
    assert summary["positive_oriented_folds"] == 1
    assert summary["negative_oriented_folds"] == 1
    assert summary["decisive_pairs"] == 210
    assert summary["oriented_signed_advantage"] == 6
