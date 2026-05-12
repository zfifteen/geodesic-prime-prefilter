#!/usr/bin/env python3
"""White-paper console test for octagonal intervals and twin primes.

This script is intentionally standalone. It imports no project code.

Claim tested on the declared finite surface:

    Every tested interval between consecutive octagonal numbers contains at
    least one twin-prime pair.

Global falsification condition:

    One interval with zero contained twin-prime pairs is a counterexample to
    the global conjecture.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt


EXACT_PREFIX_LIMIT = 5_000
HIGH_SCALE_CHECKPOINTS = (10_000, 100_000, 1_000_000)
TWIN_PRIME_CONSTANT = 0.6601618158468696
SCRIPT_DIR = Path(__file__).resolve().parent
PLOTS_DIR = SCRIPT_DIR / "plots"


@dataclass(frozen=True)
class IntervalResult:
    """Exact twin-prime measurement for one octagonal interval."""

    n: int
    lo: int
    hi: int
    width: int
    candidate_centers: int
    twin_pair_count: int
    expected_count: float
    first_pair: tuple[int, int] | None
    last_pair: tuple[int, int] | None
    first_left_margin: int | None
    first_right_margin: int | None
    first_min_margin: int | None
    max_empty_center_run: int
    desert_pressure_ratio: float


def octagonal_number(n: int) -> int:
    """Return the nth octagonal number, O(n) = n(3n - 2)."""
    return n * (3 * n - 2)


def primes_up_to(limit: int) -> list[int]:
    """Return all primes up to limit by the ordinary sieve of Eratosthenes."""
    if limit < 2:
        return []

    sieve = bytearray(b"\x01") * (limit + 1)
    sieve[0:2] = b"\x00\x00"

    for prime in range(2, math.isqrt(limit) + 1):
        if sieve[prime]:
            start = prime * prime
            stop = limit + 1
            crossed_count = ((limit - start) // prime) + 1
            sieve[start:stop:prime] = b"\x00" * crossed_count

    return [value for value in range(2, limit + 1) if sieve[value]]


def prime_flags_segment(lo: int, hi: int, base_primes: list[int]) -> bytearray:
    """Return primality flags for every integer in the inclusive interval."""
    if hi < lo:
        raise ValueError("hi must be at least lo")

    length = hi - lo + 1
    flags = bytearray(b"\x01") * length

    for value in range(lo, min(hi, 1) + 1):
        flags[value - lo] = 0

    for prime in base_primes:
        square = prime * prime
        if square > hi:
            break

        first_multiple = ((lo + prime - 1) // prime) * prime
        start = max(square, first_multiple)
        if start > hi:
            continue

        crossed_count = ((hi - start) // prime) + 1
        flags[start - lo :: prime] = b"\x00" * crossed_count

    return flags


def first_multiple_at_least(value: int, modulus: int) -> int:
    """Return the first multiple of modulus that is at least value."""
    return ((value + modulus - 1) // modulus) * modulus


def twin_prime_expected_count(lo: int, hi: int) -> float:
    """Return the Hardy-Littlewood expected twin-prime count for the interval."""
    midpoint = (lo + hi) / 2
    width = hi - lo
    return 2 * TWIN_PRIME_CONSTANT * width / (math.log(midpoint) ** 2)


def analyze_octagonal_interval(n: int, base_primes: list[int]) -> IntervalResult:
    """Measure twin-prime coverage inside [O(n), O(n + 1)]."""
    lo = octagonal_number(n)
    hi = octagonal_number(n + 1)
    width = hi - lo
    flags = prime_flags_segment(lo, hi, base_primes)

    pairs: list[tuple[int, int]] = []
    twin_center_indices: list[int] = []

    if lo <= 3 and 5 <= hi and flags[3 - lo] and flags[5 - lo]:
        pairs.append((3, 5))

    first_center = first_multiple_at_least(lo + 1, 6)
    last_center = ((hi - 1) // 6) * 6

    if first_center <= last_center:
        first_center_index = first_center // 6
        last_center_index = last_center // 6
        candidate_centers = last_center_index - first_center_index + 1
    else:
        first_center_index = 1
        last_center_index = 0
        candidate_centers = 0

    for center in range(first_center, last_center + 1, 6):
        left_prime = center - 1
        right_prime = center + 1
        if flags[left_prime - lo] and flags[right_prime - lo]:
            pairs.append((left_prime, right_prime))
            twin_center_indices.append(center // 6)

    max_empty_center_run = largest_empty_center_run(
        first_center_index,
        last_center_index,
        twin_center_indices,
    )
    desert_pressure_ratio = (
        0.0 if candidate_centers == 0 else max_empty_center_run / candidate_centers
    )

    first_pair = pairs[0] if pairs else None
    last_pair = pairs[-1] if pairs else None
    first_left_margin = None if first_pair is None else first_pair[0] - lo
    first_right_margin = None if first_pair is None else hi - first_pair[1]
    first_min_margin = (
        None
        if first_left_margin is None or first_right_margin is None
        else min(first_left_margin, first_right_margin)
    )

    return IntervalResult(
        n=n,
        lo=lo,
        hi=hi,
        width=width,
        candidate_centers=candidate_centers,
        twin_pair_count=len(pairs),
        expected_count=twin_prime_expected_count(lo, hi),
        first_pair=first_pair,
        last_pair=last_pair,
        first_left_margin=first_left_margin,
        first_right_margin=first_right_margin,
        first_min_margin=first_min_margin,
        max_empty_center_run=max_empty_center_run,
        desert_pressure_ratio=desert_pressure_ratio,
    )


def largest_empty_center_run(
    first_center_index: int,
    last_center_index: int,
    twin_center_indices: list[int],
) -> int:
    """Return the longest run of center candidates with no twin-prime pair."""
    if first_center_index > last_center_index:
        return 0

    if not twin_center_indices:
        return last_center_index - first_center_index + 1

    max_run = twin_center_indices[0] - first_center_index
    previous = twin_center_indices[0]

    for current in twin_center_indices[1:]:
        empty_between = current - previous - 1
        max_run = max(max_run, empty_between)
        previous = current

    trailing_empty = last_center_index - previous
    return max(max_run, trailing_empty)


def analyze_surface() -> tuple[list[IntervalResult], list[IntervalResult]]:
    """Run the exact prefix and high-scale checkpoint measurements."""
    largest_n = max(EXACT_PREFIX_LIMIT, *HIGH_SCALE_CHECKPOINTS)
    largest_hi = octagonal_number(largest_n + 1)
    base_primes = primes_up_to(math.isqrt(largest_hi))

    prefix_results = [
        analyze_octagonal_interval(n, base_primes)
        for n in range(1, EXACT_PREFIX_LIMIT + 1)
    ]
    checkpoint_results = [
        analyze_octagonal_interval(n, base_primes)
        for n in HIGH_SCALE_CHECKPOINTS
    ]
    return prefix_results, checkpoint_results


def weakest_results(results: list[IntervalResult], count: int) -> list[IntervalResult]:
    """Return intervals with the smallest pair counts and tightest margins."""
    return sorted(
        results,
        key=lambda result: (
            result.twin_pair_count,
            10**30 if result.first_min_margin is None else result.first_min_margin,
            result.n,
        ),
    )[:count]


def counterexamples(results: list[IntervalResult]) -> list[IntervalResult]:
    """Return all measured intervals with no contained twin-prime pair."""
    return [result for result in results if result.twin_pair_count == 0]


def print_rule(width: int = 78) -> None:
    """Print a horizontal rule."""
    print("=" * width)


def print_section(title: str) -> None:
    """Print a section heading."""
    print()
    print_rule()
    print(title)
    print_rule()


def format_pair(pair: tuple[int, int] | None) -> str:
    """Return a readable twin-prime pair."""
    if pair is None:
        return "none"
    return f"({pair[0]}, {pair[1]})"


def print_table(headers: list[str], rows: list[list[object]]) -> None:
    """Print a compact fixed-width table."""
    widths = [len(header) for header in headers]
    for row in rows:
        for index, value in enumerate(row):
            widths[index] = max(widths[index], len(str(value)))

    header_line = "  ".join(
        header.ljust(widths[index]) for index, header in enumerate(headers)
    )
    print(header_line)
    print("  ".join("-" * width for width in widths))

    for row in rows:
        print(
            "  ".join(
                str(value).ljust(widths[index]) for index, value in enumerate(row)
            )
        )


def print_white_paper(
    prefix_results: list[IntervalResult],
    checkpoint_results: list[IntervalResult],
    plot_paths: list[Path],
) -> None:
    """Print the console white paper."""
    all_results = prefix_results + checkpoint_results
    failures = counterexamples(all_results)
    weakest = weakest_results(prefix_results, 12)

    print_rule()
    print("Octagonal Intervals And Twin Primes")
    print("A finite, deterministic white-paper test")
    print_rule()
    print()
    print("Hypothesis under test:")
    print(
        "  Every tested interval between consecutive octagonal numbers contains "
        "at least one twin-prime pair."
    )
    print()
    print("Global falsification condition:")
    print(
        "  One interval [O(n), O(n+1)] with zero contained twin-prime pairs "
        "falsifies the global conjecture."
    )

    print_section("1. Definitions")
    print("Octagonal numbers:")
    print("  O(n) = n * (3*n - 2)")
    print()
    print("Tested interval:")
    print("  [O(n), O(n+1)]")
    print()
    print("Contained twin-prime pair:")
    print("  (p, p + 2), with O(n) <= p and p + 2 <= O(n+1)")

    print_section("2. Why This Scans Twin Centers")
    print(
        "Every twin-prime pair above (3, 5) has the form "
        "(6k - 1, 6k + 1)."
    )
    print(
        "The script therefore scans center candidates 6k inside the interval, "
        "not every integer."
    )
    print(
        "Primality is still exact: each interval is marked by a deterministic "
        "segmented sieve."
    )

    print_section("3. Exact Prefix Verdict")
    exact_failures = counterexamples(prefix_results)
    min_count = min(result.twin_pair_count for result in prefix_results)
    weakest_one = weakest[0]
    print(f"Exact prefix tested: n = 1..{EXACT_PREFIX_LIMIT:,}")
    print(f"Intervals tested: {len(prefix_results):,}")
    print(f"Counterexamples found: {len(exact_failures):,}")
    print(f"Smallest twin-prime pair count in prefix: {min_count:,}")
    print(
        "Weakest interval found: "
        f"n = {weakest_one.n:,}, "
        f"[{weakest_one.lo:,}, {weakest_one.hi:,}], "
        f"first pair = {format_pair(weakest_one.first_pair)}"
    )

    print_section("4. Weakest Prefix Intervals")
    print_table(
        [
            "n",
            "O(n)",
            "O(n+1)",
            "pairs",
            "first pair",
            "left margin",
            "right margin",
            "desert ratio",
        ],
        [
            [
                f"{result.n:,}",
                f"{result.lo:,}",
                f"{result.hi:,}",
                f"{result.twin_pair_count:,}",
                format_pair(result.first_pair),
                "none"
                if result.first_left_margin is None
                else f"{result.first_left_margin:,}",
                "none"
                if result.first_right_margin is None
                else f"{result.first_right_margin:,}",
                f"{result.desert_pressure_ratio:.4f}",
            ]
            for result in weakest
        ],
    )

    print_section("5. High-Scale Checkpoints")
    print_table(
        [
            "n",
            "interval width",
            "center candidates",
            "actual pairs",
            "expected pairs",
            "first pair",
            "desert ratio",
        ],
        [
            [
                f"{result.n:,}",
                f"{result.width:,}",
                f"{result.candidate_centers:,}",
                f"{result.twin_pair_count:,}",
                f"{result.expected_count:,.2f}",
                format_pair(result.first_pair),
                f"{result.desert_pressure_ratio:.6f}",
            ]
            for result in checkpoint_results
        ],
    )

    print_section("6. Falsification Verdict")
    if failures:
        first_failure = failures[0]
        print("FALSIFIED BY COUNTEREXAMPLE")
        print(
            f"First measured counterexample: n = {first_failure.n:,}, "
            f"[{first_failure.lo:,}, {first_failure.hi:,}]"
        )
    else:
        print("PASSED TESTED SURFACE")
        print(
            "No tested interval in the exact prefix or high-scale checkpoints "
            "had zero contained twin-prime pairs."
        )
        print(
            "This validates the finite surface. It does not prove the infinite "
            "conjecture."
        )

    print_section("7. Plots")
    for path in plot_paths:
        print(f"  {path}")


def plot_twin_pair_counts_prefix(results: list[IntervalResult]) -> Path:
    """Plot exact twin-prime pair counts across the prefix."""
    output_path = PLOTS_DIR / "twin_pair_counts_prefix.png"
    x_values = [result.n for result in results]
    y_values = [result.twin_pair_count for result in results]

    fig, axis = plt.subplots(figsize=(12.0, 6.0), constrained_layout=True)
    axis.plot(x_values, y_values, color="#1f77b4", linewidth=1.2)
    axis.set_title(f"Twin-prime pairs in octagonal intervals, n = 1..{EXACT_PREFIX_LIMIT:,}")
    axis.set_xlabel("n")
    axis.set_ylabel("Contained twin-prime pairs")
    axis.grid(alpha=0.25)
    fig.savefig(output_path, dpi=180)
    plt.close(fig)
    return output_path


def plot_weakest_intervals(results: list[IntervalResult]) -> Path:
    """Plot the weakest prefix intervals by pair count."""
    output_path = PLOTS_DIR / "weakest_octagonal_intervals.png"
    weakest = weakest_results(results, 20)
    labels = [str(result.n) for result in weakest]
    counts = [result.twin_pair_count for result in weakest]
    margins = [
        0 if result.first_min_margin is None else result.first_min_margin
        for result in weakest
    ]

    fig, axis = plt.subplots(figsize=(12.0, 6.0), constrained_layout=True)
    bars = axis.bar(labels, counts, color="#2ca02c")
    axis.set_title("Weakest tested octagonal intervals")
    axis.set_xlabel("n")
    axis.set_ylabel("Contained twin-prime pairs")
    axis.grid(axis="y", alpha=0.25)

    for bar, margin in zip(bars, margins):
        axis.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height(),
            f"m={margin}",
            ha="center",
            va="bottom",
            fontsize=8,
            rotation=90,
        )

    fig.savefig(output_path, dpi=180)
    plt.close(fig)
    return output_path


def plot_desert_pressure_ratio(results: list[IntervalResult]) -> Path:
    """Plot the local twin-center desert pressure ratio."""
    output_path = PLOTS_DIR / "desert_pressure_ratio.png"
    x_values = [result.n for result in results]
    y_values = [result.desert_pressure_ratio for result in results]

    fig, axis = plt.subplots(figsize=(12.0, 6.0), constrained_layout=True)
    axis.plot(x_values, y_values, color="#d62728", linewidth=1.1)
    axis.set_title("Largest empty twin-center run divided by center-window length")
    axis.set_xlabel("n")
    axis.set_ylabel("Desert pressure ratio")
    axis.set_ylim(bottom=0)
    axis.grid(alpha=0.25)
    fig.savefig(output_path, dpi=180)
    plt.close(fig)
    return output_path


def plot_high_scale_checkpoint_counts(results: list[IntervalResult]) -> Path:
    """Plot actual and expected twin-prime pair counts at checkpoints."""
    output_path = PLOTS_DIR / "high_scale_checkpoint_counts.png"
    labels = [f"{result.n:,}" for result in results]
    actual = [result.twin_pair_count for result in results]
    expected = [result.expected_count for result in results]
    positions = list(range(len(results)))
    width = 0.36

    fig, axis = plt.subplots(figsize=(10.5, 6.0), constrained_layout=True)
    axis.bar(
        [position - width / 2 for position in positions],
        actual,
        width=width,
        label="actual",
        color="#1f77b4",
    )
    axis.bar(
        [position + width / 2 for position in positions],
        expected,
        width=width,
        label="expected",
        color="#ff7f0e",
    )
    axis.set_title("High-scale checkpoint twin-prime counts")
    axis.set_xlabel("n")
    axis.set_ylabel("Contained twin-prime pairs")
    axis.set_xticks(positions)
    axis.set_xticklabels(labels)
    axis.legend()
    axis.grid(axis="y", alpha=0.25)
    fig.savefig(output_path, dpi=180)
    plt.close(fig)
    return output_path


def create_plots(
    prefix_results: list[IntervalResult],
    checkpoint_results: list[IntervalResult],
) -> list[Path]:
    """Create every plot used by the white paper."""
    PLOTS_DIR.mkdir(parents=True, exist_ok=True)
    return [
        plot_twin_pair_counts_prefix(prefix_results),
        plot_weakest_intervals(prefix_results),
        plot_desert_pressure_ratio(prefix_results),
        plot_high_scale_checkpoint_counts(checkpoint_results),
    ]


def main() -> int:
    """Run the white-paper test."""
    prefix_results, checkpoint_results = analyze_surface()
    plot_paths = create_plots(prefix_results, checkpoint_results)
    print_white_paper(prefix_results, checkpoint_results, plot_paths)
    failures = counterexamples(prefix_results + checkpoint_results)
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
