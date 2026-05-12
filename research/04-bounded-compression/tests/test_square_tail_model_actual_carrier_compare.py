"""Tests for modeled-vs-actual carrier comparisons."""

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
    / "square_tail_model_actual_carrier_compare.py"
)


def load_module():
    """Load the carrier comparison module directly from its path."""
    spec = importlib.util.spec_from_file_location("square_tail_model_actual_carrier_compare", SCRIPT_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("unable to load square_tail_model_actual_carrier_compare")
    module = importlib.util.module_from_spec(spec)
    sys.modules["square_tail_model_actual_carrier_compare"] = module
    spec.loader.exec_module(module)
    return module


def test_model_singletons_do_not_match_actual_tail_least_factors():
    """The local model carriers are distinct from actual rough-tail least factors."""
    module = load_module()
    payload = module.build_comparison()

    assert payload["actual_composite_row_count"] == 12
    assert payload["same_position_match_count"] == 0
    assert payload["any_assigned_match_count"] == 0
    assert payload["rows"][0]["m"] == 40
    assert payload["rows"][0]["actual_least_factor"] == 6_736_351
    assert payload["rows"][0]["assigned_carrier_same_m"] == 4_451
