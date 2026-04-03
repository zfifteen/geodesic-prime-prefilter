"""Tests for the GWR proof-pursuit earlier-spoiler scan script."""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
SCRIPT_PATH = ROOT / "gwr" / "experiments" / "proof" / "earlier_spoiler_scan.py"


def load_module():
    """Load the proof-pursuit script directly from its file path."""
    spec = importlib.util.spec_from_file_location("earlier_spoiler_scan", SCRIPT_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("Unable to load earlier_spoiler_scan")
    module = importlib.util.module_from_spec(spec)
    sys.modules["earlier_spoiler_scan"] = module
    spec.loader.exec_module(module)
    return module


def test_exact_score_comparison_uses_integer_power_identity():
    """The exact score comparison should agree with the known 6-versus-49 ordering."""
    module = load_module()

    assert module.score_strictly_greater(6, 4, 49, 3)
    assert not module.score_strictly_greater(49, 3, 6, 4)


def test_earlier_spoiler_scan_emits_json_and_finds_no_small_counterexample(tmp_path, capsys):
    """The scan should emit a JSON artifact on a small exact interval."""
    module = load_module()
    output_path = tmp_path / "proof" / "scan.json"

    assert (
        module.main(
            [
                "--lo",
                "2",
                "--hi",
                "10001",
                "--output",
                str(output_path),
            ]
        )
        == 0
    )

    payload = json.loads(output_path.read_text(encoding="utf-8"))
    assert payload["gap_count"] > 0
    assert payload["counterexample_gap_count"] == 0
    assert payload["exact_spoiler_count"] == 0

    stdout_payload = json.loads(capsys.readouterr().out)
    assert stdout_payload["interval"] == {"lo": 2, "hi": 10001}
