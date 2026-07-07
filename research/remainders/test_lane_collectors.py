"""Tests for lane collector probes (endpoint mask, mod30 ridge)."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent


def test_endpoint_probe_emits_mask_resolution(tmp_path: Path) -> None:
    out = tmp_path / "endpoint.json"
    cmd = [
        sys.executable,
        str(HERE / "lane_collectors/endpoint_residue_probe.py"),
        "--start-p",
        "1009",
        "--max-gaps",
        "200",
        "--output",
        str(out),
    ]
    proc = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, check=False)
    assert proc.returncode == 0, proc.stderr
    data = json.loads(out.read_text())
    assert "resolved_in_mask_fraction" in data
    assert 0.0 <= data["resolved_in_mask_fraction"] <= 1.0
    assert data["gaps_measured"] == 200


def test_mod30_ridge_probe_runs(tmp_path: Path) -> None:
    out = tmp_path / "ridge.json"
    cmd = [
        sys.executable,
        str(HERE / "lane_collectors/mod30_ridge_probe.py"),
        "--max-p",
        "5000",
        "--output",
        str(out),
    ]
    proc = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, check=False)
    assert proc.returncode == 0, proc.stderr
    data = json.loads(out.read_text())
    assert data["global_gaps"] > 0
    assert len(data["by_residue"]) == 8


def test_super_team_manifest_has_six_agents() -> None:
    from super_team import all_lane_agents, manifest_dict

    assert len(all_lane_agents()) == 6
    assert manifest_dict()["agent_count"] == 6