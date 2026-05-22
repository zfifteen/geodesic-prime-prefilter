"""Tests for the PGS chain modulus-link streaming probe."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
MODULE_PATH = ROOT / "research" / "06-cryptology-rsa" / "scripts" / "scale_pgs_chain_modulus_link.py"


def load_module():
    """Load the temporary scale probe module."""
    spec = importlib.util.spec_from_file_location(
        "scale_pgs_chain_modulus_link",
        MODULE_PATH,
    )
    if spec is None or spec.loader is None:
        raise RuntimeError("unable to load scale recursive walk module")
    module = importlib.util.module_from_spec(spec)
    sys.modules["scale_pgs_chain_modulus_link"] = module
    spec.loader.exec_module(module)
    return module


def test_modulus_link_residual_locks_exact_endpoint_pair():
    """The modulus-link residual should distinguish exact endpoint locks."""
    module = load_module()

    assert module.modulus_link_residual(35, 5, 7) == 0
    assert module.modulus_link_residual(15251, 109, 139) == 100


def test_chain_walk_recovers_medium_pair_without_classical_anchor():
    """The chain walk should recover 31 and 29 from n=899."""
    module = load_module()

    result = module.recursive_chain_modulus_lock(899, seed=23)

    assert result.endpoint_class_upper == 31
    assert result.endpoint_class_lower == 29
    assert result.chain_steps == 2
    assert result.locked_endpoint_count == 3
    assert result.stop_reason == "modulus_link_zero_locked"


def test_large_case_uses_chain_steps_not_modulus_rows():
    """The largest committed case should advance on the PGS chain only."""
    module = load_module()
    case = module.SCALE_CASES[6]

    result = module.recursive_chain_modulus_lock(case.n, case.seed)

    assert result.endpoint_class_upper == case.expected_upper_endpoint
    assert result.endpoint_class_lower == case.expected_lower_endpoint
    assert result.chain_steps == 2
    assert result.locked_endpoint_count == 3
    assert result.chain_steps < case.n // 100000


def test_wide_control_skips_nonzero_floor_closure_then_locks_endpoint_class():
    """The wide control should skip the nonzero floor pair and lock endpoints."""
    module = load_module()
    case = module.SCALE_CASES[-1]

    result = module.recursive_chain_modulus_lock(case.n, case.seed)

    assert (result.endpoint_class_upper, result.endpoint_class_lower) == (
        case.expected_upper_endpoint,
        case.expected_lower_endpoint,
    )
    assert result.chain_steps == 11
    assert result.skipped_floor_closures == 1


def test_scale_probe_cases_match_audit_pairs():
    """Every committed scale case should match its downstream audit endpoints."""
    module = load_module()
    results = module.run_scale_probe()

    assert [
        (result.n, result.endpoint_class_upper, result.endpoint_class_lower)
        for result in results
    ] == [
        (35, 7, 5),
        (77, 11, 7),
        (143, 13, 11),
        (221, 17, 13),
        (899, 31, 29),
        (10403, 103, 101),
        (1022117, 1013, 1009),
        (15251, 151, 101),
    ]
