"""Tests for PGSMPG v0.1."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[3]
SCRIPT_DIR = ROOT / "experiments" / "exponents" / "scripts"
GENERATOR_PATH = SCRIPT_DIR / "pgs_mersenne_prime_generator.py"
CONTROLLER_PATH = SCRIPT_DIR / "pgs_mersenne_prime_controller.py"
VALIDATOR_PATH = SCRIPT_DIR / "pgs_mersenne_prime_validator.py"


def load_module(path: Path, name: str):
    """Load one script module."""
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"unable to load {name}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_pgsmpg_record_has_only_p_and_q():
    """The emitted PGSMPG record should stay minimal."""
    generator = load_module(GENERATOR_PATH, "pgs_mersenne_prime_generator")

    assert generator.emit_record(31, max_exponent=127, candidate_bound=4096) == {
        "p": 31,
        "q": 61,
    }


def test_pgsmpg_generator_has_no_forbidden_classical_tools():
    """The live generator source should stay inside the PGS path."""
    source = GENERATOR_PATH.read_text(encoding="utf-8")

    forbidden_terms = [
        "factorint",
        "isprime",
        "nextprime",
        "prevprime",
        "KNOWN_MERSENNE",
        "known Mersenne",
        "Miller",
        "miller",
        "trial",
        "fallback",
        "random",
    ]
    assert all(term not in source for term in forbidden_terms)


def test_input_exponent_is_accepted_without_internal_validation():
    """The generator should treat p as accepted input state."""
    generator = load_module(GENERATOR_PATH, "pgs_mersenne_prime_generator")

    assert generator.emit_record(11, max_exponent=17, candidate_bound=4096) == {
        "p": 11,
        "q": 13,
    }


def test_composite_candidate_exponent_stops_before_wall_recovery(monkeypatch):
    """Composite candidate exponents should stop at the exponent divisor-count gate."""
    generator = load_module(GENERATOR_PATH, "pgs_mersenne_prime_generator")

    def should_not_run(_exponent, _candidate_bound):
        raise AssertionError("successor boundary inspection should not run")

    monkeypatch.setattr(generator, "left_boundary_state_certificate", should_not_run)
    row = generator.exponent_attempt_row(4, candidate_bound=4096)

    assert row["exponent_divisor_count"] == 3
    assert row["status"] == generator.STATUS_EXPONENT_DIVISOR_COUNT_NOT_TWO
    assert row["boundary_certificate"] is None


def test_known_small_transitions_resolve():
    """Small accepted exponents should resolve to the next PGSMPG exponent."""
    generator = load_module(GENERATOR_PATH, "pgs_mersenne_prime_generator")

    assert generator.emit_record(3, max_exponent=31, candidate_bound=4096) == {
        "p": 3,
        "q": 5,
    }
    assert generator.emit_record(7, max_exponent=31, candidate_bound=4096) == {
        "p": 7,
        "q": 13,
    }
    assert generator.emit_record(31, max_exponent=127, candidate_bound=4096) == {
        "p": 31,
        "q": 61,
    }


def test_admissible_left_offsets_match_reference_order():
    """The direct offset enumerator should preserve the original ordered surface."""
    generator = load_module(GENERATOR_PATH, "pgs_mersenne_prime_generator")

    def reference_offsets(exponent: int, candidate_bound: int) -> list[int]:
        power_residue_mod30 = pow(2, exponent, 30)
        small_power = 2**exponent if exponent <= 3 else None
        return [
            offset
            for offset in range(1, candidate_bound + 1)
            if (
                small_power is not None
                and small_power - offset in generator.LOW_PRIMES
            )
            or (
                power_residue_mod30 - offset
            ) % 30 in generator.WHEEL_OPEN_RESIDUES_MOD30
        ]

    for exponent in range(2, 201):
        for candidate_bound in [1, 2, 3, 29, 30, 31, 59, 60, 61, 128, 4096]:
            assert generator.admissible_left_offsets(
                exponent,
                candidate_bound,
            ) == reference_offsets(exponent, candidate_bound)


def test_too_small_max_exponent_raises_unresolved():
    """A bounded surface with no inferred successor should fail explicitly."""
    generator = load_module(GENERATOR_PATH, "pgs_mersenne_prime_generator")

    with pytest.raises(generator.PGSMPGUnresolvedError):
        generator.resolve_q(31, max_exponent=60, candidate_bound=4096)


def test_too_small_candidate_bound_records_unresolved_boundary_state():
    """A non-survivor offset-1 cell should defer without boundary scanning."""
    generator = load_module(GENERATOR_PATH, "pgs_mersenne_prime_generator")
    row = generator.exponent_attempt_row(11, candidate_bound=2)

    assert row["status"] == generator.STATUS_RESIDUE_RETURN_DEFERRED
    assert row["residue_return_pressure"]["offset_from_power_of_two"] == 1
    assert row["residue_return_pressure"]["candidate_divisor_count"] > 2
    assert row["distance_to_left_boundary"] == ""
    assert row["mersenne_location_inferred"] is False


def test_residue_return_pressure_resolves_offset_one_survivor():
    """A surviving offset-1 chamber cell should resolve the Mersenne location."""
    generator = load_module(GENERATOR_PATH, "pgs_mersenne_prime_generator")
    pressure = generator.residue_return_pressure(31)
    row = generator.exponent_attempt_row(31, candidate_bound=4096)

    assert pressure["status"] == generator.STATUS_RESIDUE_RETURN_RESOLVED_SURVIVOR
    assert pressure["pressure"] == 0
    assert row["status"] == generator.STATUS_MERSENNE_LOCATION_INFERRED
    assert row["distance_to_left_boundary"] == 1
    assert row["boundary_certificate"]["candidate_state_count"] == 1
    assert row["boundary_certificate"]["residue_return_pressure"] == pressure


def test_deferred_residue_return_candidate_does_not_run_full_boundary_scan(monkeypatch):
    """Deferred candidates should not pay for a wider left-boundary scan."""
    generator = load_module(GENERATOR_PATH, "pgs_mersenne_prime_generator")

    def should_not_run(_exponent, _candidate_bound):
        raise AssertionError("deferred residue-return state should not scan")

    monkeypatch.setattr(generator, "left_boundary_state_certificate", should_not_run)

    assert generator.emit_record(7, max_exponent=13, candidate_bound=4096) == {
        "p": 7,
        "q": 13,
    }


def test_boundary_certificate_uses_compact_integer_diagnostics():
    """PGSMPG diagnostics should avoid serializing full power-sized integers."""
    generator = load_module(GENERATOR_PATH, "pgs_mersenne_prime_generator")
    certificate = generator.left_boundary_state_certificate(31, candidate_bound=4096)

    assert certificate["distance_to_left_boundary"] == 1
    assert certificate["power_of_two_bit_length"] == 32
    assert certificate["left_boundary_bit_length"] == 31
    assert certificate["left_boundary_offset_from_power_of_two"] == 1
    assert "power_of_two" not in certificate
    assert "left_boundary" not in certificate
    assert "carrier_w" not in certificate
    assert "candidate_states" not in certificate
    assert certificate["candidate_state_count"] == 1
    assert certificate["closed_offset_count_before_boundary"] == 0


def test_boundary_scan_only_counts_admissible_offsets(monkeypatch):
    """The v0.1 boundary scan should skip impossible left offsets."""
    generator = load_module(GENERATOR_PATH, "pgs_mersenne_prime_generator")
    original_tau = generator.tau
    calls = []

    def counted_tau(n):
        calls.append(n)
        return original_tau(n)

    monkeypatch.setattr(generator, "tau", counted_tau)
    certificate = generator.left_boundary_state_certificate(23, candidate_bound=4096)
    distance = int(certificate["distance_to_left_boundary"])
    expected_calls = [
        offset
        for offset in generator.admissible_left_offsets(23, 4096)
        if offset <= distance
    ]

    assert distance == 15
    assert len(calls) == len(expected_calls)
    assert len(calls) < distance


def test_validator_confirms_records_after_generation():
    """The validator should check already emitted records."""
    validator = load_module(VALIDATOR_PATH, "pgs_mersenne_prime_validator")
    rows = validator.validate_records([{"p": 31, "q": 61}, {"p": 31, "q": 89}])

    assert rows[0]["classical_next_known_mersenne_exponent"] == 61
    assert rows[0]["classical_mersenne_number_is_prime"] is True
    assert rows[0]["classical_agreement"] is True
    assert rows[1]["classical_mersenne_number_is_prime"] is True
    assert rows[1]["classical_agreement"] is False


def test_controller_writes_minimal_records_and_compact_diagnostics(tmp_path):
    """The controller should write generation-only artifacts."""
    controller = load_module(CONTROLLER_PATH, "pgs_mersenne_prime_controller")
    out = tmp_path / "out"

    summary = controller.run_controller(
        anchors=[3, 7, 13, 31],
        start_exponent=2,
        chain_length=10,
        max_exponent=127,
        candidate_bound=4096,
        output_dir=out,
    )

    paths = [
        out / "records.jsonl",
        out / "diagnostics.jsonl",
        out / "pgs_summary.json",
        out / "summary.json",
    ]
    for path in paths:
        assert path.exists()
        assert b"\r\n" not in path.read_bytes()

    records = [
        json.loads(line)
        for line in (out / "records.jsonl").read_text(encoding="utf-8").splitlines()
    ]
    diagnostics = [
        json.loads(line)
        for line in (out / "diagnostics.jsonl").read_text(encoding="utf-8").splitlines()
    ]
    pgs_summary = json.loads((out / "pgs_summary.json").read_text(encoding="utf-8"))

    assert all(set(record) == {"p", "q"} for record in records)
    assert records == [
        {"p": 3, "q": 5},
        {"p": 7, "q": 13},
        {"p": 13, "q": 17},
        {"p": 31, "q": 61},
    ]
    assert len(diagnostics) == len(records)
    assert all("certificate" not in row for row in diagnostics)
    assert all("attempt_count" in row for row in diagnostics)
    assert pgs_summary["emitted"] == len(records)
    assert pgs_summary["unresolved"] == 0
    assert not (out / "validation_rows.csv").exists()
    assert not (out / "validation_summary.json").exists()
    assert summary == json.loads((out / "summary.json").read_text(encoding="utf-8"))
    assert summary["controller_order"] == "pgs_generator_only"


def test_controller_default_chain_writes_ten_exponents(tmp_path):
    """The no-anchor path should emit the default ten-exponent chain."""
    controller = load_module(CONTROLLER_PATH, "pgs_mersenne_prime_controller")
    out = tmp_path / "out"

    summary = controller.run_controller(
        anchors=None,
        start_exponent=2,
        chain_length=10,
        max_exponent=127,
        candidate_bound=4096,
        output_dir=out,
    )

    exponents = [
        json.loads(line)["e"]
        for line in (out / "mersenne_exponents.jsonl").read_text(encoding="utf-8").splitlines()
    ]
    records = [
        json.loads(line)
        for line in (out / "records.jsonl").read_text(encoding="utf-8").splitlines()
    ]

    assert exponents == [2, 3, 5, 7, 13, 17, 19, 31, 61, 89]
    assert len(records) == 9
    assert records[0] == {"p": 2, "q": 3}
    assert records[-1] == {"p": 61, "q": 89}
    assert summary["pgs_generator"]["chain_exponent_count"] == 10
    assert summary["pgs_generator"]["chain_exponents"] == exponents
    assert summary["controller_order"] == "pgs_generator_only"
    assert "classical_validation" not in summary


def test_controller_cli_streams_chain_exponents(tmp_path, capsys):
    """The no-anchor CLI path should print each recovered exponent as it resolves."""
    controller = load_module(CONTROLLER_PATH, "pgs_mersenne_prime_controller")
    out = tmp_path / "out"

    assert controller.main(
        [
            "--chain-length",
            "4",
            "--max-exponent",
            "13",
            "--output-dir",
            str(out),
        ]
    ) == 0

    lines = capsys.readouterr().out.splitlines()
    assert lines[:4] == [
        "PGSMPG exponent: 2",
        "PGSMPG exponent: 3",
        "PGSMPG exponent: 5",
        "PGSMPG exponent: 7",
    ]
    assert "PGSMPG records: 3 emitted, 0 unresolved" in lines
