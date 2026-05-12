"""Tests for square-tail M-rough defect audits."""

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
    / "square_tail_rough_defect_audit.py"
)


def load_module():
    """Load the M-rough defect audit module directly from its path."""
    spec = importlib.util.spec_from_file_location("square_tail_rough_defect_audit", SCRIPT_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("unable to load square_tail_rough_defect_audit")
    module = importlib.util.module_from_spec(spec)
    sys.modules["square_tail_rough_defect_audit"] = module
    spec.loader.exec_module(module)
    return module


def test_root_509_rough_defects_match_prime_offsets():
    """The 509 record has three prime-valued M-rough defects."""
    module = load_module()
    payload = module.build_rough_defect_audit(509)

    assert payload["full_counterexample_even_count"] == 39
    assert payload["repeat_capable_prime_count"] == 11
    assert payload["rough_defect_count"] == 9
    assert payload["rough_prime_defect_count"] == 3
    assert payload["rough_prime_defect_offsets"] == [48, 62, 72]
    assert payload["rough_composite_defect_count"] == 6
    assert payload["rough_composite_min_least_factor"] > payload["full_counterexample_even_count"]
    assert payload["all_rough_composite_least_factors_exceed_M"] is True
    assert payload["all_rough_rows_uncovered_by_repeat_capable_carriers"] is True
    assert payload["closed_by_rough_prime_defect"] is True


def test_record_root_rough_defects_match_current_prime_defects():
    """The standing record closes by three prime-valued M-rough defects."""
    module = load_module()
    payload = module.build_rough_defect_audit(424_171_123)

    assert payload["previous_prime_offset"] == 738
    assert payload["dynamic_cutoff"] == 790
    assert payload["full_counterexample_even_count"] == 395
    assert payload["repeat_capable_prime_count"] == 76
    assert payload["rough_defect_count"] == 65
    assert payload["rough_prime_defect_count"] == 3
    assert payload["rough_prime_defect_offsets"] == [738, 756, 758]
    assert payload["rough_composite_defect_count"] == 62
    assert payload["rough_composite_min_least_factor"] > payload["full_counterexample_even_count"]
    assert payload["all_rough_composite_least_factors_exceed_M"] is True
    assert payload["all_rough_rows_uncovered_by_repeat_capable_carriers"] is True
    assert payload["closed_by_rough_prime_defect"] is True
