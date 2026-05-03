"""Tests for the short-block branch occupancy baseline probe."""

from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from collatz_pgs_branch_occupancy_baseline_probe import (  # noqa: E402
    candidate_record,
    divisor_rank,
    run_probe,
)
from collatz_pgs_same_gap_scale_probe import PrimeContext  # noqa: E402


def test_known_branch2_hit_is_leftmost_minimizer():
    """The known small branch-2 hit should have no lower or earlier equal competitor."""
    context = PrimeContext(20_000)
    cache: dict[int, int] = {}

    rank = divisor_rank(context, cache, 10886)

    assert rank["witness_tau"] == 4
    assert rank["lower_tau_competitor_count"] == 0
    assert rank["equal_tau_before_count"] == 0
    assert rank["leftmost_minimizer"]


def test_candidate_record_preserves_below_minimizer_hit():
    """The baseline record should match the known below-minimizer branch-2 hit."""
    context = PrimeContext(20_000)
    cache: dict[int, int] = {}

    record = candidate_record(context, cache, 10886, 9675, 4, 2)

    assert record["below_minimizer_hit"]
    assert record["branch"] == 2
    assert record["final_v2"] == 4
    assert record["terminal_source"] == 10885
    assert record["leftmost_minimizer"]


def test_run_probe_writes_compact_baseline_tables(tmp_path):
    """A small deterministic run should write compact grouped outputs."""
    summary = run_probe(10_000, tmp_path)

    assert summary["candidate_count"] > 0
    assert summary["below_minimizer_hit_count_by_branch"]["1"] == 0
    assert summary["below_minimizer_hit_count_by_branch"]["2"] == 2
    assert (tmp_path / "summary.json").exists()
    assert (tmp_path / "branch_rows.jsonl").exists()
    assert (tmp_path / "tau_rows.jsonl").exists()
    assert (tmp_path / "gap_width_rows.jsonl").exists()
    assert (tmp_path / "lower_competitor_rows.jsonl").exists()
    assert (tmp_path / "terminal_source_rows.jsonl").exists()
    assert (tmp_path / "leftmost_terminal_rows.jsonl").exists()
