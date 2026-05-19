#!/usr/bin/env python3
"""Public triangulation policy for multiplicative-web distance nomination.

This module contains no benchmark factors. It receives only N and public policy
constants, observes public small-thread hits around N, and ranks absolute
distances by left/right thread triangulation.
"""

from __future__ import annotations

import time
from heapq import heappush, heapreplace
from typing import Any

THREAD_PREFIXES: tuple[tuple[int, ...], ...] = (
    (2, 3, 5),
    (2, 3, 5),
    (2, 3, 5, 7),
    (2, 3, 5, 7),
    (2, 3, 5, 7, 11),
    (2, 3, 5, 7, 11, 13),
    (2, 3, 5, 7, 11, 13, 17),
    (2, 3, 5, 7, 11, 13, 17, 19),
    (2, 3, 5, 7, 11, 13, 17, 19, 23),
    (2, 3, 5, 7, 11, 13, 17, 19, 23, 29),
)
RADII: tuple[int, ...] = (
    256,
    1024,
    4096,
    16384,
    65536,
    262144,
    524288,
    1048576,
    1572864,
    2097152,
)
TOP_K: int = 1000


def thread_hits(value: int, threads: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(thread for thread in threads if value % thread == 0)


def triplets(count: int) -> int:
    if count < 3:
        return 0
    return count * (count - 1) * (count - 2) // 6


def distance_record(n: int, distance: int, threads: tuple[int, ...], mode: str) -> dict[str, Any]:
    left_value = n - distance
    right_value = n + distance
    if left_value < 4:
        left = ()
    else:
        left = thread_hits(left_value, threads)
    right = thread_hits(right_value, threads)
    shared = tuple(thread for thread in left if thread in set(right))
    union = tuple(sorted(set(left) | set(right)))

    left_count = len(left)
    right_count = len(right)
    shared_count = len(shared)
    union_count = len(union)
    balance = min(left_count, right_count)
    spread = left_count + right_count
    shared_weight = sum(shared)
    union_weight = sum(union)

    if mode == "balanced_triplets":
        score = (triplets(balance), balance, spread, shared_count, shared_weight, -distance)
    elif mode == "shared_threads":
        score = (shared_count, triplets(union_count), balance, spread, shared_weight, -distance)
    elif mode == "union_triplets":
        score = (triplets(union_count), balance, shared_count, union_weight, -distance)
    elif mode == "asymmetry_pressure":
        score = (balance, -abs(left_count - right_count), triplets(union_count), spread, union_weight, -distance)
    else:
        score = (balance, spread, shared_count, union_weight, -distance)

    return {
        "distance": distance,
        "left_offset": -distance,
        "right_offset": distance,
        "left_threads": list(left),
        "right_threads": list(right),
        "shared_threads": list(shared),
        "union_threads": list(union),
        "left_support": left_count,
        "right_support": right_count,
        "shared_support": shared_count,
        "union_support": union_count,
        "triangles_left": triplets(left_count),
        "triangles_right": triplets(right_count),
        "triangles_union": triplets(union_count),
        "score": list(score),
    }


def policy_mode(iteration: int) -> str:
    modes = (
        "balanced_triplets",
        "shared_threads",
        "balanced_triplets",
        "union_triplets",
        "asymmetry_pressure",
        "balanced_triplets",
        "shared_threads",
        "union_triplets",
        "asymmetry_pressure",
        "balanced_triplets",
    )
    return modes[iteration - 1]


def nominate_distances(n: int, iteration: int, top_k: int = TOP_K) -> dict[str, Any]:
    if iteration < 1 or iteration > 10:
        raise ValueError("iteration must be in 1..10")
    if n < 4:
        raise ValueError("N must be >= 4")

    radius = RADII[iteration - 1]
    threads = THREAD_PREFIXES[iteration - 1]
    mode = policy_mode(iteration)
    started = time.perf_counter()
    heap: list[tuple[tuple[int, ...], int, dict[str, Any]]] = []
    for distance in range(1, radius + 1):
        row = distance_record(n, distance, threads, mode)
        score = tuple(row["score"])
        if len(heap) < top_k:
            heappush(heap, (score, distance, row))
        elif score > heap[0][0]:
            heapreplace(heap, (score, distance, row))
    rows = [item[2] for item in heap]
    rows.sort(key=lambda row: tuple(row["score"]), reverse=True)
    elapsed = time.perf_counter() - started

    return {
        "policy": "triangulated_distance_v1",
        "iteration": iteration,
        "mode": mode,
        "N": n,
        "N_bits": n.bit_length(),
        "R": radius,
        "threads": list(threads),
        "thread_count": len(threads),
        "top_k": top_k,
        "top_distances": rows[:top_k],
        "distance_count": len(rows),
        "cost": {
            "distances_scored": len(rows),
            "thread_division_checks": len(rows) * len(threads) * 2,
            "elapsed_seconds": round(elapsed, 6),
        },
        "public_only": True,
    }
