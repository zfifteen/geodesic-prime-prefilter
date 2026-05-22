# RSA v2 Reciprocal PGSPG Certificate Algorithm

This document defines the live v2 algorithm after the radius-first and
endpoint-budget scaffolds were withdrawn.

The current algorithm is a public reciprocal PGSPG endpoint-class instrument
for the exact-backend regime. It derives reciprocal certificate state and emits
public endpoint classes when certificate endpoints close under floor transport.
It does not claim that an endpoint class is the factor pair. Only downstream
audit reports whether factors were found.

Current implementation shape:

```text
UNIFIED_TRANSPORTED_CERTIFICATE_CHAIN
```

The historical linear baseline is documented in
`ORIENTED_ENDPOINT_CHAIN_BASELINE.md`. The live runner now applies the same
closure predicates inside one transported certificate-chain traversal.

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

## Stage 2: Initial Lower Anchor

Find the previous public endpoint before `isqrt(N)`.

This endpoint is the first lower-chain state. It is not a special chamber or a
separate pre-chain mode.

## Stage 3: Uniform Chain State

For each lower public endpoint in the chain, derive the PGSPG chamber-reset
certificate from that endpoint. The certificate contains the reset endpoint,
carrier state, closed offsets before reset, threat state, tail state, and
reset-deadline fields.

Choose the oriented lower transport coordinate.

When the lower reset endpoint still lies on the lower side of the square-root
orientation, the reset endpoint is the transport coordinate:

```text
x = lower.reset_endpoint  when lower.reset_endpoint <= isqrt(N)
```

If the lower reset endpoint is greater than `isqrt(N)`, the certificate is
valid but its reset endpoint has crossed the orientation boundary. It is not a
lower-side transport coordinate. In that chamber, the lower public anchor is
the transport coordinate:

```text
x = lower.anchor          when lower.reset_endpoint > isqrt(N)
```

Transport the oriented coordinate by:

```text
y = floor(N / x)
```

This is public reciprocal transport. It is not a divisibility test and does not
check product closure.

## Stage 4: Upper Certificate

Find the previous public endpoint before `y`.

Derive the PGSPG chamber-reset certificate from that endpoint.

## Stage 5: Closure Predicates

At each chain state, evaluate strict reset closure first. It resolves when:

1. both certificates exist;
2. `floor(N / lower.reset_endpoint) == upper.reset_endpoint`;
3. `floor(N / upper.reset_endpoint) == lower.reset_endpoint`;
4. lower and upper reset signatures match.

If strict reset closure fails and the upper certificate exists, evaluate one
public deadline-signature correction. Transport the upper reset endpoint back
to the lower side:

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

This predicate uses one reciprocal correction induced by the failed upper
certificate. It does not test divisibility, multiply candidate endpoints, read
audit factors, or walk a budgeted list of lower endpoints.

## Stage 6: Refined Closure Acceptance

A base closure candidate is not accepted until the matched lower certificate
also satisfies public certificate-geometry filters against the upper
certificate.

For strict reset closure, the matched lower certificate is the original lower
certificate. For deadline-signature correction, the matched lower certificate
is the corrected lower certificate, because that is the certificate whose
signature is compared to the upper certificate.

The current refined filters are:

```text
abs(floor(N / matched_lower.carrier_w) - upper.carrier_w)
  <= max(20, floor(1.2 * matched_lower.gap_offset))

if matched_lower uses deadline=tail:
  -12 <= floor(N / first_matched_lower_tail_point) - upper.anchor <= 6

for strict reset closure or nonzero endpoint-chain correction:
  2 * matched_lower.lock_carrier_offset > matched_lower.gap_offset
  matched_lower.active_count == upper.active_count
  matched_lower.unresolved_count == upper.unresolved_count
```

If a base closure candidate fails one of these public filters, the chain stops
with an unresolved structural state. It does not skip the rejected candidate and
continue to a later closure, because that would choose among multiple coherent
closure candidates without a public discriminator.

## Stage 7: Chain Transition

If neither closure predicate succeeds at the current lower endpoint, move to
the previous public endpoint before the current lower endpoint and repeat the
same state construction.

The current public balance boundary is:

```text
floor(isqrt(N) / 2)
```

The bound is an explicit public-region contract for this implementation, not a
bit-size branch. The runner also tracks visited lower endpoints and returns a
cycle status if the chain repeats.

This is endpoint-chain traversal over public PGS endpoints. It is not product
closure, divisibility testing, a fixed-radius candidate band, a hidden-factor
search, or a fallback after a separate square-root chamber mode.

## Current Status Fields

The runner emits `status = public_endpoint_class_found` when public reciprocal
structure closes. It emits `endpoint_class_lower` and `endpoint_class_upper`,
not `p` and `q`. Factor status is absent from inference output.

Audit emits:

```text
factor_found = true | false
```

The public closure status is one of:

```text
endpoint_class_by_mutual_certificate_closure
endpoint_class_by_reciprocal_deadline_signature_correction
endpoint_class_by_oriented_endpoint_chain_closure
unresolved_by_certificate_pair_not_closed
unresolved_by_endpoint_chain_boundary
unresolved_by_endpoint_chain_cycle
unresolved_by_first_tail_misalignment
unresolved_by_lower_lock_misalignment
unresolved_by_missing_lower_certificate
unresolved_by_missing_upper_certificate
unresolved_by_profile_count_mismatch
unresolved_by_reciprocal_carrier_misalignment
```

The current official rungs emit:

```text
rsa_v2_40bit_static_001 -> public endpoint class found, factor_found = true
rsa_v2_50bit_static_001 -> unresolved_by_reciprocal_carrier_misalignment
rsa_v2_64bit_static_001 -> public endpoint class found, factor_found = true
```

## Erratum: False-Resolution Wording

Earlier OECC output used `status = resolved` and factor-shaped `p` / `q`
fields for public endpoint classes. That wording was wrong. OECC_LINEAR_V1 and
OECC_RECURSIVE_V2 are historical baselines, not live status sources. The old
50-bit mutual-closure result is now rejected by refined public closure filters.
The 64-bit mutual certificate closure remains live and audit-confirmed. The old
`resolved` wording is invalidated terminology for public endpoint classes.

The unified chain runner supersedes the old OECC_LINEAR_V1 control shape. It
evaluates strict reset closure and deadline-signature correction at every lower
chain state. The refined closure filters reject the 50-bit mutual closure at
step 350 and preserve the 64-bit audit-confirmed mutual reset endpoint class.

## Explicitly Invalidated Rules

The following are not live rules:

- fixed-radius candidate bands around `isqrt(N)`;
- endpoint-walk budgets as solver coverage;
- raw equality of lower and upper reset-deadline margins;
- stationary recursive reset rounds;
- product closure as the contraction rule;
- audit factors as inference inputs.
- `status = resolved` for audit-failing public endpoint classes;
- `p` / `q` field names for non-audit inference output.

## Resolver Target

The next performance target is not a new resolver law. It is a faster traversal
that preserves the same first public closure emitted by the unified chain. Any
recursive or jump-based version must stay derived from public `N`, PGSPG
certificate fields, and floor-map transport. It must not use product closure,
divisibility, audit factors, factor APIs, primality APIs, random generation, or
fallback search.
