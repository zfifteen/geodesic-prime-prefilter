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

Let:

```text
a0 = previous_public_endpoint_before(s)
L0 = PGSPG reset certificate at a0
r0 = L0.reset_endpoint
sigma0 = L0.reset_signature
```

Transport `r0` through the public reciprocal floor map:

```text
y = floor(N / r0)
```

This transport is valid only when:

```text
r0 <= s
```

If `r0 > s`, then the lower certificate remains valid but its reset endpoint
has crossed the square-root orientation boundary. It is not a lower-side
transport coordinate, so the public state is:

```text
unresolved_by_reset_endpoint_crosses_orientation
```

No upper certificate is induced in that state.

Let:

```text
a1 = previous_public_endpoint_before(y)
U0 = PGSPG reset certificate at a1
r1 = U0.reset_endpoint
d = U0.reset_deadline_value
sigma1 = U0.reset_signature
```

The reset endpoint `r1` is the upper certificate's first reset endpoint. The
deadline value `d` is the first public upper-side boundary after `r1` where the
certificate's reset freedom ends. It is computed from the certificate's first
tail offset, first lower-divisor threat offset, or candidate bound, whichever
arrives first.

### Strict Reset Closure

Strict reset closure resolves when:

```text
floor(N / r0) == r1
floor(N / r1) == r0
sigma0 == sigma1
```

When those three conditions hold, the endpoint class is:

```text
(r0, r1)
```

### Deadline-Signature Correction

When strict reset closure fails, the single public deadline correction is:

```text
z = floor(N / r1)
c = previous_public_endpoint_before(z)
L = PGSPG reset certificate at c
sigma = L.reset_signature
```

The correction is asymmetric by construction. The lower side is corrected by
moving to the previous public endpoint before the transported failed upper
reset. The upper side moves from its failed reset endpoint `r1` to its own
certificate deadline `d`. This is the deadline-signature law: the upper
certificate supplies the deadline, and the lower corrected certificate must
carry the same reset signature.

The corrected structural endpoint class resolves exactly when:

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

If any condition fails, the public state is unresolved. The correction is one
step only; there is no loop and no widening walk.

The public law emits a structural endpoint class. It does not use `N mod c`,
`c * d == N`, `gcd`, audit endpoints, hidden factors, or a fallback path as an
inference predicate. Downstream audit may confirm that an emitted endpoint class
is the exact factor pair, but audit does not define the law.

## Confirmed Row

The official 40-bit RSA v2 rung resolves by deadline-signature correction:

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

The official 50-bit RSA v2 rung remains unresolved because its lower reset
endpoint crosses the orientation boundary:

```text
case_id = rsa_v2_50bit_static_001
closure_status = unresolved_by_reset_endpoint_crosses_orientation
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
