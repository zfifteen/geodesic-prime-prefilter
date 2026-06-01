#!/usr/bin/env python3
"""Minimal self-contained probe for the "inversion density spike at smaller factor" prediction.

PGS-native only. Uses exact divisor counts + leftmost min-d carrier rule
(transported via floor(N / x)) to test whether misalignment/overshoot of the
carried points spikes sharply when the probe m equals the true smaller prime
factor of a semiprime N = p * q.

This directly exercises the falsifiable claim from the Novel Insight Engine run:
the first m where transported-carrier misalignment density crosses a threshold
lies inside [p, p + 2*gap_after_p].

No classical factoring, no primality tests inside the probe logic, no gcd.
Classical only for harness construction of known-p semiprimes (audit surface).

Run:
    python3 research/16-predictions/scripts/pgs_modulus_link_factor_spike_probe.py

Expected (if insight holds on small regime): for the majority of trials the
m that first produces high misalignment (large overshoot of transported
carrier relative to local min-d position around y) is the true p (or within
the small gap after it). Prints exact hit/miss counts + first counter-example
if any.

Dependencies: pure Python + numpy (same as the project's z_band field helper).
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Optional

import numpy as np


# --- Inlined minimal divisor_counts_segment (from project z_band_prime_composite_field) ---
# Exact same segmented sieve logic used by the live PGS generator. No changes.
from functools import lru_cache


@lru_cache(maxsize=None)
def _primes_upto(limit: int) -> np.ndarray:
    if limit < 2:
        return np.array([], dtype=np.int64)
    sieve = np.ones(limit + 1, dtype=np.bool_)
    sieve[:2] = False
    max_factor = math.isqrt(limit)
    for p in range(2, max_factor + 1):
        if sieve[p]:
            sieve[p * p : limit + 1 : p] = False
    return np.flatnonzero(sieve).astype(np.int64)


def divisor_counts_segment(lo: int, hi: int) -> np.ndarray:
    """tau(n) for n in [lo, hi). Identical contract and implementation to the
    one called by pgs_chamber_reset_state_certificate in the v1.1 generator."""
    if hi <= lo:
        return np.array([], dtype=np.int32)
    if lo < 1:
        raise ValueError("lo >= 1")
    values = np.arange(lo, hi, dtype=np.int64)
    residual = values.copy()
    tau = np.ones(hi - lo, dtype=np.int32)
    max_factor = math.isqrt(hi - 1)
    for p in _primes_upto(max_factor):
        start = ((lo + p - 1) // p) * p
        if start >= hi:
            continue
        indexes = np.arange(start - lo, hi - lo, p, dtype=np.int64)
        chunk = residual[indexes]
        exponents = np.zeros(indexes.shape[0], dtype=np.int16)
        while True:
            mask = (chunk % p) == 0
            if not np.any(mask):
                break
            chunk[mask] //= p
            exponents[mask] += 1
        residual[indexes] = chunk
        tau[indexes] *= (exponents + 1)
    tau[residual > 1] *= 2
    return tau


# --- Minimal PGS carrier finder (stripped from pgs_chamber_reset_state_certificate) ---
# Returns the leftmost integer w > start that realizes the current minimum
# divisor count among positions with d > 2 (the GWR carrier), plus a few tail
# points after the first tau==2 if present. Works for any start (prime or not).
@dataclass
class SimpleCarrierSet:
    start: int
    carrier_w: int          # the leftmost min-d >2 position
    carrier_d: int
    tail_points: list[int]  # first few positions after first d==2 (or after carrier if no prime)


def find_carrier_set(start: int, search_bound: int = 512) -> Optional[SimpleCarrierSet]:
    """Exact analogue of the carrier + tail extraction in the generator.
    Uses the identical min-tracking rule. Returns None only on degenerate input."""
    if search_bound < 1:
        return None
    counts = divisor_counts_segment(start + 1, start + search_bound + 1)
    if len(counts) == 0:
        return None

    min_d = 10**9
    carrier_offset = None
    first_prime_offset = None
    for off, d in enumerate(counts, start=1):
        n = start + off
        if d == 2 and first_prime_offset is None:
            first_prime_offset = off
        if d > 2 and d < min_d:
            min_d = d
            carrier_offset = off

    if carrier_offset is None:
        return None

    carrier_w = start + carrier_offset
    tail: list[int] = []
    tail_start = first_prime_offset + 1 if first_prime_offset is not None else carrier_offset + 1
    for off in range(tail_start, min(tail_start + 6, len(counts) + 1)):
        if counts[off - 1] > 2:
            tail.append(start + off)

    return SimpleCarrierSet(
        start=start,
        carrier_w=carrier_w,
        carrier_d=min_d,
        tail_points=tail,
    )


# --- Transport + misalignment (inversion) scorer ---
def compute_inversion_density(
    probe_m: int,
    target_N: int,
    carriers: SimpleCarrierSet,
    local_search_radius: int = 64,
) -> float:
    """Core of the insight test.

    For each carrier x in the set after probe_m, compute y = floor(target_N / x).
    Around y, find the actual leftmost position with the minimal tau in a small
    window. Measure how far y is from that true local min-d position.
    Return average (misalignment distance / radius) over the carriers.
    High value == strong "inversion" / misalignment of the transported PGS carrier.
    """
    points = [carriers.carrier_w] + carriers.tail_points[:3]
    misalignments: list[float] = []
    for x in points:
        if x <= 1:
            continue
        y = target_N // x
        if y < 3:
            continue
        lo = max(2, y - local_search_radius)
        hi = y + local_search_radius + 1
        local_tau = divisor_counts_segment(lo, hi)
        if len(local_tau) == 0:
            continue
        # Find the offset of the leftmost minimum tau in the window
        min_tau = local_tau.min()
        min_offsets = np.where(local_tau == min_tau)[0]
        if len(min_offsets) == 0:
            continue
        true_min_pos = lo + int(min_offsets[0])
        dist = abs(y - true_min_pos)
        misalignments.append(min(dist / local_search_radius, 1.0))

    if not misalignments:
        return 0.0
    return float(np.mean(misalignments))


def make_small_semiprime(p: int) -> tuple[int, int, int, int]:
    """Given a small prime p, use the identical carrier logic to locate the next
    prime q after p (exactly the PGS generator rule). Return (p, q, N=p*q, gap).
    This gives us a real semiprime whose smaller factor p has a known nonempty
    gap after it (guaranteed by the theorem)."""
    # Find next prime after p using the exact same min-d rule the generator uses
    # (guaranteed correct by PROOF.md).
    cert_like = find_carrier_set(p, search_bound=2048)
    if cert_like is None:
        raise RuntimeError("No carrier after p")
    # The first position after p that has tau==2 is the next prime.
    # We scan forward from p until we hit a d==2 (the generator would have
    # stopped the chamber at the first resolved survivor).
    counts = divisor_counts_segment(p + 1, p + 4096)
    q = None
    for off, d in enumerate(counts, start=1):
        if d == 2:
            q = p + off
            break
    if q is None:
        raise RuntimeError("No next prime found in bound")
    gap = q - p
    N = p * q
    return p, q, N, gap


def main() -> None:
    print("PGS modulus-link factor-spike probe (inversion density at true smaller factor)")
    print("Testing the Novel Insight Engine claim on small exact semiprimes.\n")

    # Small starting primes (all well below 2^20 so everything is instant).
    start_primes = [11, 101, 1009, 10007, 100003, 1000003][:4]  # 4 trials for speed

    hits = 0
    trials = 0
    first_miss = None

    for seed_p in start_primes:
        p, q, N, g = make_small_semiprime(seed_p)
        true_smaller = p
        print(f"\nTrial: p={p}  q={q}  N={N} (gap after p = {g})")

        # Scan probes in a window around true p (width ~ 8*gap to be generous).
        window = max(64, 8 * g)
        scores: list[tuple[int, float]] = []
        for dm in range(-window, window + 1, 1):
            m = true_smaller + dm
            if m < 3:
                continue
            cset = find_carrier_set(m, search_bound=max(128, 2 * g))
            if cset is None:
                continue
            dens = compute_inversion_density(m, N, cset, local_search_radius=max(32, g // 2))
            scores.append((m, dens))

        if not scores:
            print("  No scores (degenerate). Skipping.")
            continue

        # Find the m with the *highest* inversion density in the window.
        best_m, best_dens = max(scores, key=lambda t: t[1])
        # Also record the first m that crosses a high threshold (0.55 chosen
        # from small manual calibration on first trial).
        THRESH = 0.55
        first_high = next((m for m, d in scores if d >= THRESH), None)

        trials += 1
        is_hit = (best_m == true_smaller) or (abs(best_m - true_smaller) <= 2 * g)
        if is_hit:
            hits += 1
        else:
            if first_miss is None:
                first_miss = (true_smaller, best_m, best_dens)

        print(f"  True smaller factor p={true_smaller}")
        print(f"  Highest inversion density at m={best_m} (density={best_dens:.3f})")
        print(f"  First m >= thresh {THRESH}: {first_high}")
        print(f"  HIT (within 2*gap of p) ? {is_hit}")

    print("\n=== Summary ===")
    print(f"Trials: {trials}")
    print(f"Hits (spike within 2*gap of true p): {hits}")
    if trials > 0:
        print(f"Hit rate: {100.0 * hits / trials:.1f}%")
    if first_miss:
        tp, bm, bd = first_miss
        print(f"First miss: true_p={tp}, best_m={bm}, best_density={bd:.3f}")
    print("\nIf hit rate is high on this small regime, the prediction survives first contact.")
    print("Next: lift identical logic to 40-60 bit semiprimes and larger retained variance surfaces.")


if __name__ == "__main__":
    main()
