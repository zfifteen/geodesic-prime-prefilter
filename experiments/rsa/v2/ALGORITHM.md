# RSA v2 PGS-First Anchor-Surface Algorithm

This document defines the live v2 algorithm after the radius-first scaffold was
withdrawn.

The current algorithm is an inference-surface builder, not a factor resolver.
It derives public reciprocal PGSPG state and returns unresolved until the
transported deadline invariant is derived.

## Input

Inference reads only:

```text
fixtures/ladder_cases.jsonl
```

Each row contains public data:

- `case_id`;
- `bits`;
- `N`;
- optional `description`.

Inference does not read audit factors.

## Stage 1: Public Orientation

Compute `isqrt(N)`.

The square root separates the lower and upper balanced sides. It does not define
a fixed additive candidate chamber.

## Stage 2: Balanced Endpoint Walk

Compute the public balanced interval:

```text
lower = floor(isqrt(N) / balance_band)
upper = isqrt(N) * balance_band
```

Walk downward from `isqrt(N)` through exact endpoint state. Each endpoint is a
candidate anchor because PGSPG operates from endpoint anchors, not arbitrary
integers in a close-in band.

The current implementation uses a bounded endpoint-walk budget. If the endpoint
walk does not cover enough of the balanced interval, that is a surface-budget
fact, not a factorization fallback.

## Stage 3: Reciprocal Transport

For each lower endpoint `x`, compute:

```text
y = floor(N / x)
```

This is public reciprocal transport. It is not a divisibility test and does not
check product closure.

Keep rows where `y` is on the upper balanced side and open under the fixed
30-wheel.

## Stage 4: Reciprocal Endpoint Check

Measure whether the transported `y` values are also exact endpoints.

Rows where both `x` and `y` are endpoints form the reciprocal endpoint surface.

## Stage 5: PGSPG Reset State

For each reciprocal endpoint row, derive local PGSPG reset state on both sides:

```text
previous endpoint before x -> PGSPG chamber reset
previous endpoint before y -> PGSPG chamber reset
```

Keep rows where the lower reset returns to `x` and the upper reset returns to
`y`.

These are the two-sided PGSPG reset-lock rows.

## Stage 6: Deadline Transport Facts

For each two-sided reset lock, compute reset-to-deadline transport widths:

```text
floor(N / reset_endpoint) - floor(N / reset_deadline)
```

on each side.

The runner records these facts. It does not currently use them as a resolver.

## Current Failure Mode

The runner emits:

```text
status = unresolved
unresolved_reason = transported_deadline_invariant_not_derived
```

when two-sided PGSPG reset locks exist.

If no two-sided reset locks exist, it emits:

```text
status = unresolved
unresolved_reason = no_two_sided_pgs_lock
```

If a rung exceeds the current exact interval backend boundary, it emits:

```text
status = unresolved
unresolved_reason = gmp_interval_backend_required
```

## Explicitly Invalidated Rules

The following are not live rules:

- fixed-radius candidate bands around `isqrt(N)`;
- raw equality of lower and upper reset-deadline margins;
- stationary recursive reset rounds;
- product closure as the contraction rule;
- audit factors as inference inputs.

## Resolver Target

The next algorithmic target is a transported deadline invariant.

The invariant must accept asymmetric raw margins when reciprocal transport
explains the asymmetry, and it must reject ordinary symmetric near-square false
locks. It must use only public `N`, PGSPG state, and floor-map transport.
