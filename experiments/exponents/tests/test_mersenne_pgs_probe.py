"""Tests for the Mersenne PGS endpoint probe."""

from __future__ import annotations

import csv
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
MODULE_PATH = ROOT / "experiments" / "exponents" / "scripts" / "mersenne_pgs_probe.py"


def load_module():
    """Load the Mersenne PGS probe."""
    spec = importlib.util.spec_from_file_location("mersenne_pgs_probe", MODULE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("unable to load Mersenne PGS probe")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_mersenne_exponents_respect_scale_limit():
    """The scale limit should keep only endpoints inside the measured surface."""
    module = load_module()

    assert module.mersenne_exponents_through(100) == [2, 3, 5]
    assert module.mersenne_exponents_through(10**18) == [2, 3, 5, 7, 13, 17, 19, 31]


def test_nontrivial_mersenne_chamber_selects_second_cell():
    """The first nontrivial Mersenne chamber should select q+2, not 2^p."""
    module = load_module()
    row = module.chamber_row(5)

    assert row["mersenne_prime"] == 31
    assert row["right_power"] == 32
    assert row["right_power_tau"] == 6
    assert row["second_cell"] == 33
    assert row["second_cell_signature"] == "3*11"
    assert row["second_cell_divisible_by_3"] is True
    assert row["second_cell_3adic_valuation"] == 1
    assert row["second_cell_after_one_3"] == 11
    assert row["second_cell_after_one_3_signature"] == "11"
    assert row["second_cell_after_one_3_tau"] == 2
    assert row["second_cell_after_one_3_prime"] is True
    assert row["second_cell_after_removing_3s"] == 11
    assert row["second_cell_after_removing_3s_signature"] == "11"
    assert row["second_cell_after_removing_3s_tau"] == 2
    assert row["second_cell_after_removing_3s_prime"] is True
    assert row["leftmost_minimizer"] == 33
    assert row["leftmost_minimizer_offset"] == 2
    assert row["leftmost_minimizer_tau"] == 4
    assert row["right_power_selected"] is False
    assert row["second_cell_selected"] is True


def test_summary_records_power_neighbor_and_second_cell_relation():
    """The summary should expose the measured nontrivial Mersenne relation."""
    module = load_module()
    rows = module.collect_rows(10**18)
    summary = module.summarize(rows, 10**18)

    assert summary["mersenne_prime_count"] == 8
    assert summary["nontrivial_mersenne_prime_count"] == 7
    assert summary["max_mersenne_exponent"] == 31
    assert summary["nontrivial_right_power_selected_count"] == 0
    assert summary["nontrivial_second_cell_selected_count"] == 7
    assert summary["nontrivial_second_cell_selected_rate"] == 1.0
    assert summary["nontrivial_second_cell_divisible_by_3_count"] == 7
    assert summary["nontrivial_second_cell_after_one_3_prime_count"] == 7
    assert summary["nontrivial_second_cell_after_removing_3s_prime_count"] == 6
    assert summary["nontrivial_second_cell_3adic_distribution"] == [
        {"second_cell_3adic_valuation": 1, "count": 6},
        {"second_cell_3adic_valuation": 2, "count": 1},
    ]
    assert summary["nontrivial_second_cell_after_removing_3s_tau_distribution"] == [
        {"second_cell_after_removing_3s_tau": 2, "count": 6},
        {"second_cell_after_removing_3s_tau": 1, "count": 1},
    ]
    assert summary["nontrivial_second_cell_after_one_3_tau_distribution"] == [
        {"second_cell_after_one_3_tau": 2, "count": 7}
    ]
    assert summary["nontrivial_minimizer_offset_distribution"] == [
        {"leftmost_minimizer_offset": 2, "count": 7}
    ]


def test_cli_outputs_lf_and_reconcile(tmp_path):
    """The CLI should emit LF-terminated CSV and matching JSON counts."""
    module = load_module()
    out = tmp_path / "out"

    assert module.main(["--scale-limit", str(10**18), "--output-dir", str(out)]) == 0

    summary_path = out / "summary.json"
    rows_path = out / "mersenne_chamber_rows.csv"
    assert summary_path.exists()
    assert rows_path.exists()
    assert b"\r\n" not in summary_path.read_bytes()
    assert b"\r\n" not in rows_path.read_bytes()

    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    rows = list(csv.DictReader(rows_path.open(encoding="utf-8", newline="")))
    assert summary["mersenne_prime_count"] == len(rows)
    assert rows[-1]["exponent"] == "31"
