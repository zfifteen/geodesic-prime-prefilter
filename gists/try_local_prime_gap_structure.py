#!/usr/bin/env python3
"""Try a local prime-gap endpoint selector yourself.

This file is intentionally standalone. It does not import this repository.

What it demonstrates:

1. Compute exact divisor counts in a short local interval to the right of a
   known prime p.
2. Use the local divisor-count state to select the next candidate q.
3. Verify afterward that q is the next prime after p.
4. Draw plots so the local structure is visible.

The exact divisor counts are the measured input. They are not free. The point
of the demonstration is what the local interval state determines once it is
available.
"""

from __future__ import annotations

import json
import math
from dataclasses import dataclass
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt


OUTPUT_DIR = Path("plots")
UINT64_LIMIT = 2**64  # Highest integer range covered by the deterministic check.
OPEN_RESIDUES_MOD_30 = frozenset({1, 7, 11, 13, 17, 19, 23, 29})


@dataclass(frozen=True)
class SelectionResult:
    """The selected endpoint and the local data used to select it."""

    p: int
    q: int
    bound: int
    counts: list[int]
    selected_offset: int
    simplest_composite: int | None
    simplest_composite_divisors: int | None
    candidate_rows: list[dict[str, object]]
    verified: bool


def integer_cube_root_floor(value: int) -> int:
    """Return floor(cuberoot(value)) using integer correction."""
    if value < 0:
        raise ValueError("value must be non-negative")

    root = int(round(value ** (1.0 / 3.0)))  # Estimate the cube root.
    while (root + 1) ** 3 <= value:  # Check whether the next integer still cubes below value.
        root += 1  # Move the estimate up by one.
    while root**3 > value:  # Check whether the current integer cubes above value.
        root -= 1  # Move the estimate down by one.
    return root


def primes_up_to(limit: int) -> list[int]:
    """Return all primes up to limit by the ordinary sieve of Eratosthenes."""
    if limit < 2:
        return []

    sieve = bytearray(b"\x01") * (limit + 1)  # Allocate one slot for each integer from 0 to limit.
    sieve[0:2] = b"\x00\x00"
    for n in range(2, math.isqrt(limit) + 1):  # Only factors up to sqrt(limit) can start new crossings.
        if sieve[n]:
            start = n * n  # The first new composite multiple for n is n squared.
            stop = limit + 1  # Python slices stop one past the last integer we want.
            crossed_count = ((limit - start) // n) + 1  # Count how many multiples of n are crossed off.
            sieve[start:stop:n] = b"\x00" * crossed_count  # Write one zero byte per crossed-off multiple.
    return [n for n in range(2, limit + 1) if sieve[n]]  # Read back the surviving prime slots.


def is_prime_under_2_to_64(n: int) -> bool:
    """Return True exactly when n is prime, for n below 2^64."""
    if not 0 <= n < UINT64_LIMIT:
        raise ValueError("this demonstration only checks integers below 2^64")
    if n < 2:
        return False

    small_primes = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37)
    for prime in small_primes:
        if n == prime:
            return True
        if n % prime == 0:  # A zero remainder means prime divides n.
            return False

    odd_part = n - 1  # Start from n - 1 for the standard primality check.
    shifts = 0
    while odd_part % 2 == 0:  # Remove factors of 2 from n - 1.
        odd_part //= 2  # Divide out one factor of 2.
        shifts += 1  # Count one removed factor of 2.

    # These bases make the strong probable-prime test deterministic below 2^64.
    bases = (2, 325, 9375, 28178, 450775, 9780504, 1795265022)
    for base in bases:
        base %= n  # Reduce the base into the range 0..n-1.
        if base in (0, 1):
            continue

        value = pow(base, odd_part, n)  # Compute base^odd_part modulo n.
        if value in (1, n - 1):  # n - 1 is the same as -1 modulo n.
            continue

        for _ in range(shifts - 1):  # One power was already tested, so test the remaining powers.
            value = (value * value) % n  # Square the value and keep only the remainder modulo n.
            if value == n - 1:  # n - 1 is the success value in this check.
                break
        else:
            return False

    return True


def divisor_counts_interval(lo: int, hi: int) -> list[int]:
    """Return exact divisor counts for every integer in [lo, hi)."""
    if lo < 1:
        raise ValueError("lo must be at least 1")
    if hi <= lo:
        raise ValueError("hi must be larger than lo")
    if hi > UINT64_LIMIT:
        raise ValueError("this demonstration only handles intervals below 2^64")

    residuals = list(range(lo, hi))
    divisor_counts = [1] * (hi - lo)  # Store one divisor count for each integer in the interval.
    small_primes = primes_up_to(
        integer_cube_root_floor(hi - 1)  # Only primes up to the cube root are needed at this stage.
    )

    for prime in small_primes:
        start = ((lo + prime - 1) // prime) * prime  # Round lo up to the first multiple of prime.
        for value in range(start, hi, prime):
            index = value - lo  # Convert the integer value into a zero-based list index.
            exponent = 0
            while residuals[index] % prime == 0:  # A zero remainder means prime still divides the residual.
                residuals[index] //= prime  # Divide out one copy of prime.
                exponent += 1  # Count that one copy of prime.
            if exponent:
                divisor_counts[index] *= exponent + 1  # A prime power p^e contributes e + 1 divisors.

    for index, remainder in enumerate(residuals):
        if remainder == 1:
            continue

        if is_prime_under_2_to_64(remainder):
            divisor_counts[index] *= 2  # One remaining prime factor doubles the divisor count.
            continue

        root = math.isqrt(remainder)
        if root * root == remainder and is_prime_under_2_to_64(root):  # root squared detects p^2.
            divisor_counts[index] *= 3  # One remaining square p^2 contributes 3 divisors.
            continue

        # After removing every prime factor up to the cube root, a remaining
        # composite below the interval maximum has exactly two prime factors.
        divisor_counts[index] *= 4  # Two remaining prime factors contribute 4 divisors.

    if lo <= 1 < hi:
        divisor_counts[1 - lo] = 1  # Convert integer 1 into its zero-based list index.

    return divisor_counts


def is_candidate_number(n: int) -> bool:
    """Return True for numbers not divisible by 2, 3, or 5."""
    return n % 30 in OPEN_RESIDUES_MOD_30  # Keep the remainder after division by 30.


def next_prime_after(n: int) -> int:
    """Return the next prime after n, used only for final verification."""
    if n < 2:
        return 2

    candidate = n + 1  # Start with the first integer after n.
    if candidate <= 2:
        candidate = 2
    elif candidate % 2 == 0:  # Even numbers above 2 cannot be prime.
        candidate += 1  # Move from an even candidate to the next odd candidate.

    while candidate < UINT64_LIMIT:
        if is_prime_under_2_to_64(candidate):
            return candidate
        candidate += 2  # Skip the next even number.
    raise ValueError("verification passed the 2^64 demonstration limit")


def select_next_from_local_counts(p: int, bound: int) -> SelectionResult:
    """Select the next endpoint from exact local divisor-count state."""
    if not is_prime_under_2_to_64(p):
        raise ValueError(f"p must be prime for this demonstration: {p}")
    if bound < 1:
        raise ValueError("bound must be positive")

    counts = divisor_counts_interval(
        p + 1,  # Start at the first integer to the right of p.
        p + bound + 1,  # Stop one past the requested local interval.
    )
    candidate_rows: list[dict[str, object]] = []
    simplest_offset: int | None = None
    simplest_divisors: int | None = None
    selected_offset: int | None = None
    selected_prior_simplest_offset: int | None = None
    selected_prior_simplest_divisors: int | None = None
    prior_prime_seen = False

    for offset, divisor_count in enumerate(counts, start=1):
        n = p + offset  # Convert an offset from p into the actual integer.

        if is_candidate_number(n):
            if divisor_count > 2:
                status = "rejected composite"
            elif prior_prime_seen:
                status = "later interval material"
            else:
                status = "selected endpoint"
                selected_offset = offset
                selected_prior_simplest_offset = simplest_offset
                selected_prior_simplest_divisors = simplest_divisors

            candidate_rows.append(
                {
                    "offset": offset,
                    "n": n,
                    "divisors": divisor_count,
                    "status": status,
                    "simplest_composite_so_far": (
                        None
                        if simplest_offset is None
                        else p + simplest_offset  # Convert the saved offset into the actual integer.
                    ),
                    "simplest_composite_divisors": simplest_divisors,
                }
            )

        if divisor_count > 2:
            if simplest_divisors is None or divisor_count < simplest_divisors:
                simplest_offset = offset
                simplest_divisors = divisor_count
        else:
            prior_prime_seen = True

    if selected_offset is None:
        raise RuntimeError(f"no selected endpoint inside bound={bound} for p={p}")

    q = p + selected_offset  # Convert the selected offset into the selected endpoint.
    return SelectionResult(
        p=p,
        q=q,
        bound=bound,
        counts=counts,
        selected_offset=selected_offset,
        simplest_composite=(
            None
            if selected_prior_simplest_offset is None
            else p + selected_prior_simplest_offset  # Convert the saved offset into the actual integer.
        ),
        simplest_composite_divisors=selected_prior_simplest_divisors,
        candidate_rows=candidate_rows,
        verified=next_prime_after(p) == q,
    )


def print_grade_school_example() -> None:
    """Show the small gap 23..29 using only divisor counts."""
    p = 23
    q = 29
    counts = divisor_counts_interval(p + 1, q)  # Start at the first integer after p.
    values = list(range(p + 1, q))  # List the integers strictly between p and q.
    min_count = min(counts)
    winner = values[counts.index(min_count)]

    print("Fourth-grade example: the gap from 23 to 29")
    print("The numbers between them are 24, 25, 26, 27, 28.")
    for value, divisor_count in zip(values, counts):
        marker = "  <-- smallest divisor count" if value == winner else ""
        print(f"  d({value}) = {divisor_count}{marker}")
    print(f"The leftmost smallest-count composite is {winner}.")
    print()


def print_selection_result(result: SelectionResult) -> None:
    """Print one compact record and its local verification status."""
    record = {"p": result.p, "q": result.q}
    print(json.dumps(record))
    print(
        f"  selected offset: {result.selected_offset}; "
        f"bound: {result.bound}; "
        f"verified next prime: {result.verified}"
    )
    if result.simplest_composite is not None:
        print(
            "  simplest composite before the selected endpoint: "
            f"{result.simplest_composite} "
            f"with {result.simplest_composite_divisors} divisors"
        )
    print()


def plot_small_gap() -> Path:
    """Plot the fourth-grade example."""
    output_path = OUTPUT_DIR / "small_gap_divisor_counts.png"
    p = 23
    q = 29
    values = list(range(p + 1, q))  # List the integers strictly between p and q.
    counts = divisor_counts_interval(p + 1, q)  # Start at the first integer after p.
    min_count = min(counts)
    colors = ["#2ca02c" if count == min_count else "#7f7f7f" for count in counts]

    fig, axis = plt.subplots(figsize=(8.5, 4.8), constrained_layout=True)
    axis.bar([str(value) for value in values], counts, color=colors)
    axis.set_title("Between 23 and 29, divisor counts identify the simplest composite")
    axis.set_xlabel("Composite number")
    axis.set_ylabel("Number of divisors")
    axis.grid(axis="y", alpha=0.25)
    fig.savefig(output_path, dpi=180)
    plt.close(fig)
    return output_path


def plot_candidate_scans(results: list[SelectionResult]) -> Path:
    """Plot divisor counts by offset for three example intervals."""
    output_path = OUTPUT_DIR / "candidate_scan_examples.png"
    shown = results[:3]
    fig, axes = plt.subplots(
        len(shown),
        1,
        figsize=(12.0, 8.8),
        sharex=False,
        constrained_layout=True,
    )

    for axis, result in zip(axes, shown):
        offsets = list(range(1, result.bound + 1))  # Include every offset from 1 through the bound.
        counts = result.counts
        colors = []
        for offset, divisor_count in zip(offsets, counts):
            n = result.p + offset  # Convert an offset from p into the actual integer.
            if offset == result.selected_offset:
                colors.append("#2ca02c")
            elif is_candidate_number(n) and divisor_count > 2:
                colors.append("#d62728")
            elif is_candidate_number(n):
                colors.append("#1f77b4")
            else:
                colors.append("#c7c7c7")

        axis.scatter(offsets, counts, c=colors, s=20, linewidths=0)
        axis.axvline(result.selected_offset, color="#2ca02c", linewidth=1.8)
        axis.set_title(f"p = {result.p}; selected q = {result.q}")
        axis.set_xlabel("Offset from p")
        axis.set_ylabel("Divisors")
        axis.grid(alpha=0.22)

    fig.suptitle("Local divisor-count scans select the next endpoint", fontsize=14)
    fig.savefig(output_path, dpi=180)
    plt.close(fig)
    return output_path


def plot_massive_zoom(result: SelectionResult) -> Path:
    """Plot the massive example as a close-up local interval."""
    output_path = OUTPUT_DIR / "massive_scale_zoom.png"
    max_offset = min(
        result.bound,
        max(64, result.selected_offset + 24),  # Show at least 24 offsets beyond the selected endpoint.
    )
    offsets = list(range(1, max_offset + 1))  # Include every offset from 1 through max_offset.
    counts = result.counts[:max_offset]
    colors = []
    sizes = []

    for offset, divisor_count in zip(offsets, counts):
        n = result.p + offset  # Convert an offset from p into the actual integer.
        if offset == result.selected_offset:
            colors.append("#2ca02c")
            sizes.append(80)
        elif is_candidate_number(n) and divisor_count > 2:
            colors.append("#d62728")
            sizes.append(35)
        elif is_candidate_number(n):
            colors.append("#1f77b4")
            sizes.append(55)
        else:
            colors.append("#bdbdbd")
            sizes.append(16)

    fig, axis = plt.subplots(figsize=(12.0, 5.6), constrained_layout=True)
    axis.scatter(offsets, counts, c=colors, s=sizes, linewidths=0)
    axis.axvline(result.selected_offset, color="#2ca02c", linewidth=2.2)
    axis.text(
        result.selected_offset,
        max(counts) * 0.95,  # Place the label slightly below the top of the plot.
        f"q = p + {result.selected_offset}",
        ha="left",
        va="top",
        color="#2ca02c",
        fontsize=11,
    )
    axis.set_title(f"Massive local interval: p = {result.p}")
    axis.set_xlabel("Offset from p")
    axis.set_ylabel("Number of divisors")
    axis.grid(alpha=0.22)
    fig.savefig(output_path, dpi=180)
    plt.close(fig)
    return output_path


def main() -> int:
    """Run the examples and create the plots."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    print_grade_school_example()

    examples = [
        (23, 128),
        (89, 128),
        (999_983, 128),
        (999_999_999_999_997_033, 128),
        (1_693_182_318_746_371, 2048),
    ]
    results = [select_next_from_local_counts(p, bound) for p, bound in examples]

    print("Local endpoint selections")
    for result in results:
        print_selection_result(result)

    if not all(result.verified for result in results):
        raise RuntimeError("at least one downstream verification failed")

    plot_paths = [
        plot_small_gap(),
        plot_candidate_scans(results[:4]),
        plot_massive_zoom(results[3]),
    ]

    print("Plots written")
    for path in plot_paths:
        print(f"  {path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
