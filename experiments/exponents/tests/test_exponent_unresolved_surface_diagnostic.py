"""Tests for unresolved exponent surface diagnostics."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
SCRIPT_PATH = ROOT / "experiments" / "exponents" / "scripts" / "exponent_unresolved_surface_diagnostic.py"


def load_module(path: Path, name: str):
    """Load one probe module."""
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"unable to load {name}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_diagnostic_summarizes_offset_one_stop_rule():
    """Offset-one concentration should trigger the configured stop rule."""
    diagnostic = load_module(SCRIPT_PATH, "exponent_unresolved_surface_diagnostic")
    rows = [
        {"exponent": "101", "pressure_unresolved_candidate_offset": "1", "pressure_candidate_checks": "1"},
        {"exponent": "103", "pressure_unresolved_candidate_offset": "1", "pressure_candidate_checks": "1"},
        {"exponent": "107", "pressure_unresolved_candidate_offset": "7", "pressure_candidate_checks": "2"},
    ]

    summary = diagnostic.summarize(rows)

    assert summary["row_count"] == 3
    assert summary["offset_one_count"] == 2
    assert summary["offset_one_stop_rule_triggered"] is True


def test_diagnostic_outputs_are_lf_terminated(tmp_path):
    """Diagnostic outputs should reconcile and use LF line endings."""
    diagnostic = load_module(SCRIPT_PATH, "exponent_unresolved_surface_diagnostic")
    rows = [
        {"exponent": "101", "pressure_unresolved_candidate_offset": "1", "pressure_candidate_checks": "1"},
        {"exponent": "103", "pressure_unresolved_candidate_offset": "7", "pressure_candidate_checks": "2"},
    ]
    out = tmp_path / "out"

    diagnostic.write_outputs(out, rows)

    for path in [
        out / "unresolved_offset_summary_rows.csv",
        out / "unresolved_candidate_checks_rows.csv",
        out / "diagnostic_summary.json",
    ]:
        assert path.exists()
        assert b"\r\n" not in path.read_bytes()
    summary = json.loads((out / "diagnostic_summary.json").read_text(encoding="utf-8"))
    assert summary["row_count"] == 2
