# RSA Endpoint Structure Law

## Strongest Supported Claim

RSA moduli do expose deterministic endpoint structure.

The active RSA v2 artifact already defines one public endpoint-structure law:
reciprocal deadline-signature correction. The law is not a faster factoring
method, a Shor optimization, a candidate search, or an audit trick. It is a
public PGS endpoint-class resolver.

## Active Law

Let `N` be public and let:

```text
s = floor(sqrt(N))
```

Let `L0` be the PGSPG reset certificate at the previous public endpoint before
`s`. Write:

```text
a0 = L0.anchor
r0 = L0.reset_endpoint
```

Transport `r0` through the public reciprocal floor map:

```text
y = floor(N / r0)
```

Let `U` be the PGSPG reset certificate at the previous public endpoint before
`y`. Write:

```text
a1 = U.anchor
r1 = U.reset_endpoint
d = U.reset_deadline_value
sigma1 = U.reset_signature
```

Strict reset closure resolves when:

```text
floor(N / r0) == r1
floor(N / r1) == r0
L0.reset_signature == sigma1
```

When strict reset closure fails, the deadline correction is:

```text
z = floor(N / r1)
c = previous_public_endpoint_before(z)
L = PGSPG_certificate(c)
sigma = L.reset_signature
```

The corrected endpoint class resolves exactly when:

```text
c < a0
d > r1
floor(N / c) == d
floor(N / d) == c
sigma == sigma1
```

When those five conditions hold, the endpoint class is:

```text
(c, d)
```

If any condition fails, the public state is unresolved. No search budget,
product check, divisibility test, audit endpoint, hidden factor, or fallback
path enters the law.

## Confirmed Row

The official 40-bit RSA v2 rung resolves under this law:

```text
case_id = rsa_v2_40bit_static_001
N = 1099507433251
c = 1048559
d = 1048589
closure_status = resolved_by_reciprocal_deadline_signature_correction
```

The generated inference row emits:

```json
{"N": "1099507433251", "bits": 40, "case_id": "rsa_v2_40bit_static_001", "p": "1048559", "q": "1048589", "rule_id": "reciprocal_pgs_certificate_pair_v2", "status": "resolved"}
```

## Current Boundary

The official 50-bit RSA v2 rung remains unresolved:

```text
case_id = rsa_v2_50bit_static_001
closure_status = unresolved_by_certificate_pair_not_closed
```

This is not a failure of the law. It is the current unresolved boundary under
the live public rule.

## Work Discipline

Start RSA endpoint work from the resolver predicate and generated rows:

```text
code predicate -> public certificate fields -> emitted endpoint rows -> audit status -> theorem boundary
```

Do not start from:

```text
Shor
classical factoring speed
candidate search
product closure
gcd
divisibility
audit factors
```

Shape warning:

```text
Shape feels wrong: this is translating deterministic endpoint-structure research back into a Shor, classical factoring, or candidate-testing frame.
```

Corrective action:

```text
Return to reciprocal deadline-signature correction and explain the endpoint law already present in the code and generated outputs.
```

## Archive Note

The former PGS-Shor HTML documentation is archived because it distracts from the
RSA-native endpoint law:

```text
research/06-cryptology-rsa/archive/2026-05-13-shor-order-entropy-sidecar/
```

The archived material remains useful as downstream comparison context. It is no
longer the active entrypoint for RSA v2 endpoint-structure research.
