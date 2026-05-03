# RSA v2 PGSPG Certificate Contract

The live unit of inference is a PGSPG reset certificate, not an endpoint found
by walking a budgeted list.

## Certificate

A certificate is derived from one public previous-endpoint anchor.

It contains:

- `anchor`;
- `reset_endpoint`;
- `gap_offset`;
- `candidate_bound`;
- `active_count`;
- `resolved_count`;
- `unresolved_count`;
- `closed_offsets_before_q`;
- `carrier_w`;
- `carrier_d`;
- `lock_carrier_offset`;
- `lock_carrier_d`;
- `lower_d_threat_offset`;
- `tail_after_reset_offsets`;
- `reset_deadline_value`;
- `reset_deadline_margin`;
- `reset_signature`.

The certificate is copied from PGSPG chamber-reset state. It is not an
answer-bearing fixture.

## Reciprocal Certificate Pair

For a public modulus `N`, a lower certificate is transported by:

```text
y = floor(N / lower.reset_endpoint)
```

The upper certificate is derived from the previous endpoint before `y`.

This creates a reciprocal certificate pair:

```text
lower previous endpoint -> lower reset endpoint
upper previous endpoint -> upper reset endpoint
```

## Allowed Transport Facts

Inference may compute:

- `floor(N / anchor)`;
- `floor(N / reset_endpoint)`;
- `floor(N / reset_deadline_value)`;
- differences between transported reset and deadline images;
- equality of public transported coordinates.

Inference must not compute:

- `N % x`;
- `gcd(N, x)`;
- `x * y == N` as a selection predicate;
- audit-factor comparisons;
- factor or primality API results.

## Stopping Conditions

The certificate runner may stop only with one of these states:

```text
resolved_by_mutual_certificate_closure
unresolved_by_certificate_pair_not_closed
unresolved_by_missing_lower_certificate
unresolved_by_missing_upper_certificate
gmp_interval_backend_required
```

The current implementation is expected to emit unresolved rows until the
transported certificate-closure invariant is strong enough to certify a unique
pair before audit.

## Current Closure Candidate

The first closure candidate is intentionally strict.

It requires:

1. lower and upper certificates exist;
2. both reset endpoints are produced by PGSPG;
3. the lower reset endpoint transports to the upper reset endpoint;
4. the upper reset endpoint transports to the lower reset endpoint;
5. reset signatures match.

This candidate is not final. It is a measurable starting point for deriving the
transported deadline invariant.

## Failure Discipline

If the closure candidate does not hold, return unresolved.

Do not add a search budget, a wider walk, a product check, or a fallback.
