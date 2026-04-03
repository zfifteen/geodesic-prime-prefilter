#!/usr/bin/env python3
"""Scan prime gaps for earlier higher-divisor spoilers against the GWR candidate."""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[3]
SOURCE_DIR = ROOT / "src" / "python"
if str(SOURCE_DIR) not in sys.path:
    sys.path.insert(0, str(SOURCE_DIR))

from z_band_prime_composite_field import divisor_counts_segment


@dataclass(frozen=True)
class PairStats:
    """Aggregate one winner-class / earlier-class spoiler pair."""

    winner_divisor_count: int
    earlier_divisor_count: int
    candidate_count: int = 0
    theorem_eliminated_count: int = 0
    unresolved_count: int = 0
    exact_spoiler_count: int = 0
    min_earlier_value: int | None = None
    min_winner_value: int | None = None

    def to_dict(self) -> dict[str, int | None]:
        """Return a JSON-ready mapping."""
        return asdict(self)


def build_parser() -> argparse.ArgumentParser:
    """Build the CLI parser."""
    parser = argparse.ArgumentParser(
        description=(
            "Scan one exact interval for earlier higher-divisor spoilers "
            "against the Gap Winner Rule candidate."
        ),
    )
    parser.add_argument(
        "--lo",
        type=int,
        default=2,
        help="Inclusive lower bound of the natural-number interval.",
    )
    parser.add_argument(
        "--hi",
        type=int,
        default=1_000_001,
        help="Exclusive upper bound of the natural-number interval.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Optional JSON output path.",
    )
    return parser


def score_strictly_greater(
    left_n: int,
    left_divisor_count: int,
    right_n: int,
    right_divisor_count: int,
) -> bool:
    """Return whether the score at `left_n` is strictly greater than at `right_n`."""
    if left_divisor_count < 3 or right_divisor_count < 3:
        raise ValueError("exact score comparison requires composite inputs")

    left_exponent = left_divisor_count - 2
    right_exponent = right_divisor_count - 2
    return pow(left_n, left_exponent) < pow(right_n, right_exponent)


def spoiler_bound_eliminates_candidate(
    earlier_value: int,
    earlier_divisor_count: int,
    winner_divisor_count: int,
) -> bool:
    """Return whether the current spoiler bound already eliminates one earlier candidate."""
    if not (earlier_divisor_count > winner_divisor_count >= 3):
        raise ValueError("spoiler bound requires an earlier strictly higher divisor class")

    return pow(earlier_value, earlier_divisor_count - winner_divisor_count) >= pow(
        2,
        winner_divisor_count - 2,
    )


def analyze_interval(lo: int, hi: int) -> dict[str, object]:
    """Analyze one exact interval for earlier higher-divisor spoilers."""
    if lo < 2:
        raise ValueError("lo must be at least 2")
    if hi <= lo:
        raise ValueError("hi must be greater than lo")

    divisor_count = divisor_counts_segment(lo, hi)
    values = np.arange(lo, hi, dtype=np.int64)
    primes = values[divisor_count == 2]

    pair_stats: dict[tuple[int, int], PairStats] = {}
    winner_class_counts: dict[int, int] = {}
    counterexample_examples: list[dict[str, int]] = []
    unresolved_examples: list[dict[str, int]] = []

    gap_count = 0
    gap_with_earlier_candidates_count = 0
    theorem_eliminated_gap_count = 0
    unresolved_gap_count = 0
    counterexample_gap_count = 0
    earlier_candidate_count = 0
    theorem_eliminated_candidate_count = 0
    unresolved_candidate_count = 0
    exact_spoiler_count = 0

    for left_prime, right_prime in zip(primes[:-1], primes[1:]):
        gap = int(right_prime - left_prime)
        if gap < 4:
            continue

        left_index = int(left_prime - lo + 1)
        right_index = int(right_prime - lo)
        gap_values = values[left_index:right_index]
        gap_divisors = divisor_count[left_index:right_index]

        winner_divisor_count = int(np.min(gap_divisors))
        winner_index = int(np.flatnonzero(gap_divisors == winner_divisor_count)[0])
        winner_value = int(gap_values[winner_index])

        gap_count += 1
        winner_class_counts[winner_divisor_count] = (
            winner_class_counts.get(winner_divisor_count, 0) + 1
        )

        earlier_values = gap_values[:winner_index]
        earlier_divisors = gap_divisors[:winner_index]
        if earlier_values.size == 0:
            theorem_eliminated_gap_count += 1
            continue

        gap_with_earlier_candidates_count += 1
        gap_has_unresolved_candidate = False
        gap_has_counterexample = False

        for earlier_value_raw, earlier_divisor_raw in zip(earlier_values, earlier_divisors):
            earlier_value = int(earlier_value_raw)
            earlier_divisor_count = int(earlier_divisor_raw)

            if earlier_divisor_count <= winner_divisor_count:
                raise RuntimeError(
                    "winner is not the leftmost carrier of the minimal divisor class"
                )

            earlier_candidate_count += 1
            key = (winner_divisor_count, earlier_divisor_count)
            stats = pair_stats.get(key)
            if stats is None:
                stats = PairStats(
                    winner_divisor_count=winner_divisor_count,
                    earlier_divisor_count=earlier_divisor_count,
                    candidate_count=0,
                    theorem_eliminated_count=0,
                    unresolved_count=0,
                    exact_spoiler_count=0,
                    min_earlier_value=earlier_value,
                    min_winner_value=winner_value,
                )

            candidate_count = stats.candidate_count + 1
            theorem_eliminated_count = stats.theorem_eliminated_count
            unresolved_count = stats.unresolved_count
            exact_spoiler_pair_count = stats.exact_spoiler_count
            min_earlier_value = (
                earlier_value
                if stats.min_earlier_value is None
                else min(stats.min_earlier_value, earlier_value)
            )
            min_winner_value = (
                winner_value
                if stats.min_winner_value is None
                else min(stats.min_winner_value, winner_value)
            )

            if spoiler_bound_eliminates_candidate(
                earlier_value,
                earlier_divisor_count,
                winner_divisor_count,
            ):
                theorem_eliminated_candidate_count += 1
                theorem_eliminated_count += 1
            else:
                unresolved_candidate_count += 1
                unresolved_count += 1
                gap_has_unresolved_candidate = True
                if len(unresolved_examples) < 20:
                    unresolved_examples.append(
                        {
                            "left_prime": int(left_prime),
                            "right_prime": int(right_prime),
                            "gap": gap,
                            "winner_value": winner_value,
                            "winner_divisor_count": winner_divisor_count,
                            "earlier_value": earlier_value,
                            "earlier_divisor_count": earlier_divisor_count,
                        }
                    )

            if score_strictly_greater(
                earlier_value,
                earlier_divisor_count,
                winner_value,
                winner_divisor_count,
            ):
                exact_spoiler_count += 1
                exact_spoiler_pair_count += 1
                gap_has_counterexample = True
                if len(counterexample_examples) < 20:
                    counterexample_examples.append(
                        {
                            "left_prime": int(left_prime),
                            "right_prime": int(right_prime),
                            "gap": gap,
                            "winner_value": winner_value,
                            "winner_divisor_count": winner_divisor_count,
                            "earlier_value": earlier_value,
                            "earlier_divisor_count": earlier_divisor_count,
                        }
                    )

            pair_stats[key] = PairStats(
                winner_divisor_count=winner_divisor_count,
                earlier_divisor_count=earlier_divisor_count,
                candidate_count=candidate_count,
                theorem_eliminated_count=theorem_eliminated_count,
                unresolved_count=unresolved_count,
                exact_spoiler_count=exact_spoiler_pair_count,
                min_earlier_value=min_earlier_value,
                min_winner_value=min_winner_value,
            )

        if gap_has_counterexample:
            counterexample_gap_count += 1
        if gap_has_unresolved_candidate:
            unresolved_gap_count += 1
        else:
            theorem_eliminated_gap_count += 1

    pair_summary = [pair.to_dict() for _, pair in sorted(pair_stats.items())]
    winner_class_summary = [
        {
            "winner_divisor_count": winner_divisor_count,
            "gap_count": gap_count_for_class,
        }
        for winner_divisor_count, gap_count_for_class in sorted(winner_class_counts.items())
    ]

    return {
        "interval": {"lo": lo, "hi": hi},
        "decision_surface": (
            "Earlier spoilers are the only unresolved universal step once the "
            "ordered-dominance theorem has eliminated all later candidates."
        ),
        "gap_count": gap_count,
        "gap_with_earlier_candidates_count": gap_with_earlier_candidates_count,
        "theorem_eliminated_gap_count": theorem_eliminated_gap_count,
        "unresolved_gap_count": unresolved_gap_count,
        "counterexample_gap_count": counterexample_gap_count,
        "earlier_candidate_count": earlier_candidate_count,
        "theorem_eliminated_candidate_count": theorem_eliminated_candidate_count,
        "unresolved_candidate_count": unresolved_candidate_count,
        "exact_spoiler_count": exact_spoiler_count,
        "winner_class_summary": winner_class_summary,
        "pair_summary": pair_summary,
        "unresolved_examples": unresolved_examples,
        "counterexample_examples": counterexample_examples,
    }


def main(argv: list[str] | None = None) -> int:
    """Run the earlier-spoiler exact scan."""
    args = build_parser().parse_args(argv)
    payload = analyze_interval(args.lo, args.hi)

    if args.output is not None:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    json.dump(payload, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
