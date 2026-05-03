"""Tests for the inverse short-block branch counterexample probe."""

from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from collatz_pgs_short_block_branch_counterexample_probe import (  # noqa: E402
    residue_classes,
    run_probe,
    seed_from_witness,
    verify_exact_three_step,
    witness_candidates,
)


def test_residue_classes_enforce_branch_and_exact_final_v2():
    """Residue classes should combine exact 2-adic and mod-9 conditions."""
    residues = residue_classes(4, 2)

    assert residues
    assert all(residue % 9 == 5 for residue in residues)
    assert all((3 * residue - 2) % 16 == 0 for residue in residues)
    assert all((3 * residue - 2) % 32 != 0 for residue in residues)


def test_inverse_seed_for_known_below_minimizer_hit():
    """The known k=4 hit should close branch 2 exactly."""
    assert seed_from_witness(10886, 2) == 9675
    assert verify_exact_three_step(9675, 10885, 4)


def test_witness_candidates_include_known_hits():
    """Candidate enumeration should include the known k=4 branch-2 witness."""
    candidates = set(witness_candidates(10_000, 4, 2))

    assert (10886, 9675) in candidates


def test_run_probe_finds_no_small_branch1_counterexample(tmp_path):
    """The small deterministic scan should find branch-2 hits only."""
    summary = run_probe(10_000, tmp_path)

    assert summary["branch1_counterexample_count"] == 0
    assert summary["branch2_hit_count"] == 2
    assert summary["branch_selection_survives"]
    assert summary["below_minimizer_hit_counts"]["k4_branch2"] == 1
    assert summary["below_minimizer_hit_counts"]["k8_branch2"] == 1
    assert (tmp_path / "summary.json").exists()
    assert (tmp_path / "hit_rows.jsonl").exists()
