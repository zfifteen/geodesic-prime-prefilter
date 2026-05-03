# RSA v2 Arithmetic Contract

The 40-bit implementation is the first run of the RSA-scale arithmetic path.
It is not a toy path.

## GMP From The First Step

Use `gmpy2` for factorizer arithmetic:

- `N`;
- `isqrt(N)`;
- ordered chamber coordinates;
- reciprocal floor coordinates;
- interval endpoints;
- chamber anchors.

The implementation may convert small values to Python `int` only when a library
interface requires it and the value has already been produced by the GMP path.
The logical arithmetic path remains GMP-compatible.

## No Divergent Low-Bit Path

Do not implement separate logic for 40-bit numbers.

The same functions that run the 40-bit case must also accept larger moduli. If a
future optimization is needed, it must preserve the same interface and produce
the same stage records.

## Batch-First Measurement

The factorizer should not measure local chambers one candidate at a time when
several candidates need overlapping intervals.

The intended sequence is:

```text
candidate batch
-> cheap public filters
-> reciprocal floors
-> chamber interval jobs
-> deduplicated / merged interval measurement
-> PGSPG state rows
```

The first 40-bit implementation may use small batches, but it should keep the
batch shape explicit so higher regimes do not require a redesign.

## Interval Deduplication

Before chamber measurement, collect the intervals required by candidate
analysis.

If two chamber intervals overlap, measure the shared region once and reuse the
result.

This matters because reciprocal candidate surfaces can ask for many nearby
lower and upper chamber states.

## Avoid Unneeded Expensive Facts

The factorizer needs decision facts, not complete factorization records.

Prefer measuring only what the PGS chamber rule needs:

- wheel-open status;
- endpoint-like divisor-count state;
- selected-integer / carrier state;
- lower-divisor threat state;
- chamber-reset endpoint state.

Do not compute a full factorization when a capped divisor-count comparison is
sufficient for the rule being applied.

## Arithmetic Comments

Every arithmetic operation in factorizer code must have a plain-language
comment explaining the quantity being computed.

Required comments include:

- the integer square root of `N`;
- the full chamber interval around `isqrt(N)`;
- the reciprocal floor `N // x`;
- reciprocal reset-deadline transport;
- any conversion from `gmpy2.mpz` to Python `int`;
- every divisor-count or chamber-state measurement.

Comments should explain the arithmetic, not narrate the code.

## Forbidden Arithmetic Shortcuts

Do not use:

- `gcd` as a selector;
- `N % x == 0` as a contraction filter;
- direct factorization APIs;
- primality APIs as endpoint sources;
- random candidate generation;
- answer-bearing precomputed state rows.

Product closure must not be used as the contraction rule.
