# RSA v2 Reciprocal PGSPG Certificate Algorithm

This document defines the live v2 algorithm after the radius-first and
endpoint-budget scaffolds were withdrawn.

The current algorithm is a public reciprocal PGSPG resolver for the small
exact-backend regime. It derives reciprocal certificate state and resolves only
when public certificate endpoints close under floor transport.

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

Before transport, the lower reset endpoint must still lie on the lower side of
the square-root orientation:

```text
lower.reset_endpoint <= isqrt(N)
```

If the lower reset endpoint is greater than `isqrt(N)`, the certificate is
valid but its reset endpoint has crossed the orientation boundary. It is not a
lower-side transport coordinate. The oriented endpoint-chain branch uses the
lower public anchor as the transport coordinate for that chamber.

Transport the lower reset endpoint by:

```text
y = floor(N / lower.reset_endpoint)
```

This is public reciprocal transport. It is not a divisibility test and does not
check product closure.

## Stage 4: Upper Certificate

Find the previous public endpoint before `y`.

Derive the PGSPG chamber-reset certificate from that endpoint.

## Stage 5: Reset Certificate Closure

The first closure branch is strict reset closure. It resolves when:

1. both certificates exist;
2. `floor(N / lower.reset_endpoint) == upper.reset_endpoint`;
3. `floor(N / upper.reset_endpoint) == lower.reset_endpoint`;
4. lower and upper reset signatures match.

If this branch fails, the runner does not widen into a search budget. It moves
to one public deadline-correction branch.

## Stage 6: Deadline Signature Correction

When the upper certificate exists but reset closure fails, transport the upper
reset endpoint back to the lower side:

```text
z = floor(N / upper.reset_endpoint)
```

Find the previous public endpoint before `z`. Call it `c`. Derive the PGSPG
certificate at `c`. Let:

```text
d = upper.reset_deadline_value
```

The correction branch resolves only when:

1. `c` is strictly before the original lower anchor;
2. `d` is strictly after the upper reset endpoint;
3. `floor(N / c) == d`;
4. `floor(N / d) == c`;
5. the corrected-lower reset signature matches the upper reset signature.

This branch uses one reciprocal correction induced by the failed upper
certificate. It does not test divisibility, multiply candidate endpoints, read
audit factors, or walk a budgeted list of lower endpoints.

## Stage 7: Oriented Endpoint-Chain Closure

If the square-root chamber does not close, walk the lower public endpoint chain
outward down to:

```text
floor(isqrt(N) / 2)
```

For each lower public endpoint, derive its PGSPG certificate and choose the
oriented transport coordinate:

```text
lower.reset_endpoint  when lower.reset_endpoint <= isqrt(N)
lower.anchor          when lower.reset_endpoint > isqrt(N)
```

Transport that coordinate, derive the upper certificate, and apply the same
deadline-signature correction predicate. The first public lower-chain endpoint
whose corrected lower endpoint and upper deadline mutually close under
`floor(N / x)` resolves as:

```text
resolved_by_oriented_endpoint_chain_closure
```

This is endpoint-chain traversal over public PGS endpoints. It is not product
closure, divisibility testing, a fixed-radius candidate band, or a hidden-factor
search.

## Current Failure Modes

The runner may emit:

```text
resolved_by_mutual_certificate_closure
resolved_by_reciprocal_deadline_signature_correction
resolved_by_oriented_endpoint_chain_closure
unresolved_by_certificate_pair_not_closed
unresolved_by_reset_endpoint_crosses_orientation
unresolved_by_missing_lower_certificate
unresolved_by_missing_upper_certificate
gmp_interval_backend_required
```

The current official rungs emit:

```text
rsa_v2_40bit_static_001 -> resolved_by_reciprocal_deadline_signature_correction
rsa_v2_50bit_static_001 -> resolved_by_oriented_endpoint_chain_closure
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

The next algorithmic target is scale extension of the same public correction
rule. The invariant must stay derived from public `N`, PGSPG certificate fields,
and floor-map transport. It must not use product closure, divisibility, audit
factors, factor APIs, primality APIs, random generation, or fallback search.
