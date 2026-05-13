"""Tests for child selected-square inheritance audits."""

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
    / "square_tail_child_selected_square_inheritance_audit.py"
)


def load_module():
    """Load the child selected-square inheritance module directly from its path."""
    spec = importlib.util.spec_from_file_location(
        "square_tail_child_selected_square_inheritance_audit",
        SCRIPT_PATH,
    )
    if spec is None or spec.loader is None:
        raise RuntimeError("unable to load square_tail_child_selected_square_inheritance_audit")
    module = importlib.util.module_from_spec(spec)
    sys.modules["square_tail_child_selected_square_inheritance_audit"] = module
    spec.loader.exec_module(module)
    return module


def test_child_selected_square_status_does_not_separate_actual_from_crt_model():
    """Actual descent and the local CRT model both have selected-square children."""
    module = load_module()
    payload = module.build_child_selected_square_inheritance_audit()
    summaries = {summary["label"]: summary for summary in payload["summaries"]}

    record = summaries["standing_record_actual_composite_rough_children"]
    representative = summaries["representative_actual_composite_rough_tail_children"]
    model = summaries["full_cutoff_crt_model_assigned_singleton_carriers"]

    assert payload["all_groups_have_only_selected_square_children"] is True
    assert record["child_root_count"] == 62
    assert record["selected_square_child_count"] == 62
    assert representative["child_root_count"] == 12
    assert representative["selected_square_child_count"] == 12
    assert model["child_root_count"] == 569
    assert model["selected_square_child_count"] == 569
