"""Tests for square-tail moving-cover audits."""

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
    / "square_tail_cover_audit.py"
)


def load_module():
    """Load the moving-cover audit module directly from its path."""
    spec = importlib.util.spec_from_file_location("square_tail_cover_audit", SCRIPT_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("unable to load square_tail_cover_audit")
    module = importlib.util.module_from_spec(spec)
    sys.modules["square_tail_cover_audit"] = module
    spec.loader.exec_module(module)
    return module


def test_root_11_cover_audit_marks_previous_prime_as_uncovered():
    """The small root cover misses the actual predecessor-prime position."""
    module = load_module()
    payload = module.build_cover_audit(11)

    assert payload["previous_prime_offset"] == 8
    assert payload["full_counterexample_even_count"] == 32
    assert payload["obstruction_prefix_even_count"] == 3
    assert payload["prefix_factor_count"] == 3
    assert payload["covered_by_prefix_factor_count"] == 18
    assert payload["actual_previous_prime_m"] == 4
    assert payload["actual_previous_prime_uncovered_by_prefix_factors"] is True
    assert payload["uncovered_m"][:3] == [4, 6, 7]


def test_record_cover_audit_exposes_moving_window_defect():
    """The record prefix factor classes miss exactly ten cutoff positions."""
    module = load_module()
    payload = module.build_cover_audit(424_171_123)

    assert payload["previous_prime_offset"] == 738
    assert payload["dynamic_cutoff"] == 790
    assert payload["full_counterexample_even_count"] == 395
    assert payload["obstruction_prefix_even_count"] == 368
    assert payload["prefix_factor_count"] == 99
    assert payload["covered_by_prefix_factor_count"] == 385
    assert payload["uncovered_by_prefix_factor_count"] == 10
    assert payload["actual_previous_prime_m"] == 369
    assert payload["actual_previous_prime_uncovered_by_prefix_factors"] is True
    assert payload["uncovered_offsets"] == [738, 740, 750, 756, 758, 762, 770, 776, 782, 786]
    assert payload["uncovered_prime_offsets"] == [738, 756, 758]
    assert payload["uncovered_composite_least_factors"] == [
        683,
        44971,
        8880233,
        2689,
        503,
        4219,
        367,
    ]
    assert payload["completed_factor_count"] == 106
    assert payload["covered_after_composite_defect_factors_count"] == 392
    assert payload["remaining_uncovered_after_composite_defect_factors_offsets"] == [
        738,
        756,
        758,
    ]
