#!/usr/bin/env python3
"""Public policy engine for the true triangulation iteration loop.

The policy receives only N and one public iteration spec. It extracts cheap
public threads from composites around N, projects those threads across the
window, and ranks absolute distances by two-sided thread-vote triangulation.
"""

from __future__ import annotations

import json
import time
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


def load_spec(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def cheap_threads(value: int, small_primes: list[int], residual_limit: int) -> list[int]:
    remaining = value
    threads: list[int] = []
    for prime in small_primes:
        if remaining % prime != 0:
            continue
        threads.append(prime)
        while remaining % prime == 0:
            remaining //= prime
    if 1 < remaining <= residual_limit:
        threads.append(remaining)
    return threads


def source_rows(n: int, radius: int, small_primes: list[int], residual_limit: int) -> list[dict[str, Any]]:
    rows = []
    for offset in range(-radius, radius + 1):
        if offset == 0:
            continue
        value = n + offset
        if value < 4:
            continue
        threads = cheap_threads(value, small_primes, residual_limit)
        if not threads:
            continue
        rows.append({
            "offset": offset,
            "value": value,
            "threads": threads,
        })
    return rows


def project_votes(rows: list[dict[str, Any]], radius: int) -> dict[int, dict[int, int]]:
    thread_counts: Counter[int] = Counter()
    for row in rows:
        for thread in row["threads"]:
            thread_counts[thread] += 1

    votes: dict[int, dict[int, int]] = defaultdict(dict)
    for thread, count in thread_counts.items():
        if thread <= 0 or thread > 2 * radius:
            continue
        residue = None
        for row in rows:
            if thread in row["threads"]:
                residue = row["offset"] % thread
                break
        if residue is None:
            continue
        start = -radius + ((residue + radius) % thread)
        for target in range(start, radius + 1, thread):
            if target == 0:
                continue
            votes[target][thread] = count
    return votes


def distance_scores(
    votes: dict[int, dict[int, int]],
    radius: int,
    mode: str,
    top_k: int,
    band_width: int = 0,
    top_per_band: int = 0,
) -> list[dict[str, Any]]:
    ranked = []
    for distance in range(1, radius + 1):
        left_votes = votes.get(-distance, {})
        right_votes = votes.get(distance, {})
        left_source_count = sum(left_votes.values())
        right_source_count = sum(right_votes.values())
        left_threads = set(left_votes)
        right_threads = set(right_votes)
        shared_threads = left_threads & right_threads
        union_threads = left_threads | right_threads

        if mode == "balanced_sources":
            score = (
                min(left_source_count, right_source_count),
                left_source_count + right_source_count,
                len(shared_threads),
                len(union_threads),
                -distance,
            )
        elif mode == "shared_thread_first":
            score = (
                len(shared_threads),
                min(left_source_count, right_source_count),
                left_source_count + right_source_count,
                len(union_threads),
                -distance,
            )
        elif mode == "union_thread_first":
            score = (
                len(union_threads),
                min(left_source_count, right_source_count),
                left_source_count + right_source_count,
                -distance,
            )
        elif mode == "rare_thread_balance":
            left_rarity = sum(1_000_000 // max(1, count) for count in left_votes.values())
            right_rarity = sum(1_000_000 // max(1, count) for count in right_votes.values())
            shared_rarity = sum(
                1_000_000 // max(1, min(left_votes[thread], right_votes[thread]))
                for thread in shared_threads
            )
            score = (
                min(left_rarity, right_rarity),
                left_rarity + right_rarity,
                shared_rarity,
                len(union_threads),
                -distance,
            )
        elif mode == "rare_per_distance":
            left_rarity = sum(1_000_000 // max(1, count) for count in left_votes.values())
            right_rarity = sum(1_000_000 // max(1, count) for count in right_votes.values())
            shared_rarity = sum(
                1_000_000 // max(1, min(left_votes[thread], right_votes[thread]))
                for thread in shared_threads
            )
            balanced = min(left_rarity, right_rarity)
            score = (
                (balanced * 1000) // distance,
                (shared_rarity * 1000) // distance,
                balanced,
                len(shared_threads),
                len(union_threads),
                -distance,
            )
        elif mode == "anchor_confirmed":
            left_rarity = sum(1_000_000 // max(1, count) for count in left_votes.values())
            right_rarity = sum(1_000_000 // max(1, count) for count in right_votes.values())
            shared_rarity = sum(
                1_000_000 // max(1, min(left_votes[thread], right_votes[thread]))
                for thread in shared_threads
            )
            anchor = max(left_rarity, right_rarity)
            confirm = 1 if shared_threads else 0
            score = (
                confirm,
                (anchor * 1000) // distance,
                (shared_rarity * 1000) // distance,
                max(len(left_threads), len(right_threads)),
                len(shared_threads),
                -distance,
            )
        else:
            score = (
                min(left_source_count, right_source_count),
                len(shared_threads),
                len(union_threads),
                -distance,
            )

        ranked.append({
            "distance": distance,
            "score": list(score),
            "left_vote_count": len(left_votes),
            "right_vote_count": len(right_votes),
            "left_source_count": left_source_count,
            "right_source_count": right_source_count,
            "left_thread_count": len(left_threads),
            "right_thread_count": len(right_threads),
            "shared_thread_count": len(shared_threads),
            "union_thread_count": len(union_threads),
            "sample_left_threads": sorted(left_threads)[:16],
            "sample_right_threads": sorted(right_threads)[:16],
            "sample_shared_threads": sorted(shared_threads)[:16],
        })

    ranked.sort(key=lambda row: tuple(row["score"]), reverse=True)
    if band_width <= 0 or top_per_band <= 0:
        return ranked[:top_k]

    by_band: dict[int, list[dict[str, Any]]] = defaultdict(list)
    for row in ranked:
        band = (row["distance"] - 1) // band_width
        if len(by_band[band]) < top_per_band:
            by_band[band].append(row)

    banded = []
    for band in sorted(by_band):
        banded.extend(by_band[band])
    banded.sort(key=lambda row: tuple(row["score"]), reverse=True)
    return banded[:top_k]


def public_nominate(n: int, spec: dict[str, Any]) -> dict[str, Any]:
    started = time.perf_counter()
    radius = int(spec["radius"])
    small_primes = [int(v) for v in spec["small_primes"]]
    residual_limit = int(spec["residual_limit"])
    top_k = int(spec["top_k"])
    band_width = int(spec.get("band_width", 0))
    top_per_band = int(spec.get("top_per_band", 0))
    mode = str(spec["score_mode"])

    rows = source_rows(n, radius, small_primes, residual_limit)
    votes = project_votes(rows, radius)
    top_distances = distance_scores(votes, radius, mode, top_k, band_width, top_per_band)
    elapsed = time.perf_counter() - started

    return {
        "policy": "true_triangulation_loop",
        "iteration": int(spec["iteration"]),
        "N": n,
        "N_bits": n.bit_length(),
        "radius": radius,
        "small_primes": small_primes,
        "residual_limit": residual_limit,
        "score_mode": mode,
        "band_width": band_width,
        "top_per_band": top_per_band,
        "top_k": top_k,
        "top_distances": top_distances,
        "public_cost": {
            "source_rows": len(rows),
            "vote_targets": len(votes),
            "elapsed_seconds": round(elapsed, 6),
        },
        "public_only": True,
    }
