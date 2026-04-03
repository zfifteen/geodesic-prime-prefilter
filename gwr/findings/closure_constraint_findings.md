# Closure-Constraint Findings

This note records the first empirical results for the closure-constraint
reading of the Gap Winner Rule.

## Statement Tested

For each prime gap $(p, q)$, let $w$ be the implemented log-score winner on the
interior composites. The tested closure constraint is:

$$
\text{there is no later interior composite } n \text{ with } w < n < q
\text{ and } d(n) < d(w).
$$

Equivalently:

$$
q
\text{ occurs before the first later strictly simpler composite.}
$$

This is not a tautology, because the script defines $w$ from the implemented
log-score argmax and then separately checks the later divisor profile.

## Current Artifacts

- runner:
  [`benchmarks/python/gap_ridge/gwr_closure_constraint.py`](../../benchmarks/python/gap_ridge/gwr_closure_constraint.py)
- tests:
  [`tests/python/gap_ridge/test_gwr_closure_constraint.py`](../../tests/python/gap_ridge/test_gwr_closure_constraint.py)
- JSON summary:
  [`output/gwr_closure_constraint_summary.json`](../../output/gwr_closure_constraint_summary.json)
- sampled CSV:
  [`output/gwr_closure_constraint_sampled.csv`](../../output/gwr_closure_constraint_sampled.csv)

## Tested Surface

The current documented run used:

- exact full scan to $10^6$,
- sampled scales $10^8$ and $10^9$,
- window size $2 \times 10^6$,
- $2$ even windows per sampled scale,
- $2$ fixed seeds: $20260331$ and $20260401$,
- $2$ seeded windows per seed and sampled scale.

## Closure Results

Every tested regime returned zero closure violations.

| Regime | Gap count | Violations | Match rate | Max gap |
|---|---:|---:|---:|---:|
| exact $10^6$ | 70,327 | 0 | 1.0 | 114 |
| even $10^8$ | 234,639 | 0 | 1.0 | 176 |
| even $10^9$ | 224,237 | 0 | 1.0 | 190 |
| seeded $10^8$, seed $20260331$ | 208,733 | 0 | 1.0 | 168 |
| seeded $10^9$, seed $20260331$ | 189,058 | 0 | 1.0 | 224 |
| seeded $10^8$, seed $20260401$ | 206,515 | 0 | 1.0 | 164 |
| seeded $10^9$, seed $20260401$ | 184,649 | 0 | 1.0 | 186 |

The strongest supported finding on this tested surface is therefore:

The closure constraint held exactly on every tested gap.

## Threat-Horizon Summary For $d=4$ Winners

For the dominant winner class $d(w) = 4$, the first later strictly simpler
composite must have $d = 3$. That means the first possible later threat is the
next prime square after the winner.

For each $d=4$ winner, the run recorded:

- threat distance:
  the distance from the winner to the next prime square,
- prime-arrival margin:
  the distance from the right prime $q$ to that next prime square.

A positive margin means the gap closed before the first later $d=3$ threat
could appear.

| Regime | $d=4$ winner share | Mean threat distance | Mean prime-arrival margin | Min margin |
|---|---:|---:|---:|---:|
| exact $10^6$ | 0.8290 | 5,869.6 | 5,857.5 | 2 |
| even $10^8$ | 0.8256 | 89,705.6 | 89,690.6 | 2 |
| even $10^9$ | 0.8251 | 212,536.9 | 212,521.2 | 2 |
| seeded $10^8$, seed $20260331$ | 0.8241 | 93,307.4 | 93,290.2 | 2 |
| seeded $10^9$, seed $20260331$ | 0.8241 | 415,484.3 | 415,465.2 | 2 |
| seeded $10^8$, seed $20260401$ | 0.8234 | 92,275.3 | 92,258.0 | 2 |
| seeded $10^9$, seed $20260401$ | 0.8228 | 207,755.0 | 207,735.3 | 2 |

These margins are all positive on the tested surface. In the current run, every
observed $d=4$ winner was followed by a right prime before the first later
prime-square threat.

## Interpretation

These findings support the closure reading of GWR:

- once the score winner appears, the gap closes before any later strictly
  simpler composite arrives;
- for the dominant $d=4$ winner class, the next-prime closure occurs well
  before the first later $d=3$ threat on every tested regime;
- the gap appears to be locally terminated before a strictly simpler late
  challenger can enter the interior.

This is the empirical form of the intuition that GWR constrains what
consecutive primes are allowed to leave behind after the winner.

## Scope

This note documents the current closure-constraint run only. It does not claim:

- a proof of the closure statement,
- a full asymptotic prime-distribution theorem,
- or a completed high-scale sweep beyond the documented regimes above.

The $d=4$ threat summary is exact for the dominant $d=4$ winner class because
the next lower divisor class is $d=3$, which occurs at prime squares. More
general threat summaries for other winner classes remain open follow-on work.
