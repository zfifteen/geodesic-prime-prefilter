# RSA v2 Arithmetic Contract

The live runner carries public coordinates as GMP integers, but its exact
divisor-count interval backend is still small-regime.

## Current Boundary

The runner uses `gmpy2.mpz` for:

- `N`;
- `isqrt(N)`;
- balanced interval endpoints;
- lower endpoint anchors;
- reciprocal floor coordinates;
- reset endpoints;
- reset-deadline coordinates.

The runner converts those coordinates to Python `int` only when calling the
current repository interval-measurement helper.

That helper is NumPy-backed and is not an RSA-260-scale GMP interval backend.
The official runner therefore declares:

```text
SMALL_REGIME_MAX_BITS = 50
```

Rows above that limit return unresolved with:

```text
gmp_interval_backend_required
```

## No False GMP Claim

Do not describe the current runner as GMP-only at the interval backend level.

The correct statement is:

```text
GMP coordinates, small-regime exact interval backend.
```

## No Divergent Low-Bit Logic

Do not add per-rung or per-bit selection branches.

The small-regime guard is a backend capability boundary, not an alternate
factorization algorithm. A future GMP interval backend must preserve the same
PGS-first surface:

```text
endpoint walk
-> reciprocal transport
-> reciprocal endpoint check
-> two-sided PGSPG reset state
-> transported deadline facts
```

## Batch-First Measurement

Measure public endpoint fields in batches when possible:

- lower endpoint walk by contiguous chunks;
- reciprocal endpoint check by one measured interval over transported values;
- local reset state only after both sides are endpoints.

Do not measure local reset chambers for arbitrary non-endpoint candidates.

## Arithmetic Comments

Every nontrivial arithmetic operation in factorizer code must have a plain
language comment.

Required comments include:

- the integer square root of `N`;
- balanced interval construction;
- endpoint-walk chunk boundaries;
- reciprocal floor `N // x`;
- reset-deadline transport;
- conversion from `gmpy2.mpz` to Python `int`;
- divisor-count or chamber-state measurement.

## Forbidden Arithmetic Shortcuts

Do not use:

- `gcd` as a selector;
- `N % x == 0` as a contraction filter;
- direct factorization APIs;
- primality APIs as endpoint sources;
- random candidate generation;
- answer-bearing precomputed state rows.

Product closure must not be used as the contraction rule.
