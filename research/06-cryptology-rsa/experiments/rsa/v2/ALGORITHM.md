# RSA v2 Reciprocal PGSPG Certificate Algorithm

This document defines the live v2 algorithm after the radius-first and
endpoint-budget scaffolds were withdrawn.

The current algorithm is an inference-surface builder, not a factor resolver.
It derives public reciprocal PGSPG certificate state and returns unresolved
unless the public certificate pair mutually closes.

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

The square root separates the lower and upper sides. It does not define a fixed
additive candidate chamber.

## Stage 2: Lower Certificate

Find the previous public endpoint before `isqrt(N)`.

Derive the PGSPG chamber-reset certificate from that endpoint. The certificate
contains the reset endpoint, carrier state, closed offsets before reset, threat
state, tail state, and reset-deadline fields.

## Stage 3: Reciprocal Transport

Transport the lower reset endpoint by:

```text
y = floor(N / lower.reset_endpoint)
```

This is public reciprocal transport. It is not a divisibility test and does not
check product closure.

## Stage 4: Upper Certificate

Find the previous public endpoint before `y`.

Derive the PGSPG chamber-reset certificate from that endpoint.

## Stage 5: Certificate Closure

The current closure candidate is strict.

It resolves only when:

1. both certificates exist;
2. `floor(N / lower.reset_endpoint) == upper.reset_endpoint`;
3. `floor(N / upper.reset_endpoint) == lower.reset_endpoint`;
4. lower and upper reset signatures match.

If any condition fails, inference emits unresolved.

## Current Failure Modes

The runner may emit:

```text
resolved_by_mutual_certificate_closure
unresolved_by_certificate_pair_not_closed
unresolved_by_missing_lower_certificate
unresolved_by_missing_upper_certificate
gmp_interval_backend_required
```

The current 40-bit and 50-bit rungs emit:

```text
unresolved_by_certificate_pair_not_closed
```

## Explicitly Invalidated Rules

The following are not live rules:

- fixed-radius candidate bands around `isqrt(N)`;
- endpoint-walk budgets as solver coverage;
- raw equality of lower and upper reset-deadline margins;
- stationary recursive reset rounds;
- product closure as the contraction rule;
- audit factors as inference inputs.

## Resolver Target

The next algorithmic target is a transported certificate invariant.

The invariant must be derived from public `N`, PGSPG certificate fields, and
floor-map transport. It must not use product closure, divisibility, audit
factors, factor APIs, primality APIs, random generation, or fallback search.
