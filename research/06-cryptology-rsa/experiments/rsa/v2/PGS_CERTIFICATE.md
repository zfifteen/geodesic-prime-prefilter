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

If reset closure fails after the upper certificate exists, the runner may use
one induced correction:

```text
z = floor(N / upper.reset_endpoint)
c = previous public endpoint before z
d = upper.reset_deadline_value
```

The corrected lower endpoint `c` is certified by deriving the PGSPG certificate
at `c`. The upper endpoint `d` is the public deadline field of the upper
certificate.

## Allowed Transport Facts

Inference may compute:

- `floor(N / anchor)`;
- `floor(N / reset_endpoint)`;
- `floor(N / reset_deadline_value)`;
- the previous public endpoint before a transported certificate coordinate;
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
resolved_by_reciprocal_deadline_signature_correction
unresolved_by_certificate_pair_not_closed
unresolved_by_reset_endpoint_crosses_orientation
unresolved_by_missing_lower_certificate
unresolved_by_missing_upper_certificate
gmp_interval_backend_required
```

The current implementation resolves only when reset closure or deadline
signature correction certifies a unique public pair before audit.

## Current Closure Rules

The reset closure branch is strict.

It requires:

1. lower and upper certificates exist;
2. the lower reset endpoint remains on the lower side of `floor(sqrt(N))`;
3. both reset endpoints are produced by PGSPG;
4. the lower reset endpoint transports to the upper reset endpoint;
5. the upper reset endpoint transports to the lower reset endpoint;
6. reset signatures match.

The deadline signature correction branch applies only after reset closure fails
and requires:

1. the upper certificate exists;
2. the failed upper reset transports to a lower-side coordinate;
3. the previous public endpoint before that coordinate has a PGSPG certificate;
4. the upper reset deadline mutually closes with that corrected lower endpoint;
5. the corrected-lower and upper reset signatures match;
6. the correction moves outward from the original reset pair.

## Failure Discipline

If neither closure rule holds, return unresolved.

Do not add a search budget, a wider walk, a product check, or a fallback.
