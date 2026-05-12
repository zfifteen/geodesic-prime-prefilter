"""Tests for CRT model arrival-order audits."""

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
    / "square_tail_crt_model_arrival_order_audit.py"
)


def load_module():
    """Load the CRT model arrival-order audit module directly from its path."""
    spec = importlib.util.spec_from_file_location("square_tail_crt_model_arrival_order_audit", SCRIPT_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("unable to load square_tail_crt_model_arrival_order_audit")
    module = importlib.util.module_from_spec(spec)
    sys.modules["square_tail_crt_model_arrival_order_audit"] = module
    spec.loader.exec_module(module)
    return module


def test_full_cutoff_crt_model_has_complete_ordered_arrival_cover():
    """The local CRT model has first arrivals for every rough row by its last carrier."""
    module = load_module()
    payload = module.build_arrival_order_audit(509)

    assert payload["M"] == 4444
    assert payload["rough_defect_count"] == 569
    assert payload["last_assigned_carrier"] == 14741
    assert payload["last_assigned_m"] == 4434
    assert payload["last_assigned_offset"] == 8868
    assert payload["last_assigned_sqrt_boundary_digits"] == 4136
    assert payload["last_assigned_carrier_before_sqrt_boundary"] is True
    assert payload["first_arrived_by_last_assigned_count"] == 569
    assert payload["unarrived_by_last_assigned_count"] == 0
    assert payload["assigned_first_match_count"] == 547
    assert payload["assigned_first_mismatch_count"] == 22
    assert payload["first_mismatches"][0] == {
        "m": 432,
        "offset": 864,
        "assigned_carrier": 5179,
        "first_arrival": 4969,
    }
