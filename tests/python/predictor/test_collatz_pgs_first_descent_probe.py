"""Tests for the Collatz-PGS first-descent probe."""

from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
BENCHMARK_DIR = ROOT / "benchmarks" / "python" / "predictor"
if str(BENCHMARK_DIR) not in sys.path:
    sys.path.insert(0, str(BENCHMARK_DIR))

from collatz_pgs_first_descent_probe import (  # noqa: E402
    accelerated_odd_transition,
    build_gap_states,
    first_descent_block,
    profile,
    v2,
)


def test_accelerated_odd_transition():
    """The odd Collatz transition should return the divided odd target."""
    assert v2(28) == 2
    assert accelerated_odd_transition(3).target == 5
    assert accelerated_odd_transition(3).v2 == 1


def test_first_descent_block_stops_at_first_lower_odd():
    """The first-descent block includes the transition that drops below seed."""
    transitions = first_descent_block(3)

    assert [(item.source, item.target, item.v2) for item in transitions] == [
        (3, 5, 1),
        (5, 1, 4),
    ]


def test_profile_separates_prime_endpoints_from_interior_witness_hits():
    """Interior witness rates should not count prime endpoints as witness hits."""
    states = build_gap_states(31)

    record = profile([5, 9, 15], states)

    assert record["count"] == 3
    assert record["prime_count"] == 1
    assert record["composite_count"] == 2
    assert record["interior_odd_projected_witness_hit_count"] == 2
    assert record["interior_odd_projected_witness_hit_rate"] == 1.0
