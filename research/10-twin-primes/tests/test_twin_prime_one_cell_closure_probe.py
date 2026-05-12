"""Tests for the PGS-native twin-prime one-cell closure probe."""

from __future__ import annotations

import csv
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
MODULE_PATH = ROOT / "research" / "10-twin-primes" / "scripts" / "twin_prime_one_cell_closure_probe.py"


def load_module():
    """Load the one-cell closure probe from its file path."""
    spec = importlib.util.spec_from_file_location("twin_prime_one_cell_closure_probe", MODULE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("unable to load twin_prime_one_cell_closure_probe module")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_eligible_residues_are_exact_twin_candidate_residues():
    """Only residues with q+2 wheel-open should be eligible."""
    module = load_module()

    assert module.ELIGIBLE_RESIDUES == (11, 17, 29)


def test_prime_closure_row_records_forced_one_cell_selected_integer():
    """For q=11, q+2=13 closes and w=q+1 is forced."""
    module = load_module()
    row = module.closure_row(module.GAP_TYPE_PROBE.gap_type_row(11))

    assert row["q"] == 11
    assert row["w"] == 12
    assert row["forced_selected_integer"] == 12
    assert row["candidate_endpoint"] == 13
    assert row["tau_endpoint"] == 2
    assert row["endpoint_class"] == "prime_closure"
    assert row["first_later_le_tau_w"] is None


def test_composite_obstruction_row_compares_endpoint_tau_to_forced_load():
    """For q=47, q+2=49 is a composite endpoint obstruction."""
    module = load_module()
    row = module.closure_row(module.GAP_TYPE_PROBE.gap_type_row(47))

    assert row["q"] == 47
    assert row["w"] == 48
    assert row["candidate_endpoint"] == 49
    assert row["tau_endpoint"] > 2
    assert row["endpoint_class"] == "composite_obstruction"
    assert row["obstruction_relation"] == module.obstruction_relation(row["tau_endpoint"], row["tau_w"])
    assert row["first_later_le_tau_w"] is not None
    assert row["first_later_le_tau_w_offset"] > 2


def test_closure_rows_only_include_eligible_residues():
    """The measured surface should contain only one-cell candidate residues."""
    module = load_module()
    rows = module.closure_rows(200)

    assert rows
    assert {int(row["q_mod30"]) for row in rows} <= set(module.ELIGIBLE_RESIDUES)
    assert all(int(row["w"]) == int(row["q"]) + 1 for row in rows)


def test_entry_point_writes_lf_csv_and_reconciled_summary(tmp_path):
    """The CLI should emit LF-terminated rows that reconcile with summary counts."""
    module = load_module()

    assert module.main(["--max-right-prime", "200", "--output-dir", str(tmp_path)]) == 0

    summary_path = tmp_path / "summary.json"
    closure_path = tmp_path / "closure_rows.csv"
    obstruction_path = tmp_path / "obstruction_family_rows.csv"
    assert summary_path.exists()
    assert closure_path.exists()
    assert obstruction_path.exists()
    assert b"\r\n" not in closure_path.read_bytes()
    assert b"\r\n" not in obstruction_path.read_bytes()

    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    rows = list(csv.DictReader(closure_path.open(encoding="utf-8", newline="")))
    assert len(rows) == summary["eligible_anchor_count"]
    assert sum(1 for row in rows if row["endpoint_class"] == "prime_closure") == summary["prime_closure_count"]
    assert (
        sum(1 for row in rows if row["endpoint_class"] == "composite_obstruction")
        == summary["composite_obstruction_count"]
    )
