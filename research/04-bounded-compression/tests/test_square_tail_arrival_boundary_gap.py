"""Tests for arrival-boundary gap audits."""

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
    / "square_tail_arrival_boundary_gap.py"
)


def load_module():
    """Load the arrival-boundary gap module directly from its path."""
    spec = importlib.util.spec_from_file_location("square_tail_arrival_boundary_gap", SCRIPT_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("unable to load square_tail_arrival_boundary_gap")
    module = importlib.util.module_from_spec(spec)
    sys.modules["square_tail_arrival_boundary_gap"] = module
    spec.loader.exec_module(module)
    return module


def test_first_unarrived_rows_show_boundary_gap():
    """The first seven unarrived rows include six later arrivals and one prime row."""
    module = load_module()
    payload = module.build_boundary_gap(row_count=7)

    assert payload["arrival_bound"] == 1_000_000
    assert payload["dynamic_cutoff"] == 8_889
    assert payload["row_count"] == 7
    assert payload["composite_row_count"] == 6
    assert payload["prime_row_count"] == 1
    assert payload["rows"][0]["offset"] == 80
    assert payload["rows"][0]["actual_least_factor"] == 6_736_351
    assert payload["rows"][0]["least_factor_exceeds_arrival_bound"] is True
    assert payload["rows"][6]["offset"] == 338
    assert payload["rows"][6]["actual_status"] == "prime"
    assert payload["rows"][6]["no_arrival_to_sqrt_required_for_prime"] is True
