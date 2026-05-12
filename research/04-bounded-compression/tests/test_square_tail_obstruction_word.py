"""Tests for the square-tail obstruction-word emitter."""

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
    / "square_tail_obstruction_word.py"
)


def load_module():
    """Load the obstruction-word module directly from its path."""
    spec = importlib.util.spec_from_file_location("square_tail_obstruction_word", SCRIPT_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("unable to load square_tail_obstruction_word")
    module = importlib.util.module_from_spec(spec)
    sys.modules["square_tail_obstruction_word"] = module
    spec.loader.exec_module(module)
    return module


def test_root_11_obstruction_word_matches_exact_prefix():
    """The square 11^2 has the expected composite prefix before 113."""
    module = load_module()
    payload = module.build_payload(11)

    assert payload["square"] == 121
    assert payload["previous_prime"] == 113
    assert payload["previous_prime_offset"] == 8
    assert payload["closed_by_cutoff"] is True
    assert payload["selected_square_condition"] is True
    assert [row["offset"] for row in payload["obstruction_rows"]] == [2, 4, 6]
    assert [row["least_factor"] for row in payload["obstruction_rows"]] == [7, 3, 5]
    assert payload["child_projection_count"] == 3
    assert payload["child_projection_closed_count"] == 3


def test_record_root_summary_keeps_high_utilization_geometry():
    """The current high-utilization record emits the known offset and cutoff."""
    module = load_module()
    payload = module.build_payload(424_171_123)

    assert payload["previous_prime_offset"] == 738
    assert payload["dynamic_cutoff"] == 790
    assert payload["closed_by_cutoff"] is True
    assert payload["obstruction_prefix_even_count"] == 368
    assert payload["full_counterexample_even_count"] == 395
    assert payload["max_least_factor_row"]["offset"] == 152
    assert payload["child_projection_count"] == 99
    assert payload["child_projection_closed_count"] == 99
    assert payload["child_projection_selected_square_count"] == 99
    assert payload["max_child_projection_utilization_row"]["root"] == 509
