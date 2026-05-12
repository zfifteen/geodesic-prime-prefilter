"""Tests for dynamic-tail square-tail audits."""

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
    / "square_tail_dynamic_tail_audit.py"
)


def load_module():
    """Load the dynamic-tail audit module directly from its path."""
    spec = importlib.util.spec_from_file_location("square_tail_dynamic_tail_audit", SCRIPT_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("unable to load square_tail_dynamic_tail_audit")
    module = importlib.util.module_from_spec(spec)
    sys.modules["square_tail_dynamic_tail_audit"] = module
    spec.loader.exec_module(module)
    return module


def test_root_509_prime_representative_dynamic_tail_classification():
    """The representative closes at the only prime-valued actual rough tail row."""
    module = load_module()
    payload = module.build_dynamic_tail_audit(509)

    assert payload["source_M"] == 39
    assert payload["actual_M"] == 4444
    assert payload["closing_m"] == 169
    assert payload["tail_even_offset_range"] == [80, 338]
    assert payload["counts"]["tail_position_count"] == 130
    assert payload["counts"]["source_small_covered_count"] == 94
    assert payload["counts"]["source_assigned_large_covered_count"] == 20
    assert payload["counts"]["source_modeled_covered_count"] == 98
    assert payload["counts"]["new_repeat_capable_covered_count"] == 65
    assert payload["counts"]["actual_rough_count"] == 13
    assert payload["counts"]["prime_value_count"] == 1
    assert payload["actual_rough_offsets"] == [
        80,
        114,
        128,
        132,
        182,
        194,
        252,
        260,
        278,
        300,
        318,
        332,
        338,
    ]
    assert payload["prime_offsets"] == [338]
    assert payload["prime_rows"][0]["actual_rough"] is True
