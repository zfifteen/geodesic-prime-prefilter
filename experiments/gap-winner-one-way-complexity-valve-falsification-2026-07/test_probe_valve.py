#!/usr/bin/env python3
"""Local unit checks for the one-way complexity valve probe."""

from __future__ import annotations

import math

from probe_valve import (
    analyze_gap,
    divisor_counts,
    dynamic_cutoff,
    interval_mean,
    leftmost_min_tau,
    run_probe,
    spearman_rho,
)


def test_dynamic_cutoff_floor():
    assert dynamic_cutoff(11) == 64
    assert dynamic_cutoff(10**6) >= 64


def test_divisor_counts_small():
    tau = divisor_counts(20)
    assert tau[2] == 2
    assert tau[4] == 3  # 1,2,4
    assert tau[6] == 4  # 1,2,3,6
    assert tau[12] == 6


def test_leftmost_min_tau_prefers_left_tie():
    # Synthetic: force equal mins at two positions by using real field
    # on a known gap with possible ties; structural check on helper.
    tau = divisor_counts(30)
    # gap 23..29: interior 24,25,26,27,28
    w, mt = leftmost_min_tau(23, 29, tau)
    assert w == min(n for n in range(24, 29) if tau[n] == mt)
    assert all(tau[n] >= mt for n in range(24, 29))


def test_interval_mean_empty():
    tau = divisor_counts(20)
    assert interval_mean(5, 5, tau) is None
    m = interval_mean(4, 7, tau)
    assert m is not None
    assert math.isclose(m, (tau[4] + tau[5] + tau[6]) / 3)


def test_analyze_gap_eligible_structure():
    tau = divisor_counts(50)
    # 29, 31 is twin: empty interior -> None
    assert analyze_gap(29, 31, tau) is None
    # 23, 29 has interior; may or may not be both-sided
    row = analyze_gap(23, 29, tau)
    assert row is not None
    assert row.w > 23
    assert row.w < 29
    if row.eligible:
        assert row.mean_pre is not None
        assert row.mean_res is not None
        assert row.ratio is not None
        assert row.n_pre > 0 and row.n_res > 0


def test_spearman_monotone():
    xs = [1.0, 2.0, 3.0, 4.0, 5.0]
    ys = [2.0, 4.0, 6.0, 8.0, 10.0]
    rho = spearman_rho(xs, ys)
    assert rho is not None
    assert math.isclose(rho, 1.0, abs_tol=1e-9)
    rho_neg = spearman_rho(xs, list(reversed(ys)))
    assert rho_neg is not None
    assert math.isclose(rho_neg, -1.0, abs_tol=1e-9)


def test_run_probe_smoke():
    result = run_probe(p_max=500, p_min=11)
    assert result["counts"]["gaps_nonempty_interior"] > 0
    assert "H1_residual_mean_elevation" in result["outcomes"]
    assert result["status_language"] == "measured_on_regime_only"
    # No theorem language keys
    blob = str(result).lower()
    assert "validated" not in blob
    assert "verified" not in blob
