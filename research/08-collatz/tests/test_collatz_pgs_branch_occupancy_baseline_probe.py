"""Tests for the short-block branch occupancy baseline probe."""

from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from collatz_pgs_branch_occupancy_baseline_probe import (  # noqa: E402
    GEOMETRY_AUTOMATIC_TWIN,
    GEOMETRY_COMPOSITE_BELOW,
    branch1_composite_exception_rows,
    candidate_record,
    divisor_rank,
    run_probe,
    terminal_geometry_label,
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
    assert record["terminal_source_gap_offset"] == 2
    assert record["witness_gap_offset"] == 3
    assert record["terminal_geometry"] == GEOMETRY_COMPOSITE_BELOW
    assert record["leftmost_minimizer"]


def test_twin_gap_prime_terminal_geometry_is_automatic():
    """A twin-prime gap leftmost success is automatic but terminal-prime."""
    assert (
        terminal_geometry_label(
            leftmost_minimizer=True,
            terminal_source_is_prime=True,
            gap_width=2,
            below_minimizer_hit=False,
        )
        == GEOMETRY_AUTOMATIC_TWIN
    )


def test_known_branch1_exception_is_composite_below_minimizer():
    """The first branch-1 exception should be emitted as a composite hit."""
    context = PrimeContext(14_000_000)
    cache: dict[int, int] = {}

    record = candidate_record(context, cache, 13_501_062, 6_000_471, 4, 1)
    rows = branch1_composite_exception_rows([record])

    assert record["terminal_geometry"] == GEOMETRY_COMPOSITE_BELOW
    assert record["below_minimizer_hit"]
    assert record["leftmost_minimizer"]
    assert not record["terminal_source_is_prime"]
    assert len(rows) == 1
    assert rows[0]["witness"] == 13_501_062
    assert rows[0]["gap_width"] == 6


def test_run_probe_writes_compact_baseline_tables(tmp_path):
    """A small deterministic run should write compact grouped outputs."""
    summary = run_probe(10_000, tmp_path)

    assert summary["candidate_count"] > 0
    assert summary["below_minimizer_hit_count_by_branch"]["1"] == 0
    assert summary["below_minimizer_hit_count_by_branch"]["2"] == 2
    assert summary["branch1_composite_exception_count"] == 0
    assert summary["leftmost_success_count"] == 23
    assert (tmp_path / "summary.json").exists()
    assert (tmp_path / "branch_rows.jsonl").exists()
    assert (tmp_path / "tau_rows.jsonl").exists()
    assert (tmp_path / "gap_width_rows.jsonl").exists()
    assert (tmp_path / "lower_competitor_rows.jsonl").exists()
    assert (tmp_path / "terminal_source_rows.jsonl").exists()
    assert (tmp_path / "leftmost_terminal_rows.jsonl").exists()
    assert (tmp_path / "terminal_geometry_rows.jsonl").exists()
    assert (tmp_path / "leftmost_gap_width_rows.jsonl").exists()
    assert (tmp_path / "leftmost_geometry_rows.jsonl").exists()
    assert (tmp_path / "branch1_composite_exception_rows.jsonl").exists()
