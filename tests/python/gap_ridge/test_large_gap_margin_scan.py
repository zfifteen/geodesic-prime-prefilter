"""Tests for the exact large-gap no-early-spoiler margin scan."""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
SCRIPT_PATH = ROOT / "gwr" / "experiments" / "proof" / "large_gap_margin_scan.py"


def load_module():
    """Load the proof-pursuit script directly from its file path."""
    spec = importlib.util.spec_from_file_location(
        "large_gap_margin_scan",
        SCRIPT_PATH,
    )
    if spec is None or spec.loader is None:
        raise RuntimeError("Unable to load large_gap_margin_scan")
    module = importlib.util.module_from_spec(spec)
    sys.modules["large_gap_margin_scan"] = module
    spec.loader.exec_module(module)
    return module


def test_large_gap_margin_scan_emits_gap_surfaces(tmp_path, capsys):
    """The scan should emit largest-gap and gap-size surfaces on a small interval."""
    module = load_module()
    output_path = tmp_path / "proof" / "large_gap_margin_scan.json"

    assert (
        module.main(
            [
                "--lo",
                "2",
                "--hi",
                "10001",
                "--top-gap-limit",
                "5",
                "--output",
                str(output_path),
            ]
        )
        == 0
    )

    payload = json.loads(output_path.read_text(encoding="utf-8"))
    assert payload["interval"] == {"lo": 2, "hi": 10001}
    assert payload["top_gap_limit"] == 5
    assert payload["gap_count"] > 0
    assert payload["gap_with_earlier_candidates_count"] > 0
    assert payload["largest_gap_cases"]
    assert payload["gap_size_frontier"]
    assert min(row["critical_ratio_margin"] for row in payload["largest_gap_cases"]) > 0.0
    assert min(row["critical_ratio_margin"] for row in payload["gap_size_frontier"]) > 0.0

    stdout_payload = json.loads(capsys.readouterr().out)
    assert stdout_payload["interval"] == {"lo": 2, "hi": 10001}
