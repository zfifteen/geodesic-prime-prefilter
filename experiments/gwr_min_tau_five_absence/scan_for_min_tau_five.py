#!/usr/bin/env python3
"""
GWR Min-Tau=5 Absence Probe

Scans consecutive prime gaps and reports whether the minimum divisor count
(tau) in any interior ever equals exactly 5.

This is a measured surface, not a universal theorem.

Usage:
    python3 scan_for_min_tau_five.py --limit 1000000

Reproduces the observation that 5 never appears as the GWR minimum
in standard prime-to-prime gaps on the tested range.
"""

import argparse
import sympy
from collections import Counter
from sympy import primerange, divisor_count


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=1_000_000,
                        help="Upper bound for primes (default 1e6)")
    args = parser.parse_args()

    print(f"Scanning standard prime gaps up to p < {args.limit} ...")
    primes = list(primerange(2, args.limit))

    min_taus = []
    five_count = 0
    total_gaps = 0

    for i in range(len(primes) - 1):
        p = primes[i]
        q = primes[i + 1]
        interior = range(p + 1, q)
        if not interior:
            continue
        total_gaps += 1

        ds = [divisor_count(n) for n in interior]
        m = min(ds)
        min_taus.append(m)
        if m == 5:
            five_count += 1

    dist = dict(Counter(min_taus))
    print("\n=== RESULTS ===")
    print(f"Gaps with nonempty interior: {total_gaps}")
    print(f"Occurrences of min_tau == 5: {five_count}")
    print("\nObserved min_tau distribution (sorted):")
    for k in sorted(dist):
        print(f"  {k}: {dist[k]}")

    if five_count == 0:
        print("\nCONCLUSION (measured surface): In all standard consecutive-prime gaps")
        print("on this range, the GWR minimum divisor count in the interior is never 5.")
    else:
        print(f"\nWARNING: {five_count} gaps found with min_tau=5 (unexpected).")


if __name__ == "__main__":
    main()
