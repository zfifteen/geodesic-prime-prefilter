"""Unit tests for chamber_compression shipped functions."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[3]
SRC = REPO_ROOT / "src" / "python"
EMP = REPO_ROOT / "research" / "19-rh-corpus" / "empirics"
for path in (SRC, EMP):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from chamber_compression import analyze_chamber_gap, f18_branch_label


def test_exact_zero_excess_used_in_budget():
    report = analyze_chamber_gap(89, 97)
    assert report.excess_budget > 0
    assert report.load_budget > report.excess_budget


def test_f18_branch_labels():
    assert f18_branch_label(25, 3, 29, 2) == "prime_square"
    assert f18_branch_label(91, 4, 97, 2) == "non_square_subthreshold"
    assert f18_branch_label(15437041, 3, 15437053, 98) == "prime_square"