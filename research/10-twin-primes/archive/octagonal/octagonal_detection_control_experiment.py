#!/usr/bin/env python3
"""Control experiment for octagonal intervals and twin primes.

This script asks a stricter question than the coverage test:

    Do octagonal intervals beat same-width nearby intervals?

If they do, that would support an octagonal placement signal. If they do not,
the evidence favors ordinary widening-window coverage.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt


CONTROL_PREFIX_START = 7
CONTROL_PREFIX_LIMIT = 1_500
CONTROL_SHIFTS = (-3, -2, -1, 1, 2, 3)
HIGH_SCALE_CHECKPOINTS = (10_000, 100_000, 1_000_000)
SCRIPT_DIR = Path(__file__).resolve().parent
PLOTS_DIR = SCRIPT_DIR / "plots"


@dataclass(frozen=True)
class WindowResult:
    """Twin-prime measurements for one fixed-width interval."""

    label: str
    shift: int
    lo: int
    hi: int
    width: int
    candidate_centers: int
    twin_pair_count: int
    first_pair: tuple[int, int] | None
    first_min_margin: int | None
    max_empty_center_run: int
    desert_pressure_ratio: float


@dataclass(frozen=True)
class ComparisonResult:
    """Octagonal interval compared to deterministic controls."""

    n: int
    octagonal: WindowResult
    controls: list[WindowResult]
    control_mean_count: float
    control_mean_desert_ratio: float
    count_delta: float
    count_ratio: float
    desert_delta: float
    desert_ratio: float
    pair_count_win_share: float
    desert_win_share: float


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
    if lo < 1:
        raise ValueError("lo must be positive")
    if hi < lo:
        raise ValueError("hi must be at least lo")

    length = hi - lo + 1
    flags = bytearray(b"\x01") * length

    if lo == 1:
        flags[0] = 0

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


def measure_window(
    label: str,
    shift: int,
    lo: int,
    hi: int,
    band_lo: int,
    flags: bytearray,
) -> WindowResult:
    """Measure twin-prime coverage in one subwindow of a sieved band."""
    pairs: list[tuple[int, int]] = []
    twin_center_indices: list[int] = []

    if lo <= 3 and 5 <= hi and flags[3 - band_lo] and flags[5 - band_lo]:
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
        if flags[left_prime - band_lo] and flags[right_prime - band_lo]:
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
    first_left_margin = None if first_pair is None else first_pair[0] - lo
    first_right_margin = None if first_pair is None else hi - first_pair[1]
    first_min_margin = (
        None
        if first_left_margin is None or first_right_margin is None
        else min(first_left_margin, first_right_margin)
    )

    return WindowResult(
        label=label,
        shift=shift,
        lo=lo,
        hi=hi,
        width=hi - lo,
        candidate_centers=candidate_centers,
        twin_pair_count=len(pairs),
        first_pair=first_pair,
        first_min_margin=first_min_margin,
        max_empty_center_run=max_empty_center_run,
        desert_pressure_ratio=desert_pressure_ratio,
    )


def compare_octagonal_interval(n: int, base_primes: list[int]) -> ComparisonResult:
    """Compare one octagonal interval with deterministic same-width controls."""
    oct_lo = octagonal_number(n)
    oct_hi = octagonal_number(n + 1)
    width = oct_hi - oct_lo

    band_lo = min(oct_lo, *(oct_lo + shift * width for shift in CONTROL_SHIFTS))
    band_hi = max(oct_hi, *(oct_hi + shift * width for shift in CONTROL_SHIFTS))
    if band_lo < 1:
        raise ValueError("control band crossed below 1")

    flags = prime_flags_segment(band_lo, band_hi, base_primes)
    octagonal = measure_window(
        label="octagonal",
        shift=0,
        lo=oct_lo,
        hi=oct_hi,
        band_lo=band_lo,
        flags=flags,
    )
    controls = [
        measure_window(
            label=f"shift {shift:+d}",
            shift=shift,
            lo=oct_lo + shift * width,
            hi=oct_hi + shift * width,
            band_lo=band_lo,
            flags=flags,
        )
        for shift in CONTROL_SHIFTS
    ]

    control_mean_count = sum(result.twin_pair_count for result in controls) / len(controls)
    control_mean_desert_ratio = (
        sum(result.desert_pressure_ratio for result in controls) / len(controls)
    )
    count_delta = octagonal.twin_pair_count - control_mean_count
    count_ratio = (
        math.inf if control_mean_count == 0 else octagonal.twin_pair_count / control_mean_count
    )
    desert_delta = octagonal.desert_pressure_ratio - control_mean_desert_ratio
    desert_ratio = (
        math.inf
        if control_mean_desert_ratio == 0
        else octagonal.desert_pressure_ratio / control_mean_desert_ratio
    )
    pair_count_win_share = sum(
        1 for result in controls if octagonal.twin_pair_count > result.twin_pair_count
    ) / len(controls)
    desert_win_share = sum(
        1
        for result in controls
        if octagonal.desert_pressure_ratio < result.desert_pressure_ratio
    ) / len(controls)

    return ComparisonResult(
        n=n,
        octagonal=octagonal,
        controls=controls,
        control_mean_count=control_mean_count,
        control_mean_desert_ratio=control_mean_desert_ratio,
        count_delta=count_delta,
        count_ratio=count_ratio,
        desert_delta=desert_delta,
        desert_ratio=desert_ratio,
        pair_count_win_share=pair_count_win_share,
        desert_win_share=desert_win_share,
    )


def run_experiment() -> tuple[list[ComparisonResult], list[ComparisonResult]]:
    """Run the prefix and checkpoint control comparisons."""
    largest_n = max(CONTROL_PREFIX_LIMIT, *HIGH_SCALE_CHECKPOINTS)
    largest_octagonal_hi = octagonal_number(largest_n + 1)
    largest_width = octagonal_number(largest_n + 1) - octagonal_number(largest_n)
    largest_control_hi = largest_octagonal_hi + max(CONTROL_SHIFTS) * largest_width
    base_primes = primes_up_to(math.isqrt(largest_control_hi))

    prefix_results = [
        compare_octagonal_interval(n, base_primes)
        for n in range(CONTROL_PREFIX_START, CONTROL_PREFIX_LIMIT + 1)
    ]
    checkpoint_results = [
        compare_octagonal_interval(n, base_primes)
        for n in HIGH_SCALE_CHECKPOINTS
    ]
    return prefix_results, checkpoint_results


def mean(values: list[float]) -> float:
    """Return the arithmetic mean."""
    return sum(values) / len(values)


def print_rule(width: int = 78) -> None:
    """Print a horizontal rule."""
    print("=" * width)


def print_section(title: str) -> None:
    """Print a section heading."""
    print()
    print_rule()
    print(title)
    print_rule()


def print_table(headers: list[str], rows: list[list[object]]) -> None:
    """Print a fixed-width table."""
    widths = [len(header) for header in headers]
    for row in rows:
        for index, value in enumerate(row):
            widths[index] = max(widths[index], len(str(value)))

    print("  ".join(header.ljust(widths[index]) for index, header in enumerate(headers)))
    print("  ".join("-" * width for width in widths))
    for row in rows:
        print(
            "  ".join(
                str(value).ljust(widths[index]) for index, value in enumerate(row)
            )
        )


def format_pair(pair: tuple[int, int] | None) -> str:
    """Return a readable twin-prime pair."""
    if pair is None:
        return "none"
    return f"({pair[0]}, {pair[1]})"


def summarize(prefix_results: list[ComparisonResult]) -> dict[str, float]:
    """Return aggregate comparison metrics for the prefix surface."""
    return {
        "mean_octagonal_count": mean(
            [result.octagonal.twin_pair_count for result in prefix_results]
        ),
        "mean_control_count": mean(
            [result.control_mean_count for result in prefix_results]
        ),
        "mean_count_ratio": mean([result.count_ratio for result in prefix_results]),
        "mean_pair_count_win_share": mean(
            [result.pair_count_win_share for result in prefix_results]
        ),
        "mean_octagonal_desert_ratio": mean(
            [result.octagonal.desert_pressure_ratio for result in prefix_results]
        ),
        "mean_control_desert_ratio": mean(
            [result.control_mean_desert_ratio for result in prefix_results]
        ),
        "mean_desert_ratio": mean([result.desert_ratio for result in prefix_results]),
        "mean_desert_win_share": mean(
            [result.desert_win_share for result in prefix_results]
        ),
    }


def detection_verdict(summary: dict[str, float]) -> str:
    """Return the pre-registered detection verdict."""
    count_advantage = (
        summary["mean_count_ratio"] >= 1.05
        and summary["mean_pair_count_win_share"] >= 0.55
    )
    desert_advantage = (
        summary["mean_desert_ratio"] <= 0.95
        and summary["mean_desert_win_share"] >= 0.55
    )

    if count_advantage and desert_advantage:
        return "DETECTION ADVANTAGE FOUND"
    return "NO DETECTION ADVANTAGE ON TESTED SURFACE"


def print_report(
    prefix_results: list[ComparisonResult],
    checkpoint_results: list[ComparisonResult],
    plot_paths: list[Path],
) -> None:
    """Print the console experiment report."""
    summary = summarize(prefix_results)
    verdict = detection_verdict(summary)
    strongest_positive = max(prefix_results, key=lambda result: result.count_delta)
    strongest_negative = min(prefix_results, key=lambda result: result.count_delta)

    print_rule()
    print("Octagonal Intervals: Detection Control Experiment")
    print("Same-width nearby controls, deterministic segmented sieving")
    print_rule()
    print()
    print("Question:")
    print(
        "  Do octagonal intervals contain twin-prime pairs better than "
        "same-width nearby intervals?"
    )
    print()
    print("Interpretation:")
    print(
        "  If octagonal intervals consistently beat controls, that supports an "
        "octagonal placement signal."
    )
    print(
        "  If they look like controls, the evidence supports widening-window "
        "coverage instead."
    )

    print_section("1. Control Construction")
    print("Octagonal interval:")
    print("  [O(n), O(n+1)], where O(n) = n * (3*n - 2)")
    print()
    print("Control intervals:")
    print("  [O(n) + s*w, O(n+1) + s*w], where w = O(n+1) - O(n)")
    print(f"  shifts tested: {CONTROL_SHIFTS}")
    print()
    print("All intervals have the same width for the same n.")
    print("No randomness is used.")

    print_section("2. Decision Rule")
    print("Detection advantage requires both:")
    print("  mean octagonal pair-count ratio >= 1.05")
    print("  mean octagonal pair-count win share >= 0.55")
    print("and both:")
    print("  mean octagonal desert-pressure ratio <= 0.95")
    print("  mean octagonal desert-pressure win share >= 0.55")
    print()
    print("Pair count is better when higher.")
    print("Desert pressure is better when lower.")

    print_section("3. Prefix Result")
    print(f"Prefix compared: n = {CONTROL_PREFIX_START:,}..{CONTROL_PREFIX_LIMIT:,}")
    print(f"Octagonal intervals compared: {len(prefix_results):,}")
    print()
    print_table(
        ["metric", "octagonal", "controls", "ratio or share"],
        [
            [
                "mean pair count",
                f"{summary['mean_octagonal_count']:.4f}",
                f"{summary['mean_control_count']:.4f}",
                f"{summary['mean_count_ratio']:.4f}",
            ],
            [
                "pair-count win share",
                "",
                "",
                f"{summary['mean_pair_count_win_share']:.4f}",
            ],
            [
                "mean desert pressure",
                f"{summary['mean_octagonal_desert_ratio']:.6f}",
                f"{summary['mean_control_desert_ratio']:.6f}",
                f"{summary['mean_desert_ratio']:.4f}",
            ],
            [
                "desert-pressure win share",
                "",
                "",
                f"{summary['mean_desert_win_share']:.4f}",
            ],
        ],
    )

    print_section("4. Strongest Prefix Deviations")
    print_table(
        [
            "case",
            "n",
            "oct pairs",
            "control mean",
            "delta",
            "oct first pair",
            "oct desert",
        ],
        [
            [
                "most above controls",
                f"{strongest_positive.n:,}",
                f"{strongest_positive.octagonal.twin_pair_count:,}",
                f"{strongest_positive.control_mean_count:.2f}",
                f"{strongest_positive.count_delta:.2f}",
                format_pair(strongest_positive.octagonal.first_pair),
                f"{strongest_positive.octagonal.desert_pressure_ratio:.4f}",
            ],
            [
                "most below controls",
                f"{strongest_negative.n:,}",
                f"{strongest_negative.octagonal.twin_pair_count:,}",
                f"{strongest_negative.control_mean_count:.2f}",
                f"{strongest_negative.count_delta:.2f}",
                format_pair(strongest_negative.octagonal.first_pair),
                f"{strongest_negative.octagonal.desert_pressure_ratio:.4f}",
            ],
        ],
    )

    print_section("5. High-Scale Checkpoints")
    print_table(
        [
            "n",
            "oct pairs",
            "control mean",
            "count ratio",
            "oct desert",
            "control desert",
            "desert ratio",
        ],
        [
            [
                f"{result.n:,}",
                f"{result.octagonal.twin_pair_count:,}",
                f"{result.control_mean_count:,.2f}",
                f"{result.count_ratio:.4f}",
                f"{result.octagonal.desert_pressure_ratio:.6f}",
                f"{result.control_mean_desert_ratio:.6f}",
                f"{result.desert_ratio:.4f}",
            ]
            for result in checkpoint_results
        ],
    )

    print_section("6. Verdict")
    print(verdict)
    if verdict.startswith("NO"):
        print(
            "The octagonal intervals did not clear the pre-registered control "
            "thresholds."
        )
        print(
            "On this surface, the stronger reading is coverage by widening "
            "intervals, not detection by octagonal placement."
        )
    else:
        print(
            "The octagonal intervals beat same-width controls on both pair "
            "count and desert pressure."
        )
        print(
            "That would justify treating octagonal placement as a candidate "
            "signal for follow-up."
        )

    print_section("7. Plots")
    for path in plot_paths:
        print(f"  {path}")


def plot_pair_count_delta(results: list[ComparisonResult]) -> Path:
    """Plot octagonal pair count minus mean control pair count."""
    output_path = PLOTS_DIR / "detection_pair_count_delta_prefix.png"
    x_values = [result.n for result in results]
    y_values = [result.count_delta for result in results]

    fig, axis = plt.subplots(figsize=(12.0, 6.0), constrained_layout=True)
    axis.axhline(0, color="#333333", linewidth=1.0)
    axis.plot(x_values, y_values, color="#1f77b4", linewidth=1.1)
    axis.set_title("Octagonal pair count minus same-width control mean")
    axis.set_xlabel("n")
    axis.set_ylabel("Pair-count delta")
    axis.grid(alpha=0.25)
    fig.savefig(output_path, dpi=180)
    plt.close(fig)
    return output_path


def plot_count_ratio(results: list[ComparisonResult]) -> Path:
    """Plot octagonal pair count divided by mean control pair count."""
    output_path = PLOTS_DIR / "detection_count_ratio_prefix.png"
    x_values = [result.n for result in results]
    y_values = [result.count_ratio for result in results]

    fig, axis = plt.subplots(figsize=(12.0, 6.0), constrained_layout=True)
    axis.axhline(1.0, color="#333333", linewidth=1.0)
    axis.axhline(1.05, color="#2ca02c", linewidth=1.0, linestyle=":")
    axis.plot(x_values, y_values, color="#2ca02c", linewidth=1.1)
    axis.set_title("Octagonal pair-count ratio against controls")
    axis.set_xlabel("n")
    axis.set_ylabel("Octagonal / control mean")
    axis.grid(alpha=0.25)
    fig.savefig(output_path, dpi=180)
    plt.close(fig)
    return output_path


def plot_desert_ratio_delta(results: list[ComparisonResult]) -> Path:
    """Plot octagonal desert pressure minus mean control desert pressure."""
    output_path = PLOTS_DIR / "detection_desert_ratio_delta_prefix.png"
    x_values = [result.n for result in results]
    y_values = [result.desert_delta for result in results]

    fig, axis = plt.subplots(figsize=(12.0, 6.0), constrained_layout=True)
    axis.axhline(0, color="#333333", linewidth=1.0)
    axis.plot(x_values, y_values, color="#d62728", linewidth=1.1)
    axis.set_title("Octagonal desert pressure minus same-width control mean")
    axis.set_xlabel("n")
    axis.set_ylabel("Desert-pressure delta")
    axis.grid(alpha=0.25)
    fig.savefig(output_path, dpi=180)
    plt.close(fig)
    return output_path


def plot_high_scale_checkpoints(results: list[ComparisonResult]) -> Path:
    """Plot octagonal and control counts at high-scale checkpoints."""
    output_path = PLOTS_DIR / "detection_high_scale_checkpoints.png"
    labels = [f"{result.n:,}" for result in results]
    octagonal_counts = [result.octagonal.twin_pair_count for result in results]
    control_counts = [result.control_mean_count for result in results]
    positions = list(range(len(results)))
    width = 0.36

    fig, axis = plt.subplots(figsize=(10.5, 6.0), constrained_layout=True)
    axis.bar(
        [position - width / 2 for position in positions],
        octagonal_counts,
        width=width,
        label="octagonal",
        color="#1f77b4",
    )
    axis.bar(
        [position + width / 2 for position in positions],
        control_counts,
        width=width,
        label="control mean",
        color="#ff7f0e",
    )
    axis.set_title("High-scale detection controls")
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
    prefix_results: list[ComparisonResult],
    checkpoint_results: list[ComparisonResult],
) -> list[Path]:
    """Create plots for the control experiment."""
    PLOTS_DIR.mkdir(parents=True, exist_ok=True)
    return [
        plot_pair_count_delta(prefix_results),
        plot_count_ratio(prefix_results),
        plot_desert_ratio_delta(prefix_results),
        plot_high_scale_checkpoints(checkpoint_results),
    ]


def main() -> int:
    """Run the detection control experiment."""
    prefix_results, checkpoint_results = run_experiment()
    plot_paths = create_plots(prefix_results, checkpoint_results)
    print_report(prefix_results, checkpoint_results, plot_paths)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
