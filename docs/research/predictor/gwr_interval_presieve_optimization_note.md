# GWR Interval Pre-Sieve Optimization Note

Date: 2026-05-09

## Strongest Supported Claim

An exact interval pre-sieve is a real optimization for GWR/DNI divisor-field
scans that consume a short contiguous chamber in offset order.

The winning mechanism is:

```text
For anchor q and cutoff C(q), pre-sieve [q + 1, q + C(q)] through
floor(cuberoot(q + C(q))). Store partial divisor-count products and residual
cofactors. Then scan offsets in order, classifying a residual only when the
partial count can improve the current lex-min state or when endpoint detection
is needed.
```

This preserves the PGS invariant:

```text
same ordered offsets -> same tau comparisons -> same leftmost minimum ->
same first tau(n) = 2 boundary
```

No offsets are skipped. The optimization changes divisor-count computation
cost, not the GWR rule.

## Measured Result

Benchmark output:

```text
output/gwr_interval_presieve_benchmark_20260509/summary.json
```

Measured exact-match surfaces:

| Surface | Current clipped | Live bounded | Presieved capped | Speedup vs clipped | Speedup vs bounded |
|---|---:|---:|---:|---:|---:|
| 5000 gaps near 10^7 | 0.291 ms/gap | 0.292 ms/gap | 0.061 ms/gap | 4.76x | 4.79x |
| 5000 gaps near 10^8 | 0.360 ms/gap | 0.413 ms/gap | 0.088 ms/gap | 4.11x | 4.71x |
| 1000 gaps near 10^12 | 1.336 ms/gap | 4.465 ms/gap | 0.437 ms/gap | 3.06x | 10.22x |

Every tested row matched the current oracle exactly on:

```text
(next_dmin, next_peak_offset, gap_boundary_offset)
```

## Invalidated Variant

The fixed small-prime bound `primes <= 200` is invalid as an exact production
replacement.

Counterexample:

```text
q = 100000007
offset = 24
n = 100000031 = 283 * 307 * 1151
tau(n) = 8
```

A `<= 200` pre-sieve strips nothing and misclassifies the residual as a
two-factor composite with multiplier `4`. Exactness requires pre-sieving
through `floor(cuberoot(q + C(q)))`, matching the residual-classification
condition used by the current exact interval field.

## Refactor Targets

Primary target:

```text
benchmarks/python/predictor/gwr_dni_recursive_walk.py
```

Replace the scalar capped tail path around `_divisor_count_capped` with an
exact interval-presieved capped scanner. Preserve the existing public outputs.

Secondary targets after the primary refactor is tested:

```text
src/python/z_band_prime_predictor/gwr_boundary_walk.py
src/python/z_band_prime_predictor/simple_pgs_generator.py
```

For `gwr_boundary_walk.py`, the advantage is event-based stopping inside a
short presieved block instead of fully classifying unused tail positions after
the first `tau(n) = 2` boundary.

For `simple_pgs_generator.py`, the generator output contract is unchanged:

```json
{"p": 11, "q": 13}
```

The optimization belongs in the internal chamber field used by certificates and
resolution logic. It must not add source labels, diagnostics, confidence
fields, fallback paths, or alternate inference rules to generator output.

## Implementation Contract

Add one narrow helper before broad refactors:

```text
presieved_capped_gap_scan(q, cutoff) -> next_dmin, next_peak_offset, boundary_offset
```

The helper must:

- scan offsets in increasing order;
- stop at the first `tau(n) = 2` boundary;
- update the leftmost lex-min exactly as the current GWR scan does;
- pre-sieve through `floor(cuberoot(q + cutoff))`, not a fixed small-prime
  frontier;
- return explicit failure if the boundary is not reached by the cutoff;
- avoid fallback search, randomization, or alternate implementations.

Required tests:

- exact match against the current clipped oracle on small primes including
  `23`;
- exact match on `q = 100000007`, offset `24` residual-classification
  counterexample coverage;
- exact match against current recursive-walk surfaces near `10^7`, `10^8`,
  and at least one higher coordinate surface;
- preservation of intermediate `(best_d, best_offset)` updates where practical.

## Status

This is a measured implementation optimization, not a new theorem.

The theorem status remains controlled by `PROOF.md`. The optimization is
production-relevant because it preserves exact GWR state while reducing
duplicated divisor-field work inside short chambers.
