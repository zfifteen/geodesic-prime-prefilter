# Reciprocal Shadow Vote Probe

## Contract

The probe removes every nearby composite row whose factorization contains
the audit factors `p` or `q`. It then scores prime lower-endpoint candidates
using only reciprocal residue shadows cast by the remaining composite
factor threads.

A run succeeds when it identifies either hidden factor. In these
semiprime cases `p < q`, so the scored lower-endpoint surface tests
one-factor success by asking whether `p` ranks first.

The score does not call `N % candidate`, does not multiply a candidate pair
as an acceptance test, and does not use the removed direct factor rows.

## Results

| N | p | q | radius | heldout rows | direct rows removed | candidates | p rank | p coherence | rotated-control p rank | rotated-control p coherence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 713 | 23 | 31 | 300 | 466 | 44 | 9 | 1 | 1.000000 | 9 | 0.090989 |
| 2537 | 43 | 59 | 300 | 497 | 22 | 15 | 1 | 1.000000 | 15 | 0.068164 |
| 5063 | 61 | 83 | 300 | 519 | 14 | 20 | 1 | 1.000000 | 19 | 0.053740 |
| 10057 | 89 | 113 | 300 | 522 | 10 | 25 | 1 | 1.000000 | 25 | 0.049755 |
| 13837 | 101 | 137 | 300 | 531 | 8 | 30 | 1 | 1.000000 | 30 | 0.044490 |
| 21877 | 131 | 167 | 300 | 528 | 6 | 34 | 1 | 1.000000 | 34 | 0.045884 |
| 36503 | 173 | 211 | 300 | 535 | 4 | 43 | 1 | 1.000000 | 42 | 0.040079 |
| 63433 | 229 | 277 | 300 | 536 | 4 | 54 | 1 | 1.000000 | 54 | 0.039279 |
| 112669 | 307 | 367 | 300 | 558 | 0 | 67 | 1 | 1.000000 | 67 | 0.026560 |
| 201703 | 401 | 503 | 300 | 541 | 0 | 87 | 1 | 1.000000 | 86 | 0.036420 |
| 368177 | 557 | 661 | 300 | 557 | 0 | 110 | 1 | 1.000000 | 110 | 0.026379 |
| 621787 | 701 | 887 | 300 | 559 | 0 | 138 | 1 | 1.000000 | 137 | 0.024779 |
| 1242079 | 1009 | 1231 | 300 | 556 | 0 | 186 | 1 | 1.000000 | 185 | 0.025567 |
| 3206803 | 1601 | 2003 | 300 | 551 | 0 | 278 | 1 | 1.000000 | 277 | 0.028441 |
| 12007001 | 3001 | 4001 | 300 | 568 | 0 | 485 | 1 | 1.000000 | 484 | 0.018033 |
| 35026003 | 5003 | 7001 | 300 | 570 | 0 | 777 | 1 | 1.000000 | 772 | 0.016658 |

## Boundary

This is a fixed-window scale test of the indirect-web hypothesis.
It shows whether non-direct neighboring composites create a
reciprocal residue field that ranks one hidden factor. It is not a
proof and not a live factor resolver.

The rotated-control columns keep the same factor rows but rotate offsets
between rows. They test whether the signal depends on the true local
offset-to-factor pairing rather than on the marginal factor multiset.
