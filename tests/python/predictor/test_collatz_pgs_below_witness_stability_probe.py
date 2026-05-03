"""Tests for the below-witness stability probe."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
BENCHMARK_DIR = ROOT / "benchmarks" / "python" / "predictor"
if str(BENCHMARK_DIR) not in sys.path:
    sys.path.insert(0, str(BENCHMARK_DIR))

from collatz_pgs_below_witness_stability_probe import (  # noqa: E402
    run_probe,
    sign_test_two_sided,
)
from collatz_pgs_same_gap_scale_probe import first_descent_block  # noqa: E402
from collatz_pgs_terminal_adjacent_side_probe import (  # noqa: E402
    CLASS_ABOVE_WITNESS,
    CLASS_BELOW_WITNESS,
)
from collatz_pgs_terminal_contact_decomposition_probe import (  # noqa: E402
    CLASS_NO_WITNESS,
)


def write_rows(path: Path, rows: list[dict[str, object]]) -> None:
    """Write LF-terminated JSONL rows."""
    with path.open("w", encoding="utf-8", newline="") as handle:
        for row in rows:
            handle.write(json.dumps(row, sort_keys=True) + "\n")


def row(seed: int, reset_strength: float) -> dict[str, object]:
    """Return a block row with exact transition metadata."""
    transitions = first_descent_block(seed)
    return {
        "seed": seed,
        "odd_steps_to_first_descent": len(transitions),
        "final_v2": transitions[-1].v2,
        "reset_strength": reset_strength,
        "max_source": max(transition.source for transition in transitions),
        "max_source_over_seed": (
            max(transition.source for transition in transitions) / seed
        ),
    }


def test_sign_test_two_sided_is_exact_for_small_counts():
    """The sign test should use exact binomial tail mass."""
    assert sign_test_two_sided(0, 0) == 1.0
    assert sign_test_two_sided(1, 0) == 1.0
    assert sign_test_two_sided(2, 0) == 0.5
    assert sign_test_two_sided(3, 1) == 0.625


def test_run_probe_reports_median_and_tail_sign_stability(tmp_path):
    """The full probe should report sign facts for median and tail deltas."""
    input_path = tmp_path / "blocks.jsonl"
    output_dir = tmp_path / "out"
    write_rows(
        input_path,
        [
            row(777, 5.0),
            row(825, 3.0),
            row(17, 2.0),
            row(9, 7.0),
            row(15, 11.0),
        ],
    )

    summary = run_probe(input_path, output_dir)

    assert summary["class_counts"] == {
        CLASS_BELOW_WITNESS: 1,
        CLASS_ABOVE_WITNESS: 1,
        CLASS_NO_WITNESS: 1,
    }
    assert summary["strata_count"] == 1
    below_vs_no = summary["below_vs_no_witness"]
    assert below_vs_no["matched_strata_count"] == 1
    assert below_vs_no["matched_weight_total"] == 1
    assert below_vs_no["median_delta_sign"]["positive_strata_count"] == 1
    assert below_vs_no["median_delta_sign"]["weighted_mean_delta"] == 3.0
    assert below_vs_no["p90_delta_sign"]["weighted_mean_delta"] == 3.0
    assert below_vs_no["p99_delta_sign"]["weighted_mean_delta"] == 3.0

    below_vs_above = summary["below_vs_above"]
    assert below_vs_above["median_delta_sign"]["weighted_mean_delta"] == 2.0
    top_row = below_vs_above["top_positive_median_delta_strata"][0]
    assert top_row["matched_weighted_mean_of_stratum_median_delta_contribution"] == 2.0
    assert (output_dir / "summary.json").exists()
    assert (output_dir / "stability_rows.jsonl").exists()


def test_run_probe_rejects_final_v2_mismatch(tmp_path):
    """Input rows must match recomputed terminal transition metadata."""
    input_path = tmp_path / "blocks.jsonl"
    output_dir = tmp_path / "out"
    bad_row = row(777, 5.0)
    bad_row["final_v2"] = 1
    write_rows(input_path, [bad_row])

    try:
        run_probe(input_path, output_dir)
    except ValueError as error:
        assert "final-v2 mismatch" in str(error)
    else:
        raise AssertionError("expected final-v2 mismatch")
