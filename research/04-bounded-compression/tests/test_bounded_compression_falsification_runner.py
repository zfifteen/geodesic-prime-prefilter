"""Tests for the bounded-compression falsification runner."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
MODULE_PATH = (
    ROOT
    / "research"
    / "04-bounded-compression"
    / "scripts"
    / "bounded_compression_falsification_runner.py"
)


def load_module():
    """Load the runner from its file path."""
    spec = importlib.util.spec_from_file_location(
        "bounded_compression_falsification_runner",
        MODULE_PATH,
    )
    if spec is None or spec.loader is None:
        raise RuntimeError("unable to load bounded_compression_falsification_runner")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_small_surface_has_no_failure():
    """The exact witness stays inside the dynamic cutoff on a small surface."""
    module = load_module()
    frontier_rows, summary, first_failure = module.run_scan(11, 10_000)

    assert first_failure is None
    assert summary["first_failure"] is None
    assert summary["tested_gap_count"] > 0
    assert summary["first_tested_q"] == 11
    assert summary["last_tested_q"] is not None
    assert summary["max_witness_offset"] > 0
    assert summary["max_cutoff_utilization"] <= 1.0
    assert summary["extremal_q"] == summary["extremal_row"]["q"]
    assert frontier_rows


def test_square_obstruction_metadata_is_explicit():
    """The committed fixed-cutoff counterexample gap exposes its square metadata."""
    module = load_module()
    row = module.row_for_right_prime(24_098_209)

    assert row["next_prime"] == 24_098_287
    assert row["first_interior_prime_square"] == 24_098_281
    assert row["first_interior_prime_square_root"] == 4_909
    assert row["first_interior_prime_square_offset"] == 72
    assert row["selected_witness_is_prime_square"] is True
    assert row["witness_offset"] == 72
    assert row["square_offset_minus_witness_offset"] == 0


def test_cli_writes_summary_and_frontier(tmp_path):
    """The runner writes the finite-surface summary and extremal frontier."""
    module = load_module()

    assert (
        module.main(
            [
                "--min-right-prime",
                "11",
                "--max-right-prime",
                "10000",
                "--output-dir",
                str(tmp_path),
            ]
        )
        == 0
    )

    summary_path = tmp_path / "bounded_compression_falsification_summary.json"
    frontier_path = tmp_path / "bounded_compression_falsification_frontier.csv"
    failure_path = tmp_path / "bounded_compression_first_failure.json"

    assert summary_path.exists()
    assert frontier_path.exists()
    assert not failure_path.exists()

    payload = json.loads(summary_path.read_text(encoding="utf-8"))
    assert payload["first_failure"] is None
    assert payload["tested_gap_count"] > 0
    assert payload["max_witness_offset"] > 0
    assert payload["max_cutoff_utilization"] <= 1.0


def test_scan_stops_at_first_failure(monkeypatch):
    """The scan stops when the exact witness exceeds the cutoff."""
    module = load_module()
    original = module.row_for_right_prime

    def forced_failure(q: int):
        row = original(q)
        if q == 11:
            row["witness_offset"] = int(row["cutoff"]) + 1
            row["cutoff_utilization"] = row["witness_offset"] / int(row["cutoff"])
        return row

    monkeypatch.setattr(module, "row_for_right_prime", forced_failure)

    frontier_rows, summary, first_failure = module.run_scan(11, 1_000)

    assert frontier_rows
    assert summary["tested_gap_count"] == 1
    assert first_failure is not None
    assert summary["first_failure"]["q"] == 11
    assert summary["max_witness_offset"] == summary["first_failure"]["witness_offset"]
