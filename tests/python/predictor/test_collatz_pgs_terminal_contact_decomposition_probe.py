"""Tests for the Collatz-PGS terminal-contact decomposition probe."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[3]
BENCHMARK_DIR = ROOT / "benchmarks" / "python" / "predictor"
if str(BENCHMARK_DIR) not in sys.path:
    sys.path.insert(0, str(BENCHMARK_DIR))

from collatz_pgs_same_gap_scale_probe import PrimeContext, first_descent_block  # noqa: E402
from collatz_pgs_terminal_contact_decomposition_probe import (  # noqa: E402
    CLASS_NO_WITNESS,
    CLASS_NONTERMINAL,
    CLASS_TERMINAL,
    run_probe,
    terminal_contact_class,
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


def test_terminal_contact_class_distinguishes_three_cases():
    """Blocks should split into terminal, nonterminal-only, and no-contact classes."""
    context = PrimeContext(500)

    assert terminal_contact_class(row(9, 1.0), context) == CLASS_TERMINAL
    assert terminal_contact_class(row(15, 1.0), context) == CLASS_NONTERMINAL
    assert terminal_contact_class(row(23, 1.0), context) == CLASS_NO_WITNESS


def test_terminal_contact_class_rejects_final_v2_mismatch():
    """The probe should fail on inconsistent final-v2 metadata."""
    context = PrimeContext(100)
    bad_row = row(9, 1.0)
    bad_row["final_v2"] = int(bad_row["final_v2"]) + 1

    with pytest.raises(ValueError, match="final-v2 mismatch"):
        terminal_contact_class(bad_row, context)


def test_run_probe_uses_exact_step_and_final_v2_matching(tmp_path):
    """Matched comparisons should use identical odd-step and final-v2 strata."""
    input_path = tmp_path / "blocks.jsonl"
    output_dir = tmp_path / "out"
    write_rows(
        input_path,
        [
            row(9, 6.0),
            row(17, 2.0),
            row(275, 5.0),
            row(19, 3.0),
            row(395, 9.0),
            row(55, 4.0),
        ],
    )

    summary = run_probe(input_path, output_dir)

    assert summary["class_counts"] == {
        CLASS_TERMINAL: 2,
        CLASS_NONTERMINAL: 2,
        CLASS_NO_WITNESS: 2,
    }
    assert summary["terminal_vs_no_witness"]["matched_strata_count"] == 1
    top_row = summary["terminal_vs_no_witness"]["top_positive_strata"][0]
    assert (
        "matched_weighted_mean_of_stratum_median_delta_contribution"
        in top_row
    )
    assert "matched_weighted_median_delta_contribution" not in top_row
    assert (
        summary["terminal_vs_no_witness"][
            "weighted_mean_of_stratum_median_reset_delta"
        ]
        == 4.0
    )
    assert summary["nonterminal_vs_no_witness"]["matched_strata_count"] == 1
    assert (
        summary["nonterminal_vs_no_witness"][
            "weighted_mean_of_stratum_median_reset_delta"
        ]
        == 2.0
    )
    assert summary["terminal_vs_nonterminal"]["matched_strata_count"] == 1
    assert (
        summary["terminal_vs_nonterminal"][
            "weighted_mean_of_stratum_median_reset_delta"
        ]
        == 5.0
    )
    assert (output_dir / "summary.json").exists()
    assert (output_dir / "strata_rows.jsonl").exists()
