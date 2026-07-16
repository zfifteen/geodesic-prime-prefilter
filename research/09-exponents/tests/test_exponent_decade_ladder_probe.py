"""Tests for the exponent-decade ladder harness."""

from __future__ import annotations

import csv
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
SCRIPT_DIR = ROOT / "research" / "09-exponents" / "scripts"
MECHANISM_PATH = SCRIPT_DIR / "exponent_decade_ladder_pgs_mechanism.py"
VALIDATOR_PATH = SCRIPT_DIR / "exponent_decade_ladder_validator.py"
CONTROLLER_PATH = SCRIPT_DIR / "exponent_decade_ladder_probe.py"


def load_module(path: Path, name: str):
    """Load one probe module."""
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"unable to load {name}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_pgs_ladder_mechanism_has_no_forbidden_classical_tools():
    """The live ladder mechanism should not contain classical lookup tools."""
    source = MECHANISM_PATH.read_text(encoding="utf-8")

    for forbidden in ["factorint", "isprime", "nextprime", "prevprime", "KNOWN_MERSENNE"]:
        assert forbidden not in source


def test_composite_exponent_is_excluded_before_wall_recovery():
    """Composite exponents should stop at the exponent divisor-count gate."""
    mechanism = load_module(MECHANISM_PATH, "exponent_decade_ladder_pgs_mechanism")
    row = mechanism.pgs_row(100, 100, candidate_bound=4096)

    assert row["exponent_divisor_count"] == 9
    assert row["exponent_status"] == mechanism.STATUS_EXPONENT_DIVISOR_COUNT_NOT_TWO
    assert row["power_of_two"] == ""
    assert row["mersenne_number"] == ""
    assert row["left_prime"] == ""


def test_ladder_rows_are_non_cumulative_windows():
    """The primary ladder rows should contain each exponent once."""
    mechanism = load_module(MECHANISM_PATH, "exponent_decade_ladder_pgs_mechanism")
    rows = mechanism.collect_rows([31, 100], candidate_bound=4096)
    exponents = [int(row["exponent"]) for row in rows]

    assert len(rows) == 99
    assert len(set(exponents)) == 99
    assert min(exponents) == 2
    assert max(exponents) == 100
    assert {int(row["rung_min_exponent"]) for row in rows if int(row["rung_max_exponent"]) == 31} == {2}
    assert {int(row["rung_min_exponent"]) for row in rows if int(row["rung_max_exponent"]) == 100} == {32}


def test_known_small_inferred_exponents_have_distance_one():
    """Small inferred exponent rows should recover distance one under both modes."""
    mechanism = load_module(MECHANISM_PATH, "exponent_decade_ladder_pgs_mechanism")

    for mode in [
        mechanism.INFERENCE_RESIDUE_RETURN,
        mechanism.INFERENCE_LEFT_PRIME,
    ]:
        for exponent in [31, 61, 127]:
            row = mechanism.pgs_row(
                exponent,
                exponent,
                candidate_bound=4096,
                mersenne_inference=mode,
            )
            assert row["exponent_status"] == mechanism.STATUS_LEFT_PRIME_RESOLVED
            assert row["distance_to_left_prime"] == 1
            assert row["mersenne_location_inferred"] is True
            assert row["mersenne_inference_mode"] == mode


def test_residue_return_defers_without_multi_offset_distance():
    """Residue-return mode defers composite Mersenne cells without left-prime distance."""
    mechanism = load_module(MECHANISM_PATH, "exponent_decade_ladder_pgs_mechanism")
    row = mechanism.pgs_row(
        11,
        11,
        candidate_bound=4096,
        mersenne_inference=mechanism.INFERENCE_RESIDUE_RETURN,
    )

    assert row["exponent_status"] == mechanism.STATUS_LEFT_PRIME_RESOLVED
    assert row["mersenne_location_inferred"] is False
    assert row["distance_to_left_prime"] == ""
    assert row["candidate_checks"] == 1
    assert row["residue_return_status"] == "residue_return_deferred"


def test_small_prime_exponent_can_resolve_without_inference():
    """A resolved prime exponent can still miss the distance-one condition."""
    mechanism = load_module(MECHANISM_PATH, "exponent_decade_ladder_pgs_mechanism")
    row = mechanism.pgs_row(
        11,
        11,
        candidate_bound=4096,
        mersenne_inference=mechanism.INFERENCE_LEFT_PRIME,
    )

    assert row["exponent_status"] == mechanism.STATUS_LEFT_PRIME_RESOLVED
    assert row["distance_to_left_prime"] == 9
    assert row["mersenne_location_inferred"] is False


def test_unresolved_rows_are_explicit_when_bound_is_too_small():
    """A small candidate bound should create an explicit unresolved row."""
    mechanism = load_module(MECHANISM_PATH, "exponent_decade_ladder_pgs_mechanism")
    row = mechanism.pgs_row(
        11,
        11,
        candidate_bound=2,
        mersenne_inference=mechanism.INFERENCE_LEFT_PRIME,
    )

    assert row["exponent_status"] == mechanism.STATUS_LEFT_PRIME_UNRESOLVED
    assert row["candidate_bound"] == 2
    assert row["unresolved_reason"] == "candidate_bound_exhausted"
    assert row["distance_to_left_prime"] == ""
    assert row["mersenne_location_inferred"] is False


def test_unresolved_rows_are_explicit_when_work_limit_is_hit(monkeypatch):
    """A per-candidate work limit should create an explicit unresolved row."""
    mechanism = load_module(MECHANISM_PATH, "exponent_decade_ladder_pgs_mechanism")

    def raise_work_limit(_candidate, _seconds_limit):
        raise mechanism.CandidateWorkLimitReached

    monkeypatch.setattr(mechanism, "limited_tau", raise_work_limit)
    row = mechanism.pgs_row(
        97,
        97,
        candidate_bound=4096,
        candidate_seconds_limit=0.001,
        mersenne_inference=mechanism.INFERENCE_LEFT_PRIME,
    )

    assert row["exponent_status"] == mechanism.STATUS_LEFT_PRIME_UNRESOLVED
    assert row["unresolved_reason"] == "candidate_work_limit"
    assert row["distance_to_left_prime"] == ""
    assert row["mersenne_location_inferred"] is False


def test_residue_return_work_limit_is_explicit(monkeypatch):
    """Residue-return mode should surface offset-1 work-limit unresolved rows."""
    mechanism = load_module(MECHANISM_PATH, "exponent_decade_ladder_pgs_mechanism")

    def raise_work_limit(*_args, **_kwargs):
        raise mechanism.CandidateWorkLimitReached

    monkeypatch.setattr(mechanism, "limited_call", raise_work_limit)
    row = mechanism.pgs_row(
        97,
        97,
        candidate_bound=4096,
        candidate_seconds_limit=0.001,
        mersenne_inference=mechanism.INFERENCE_RESIDUE_RETURN,
    )

    assert row["exponent_status"] == mechanism.STATUS_LEFT_PRIME_UNRESOLVED
    assert row["unresolved_reason"] == "candidate_work_limit"
    assert row["unresolved_candidate_offset"] == 1
    assert row["mersenne_location_inferred"] is False


def test_validator_checks_after_pgs_rows():
    """The validator should audit emitted PGS rows."""
    mechanism = load_module(MECHANISM_PATH, "exponent_decade_ladder_pgs_mechanism")
    validator = load_module(VALIDATOR_PATH, "exponent_decade_ladder_validator")
    pgs_rows = [
        {
            key: str(value)
            for key, value in mechanism.pgs_row(
                31, 31, 4096, mersenne_inference=mechanism.INFERENCE_RESIDUE_RETURN
            ).items()
        },
        {
            key: str(value)
            for key, value in mechanism.pgs_row(
                11, 11, 4096, mersenne_inference=mechanism.INFERENCE_RESIDUE_RETURN
            ).items()
        },
        {
            key: str(value)
            for key, value in mechanism.pgs_row(
                100, 100, 4096, mersenne_inference=mechanism.INFERENCE_RESIDUE_RETURN
            ).items()
        },
    ]

    rows = validator.validate_rows(pgs_rows)

    assert rows[0]["classical_mersenne_number_is_prime"] is True
    assert rows[0]["classical_agreement"] is True
    assert rows[1]["classical_mersenne_number_is_prime"] is False
    assert rows[1]["classical_agreement"] is True
    assert rows[2]["classical_validation_reason"] == "composite_exponent"
    assert rows[2]["classical_agreement"] is True


def test_controller_outputs_reconcile_and_are_lf_terminated(tmp_path):
    """The controller should write separate reconciled artifacts."""
    controller = load_module(CONTROLLER_PATH, "exponent_decade_ladder_probe")
    out = tmp_path / "out"

    summary = controller.run_controller(
        rungs=[11, 31],
        candidate_bound=4096,
        candidate_seconds_limit=1.0,
        output_dir=out,
        mersenne_inference="residue_return",
    )

    paths = [
        out / "pgs_ladder_rows.csv",
        out / "pgs_rung_summary_rows.csv",
        out / "pgs_cumulative_summary_rows.csv",
        out / "pgs_summary.json",
        out / "validation_rows.csv",
        out / "validation_summary.json",
        out / "summary.json",
        out / "mersenne_location_inferred_rows.csv",
        out / "pgs_unresolved_rows.csv",
    ]
    for path in paths:
        assert path.exists()
        assert b"\r\n" not in path.read_bytes()

    pgs_rows = list(csv.DictReader((out / "pgs_ladder_rows.csv").open(encoding="utf-8", newline="")))
    validation_rows = list(
        csv.DictReader((out / "validation_rows.csv").open(encoding="utf-8", newline=""))
    )
    pgs_summary = json.loads((out / "pgs_summary.json").read_text(encoding="utf-8"))
    validation_summary = json.loads((out / "validation_summary.json").read_text(encoding="utf-8"))

    assert summary == json.loads((out / "summary.json").read_text(encoding="utf-8"))
    assert summary["controller_order"] == "pgs_mechanism_then_classical_validation"
    assert pgs_summary["row_count"] == len(pgs_rows)
    assert pgs_summary["row_model"] == "non_cumulative_exponent_windows"
    assert pgs_summary["unique_exponents_tested"] == len(pgs_rows)
    assert validation_summary["validated_row_count"] == len(validation_rows)
    assert len(pgs_rows) == len(validation_rows)
    assert validation_summary["classical_false_positive_count"] == 0
    assert validation_summary["classical_false_negative_count"] == 0
