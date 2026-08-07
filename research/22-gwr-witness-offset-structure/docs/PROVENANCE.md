# Provenance

The observation was made during a Grok research session on 2026-08-06 / 2026-08-07.

The starting point was the bounded-compression scatter for small primes.
Extension of that plot to all primes up to 10^6 revealed the dense horizontal layering and the extreme concentration of offsets.

All measurements use the exact Gap Winner Rule:
w is the leftmost interior integer of minimum divisor count.

The generation script in scripts/ reproduces the plot and the statistics file from first principles.
No external data tables are required beyond sympy's prime generator and divisor function.
