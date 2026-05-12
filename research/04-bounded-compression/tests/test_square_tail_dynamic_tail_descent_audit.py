"""Tests for dynamic-tail least-factor descent audits."""

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
    / "square_tail_dynamic_tail_descent_audit.py"
)


def load_module():
    """Load the dynamic-tail descent audit module directly from its path."""
    spec = importlib.util.spec_from_file_location(
        "square_tail_dynamic_tail_descent_audit",
        SCRIPT_PATH,
    )
    if spec is None or spec.loader is None:
        raise RuntimeError("unable to load square_tail_dynamic_tail_descent_audit")
    module = importlib.util.module_from_spec(spec)
    sys.modules["square_tail_dynamic_tail_descent_audit"] = module
    spec.loader.exec_module(module)
    return module


def test_fast_tail_value_factor_and_child_projection():
    """A fast representative tail row projects to a closed selected-square child."""
    module = load_module()
    row = module.factor_tail_value(89_726_961_223_544_427_015_292_389_839, 130, 4444)
    child = row["child_projection"]
    residue = row["child_prime_parent_residue"]

    assert row["offset"] == 260
    assert row["least_factor"] == 15_277
    assert row["factorization"]["15277"] == 1
    assert child["root"] == 15_277
    assert child["previous_prime_offset"] == 8
    assert child["dynamic_cutoff"] == 186
    assert child["closed_by_cutoff"] is True
    assert child["selected_square_condition"] is True
    assert residue["parent_residue_m"] == 111_310_662
    assert residue["inside_parent_M"] is False
