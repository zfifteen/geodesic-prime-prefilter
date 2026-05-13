"""Tests for local-model obstruction-inheritance audits."""

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
    / "square_tail_obstruction_inheritance_local_model_audit.py"
)


def load_module():
    """Load the local-model obstruction-inheritance audit module."""
    spec = importlib.util.spec_from_file_location(
        "square_tail_obstruction_inheritance_local_model_audit",
        SCRIPT_PATH,
    )
    if spec is None or spec.loader is None:
        raise RuntimeError("unable to load square_tail_obstruction_inheritance_local_model_audit")
    module = importlib.util.module_from_spec(spec)
    sys.modules["square_tail_obstruction_inheritance_local_model_audit"] = module
    spec.loader.exec_module(module)
    return module


def test_local_crt_model_does_not_force_obstruction_inheritance():
    """The local CRT model has a complete cover and no obstructed assigned carriers."""
    module = load_module()
    payload = module.build_local_model_inheritance_audit()

    assert payload["parent_local_model_consistent"] is True
    assert payload["parent_rough_defect_count"] == 569
    assert payload["assigned_carrier_count"] == 569
    assert payload["assigned_carriers_with_O_count"] == 0
    assert payload["assigned_carriers_closed_count"] == 569
    assert payload["all_assigned_carriers_closed"] is True
    assert payload["min_assigned_carrier_rough_prime_defect_count"] >= 1
