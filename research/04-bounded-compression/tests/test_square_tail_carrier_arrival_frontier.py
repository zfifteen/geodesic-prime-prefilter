"""Tests for carrier-arrival frontier audits."""

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
    / "square_tail_carrier_arrival_frontier.py"
)


def load_module():
    """Load the carrier-arrival frontier module directly from its path."""
    spec = importlib.util.spec_from_file_location("square_tail_carrier_arrival_frontier", SCRIPT_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("unable to load square_tail_carrier_arrival_frontier")
    module = importlib.util.module_from_spec(spec)
    sys.modules["square_tail_carrier_arrival_frontier"] = module
    spec.loader.exec_module(module)
    return module


def test_root_509_representative_carrier_arrival_frontier_to_1e6():
    """The representative has a sparse first-arrival frontier through 1e6."""
    module = load_module()
    payload = module.build_arrival_frontier(509, 1_000_000)

    assert payload["M"] == 4444
    assert payload["dynamic_cutoff"] == 8889
    assert payload["rough_defect_count"] == 569
    assert payload["arrived_count"] == 222
    assert payload["unarrived_count"] == 347
    assert payload["closing_m"] == 169
    assert payload["closing_offset"] == 338
    assert payload["closing_row_arrival"] is None
    assert payload["milestones"][-1] == {
        "carrier_bound": 1_000_000,
        "arrived_count": 222,
        "unarrived_count": 347,
    }
    assert payload["first_unarrived_offsets"][:6] == [80, 114, 128, 182, 194, 332]
