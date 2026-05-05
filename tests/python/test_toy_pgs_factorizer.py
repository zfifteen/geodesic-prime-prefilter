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
    matrix_rows = list(
        csv.DictReader((tmp_path / "rule_audit_matrix.csv").open(encoding="utf-8"))
    )
    assert len(matrix_rows) == 231 * 7
    structural_rows = list(
        csv.DictReader(
            (tmp_path / "structural_candidate_matrix.csv").open(encoding="utf-8")
        )
    )
    assert len(structural_rows) == 231 * 8
    law_rows = list(
        csv.DictReader((tmp_path / "pgspg_law_matrix.csv").open(encoding="utf-8"))
    )
    assert len(law_rows) == 436 * 8
    replay_rows = list(
        csv.DictReader(
            (tmp_path / "directed_reset_replay_matrix.csv").open(encoding="utf-8")
        )
    )
    assert len(replay_rows) == 436 * 2
    none_none_rows = list(
        csv.DictReader(
            (tmp_path / "none_none_replay_alias_rows.csv").open(encoding="utf-8")
        )
    )
    assert len(none_none_rows) == 26
    assert sum(row["audit_role"] == "false_alias" for row in none_none_rows) == 14
    replay_divergences = [
        row
        for row in replay_rows
        if row["direction"] == "lower_to_upper"
        and row["audit_role"] == "false_alias"
        and row["first_divergence_stage"] == "deadline_transport"
    ]
    assert len(replay_divergences) == 57
    law_hits = [
        row
        for row in law_rows
        if row["law"] == "tail_offsets_echo"
        and row["audit_role"] == "false_alias"
        and row["law_holds"] == "True"
    ]
    assert len(law_hits) == 49
    structural_actions = {
        row["candidate"]: row["rule_action"]
        for row in structural_rows
        if row["case_id"] == "toy_le_99_11_11"
    }
    assert structural_actions["singleton_endpoint_lock"] == "positive_certificate"
    assert (
        structural_actions["mixed_topology_collision_blocker"]
        == "not_applicable"
    )
    staged_actions = [
        row["rule_action"]
        for row in matrix_rows
        if row["knob"] == "endpoint_lock_then_upper_native_width_dominance"
    ]
    assert staged_actions.count("positive_certificate") == 88
    assert staged_actions.count("invalid_selector") == 0
    first_failure = json.loads(
        (tmp_path / "upper_width_first_failure.json").read_text(encoding="utf-8")
    )
    assert first_failure == {
        "checked_cases": 231,
        "knob": "endpoint_lock_then_upper_native_width_dominance",
        "max_audit_factor": 99,
        "status": "no_failure",
    }
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
    matrix_rows = list(
        csv.DictReader((tmp_path / "rule_audit_matrix.csv").open(encoding="utf-8"))
    )
    assert len(matrix_rows) == 496 * 7
    structural_rows = list(
        csv.DictReader(
            (tmp_path / "structural_candidate_matrix.csv").open(encoding="utf-8")
        )
    )
    assert len(structural_rows) == 496 * 8
    law_rows = list(
        csv.DictReader((tmp_path / "pgspg_law_matrix.csv").open(encoding="utf-8"))
    )
    assert len(law_rows) == 1113 * 8
    replay_rows = list(
        csv.DictReader(
            (tmp_path / "directed_reset_replay_matrix.csv").open(encoding="utf-8")
        )
    )
    assert len(replay_rows) == 1113 * 2
    none_none_rows = list(
        csv.DictReader(
            (tmp_path / "none_none_replay_alias_rows.csv").open(encoding="utf-8")
        )
    )
    assert len(none_none_rows) == 46
    assert sum(row["audit_role"] == "false_alias" for row in none_none_rows) == 29
    upper_replay_clean_false_aliases = [
        row
        for row in replay_rows
        if row["direction"] == "upper_to_lower"
        and row["audit_role"] == "false_alias"
        and row["first_divergence_stage"] == "none"
    ]
    assert len(upper_replay_clean_false_aliases) == 55
    carrier_echo_false_aliases = [
        row
        for row in law_rows
        if row["law"] == "lock_carrier_echo"
        and row["audit_role"] == "false_alias"
        and row["law_holds"] == "True"
    ]
    assert len(carrier_echo_false_aliases) == 245
    capacity_actions = [
        row["rule_action"]
        for row in structural_rows
        if row["candidate"] == "unique_capacity_vector_dominance"
    ]
    assert capacity_actions.count("positive_certificate") == 156
    assert capacity_actions.count("invalid_selector") == 43
    staged_actions = [
        row["rule_action"]
        for row in matrix_rows
        if row["knob"] == "endpoint_lock_then_upper_native_width_dominance"
    ]
    assert staged_actions.count("positive_certificate") == 135
    assert staged_actions.count("invalid_selector") == 0
    first_failure = json.loads(
        (tmp_path / "upper_width_first_failure.json").read_text(encoding="utf-8")
    )
    assert first_failure == {
        "checked_cases": 496,
        "knob": "endpoint_lock_then_upper_native_width_dominance",
        "max_audit_factor": 149,
        "status": "no_failure",
    }


def test_upper_width_candidate_surface_199_writes_first_failure_artifact(tmp_path):
    """The 199 surface should report the first wrong dominance hit if present."""
    controller = load_module("controller")

    summary = controller.run_experiment(tmp_path, max_audit_factor=199)

    assert summary == {
        "total_cases": 903,
        "resolved": 156,
        "unresolved": 747,
        "audit_pass": 156,
        "audit_fail": 0,
        "resolution_rate": 156 / 903,
        "resolved_precision": 1.0,
    }
    knob_rows = {
        row["knob"]: row
        for row in csv.DictReader((tmp_path / "decision_knob_rows.csv").open(encoding="utf-8"))
    }
    dominance = knob_rows["endpoint_lock_then_upper_native_width_dominance"]
    assert dominance["valid_for_pgs_factorizer"] == "False"
    assert int(dominance["resolved"]) == 168
    assert int(dominance["audit_pass"]) == 167
    assert int(dominance["audit_fail"]) == 1

    first_failure = json.loads(
        (tmp_path / "upper_width_first_failure.json").read_text(encoding="utf-8")
    )
    assert first_failure == {
        "N": 16129,
        "audit_p": 127,
        "audit_q": 127,
        "case_id": "toy_le_199_127_127",
        "checked_cases_before_failure": 768,
        "diagonal_echo_count": 1,
        "knob": "endpoint_lock_then_upper_native_width_dominance",
        "lower_capacity_margin": -14,
        "max_audit_factor": 199,
        "mixed_topology_collision": True,
        "off_diagonal_count": 1,
        "selected_p": 89,
        "selected_q": 181,
        "selected_row_topology": "off_diagonal",
        "status": "failure",
        "survivor_count": 2,
        "upper_capacity_margin": 1,
    }
    failure_rows = list(
        csv.DictReader((tmp_path / "upper_width_failure_rows.csv").open(encoding="utf-8"))
    )
    assert failure_rows == [
        {
            "case_id": "toy_le_199_127_127",
            "N": "16129",
            "audit_p": "127",
            "audit_q": "127",
            "selected_p": "89",
            "selected_q": "181",
            "survivor_count": "2",
            "diagonal_echo_count": "1",
            "off_diagonal_count": "1",
            "selected_row_topology": "off_diagonal",
            "upper_capacity_margin": "1",
            "lower_capacity_margin": "-14",
            "mixed_topology_collision": "True",
        }
    ]
    matrix_rows = list(
        csv.DictReader((tmp_path / "rule_audit_matrix.csv").open(encoding="utf-8"))
    )
    assert len(matrix_rows) == 903 * 7
    structural_rows = list(
        csv.DictReader(
            (tmp_path / "structural_candidate_matrix.csv").open(encoding="utf-8")
        )
    )
    assert len(structural_rows) == 903 * 8
    law_rows = list(
        csv.DictReader((tmp_path / "pgspg_law_matrix.csv").open(encoding="utf-8"))
    )
    assert len(law_rows) == 2346 * 8
    replay_rows = list(
        csv.DictReader(
            (tmp_path / "directed_reset_replay_matrix.csv").open(encoding="utf-8")
        )
    )
    assert len(replay_rows) == 2346 * 2
    none_none_rows = list(
        csv.DictReader(
            (tmp_path / "none_none_replay_alias_rows.csv").open(encoding="utf-8")
        )
    )
    assert len(none_none_rows) == 78
    assert sum(row["audit_role"] == "false_alias" for row in none_none_rows) == 52
    assert not any(
        row["case_id"] == "toy_le_199_127_127"
        and row["selected_p"] == "89"
        and row["selected_q"] == "181"
        for row in none_none_rows
    )
    failure_replay = [
        row
        for row in replay_rows
        if row["case_id"] == "toy_le_199_127_127"
        and row["audit_role"] == "false_alias"
    ]
    assert [
        (row["direction"], row["first_divergence_stage"])
        for row in failure_replay
    ] == [
        ("lower_to_upper", "deadline_transport"),
        ("upper_to_lower", "deadline_kind"),
    ]
    failure_laws = [
        row
        for row in law_rows
        if row["case_id"] == "toy_le_199_127_127"
        and row["lower_reset_endpoint"] == "89"
        and row["upper_reset_endpoint"] == "181"
        and row["law_holds"] == "True"
    ]
    assert [row["law"] for row in failure_laws] == [
        "one_sided_chamber_containment",
    ]
    structural_failure = [
        row
        for row in structural_rows
        if row["case_id"] == "toy_le_199_127_127"
        and row["candidate"] == "unique_diagonal_echo"
    ]
    assert structural_failure[0]["rule_action"] == "positive_certificate"
    staged_failures = [
        row
        for row in matrix_rows
        if row["knob"] == "endpoint_lock_then_upper_native_width_dominance"
        and row["rule_action"] == "invalid_selector"
    ]
    assert staged_failures == [
        {
            "case_id": "toy_le_199_127_127",
            "N": "16129",
            "knob": "endpoint_lock_then_upper_native_width_dominance",
            "rule_family": "staged_one_sided_capacity",
            "valid_for_pgs_factorizer": "False",
            "rule_action": "invalid_selector",
            "survivor_count": "2",
            "endpoint_lock_state": "ambiguous",
            "diagonal_echo_count": "1",
            "off_diagonal_count": "1",
            "mixed_topology_collision": "True",
            "reciprocal_image_containment_state": "both=0;upper_only=1;lower_only=0;neither=1",
            "signature_compatibility": "equal=1;unequal=1",
            "carrier_compatibility": "equal=1;unequal=1",
            "selected_p": "89",
            "selected_q": "181",
            "audit_p": "127",
            "audit_q": "127",
            "selected_row_topology": "off_diagonal",
            "upper_capacity_margin": "1",
            "lower_capacity_margin": "-14",
        }
    ]


def test_upper_width_failure_topology_on_next_surface_251(tmp_path):
    """The next larger surface should keep topology failure rows explicit."""
    controller = load_module("controller")

    summary = controller.run_experiment(tmp_path, max_audit_factor=251)

    assert summary == {
        "total_cases": 1275,
        "resolved": 169,
        "unresolved": 1106,
        "audit_pass": 169,
        "audit_fail": 0,
        "resolution_rate": 169 / 1275,
        "resolved_precision": 1.0,
    }
    knob_rows = {
        row["knob"]: row
        for row in csv.DictReader((tmp_path / "decision_knob_rows.csv").open(encoding="utf-8"))
    }
    dominance = knob_rows["endpoint_lock_then_upper_native_width_dominance"]
    assert int(dominance["resolved"]) == 179
    assert int(dominance["audit_pass"]) == 179
    assert int(dominance["audit_fail"]) == 0

    first_failure = json.loads(
        (tmp_path / "upper_width_first_failure.json").read_text(encoding="utf-8")
    )
    assert first_failure == {
        "checked_cases": 1275,
        "knob": "endpoint_lock_then_upper_native_width_dominance",
        "max_audit_factor": 251,
        "status": "no_failure",
    }
    failure_rows = list(
        csv.DictReader((tmp_path / "upper_width_failure_rows.csv").open(encoding="utf-8"))
    )
    assert failure_rows == []
    matrix_rows = list(
        csv.DictReader((tmp_path / "rule_audit_matrix.csv").open(encoding="utf-8"))
    )
    assert len(matrix_rows) == 1275 * 7
    structural_rows = list(
        csv.DictReader(
            (tmp_path / "structural_candidate_matrix.csv").open(encoding="utf-8")
        )
    )
    assert len(structural_rows) == 1275 * 8
    law_rows = list(
        csv.DictReader((tmp_path / "pgspg_law_matrix.csv").open(encoding="utf-8"))
    )
    assert len(law_rows) == 3625 * 8
    replay_rows = list(
        csv.DictReader(
            (tmp_path / "directed_reset_replay_matrix.csv").open(encoding="utf-8")
        )
    )
    assert len(replay_rows) == 3625 * 2
    none_none_rows = list(
        csv.DictReader(
            (tmp_path / "none_none_replay_alias_rows.csv").open(encoding="utf-8")
        )
    )
    assert len(none_none_rows) == 101
    assert sum(row["audit_role"] == "false_alias" for row in none_none_rows) == 70
    lower_deadline_false_aliases = [
        row
        for row in replay_rows
        if row["direction"] == "lower_to_upper"
        and row["audit_role"] == "false_alias"
        and row["first_divergence_stage"] == "deadline_transport"
    ]
    assert len(lower_deadline_false_aliases) == 1120
    reset_echo_false_aliases = [
        row
        for row in law_rows
        if row["law"] == "reset_signature_echo"
        and row["audit_role"] == "false_alias"
        and row["law_holds"] == "True"
    ]
    assert len(reset_echo_false_aliases) == 451
    diagonal_actions = [
        row["rule_action"]
        for row in structural_rows
        if row["candidate"] == "unique_diagonal_echo"
    ]
    assert diagonal_actions.count("positive_certificate") == 50
    assert diagonal_actions.count("invalid_selector") == 107
    staged_actions = [
        row["rule_action"]
        for row in matrix_rows
        if row["knob"] == "endpoint_lock_then_upper_native_width_dominance"
    ]
    assert staged_actions.count("positive_certificate") == 179
    assert staged_actions.count("invalid_selector") == 0
