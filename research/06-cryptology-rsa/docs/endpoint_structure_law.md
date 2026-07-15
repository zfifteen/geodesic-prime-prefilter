# RSA Endpoint Structure Law

## Strongest Supported Claim

RSA moduli do expose deterministic endpoint structure.

The active RSA v2 artifact defines one public endpoint-structure law over a
transported certificate chain. The law is not a faster factoring method, a Shor
optimization, a candidate search, or an audit trick. It is a public PGS
endpoint-class resolver.

## Active Law

Let `N` be public and let:

```text
s = floor(sqrt(N))
```

The first lower-chain state begins at:

```text
a0 = previous_public_endpoint_before(s)
L0 = PGSPG reset certificate at a0
```

For any lower-chain state `a`, let:

```text
L = PGSPG reset certificate at a
r0 = L.reset_endpoint
sigma0 = L.reset_signature
```

Choose the oriented transport coordinate:

```text
x = r0       if r0 <= s
x = L.anchor otherwise
```

Transport `x` through the public reciprocal floor map:

```text
y = floor(N / x)
```

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

When strict reset closure fails at the current chain state, the single public
deadline correction is:

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
c < a
d > r1
floor(N / c) == d
floor(N / d) == c
sigma == sigma1
```

When those five conditions hold, the endpoint class is:

```text
(c, d)
```

### Refined Closure Acceptance

A base closure candidate is accepted only after the matched lower certificate
and the upper certificate pass public certificate-geometry filters.

For strict reset closure, the matched lower certificate is the current lower
certificate. For deadline-signature correction, it is the corrected lower
certificate. The active filters compare carrier transport, first-tail transport
when the matched lower deadline comes from the tail, lower lock placement for
nonzero chain closure, and active/unresolved profile counts.

If a base closure candidate fails one of these filters, the runner returns an
unresolved structural state at that chain position. It does not continue past a
rejected closure candidate to choose a later closure without an additional
public discriminator.

If neither strict reset closure nor deadline-signature correction resolves, the
runner moves to the previous lower public endpoint and repeats the same state
construction. The square-root chamber is step zero of this chain, not a
separate pre-chain mode.

### Endpoint-Chain Boundary

The runner walks the lower public endpoint chain outward inside the public
balance interval:

```text
lower_bound = floor(s / 2)
```

The walk has a deterministic stop condition: it ends at `floor(s / 2)`. It does
not use a fixed candidate radius, a retry ladder, product closure, divisibility,
`gcd`, primality APIs, hidden factors, or audit endpoints.

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
{"N": "1099507433251", "bits": 40, "case_id": "rsa_v2_40bit_static_001", "endpoint_class_lower": "1048559", "endpoint_class_upper": "1048589", "public_closure_status": "endpoint_class_by_reciprocal_deadline_signature_correction", "public_structure_found": true, "rule_id": "reciprocal_pgs_certificate_pair_v2", "status": "public_endpoint_class_found"}
```

## Current Boundary

The official 50-bit RSA v2 rung reaches a mutual certificate closure candidate
inside the endpoint chain, but refined public geometry rejects that candidate.
The runner returns an **unresolved** structural state (no public endpoint class):

```text
case_id = rsa_v2_50bit_static_001
endpoint_chain_steps = 350
rejected_candidate = (32047651, 32059633)
rsa-v2 residual pin = unresolved_by_reciprocal_carrier_misalignment
```

**rsa-v3 residual refinement (same fixture, still unresolved):** dual-gap D holds
on the public carrier transport; residual migrates first to
`unresolved_by_first_tail_misalignment`, then to joint residual cell
`unresolved_by_joint_cell_C1T2L1` with residual vector R = (1, 2, 1) and
pinch_S = 54. Residual maps remain hypothesis. See
`experiments/live-solver/rsa-v3/output/residual_cell_C1T2L1/` and
`experiments/live-solver/rsa-v3/RESIDUAL_TAXONOMY.md`.

The official 64-bit RSA v2 rung resolves by the same mutual closure predicate
plus the refined public certificate-geometry filters, and audit confirms the
emitted endpoint class as the factor pair:

```text
case_id = rsa_v2_64bit_static_001
closure_status = endpoint_class_by_mutual_certificate_closure
endpoint_chain_steps = 1162
endpoint_class = (3221225473, 3221275501)
factor_found = true
```

These are structural endpoint classes. Exact factor-pair confirmation remains a
separate downstream audit role and is not an inference predicate.

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
Return to reciprocal deadline-signature correction, oriented endpoint-chain closure, and the generated endpoint rows.
```

## Archive Note

The former PGS-Shor HTML documentation is archived because it distracts from the
RSA-native endpoint law:

```text
research/06-cryptology-rsa/archive/2026-05-13-shor-order-entropy-sidecar/
```

The archived material remains useful as downstream comparison context. It is no
longer the active entrypoint for RSA v2 endpoint-structure research.
