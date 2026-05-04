"""Tests for endpoint fixed-point decomposition in width-2 chambers."""

from __future__ import annotations

import csv
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
MODULE_PATH = (
    ROOT
    / "experiments"
    / "twin-primes"
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
    assert obstruction_row["cofactor"] == 7
    assert obstruction_row["cofactor_family"] == "fixed_point"


def test_small_summary_matches_width2_contract():
    """The decomposition should preserve the width-2 endpoint fixed-point split."""
    module = load_module()
    rows = module.decomposition_rows(200)
    summary = module.summarize(rows)

    assert summary["eligible_anchor_count"] == len(rows)
    assert summary["endpoint_fixed_point_count"] == sum(1 for row in rows if row["endpoint_fixed_point"])
    assert summary["endpoint_obstruction_count"] == sum(1 for row in rows if not row["endpoint_fixed_point"])
    assert summary["status_mismatch_count"] == 0
    assert summary["audit_status"] == "PASS"
    assert summary["compact_obstruction_grammar"]


def test_entry_point_writes_lf_decomposition_artifacts(tmp_path):
    """The CLI should emit LF-terminated decomposition artifacts."""
    module = load_module()

    assert module.main(["--max-right-prime", "200", "--output-dir", str(tmp_path)]) == 0

    summary_path = tmp_path / "summary.json"
    rows_path = tmp_path / "endpoint_decomposition_rows.csv"
    grammar_path = tmp_path / "compact_obstruction_grammar_rows.csv"
    assert summary_path.exists()
    assert rows_path.exists()
    assert grammar_path.exists()
    assert b"\r\n" not in summary_path.read_bytes()
    assert b"\r\n" not in rows_path.read_bytes()
    assert b"\r\n" not in grammar_path.read_bytes()

    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    rows = list(csv.DictReader(rows_path.open(encoding="utf-8", newline="")))
    grammar_rows = list(csv.DictReader(grammar_path.open(encoding="utf-8", newline="")))
    assert len(rows) == summary["eligible_anchor_count"]
    assert grammar_rows
    assert summary["audit_status"] == "PASS"
