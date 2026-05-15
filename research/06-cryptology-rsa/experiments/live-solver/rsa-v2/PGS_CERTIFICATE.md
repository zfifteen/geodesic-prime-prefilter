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

For a public modulus `N`, each lower-chain certificate is transported by an
oriented coordinate:

```text
y = floor(N / x)
x = lower.reset_endpoint  when lower.reset_endpoint <= floor(sqrt(N))
x = lower.anchor          otherwise
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

The runner walks the lower public endpoint chain inside the public balance
interval and applies the same closure predicates at each lower-chain
certificate. The first endpoint before `floor(sqrt(N))` is step zero of this
same chain, not a separate square-root chamber mode.

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
endpoint_class_by_mutual_certificate_closure
endpoint_class_by_reciprocal_deadline_signature_correction
endpoint_class_by_oriented_endpoint_chain_closure
unresolved_by_certificate_pair_not_closed
unresolved_by_endpoint_chain_boundary
unresolved_by_endpoint_chain_cycle
unresolved_by_missing_lower_certificate
unresolved_by_missing_upper_certificate
```

The current implementation resolves only when reset closure or deadline
signature correction certifies a unique public pair before audit.

## Current Closure Rules

The reset closure predicate is strict and is evaluated at every lower-chain
state.

It requires:

1. lower and upper certificates exist;
2. both reset endpoints are produced by PGSPG;
3. the lower reset endpoint transports to the upper reset endpoint;
4. the upper reset endpoint transports to the lower reset endpoint;
5. reset signatures match.

The deadline signature correction branch applies only after reset closure fails
and requires:

1. the upper certificate exists;
2. the failed upper reset transports to a lower-side coordinate;
3. the previous public endpoint before that coordinate has a PGSPG certificate;
4. the upper reset deadline mutually closes with that corrected lower endpoint;
5. the corrected-lower and upper reset signatures match;
6. the correction moves outward from the original reset pair.

The lower endpoint chain advances from the previous public endpoint before
`floor(sqrt(N))` down to `floor(floor(sqrt(N)) / 2)`. At each step, strict
reset closure is evaluated first. If strict reset closure fails,
deadline-signature correction is evaluated next. The first public endpoint
whose closure predicate succeeds emits a structural endpoint class.

## Failure Discipline

If none of the closure rules holds before the lower balance boundary, return
unresolved.

Do not add a product check, divisibility test, hidden-factor comparison, or
fallback.
