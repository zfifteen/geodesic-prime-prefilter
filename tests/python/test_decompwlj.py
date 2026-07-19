"""Tests for joint decompwlj and PGS enrichment logic."""

from __future__ import annotations

import os
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
SOURCE_DIR = ROOT / "src" / "python"
EXPERIMENT_DIR = ROOT / "experiments" / "decompwlj-pgs"

if str(SOURCE_DIR) not in sys.path:
    sys.path.insert(0, str(SOURCE_DIR))
if str(EXPERIMENT_DIR) not in sys.path:
    sys.path.insert(0, str(EXPERIMENT_DIR))

# Test both imports to ensure both structures are working
from prime_gap_structure.decompwlj import (
    decomp_prime as pgs_decomp_prime,
    generate_hybrid_csv as pgs_generate_hybrid_csv,
)
from decompwlj import (
    decomp_prime as exp_decomp_prime,
    generate_hybrid_csv as exp_generate_hybrid_csv,
)


def test_decomp_prime_correctness():
    """Verify that decomp_prime correctly decomposes consecutive prime pairs."""
    # Test a typical prime pair with a valid decomposition
    # p = 11, q = 13. g = 2, ell = 2*11 - 13 = 9.
    # Divisors of 9 are 1, 3, 9. Candidates > g: 3, 9.
    # k = min(3, 9) = 3. L = 9 // 3 = 3.
    # w (leftmost min tau in interior range(12, 13) which is just {12}).
    # tau(12) = 6. E_w = (6/2 - 1)*log(12) = 2*log(12).
    # Z_w = exp(-E_w) = 1/144.
    rec = pgs_decomp_prime(11, 13)
    assert rec is not None
    assert rec["p"] == 11
    assert rec["q"] == 13
    assert rec["g"] == 2
    assert rec["ell"] == 9
    assert rec["k"] == 3
    assert rec["L"] == 3
    assert rec["class"] == "weight"
    assert rec["w"] == 12
    assert rec["tau_w"] == 6
    assert rec["is_square"] is False
    assert rec["compress"] == 1

    # Ensure experiment module version behaves exactly the same
    rec_exp = exp_decomp_prime(11, 13)
    assert rec_exp == rec


def test_decomp_prime_edge_cases():
    """Verify that decomp_prime handles small gaps and invalid arguments."""
    # p < 2
    assert pgs_decomp_prime(1, 3) is None
    # q <= p
    assert pgs_decomp_prime(5, 5) is None
    # ell <= g: p = 3, q = 5. g = 2. ell = 6 - 5 = 1 <= 2.
    assert pgs_decomp_prime(3, 5) is None


def test_generate_hybrid_csv(tmp_path):
    """Verify that generate_hybrid_csv builds the dataset file correctly."""
    output_file = tmp_path / "test_hybrid.csv"
    records = pgs_generate_hybrid_csv(
        num_primes=20,
        output_file=str(output_file),
        start_p=2,
    )
    assert len(records) > 0
    assert output_file.exists()

    # Check headers and row count
    with open(output_file, "r") as f:
        lines = f.readlines()
        assert len(lines) == len(records) + 1  # header + data rows
