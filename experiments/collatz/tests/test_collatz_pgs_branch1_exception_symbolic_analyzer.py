"""Tests for the branch-1 exception symbolic analyzer."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from collatz_pgs_branch1_exception_symbolic_analyzer import (  # noqa: E402
    analyze,
    run_analyzer,
    validate_exception_row,
)


EXCEPTION_ROWS = (
    ROOT
    / "output"
    / "collatz_pgs_branch_occupancy_baseline_probe"
    / "branch1_composite_exception_rows.jsonl"
)


def read_committed_rows() -> list[dict[str, object]]:
    """Read committed branch-1 exception rows."""
    with EXCEPTION_ROWS.open("r", encoding="utf-8", newline="") as handle:
        return [json.loads(line) for line in handle]


def test_committed_exception_rows_have_symbolic_normal_form():
    """All committed exception rows should satisfy the branch-1 normal form."""
    summary = analyze(read_committed_rows())

    assert summary["row_count"] == 41
    assert summary["normal_form"] == "w = 18u, u prime"
    assert summary["all_witness_tau"] == 12
    assert summary["counts_by_final_v2"] == [
        {"final_v2": 4, "count": 36},
        {"final_v2": 8, "count": 5},
    ]
    assert summary["counts_by_gap_width"] == [
        {"gap_width": 6, "count": 37},
        {"gap_width": 8, "count": 3},
        {"gap_width": 10, "count": 1},
    ]
    assert summary["counts_by_witness_tau"] == [{"witness_tau": 12, "count": 41}]
    assert summary["factor_form_rows"] == [
        {
            "factor_form": "w = 2 * 3^2 * u, u prime",
            "equivalent_form": "w = 18u, u prime",
            "count": 41,
        },
    ]


def test_offset_counts_match_committed_exception_rows():
    """Offset counts should reconcile with the exception row table."""
    summary = analyze(read_committed_rows())

    assert summary["counts_by_witness_gap_offset"] == [
        {"witness_gap_offset": 5, "count": 38},
        {"witness_gap_offset": 7, "count": 3},
    ]
    assert summary["counts_by_terminal_source_gap_offset"] == [
        {"terminal_source_gap_offset": 4, "count": 38},
        {"terminal_source_gap_offset": 6, "count": 3},
    ]


def test_non_branch1_row_fails_contract():
    """Rows explicitly labeled as another branch should fail."""
    row = dict(read_committed_rows()[0])
    row["branch"] = 2

    with pytest.raises(ValueError, match="non-branch-1"):
        validate_exception_row(row)


def test_non_composite_hit_row_fails_contract():
    """Rows outside composite below-minimizer geometry should fail."""
    row = dict(read_committed_rows()[0])
    row["terminal_geometry"] = "terminal_prime_non_twin"

    with pytest.raises(ValueError, match="unexpected terminal geometry"):
        validate_exception_row(row)


def test_run_analyzer_writes_summary(tmp_path):
    """The command helper should write the compact grouped summary."""
    output = tmp_path / "summary.json"
    summary = run_analyzer(EXCEPTION_ROWS, output)

    assert output.exists()
    assert json.loads(output.read_text(encoding="utf-8")) == summary
