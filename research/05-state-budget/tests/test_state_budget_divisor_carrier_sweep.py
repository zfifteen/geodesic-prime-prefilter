"""Tests for the state-budget divisor-carrier sweep."""

from __future__ import annotations

import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
MODULE_PATH = ROOT / "research" / "05-state-budget" / "scripts" / "state_budget_divisor_carrier_sweep.py"


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


# =============================================================================
# Phase 3 square-phase attachment test (T-001 Rank #2 continuation)
# =============================================================================
# Exercises the first implemented unit (attach_square_phase_utilization)
# against a tiny synthetic surface that mimics the 12-13 d=4 geometry.
# The test lives in the audited carrier-sweep test module so that the
# protocol machinery and the new attachment stay co-located and cross-checked.


def test_attach_square_phase_utilization_on_synthetic_d4_slice():
    """
    The attach function must produce the three documented fields for d=4
    rows, label them d4_low / d4_high inside each geometry cell by median,
    mark non-d=4 rows cleanly, and remain strictly additive.
    """
    # Dynamic import of the probe (avoids polluting the test module namespace
    # and mirrors how the existing tests load the sweep machinery).
    import importlib.util
    import sys
    from pathlib import Path

    probe_path = (
        Path(__file__).resolve().parents[3]
        / "research"
        / "16-predictions"
        / "scripts"
        / "w_offset_carrier_probe.py"
    )
    spec = importlib.util.spec_from_file_location(
        "w_offset_carrier_probe", probe_path
    )
    if spec is None or spec.loader is None:
        raise RuntimeError("unable to load w_offset_carrier_probe for test")
    probe = importlib.util.module_from_spec(spec)
    # Ensure the probe can resolve its internal 05 imports.
    sys.path.insert(0, str(probe_path.parents[2] / "05-state-budget" / "scripts"))
    spec.loader.exec_module(probe)

    attach = probe.attach_square_phase_utilization

    # Two geometry cells. The first cell deliberately contains two d=4
    # transitions that share the same (family, w_off, first_open) label
    # but come from different chambers (different right edges) so they
    # receive distinct U_□ values and therefore opposite low/high labels
    # after the median split. This exercises the exact grouping + labeling
    # logic from the 05 audited precedent.
    synthetic_transitions = [
        {
            "surface_label": "10^12",
            "current_carrier_family": "even_semiprime",
            "current_winner_offset": 5,
            "current_first_open_offset": 3,
            "current_next_dmin": 4,
            "d4_count": 12,
            "current_right_prime": 1000000000123,
            "target_w_offset": 7,
        },
        {
            "surface_label": "10^12",
            "current_carrier_family": "even_semiprime",
            "current_winner_offset": 5,
            "current_first_open_offset": 3,
            "current_next_dmin": 4,
            "d4_count": 9,
            "current_right_prime": 1000000000157,  # different chamber, same geometry key
            "target_w_offset": 4,
        },
        {
            "surface_label": "10^12",
            "current_carrier_family": "odd_semiprime",
            "current_winner_offset": 2,
            "current_first_open_offset": 1,
            "current_next_dmin": 4,
            "d4_count": 7,
            "current_right_prime": 1000000000099,
            "target_w_offset": 9,
        },
        {
            "surface_label": "10^12",
            "current_carrier_family": "odd_semiprime",
            "current_winner_offset": 2,
            "current_first_open_offset": 1,
            "current_next_dmin": 4,
            "d4_count": 11,
            "current_right_prime": 1000000000099,
            "target_w_offset": 3,
        },
        {
            "surface_label": "10^12",
            "current_carrier_family": "even_semiprime",
            "current_winner_offset": 1,
            "current_first_open_offset": 0,
            "current_next_dmin": 6,  # not d=4
            "d4_count": 0,
            "current_right_prime": 1000000000050,
            "target_w_offset": 2,
        },
    ]

    # Detail rows now supply two distinct right edges for the even cell
    # so the two transitions receive different U_□ values.
    synthetic_detail = [
        {
            "surface_label": "10^12",
            "next_right_prime": 1000000000123,
            "next_peak_offset": 1000000000118,
            "next_dmin": 4,
            "carrier_family": "even_semiprime",
            "first_open_offset": 3,
            "power": 12,
        },
        {
            "surface_label": "10^12",
            "next_right_prime": 1000000000157,
            "next_peak_offset": 1000000000152,
            "next_dmin": 4,
            "carrier_family": "even_semiprime",
            "first_open_offset": 3,
            "power": 12,
        },
        {
            "surface_label": "10^12",
            "next_right_prime": 1000000000099,
            "next_peak_offset": 1000000000097,
            "next_dmin": 4,
            "carrier_family": "odd_semiprime",
            "first_open_offset": 1,
            "power": 12,
        },
    ]

    augmented = attach(synthetic_transitions, detail_rows=synthetic_detail)

    assert len(augmented) == 5
    # Original keys survive (additive contract).
    for row in augmented:
        assert "target_w_offset" in row
        assert "d4_count" in row

    # The three new fields exist on every row.
    for row in augmented:
        assert "square_phase_utilization" in row
        assert "square_phase_bit" in row
        assert "is_d4_low" in row

    # Non-d4 row receives the documented sentinel values.
    non_d4 = [r for r in augmented if r["current_next_dmin"] != 4][0]
    assert non_d4["square_phase_bit"] == "non_d4"
    assert non_d4["is_d4_low"] is None
    assert non_d4["square_phase_utilization"] is None

    # The two d=4 rows in the first geometry cell receive opposite low/high labels.
    d4_cell1 = [r for r in augmented if r["current_carrier_family"] == "even_semiprime" and r["current_next_dmin"] == 4]
    bits_cell1 = {r["square_phase_bit"] for r in d4_cell1}
    assert bits_cell1 == {"d4_low", "d4_high"}

    # The is_d4_low ints are 0/1 only for real d=4 rows.
    lows = [r["is_d4_low"] for r in d4_cell1]
    assert set(lows) == {0, 1}

    # The measure names are present in the documented extended candidate list
    # so that later scoring units can select them without further change.
    assert "square_phase_utilization" in probe.W_CANDIDATE_MEASURES_WITH_SQUARE_RESET
    assert "is_d4_low" in probe.W_CANDIDATE_MEASURES_WITH_SQUARE_RESET

    # All claims in this test are labeled measured on the synthetic surface.
    # No probabilistic language. PGS objects (d4_count field + GWR w target
    # + square U_□ after first d=4) → invariants (NLSC + match-mode cells) →
    # additional candidate carrier measure or explicit handling for non-d=4.
