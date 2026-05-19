#!/usr/bin/env python3
"""Private 128-bit audit for the frozen ratio web formula."""

from __future__ import annotations

import json
import math
import time
from fractions import Fraction
from itertools import combinations
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
OUT_ROOT = HERE / "output" / "audit_anchor_band_128bit"

SMALL_PRIMES = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29)
ODD_PRIMES = SMALL_PRIMES[1:]
BAND_WIDTH_RATIO = Fraction(1, 64)
CAP_RATIO = Fraction(1, 2)

CASE = {
    "name": "scale_128bit_9223372036854903989x18446744073709423363",
    "p": 9223372036854903989,
    "q": 18446744073709423363,
}


def public_radius(n_value: int) -> int:
    return 1 << ((n_value.bit_length() + 1) // 2)


def public_band_width(radius: int) -> int:
    return max(1, (radius * BAND_WIDTH_RATIO.numerator + BAND_WIDTH_RATIO.denominator - 1) // BAND_WIDTH_RATIO.denominator)


def public_cap(band_width: int) -> int:
    return max(1, (band_width * CAP_RATIO.numerator + CAP_RATIO.denominator - 1) // CAP_RATIO.denominator)


def congruent_count(low: int, high: int, residue: int, modulus: int) -> int:
    first = low + ((residue - low) % modulus)
    if first > high:
        return 0
    return ((high - first) // modulus) + 1


def crt_pair(a_mod: int, a_residue: int, b_mod: int, b_residue: int) -> tuple[int, int]:
    inverse = pow(a_mod, -1, b_mod)
    step = ((b_residue - a_residue) * inverse) % b_mod
    modulus = a_mod * b_mod
    residue = (a_residue + a_mod * step) % modulus
    return modulus, residue


def count_constraints(low: int, high: int, constraints: tuple[tuple[int, int], ...]) -> int:
    modulus = 1
    residue = 0
    for current_modulus, current_residue in constraints:
        modulus, residue = crt_pair(modulus, residue, current_modulus, current_residue % current_modulus)
    return congruent_count(low, high, residue, modulus)


def public_thread_counts(n_value: int, radius: int) -> dict[int, int]:
    counts = {}
    for thread in SMALL_PRIMES:
        residue = (-n_value) % thread
        count = congruent_count(-radius, radius, residue, thread)
        if residue == 0:
            count -= 1
        if count > 0:
            counts[thread] = count
    return counts


def scalar_score(n_value: int, distance: int, counts: dict[int, int]) -> tuple[int, int, int, int, int, int]:
    left_threads = []
    right_threads = []
    for thread, count in counts.items():
        residue = (-n_value) % thread
        current = distance % thread
        if (-current) % thread == residue:
            left_threads.append((thread, count))
        if current == residue:
            right_threads.append((thread, count))
    left_set = {thread for thread, _ in left_threads}
    right_set = {thread for thread, _ in right_threads}
    shared = left_set & right_set
    left_rarity = sum(1_000_000 // count for _, count in left_threads)
    right_rarity = sum(1_000_000 // count for _, count in right_threads)
    shared_rarity = sum(1_000_000 // counts[thread] for thread in shared)
    anchor = max(left_rarity, right_rarity)
    confirm = 1 if shared else 0
    return (
        confirm,
        (anchor * 1000) // distance,
        (shared_rarity * 1000) // distance,
        max(len(left_set), len(right_set)),
        len(shared),
        -distance,
    )


def residue_tables(n_value: int) -> tuple[dict[int, int], dict[int, int]]:
    left_residue = {}
    right_residue = {}
    for thread in ODD_PRIMES:
        left_residue[thread] = n_value % thread
        right_residue[thread] = (-n_value) % thread
    return left_residue, right_residue


def f_table(low: int, high: int, n_value: int) -> list[list[int]]:
    left_residue, right_residue = residue_tables(n_value)
    table = [[0 for _ in range(len(ODD_PRIMES) + 1)] for _ in range(len(ODD_PRIMES) + 1)]
    states: list[tuple[int, int, tuple[tuple[int, int], ...]]] = [(0, 0, ((2, 1),))]
    for thread in ODD_PRIMES:
        next_states = []
        for left_count, right_count, constraints in states:
            next_states.append((left_count, right_count, constraints))
            next_states.append((left_count + 1, right_count, constraints + ((thread, left_residue[thread]),)))
            next_states.append((left_count, right_count + 1, constraints + ((thread, right_residue[thread]),)))
        states = next_states
    for left_count, right_count, constraints in states:
        table[left_count][right_count] += count_constraints(low, high, constraints)
    return table


def at_least_from_moments(values: list[int], threshold: int) -> int:
    if threshold <= 0:
        return values[0]
    total = 0
    for size in range(threshold, len(values)):
        total += ((-1) ** (size - threshold)) * math.comb(size - 1, threshold - 1) * values[size]
    return total


def at_least_both(table: list[list[int]], left_threshold: int, right_threshold: int) -> int:
    if left_threshold <= 0 and right_threshold <= 0:
        return table[0][0]
    total = 0
    for left_size in range(left_threshold, len(table)):
        if left_size == 0:
            left_coeff = 1
        else:
            left_coeff = ((-1) ** (left_size - left_threshold)) * math.comb(left_size - 1, left_threshold - 1)
        for right_size in range(right_threshold, len(table[left_size])):
            if right_size == 0:
                right_coeff = 1
            else:
                right_coeff = ((-1) ** (right_size - right_threshold)) * math.comb(right_size - 1, right_threshold - 1)
            total += left_coeff * right_coeff * table[left_size][right_size]
    return total


def count_max_at_least(low: int, high: int, n_value: int, odd_prime_threshold: int) -> int:
    if low > high:
        return 0
    table = f_table(low, high, n_value)
    left_moments = [table[size][0] for size in range(len(table))]
    right_moments = [table[0][size] for size in range(len(table))]
    left = at_least_from_moments(left_moments, odd_prime_threshold)
    right = at_least_from_moments(right_moments, odd_prime_threshold)
    both = at_least_both(table, odd_prime_threshold, odd_prime_threshold)
    return left + right - both


def exact_band_rank(n_value: int, distance: int, radius: int, band_width: int, counts: dict[int, int]) -> dict[str, Any]:
    band = (distance - 1) // band_width
    low = band * band_width + 1
    high = min(radius, (band + 1) * band_width)
    target = scalar_score(n_value, distance, counts)
    target_max_threads = target[3]
    better = count_max_at_least(low, high, n_value, target_max_threads)
    equal_before = count_max_at_least(low, distance - 1, n_value, target_max_threads - 1) - count_max_at_least(
        low,
        distance - 1,
        n_value,
        target_max_threads,
    )
    return {
        "distance": distance,
        "band": band,
        "band_low": low,
        "band_high": high,
        "score": list(target),
        "band_rank": better + equal_before + 1,
    }


def main() -> None:
    started = time.perf_counter()
    p_value = CASE["p"]
    q_value = CASE["q"]
    n_value = p_value * q_value
    radius = public_radius(n_value)
    band_width = public_band_width(radius)
    cap = public_cap(band_width)
    counts = public_thread_counts(n_value, radius)
    p_rank = exact_band_rank(n_value, p_value, radius, band_width, counts)
    q_rank = exact_band_rank(n_value, q_value, radius, band_width, counts)
    hits = []
    if p_rank["band_rank"] <= cap:
        hits.append({"which": "p", **p_rank})
    if q_rank["band_rank"] <= cap:
        hits.append({"which": "q", **q_rank})
    summary = {
        "status": "success" if hits else "failure",
        "case": CASE["name"],
        "N": n_value,
        "N_bits": n_value.bit_length(),
        "radius": radius,
        "band_width_ratio": f"{BAND_WIDTH_RATIO.numerator}/{BAND_WIDTH_RATIO.denominator}",
        "band_width": band_width,
        "cap_ratio": f"{CAP_RATIO.numerator}/{CAP_RATIO.denominator}",
        "top_per_band": cap,
        "thread_counts": counts,
        "p": p_value,
        "q": q_value,
        "p_rank": p_rank,
        "q_rank": q_rank,
        "hits": hits,
        "elapsed_seconds": round(time.perf_counter() - started, 6),
    }
    OUT_ROOT.mkdir(parents=True, exist_ok=True)
    (OUT_ROOT / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    lines = [
        "# Anchor-Confirmed 128-Bit Ratio Audit",
        "",
        f"Status: `{summary['status']}`",
        "",
        f"- case: `{summary['case']}`",
        f"- bits: `{summary['N_bits']}`",
        f"- radius: `{summary['radius']}`",
        f"- band width ratio: `{summary['band_width_ratio']}`",
        f"- cap ratio: `{summary['cap_ratio']}`",
        f"- top per band: `{summary['top_per_band']}`",
        f"- p band rank: `{summary['p_rank']['band_rank']}`",
        f"- q band rank: `{summary['q_rank']['band_rank']}`",
        f"- elapsed seconds: `{summary['elapsed_seconds']}`",
        "",
        "## Hit",
        "",
    ]
    for hit in hits:
        lines.append(f"- `{hit['which']}={hit['distance']}` at band rank `{hit['band_rank']}`")
    if not hits:
        lines.append("- none")
    (OUT_ROOT / "summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
