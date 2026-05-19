#!/usr/bin/env python3
"""Shared public policy for adaptive alphabet sparse-window experiments.

This module contains only public constants and public ranking functions. It
does not know benchmark factors or audit targets.
"""

from __future__ import annotations

import time
from typing import Any

PUBLIC_THREAD_PREFIXES: tuple[tuple[int, ...], ...] = (
    (2, 3, 5),
    (2, 3, 5, 7),
    (2, 3, 5, 7, 11),
    (2, 3, 5, 7, 11, 13),
    (2, 3, 5, 7, 11, 13, 17),
    (2, 3, 5, 7, 11, 13, 17, 19),
    (2, 3, 5, 7, 11, 13, 17, 19, 23),
    (2, 3, 5, 7, 11, 13, 17, 19, 23, 29),
)
PUBLIC_RADII: tuple[int, ...] = (
    1 << 8,
    1 << 10,
    1 << 12,
    1 << 14,
    1 << 16,
    1 << 18,
    1 << 20,
    1 << 21,
)
PUBLIC_TOP_K: int = 1000


def congruent_offsets(n: int, thread: int, radius: int) -> list[int]:
    res = (-n) % thread
    first = res if res != 0 else thread
    offsets: list[int] = []

    t = first
    while t <= radius:
        offsets.append(t)
        t += thread

    t = first - thread
    while t >= -radius:
        if t != 0:
            offsets.append(t)
        t -= thread

    return offsets


def signature_surface(n: int, radius: int, threads: tuple[int, ...]) -> tuple[dict[int, list[int]], int]:
    hit_threads: dict[int, list[int]] = {}
    generator_steps = 0
    for thread in threads:
        for offset in congruent_offsets(n, thread, radius):
            generator_steps += 1
            value = n + offset
            if value < 4:
                continue
            hit_threads.setdefault(offset, []).append(thread)
    return hit_threads, generator_steps


def signature_counts(hit_threads: dict[int, list[int]]) -> dict[tuple[int, ...], int]:
    counts: dict[tuple[int, ...], int] = {}
    for threads_hit in hit_threads.values():
        signature = tuple(threads_hit)
        counts[signature] = counts.get(signature, 0) + 1
    return counts


def ranking_key(offset: int, threads_hit: list[int], counts: dict[tuple[int, ...], int]) -> tuple[int, int, int, int, int]:
    signature = tuple(threads_hit)
    return (
        -len(signature),
        counts[signature],
        -sum(signature),
        abs(offset),
        offset,
    )


def ranked_offsets_at_rung(n: int, radius: int, threads: tuple[int, ...], top_k: int | None) -> dict[str, Any]:
    started = time.perf_counter()
    hit_threads, generator_steps = signature_surface(n, radius, threads)
    counts = signature_counts(hit_threads)

    ranked = []
    for offset, threads_hit in hit_threads.items():
        signature = tuple(threads_hit)
        ranked.append({
            "offset": offset,
            "value": n + offset,
            "threads": list(signature),
            "support_count": len(signature),
            "signature_count": counts[signature],
            "signature_weight": sum(signature),
        })

    ranked.sort(key=lambda item: ranking_key(item["offset"], item["threads"], counts))
    emitted = ranked if top_k is None else ranked[:top_k]
    elapsed = time.perf_counter() - started

    return {
        "R": radius,
        "threads": list(threads),
        "thread_count": len(threads),
        "top_nominated": emitted,
        "nominated_count": len(ranked),
        "cost": {
            "generator_steps": generator_steps,
            "unique_nominated_within_R": len(ranked),
            "signature_count": len(counts),
            "top_k_emitted": len(emitted),
            "elapsed_seconds": round(elapsed, 6),
        },
    }
