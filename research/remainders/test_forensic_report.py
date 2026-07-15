"""Tests for remainder forensic report and verifier."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REMAINDERS = ROOT / "research" / "remainders"
REPORT = REMAINDERS / "REMAINDER_FORENSIC_REPORT.md"
MANIFEST = REMAINDERS / "DETECTIVE_TEAM_MANIFEST.md"
VERIFY = REMAINDERS / "forensic_verify.py"

LANE_AGENTS = [
    "interior_rnm",
    "modular_remainder_status",
    "endpoint_mask",
    "mod30_ridge",
    "state_budget",
    "rsa_backward",
]


def test_forensic_report_exists():
    assert REPORT.is_file()


def test_detective_manifest_exists():
    assert MANIFEST.is_file()


def test_report_covers_all_lanes():
    text = REPORT.read_text(encoding="utf-8")
    for agent in LANE_AGENTS:
        assert agent in text, f"missing agent {agent}"


def test_report_has_required_sections():
    text = REPORT.read_text(encoding="utf-8")
    for section in (
        "## Synthesis",
        "## Downstream Research Index",
        "## Cross-Lane Epistemic Audit",
        "CORRELATION_REPORT.md",
    ):
        assert section in text, f"missing section {section}"


def test_forensic_verify_passes():
    proc = subprocess.run(
        [sys.executable, str(VERIFY)],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr