#!/usr/bin/env python3
"""Local unit checks for parity-bias probe (not a 10^18 surface)."""

from __future__ import annotations

from probe_parity_bias import (
    PINNED_GWR_CE,
    divisor_counts,
    min_tau_set,
    run_probe,
    zcount,
)


def test_z4_implies_even() -> None:
    """Primary mismatch gate is impossible on odd witnesses (M_v1 structure)."""
    for n in range(1, 5000, 2):
        assert zcount(n) < 4
    # Multiples of 30 are even and have z >= 4.
    assert 30 % 2 == 0
    assert zcount(30) >= 4
    assert zcount(210) >= 5


def test_odd_can_reach_z3() -> None:
    """Non-degenerate control: odd n can hit z >= 3 via 3,5,7."""
    # 3*5*7 = 105 is odd; zeros on 3,5,7 (and not 2/30/210/2310).
    assert 105 % 2 == 1
    assert zcount(105) == 3


def test_pinned_ce_is_left_endpoint_even() -> None:
    """Both mod30-adjacent CEs: GWR witness is p+1 (even) on multi-way ties."""
    for ce in PINNED_GWR_CE:
        hard = ce["q"] + 10
        tau = divisor_counts(hard)
        mins = min_tau_set(ce["p"], ce["q"], tau)
        assert mins[0] == ce["w"]
        assert ce["w"] == ce["p"] + 1
        assert ce["w"] % 2 == 0
        assert zcount(ce["w"]) >= 4
        # Rightmost escapes the primary mismatch.
        assert zcount(mins[-1]) < 4
        assert len(mins) > 1


def test_smoke_regime_parity_structure() -> None:
    """Small regime: odd GWR mismatch_z4 stays 0; tables are populated."""
    result = run_probe(p_max=5_000, p_min=11, sample_cap=5)
    assert result["status"] == "measured"
    assert result["regime"]["gaps_scanned"] > 100
    odd = result["probe1_parity_gwr"]["odd"]
    even = result["probe1_parity_gwr"]["even"]
    assert odd["mismatch_z4"] == 0
    assert odd["z4"] == 0
    assert even["gaps"] > 0
    # Twin interiors force even GWR (p+1).
    assert even["w_is_p1"] >= result["regime"]["twins_g2"]


def test_twin_gap_selects_p1() -> None:
    tau = divisor_counts(20)
    mins = min_tau_set(11, 13, tau)
    assert mins == [12]
