"""Tests for selected-square deadline audits."""

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
    / "square_tail_selected_square_deadline_audit.py"
)


def load_module():
    """Load the selected-square deadline module directly from its path."""
    spec = importlib.util.spec_from_file_location("square_tail_selected_square_deadline_audit", SCRIPT_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("unable to load square_tail_selected_square_deadline_audit")
    module = importlib.util.module_from_spec(spec)
    sys.modules["square_tail_selected_square_deadline_audit"] = module
    spec.loader.exec_module(module)
    return module


def test_selected_square_deadline_rows_exceed_dynamic_cutoff():
    """Selected-square membership supplies a broad deadline, not the dynamic cutoff."""
    module = load_module()
    payload = module.build_deadline_audit(
        [424_171_123, 89_726_961_223_544_427_015_292_389_839]
    )
    record, representative = payload["rows"]

    assert payload["all_selected_square"] is True
    assert payload["all_deadlines_exceed_dynamic_cutoff"] is True
    assert record["previous_root_gap"] == 30
    assert record["selected_square_deadline_offset"] == "25450266480"
    assert record["actual_previous_prime_offset"] == 738
    assert record["dynamic_cutoff"] == 790
    assert representative["previous_root_gap"] == 112
    assert representative["selected_square_deadline_offset"] == "20098839314073951651425495311392"
    assert representative["actual_previous_prime_offset"] == 338
    assert representative["dynamic_cutoff"] == 8889
