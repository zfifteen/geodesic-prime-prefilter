"""Unit tests for pure residual partition logic (chapter 21).

Tests drive the shipped module. They do not reimplement residual_state as an
oracle for the main closed/open assertions.
"""

from __future__ import annotations

import ast
import importlib.util
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts" / "residual_partition.py"


def load_module():
    spec = importlib.util.spec_from_file_location(
        "residual_partition_ch21", MODULE_PATH
    )
    if spec is None or spec.loader is None:
        raise RuntimeError(f"unable to load {MODULE_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="module")
def rp():
    return load_module()


def test_m_v1_matches_proof_vector(rp):
    assert rp.M_V1 == (2, 3, 5, 7, 30, 210, 2310)


def test_wheel_from_30_and_210(rp):
    assert rp.wheel_from_carrier(30) == frozenset({2, 3, 5})
    assert rp.wheel_from_carrier(210) == frozenset({2, 3, 5, 7})
    assert rp.zero_count(30) >= 4
    assert rp.zero_count(210) >= 4


def test_thirty_plus_minus_one_modular_closed(rp):
    """Salvage toy: S=30 forces empty residual on both neighbors."""
    for offset in (-1, 1):
        record = rp.classify_neighbor(30, offset=offset)
        assert record["wheel"] == [2, 3, 5]
        assert record["residual_set"] == []
        assert record["residual_state"] == rp.STATE_MODULAR_CLOSED
        assert record["modular_closed"] is True
        # Decision must be emptiness of residual_set from the shipped builder.
        assert rp.residual_set(record["neighbor"], record["wheel"]) == frozenset()


def test_two_ten_plus_minus_one_residual_open(rp):
    """At 210, residual includes 11 and 13; state is residual-open."""
    for offset in (-1, 1):
        record = rp.classify_neighbor(210, offset=offset)
        assert set(record["wheel"]) == {2, 3, 5, 7}
        residual = set(record["residual_set"])
        assert 11 in residual
        assert 13 in residual
        assert record["residual_state"] == rp.STATE_RESIDUAL_OPEN
        assert record["modular_closed"] is False
        assert rp.residual_set(record["neighbor"], record["wheel"])


def test_z4_twin_lock_ce_neighborhood_w_plus_one_open(rp):
    """Pinned CE carrier: w=17666310, neighbor w+1 is residual-open.

    Does not claim primality; only residual-state under the wheel from zeros.
    """
    w = 17_666_310
    assert rp.zero_count(w) >= 4
    assert 30 in [m for m in rp.M_V1 if w % m == 0]
    record = rp.classify_neighbor(w, offset=1)
    assert record["carrier"] == w
    assert record["neighbor"] == w + 1
    assert set(record["wheel"]) == {2, 3, 5}
    assert record["residual_state"] == rp.STATE_RESIDUAL_OPEN
    assert record["modular_closed"] is False
    assert len(record["residual_set"]) > 0
    # Residual construction matches direct call on shipped residual_set.
    direct = rp.residual_set(w + 1, rp.wheel_from_carrier(w))
    assert set(record["residual_set"]) == set(direct)


def test_second_ce_neighborhood_also_open(rp):
    w = 22_284_030
    assert rp.zero_count(w) >= 4
    record = rp.classify_neighbor(w, offset=1)
    assert record["residual_state"] == rp.STATE_RESIDUAL_OPEN
    assert record["residual_set"]


def test_decision_path_source_has_no_primality_or_trial_choice(rp):
    """Static guard: residual_state body must not invoke trial/primality helpers."""
    source = MODULE_PATH.read_text(encoding="utf-8")
    tree = ast.parse(source)
    forbidden_names = {
        "is_prime",
        "isprime",
        "next_prime",
        "trial_divide",
        "sympy",
    }
    # Names used only outside residual_state / residual_set are allowed in
    # measurement scripts, not in this pure module.
    used: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Name):
            used.add(node.id)
        elif isinstance(node, ast.Attribute):
            used.add(node.attr)
    assert forbidden_names.isdisjoint(used), (
        f"pure residual module must not reference {forbidden_names & used}"
    )
    # residual_state must only branch on residual_set emptiness / n bound.
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name == "residual_state":
            body_src = ast.get_source_segment(source, node) or ""
            assert "residual_set" in body_src
            assert "is_prime" not in body_src
            assert "%" not in body_src or "n %" not in body_src
            # No trial of residual primes against n inside residual_state.
            assert "for " not in body_src or "residual_set" in body_src


def test_zero_count_four_implies_thirty_divides_on_m_v1(rp):
    """Sanity for modular half: z>=4 samples are 30-multiples (proved lemma)."""
    for w in (30, 60, 90, 210, 17_666_310, 22_284_030):
        if rp.zero_count(w) >= 4:
            assert w % 30 == 0


def test_dynamic_moduli_family_from_primes(rp):
    """Optional dynamic family builder (hypothesis path, not theorem)."""
    family = rp.moduli_family_from_primes([2, 3, 5, 7, 11])
    assert 2 in family and 11 in family
    assert 30 in family and 210 in family and 2310 in family
    # Cumulative primorial 2*3*5*7*11 = 2310 already; product through 11 is 2310.
    assert family == rp.normalize_moduli_family(family)


def test_dynamic_wheel_deepens_beyond_m_v1(rp):
    """On M_DYNAMIC_HYPOTHESIS, 2310-carrier wheel includes 11."""
    w = 2310
    wheel_default = rp.wheel_from_carrier(w, rp.M_V1)
    wheel_dyn = rp.wheel_from_carrier(w, rp.M_DYNAMIC_HYPOTHESIS)
    assert wheel_default == frozenset({2, 3, 5, 7, 11})
    assert 11 in wheel_dyn
    # Custom family that stops before 11 yields smaller wheel on 30.
    small = rp.wheel_from_carrier(30, moduli=(2, 3, 5, 30))
    assert small == frozenset({2, 3, 5})
    record = rp.classify_neighbor(2310, offset=1, moduli=rp.M_DYNAMIC_HYPOTHESIS)
    assert record["moduli_is_m_v1"] is False
    assert record["moduli_status"] == "dynamic_hypothesis_optional"
    assert 11 in record["wheel"]
    # Residual state still decided by residual_set emptiness from shipped API.
    assert record["residual_state"] in (
        rp.STATE_MODULAR_CLOSED,
        rp.STATE_RESIDUAL_OPEN,
    )
    assert record["modular_closed"] == (record["residual_state"] == rp.STATE_MODULAR_CLOSED)
    assert set(record["residual_set"]) == set(
        rp.residual_set(record["neighbor"], record["wheel"])
    )


def test_normalize_moduli_rejects_empty_and_small(rp):
    with pytest.raises(ValueError):
        rp.normalize_moduli_family([])
    with pytest.raises(ValueError):
        rp.normalize_moduli_family([1, 2])
