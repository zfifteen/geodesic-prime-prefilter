"""Tests for multi-lane remainder investigation orchestrator."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent


def test_run_investigation_tiny_surface(tmp_path: Path) -> None:
    """Investigation runner produces lane summaries on the tiny validation set."""
    out = tmp_path / "investigation"
    cmd = [
        sys.executable,
        str(HERE / "run_investigation.py"),
        "--skip-lane-execution",
        "--tiny-jsonl",
        str(HERE / "output/tiny_val/raw_records.jsonl"),
        "--interior-jsonl",
        str(HERE / "output/tiny_val/raw_records.jsonl"),
        "--output-dir",
        str(out),
    ]
    proc = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, check=False)
    assert proc.returncode == 0, proc.stderr

    interior = json.loads((out / "interior_placement_stats.json").read_text())
    assert interior["gaps_with_interiors"] == 108
    assert interior["records_analyzed"] == 490
    assert 0.0 <= interior["gwr_last_rate"] <= 1.0

    for name in (
        "endpoint_lane_summary.json",
        "mod30_ridge_lane_summary.json",
        "state_budget_lane_summary.json",
        "rsa_lane_summary.json",
        "modular_remainder_status.json",
        "placement_correlation_table.md",
    ):
        assert (out / name).exists()


def test_correlation_analysis_cli(tmp_path: Path) -> None:
    """Correlation CLI writes numeric descriptive tables."""
    out = tmp_path / "corr"
    cmd = [
        sys.executable,
        str(HERE / "correlation_analysis.py"),
        "--records",
        str(HERE / "output/tiny_val/raw_records.jsonl"),
        "--out",
        str(out),
    ]
    proc = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, check=False)
    assert proc.returncode == 0, proc.stderr
    stats = json.loads((out / "descriptive_stats.json").read_text())
    assert stats["records"] == 490
    assert "mi_num_zeros_vs_dist_bin" in stats
    assert (out / "descriptive_stats.md").read_text().count("|") >= 6