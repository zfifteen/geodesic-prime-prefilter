#!/usr/bin/env python3
"""
Rich Literal Multiplicative Web Reducer (Research Version)

Goal: Maximum search-space reduction for semiprime factor distances
by building a rich, literal web of real factor threads from numbers
around N.

Constraints for this phase:
- N ≤ 48 bits
- Public-only during web construction (we factor nearby numbers but
  do not use knowledge of p or q to guide factoring or scoring)
- Focus is reduction, not speed or scalability (yet)

This is an experimental, aggressive version meant to test how much
reduction is possible when we stop being cheap.
"""

from __future__ import annotations

import argparse
import json
import math
import time
from pathlib import Path
from collections import defaultdict
import sympy


def public_radius(n: int) -> int:
    """Rough public search radius (odd distances up to ~sqrt(N))."""
    return (1 << ((n.bit_length() + 1) // 2))


def original_space_size(n: int) -> int:
    r = public_radius(n)
    return (r + 1) // 2   # count of odd positive distances <= r


def factor_window(n: int, radius: int) -> dict[int, dict[int, int]]:
    """
    Factor every integer in [n-radius, n+radius] except N itself.
    Returns {value: factor_dict}
    """
    factors = {}
    start = max(2, n - radius)
    end = n + radius
    for val in range(start, end + 1):
        if val == n:
            continue
        try:
            fac = sympy.factorint(val)
            if fac:
                factors[val] = fac
        except Exception:
            continue
    return factors


def extract_threads(factor_dicts: dict[int, dict[int, int]]) -> set[int]:
    """Collect all unique prime factors seen in the window."""
    threads: set[int] = set()
    for facs in factor_dicts.values():
        threads.update(facs.keys())
    return threads


def score_distance(n: int, d: int, threads: set[int]) -> int:
    """
    Count how many threads 'support' this distance.
    A thread f supports d if d ≡ N (mod f) or d ≡ -N (mod f).
    """
    support = 0
    n_mod = n
    neg_n_mod = (-n) % d if d else 0   # not used directly
    for f in threads:
        if f == 0:
            continue
        try:
            if d % f == n_mod % f:
                support += 1
            elif d % f == ((-n) % f):
                support += 1
        except ZeroDivisionError:
            continue
    return support


def compute_all_scores(n: int, threads: set[int], radius: int) -> list[tuple[int, int]]:
    """
    Score every odd positive distance <= radius.
    Returns list of (support, distance) sorted best-first.
    """
    scores = []
    for d in range(1, radius + 1, 2):   # only odd distances
        sup = score_distance(n, d, threads)
        scores.append((sup, d))
    scores.sort(reverse=True)   # highest support first
    return scores


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, required=True)
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--radius", type=int, default=None,
                        help="Optional explicit radius. If not given, uses public_radius(N)")
    parser.add_argument("--max-candidates", type=int, default=128,
                        help="How many top distances to keep after scoring")
    args = parser.parse_args()

    n = args.n
    if n.bit_length() > 48:
        print("ERROR: This rich reducer is currently limited to ≤48-bit N.")
        return

    radius = args.radius or public_radius(n)
    out_dir = args.out_dir
    out_dir.mkdir(parents=True, exist_ok=True)

    started = time.perf_counter()

    print(f"[*] Factoring window around N={n} (radius={radius}) ...")
    window_factors = factor_window(n, radius)
    threads = extract_threads(window_factors)
    print(f"[*] Found {len(threads)} unique prime threads from the window.")

    print("[*] Scoring all odd distances...")
    scored = compute_all_scores(n, threads, radius)

    # Keep top K
    top_k = scored[:args.max_candidates]

    # Build output
    rows = []
    for rank, (support, dist) in enumerate(top_k, 1):
        rows.append({
            "rank": rank,
            "distance": dist,
            "support": support,
            "score": [support, -dist]
        })

    orig_size = original_space_size(n)
    emitted = len(rows)
    reduction_ratio = f"{orig_size}/{emitted}" if emitted else None
    reduction_bits = math.log2(orig_size) - math.log2(emitted) if emitted else None

    manifest = {
        "N": n,
        "N_bits": n.bit_length(),
        "radius": radius,
        "threads_found": len(threads),
        "original_space_size": orig_size,
        "emitted_count": emitted,
        "candidate_reduction_ratio": reduction_ratio,
        "candidate_reduction_bits": reduction_bits,
        "max_candidates": args.max_candidates,
        "elapsed_seconds": round(time.perf_counter() - started, 3),
        "mode": "rich_literal_web"
    }

    # Write outputs
    (out_dir / "public_output.jsonl").write_text(
        "\n".join(json.dumps(r, sort_keys=True) for r in rows) + "\n",
        encoding="utf-8"
    )
    (out_dir / "public_manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8"
    )

    print("=== RICH LITERAL WEB REDUCER ===")
    print(f"N = {n}")
    print(f"Original space size: {orig_size}")
    print(f"Emitted candidates:  {emitted}")
    print(f"Reduction:           {reduction_ratio}  (~{reduction_bits:.2f} bits)")
    print(f"Output written to:   {out_dir}")


if __name__ == "__main__":
    main()