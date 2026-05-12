"""Tests for the Collatz-PGS same-gap scale probe."""

from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from collatz_pgs_same_gap_scale_probe import (  # noqa: E402
    PrimeContext,
    accelerated_odd_transition,
    classify_block,
    first_descent_block,
    rate,
    v2,
)


def test_accelerated_odd_transition_values():
    """The accelerated odd map should divide out the full power of 2."""
    transition = accelerated_odd_transition(3)

    assert v2(28) == 2
    assert transition.source == 3
    assert transition.target == 5
    assert transition.v2 == 1


def test_first_descent_block_stopping_condition():
    """The block includes the transition that first drops below seed."""
    transitions = first_descent_block(3)

    assert [(item.source, item.target, item.v2) for item in transitions] == [
        (3, 5, 1),
        (5, 1, 4),
    ]


def test_same_gap_background_excludes_prime_endpoints():
    """Prime endpoints should not contribute to same-gap interior background."""
    context = PrimeContext(31)
    prime_state = context.source_state(5)
    composite_state = context.source_state(9)
    gap = context.gap_profile(composite_state.prev_prime, composite_state.next_prime)

    assert prime_state.is_prime
    assert composite_state.prev_prime == 7
    assert composite_state.next_prime == 11
    assert gap.odd_interior_count == 1
    assert gap.odd_projected_witness_hit_count == 1


def test_witness_contact_block_classification():
    """A block with one composite witness source should classify as contact."""
    context = PrimeContext(31)

    assert classify_block(first_descent_block(3), context) == "no_witness_contact"
    assert classify_block(first_descent_block(9), context) == "witness_contact"


def test_reset_strength_calculation():
    """Reset strength should be seed divided by first lower odd target."""
    transitions = first_descent_block(9)
    reset_strength = 9 / transitions[-1].target

    assert transitions[-1].target == 7
    assert reset_strength == 9 / 7
    assert rate(1, 4) == 0.25
