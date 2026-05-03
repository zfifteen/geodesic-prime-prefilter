"""Tests for the Collatz-PGS terminal geometry probe."""

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
    CLASS_TERMINAL,
)
from collatz_pgs_terminal_geometry_probe import GeometryStats, run_probe  # noqa: E402


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


def test_geometry_stats_distinguishes_exact_and_adjacent_hits():
    """Terminal hits should preserve exact versus projected-adjacent geometry."""
    context = PrimeContext(100)
    exact_stats = GeometryStats()
    adjacent_stats = GeometryStats()

    exact_stats.add(row(9, 1.0), first_descent_block(9), context)
    adjacent_stats.add(row(45, 1.0), first_descent_block(45), context)

    exact_record = exact_stats.record()
    adjacent_record = adjacent_stats.record()
    assert exact_record["exact_witness_hit_rate"] == 1.0
    assert exact_record["hit_offset_rates"] == {"-1": 0.0, "0": 1.0, "1": 0.0}
    assert adjacent_record["exact_witness_hit_rate"] == 0.0
    assert adjacent_record["adjacent_projected_witness_hit_rate"] == 1.0
    assert adjacent_record["hit_offset_rates"] == {"-1": 1.0, "0": 0.0, "1": 0.0}


def test_run_probe_reports_signed_terminal_geometry(tmp_path):
    """The full probe should report geometry for positive and negative carriers."""
    input_path = tmp_path / "blocks.jsonl"
    output_dir = tmp_path / "out"
    write_rows(
        input_path,
        [
            row(9, 6.0),
            row(17, 2.0),
            row(45, 1.0),
            row(13, 4.0),
        ],
    )

    summary = run_probe(input_path, output_dir)

    assert summary["class_counts"] == {
        CLASS_TERMINAL: 2,
        CLASS_NONTERMINAL: 0,
        CLASS_NO_WITNESS: 2,
    }
    assert summary["matched_strata_count"] == 2
    assert summary["positive_geometry_summary"]["strata_count"] == 1
    assert summary["negative_geometry_summary"]["strata_count"] == 1
    assert (
        summary["positive_geometry_summary"][
            "weighted_mean_terminal_exact_witness_hit_rate"
        ]
        == 1.0
    )
    assert (
        summary["negative_geometry_summary"][
            "weighted_mean_terminal_adjacent_projected_witness_hit_rate"
        ]
        == 1.0
    )
    top_positive = summary["top_positive_geometry_carriers"][0]
    top_negative = summary["top_negative_geometry_carriers"][0]
    assert top_positive["terminal_hit_offset_rates"] == {
        "-1": 0.0,
        "0": 1.0,
        "1": 0.0,
    }
    assert top_negative["terminal_hit_offset_rates"] == {
        "-1": 1.0,
        "0": 0.0,
        "1": 0.0,
    }
    assert (output_dir / "summary.json").exists()
    assert (output_dir / "geometry_rows.jsonl").exists()
