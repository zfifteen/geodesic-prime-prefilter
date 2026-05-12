"""Tests for square-tail transitive projection graphs."""

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
    / "square_tail_projection_graph.py"
)


def load_module():
    """Load the projection graph module directly from its path."""
    spec = importlib.util.spec_from_file_location("square_tail_projection_graph", SCRIPT_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("unable to load square_tail_projection_graph")
    module = importlib.util.module_from_spec(spec)
    sys.modules["square_tail_projection_graph"] = module
    spec.loader.exec_module(module)
    return module


def test_root_11_projection_graph_has_strict_decreasing_base_sinks():
    """The small square-tail graph descends directly to closed base roots."""
    module = load_module()
    payload = module.build_graph(11)

    assert payload["node_count"] == 4
    assert payload["edge_count"] == 3
    assert payload["max_depth"] == 1
    assert payload["sink_roots"] == [3, 5, 7]
    assert payload["all_edges_strictly_decrease"] is True
    assert payload["all_nodes_closed_by_cutoff"] is True
    assert payload["all_nodes_selected_square_condition"] is True
