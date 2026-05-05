"""Tests for the Mersenne boundary-contract probe."""

from __future__ import annotations

import csv
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
MODULE_PATH = ROOT / "experiments" / "exponents" / "scripts" / "mersenne_boundary_contract_probe.py"


def load_module():
    """Load the Mersenne boundary-contract probe."""
    spec = importlib.util.spec_from_file_location("mersenne_boundary_contract_probe", MODULE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("unable to load Mersenne boundary-contract probe")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_working_exponent_survives_boundary_contract():
    """A working exponent should make 2^p - 1 the recovered left boundary."""
    module = load_module()
    row = module.boundary_row(31)

    assert row["candidate_tau"] == 2
    assert row["recovered_left_boundary"] == row["candidate"]
    assert row["boundary_survives"] is True
    assert row["boundary_distance_from_power"] == 1
    assert row["exponent_wall_tau"] == 32
    assert row["leftmost_minimizer_offset_from_candidate"] == 2


def test_nonworking_exponent_has_boundary_leakage():
    """A nonworking exponent should expose leakage before the exponent wall."""
    module = load_module()
    row = module.boundary_row(11)

    assert row["candidate_tau"] > 2
    assert row["candidate_factor_signature"] == "23*89"
    assert row["boundary_survives"] is False
    assert row["boundary_distance_from_power"] == 9
    assert row["recovered_left_boundary"] < row["candidate"]
    assert row["leftmost_minimizer_offset_from_candidate"] < 0


def test_summary_separates_boundary_survival_from_offset2_selection():
    """Boundary survival is exact through 127, while offset-2 selection is not."""
    module = load_module()
    rows = module.collect_rows(127)
    summary = module.summarize(rows, 127)

    assert summary["prime_exponent_count"] == 31
    assert summary["boundary_survival_count"] == 12
    assert summary["boundary_leak_count"] == 19
    assert summary["audit_candidate_prime_count"] == 12
    assert summary["audit_candidate_composite_count"] == 19
    assert summary["audit_false_positive_count"] == 0
    assert summary["audit_false_negative_count"] == 0
    assert summary["survivor_second_cell_selected_count"] == 9
    assert summary["audit_prime_after_one_3_prime_count"] == 10
    assert summary["audit_composite_after_one_3_prime_count"] == 5


def test_cli_outputs_lf_and_reconcile(tmp_path):
    """The CLI should emit LF-terminated CSV and matching JSON."""
    module = load_module()
    out = tmp_path / "out"

    assert module.main(["--max-exponent", "31", "--output-dir", str(out)]) == 0
    summary_path = out / "summary.json"
    rows_path = out / "boundary_contract_rows.csv"
    failure_path = out / "boundary_failure_rows.csv"
    for path in [summary_path, rows_path, failure_path]:
        assert path.exists()
        assert b"\r\n" not in path.read_bytes()

    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    rows = list(csv.DictReader(rows_path.open(encoding="utf-8", newline="")))
    failures = list(csv.DictReader(failure_path.open(encoding="utf-8", newline="")))
    assert summary["prime_exponent_count"] == len(rows)
    assert summary["boundary_leak_count"] == len(failures)
