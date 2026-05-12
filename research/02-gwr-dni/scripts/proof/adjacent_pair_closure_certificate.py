#!/usr/bin/env python3
"""Emit the adjacent-pair closure certificate for reviewer-cited rows."""

from __future__ import annotations

import argparse
import importlib.util
import json
import math
import sys
from pathlib import Path

import gmpy2


ROOT = Path(__file__).resolve().parents[4]
SOURCE_DIR = ROOT / "src" / "python"
if str(SOURCE_DIR) not in sys.path:
    sys.path.insert(0, str(SOURCE_DIR))

from z_band_prime_composite_field import divisor_counts_segment


LARGE_PRIME_REDUCER_PATH = ROOT / "research" / "02-gwr-dni" / "scripts" / "proof" / "large_prime_reducer.py"
DEFAULT_PRIME_THRESHOLD = 5_000_000_000
DEFAULT_REVIEWER_PAIRS = ((36, 37), (64, 65), (72, 73))


def load_large_prime_reducer():
    """Load the existing minimal-divisor-count helper."""
    spec = importlib.util.spec_from_file_location(
        "adjacent_pair_closure_large_prime_reducer",
        LARGE_PRIME_REDUCER_PATH,
    )
    if spec is None or spec.loader is None:
        raise RuntimeError(f"unable to load {LARGE_PRIME_REDUCER_PATH}")
    module = importlib.util.module_from_spec(spec)
    sys.modules["adjacent_pair_closure_large_prime_reducer"] = module
    spec.loader.exec_module(module)
    return module


LARGE_PRIME_REDUCER = load_large_prime_reducer()


def build_parser() -> argparse.ArgumentParser:
    """Build the CLI parser."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--prime-threshold",
        type=int,
        default=DEFAULT_PRIME_THRESHOLD,
        help="Finite-base left-prime ceiling already closed exactly.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Optional JSON output path.",
    )
    return parser


def primes_up_to(limit: int) -> list[int]:
    """Return every prime up to `limit`."""
    if limit < 2:
        return []
    sieve = bytearray(b"\x01") * (limit + 1)
    sieve[:2] = b"\x00\x00"
    root = int(limit**0.5)
    for prime in range(2, root + 1):
        if sieve[prime]:
            start = prime * prime
            sieve[start : limit + 1 : prime] = b"\x00" * (((limit - start) // prime) + 1)
    return [value for value, is_prime in enumerate(sieve) if is_prime]


def exponent_patterns(divisor_count: int) -> list[tuple[int, ...]]:
    """Return canonical exponent patterns for integers with `divisor_count` divisors."""
    patterns: set[tuple[int, ...]] = set()

    def search(remaining: int, least_factor: int, factors: list[int]) -> None:
        if remaining == 1:
            patterns.add(tuple(sorted((factor - 1 for factor in factors), reverse=True)))
            return
        for factor in range(least_factor, remaining + 1):
            if remaining % factor == 0:
                search(remaining // factor, factor, [*factors, factor])

    search(divisor_count, 2, [])
    return sorted(patterns, reverse=True)


def enumerate_values_with_tau(divisor_count: int, limit: int) -> list[int]:
    """Enumerate every value below `limit` with exactly `divisor_count` divisors."""
    patterns = exponent_patterns(divisor_count)
    max_prime = max(int(limit ** (1.0 / min(pattern))) + 10 for pattern in patterns)
    primes = primes_up_to(max_prime)
    values: set[int] = set()

    def extend(pattern: tuple[int, ...], start_index: int, current: int) -> None:
        if not pattern:
            values.add(current)
            return
        exponent = pattern[0]
        for index in range(start_index, len(primes)):
            prime = primes[index]
            candidate = current * (prime**exponent)
            if candidate >= limit:
                break
            extend(pattern[1:], index + 1, candidate)

    for pattern in patterns:
        extend(pattern, 0, 1)

    return sorted(values)


def ratio_rows(prime_threshold: int) -> list[dict[str, int | float | bool]]:
    """Return the large-prime ratio rows for the reviewer-cited pairs."""
    alpha = LARGE_PRIME_REDUCER.large_prime_factor(prime_threshold)
    rows: list[dict[str, int | float | bool]] = []
    for winner_divisor_count, earlier_divisor_count in DEFAULT_REVIEWER_PAIRS:
        minimal_earlier_value = LARGE_PRIME_REDUCER.min_n_with_tau(earlier_divisor_count)
        ratio_threshold = alpha ** (earlier_divisor_count - 3)
        rows.append(
            {
                "winner_divisor_count": winner_divisor_count,
                "earlier_divisor_count": earlier_divisor_count,
                "minimal_earlier_value": minimal_earlier_value,
                "ratio_threshold": ratio_threshold,
                "eliminated": minimal_earlier_value > ratio_threshold,
                "bertrand_threshold": 2 ** (winner_divisor_count - 2),
            }
        )
    return rows


def pair_64_65_enumeration(prime_threshold: int) -> dict[str, object]:
    """Return the exact carrier enumeration for the `(64,65)` branch."""
    winner_divisor_count = 64
    earlier_divisor_count = 65
    bertrand_threshold = 2 ** (winner_divisor_count - 2)
    value_limit = 2 * bertrand_threshold
    carriers = enumerate_values_with_tau(earlier_divisor_count, value_limit)

    values_in_window = 0
    realized_winner_count = 0
    realized_pair_count = 0
    worst_margin: float | None = None

    for earlier_value in carriers:
        left_prime = int(gmpy2.prev_prime(earlier_value))
        if left_prime <= prime_threshold or left_prime > bertrand_threshold:
            continue
        values_in_window += 1
        right_prime = int(gmpy2.next_prime(earlier_value))
        gap_divisors = divisor_counts_segment(left_prime + 1, right_prime)
        gap_min = int(gap_divisors.min())
        first_min_index = int((gap_divisors == gap_min).nonzero()[0][0])
        winner_value = left_prime + 1 + first_min_index
        if gap_min != winner_divisor_count:
            continue
        realized_winner_count += 1
        if earlier_value < winner_value:
            realized_pair_count += 1
            margin = (
                (earlier_divisor_count - 2) * math.log(earlier_value)
                - (winner_divisor_count - 2) * math.log(winner_value)
            )
            worst_margin = margin if worst_margin is None else min(worst_margin, margin)

    return {
        "winner_divisor_count": winner_divisor_count,
        "earlier_divisor_count": earlier_divisor_count,
        "bertrand_threshold": bertrand_threshold,
        "value_limit": value_limit,
        "exponent_patterns": [list(pattern) for pattern in exponent_patterns(earlier_divisor_count)],
        "carrier_count_below_value_limit": len(carriers),
        "carriers_in_unresolved_prime_window": values_in_window,
        "realized_winner_count": realized_winner_count,
        "realized_pair_count": realized_pair_count,
        "worst_log_margin": worst_margin,
    }


def build_payload(prime_threshold: int) -> dict[str, object]:
    """Return the adjacent-pair closure certificate payload."""
    alpha = LARGE_PRIME_REDUCER.large_prime_factor(prime_threshold)
    return {
        "prime_threshold": prime_threshold,
        "alpha": alpha,
        "large_prime_ratio_rule": (
            "For p above the finite base, q/p < alpha. If M(e) > alpha^(e-3), "
            "then every earlier divisor class e beats no later winner divisor class d<e."
        ),
        "reviewer_pair_rows": ratio_rows(prime_threshold),
        "pair_64_65_exact_enumeration": pair_64_65_enumeration(prime_threshold),
    }


def main(argv: list[str] | None = None) -> int:
    """Run the certificate and emit JSON."""
    args = build_parser().parse_args(argv)
    payload = build_payload(args.prime_threshold)
    serialized = json.dumps(payload, indent=2)
    if args.output is not None:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(serialized + "\n", encoding="utf-8")
    print(serialized)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
