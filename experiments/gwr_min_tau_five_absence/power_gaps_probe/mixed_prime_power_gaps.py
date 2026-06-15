#!/usr/bin/env python3
"""
Probe for min_tau in "prime related gaps": intervals between consecutive
elements in the set of primes union prime powers (squares, cubes, fourth powers).

This directly tests @materion's question: can 5 be the minimum divisor count
in interiors of such mixed sets?

See the main FINDINGS.md for the standard prime gap case (never 5).

Usage:
    python3 mixed_prime_power_gaps.py --limit 100000
"""

import argparse
from collections import Counter
import sympy
from sympy import primerange, divisor_count, factorint


def generate_specials(limit):
    specials = set()
    primes = list(primerange(2, limit))
    for p in primes:
        specials.add(p)
        # squares
        sq = p * p
        if sq < limit:
            specials.add(sq)
        # cubes
        cu = p * p * p
        if cu < limit:
            specials.add(cu)
        # fourth powers
        fp = p * p * p * p
        if fp < limit:
            specials.add(fp)
    return sorted(specials)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=100000,
                        help="Upper limit for numbers (default 1e5)")
    args = parser.parse_args()

    print(f"Generating prime-related specials (primes + p^2 + p^3 + p^4) up to {args.limit}...")
    specials = generate_specials(args.limit)
    print(f"Found {len(specials)} special numbers.")

    min_taus = []
    five_examples = []
    total_interiors = 0

    for i in range(len(specials) - 1):
        s = specials[i]
        t = specials[i + 1]
        interior = list(range(s + 1, t))
        if not interior:
            continue
        total_interiors += 1

        ds = [(n, divisor_count(n)) for n in interior]
        m = min(d for _, d in ds)
        min_taus.append(m)

        if m == 5:
            ws = [n for n, d in ds if d == 5]
            w = min(ws) if ws else None
            facts = factorint(w) if w else {}
            five_examples.append((s, t, w, facts))

    dist = dict(Counter(min_taus))
    print("\n=== RESULTS ===")
    print(f"Interiors with numbers: {total_interiors}")
    print(f"Occurrences of min_tau == 5: {len(five_examples)}")
    print("\nObserved min_tau distribution (sorted):")
    for k in sorted(dist):
        print(f"  {k}: {dist[k]}")

    if five_examples:
        print("\nExamples where min_tau=5:")
        for ex in five_examples[:5]:
            print(f"  Between {ex[0]} and {ex[1]}: w={ex[2]} factors={ex[3]}")
    else:
        print("\nNo interiors with min_tau exactly 5 found in this range.")

    print("\nNote: These are intervals between 'prime-related' numbers (primes + their powers).")
    print("Compare to standard consecutive-prime gaps, where 5 also never appears as min.")


if __name__ == "__main__":
    main()
