#!/usr/bin/env python3
"""Smoke tests for plot-library pure helpers (stdlib + fixtures only)."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

LIBRARY = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(LIBRARY))

from _common.data import divisor_count, gwr_witness, materialize_gap_field, zero_excess_e  # noqa: E402
from _common.status import lint_caption_text, normalize_status  # noqa: E402


class TestDataHelpers(unittest.TestCase):
    def test_primes_have_two_divisors(self) -> None:
        for p in (11, 13, 89, 97):
            self.assertEqual(divisor_count(p), 2)

    def test_zero_excess_on_primes(self) -> None:
        self.assertAlmostEqual(zero_excess_e(89, 2), 0.0)

    def test_gwr_on_89_97(self) -> None:
        w, d = gwr_witness(89, 97)
        field = materialize_gap_field(89, 97)
        self.assertEqual(w, field["w"])
        self.assertEqual(d, field["w_d"])
        # leftmost min-d among interior
        interior_ds = [divisor_count(n) for n in range(90, 97)]
        self.assertEqual(d, min(interior_ds))

    def test_status_lint_blocks_validated_on_weak(self) -> None:
        issues = lint_caption_text("This is validated on our laptop", claim_language="weak")
        self.assertTrue(any("validated" in i for i in issues))

    def test_status_lint_blocks_measured_pass_on_weak(self) -> None:
        issues = lint_caption_text("A measured pass is not a theorem", claim_language="weak")
        self.assertTrue(any("measured pass" in i for i in issues))

    def test_status_normalize(self) -> None:
        self.assertEqual(normalize_status("Theorem"), "theorem")


if __name__ == "__main__":
    raise SystemExit(unittest.main())
