"""Tests for endpoint fixed-point decomposition in width-2 chambers."""

from __future__ import annotations

import csv
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
MODULE_PATH = (
    ROOT
    / "research"
    / "10-twin-primes"
    / "scripts"
    / "twin_prime_endpoint_fixed_point_decomposition_probe.py"
)


def load_module():
    """Load the endpoint decomposition probe from its file path."""
    spec = importlib.util.spec_from_file_location(
        "twin_prime_endpoint_fixed_point_decomposition_probe",
        MODULE_PATH,
    )
    if spec is None or spec.loader is None:
        raise RuntimeError("unable to load twin_prime_endpoint_fixed_point_decomposition_probe module")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_factorization_and_endpoint_family_are_exact():
    """Endpoint families should follow the exact factorization."""
    module = load_module()

    assert module.factorization(13) == [(13, 1)]
    assert module.factorization(49) == [(7, 2)]
    assert module.factorization(77) == [(7, 1), (11, 1)]
    assert module.tau_from_factors([(7, 2)]) == 3
    assert module.factor_signature([(7, 2), (11, 1)]) == "7^2*11"
    assert module.endpoint_family([(13, 1)], 2) == "fixed_point"
    assert module.endpoint_family([(7, 2)], 3) == "prime_square"
    assert module.endpoint_family([(7, 1), (11, 1)], 4) == "semiprime_distinct"
    assert module.reduced_obstruction_family(None) == "endpoint_fixed_point"
    assert (
        module.reduced_obstruction_family("fixed_point")
        == "least_factor_times_fixed_point_cofactor"
    )
    assert (
        module.reduced_obstruction_family("semiprime_distinct")
        == "least_factor_times_semiprime_cofactor"
    )
    assert module.second_strip_family(None) == "not_second_stripped"
    assert (
        module.second_strip_family("fixed_point")
        == "second_factor_times_fixed_point_remainder"
    )
    assert (
        module.second_strip_family("semiprime_distinct")
        == "second_factor_times_semiprime_remainder"
    )
    assert module.third_strip_family(None) == "not_third_stripped"
    assert (
        module.third_strip_family("fixed_point")
        == "third_factor_times_fixed_point_remainder"
    )
    assert (
        module.third_strip_family("semiprime_distinct")
        == "third_factor_times_semiprime_remainder"
    )
    assert module.is_prime_power_tail("prime_square") is True
    assert module.is_prime_power_tail("prime_cube") is True
    assert module.is_prime_power_tail("prime_power") is True
    assert module.is_prime_power_tail("two_prime_power_family") is True
    assert module.is_prime_power_tail("fixed_point") is False


def test_decomposition_row_separates_fixed_point_from_obstruction():
    """Prime closures and composite obstructions should decompose differently."""
    module = load_module()
    width2 = module.WIDTH2_PROBE
    fixed_row = module.decomposition_row(width2.audit_record(width2.width2_record(11)))
    obstruction_row = module.decomposition_row(width2.audit_record(width2.width2_record(47)))

    assert fixed_row["candidate"] == 13
    assert fixed_row["endpoint_fixed_point"] is True
    assert fixed_row["endpoint_family"] == "fixed_point"
    assert fixed_row["factor_signature"] == "13"
    assert fixed_row["least_factor"] is None
    assert obstruction_row["candidate"] == 49
    assert obstruction_row["endpoint_fixed_point"] is False
    assert obstruction_row["endpoint_family"] == "prime_square"
    assert obstruction_row["factor_signature"] == "7^2"
    assert obstruction_row["least_factor"] == 7
    assert obstruction_row["least_factor_mod30"] == 7
    assert obstruction_row["cofactor"] == 7
    assert obstruction_row["cofactor_mod30"] == 7
    assert obstruction_row["cofactor_family"] == "fixed_point"
    assert obstruction_row["reduced_obstruction_family"] == "least_factor_times_fixed_point_cofactor"
    assert obstruction_row["low_complexity_cofactor_obstruction"] is True
    assert obstruction_row["higher_cofactor_obstruction"] is False
    assert obstruction_row["second_strip_family"] == "not_second_stripped"
    assert obstruction_row["third_strip_family"] == "not_third_stripped"
    assert obstruction_row["third_strip_prime_power_tail"] is False


def test_small_summary_matches_width2_contract():
    """The decomposition should preserve the width-2 endpoint fixed-point split."""
    module = load_module()
    rows = module.decomposition_rows(200)
    summary = module.summarize(rows)

    assert summary["eligible_anchor_count"] == len(rows)
    assert summary["endpoint_fixed_point_count"] == sum(1 for row in rows if row["endpoint_fixed_point"])
    assert summary["endpoint_obstruction_count"] == sum(1 for row in rows if not row["endpoint_fixed_point"])
    assert summary["status_mismatch_count"] == 0
    assert summary["low_complexity_cofactor_obstruction_count"] == sum(
        1
        for row in rows
        if row["low_complexity_cofactor_obstruction"]
    )
    assert summary["higher_cofactor_obstruction_count"] == sum(
        1
        for row in rows
        if row["higher_cofactor_obstruction"]
    )
    assert summary["audit_status"] == "PASS"
    assert summary["compact_obstruction_grammar"]
    assert summary["reduced_obstruction_family_distribution"]
    assert summary["least_factor_residue_distribution"]
    assert "second_strip_family_distribution" in summary
    assert "third_strip_family_distribution" in summary
    assert "third_strip_higher_remainder_count" in summary
    assert "third_strip_prime_power_tail_count" in summary

    for row in rows:
        if row["endpoint_fixed_point"]:
            continue
        assert int(row["candidate_mod30"]) == (
            int(row["least_factor_mod30"]) * int(row["cofactor_mod30"])
        ) % 30
        if not row["higher_cofactor_obstruction"]:
            continue
        assert int(row["cofactor_mod30"]) == (
            int(row["second_factor_mod30"]) * int(row["second_remainder_mod30"])
        ) % 30
        if row["second_strip_family"] != "second_factor_times_higher_remainder":
            continue
        assert int(row["second_remainder_mod30"]) == (
            int(row["third_factor_mod30"]) * int(row["third_remainder_mod30"])
        ) % 30


def test_entry_point_writes_lf_decomposition_artifacts(tmp_path):
    """The CLI should emit LF-terminated decomposition artifacts."""
    module = load_module()

    assert module.main(["--max-right-prime", "200", "--output-dir", str(tmp_path)]) == 0

    summary_path = tmp_path / "summary.json"
    rows_path = tmp_path / "endpoint_decomposition_rows.csv"
    grammar_path = tmp_path / "compact_obstruction_grammar_rows.csv"
    second_strip_path = tmp_path / "second_strip_grammar_rows.csv"
    third_strip_path = tmp_path / "third_strip_grammar_rows.csv"
    third_strip_higher_path = tmp_path / "third_strip_higher_rows.csv"
    assert summary_path.exists()
    assert rows_path.exists()
    assert grammar_path.exists()
    assert second_strip_path.exists()
    assert third_strip_path.exists()
    assert third_strip_higher_path.exists()
    assert b"\r\n" not in summary_path.read_bytes()
    assert b"\r\n" not in rows_path.read_bytes()
    assert b"\r\n" not in grammar_path.read_bytes()
    assert b"\r\n" not in second_strip_path.read_bytes()
    assert b"\r\n" not in third_strip_path.read_bytes()
    assert b"\r\n" not in third_strip_higher_path.read_bytes()

    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    rows = list(csv.DictReader(rows_path.open(encoding="utf-8", newline="")))
    grammar_rows = list(csv.DictReader(grammar_path.open(encoding="utf-8", newline="")))
    assert len(rows) == summary["eligible_anchor_count"]
    assert "reduced_obstruction_family" in rows[0]
    assert "low_complexity_cofactor_obstruction" in rows[0]
    assert "cofactor_mod30" in rows[0]
    assert "second_strip_family" in rows[0]
    assert "higher_cofactor_obstruction" in rows[0]
    assert "third_strip_family" in rows[0]
    assert "third_strip_prime_power_tail" in rows[0]
    assert grammar_rows
    assert summary["audit_status"] == "PASS"
