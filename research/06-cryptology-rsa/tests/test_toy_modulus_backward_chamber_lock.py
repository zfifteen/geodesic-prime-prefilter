"""Tests for the pure recursive toy PGS backward chamber lock."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
MODULE_PATH = ROOT / "research" / "06-cryptology-rsa" / "scripts" / "toy_modulus_backward_chamber_lock.py"


def load_module():
    """Load the temporary recursive backward chamber module."""
    spec = importlib.util.spec_from_file_location(
        "toy_modulus_backward_chamber_lock",
        MODULE_PATH,
    )
    if spec is None or spec.loader is None:
        raise RuntimeError("unable to load toy backward chamber module")
    module = importlib.util.module_from_spec(spec)
    sys.modules["toy_modulus_backward_chamber_lock"] = module
    spec.loader.exec_module(module)
    return module


def test_recursive_walk_locks_toy_pair_by_floor_closure():
    """The walk should stop when locked endpoints mutually floor-close."""
    module = load_module()

    result = module.recursive_backward_walk(module.START_N, module.MIN_COORDINATE)

    assert result["stop_reason"] == "reciprocal_floor_closure_locked"
    assert result["closure"] == (7, 5)
    assert result["endpoints"] == (31, 29, 23, 19, 17, 13, 11, 7, 5)


def test_floor_closure_is_absent_until_both_endpoints_are_locked():
    """The closure must not appear before both 7 and 5 are in the chain."""
    module = load_module()

    assert module.reciprocal_floor_closure(module.START_N, [31, 29, 23, 19, 17, 13, 11, 7]) is None
    assert module.reciprocal_floor_closure(module.START_N, [31, 29, 23, 19, 17, 13, 11, 7, 5]) == (7, 5)


def test_recursive_walk_emits_law_facing_chamber_reads():
    """The chamber reads should expose tau locks, not factor tests."""
    module = load_module()
    result = module.recursive_backward_walk(module.START_N, module.MIN_COORDINATE)
    chambers = result["chambers"]

    assert chambers[-1]["read"] == (6, 5)
    assert chambers[-1]["tau"] == (4, 2)
    assert chambers[-1]["endpoint"] == 5
    assert chambers[-1]["reciprocal_floor_closure"] == (7, 5)


def test_main_displays_selected_pair(capsys):
    """The script should display p and q after recursive floor closure."""
    module = load_module()

    module.main()
    output = capsys.readouterr().out

    assert "endpoint_chain:" in output
    assert "31 -> 29 -> 23 -> 19 -> 17 -> 13 -> 11 -> 7 -> 5" in output
    assert "reciprocal_floor_closure: 7 -> 5 and 5 -> 7" in output
    assert "selected_pair:" in output
    assert "q = 7" in output
    assert "p = 5" in output
