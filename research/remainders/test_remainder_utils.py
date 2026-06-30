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


if __name__ == "__main__":
    # Allow direct execution for quick smoke in research flow.
    test_default_moduli_v1()
    test_basic_residues_small_n()
    test_modulus_one_always_zero()
    test_explicit_moduli_list_and_tuple()
    test_large_int_exact()
    test_error_cases()
    test_length_matches_moduli()
    print("All remainder_utils tests passed (direct run).")
