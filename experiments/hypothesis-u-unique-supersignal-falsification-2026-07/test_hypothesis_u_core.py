"""Unit tests for Hypothesis U experiment decision core (shipped functions)."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def _load_mod():
    path = HERE / "run_hypothesis_u.py"
    spec = importlib.util.spec_from_file_location("run_hypothesis_u", path)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    sys.modules["run_hypothesis_u"] = mod
    spec.loader.exec_module(mod)
    return mod


def test_known_bare_supersignal_ce_is_not_hypothesis_u_ce():
    """Pinned bare Super-Signal CE has ties>1 so does NOT falsify Hypothesis U."""
    mod = _load_mod()
    import sympy as sp

    p, q = 17_666_309, 17_666_317
    assert sp.isprime(p) and sp.isprime(q)
    assert sp.nextprime(p) == q
    w, tw, ties = mod.gwr_from_tau_segment(p, q, lambda n: int(sp.divisor_count(n)))
    flags = mod.classify_gap(p, q, w, tw, ties)
    assert w == 17_666_310
    assert flags["z"] >= 4
    assert flags["g"] == 8
    assert flags["ties"] > 1
    assert flags["bare_z4_fp"] is True
    assert flags["hypothesis_u_ce"] is False
    assert flags["hypothesis_u_hit"] is False


def test_twin_gap_30_is_hypothesis_u_hit_not_ce():
    """Classic twin 29,31 with w=30: unique min + z>=4 + g=2 → hit, not CE."""
    mod = _load_mod()
    import sympy as sp

    p, q = 29, 31
    w, tw, ties = mod.gwr_from_tau_segment(p, q, lambda n: int(sp.divisor_count(n)))
    flags = mod.classify_gap(p, q, w, tw, ties)
    assert w == 30
    assert flags["z"] >= 4
    assert flags["ties"] == 1
    assert flags["g"] == 2
    assert flags["hypothesis_u_hit"] is True
    assert flags["hypothesis_u_ce"] is False
    assert flags["bare_z4_fp"] is False


def test_zcount_modular_half_on_known_values():
    mod = _load_mod()
    assert mod.zcount(30) >= 4
    assert mod.zcount(210) >= 6
    assert mod.zcount(31) == 0
    # no integer with exactly 5 zeros on M_v1 in 1..1000
    assert all(mod.zcount(n) != 5 for n in range(1, 1001))


def test_pinned_hypothesis_u_counterexample_is_ce():
    """Experiment CE p=156942923 falsifies unique-min Super-Signal repair."""
    mod = _load_mod()
    import sympy as sp

    p, q = 156_942_923, 156_942_931
    assert sp.isprime(p) and sp.isprime(q) and sp.nextprime(p) == q
    w, tw, ties = mod.gwr_from_tau_segment(p, q, lambda n: int(sp.divisor_count(n)))
    flags = mod.classify_gap(p, q, w, tw, ties)
    assert w == 156_942_930
    assert tw == 16
    assert ties == 1
    assert flags["z"] >= 4
    assert flags["g"] == 8
    assert flags["hypothesis_u_ce"] is True
