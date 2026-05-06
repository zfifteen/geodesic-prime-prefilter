"""Tests for the recursive backward chamber walk scale probe."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
MODULE_PATH = ROOT / "tmp" / "scale_recursive_backward_chamber_walk.py"


def load_module():
    """Load the temporary scale probe module."""
    spec = importlib.util.spec_from_file_location(
        "scale_recursive_backward_chamber_walk",
        MODULE_PATH,
    )
    if spec is None or spec.loader is None:
        raise RuntimeError("unable to load scale recursive walk module")
    module = importlib.util.module_from_spec(spec)
    sys.modules["scale_recursive_backward_chamber_walk"] = module
    spec.loader.exec_module(module)
    return module


def test_closure_for_new_endpoint_waits_until_partner_locked():
    """The floor closure should appear only after the partner endpoint is locked."""
    module = load_module()

    assert module.closure_for_new_endpoint(35, frozenset({31, 29, 23, 19, 17, 13, 11, 7}), 7) is None
    assert module.closure_for_new_endpoint(35, frozenset({31, 29, 23, 19, 17, 13, 11, 7, 5}), 5) == (7, 5)


def test_recursive_backward_walk_recovers_medium_pair():
    """The scaled walk should recover 31 and 29 from n=899."""
    module = load_module()
    table = module.build_exact_chamber_table(899)

    result = module.recursive_backward_walk(899, table)

    assert result.q == 31
    assert result.p == 29
    assert result.locked_endpoint_count == 145
    assert result.chamber_rows_read == 871
    assert result.stop_reason == "reciprocal_floor_closure_locked"


def test_scale_probe_cases_match_audit_pairs():
    """Every committed scale case should recover its audit pair."""
    module = load_module()
    subset = module.SCALE_CASES[:6]
    results = module.run_scale_probe(subset)

    assert [
        (result.n, result.q, result.p)
        for result in results
    ] == [
        (35, 7, 5),
        (77, 11, 7),
        (143, 13, 11),
        (221, 17, 13),
        (899, 31, 29),
        (10403, 103, 101),
    ]
