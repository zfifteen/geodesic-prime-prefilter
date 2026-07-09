#!/usr/bin/env python3
"""
Near-Maximal Witness Offset Audit
---------------------------------
Scans consecutive prime gaps up to LIMIT.
For each gap p < q with nonempty interior:
  - Finds GWR witness w = leftmost n in (p, q) with minimal tau(n)
  - Computes d = tau(w), offset = w - p
  - C = max(64, ceil(0.5 * log(q)**2))
  - ratio = offset / C
Collects:
  - Global max ratio and associated stats
  - All cases with ratio >= 0.70 (near the bound)
  - For those: reports d, offset, C, log(q), whether d<=5 or prime-square
Falsification test for the "rough witness" prediction.
"""

import numpy as np
import math
from math import log, ceil

LIMIT = 40_000_000   # Extended target for falsification attempt
RATIO_THRESHOLD = 0.65
PROGRESS_EVERY = 100_000  # primes

def sieve_spf(limit):
    spf = np.arange(limit + 1, dtype=np.int32)
    for i in range(2, int(limit**0.5) + 1):
        if spf[i] == i:
            for j in range(i*i, limit + 1, i):
                if spf[j] == j:
                    spf[j] = i
    return spf

def divisor_count(n, spf):
    if n <= 1:
        return 1
    cnt = 1
    while n > 1:
        p = spf[n]
        exp = 0
        while n % p == 0:
            n //= p
            exp += 1
        cnt *= (exp + 1)
    return cnt

def is_perfect_square(n):
    if n < 0:
        return False
    r = int(math.isqrt(n))
    return r * r == n

def main():
    print(f"Building SPF sieve up to {LIMIT}...")
    spf = sieve_spf(LIMIT)
    print("Extracting primes...")
    primes = [i for i in range(2, LIMIT + 1) if spf[i] == i]
    print(f"Found {len(primes)} primes. Starting gap scan...")

    max_ratio = 0.0
    max_case = None
    near_max_cases = []
    total_gaps_with_interior = 0
    processed_primes = 0

    for i in range(len(primes) - 1):
        p = primes[i]
        q = primes[i + 1]
        if q > LIMIT:
            break
        interior_start = p + 1
        interior_end = q - 1   # inclusive
        if interior_start > interior_end:
            continue
        total_gaps_with_interior += 1
        processed_primes += 1
        if processed_primes % PROGRESS_EVERY == 0:
            print(f"  Processed {processed_primes:,} primes... (current q ≈ {q:,})")

        # Find leftmost minimal tau
        min_tau = None
        w = None
        for n in range(interior_start, interior_end + 1):
            tau = divisor_count(n, spf)
            if min_tau is None or tau < min_tau:
                min_tau = tau
                w = n

        offset = w - p
        Lq = log(q)
        C = max(64, ceil(0.5 * Lq * Lq))
        ratio = offset / C if C > 0 else 0.0

        if ratio > max_ratio:
            max_ratio = ratio
            max_case = {
                'p': p, 'q': q, 'w': w, 'd': min_tau,
                'offset': offset, 'C': C, 'ratio': ratio, 'logq': Lq
            }

        if ratio >= RATIO_THRESHOLD:
            is_square = is_perfect_square(w) and min_tau == 3
            near_max_cases.append({
                'p': p, 'q': q, 'w': w, 'd': min_tau,
                'offset': offset, 'C': C, 'ratio': ratio,
                'logq': round(Lq, 2),
                'is_prime_square': is_square,
                'low_d': min_tau <= 5
            })

    print("\n=== AUDIT SUMMARY ===")
    print(f"Total gaps with interior scanned: {total_gaps_with_interior}")
    print(f"Global maximum ratio (w-p)/C : {max_ratio:.4f}")
    if max_case:
        print(f"  Achieved at p={max_case['p']}, q={max_case['q']}, w={max_case['w']}, d={max_case['d']}")
        print(f"  offset={max_case['offset']}, C={max_case['C']}, log(q)≈{max_case['logq']:.2f}")

    print(f"\nCases with ratio >= {RATIO_THRESHOLD}: {len(near_max_cases)}")
    if near_max_cases:
        print("Details (first 20 or all if fewer):")
        for case in near_max_cases[:20]:
            print(f"  q={case['q']}: ratio={case['ratio']:.3f}, d={case['d']}, "
                  f"offset={case['offset']}/C={case['C']}, logq≈{case['logq']}, "
                  f"prime_square={case['is_prime_square']}, d<=5={case['low_d']}")
    else:
        print("No near-maximal witness offsets found at this threshold.")

    # Falsification check - strict for non-square low-d
    non_square_falsifiers = [c for c in near_max_cases if (not c['is_prime_square']) and c['low_d']]
    square_high_ratio = [c for c in near_max_cases if c['is_prime_square']]

    print(f"\n=== FALSIFICATION RESULTS ===")
    print(f"Non-square low-d (d≤5) high-ratio cases: {len(non_square_falsifiers)}")
    if non_square_falsifiers:
        print("*** FALSIFIED *** Found non-square counterexamples:")
        for f in non_square_falsifiers:
            print(f"  q={f['q']}, d={f['d']}, ratio={f['ratio']:.3f} (threshold 0.65)")
    else:
        print("No non-square low-d falsifiers. Core rough-witness claim holds in scanned range.")

    print(f"Prime-square high-ratio cases: {len(square_high_ratio)}")
    if square_high_ratio:
        max_square_ratio = max(c['ratio'] for c in square_high_ratio)
        print(f"  Highest square ratio observed: {max_square_ratio:.4f}")
        if max_square_ratio > 0.80:
            print("  NOTE: Square achieved >80% of bound, challenges 'bounded away from 1.0' observation.")

    # Save detailed results
    import json
    results = {
        "limit": LIMIT,
        "total_gaps": total_gaps_with_interior,
        "max_ratio": max_ratio,
        "max_case": max_case,
        "near_max_count": len(near_max_cases),
        "non_square_falsifiers_count": len(non_square_falsifiers),
        "square_high_ratio_count": len(square_high_ratio),
        "non_square_falsifiers": non_square_falsifiers,
        "square_cases": square_high_ratio[:5] if square_high_ratio else []
    }
    with open("/home/workdir/artifacts/near_maximal_audit_results.json", "w") as f:
        json.dump(results, f, indent=2, default=str)
    print("\nDetailed results saved to near_maximal_audit_results.json")

if __name__ == "__main__":
    main()
