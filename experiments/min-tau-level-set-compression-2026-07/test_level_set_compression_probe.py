#!/usr/bin/env python3
"""Local unit checks for level-set compression probe (not a 10^18 surface)."""

from __future__ import annotations

import math

from level_set_compression_probe import (
    analyze_gap,
    divisor_counts,
    dynamic_cutoff,
    run_probe,
)


def test_dynamic_cutoff_matches_proof_form():
    assert dynamic_cutoff(100) == 64
    # log(e^16)^2 / 2 = 128; ceil path for large q
    q = 1_000_000
    expected = max(64, math.ceil(0.5 * (math.log(q) ** 2)))
    assert dynamic_cutoff(q) == expected


def test_known_spill_row_31397():
    """First LSC violator on the 1e5 surface: early d=4 lock, late co-minimals."""
    p, q = 31397, 31469
    tau = divisor_counts(q + 10)
    rec = analyze_gap(p, q, tau)
    assert rec is not None
    assert rec["tau_w"] == 4
    assert rec["alpha"] == 2
    assert rec["left_in_bound"] is True
    assert rec["spill"] is True
    assert rec["right_off"] > rec["C"]
    assert rec["n_ties"] >= 2


def test_leftmost_bound_holds_on_small_regime():
    result = run_probe(5_000)
    assert result["totals"]["theorem_breaks_leftmost"] == 0
    assert result["regime"]["gaps_scanned"] > 100


def test_lscd_on_small_regime_if_spill():
    result = run_probe(100_000)
    # LSC may already fail; off-d4 spill must stay zero on this band
    assert result["totals"]["spill_off_d4"] == 0
    assert result["totals"]["spill_on_square_tau3"] == 0
    assert result["totals"]["spill_on_tau_ge6"] == 0
    assert result["totals"]["spill_count"] >= 1
