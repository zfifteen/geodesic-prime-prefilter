"""Tests for the toy exponent-wall harness."""

from __future__ import annotations

import csv
import importlib.util
import json
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[3]
SCRIPT_DIR = ROOT / "experiments" / "exponents" / "scripts"
MECHANISM_PATH = SCRIPT_DIR / "toy_exponent_wall_pgs_mechanism.py"
VALIDATOR_PATH = SCRIPT_DIR / "toy_exponent_wall_validator.py"
CONTROLLER_PATH = SCRIPT_DIR / "toy_exponent_wall_mechanics_probe.py"


def load_module(path: Path, name: str):
    """Load one probe module."""
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"unable to load {name}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_pgs_mechanism_has_no_classical_lookup_imports():
    """The live mechanism should not contain classical lookup tools."""
    source = MECHANISM_PATH.read_text(encoding="utf-8")

    for forbidden in ["factorint", "isprime", "nextprime", "prevprime", "KNOWN_MERSENNE"]:
        assert forbidden not in source


def test_pgs_surface_is_power_of_two_only():
    """The PGS surface should contain only powers of two."""
    mechanism = load_module(MECHANISM_PATH, "toy_exponent_wall_pgs_mechanism")
    rows = mechanism.collect_rows(2, 6)

    assert [row["exponent"] for row in rows] == [2, 3, 4, 5, 6]
    assert all(row["number_family"] == "power_of_two" for row in rows)
    assert all(row["power_of_two"] == 2 ** int(row["exponent"]) for row in rows)
    assert all(row["left_prime_rule_id"] == mechanism.PGS_LEFT_PRIME_RULE_ID for row in rows)


def test_pgs_left_prime_uses_wheel_open_candidates():
    """The PGS mechanism should check admissible left-prime candidates."""
    mechanism = load_module(MECHANISM_PATH, "toy_exponent_wall_pgs_mechanism")

    assert mechanism.left_prime_candidate_offsets(64, 8) == [3, 5]
    assert mechanism.left_prime_candidate_offsets(32, 4) == [1, 3]
    assert mechanism.left_prime_candidate_offsets(4, 2) == [1, 2]


def test_pgs_record_tracks_rejected_candidate_offsets():
    """The PGS record should expose rejected offsets before the left prime."""
    mechanism = load_module(MECHANISM_PATH, "toy_exponent_wall_pgs_mechanism")
    record = mechanism.recover_left_prime_record(2048)

    assert record["left_prime"] == 2039
    assert record["distance_to_left_prime"] == 9
    assert record["candidate_checks"] == 3
    assert record["rejected_candidate_offsets_before_left_prime"] == "1;7"


def test_pgs_recovery_fails_loudly_when_bound_is_too_small():
    """The PGS mechanism should raise instead of falling back."""
    mechanism = load_module(MECHANISM_PATH, "toy_exponent_wall_pgs_mechanism")

    with pytest.raises(mechanism.PGSLeftPrimeUnresolvedError):
        mechanism.recover_left_prime(64, candidate_bound=2)


def test_pgs_mersenne_location_inference_is_distance_one():
    """Mersenne-location inference should be exactly distance one."""
    mechanism = load_module(MECHANISM_PATH, "toy_exponent_wall_pgs_mechanism")
    inferred = mechanism.pgs_row(5)
    not_inferred = mechanism.pgs_row(6)

    assert inferred["distance_to_left_prime"] == 1
    assert inferred["mersenne_location_inferred"] is True
    assert not_inferred["distance_to_left_prime"] == 3
    assert not_inferred["mersenne_location_inferred"] is False


def test_validator_uses_classical_checks_after_pgs_rows():
    """The validator should audit PGS rows with classical checks."""
    mechanism = load_module(MECHANISM_PATH, "toy_exponent_wall_pgs_mechanism")
    validator = load_module(VALIDATOR_PATH, "toy_exponent_wall_validator")
    pgs_rows = [
        {key: str(value) for key, value in mechanism.pgs_row(5).items()},
        {key: str(value) for key, value in mechanism.pgs_row(6).items()},
    ]

    rows = validator.validate_rows(pgs_rows)

    assert rows[0]["classical_mersenne_number_is_prime"] is True
    assert rows[0]["classical_agreement"] is True
    assert rows[1]["classical_mersenne_number_is_prime"] is False
    assert rows[1]["classical_agreement"] is True
    assert rows[1]["mersenne_number_factor_signature"] == "3^2*7"


def test_controller_runs_pgs_then_validation_and_reconciles(tmp_path):
    """The controller should write separate PGS and validation artifacts."""
    controller = load_module(CONTROLLER_PATH, "toy_exponent_wall_mechanics_probe")
    out = tmp_path / "out"

    summary = controller.run_controller(
        min_exponent=2,
        max_exponent=8,
        candidate_bound=128,
        output_dir=out,
    )

    pgs_summary_path = out / "pgs_summary.json"
    validation_summary_path = out / "validation_summary.json"
    combined_summary_path = out / "summary.json"
    pgs_rows_path = out / "pgs_power_of_two_rows.csv"
    validation_rows_path = out / "validation_rows.csv"
    inferred_path = out / "mersenne_location_inferred_rows.csv"
    not_inferred_path = out / "mersenne_location_not_inferred_rows.csv"
    for path in [
        pgs_summary_path,
        validation_summary_path,
        combined_summary_path,
        pgs_rows_path,
        validation_rows_path,
        inferred_path,
        not_inferred_path,
    ]:
        assert path.exists()
        assert b"\r\n" not in path.read_bytes()

    pgs_summary = json.loads(pgs_summary_path.read_text(encoding="utf-8"))
    validation_summary = json.loads(validation_summary_path.read_text(encoding="utf-8"))
    pgs_rows = list(csv.DictReader(pgs_rows_path.open(encoding="utf-8", newline="")))
    validation_rows = list(csv.DictReader(validation_rows_path.open(encoding="utf-8", newline="")))
    assert summary["controller_order"] == "pgs_mechanism_then_classical_validation"
    assert summary == json.loads(combined_summary_path.read_text(encoding="utf-8"))
    assert pgs_summary["row_count"] == len(pgs_rows)
    assert validation_summary["validated_row_count"] == len(validation_rows)
    assert pgs_summary["row_count"] == validation_summary["validated_row_count"]
    assert validation_summary["classical_false_positive_count"] == 0
    assert validation_summary["classical_false_negative_count"] == 0
