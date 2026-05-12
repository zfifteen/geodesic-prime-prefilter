"""Tests for the Collatz-PGS source-position carrier probe."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from collatz_pgs_same_gap_scale_probe import PrimeContext, first_descent_block  # noqa: E402
from collatz_pgs_source_position_carrier_probe import (  # noqa: E402
    CLASS_NO_WITNESS,
    CLASS_WITNESS,
    PositionStats,
    run_probe,
)


def write_rows(path: Path, rows: list[dict[str, object]]) -> None:
    """Write LF-terminated JSONL rows."""
    with path.open("w", encoding="utf-8", newline="") as handle:
        for row in rows:
            handle.write(json.dumps(row, sort_keys=True) + "\n")


def row(seed: int, block_class: str, reset_strength: float) -> dict[str, object]:
    """Return a block row with exact odd-step metadata."""
    transitions = first_descent_block(seed)
    return {
        "seed": seed,
        "block_class": block_class,
        "odd_steps_to_first_descent": len(transitions),
        "reset_strength": reset_strength,
        "max_source": max(transition.source for transition in transitions),
    }


def test_position_stats_reports_terminal_one_step_hit():
    """A one-step witness block should report first and final source contact."""
    context = PrimeContext(100)
    stats = PositionStats()

    stats.add(row(9, CLASS_WITNESS, 4.0), context)

    record = stats.record()
    assert record["count"] == 1
    assert record["source_witness_hit_rate"] == 1.0
    assert record["first_source_witness_hit_rate"] == 1.0
    assert record["final_source_witness_hit_rate"] == 1.0
    assert record["median_first_hit_fraction"] == 1.0
    assert record["median_last_hit_fraction"] == 1.0
    assert record["exact_witness_hit_rate"] == 1.0
    assert record["hit_index_rates"] == {"1": 1.0}


def test_position_stats_reports_nearest_nonhit_source():
    """A no-witness block should retain nearest-witness source position."""
    context = PrimeContext(200)
    stats = PositionStats()

    stats.add(row(23, CLASS_NO_WITNESS, 2.0), context)

    record = stats.record()
    assert record["source_witness_hit_rate"] == 0.0
    assert record["final_source_witness_hit_rate"] == 0.0
    assert record["median_min_odd_witness_distance"] == 2.0
    assert record["median_closest_index_fraction"] == pytest.approx(2.0 / 3.0)


def test_position_stats_rejects_odd_step_mismatch():
    """The probe should fail on inconsistent block metadata."""
    context = PrimeContext(100)
    stats = PositionStats()
    bad_row = row(9, CLASS_WITNESS, 4.0)
    bad_row["odd_steps_to_first_descent"] = 2

    with pytest.raises(ValueError, match="odd-step mismatch"):
        stats.add(bad_row, context)


def test_run_probe_reports_signed_position_carriers(tmp_path):
    """The full probe should summarize favorable and unfavorable source positions."""
    input_path = tmp_path / "blocks.jsonl"
    output_dir = tmp_path / "out"
    write_rows(
        input_path,
        [
            row(9, CLASS_WITNESS, 4.0),
            row(5, CLASS_NO_WITNESS, 2.0),
            row(43, CLASS_WITNESS, 1.0),
            row(23, CLASS_NO_WITNESS, 3.0),
        ],
    )

    summary = run_probe(input_path, output_dir)

    assert summary["matched_strata_count"] == 2
    assert summary["matched_weight_total"] == 2
    assert (
        summary["top_positive_position_carriers"][0][
            "odd_steps_to_first_descent"
        ]
        == 1
    )
    assert (
        summary["top_negative_position_carriers"][0][
            "odd_steps_to_first_descent"
        ]
        == 3
    )
    assert (
        summary["top_positive_position_carriers"][0][
            "witness_final_source_witness_hit_rate"
        ]
        == 1.0
    )
    assert (output_dir / "summary.json").exists()
    assert (output_dir / "source_position_rows.jsonl").exists()
