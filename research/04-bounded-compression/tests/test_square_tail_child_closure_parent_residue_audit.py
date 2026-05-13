"""Tests for direct child-closure parent-residue audits."""

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
    / "square_tail_child_closure_parent_residue_audit.py"
)


def load_module():
    """Load the direct child-closure parent-residue audit module."""
    spec = importlib.util.spec_from_file_location(
        "square_tail_child_closure_parent_residue_audit",
        SCRIPT_PATH,
    )
    if spec is None or spec.loader is None:
        raise RuntimeError("unable to load square_tail_child_closure_parent_residue_audit")
    module = importlib.util.module_from_spec(spec)
    sys.modules["square_tail_child_closure_parent_residue_audit"] = module
    spec.loader.exec_module(module)
    return module


def test_child_closing_primes_do_not_directly_cover_parent_windows():
    """Child closing primes land outside both measured parent windows."""
    module = load_module()
    payload = module.build_child_closure_parent_residue_audit()
    surfaces = {surface["label"]: surface for surface in payload["surfaces"]}
    record = surfaces["standing_record_actual_composite_rough_children"]
    representative = surfaces["representative_actual_composite_rough_tail_children"]

    assert payload["all_child_closing_prime_residues_outside_parent_M"] is True
    assert record["parent_M"] == 395
    assert record["parent_residue_rows_checked"] == 664
    assert record["inside_parent_M_count"] == 0
    assert representative["parent_M"] == 4444
    assert representative["parent_residue_rows_checked"] == 167
    assert representative["inside_parent_M_count"] == 0
