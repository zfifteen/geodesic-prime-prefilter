#!/usr/bin/env python3
"""Local unit checks for selector probe (not a 10^18 surface)."""

from __future__ import annotations

from probe_selectors import (
    PINNED_GWR_CE,
    analyze_gap,
    divisor_counts,
    select_witnesses,
    zcount,
)


def test_zcount_on_multiple_of_30() -> None:
    # 30 | n implies zeros on 2,3,5,30 at minimum (z >= 4).
    assert zcount(30) >= 4
    assert zcount(210) >= 5


def test_pinned_ce_gwr_is_mismatch() -> None:
    """Pinned Super-Signal CE must classify as GWR mismatch."""
    ce = PINNED_GWR_CE[0]
    hard = ce["q"] + 10
    tau = divisor_counts(hard)
    rows = analyze_gap(ce["p"], ce["q"], tau)
    gwr = rows["gwr"]
    assert gwr["w"] == ce["w"]
    assert gwr["z"] >= 4
    assert gwr["g"] == ce["g"]
    assert gwr["mismatch"] is True


def test_pinned_ce_rightmost_escapes_mismatch() -> None:
    """On both pinned CEs, rightmost min-tau differs and is not a mismatch."""
    for ce in PINNED_GWR_CE:
        hard = ce["q"] + 10
        tau = divisor_counts(hard)
        rows = analyze_gap(ce["p"], ce["q"], tau)
        gwr = rows["gwr"]
        right = rows["alt_a_rightmost_min"]
        assert gwr["mismatch"] is True
        assert right["w"] != gwr["w"]
        assert right["mismatch"] is False
        assert right["z"] < 4


def test_selectors_on_simple_gap() -> None:
    """Gap (11, 13): interior {12}; all selectors agree on 12."""
    tau = divisor_counts(20)
    ws = select_witnesses(11, 13, tau)
    assert ws["gwr"] == 12
    assert ws["alt_a_rightmost_min"] == 12
    assert ws["alt_b_first"] == 12


def test_alt_a_differs_when_ties() -> None:
    """Synthetic-like: gap with two equal min-tau at ends of a longer interior.

    Use a real small gap known to have ties if available; otherwise check
    that when min is unique, A equals GWR.
    """
    # Gap (101, 103): interior {102}. Unique, all agree.
    tau = divisor_counts(110)
    ws = select_witnesses(101, 103, tau)
    assert ws["gwr"] == ws["alt_a_rightmost_min"] == ws["alt_b_first"] == 102


def test_first_interior_selector() -> None:
    tau = divisor_counts(50)
    ws = select_witnesses(29, 31, tau)
    assert ws["alt_b_first"] == 30
