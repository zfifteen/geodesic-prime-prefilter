"""Tests for the square-budget handoff shock demo."""

from __future__ import annotations

import importlib.util
import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
MODULE_PATH = (
    ROOT
    / "benchmarks"
    / "python"
    / "predictor"
    / "gwr_square_budget_handoff_shock_demo.py"
)


def load_module():
    """Load the square-budget handoff shock demo from disk."""
    spec = importlib.util.spec_from_file_location(
        "gwr_square_budget_handoff_shock_demo",
        MODULE_PATH,
    )
    if spec is None or spec.loader is None:
        raise RuntimeError("unable to load square-budget handoff shock demo")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_assign_scale_neutral_phase_budget_bit_splits_by_power_and_geometry():
    """The scale-neutral bit should split d=4 rows inside power-local geometry cells."""
    module = load_module()
    rows = [
        {
            "power": 12,
            "current_next_dmin": 4,
            "current_carrier_family": "odd_semiprime",
            "current_winner_offset": 2,
            "current_first_open_offset": 4,
            "current_square_phase_utilization": 0.10,
        },
        {
            "power": 12,
            "current_next_dmin": 4,
            "current_carrier_family": "odd_semiprime",
            "current_winner_offset": 2,
            "current_first_open_offset": 4,
            "current_square_phase_utilization": 0.20,
        },
        {
            "power": 18,
            "current_next_dmin": 4,
            "current_carrier_family": "odd_semiprime",
            "current_winner_offset": 2,
            "current_first_open_offset": 4,
            "current_square_phase_utilization": 0.01,
        },
        {
            "power": 18,
            "current_next_dmin": 4,
            "current_carrier_family": "odd_semiprime",
            "current_winner_offset": 2,
            "current_first_open_offset": 4,
            "current_square_phase_utilization": 0.02,
        },
        {
            "power": 18,
            "current_next_dmin": 8,
            "current_carrier_family": "higher_divisor_even",
            "current_winner_offset": 1,
            "current_first_open_offset": 2,
            "current_square_phase_utilization": None,
        },
    ]

    module.assign_scale_neutral_phase_budget_bit(rows)

    assert rows[0][module.SCALE_NEUTRAL_FIELD] == "d4_low"
    assert rows[1][module.SCALE_NEUTRAL_FIELD] == "d4_high"
    assert rows[2][module.SCALE_NEUTRAL_FIELD] == "d4_low"
    assert rows[3][module.SCALE_NEUTRAL_FIELD] == "d4_high"
    assert rows[4][module.SCALE_NEUTRAL_FIELD] == "non_d4"


def test_summarize_matches_scale_neutral_surface():
    """The committed retained surface should keep the scale-neutral handoff signal."""
    module = load_module()
    summary = module.summarize(
        module.DEFAULT_DETAIL_CSV,
        module.DEFAULT_HANDOFF_SUMMARY,
        min_power=12,
        max_power=18,
    )

    scale = summary["scale_neutral_phase_budget_bit"]
    stats = scale["label_stats"]
    metrics = {
        row["candidate_id"]: row
        for row in summary["candidate_metrics"]
    }
    handoff = summary["existing_matched_high_scale_handoff"]

    assert summary["transition_count"] == 1778
    assert math.isclose(summary["baseline_log_loss"], 0.5993080476093358)
    assert math.isclose(handoff["low_next_triad_share"], 0.6993865030674846)
    assert math.isclose(handoff["high_next_triad_share"], 0.6595092024539877)
    assert stats["d4_low"]["support"] == 618
    assert stats["d4_high"]["support"] == 803
    assert stats["non_d4"]["support"] == 357
    assert math.isclose(stats["d4_low"]["next_triad_share"], 0.7038834951456311)
    assert math.isclose(stats["d4_high"]["next_triad_share"], 0.6662515566625156)
    assert math.isclose(scale["low_minus_high_lift"], 0.03763193848311553)
    assert math.isclose(
        metrics["scale_neutral_phase_budget_bit"]["log_loss_gain"],
        0.015048506005672202,
    )
    assert (
        metrics["scale_neutral_phase_budget_bit"]["log_loss_gain"]
        > metrics["current_winner_parity"]["log_loss_gain"]
    )
    assert math.isclose(
        metrics[
            "current_winner_parity+previous_reduced_state+scale_neutral_phase_budget_bit"
        ]["log_loss_gain"],
        0.1247779984979338,
    )
    assert (
        metrics[
            "current_winner_parity+previous_reduced_state+scale_neutral_phase_budget_bit"
        ]["log_loss_gain"]
        > metrics["current_winner_parity+previous_reduced_state"]["log_loss_gain"]
    )
    assert scale["all_per_power_phase_gains_positive"] is True
    assert all(
        value > 0.0
        for value in metrics["scale_neutral_phase_budget_bit"][
            "per_power_log_loss_gain"
        ].values()
    )


def test_cli_writes_compact_summary_and_findings(tmp_path):
    """The CLI should emit the JSON summary and Markdown findings note."""
    module = load_module()
    findings_path = tmp_path / "square_budget_handoff_shock.md"

    assert (
        module.main(
            [
                "--output-dir",
                str(tmp_path),
                "--findings-path",
                str(findings_path),
            ]
        )
        == 0
    )

    summary = json.loads(
        (tmp_path / module.SUMMARY_FILENAME).read_text(encoding="utf-8")
    )
    findings_text = findings_path.read_text(encoding="utf-8")

    assert summary["title"] == "Prime-Square Interval Utilization and Next-Gap Semiprime Return"
    assert "scale_neutral_phase_budget_bit" in summary
    assert "Prime-Square Interval Utilization" in findings_text
    assert "Held-Out Test" in findings_text
