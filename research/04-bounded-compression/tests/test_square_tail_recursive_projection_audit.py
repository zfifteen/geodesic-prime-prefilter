"""Tests for direct square-tail recursive projection audits."""

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
    / "square_tail_recursive_projection_audit.py"
)


def load_module():
    """Load the recursive projection audit module directly from its path."""
    spec = importlib.util.spec_from_file_location(
        "square_tail_recursive_projection_audit",
        SCRIPT_PATH,
    )
    if spec is None or spec.loader is None:
        raise RuntimeError("unable to load square_tail_recursive_projection_audit")
    module = importlib.util.module_from_spec(spec)
    sys.modules["square_tail_recursive_projection_audit"] = module
    spec.loader.exec_module(module)
    return module


def test_record_parent_does_not_directly_contain_strongest_child_word():
    """The record parent invalidates naive direct child-word containment."""
    module = load_module()
    payload = module.build_audit(424_171_123, 509)

    assert payload["parent_previous_prime_offset"] == 738
    assert payload["parent_dynamic_cutoff"] == 790
    assert payload["child_previous_prime_offset"] == 48
    assert payload["child_dynamic_cutoff"] == 78
    assert payload["child_closed_by_cutoff"] is True
    assert payload["child_selected_square_condition"] is True
    assert payload["parent_child_occurrence_count"] == 1
    assert payload["parent_child_occurrence_offsets"] == [498]
    assert payload["child_obstruction_prefix_even_count"] == 23
    assert payload["child_full_counterexample_even_count"] == 39
    assert payload["child_word_factors_subset_of_parent_word"] is False
    assert payload["missing_child_factors_from_parent_word"] == [83, 449]
    assert payload["parent_child_occurrences_cover_child_prefix"] is False
    assert payload["parent_child_occurrences_cover_child_full_word"] is False
    assert payload["direct_recursive_containment_holds"] is False
