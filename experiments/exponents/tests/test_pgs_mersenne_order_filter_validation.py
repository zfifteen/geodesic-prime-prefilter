"""Tests for Mersenne order-filter validation."""

from __future__ import annotations

import csv
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
VALIDATION_PATH = (
    ROOT
    / "experiments"
    / "exponents"
    / "validation"
    / "pgs_mersenne_order_filter_validation.py"
)


def load_module():
    """Load the validation module."""
    spec = importlib.util.spec_from_file_location(
        "pgs_mersenne_order_filter_validation",
        VALIDATION_PATH,
    )
    if spec is None or spec.loader is None:
        raise RuntimeError("unable to load validation module")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_composite_mersenne_exponent_exposes_order_filtered_factor():
    """A composite Mersenne row should expose the order-filter obstruction."""
    module = load_module()
    row = module.validation_row(11)

    assert row["mersenne_number_is_prime"] is False
    assert row["least_factor"] == 23
    assert row["least_factor_mod_2e"] == 1
    assert row["least_factor_mod_8"] == 7
    assert row["order_filter_pass"] is True
    assert row["order_filter_candidate_rank"] == 1


def test_mersenne_prime_exponent_has_no_obstruction_row():
    """A Mersenne-prime exponent should have no least-factor obstruction."""
    module = load_module()
    row = module.validation_row(31)

    assert row["mersenne_number_is_prime"] is True
    assert row["least_factor"] == ""
    assert row["order_filter_pass"] is True


def test_default_surface_survives_order_filter_check():
    """The toy surface should pass the order-filter validation."""
    module = load_module()
    rows = module.collect_rows(127)
    summary = module.summarize(rows, 127)

    assert summary["prime_exponent_count"] == 31
    assert summary["mersenne_prime_count"] == 12
    assert summary["mersenne_composite_count"] == 19
    assert summary["composite_order_filter_failure_count"] == 0
    assert summary["result"] == "SURVIVES"


def test_fixed_point_pressure_hits_zero_at_factor():
    """A true factor should have zero fixed-point residue pressure."""
    module = load_module()

    assert module.fixed_point_pressure(11, 23) == 0


def test_residue_return_events_compress_raw_candidate_rank():
    """Record-low residue events should compress the raw order-filter scan."""
    module = load_module()
    row = module.validation_row(59)
    compression = module.residue_return_compression_row(row)

    assert row["least_factor"] == 179951
    assert row["order_filter_candidate_rank"] == 763
    assert compression["scan_status"] == "scanned"
    assert compression["raw_candidate_rank"] == 763
    assert compression["record_low_event_count"] == 3
    assert compression["zero_pressure_rank"] == 763
    assert compression["zero_pressure_event_index"] == 3


def test_large_raw_rank_is_explicitly_skipped_by_residue_scan_limit():
    """A huge raw rank should be skipped instead of silently widening the scan."""
    module = load_module()
    row = module.validation_row(101)
    compression = module.residue_return_compression_row(row, max_rank=10000)

    assert row["order_filter_candidate_rank"] > 10000
    assert compression["scan_status"] == "skipped_rank_above_limit"
    assert compression["record_low_event_count"] == ""


def test_cli_writes_lf_outputs(tmp_path):
    """The validation CLI should write LF-terminated artifacts."""
    module = load_module()
    output_dir = tmp_path / "out"

    assert module.main(["--max-exponent", "127", "--output-dir", str(output_dir)]) == 0

    rows_path = output_dir / "order_filter_rows.csv"
    composite_path = output_dir / "composite_obstruction_rows.csv"
    event_path = output_dir / "residue_return_event_rows.csv"
    compression_path = output_dir / "residue_return_compression_rows.csv"
    summary_path = output_dir / "summary.json"
    for path in [rows_path, composite_path, event_path, compression_path, summary_path]:
        assert path.exists()
        assert b"\r\n" not in path.read_bytes()

    rows = list(csv.DictReader(rows_path.open(encoding="utf-8", newline="")))
    compression_rows = list(
        csv.DictReader(compression_path.open(encoding="utf-8", newline=""))
    )
    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    assert len(rows) == summary["prime_exponent_count"]
    assert len(compression_rows) == summary["mersenne_composite_count"]
    assert summary["result"] == "SURVIVES"
    assert summary["residue_return_scanned_composite_count"] == 15
    assert summary["residue_return_zero_pressure_found_count"] == 15
