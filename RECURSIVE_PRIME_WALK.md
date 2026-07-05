# Recursive Prime Walk

The README follows one gap. Start with one prime, read the integers after it, and the next prime appears at the first later divisor count of `2`.

The recursive walk asks what happens when that step is repeated.

Start at one prime. Recover the next prime. Then use that next prime as the new starting point. Read the next interval. Recover the next endpoint. Continue.

That is the walk: a deterministic prime-to-prime movement built from exact divisor counts and the selected-composite structure inside each gap.

## Exact Recursive Prime Walk

Given a known prime `p`, the exact divisor-count theorem determines the next prime `q` directly. Check the integers greater than `p` in increasing order, compute `tau(n)` exactly, and stop at the first integer with `tau(n) = 2`.

The recursive walk uses that exact `p -> q` step as its successor-prime transition. No cutoff theorem is involved in the exact walk.

The most jarring combined predictor result is the closure that appears after the score maximizer. Once the implemented score maximizer appears inside a prime gap, the next prime arrives before any later interior composite with strictly smaller divisor count can appear.

That closure law lets the unbounded DNI/GWR walker recover the next prime exactly from the ordered divisor structure of the next-gap interior.

On the current verified surface, this supports an exact deterministic no-skip sequential walk. The transition rule is exact on `743,075 / 743,075` rows from the combined $10^6 + 10^7$ next-gap surface. The recursive walk records `664,578 / 664,578` exact consecutive next-prime recoveries from prime `11` through prime `10,000,121` with `0` skipped gaps. The sampled decade ladder from $10^2$ through $10^18$ also stayed at exact hit rate `1.0` with `0` skipped gaps across `860` measured recursive steps.

The predictor note is documented in [research/02-gwr-dni/docs/gwr_dni_exact_recursive_prime_walk_note.md](research/02-gwr-dni/docs/gwr_dni_exact_recursive_prime_walk_note.md), and the live implementation is [research/02-gwr-dni/scripts/gwr_dni_recursive_walk.py](research/02-gwr-dni/scripts/gwr_dni_recursive_walk.py).

![Exact DNI recursive-walk performance](research/02-gwr-dni/assets/gwr_dni_recursive_gap_scaling_performance.png)

## No-Later-Simpler-Composite

Inside a prime gap, the selected composite is the first interior number with the lowest divisor count. After that point, the gap does not later produce a strictly simpler interior composite before the next prime arrives.

That is the No-Later-Simpler-Composite condition.

In words: once the selected integer appears, the next prime closes the interval before any later interior composite with a smaller divisor count can appear.

In symbols, if $w$ is the implemented log-score maximizer in the gap $(p, q)$ and:

$$T_{<}(w)=\min\{\,n>w:d(n)<d(w)\,\}$$

then the closure condition is:

$$q\le T_{<}(w)$$

This is an exact corollary of the proved GWR theorem. A separate question is whether it can stand on its own as a direct prime-gap theorem without using GWR as the parent result. The current documented surface includes a deterministic even-band ladder at every decade from $10^8$ through $10^{18}$ with zero observed violations.

See [PROOF.md](PROOF.md), [research/02-gwr-dni/docs/closure_constraint_findings.md](research/02-gwr-dni/docs/closure_constraint_findings.md), and [docs/current_headline_results.md](docs/current_headline_results.md).

## Dynamic Cutoff and Square-Branch Falsification

The exact walk does not need a cutoff theorem. The bounded walk does — and that
theorem is now proved.

Universal bounded compression is proved in [PROOF.md](PROOF.md) (2026-07-05).
For every consecutive prime gap, the GWR-selected witness satisfies

```text
C(q) = max(64, ceil(0.5 * log(q)^2))
```

The Prime-Square Proximity Theorem closes the square branch at Cramér scale.
This bounds the selected-witness offset `w - p`; it does not by itself prove
RH, PNT, or every classical formulation of Cramér's conjecture for raw gap
size `q - p`.

The old fixed cutoff theorem `{2:44, 4:60, 6:60}` is false and invalidated.
It fails at `q = 24,098,209`, where the square branch gives `E(q) = 72 > 60`.
The bounded walker no longer treats that fixed map as live.

Falsification scripts provide **audit corroboration** of the proved bound, not
proof boundaries. Through the direct square-branch audit at `p <= 10^6`, the
repository tested `78,498` prime squares, found `7,477` violations of the old
fixed map, and observed maximum square offset `246`.

The compare mode in the recursive walker is the live audit instrument. It runs
the bounded and unbounded walkers in lockstep and records any bounded miss
immediately.

See [research/04-bounded-compression/scripts/square_branch_gap_audit.py](research/04-bounded-compression/scripts/square_branch_gap_audit.py), [research/02-gwr-dni/scripts/gwr_dni_recursive_walk.py](research/02-gwr-dni/scripts/gwr_dni_recursive_walk.py), and [research/02-gwr-dni/docs/gwr_dni_exact_recursive_prime_walk_note.md](research/02-gwr-dni/docs/gwr_dni_exact_recursive_prime_walk_note.md).

## Dominant d=4 Reduction

In the most common selected-integer regime, the gap interior has no prime square. When that square branch is excluded, the implemented score maximizer is exactly the first interior integer with divisor count `4`.

That gives the leading regime a visible mechanism: square exclusion first, then first-`d=4` arrival.

The stricter semiprime-only slogan is false. A thin prime-cube exception family survives inside the broader `d=4` class.

The dominant `d=4` reduction is exact on full scans through `2x10^7`.

See [research/02-gwr-dni/docs/dominant_d4_arrival_reduction_findings.md](research/02-gwr-dni/docs/dominant_d4_arrival_reduction_findings.md) and [docs/current_headline_results.md](docs/current_headline_results.md).
