"""Tests for square-tail rough-defect descent audits."""

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
    / "square_tail_rough_descent_audit.py"
)


def load_module():
    """Load the rough-defect descent audit module directly from its path."""
    spec = importlib.util.spec_from_file_location("square_tail_rough_descent_audit", SCRIPT_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("unable to load square_tail_rough_descent_audit")
    module = importlib.util.module_from_spec(spec)
    sys.modules["square_tail_rough_descent_audit"] = module
    spec.loader.exec_module(module)
    return module


def test_root_509_rough_descent_children_are_closed():
    """The 509 rough-composite children descend to closed rough-defect roots."""
    module = load_module()
    payload = module.build_descent_audit(509)

    assert payload["parent_M"] == 39
    assert payload["parent_rough_defect_count"] == 9
    assert payload["parent_rough_prime_defect_count"] == 3
    assert payload["parent_rough_composite_defect_count"] == 6
    assert payload["child_count"] == 6
    assert payload["all_child_roots_strictly_decrease"] is True
    assert payload["all_children_closed_by_rough_prime_defect"] is True


def test_record_root_rough_descent_children_are_closed():
    """The standing record's rough-composite children all close recursively."""
    module = load_module()
    payload = module.build_descent_audit(424_171_123)

    assert payload["parent_M"] == 395
    assert payload["parent_rough_defect_count"] == 65
    assert payload["parent_rough_prime_defect_count"] == 3
    assert payload["parent_rough_composite_defect_count"] == 62
    assert payload["child_count"] == 62
    assert payload["all_child_roots_strictly_decrease"] is True
    assert payload["all_children_closed_by_rough_prime_defect"] is True
    assert payload["max_child_M_row"]["root"] == 159_673_649
    assert payload["max_child_rough_defect_row"]["root"] == 108_562_759
