"""Tests for the gap divisor count probe."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
MODULE_PATH = ROOT / "benchmarks" / "python" / "predictor" / "gap_divisor_count_probe.py"


def load_module():
    """Load the gap divisor count probe script from its file path."""
    spec = importlib.util.spec_from_file_location("gap_divisor_count_probe", MODULE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("unable to load gap_divisor_count_probe module")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_gap_divisor_count_examples():
    """The metric sums divisor counts across the gap interior."""
    module = load_module()

    assert module.gap_divisor_count(11, 13) == 6
    assert module.gap_divisor_count(13, 17) == 13
    assert module.gap_divisor_count(23, 29) == 25


def test_row_from_pair_records_gap_metric():
    """One p,q pair should produce the requested metric fields."""
    module = load_module()

    row = module.row_from_pair("low_full", None, 23, 29)

    assert row == {
        "surface": "low_full",
        "scale_exponent": None,
        "p": 23,
        "q": 29,
        "gap": 6,
        "interior_composite_count": 5,
        "gap_divisor_count": 25,
    }


def test_anchor_construction_is_deterministic():
    """Low and high-scale anchor surfaces should be deterministic."""
    module = load_module()

    assert module.low_surface_anchors(30)[:5] == [11, 13, 17, 19, 23]
    first = module.sampled_anchors_near(10**8, 5)
    second = module.sampled_anchors_near(10**8, 5)

    assert first == second
    assert len(first) == 5
    assert all(first[index] > first[index + 1] for index in range(len(first) - 1))


def test_artifacts_are_lf_terminated_and_summary_counts_rows(tmp_path):
    """The CLI should write numeric artifacts with LF line endings."""
    module = load_module()

    assert (
        module.main(
            [
                "--output-dir",
                str(tmp_path),
                "--low-limit",
                "30",
                "--min-exponent",
                "2",
                "--max-exponent",
                "3",
                "--high-sample-size",
                "3",
            ]
        )
        == 0
    )

    artifact_names = [
        "rows.jsonl",
        "gap_frequency.csv",
        "divisor_count_frequency.csv",
        "scale_summary.csv",
        "summary.json",
    ]
    for name in artifact_names:
        payload = (tmp_path / name).read_bytes()
        assert b"\r\n" not in payload

    rows = [
        json.loads(line)
        for line in (tmp_path / "rows.jsonl").read_text(encoding="utf-8").splitlines()
    ]
    summary = json.loads((tmp_path / "summary.json").read_text(encoding="utf-8"))

    assert summary["total_rows"] == len(rows)
    assert summary["global"]["total_gap_records"] == len(rows)
    assert rows[0]["surface"] == "low_full"
    assert {
        "gap",
        "count",
        "share",
        "min_gap_divisor_count",
        "mean_gap_divisor_count",
        "max_gap_divisor_count",
    } == set(
        (tmp_path / "gap_frequency.csv")
        .read_text(encoding="utf-8")
        .splitlines()[0]
        .split(",")
    )
