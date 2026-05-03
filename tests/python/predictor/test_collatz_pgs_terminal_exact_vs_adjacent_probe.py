"""Tests for the exact versus adjacent terminal Collatz-PGS probe."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
BENCHMARK_DIR = ROOT / "benchmarks" / "python" / "predictor"
if str(BENCHMARK_DIR) not in sys.path:
    sys.path.insert(0, str(BENCHMARK_DIR))

from collatz_pgs_same_gap_scale_probe import PrimeContext, first_descent_block  # noqa: E402
from collatz_pgs_terminal_contact_decomposition_probe import (  # noqa: E402
    CLASS_NO_WITNESS,
    CLASS_NONTERMINAL,
)
from collatz_pgs_terminal_exact_vs_adjacent_probe import (  # noqa: E402
    CLASS_ADJACENT_TERMINAL,
    CLASS_EXACT_TERMINAL,
    run_probe,
    terminal_exactness_class,
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


def test_terminal_exactness_class_splits_exact_adjacent_and_other_blocks():
    """Terminal projected hits should split by exact witness offset."""
    context = PrimeContext(100)

    assert terminal_exactness_class(first_descent_block(9), context) == (
        CLASS_EXACT_TERMINAL
    )
    assert terminal_exactness_class(first_descent_block(45), context) == (
        CLASS_ADJACENT_TERMINAL
    )
    assert terminal_exactness_class(first_descent_block(17), context) == (
        CLASS_NO_WITNESS
    )
    assert terminal_exactness_class(first_descent_block(15), context) == (
        CLASS_NONTERMINAL
    )


def test_run_probe_matches_exact_adjacent_and_no_witness_blocks(tmp_path):
    """The full probe should compare exact, adjacent, and no-witness blocks."""
    input_path = tmp_path / "blocks.jsonl"
    output_dir = tmp_path / "out"
    write_rows(
        input_path,
        [
            row(9, 6.0),
            row(81, 3.0),
            row(17, 2.0),
            row(15, 5.0),
        ],
    )

    summary = run_probe(input_path, output_dir)

    assert summary["class_counts"] == {
        CLASS_EXACT_TERMINAL: 1,
        CLASS_ADJACENT_TERMINAL: 1,
        CLASS_NONTERMINAL: 1,
        CLASS_NO_WITNESS: 1,
    }
    assert summary["strata_count"] == 1
    assert summary["exact_vs_adjacent"]["matched_strata_count"] == 1
    assert (
        summary["exact_vs_adjacent"][
            "weighted_mean_of_stratum_median_reset_delta"
        ]
        == 3.0
    )
    assert (
        summary["exact_vs_no_witness"][
            "weighted_mean_of_stratum_median_reset_delta"
        ]
        == 4.0
    )
    assert (
        summary["adjacent_vs_no_witness"][
            "weighted_mean_of_stratum_median_reset_delta"
        ]
        == 1.0
    )

    top_row = summary["exact_vs_adjacent"]["top_positive_strata"][0]
    assert top_row["matched_weighted_mean_of_stratum_median_delta_contribution"] == 3.0
    assert top_row["left_median_reset_strength"] == 6.0
    assert top_row["right_median_reset_strength"] == 3.0
    assert (output_dir / "summary.json").exists()
    assert (output_dir / "strata_rows.jsonl").exists()


def test_run_probe_rejects_final_v2_mismatch(tmp_path):
    """Input rows must match recomputed terminal transition metadata."""
    input_path = tmp_path / "blocks.jsonl"
    output_dir = tmp_path / "out"
    bad_row = row(9, 6.0)
    bad_row["final_v2"] = 1
    write_rows(input_path, [bad_row])

    try:
        run_probe(input_path, output_dir)
    except ValueError as error:
        assert "final-v2 mismatch" in str(error)
    else:
        raise AssertionError("expected final-v2 mismatch")
