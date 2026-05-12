"""Tests for the adjacent-pair closure certificate helper."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
SCRIPT_PATH = (
    ROOT
    / "research"
    / "02-gwr-dni"
    / "scripts"
    / "proof"
    / "adjacent_pair_closure_certificate.py"
)


def load_module():
    """Load the certificate module directly from its file path."""
    spec = importlib.util.spec_from_file_location("adjacent_pair_closure_certificate", SCRIPT_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("Unable to load adjacent_pair_closure_certificate")
    module = importlib.util.module_from_spec(spec)
    sys.modules["adjacent_pair_closure_certificate"] = module
    spec.loader.exec_module(module)
    return module


def test_ratio_rows_close_reviewer_pairs():
    """The large-prime ratio rows close every reviewer-cited pair."""
    module = load_module()
    rows = module.ratio_rows(5_000_000_000)

    assert [(row["winner_divisor_count"], row["earlier_divisor_count"]) for row in rows] == [
        (36, 37),
        (64, 65),
        (72, 73),
    ]
    assert all(row["eliminated"] is True for row in rows)


def test_tau_65_patterns_are_the_expected_square_patterns():
    """The tau-65 branch has the two exponent patterns used by the certificate."""
    module = load_module()

    assert module.exponent_patterns(65) == [(64,), (12, 4)]
