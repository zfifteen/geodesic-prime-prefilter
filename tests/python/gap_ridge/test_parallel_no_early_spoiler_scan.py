"""Tests for the deterministic segmented no-early-spoiler scanner."""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
PARALLEL_SCRIPT_PATH = ROOT / "gwr" / "experiments" / "proof" / "parallel_no_early_spoiler_scan.py"
MARGIN_SCRIPT_PATH = ROOT / "gwr" / "experiments" / "proof" / "no_early_spoiler_margin_scan.py"
BRIDGE_SCRIPT_PATH = ROOT / "gwr" / "experiments" / "proof" / "asymptotic_bridge_load_scan.py"


def load_module(module_name: str, script_path: Path):
    """Load one proof helper directly from its file path."""
    spec = importlib.util.spec_from_file_location(module_name, script_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load {script_path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def test_parallel_scan_matches_exact_small_interval(tmp_path, capsys):
    """The segmented scan should match the exact single-interval helpers."""
    parallel_module = load_module("parallel_no_early_spoiler_scan", PARALLEL_SCRIPT_PATH)
    margin_module = load_module("no_early_spoiler_margin_scan_test_runtime", MARGIN_SCRIPT_PATH)
    bridge_module = load_module("asymptotic_bridge_load_scan_test_runtime", BRIDGE_SCRIPT_PATH)

    segment_output_dir = tmp_path / "segments"
    aggregate_output = tmp_path / "aggregate.json"

    assert (
        parallel_module.main(
            [
                "--lo",
                "2",
                "--hi",
                "10001",
                "--segment-size",
                "1000",
                "--jobs",
                "1",
                "--segment-output-dir",
                str(segment_output_dir),
                "--aggregate-output",
                str(aggregate_output),
            ]
        )
        == 0
    )

    payload = json.loads(aggregate_output.read_text(encoding="utf-8"))
    _, comparison_hi = parallel_module.padded_interval(2, 10001)
    exact_margin = margin_module.analyze_interval(2, comparison_hi)
    exact_bridge = bridge_module.analyze_interval(2, comparison_hi)

    assert payload["interval"] == {"lo": 2, "hi": 10001}
    assert payload["segment_count"] == 10
    assert len(list(segment_output_dir.glob("segment_*.json"))) == 10

    assert payload["gap_count"] == exact_margin["gap_count"] == exact_bridge["gap_count"]
    assert (
        payload["earlier_candidate_count"]
        == exact_margin["earlier_candidate_count"]
        == exact_bridge["earlier_candidate_count"]
    )
    assert payload["exact_spoiler_count"] == exact_margin["exact_spoiler_count"]
    assert payload["bridge_failure_count"] == exact_bridge["bridge_failure_count"]
    assert payload["min_log_margin_case"]["log_score_margin"] == exact_margin["min_log_score_margin"]
    assert payload["min_ratio_margin_case"]["critical_ratio_margin"] == exact_margin["min_critical_ratio_margin"]
    assert payload["max_bridge_load"] == exact_bridge["max_bridge_load"]
    assert payload["top_bridge_load_cases"]

    stdout_payload = json.loads(capsys.readouterr().out)
    assert stdout_payload["interval"] == {"lo": 2, "hi": 10001}
