"""Tests for the unresolved exponent pressure harness."""

from __future__ import annotations

import csv
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
SCRIPT_DIR = ROOT / "research" / "09-exponents" / "scripts"
PGS_PATH = SCRIPT_DIR / "exponent_unresolved_pressure_pgs_mechanism.py"
VALIDATOR_PATH = SCRIPT_DIR / "exponent_unresolved_pressure_validator.py"
CONTROLLER_PATH = SCRIPT_DIR / "exponent_unresolved_pressure_probe.py"


def load_module(path: Path, name: str):
    """Load one probe module."""
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"unable to load {name}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def unresolved_source_row(exponent: int = 11) -> dict[str, str]:
    """Return one unresolved source row."""
    return {
        "rung_min_exponent": "2",
        "rung_max_exponent": "31",
        "exponent": str(exponent),
        "exponent_divisor_count": "2",
        "exponent_status": "left_prime_unresolved",
        "number_family": "power_of_two",
        "left_prime_rule_id": "pgs_left_prime_wheel_open_v1",
        "candidate_bound": "2",
        "candidate_seconds_limit": "1.0",
        "candidate_checks": "2",
        "rejected_candidate_offsets_before_left_prime": "1;7",
        "unresolved_reason": "candidate_bound_exhausted",
        "unresolved_candidate_offset": "",
        "power_of_two": str(2**exponent),
        "mersenne_number": str(2**exponent - 1),
        "distance_to_left_prime": "",
        "mersenne_location_inferred": "False",
        "left_prime": "",
    }


def test_pressure_pgs_mechanism_has_no_forbidden_classical_tools():
    """The pressure PGS mechanism should not contain classical lookup tools."""
    source = PGS_PATH.read_text(encoding="utf-8")

    for forbidden in ["factorint", "isprime", "nextprime", "prevprime", "KNOWN_MERSENNE"]:
        assert forbidden not in source


def test_pressure_resolves_source_row_with_same_pgs_rule():
    """A pressure row should rerun the same PGS boundary rule."""
    pressure = load_module(PGS_PATH, "exponent_unresolved_pressure_pgs_mechanism")
    row = pressure.pressure_row(
        unresolved_source_row(11),
        candidate_bound=4096,
        candidate_seconds_limit=1.0,
    )

    assert row["exponent"] == 11
    assert row["pressure_exponent_status"] == "left_prime_resolved"
    assert row["distance_to_left_prime"] == 9
    assert row["mersenne_location_inferred"] is False


def test_pressure_keeps_unresolved_rows_explicit(monkeypatch):
    """A pressure work-limit row should remain explicit."""
    pressure = load_module(PGS_PATH, "exponent_unresolved_pressure_pgs_mechanism")
    ladder = pressure.ladder

    def raise_work_limit(_candidate, _seconds_limit):
        raise ladder.CandidateWorkLimitReached

    monkeypatch.setattr(ladder, "limited_tau", raise_work_limit)
    row = pressure.pressure_row(
        unresolved_source_row(11),
        candidate_bound=4096,
        candidate_seconds_limit=1.0,
    )

    assert row["pressure_exponent_status"] == "left_prime_unresolved"
    assert row["pressure_unresolved_reason"] == "candidate_work_limit"


def test_pressure_accepts_previous_pressure_unresolved_rows():
    """A later pressure pass should accept rows from a prior pressure pass."""
    pressure = load_module(PGS_PATH, "exponent_unresolved_pressure_pgs_mechanism")
    previous = {
        "source_rung_min_exponent": "2",
        "source_rung_max_exponent": "31",
        "exponent": "11",
        "exponent_divisor_count": "2",
        "pressure_candidate_bound": "2",
        "pressure_candidate_seconds_limit": "1.0",
        "pressure_candidate_checks": "2",
        "pressure_unresolved_candidate_offset": "",
    }

    row = pressure.pressure_row(
        previous,
        candidate_bound=4096,
        candidate_seconds_limit=1.0,
    )

    assert row["exponent"] == 11
    assert row["pressure_exponent_status"] == "left_prime_resolved"
    assert row["distance_to_left_prime"] == 9


def test_pressure_validator_validates_inferred_rows_only():
    """The validator should validate rows already inferred by PGS."""
    validator = load_module(VALIDATOR_PATH, "exponent_unresolved_pressure_validator")
    rows = validator.validate_rows(
        [
            {
                "exponent": "31",
                "mersenne_number": str(2**31 - 1),
                "mersenne_location_inferred": "True",
            }
        ]
    )

    assert rows[0]["classical_mersenne_number_is_prime"] is True
    assert rows[0]["classical_agreement"] is True


def test_pressure_controller_outputs_reconcile(tmp_path):
    """The controller should write pressure and validation artifacts."""
    controller = load_module(CONTROLLER_PATH, "exponent_unresolved_pressure_probe")
    input_path = tmp_path / "source.csv"
    with input_path.open("w", encoding="utf-8", newline="") as handle:
        fieldnames = list(unresolved_source_row().keys())
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerow(unresolved_source_row(11))
    out = tmp_path / "out"

    summary = controller.run_controller(
        input_path=input_path,
        output_dir=out,
        candidate_bound=4096,
        candidate_seconds_limit=1.0,
    )

    paths = [
        out / "resolved_after_pressure_rows.csv",
        out / "still_unresolved_rows.csv",
        out / "inferred_after_pressure_rows.csv",
        out / "pressure_summary.json",
        out / "validation_rows.csv",
        out / "validation_summary.json",
        out / "summary.json",
    ]
    for path in paths:
        assert path.exists()
        assert b"\r\n" not in path.read_bytes()

    pressure_summary = json.loads((out / "pressure_summary.json").read_text(encoding="utf-8"))
    validation_summary = json.loads((out / "validation_summary.json").read_text(encoding="utf-8"))
    assert pressure_summary["source_unresolved_count"] == 1
    assert pressure_summary["resolved_after_pressure_count"] == 1
    assert validation_summary["validated_inferred_count"] == 0
    assert summary == json.loads((out / "summary.json").read_text(encoding="utf-8"))
