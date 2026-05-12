"""Tests for the short-block reset theorem-candidate probe."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from collatz_pgs_short_block_reset_candidate_probe import (  # noqa: E402
    CLASS_BELOW,
    CLASS_NO_WITNESS,
    exact_reset_formula,
    inverse_seed_from_terminal,
    row_record,
    run_probe,
    terminal_class,
    transition_exponents,
)


def write_rows(path: Path, rows: list[dict[str, object]]) -> None:
    """Write LF-terminated JSONL rows."""
    with path.open("w", encoding="utf-8", newline="") as handle:
        for row in rows:
            handle.write(json.dumps(row, sort_keys=True) + "\n")


def below_row() -> dict[str, object]:
    """Return one real exact 3-step, final-v2=4, below-minimizer row."""
    return {
        "final_gap_width": 6,
        "final_is_prime": False,
        "final_next_prime": 10889,
        "final_odd_projected_witness_hit": True,
        "final_prev_prime": 10883,
        "final_source": 10885,
        "final_v2": 4,
        "final_witness": 10886,
        "odd_steps_to_first_descent": 3,
        "seed": 9675,
        "source_interior_odd_projected_witness_hit_count": 1,
        "terminal_below_seed": 2041,
    }


def no_witness_row() -> dict[str, object]:
    """Return one real exact 3-step, final-v2=4, no-witness row."""
    return {
        "final_gap_width": 0,
        "final_is_prime": True,
        "final_next_prime": 197,
        "final_odd_projected_witness_hit": False,
        "final_prev_prime": 197,
        "final_source": 197,
        "final_v2": 4,
        "final_witness": 197,
        "odd_steps_to_first_descent": 3,
        "seed": 87,
        "source_interior_odd_projected_witness_hit_count": 0,
        "terminal_below_seed": 37,
    }


def test_inverse_branch_formula_for_exact_three_step_row():
    """The observed below row should close the branch-2 inverse formula."""
    sources, targets, exponents = transition_exponents(9675, 3)

    assert sources == [9675, 14513, 10885]
    assert targets == [14513, 10885, 2041]
    assert exponents == [1, 2, 4]
    assert inverse_seed_from_terminal(10885, 2) == 9675
    assert exact_reset_formula(10885, 4, 2) == 9675 / 2041


def test_row_record_classifies_below_minimizer_branch():
    """The target row should preserve residue, mod-9, and formula checks."""
    record = row_record(below_row())

    assert record is not None
    assert terminal_class(below_row()) == CLASS_BELOW
    assert record["terminal_class"] == CLASS_BELOW
    assert record["middle_v2"] == 2
    assert record["witness_mod9"] == 5
    assert record["below_residue_exact_for_final_v2"]
    assert record["formula_seed_ok"]
    assert record["formula_reset_ok"]


def test_row_record_classifies_no_witness_control():
    """A no-contact block should stay in the no-witness control class."""
    record = row_record(no_witness_row())

    assert record is not None
    assert terminal_class(no_witness_row()) == CLASS_NO_WITNESS
    assert record["terminal_class"] == CLASS_NO_WITNESS
    assert record["middle_v2"] == 1
    assert record["formula_seed_ok"]


def test_run_probe_writes_compact_candidate_tables(tmp_path):
    """The probe should produce compact theorem-candidate summaries."""
    input_path = tmp_path / "block_rows.jsonl"
    output_dir = tmp_path / "out"
    write_rows(input_path, [below_row(), no_witness_row()])

    summary = run_probe(input_path, output_dir)

    assert summary["target_row_count"] == 2
    assert summary["exponent_law"]["first_v2_all_one"]
    assert summary["exponent_law"]["middle_v2_only_one_or_two"]
    assert summary["below_minimizer_target"]["count"] == 1
    assert summary["below_minimizer_target"]["all_observed_below_rows_are_middle_v2_2"]
    assert summary["below_minimizer_target"]["all_observed_below_rows_have_witness_mod9_5"]
    assert summary["median_comparisons"][0]["left_class"] == CLASS_BELOW
    assert (output_dir / "summary.json").exists()
    assert (output_dir / "target_rows.jsonl").exists()
    assert (output_dir / "class_rows.jsonl").exists()
    assert (output_dir / "branch_rows.jsonl").exists()
    assert (output_dir / "gap_width_rows.jsonl").exists()
    assert (output_dir / "residue_gap_width_rows.jsonl").exists()
