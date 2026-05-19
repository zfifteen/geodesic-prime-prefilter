#!/usr/bin/env python3
"""Public scale runner for anchor-confirmed band triangulation.

The public surface receives only N. The radius rule is public and depends only
on N.bit_length(). No private endpoint values are present in this file.
"""

from __future__ import annotations

import argparse
import gzip
import json
import time
from collections import defaultdict
from fractions import Fraction
from heapq import heappush, heapreplace
from pathlib import Path
from typing import Any

SMALL_PRIMES = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29)
RESIDUAL_LIMIT = 1
BAND_WIDTH_RATIO = Fraction(1, 64)
DEFAULT_CAP_RATIO = Fraction(1, 8)


def public_radius(n: int) -> int:
    return 1 << ((n.bit_length() + 1) // 2)


def parse_ratio(value: str) -> Fraction:
    ratio = Fraction(value)
    if ratio <= 0 or ratio > 1:
        raise ValueError("ratio must be in the interval (0, 1]")
    return ratio


def public_band_width(radius: int) -> int:
    width = (radius * BAND_WIDTH_RATIO.numerator + BAND_WIDTH_RATIO.denominator - 1) // BAND_WIDTH_RATIO.denominator
    return max(1, width)


def public_top_per_band(band_width: int, cap_ratio: Fraction) -> int:
    return max(1, (band_width * cap_ratio.numerator + cap_ratio.denominator - 1) // cap_ratio.denominator)


def congruent_count(low: int, high: int, residue: int, modulus: int) -> int:
    first = low + ((residue - low) % modulus)
    if first > high:
        return 0
    return ((high - first) // modulus) + 1


def public_thread_counts(n: int, radius: int) -> dict[int, int]:
    counts: dict[int, int] = {}
    for thread in SMALL_PRIMES:
        residue = (-n) % thread
        count = congruent_count(-radius, radius, residue, thread)
        if residue == 0:
            count -= 1
        if count > 0:
            counts[thread] = count
    return counts


def score_distance(n: int, distance: int, counts: dict[int, int]) -> dict[str, Any]:
    left_threads = []
    right_threads = []
    for thread, count in counts.items():
        residue = (-n) % thread
        if (-distance) % thread == residue:
            left_threads.append((thread, count))
        if distance % thread == residue:
            right_threads.append((thread, count))

    left_set = {thread for thread, _ in left_threads}
    right_set = {thread for thread, _ in right_threads}
    shared = left_set & right_set
    union = left_set | right_set
    left_rarity = sum(1_000_000 // count for _, count in left_threads)
    right_rarity = sum(1_000_000 // count for _, count in right_threads)
    shared_rarity = sum(1_000_000 // min(counts[thread], counts[thread]) for thread in shared)
    anchor = max(left_rarity, right_rarity)
    confirm = 1 if shared else 0
    score = (
        confirm,
        (anchor * 1000) // distance,
        (shared_rarity * 1000) // distance,
        max(len(left_set), len(right_set)),
        len(shared),
        -distance,
    )
    return {
        "distance": distance,
        "score": list(score),
        "left_source_count": sum(count for _, count in left_threads),
        "right_source_count": sum(count for _, count in right_threads),
        "left_thread_count": len(left_set),
        "right_thread_count": len(right_set),
        "shared_thread_count": len(shared),
        "union_thread_count": len(union),
        "sample_left_threads": sorted(left_set),
        "sample_right_threads": sorted(right_set),
        "sample_shared_threads": sorted(shared),
    }


def public_nominate_scaled(n: int, cap_ratio: Fraction = DEFAULT_CAP_RATIO) -> dict[str, Any]:
    started = time.perf_counter()
    radius = public_radius(n)
    band_width = public_band_width(radius)
    top_per_band = public_top_per_band(band_width, cap_ratio)
    counts = public_thread_counts(n, radius)
    heaps: dict[int, list[tuple[tuple[int, ...], dict[str, Any]]]] = defaultdict(list)

    for distance in range(1, radius + 1):
        row = score_distance(n, distance, counts)
        band = (distance - 1) // band_width
        key = tuple(row["score"])
        heap_row = (key, row)
        heap = heaps[band]
        if len(heap) < top_per_band:
            heappush(heap, heap_row)
        elif key > heap[0][0]:
            heapreplace(heap, heap_row)

    elapsed = time.perf_counter() - started
    return {
        "policy": "anchor_confirmed_band_scale",
        "N": n,
        "N_bits": n.bit_length(),
        "radius": radius,
        "small_primes": list(SMALL_PRIMES),
        "residual_limit": RESIDUAL_LIMIT,
        "score_mode": "anchor_confirmed",
        "band_width_ratio": f"{BAND_WIDTH_RATIO.numerator}/{BAND_WIDTH_RATIO.denominator}",
        "band_width": band_width,
        "cap_ratio": f"{cap_ratio.numerator}/{cap_ratio.denominator}",
        "top_per_band": top_per_band,
        "thread_counts": counts,
        "band_rows": {
            str(band): [row for _, row in sorted(heap, key=lambda item: item[0], reverse=True)]
            for band, heap in sorted(heaps.items())
        },
        "public_cost": {
            "scored_distances": radius,
            "band_count": len(heaps),
            "elapsed_seconds": round(elapsed, 6),
        },
        "public_only": True,
    }


def write_public_result(n: int, out_dir: Path, cap_ratio: Fraction = DEFAULT_CAP_RATIO) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    result = public_nominate_scaled(n, cap_ratio)
    manifest = {key: value for key, value in result.items() if key != "band_rows"}
    selected_count = sum(len(rows) for rows in result["band_rows"].values())
    manifest["selected_band_rows"] = selected_count
    (out_dir / "public_manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    with gzip.open(out_dir / "public_band_rows.jsonl.gz", "wt", encoding="utf-8", newline="\n") as handle:
        for band, rows in result["band_rows"].items():
            for rank, row in enumerate(rows, start=1):
                handle.write(json.dumps({"band": int(band), "band_rank": rank, **row}, sort_keys=True) + "\n")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--n", type=int, required=True)
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--cap-ratio", default=str(DEFAULT_CAP_RATIO))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.n < 4:
        raise SystemExit("--n must be at least 4")
    write_public_result(args.n, args.out_dir, parse_ratio(args.cap_ratio))


if __name__ == "__main__":
    main()
