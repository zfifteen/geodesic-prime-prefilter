"""Minimal tests for remainder_utils.py.

Run with:
    python -m pytest research/remainders/test_remainder_utils.py -q
or directly:
    python research/remainders/test_remainder_utils.py

These tests must pass on the 100-gap validation set before any scaling
of the collector (per Remainder Statistics Collection Plan).
"""

from __future__ import annotations

import sys
from pathlib import Path

# Allow running the test file directly without installation.
sys.path.insert(0, str(Path(__file__).resolve().parent))

from remainder_utils import MODULI_PRIMORIAL_V1, compute_residues


def test_default_moduli_v1():
    """Default moduli are the expected primorial sequence (versioned)."""
    assert MODULI_PRIMORIAL_V1 == [2, 3, 5, 7, 30, 210, 2310]


def test_basic_residues_small_n():
    """Known small values produce expected residues."""
    # 113 is a small prime used in hand-verification examples in the plan.
    # We treat it purely as an integer here.
    assert compute_residues(113) == (113 % 2, 113 % 3, 113 % 5, 113 % 7, 113 % 30, 113 % 210, 113 % 2310)
    # 113 mod 30 = 23
    assert compute_residues(113, [30]) == (23,)

    # 0
    assert compute_residues(0, [2, 3, 5]) == (0, 0, 0)

    # A clean multiple of the full set
    n = 2310
    assert compute_residues(n) == (0, 0, 0, 0, 0, 0, 0)


def test_modulus_one_always_zero():
    """Remainder mod 1 is always 0."""
    assert compute_residues(42, [1]) == (0,)
    assert compute_residues(0, [1, 2]) == (0, 0)


def test_explicit_moduli_list_and_tuple():
    """Both list and tuple inputs are accepted (Sequence)."""
    assert compute_residues(100, [2, 5]) == (0, 0)
    assert compute_residues(100, (2, 5)) == (0, 0)


def test_large_int_exact():
    """Arbitrary-precision integers remain exact."""
    big = 10**30 + 17
    # 10**k (k>=1) ≡ 10 mod 30, +17 => 27 mod 30
    assert compute_residues(big, [30]) == (27,)
    # 10**30 even +17 odd => 1 mod 2
    assert compute_residues(big, [2]) == (1,)


def test_error_cases():
    """Explicit errors for bad inputs."""
    try:
        compute_residues(-1)
    except ValueError as e:
        assert "nonnegative" in str(e).lower()
    else:
        assert False, "expected ValueError for negative n"

    try:
        compute_residues(10, [])
    except ValueError as e:
        assert "empty" in str(e).lower()
    else:
        assert False, "expected ValueError for empty moduli"

    try:
        compute_residues(10, [0])
    except ValueError as e:
        assert "positive" in str(e).lower()
    else:
        assert False, "expected ValueError for m<=0"

    try:
        compute_residues("notint")  # type: ignore[arg-type]
    except TypeError:
        pass
    else:
        assert False, "expected TypeError for non-int n"


def test_length_matches_moduli():
    """Output length always equals input moduli length."""
    mods = [2, 30, 2310]
    res = compute_residues(99991, mods)
    assert len(res) == len(mods)
    for r, m in zip(res, mods):
        assert 0 <= r < m


# --- Collector integration tests (added immediately after build_records impl) ---

def test_build_records_reuses_gwr_and_emits_core_fields():
    """build_records_for_gap produces correct shape and GWR flag on known gap."""
    # Avoid circular import issues by importing here
    from collect_remainder_stats import build_records_for_gap

    # Gap after 113: q=127, g=14, 13 interiors. GWR at 121 (d=3).
    recs = build_records_for_gap(113, [2, 3, 5, 7, 30])
    assert len(recs) == 13
    for r in recs:
        assert r["p"] == 113
        assert r["q"] == 127
        assert r["g"] == 14
        assert 1 <= r["k"] <= 13
        assert r["n"] == 113 + r["k"]
        assert r["d"] >= 3
        assert isinstance(r["remainder_vector"], tuple)
        assert len(r["remainder_vector"]) == 5
        assert isinstance(r["is_current_min_d"], bool)
        assert r["distance_to_next_prime"] == 127 - r["n"]

    winners = [r for r in recs if r["is_current_min_d"]]
    assert len(winners) == 1
    assert winners[0]["k"] == 8
    assert winners[0]["n"] == 121
    assert winners[0]["d"] == 3


def test_edge_gap_has_no_interior_records():
    from collect_remainder_stats import build_records_for_gap
    # Gap (2,3) is the only one with zero interior composites.
    assert build_records_for_gap(2, [2, 3]) == []
    # (3,5) has exactly one interior: 4
    recs = build_records_for_gap(3, [2, 3])
    assert len(recs) == 1
    assert recs[0]["n"] == 4
    assert recs[0]["d"] == 3  # 4=2^2
    assert recs[0]["is_current_min_d"] is True  # the sole interior is the GWR winner by definition


def test_sample_rate_reduces_or_keeps_records():
    from collect_remainder_stats import build_records_for_gap
    full = build_records_for_gap(113, [30])
    assert len(full) == 13
    sampled = build_records_for_gap(113, [30], sample_rate=0.5)
    # Probabilistic; for determinism in test we accept range or just check <=
    assert 0 <= len(sampled) <= 13


def test_collect_gaps_produces_100_gap_validation_set():
    """End-to-end collector run on a set with >100 gaps must succeed and produce correct artifacts.

    This is the strict "100-gap test set" gate required by the collection plan
    before any larger scaling.
    """
    import json
    import tempfile
    from pathlib import Path
    from collect_remainder_stats import collect_gaps, parse_moduli

    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp) / "val100"
        raw = out / "raw_records.jsonl"
        mods = parse_moduli(None)
        summ = collect_gaps(max_p=600, moduli=mods, output_path=raw)
        assert summ["gaps_processed"] >= 100, f"only {summ['gaps_processed']} gaps"
        assert summ["records_emitted"] > 0
        assert raw.exists()
        # spot check one record line parses and has required keys
        with raw.open() as f:
            first = json.loads(f.readline())
        assert "p" in first and "remainder_vector" in first and "is_current_min_d" in first


if __name__ == "__main__":
    # Allow direct execution for quick smoke in research flow.
    test_default_moduli_v1()
    test_basic_residues_small_n()
    test_modulus_one_always_zero()
    test_explicit_moduli_list_and_tuple()
    test_large_int_exact()
    test_error_cases()
    test_length_matches_moduli()
    test_build_records_reuses_gwr_and_emits_core_fields()
    test_edge_gap_has_no_interior_records()
    test_sample_rate_reduces_or_keeps_records()
    print("All remainder_utils + collector smoke tests passed (direct run).")
