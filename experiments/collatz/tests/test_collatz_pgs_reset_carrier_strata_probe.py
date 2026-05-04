"""Tests for the Collatz-PGS reset carrier-strata probe."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from collatz_pgs_reset_carrier_strata_probe import (  # noqa: E402
    CLASS_NO_WITNESS,
    CLASS_WITNESS,
    CarrierStats,
    run_probe,
)


def write_rows(path: Path, rows: list[dict[str, object]]) -> None:
    """Write LF-terminated JSONL rows."""
    with path.open("w", encoding="utf-8", newline="") as handle:
        for row in rows:
            handle.write(json.dumps(row, sort_keys=True) + "\n")


def row(
    seed: int,
    block_class: str,
    odd_steps: int,
    reset_strength: float,
) -> dict[str, object]:
    """Return a minimal block row."""
    return {
        "seed": seed,
        "block_class": block_class,
        "odd_steps_to_first_descent": odd_steps,
        "reset_strength": reset_strength,
    }


def test_carrier_stats_reconstructs_transition_composition():
    """Transition composition should come from the seed, not from labels."""
    stats = CarrierStats()

    stats.add(row(7, CLASS_WITNESS, 4, 1.4))

    record = stats.record()
    assert record["count"] == 1
    assert record["mean_v2_sum"] == 7.0
    assert record["median_final_v2"] == 3.0
    assert record["final_v2_mode"] == 3
    assert record["v2_bin_rates"] == {
        "1": 0.5,
        "2": 0.25,
        "3-4": 0.25,
        ">=5": 0.0,
    }


def test_carrier_stats_rejects_odd_step_mismatch():
    """The probe should fail on inconsistent source rows."""
    stats = CarrierStats()

    with pytest.raises(ValueError, match="odd-step mismatch"):
        stats.add(row(7, CLASS_WITNESS, 3, 1.4))


def test_run_probe_reports_positive_and_negative_carriers(tmp_path):
    """The full probe should identify signed carrier strata."""
    input_path = tmp_path / "blocks.jsonl"
    output_dir = tmp_path / "out"
    write_rows(
        input_path,
        [
            row(5, CLASS_WITNESS, 1, 6.0),
            row(9, CLASS_NO_WITNESS, 1, 3.0),
            row(3, CLASS_WITNESS, 2, 2.0),
            row(19, CLASS_NO_WITNESS, 2, 4.0),
            row(7, CLASS_WITNESS, 4, 8.0),
        ],
    )

    summary = run_probe(input_path, output_dir)

    assert summary["matched_strata_count"] == 2
    assert summary["matched_weight_total"] == 2
    assert summary["favorable_strata_count"] == 1
    assert summary["unfavorable_strata_count"] == 1
    assert summary["net_weighted_mean_of_stratum_median_reset_delta"] == 0.5
    assert summary["positive_delta_contribution_sum"] == 1.5
    assert summary["negative_delta_contribution_sum"] == -1.0
    assert (
        summary["top_positive_delta_carriers"][0]["odd_steps_to_first_descent"]
        == 1
    )
    assert (
        summary["top_negative_delta_carriers"][0]["odd_steps_to_first_descent"]
        == 2
    )
    assert (output_dir / "summary.json").exists()
    assert (output_dir / "carrier_rows.jsonl").exists()
