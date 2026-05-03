"""Tests for the terminal adjacent residue probe."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
BENCHMARK_DIR = ROOT / "benchmarks" / "python" / "predictor"
if str(BENCHMARK_DIR) not in sys.path:
    sys.path.insert(0, str(BENCHMARK_DIR))

from collatz_pgs_terminal_adjacent_residue_probe import (  # noqa: E402
    SIDE_ABOVE,
    SIDE_BELOW,
    adjacent_side,
    expected_witness_residue,
    residue_row,
    run_probe,
)


def write_rows(path: Path, rows: list[dict[str, object]]) -> None:
    """Write LF-terminated JSONL rows."""
    with path.open("w", encoding="utf-8", newline="") as handle:
        for row in rows:
            handle.write(json.dumps(row, sort_keys=True) + "\n")


def block_row(
    seed: int,
    final_source: int,
    final_witness: int,
    final_v2: int,
    target: int,
    reset_strength: float,
) -> dict[str, object]:
    """Return one minimal block row."""
    return {
        "seed": seed,
        "final_source": final_source,
        "final_witness": final_witness,
        "final_v2": final_v2,
        "final_is_prime": False,
        "final_odd_projected_witness_hit": True,
        "terminal_below_seed": target,
        "reset_strength": reset_strength,
        "odd_steps_to_first_descent": 3,
    }


def test_expected_residues_match_below_and_above_identities():
    """Residues should encode 3(w - 1)+1 and 3(w + 1)+1 divisibility."""
    assert expected_witness_residue(SIDE_BELOW, 2) == 2
    assert expected_witness_residue(SIDE_BELOW, 4) == 6
    assert expected_witness_residue(SIDE_ABOVE, 6) == 20


def test_adjacent_residue_row_checks_exact_final_v2():
    """One row should record residue, exact-v2, and target consistency."""
    row = block_row(
        seed=27,
        final_source=9,
        final_witness=10,
        final_v2=2,
        target=7,
        reset_strength=27.0 / 7.0,
    )

    assert adjacent_side(row) == SIDE_BELOW
    record = residue_row(row, SIDE_BELOW)

    assert record["residue_ok"] is True
    assert record["exact_v2_residue_ok"] is True
    assert record["computed_v2_ok"] is True
    assert record["target_match"] is True
    assert record["witness_residue"] == record["expected_witness_residue"]


def test_run_probe_reports_adjacent_residue_summaries(tmp_path):
    """The probe should ignore exact hits and summarize adjacent sides."""
    input_path = tmp_path / "block_rows.jsonl"
    output_dir = tmp_path / "out"
    write_rows(
        input_path,
        [
            block_row(27, 9, 10, 2, 7, 27.0 / 7.0),
            block_row(63, 21, 20, 6, 1, 63.0),
            block_row(15, 12, 12, 1, 37, 1.0),
        ],
    )

    summary = run_probe(input_path, output_dir)

    assert summary["adjacent_terminal_count"] == 2
    assert summary["overall"]["residue_ok_rate"] == 1.0
    assert summary["overall"]["exact_v2_residue_ok_rate"] == 1.0
    assert summary["overall"]["computed_v2_ok_rate"] == 1.0
    assert summary["overall"]["target_match_rate"] == 1.0
    assert summary["by_side"][SIDE_BELOW]["count"] == 1
    assert summary["by_side"][SIDE_ABOVE]["count"] == 1
    assert (output_dir / "summary.json").exists()
    assert (output_dir / "residue_rows.jsonl").exists()
    assert (output_dir / "side_rows.jsonl").exists()
    assert (output_dir / "side_final_v2_rows.jsonl").exists()
