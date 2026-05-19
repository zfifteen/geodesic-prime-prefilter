#!/usr/bin/env python3
"""Private 64-bit audit for the frozen ratio web formula."""

from __future__ import annotations

import json
import time
from fractions import Fraction
from pathlib import Path
from typing import Any

import numpy as np

HERE = Path(__file__).resolve().parent
OUT_ROOT = HERE / "output" / "audit_anchor_band_64bit"

SMALL_PRIMES = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29)
BAND_WIDTH_RATIO = Fraction(1, 64)
CAP_RATIO = Fraction(1, 2)
CHUNK_SIZE = 1_000_000

CASE = {
    "name": "scale_64bit_2147547791x4294902979",
    "p": 2147547791,
    "q": 4294902979,
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
        if (-distance) % thread == residue:
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


def count_better_in_band(n_value: int, distance: int, radius: int, band_width: int, counts: dict[int, int]) -> dict[str, Any]:
    band = (distance - 1) // band_width
    low = band * band_width + 1
    high = min(radius, (band + 1) * band_width)
    target = scalar_score(n_value, distance, counts)
    better = 0

    for start in range(low, high + 1, CHUNK_SIZE):
        stop = min(high, start + CHUNK_SIZE - 1)
        values = np.arange(start, stop + 1, dtype=np.int64)
        left_rarity = np.zeros(values.shape, dtype=np.int64)
        right_rarity = np.zeros(values.shape, dtype=np.int64)
        shared_rarity = np.zeros(values.shape, dtype=np.int64)
        left_count = np.zeros(values.shape, dtype=np.int16)
        right_count = np.zeros(values.shape, dtype=np.int16)
        shared_count = np.zeros(values.shape, dtype=np.int16)

        for thread, count in counts.items():
            residue = (-n_value) % thread
            weight = 1_000_000 // count
            current = values % thread
            left = ((-current) % thread) == residue
            right = current == residue
            shared = left & right
            left_count += left
            right_count += right
            shared_count += shared
            if weight:
                left_rarity += left.astype(np.int64) * weight
                right_rarity += right.astype(np.int64) * weight
                shared_rarity += shared.astype(np.int64) * weight

        confirm = shared_count > 0
        anchor = np.maximum(left_rarity, right_rarity)
        anchor_part = (anchor * 1000) // values
        shared_part = (shared_rarity * 1000) // values
        max_threads = np.maximum(left_count, right_count)

        mask = confirm.astype(np.int16) > target[0]
        mask |= (confirm.astype(np.int16) == target[0]) & (anchor_part > target[1])
        mask |= (confirm.astype(np.int16) == target[0]) & (anchor_part == target[1]) & (shared_part > target[2])
        mask |= (
            (confirm.astype(np.int16) == target[0])
            & (anchor_part == target[1])
            & (shared_part == target[2])
            & (max_threads > target[3])
        )
        mask |= (
            (confirm.astype(np.int16) == target[0])
            & (anchor_part == target[1])
            & (shared_part == target[2])
            & (max_threads == target[3])
            & (shared_count > target[4])
        )
        mask |= (
            (confirm.astype(np.int16) == target[0])
            & (anchor_part == target[1])
            & (shared_part == target[2])
            & (max_threads == target[3])
            & (shared_count == target[4])
            & (values < distance)
        )
        better += int(mask.sum())

    return {
        "distance": distance,
        "band": band,
        "band_low": low,
        "band_high": high,
        "score": list(target),
        "band_rank": better + 1,
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
    p_rank = count_better_in_band(n_value, p_value, radius, band_width, counts)
    q_rank = count_better_in_band(n_value, q_value, radius, band_width, counts)
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
        "# Anchor-Confirmed 64-Bit Ratio Audit",
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
