#!/usr/bin/env python3
"""Self-contained Collatz and prime-gap divisor-minimizer demonstration."""

from __future__ import annotations

import argparse
import json
import math
from collections import Counter
from dataclasses import dataclass


DEFAULT_LIMIT = 100_000
MR_BASES_64 = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37)


@dataclass(frozen=True)
class Transition:
    """One accelerated odd Collatz transition."""

    source: int
    target: int
    factors_of_two: int


@dataclass(frozen=True)
class GapProfile:
    """Divisor-minimizer profile for one prime gap."""

    left_prime: int
    right_prime: int
    minimizer: int
    minimizer_divisor_count: int
    odd_interior_count: int
    odd_minimizer_cell_count: int


@dataclass(frozen=True)
class SourceState:
    """Prime-gap divisor state for one odd Collatz source."""

    n: int
    is_prime: bool
    divisor_count: int
    left_prime: int
    right_prime: int
    minimizer: int
    odd_minimizer_distance: int
    odd_minimizer_hit: bool


class PrimeGapContext:
    """Exact local prime-gap and divisor-count context."""

    def __init__(self, max_value: int) -> None:
        self.factor_primes = small_primes(math.isqrt(max(4, 2 * max_value)) + 16)
        self.prime_cache: dict[int, bool] = {}
        self.source_cache: dict[int, SourceState] = {}
        self.gap_cache: dict[tuple[int, int], GapProfile] = {}

    def is_prime(self, n: int) -> bool:
        """Return deterministic primality for one positive integer below 2^64."""
        cached = self.prime_cache.get(n)
        if cached is not None:
            return cached

        if n < 2:
            result = False
        elif n in MR_BASES_64:
            result = True
        elif n % 2 == 0:
            result = False
        else:
            result = True
            for base in MR_BASES_64:
                if n % base == 0:
                    result = False
                    break
            if result:
                result = strong_base_test(n)

        self.prime_cache[n] = result
        return result

    def divisor_count(self, n: int) -> int:
        """Return the exact number of positive divisors of n."""
        remaining = n
        total = 1
        for prime in self.factor_primes:
            if prime * prime > remaining:
                break
            if remaining % prime != 0:
                continue
            exponent = 0
            while remaining % prime == 0:
                remaining //= prime
                exponent += 1
            total *= exponent + 1
        if remaining > 1:
            total *= 2
        return total

    def previous_prime(self, n: int) -> int:
        """Return the greatest prime below n."""
        candidate = n - 1
        if candidate % 2 == 0:
            candidate -= 1
        while candidate >= 3:
            if self.is_prime(candidate):
                return candidate
            candidate -= 2
        return 2

    def next_prime(self, n: int) -> int:
        """Return the least prime above n."""
        candidate = n + 1
        if candidate % 2 == 0:
            candidate += 1
        while True:
            if self.is_prime(candidate):
                return candidate
            candidate += 2

    def gap_profile(self, left_prime: int, right_prime: int) -> GapProfile:
        """Return the leftmost divisor-count minimizer inside one prime gap."""
        key = (left_prime, right_prime)
        cached = self.gap_cache.get(key)
        if cached is not None:
            return cached

        minimizer = left_prime + 1
        minimizer_divisor_count = self.divisor_count(minimizer)
        for value in range(left_prime + 2, right_prime):
            divisor_count = self.divisor_count(value)
            if divisor_count < minimizer_divisor_count:
                minimizer = value
                minimizer_divisor_count = divisor_count

        odd_start = left_prime + 1
        if odd_start % 2 == 0:
            odd_start += 1
        odd_interior_count = len(range(odd_start, right_prime, 2))
        odd_minimizer_cell_count = len(
            odd_cells_nearest_minimizer(left_prime, right_prime, minimizer)
        )
        profile = GapProfile(
            left_prime=left_prime,
            right_prime=right_prime,
            minimizer=minimizer,
            minimizer_divisor_count=minimizer_divisor_count,
            odd_interior_count=odd_interior_count,
            odd_minimizer_cell_count=odd_minimizer_cell_count,
        )
        self.gap_cache[key] = profile
        return profile

    def source_state(self, n: int) -> SourceState:
        """Return the prime-gap divisor state for one odd source value."""
        cached = self.source_cache.get(n)
        if cached is not None:
            return cached

        if self.is_prime(n):
            state = SourceState(
                n=n,
                is_prime=True,
                divisor_count=2,
                left_prime=n,
                right_prime=n,
                minimizer=n,
                odd_minimizer_distance=0,
                odd_minimizer_hit=False,
            )
            self.source_cache[n] = state
            return state

        left_prime = self.previous_prime(n)
        right_prime = self.next_prime(n)
        gap = self.gap_profile(left_prime, right_prime)
        distance = odd_minimizer_distance(n, left_prime, right_prime, gap.minimizer)
        state = SourceState(
            n=n,
            is_prime=False,
            divisor_count=self.divisor_count(n),
            left_prime=left_prime,
            right_prime=right_prime,
            minimizer=gap.minimizer,
            odd_minimizer_distance=distance,
            odd_minimizer_hit=distance == 0,
        )
        self.source_cache[n] = state
        return state


def small_primes(limit: int) -> list[int]:
    """Return every prime up to limit by sieve."""
    sieve = bytearray(b"\x01") * (limit + 1)
    if limit >= 0:
        sieve[0] = 0
    if limit >= 1:
        sieve[1] = 0
    for value in range(2, math.isqrt(limit) + 1):
        if not sieve[value]:
            continue
        start = value * value
        sieve[start : limit + 1 : value] = b"\x00" * (((limit - start) // value) + 1)
    return [value for value in range(2, limit + 1) if sieve[value]]


def strong_base_test(n: int) -> bool:
    """Return deterministic Miller-Rabin primality for n below 2^64."""
    odd_part = n - 1
    shifts = 0
    while odd_part % 2 == 0:
        odd_part //= 2
        shifts += 1

    for base in MR_BASES_64:
        if base >= n:
            continue
        value = pow(base, odd_part, n)
        if value == 1 or value == n - 1:
            continue
        passed = False
        for _ in range(shifts - 1):
            value = (value * value) % n
            if value == n - 1:
                passed = True
                break
        if not passed:
            return False
    return True


def factors_of_two(value: int) -> int:
    """Return the exponent of 2 dividing one positive even integer."""
    return (value & -value).bit_length() - 1


def accelerated_odd_step(n: int) -> Transition:
    """Return the next odd Collatz value after one odd source."""
    value = 3 * n + 1
    exponent = factors_of_two(value)
    return Transition(source=n, target=value >> exponent, factors_of_two=exponent)


def first_descent_block(seed: int) -> list[Transition]:
    """Return odd steps through the first odd target below the seed."""
    block: list[Transition] = []
    current = seed
    while True:
        transition = accelerated_odd_step(current)
        block.append(transition)
        if transition.target < seed:
            return block
        current = transition.target


def odd_cells_nearest_minimizer(
    left_prime: int,
    right_prime: int,
    minimizer: int,
) -> tuple[int, ...]:
    """Return odd interior cells at or adjacent to the divisor minimizer."""
    return tuple(
        value
        for value in (minimizer - 1, minimizer, minimizer + 1)
        if left_prime < value < right_prime and value % 2 == 1
    )


def odd_minimizer_distance(
    n: int,
    left_prime: int,
    right_prime: int,
    minimizer: int,
) -> int:
    """Return distance from n to the odd cells nearest the divisor minimizer."""
    return min(abs(n - value) for value in odd_cells_nearest_minimizer(left_prime, right_prime, minimizer))


def median(values: list[float]) -> float:
    """Return the median value."""
    if not values:
        return 0.0
    ordered = sorted(values)
    midpoint = len(ordered) // 2
    if len(ordered) % 2:
        return ordered[midpoint]
    return (ordered[midpoint - 1] + ordered[midpoint]) / 2.0


def rate(numerator: int, denominator: int) -> float:
    """Return a zero-safe rate."""
    return numerator / denominator if denominator else 0.0


def rate_ratio(
    left_numerator: int,
    left_denominator: int,
    right_numerator: int,
    right_denominator: int,
) -> float:
    """Return a zero-safe rate ratio."""
    right_rate = rate(right_numerator, right_denominator)
    return rate(left_numerator, left_denominator) / right_rate if right_rate else 0.0


def expected_minimizer_residue(side: str, exponent: int) -> int:
    """Return the residue forced on the divisor minimizer by the terminal step."""
    modulus = 1 << exponent
    inverse_three = pow(3, -1, modulus)
    if side == "below":
        return (2 * inverse_three) % modulus
    if side == "above":
        return (-4 * inverse_three) % modulus
    raise ValueError(f"unknown side={side}")


def first_pass_max_seen(limit: int) -> dict[str, int]:
    """Return range facts before prime-gap state construction."""
    max_seen = 3
    total_source_states = 0
    max_odd_steps = 0
    for seed in range(3, limit + 1, 2):
        block = first_descent_block(seed)
        max_seen = max(
            max_seen,
            max(transition.source for transition in block),
            block[-1].target,
        )
        total_source_states += len(block)
        max_odd_steps = max(max_odd_steps, len(block))
    return {
        "max_seen": max_seen,
        "total_source_states": total_source_states,
        "max_odd_steps": max_odd_steps,
    }


def run(limit: int) -> dict[str, object]:
    """Run the standalone demonstration."""
    if limit < 3:
        raise ValueError("limit must be at least 3")

    first_pass = first_pass_max_seen(limit)
    context = PrimeGapContext(first_pass["max_seen"])

    composite_source_count = 0
    source_minimizer_hit_count = 0
    same_gap_odd_count = 0
    same_gap_minimizer_cell_count = 0
    block_class_counts: Counter[str] = Counter()
    terminal_adjacent_counts: Counter[str] = Counter()
    terminal_adjacent_family_counts: Counter[str] = Counter()
    residue_ok_count = 0
    exact_residue_ok_count = 0
    recomputed_step_ok_count = 0
    terminal_target_ok_count = 0
    reset_strengths_by_class = {
        "minimizer_contact": [],
        "no_minimizer_contact": [],
        "terminal_below_minimizer": [],
        "terminal_above_minimizer": [],
    }
    examples = []

    for seed in range(3, limit + 1, 2):
        block = first_descent_block(seed)
        reset_strength = seed / block[-1].target
        has_contact = False

        for transition in block:
            state = context.source_state(transition.source)
            if state.is_prime:
                continue
            composite_source_count += 1
            gap = context.gap_profile(state.left_prime, state.right_prime)
            same_gap_odd_count += gap.odd_interior_count
            same_gap_minimizer_cell_count += gap.odd_minimizer_cell_count
            if state.odd_minimizer_hit:
                source_minimizer_hit_count += 1
                has_contact = True

        block_class = "minimizer_contact" if has_contact else "no_minimizer_contact"
        block_class_counts[block_class] += 1
        reset_strengths_by_class[block_class].append(reset_strength)

        terminal_transition = block[-1]
        terminal_state = context.source_state(terminal_transition.source)
        if terminal_state.is_prime or not terminal_state.odd_minimizer_hit:
            continue

        offset = terminal_state.n - terminal_state.minimizer
        if offset == -1:
            side = "below"
            reset_strengths_by_class["terminal_below_minimizer"].append(reset_strength)
        elif offset == 1:
            side = "above"
            reset_strengths_by_class["terminal_above_minimizer"].append(reset_strength)
        else:
            continue

        exponent = terminal_transition.factors_of_two
        modulus = 1 << exponent
        next_modulus = 1 << (exponent + 1)
        expected = expected_minimizer_residue(side, exponent)
        next_expected = expected_minimizer_residue(side, exponent + 1)
        residue_ok = terminal_state.minimizer % modulus == expected
        exact_residue_ok = terminal_state.minimizer % next_modulus != next_expected
        recomputed_exponent = factors_of_two(3 * terminal_state.n + 1)
        recomputed_target = (3 * terminal_state.n + 1) >> exponent

        residue_ok_count += int(residue_ok)
        exact_residue_ok_count += int(exact_residue_ok)
        recomputed_step_ok_count += int(recomputed_exponent == exponent)
        terminal_target_ok_count += int(recomputed_target == terminal_transition.target)
        terminal_adjacent_counts[side] += 1
        terminal_adjacent_family_counts[f"{len(block)} steps, {exponent} factors of 2"] += 1

        if len(examples) < 5:
            examples.append(
                {
                    "seed": seed,
                    "terminal_source": terminal_state.n,
                    "divisor_minimizer": terminal_state.minimizer,
                    "side": side,
                    "factors_of_two": exponent,
                    "modulus": modulus,
                    "minimizer_residue": terminal_state.minimizer % modulus,
                    "expected_residue": expected,
                    "terminal_target": terminal_transition.target,
                    "reset_strength": reset_strength,
                }
            )

    terminal_adjacent_total = sum(terminal_adjacent_counts.values())
    summary = {
        "limit": limit,
        "odd_seed_count": len(range(3, limit + 1, 2)),
        "max_seen_in_first_descent_blocks": first_pass["max_seen"],
        "total_source_states": first_pass["total_source_states"],
        "max_odd_steps_to_first_descent": first_pass["max_odd_steps"],
        "composite_source_count": composite_source_count,
        "source_minimizer_cell_hit_count": source_minimizer_hit_count,
        "source_minimizer_cell_hit_rate": rate(
            source_minimizer_hit_count,
            composite_source_count,
        ),
        "same_gap_background_odd_cell_count": same_gap_odd_count,
        "same_gap_background_minimizer_cell_count": same_gap_minimizer_cell_count,
        "same_gap_background_hit_rate": rate(
            same_gap_minimizer_cell_count,
            same_gap_odd_count,
        ),
        "source_vs_same_gap_hit_ratio": rate_ratio(
            source_minimizer_hit_count,
            composite_source_count,
            same_gap_minimizer_cell_count,
            same_gap_odd_count,
        ),
        "block_class_counts": dict(sorted(block_class_counts.items())),
        "median_reset_strengths": {
            key: median(values)
            for key, values in sorted(reset_strengths_by_class.items())
        },
        "terminal_adjacent_counts": dict(sorted(terminal_adjacent_counts.items())),
        "terminal_adjacent_total": terminal_adjacent_total,
        "terminal_residue_identity_rate": rate(residue_ok_count, terminal_adjacent_total),
        "terminal_exact_residue_rate": rate(
            exact_residue_ok_count,
            terminal_adjacent_total,
        ),
        "terminal_recomputed_step_rate": rate(
            recomputed_step_ok_count,
            terminal_adjacent_total,
        ),
        "terminal_target_match_rate": rate(
            terminal_target_ok_count,
            terminal_adjacent_total,
        ),
        "most_common_terminal_adjacent_families": terminal_adjacent_family_counts.most_common(8),
        "examples": examples,
    }
    return summary


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description=(
            "Demonstrate a reproducible link between Collatz first-descent "
            "blocks and divisor-count minimizers inside prime gaps."
        )
    )
    parser.add_argument("--limit", type=int, default=DEFAULT_LIMIT)
    return parser.parse_args()


def main() -> None:
    """Run the command-line demonstration."""
    args = parse_args()
    summary = run(args.limit)
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
