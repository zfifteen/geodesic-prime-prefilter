"""Local unit checks for F18-004 audit helpers (not a 10^18 surface)."""

from __future__ import annotations

import importlib.util
import math
import sys
from pathlib import Path

SCRIPT = (
    Path(__file__).resolve().parents[1]
    / "scripts"
    / "near_maximal_witness_audit.py"
)


def load_mod():
    spec = importlib.util.spec_from_file_location("near_maximal_witness_audit", SCRIPT)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


def test_compression_bound_matches_packaging():
    m = load_mod()
    assert m.compression_bound(3) == 64
    q = 15_437_053
    lq = math.log(q)
    expected = max(64, math.ceil(0.5 * lq * lq))
    assert m.compression_bound(q) == expected


def test_f18_004_falsifier_definition():
    m = load_mod()
    # Non-square, high ratio, q large, d below rough floor -> falsifier.
    bad = m.GapCase(
        p=10_000_000,
        q=10_000_100,
        w=10_000_050,
        d=4,
        offset=50,
        C=64,
        ratio=0.90,
        logq=math.log(10_000_100),
        is_prime_square=False,
    )
    assert bad.rough_floor(0.75) >= 6
    assert bad.is_f18_004_falsifier(0.65, 10_000_000, 0.75)

    # Prime square high ratio is not an F18-004 non-square falsifier.
    square = m.GapCase(
        p=15_436_943,
        q=15_437_053,
        w=15_437_041,
        d=3,
        offset=98,
        C=137,
        ratio=0.715,
        logq=math.log(15_437_053),
        is_prime_square=True,
    )
    assert not square.is_f18_004_falsifier(0.65, 10_000_000, 0.75)

    # q too small: not counted under q_min gate.
    small_q = m.GapCase(
        p=100,
        q=110,
        w=105,
        d=4,
        offset=5,
        C=64,
        ratio=0.90,
        logq=math.log(110),
        is_prime_square=False,
    )
    assert not small_q.is_f18_004_falsifier(0.65, 10_000_000, 0.75)


def test_smoke_scan_tiny_limit():
    m = load_mod()
    cases, max_case, total = m.scan_gaps(limit=200, progress_every=0)
    assert total > 0
    assert max_case is not None
    assert all(c.offset >= 0 for c in cases)
    assert all(c.d >= 2 for c in cases)
    results = m.build_results(
        limit=200,
        ratio_threshold=0.65,
        q_min=10_000_000,
        d_log_coeff=0.75,
        cases=cases,
        max_case=max_case,
        total_gaps=total,
        ratio_levels=[0.50, 0.65],
    )
    assert results["status"] == "measured"
    assert results["f18_004_falsifiers_count"] == 0  # q_min gates all tiny-q cases
    assert len(results["threshold_matrix"]) == 2
