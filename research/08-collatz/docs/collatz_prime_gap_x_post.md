# X Post Draft

## Single Post

I found a reproducible bridge between prime gaps and Collatz descents.

For each prime gap, pick the first integer inside it with the fewest divisors.
In Collatz first-descent blocks, odd source values hit the neighboring odd
cells around that integer at 1.76x the same-gap background rate.

Those contact blocks also reset differently: median reset is 2.08x versus
1.87x for no-contact blocks.

The strongest reset carrier localizes to the terminal source, specifically
when the last odd source before descent sits one below the prime-gap divisor
minimum.

For that carrier, the residue identity is exact normal form: if the minimizer
is w and the final exponent is k, then 3w ≡ 2 mod 2^k, but not mod 2^(k+1).

At the 1M odd-seed run:

- source hit rate vs same-gap background: 1.76x
- median reset: 2.08x contact vs 1.87x no-contact
- terminal adjacent residue checks: 15,558 / 15,558
- short 3-step k=4/8 carrier: exact branch formulas explain the doubled reset
  scale

This gives a concrete bridge object:

prime-gap divisor minimum + Collatz terminal power-of-two residue.

Code: <gist link>

## Thread Draft

1.

I found a reproducible bridge between prime gaps and Collatz descents.

It starts with a very ordinary object: take two consecutive primes, look at
the integers between them, and pick the first integer with the fewest divisors.

2.

Now look at the odd Collatz map.

Start with an odd number and follow only the odd values until the first time
the orbit drops below the starting number.

That finite segment is a first-descent block. Its length is the number of odd
steps. Its reset strength is the starting value divided by the first lower odd
target.

3.

The experiment asks a simple question:

Do the odd values inside those first-descent blocks interact with the
divisor-minimum structure inside prime gaps?

They do.

4.

At the 1M odd-seed scale, Collatz source values hit the neighboring odd cells
around prime-gap divisor minima about 1.76x as often as the same-gap
background rate.

Same-gap background means: for every visited composite source, compare against
all odd interior cells in that same prime gap, excluding the prime endpoints.

5.

The reset profile separates too.

Witness-contact blocks have median reset 2.08x. No-contact blocks have median
reset 1.87x.

6.

The positive carrier then localizes further.

It is strongest when the terminal source, the last odd value before first
descent, sits one below the prime-gap divisor minimum.

7.

For that below-minimizer terminal carrier, the residue identity is exact normal
form.

If the minimizer is w and the final exponent is k:

3w ≡ 2 mod 2^k

3w ≢ 2 mod 2^(k+1)

8.

At the 1M odd-seed run:

- source hit rate vs same-gap background: 1.76x
- median reset: 2.08x contact vs 1.87x no-contact
- terminal adjacent residue checks: 15,558 / 15,558
- exact 3-step k=4/8 rows split into two explicit reset branches

9.

The bridge object is:

prime-gap divisor minimum + Collatz terminal power-of-two residue.

A targeted 100M inverse scan found rare lower-branch counterexamples, but the
doubled branch dominated below-minimizer hits: 12,218 vs 41.

That gives a concrete next problem: explain the branch imbalance.

Code: <gist link>

## Gist Description

Single-file deterministic Python demo. It recomputes odd Collatz first-descent
blocks, prime gaps, divisor counts, same-gap background controls, terminal
adjacent residue checks, and compact summary metrics. No external packages.
