"""Tests for the Collatz-PGS reset length strata probe."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
BENCHMARK_DIR = ROOT / "benchmarks" / "python" / "predictor"
if str(BENCHMARK_DIR) not in sys.path:
    sys.path.insert(0, str(BENCHMARK_DIR))

from collatz_pgs_reset_length_strata_probe import (  # noqa: E402
    CLASS_NO_WITNESS,
    CLASS_WITNESS,
    load_strata,
    run_probe,
    stratum_row,
)


def write_rows(path: Path, rows: list[dict[str, object]]) -> None:
    """Write LF-terminated JSONL rows."""
    with path.open("w", encoding="utf-8", newline="") as handle:
        for row in rows:
            handle.write(json.dumps(row, sort_keys=True) + "\n")


def row(
    block_class: str,
    odd_steps: int,
    reset_strength: float,
    max_source_over_seed: float = 1.0,
    final_hit: bool = False,
) -> dict[str, object]:
    """Return a minimal block row."""
    return {
        "block_class": block_class,
        "odd_steps_to_first_descent": odd_steps,
        "reset_strength": reset_strength,
        "max_source_over_seed": max_source_over_seed,
        "final_odd_projected_witness_hit": final_hit,
    }


def test_load_strata_groups_by_exact_odd_step(tmp_path):
    """Rows should be grouped by exact odd-step count and class."""
    input_path = tmp_path / "blocks.jsonl"
    write_rows(
        input_path,
        [
            row(CLASS_WITNESS, 3, 4.0, final_hit=True),
            row(CLASS_NO_WITNESS, 3, 2.0),
            row(CLASS_WITNESS, 5, 7.0),
        ],
    )

    strata = load_strata(input_path)

    assert len(strata) == 2
    assert strata[3][CLASS_WITNESS].record()["count"] == 1
    assert strata[3][CLASS_NO_WITNESS].record()["count"] == 1
    assert strata[5][CLASS_WITNESS].record()["count"] == 1


def test_stratum_row_reports_matched_reset_delta():
    """A stratum row should compare class medians directly."""
    stats = {
        CLASS_WITNESS: load_stats([row(CLASS_WITNESS, 4, 6.0)]),
        CLASS_NO_WITNESS: load_stats([row(CLASS_NO_WITNESS, 4, 3.0)]),
    }

    record = stratum_row(4, stats)

    assert record["has_both_classes"] is True
    assert record["matched_weight"] == 1
    assert record["median_reset_strength_delta"] == 3.0
    assert record["median_reset_strength_ratio"] == 2.0


def test_run_probe_writes_summary_and_strata_rows(tmp_path):
    """The full probe should write compact summary and stratum rows."""
    input_path = tmp_path / "blocks.jsonl"
    output_dir = tmp_path / "out"
    write_rows(
        input_path,
        [
            row(CLASS_WITNESS, 1, 5.0),
            row(CLASS_NO_WITNESS, 1, 2.0),
            row(CLASS_WITNESS, 3, 4.0),
            row(CLASS_NO_WITNESS, 3, 3.0),
            row(CLASS_WITNESS, 5, 9.0),
        ],
    )

    summary = run_probe(input_path, output_dir)

    assert summary["strata_count"] == 3
    assert summary["matched_strata_count"] == 2
    assert summary["total_witness_contact_blocks"] == 3
    assert summary["total_no_witness_contact_blocks"] == 2
    assert summary["strata_where_witness_median_reset_is_higher"] == 2
    assert (output_dir / "summary.json").exists()
    assert (output_dir / "strata_rows.jsonl").exists()


def load_stats(rows: list[dict[str, object]]):
    """Return a VectorStats loaded from rows."""
    from collatz_pgs_reset_length_strata_probe import VectorStats

    stats = VectorStats()
    for item in rows:
        stats.add(item)
    return stats
