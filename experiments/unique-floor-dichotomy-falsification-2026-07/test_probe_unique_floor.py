#!/usr/bin/env python3
"""Local unit checks for unique-floor dichotomy probe."""

from __future__ import annotations

from probe_unique_floor import analyze_gap, divisor_counts, run_probe, u1_ceiling


def test_u1_ceiling_schedule():
    assert u1_ceiling(2_000_000, 100) == 40
    assert u1_ceiling(5_000_000, 100) == 40
    assert u1_ceiling(10_000_000, 10**6) >= 48


def test_analyze_gap_fields():
    tau = divisor_counts(100)
    row = analyze_gap(23, 29, tau)
    assert row is not None
    assert row["g"] == 6
    assert row["L_size"] >= 1
    assert row["unique"] == (row["L_size"] == 1)


def test_run_probe_smoke():
    result = run_probe(p_max=800, p_min=11)
    assert result["counts"]["gaps_nonempty"] > 0
    assert result["status_language"] == "measured_on_regime_only"
    blob = str(result).lower()
    assert "validated" not in blob
    assert "verified" not in blob


def test_outcomes_keys():
    result = run_probe(p_max=500, p_min=11)
    for k in (
        "U1_unique_m4_short_gap",
        "U2_long_m4_multi_rate",
        "U3_unique_high_floor_short",
        "U4_square_long_unique_contrast",
    ):
        assert k in result["outcomes"]
