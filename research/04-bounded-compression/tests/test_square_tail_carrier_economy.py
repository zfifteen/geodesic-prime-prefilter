"""Tests for square-tail carrier-economy audits."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
SCRIPT_PATH = (
    ROOT
    / "research"
    / "04-bounded-compression"
    / "scripts"
    / "square_tail_carrier_economy.py"
)


def load_module():
    """Load the carrier-economy module directly from its path."""
    spec = importlib.util.spec_from_file_location("square_tail_carrier_economy", SCRIPT_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("unable to load square_tail_carrier_economy")
    module = importlib.util.module_from_spec(spec)
    sys.modules["square_tail_carrier_economy"] = module
    spec.loader.exec_module(module)
    return module


def test_root_509_carrier_economy_matches_known_prefix():
    """The 509 square-tail prefix has the expected carrier split."""
    module = load_module()
    payload = module.build_carrier_economy(509)

    assert payload["full_counterexample_even_count"] == 39
    assert payload["obstruction_prefix_even_count"] == 23
    assert payload["distinct_factor_count"] == 12
    assert payload["repeat_factor_count"] == 8
    assert payload["singleton_factor_count"] == 4
    assert payload["prefix_singleton_row_count"] == 4
    assert payload["repeat_covered_count"] == 28
    assert payload["all_prefix_factor_covered_count"] == 32
    assert payload["repeat_uncovered_count"] == 11
    assert payload["all_prefix_factor_uncovered_count"] == 7


def test_record_root_carrier_economy_exposes_singleton_burden():
    """The record root relies on singleton carriers for most suffix fill."""
    module = load_module()
    payload = module.build_carrier_economy(424_171_123)

    assert payload["full_counterexample_even_count"] == 395
    assert payload["obstruction_prefix_even_count"] == 368
    assert payload["distinct_factor_count"] == 99
    assert payload["repeat_factor_count"] == 43
    assert payload["singleton_factor_count"] == 56
    assert payload["prefix_singleton_row_count"] == 56
    assert payload["repeat_covered_count"] == 329
    assert payload["all_prefix_factor_covered_count"] == 385
    assert payload["repeat_uncovered_count"] == 66
    assert payload["all_prefix_factor_uncovered_count"] == 10
