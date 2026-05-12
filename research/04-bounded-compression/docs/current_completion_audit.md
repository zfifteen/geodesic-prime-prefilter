# Dynamic Cutoff Completion Audit

## Objective

Prove or falsify the Dynamic Cutoff Conjecture for bounded GWR/DNI prime
walks:

```text
For every right prime q, the exact unbounded GWR/DNI-selected witness occurs
within C(q) = max(64, ceil(0.5 * log(q)^2)) of q.
```

## Success Criteria

| Requirement | Evidence | Status |
|---|---|---|
| Prove the cutoff law for every right prime `q` | No proof artifact exists. | `unresolved` |
| Falsify the cutoff law with a first explicit counterexample | The bounded-compression runner found no failure through `q <= 10,000,000`; no universal counterexample exists in the repo. | `unresolved` |
| Preserve an executable falsifier | `research/04-bounded-compression/scripts/bounded_compression_falsification_runner.py` exists with tests. | `done` |
| Preserve measured finite surfaces | `1e6` and `1e7` findings exist. | `done` |
| Reduce non-square branch | Lemma A' survives through `q <= 10,000,000` with `499,896` no-square `d=4` fallback cases and no failure. | `measured only` |
| Identify invalidated reduction | Literal prior-square Lemma A fails at `q = 113`, where the exact witness is later square `121 = 11^2`. | `done` |
| Pressure-test square branch | Documented square-offset envelope surfaces through prime roots `p <= 500,000,000` found no counterexample; standing utilization record is `0.9341772151898734`. | `measured only` |

## Current State

The goal is not complete.

The current measured reduction is:

```text
no interior prime square -> first d=4 carrier wins on q <= 10,000,000
interior prime square -> square-offset envelope remains unresolved
```

The remaining proof or falsification pressure is Lemma B:

```text
If the selected witness is r^2 after right-prime q, then r^2 - q < C(q).
```

## Next Valid Work

Continue on the square branch. A completion claim requires either a proof that
the square-offset envelope holds for all right primes, or a first explicit
counterexample where a square witness exceeds `C(q)`.
