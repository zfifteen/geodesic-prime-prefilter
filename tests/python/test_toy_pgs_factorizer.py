from __future__ import annotations

import csv
import importlib.util
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
TOY = ROOT / "experiments" / "rsa" / "toy_pgs_factorizer"


def load_module(name: str):
    """Load one toy factorizer module."""
    path = TOY / f"{name}.py"
    if str(TOY) not in sys.path:
        sys.path.insert(0, str(TOY))
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_factorizer_keeps_classical_boundary_knob_out_of_inference():
    """The factorizer must not contain classical or divisibility-adjacent gates."""
    source = (TOY / "pgs_factorizer.py").read_text(encoding="utf-8")
    forbidden = (
        "gcd",
        "factorint",
        "isprime",
        "is_prime",
        "nextprime",
        "prevprime",
        "upper_native_width_dominance",
        "reciprocal_floor_boundary",
        "n_value - 1",
    )

    for token in forbidden:
        assert token not in source


def test_factorizer_reports_ambiguous_case_as_unresolved():
    """N=253 should remain unresolved under the PGS-only endpoint lock."""
    factorizer = load_module("pgs_factorizer")

    inference, survivors = factorizer.factorize(253)

    assert inference == {
        "N": 253,
        "status": "unresolved",
        "unresolved_reason": "survivor_count_not_one",
        "survivor_count": 2,
        "candidate_pair_count": 38,
        "rule_id": "toy_pgspg_mutual_reciprocal_endpoint_lock_v1",
    }
    assert [(row["lower_reset_endpoint"], row["upper_reset_endpoint"]) for row in survivors] == [
        (11, 23),
        (13, 19),
    ]


def test_controller_writes_factorizer_and_validator_surfaces(tmp_path):
    """The controller should emit honest PGS inference plus validator knob rows."""
    controller = load_module("controller")

    summary = controller.run_experiment(tmp_path)

    assert summary == {
        "total_cases": 231,
        "resolved": 82,
        "unresolved": 149,
        "audit_pass": 82,
        "audit_fail": 0,
        "resolution_rate": 82 / 231,
        "resolved_precision": 1.0,
    }
    knob_rows = {
        row["knob"]: row
        for row in csv.DictReader((tmp_path / "decision_knob_rows.csv").open(encoding="utf-8"))
    }
    assert knob_rows["pgs_endpoint_lock"]["valid_for_pgs_factorizer"] == "True"
    assert int(knob_rows["pgs_endpoint_lock"]["resolved"]) == 82
    assert int(knob_rows["pgs_endpoint_lock"]["unresolved"]) == 149
    assert int(knob_rows["pgs_endpoint_lock"]["audit_fail"]) == 0

    dominance = knob_rows["endpoint_lock_then_upper_native_width_dominance"]
    assert dominance["valid_for_pgs_factorizer"] == "False"
    assert dominance["validity_note"] == "staged validator-only candidate after endpoint lock"
    assert int(dominance["resolved"]) == 88
    assert int(dominance["unresolved"]) == 143
    assert int(dominance["audit_pass"]) == 88
    assert int(dominance["audit_fail"]) == 0

    boundary = knob_rows["reciprocal_floor_boundary_lock"]
    assert boundary["valid_for_pgs_factorizer"] == "False"
    assert boundary["validity_note"] == "divisibility-adjacent reciprocal cell boundary"
    assert int(boundary["resolved"]) == 231
    assert int(boundary["unresolved"]) == 0
    assert int(boundary["audit_pass"]) == 231
    assert int(boundary["audit_fail"]) == 0

    summary_file = json.loads((tmp_path / "summary.json").read_text(encoding="utf-8"))
    assert summary_file == summary
    for path in tmp_path.iterdir():
        data = path.read_bytes()
        assert b"\r\n" not in data
        assert data.endswith(b"\n")


def test_larger_surface_falsifies_upper_width_candidate_without_factorizer_leak(tmp_path):
    """The staged candidate should remain validator-only on a larger surface."""
    controller = load_module("controller")

    summary = controller.run_experiment(tmp_path, max_audit_factor=149)

    assert summary == {
        "total_cases": 496,
        "resolved": 126,
        "unresolved": 370,
        "audit_pass": 126,
        "audit_fail": 0,
        "resolution_rate": 126 / 496,
        "resolved_precision": 1.0,
    }
    knob_rows = {
        row["knob"]: row
        for row in csv.DictReader((tmp_path / "decision_knob_rows.csv").open(encoding="utf-8"))
    }
    dominance = knob_rows["endpoint_lock_then_upper_native_width_dominance"]
    assert dominance["valid_for_pgs_factorizer"] == "False"
    assert int(dominance["resolved"]) == 135
    assert int(dominance["unresolved"]) == 361
    assert int(dominance["audit_pass"]) == 135
    assert int(dominance["audit_fail"]) == 0

    raw_candidate = knob_rows["upper_native_width_dominance"]
    assert raw_candidate["validity_note"] == "candidate public PGSPG invariant, validator-side only"
    assert int(raw_candidate["resolved"]) == 131
    assert int(raw_candidate["audit_fail"]) == 0
