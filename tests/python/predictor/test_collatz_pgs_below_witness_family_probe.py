"""Tests for the below-witness exact carrier-family probe."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
BENCHMARK_DIR = ROOT / "benchmarks" / "python" / "predictor"
if str(BENCHMARK_DIR) not in sys.path:
    sys.path.insert(0, str(BENCHMARK_DIR))

from collatz_pgs_below_witness_family_probe import (  # noqa: E402
    run_probe,
    sign_label,
    sign_pattern,
)


def write_rows(path: Path, rows: list[dict[str, object]]) -> None:
    """Write LF-terminated JSONL rows."""
    with path.open("w", encoding="utf-8", newline="") as handle:
        for row in rows:
            handle.write(json.dumps(row, sort_keys=True) + "\n")


def stability_row(
    odd_steps: int,
    final_v2: int,
    matched_weight: int,
    median_delta: float,
    p90_delta: float,
    p99_delta: float,
) -> dict[str, object]:
    """Return one minimal stability row."""
    left_count = matched_weight
    right_count = matched_weight + 1
    return {
        "odd_steps_to_first_descent": odd_steps,
        "final_v2": final_v2,
        "below_vs_no_witness": {
            "has_both_classes": True,
            "left_count": left_count,
            "right_count": right_count,
            "matched_weight": matched_weight,
            "median_reset_strength_delta": median_delta,
            "median_reset_strength_ratio": 2.0,
            "p90_reset_strength_delta": p90_delta,
            "p90_reset_strength_ratio": 1.5,
            "p99_reset_strength_delta": p99_delta,
            "p99_reset_strength_ratio": 1.25,
            "median_max_source_over_seed_delta": 0.0,
        },
    }


def test_sign_label_and_pattern_are_deterministic():
    """Sign helpers should preserve median/P90/P99 order."""
    row = {
        "median_reset_strength_delta": 3.0,
        "p90_reset_strength_delta": -1.0,
        "p99_reset_strength_delta": 0.0,
    }
    assert sign_label(1.0) == "positive"
    assert sign_label(-1.0) == "negative"
    assert sign_label(0.0) == "tied"
    assert sign_pattern(row) == "positive_negative_tied"


def test_run_probe_decomposes_exact_carrier_families(tmp_path):
    """The probe should report exact family and grouped contributions."""
    input_path = tmp_path / "stability_rows.jsonl"
    output_dir = tmp_path / "out"
    write_rows(
        input_path,
        [
            stability_row(3, 4, 2, 5.0, -1.0, -2.0),
            stability_row(3, 5, 1, -4.0, -2.0, 3.0),
            stability_row(4, 4, 3, 1.0, 2.0, 1.0),
        ],
    )

    summary = run_probe(input_path, output_dir)

    assert summary["family_count"] == 3
    assert summary["matched_weight_total"] == 6
    assert summary["overall"]["overall_median_delta_contribution"] == 1.5
    assert summary["overall"]["overall_p90_delta_contribution"] == (2.0 / 6.0)
    assert summary["overall"]["overall_p99_delta_contribution"] == (2.0 / 6.0)
    assert summary["top_positive_median_families"][0][
        "overall_median_delta_contribution"
    ] == (10.0 / 6.0)
    assert summary["top_negative_median_families"][0][
        "overall_median_delta_contribution"
    ] == (-4.0 / 6.0)

    pattern_rows = {
        row["sign_pattern"]: row for row in summary["sign_pattern_summary"]
    }
    assert pattern_rows["positive_negative_negative"]["matched_weight"] == 2
    assert pattern_rows["negative_negative_positive"]["matched_weight"] == 1
    assert pattern_rows["positive_positive_positive"]["matched_weight"] == 3
    assert (output_dir / "summary.json").exists()
    assert (output_dir / "family_rows.jsonl").exists()
    assert (output_dir / "odd_step_rows.jsonl").exists()
    assert (output_dir / "final_v2_rows.jsonl").exists()
    assert (output_dir / "sign_pattern_rows.jsonl").exists()
