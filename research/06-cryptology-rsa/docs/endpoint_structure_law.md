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

### Strict Reset Closure

Strict reset closure resolves when floor transport images match reset endpoints
both ways and reset signatures match.

### Deadline-Signature Correction

When strict reset closure fails, one public deadline correction is applied. The
corrected structural endpoint class resolves when reciprocal floor transport and
signature equality hold under the corrected lower certificate and upper deadline.

### Refined Closure Acceptance

A base closure candidate is accepted only after the matched lower certificate
and the upper certificate pass public certificate-geometry filters.

## Confirmed Row

The official 40-bit RSA v2 rung resolves by deadline-signature correction:

```text
case_id = rsa_v2_40bit_static_001
N = 1099507433251
c = 1048559
d = 1048589
closure_status = resolved_by_reciprocal_deadline_signature_correction
```

## Current Boundary (50-bit)

The official 50-bit RSA v2 rung reaches a mutual certificate closure candidate
inside the endpoint chain, but refined public geometry rejects that candidate.
The **v2 runner** returns an **unresolved** structural state (no public endpoint class):

```text
case_id = rsa_v2_50bit_static_001
endpoint_chain_steps = 350
rejected_candidate = (32047651, 32059633)
rsa-v2 residual pin = unresolved_by_reciprocal_carrier_misalignment
```

**rsa-v3 residual refinement (same fixture):** dual-gap D holds
on the public carrier transport; residual migrates first to
`unresolved_by_first_tail_misalignment`, then to joint residual cell
`unresolved_by_joint_cell_C1T2L1` with residual vector R = (1, 2, 1) and
pinch_S = 54. Residual maps remain hypothesis. See
`experiments/live-solver/rsa-v3/output/residual_cell_C1T2L1/` and
`experiments/live-solver/rsa-v3/RESIDUAL_TAXONOMY.md`.

**V3 update (2026-08-07):** carrier reciprocal closure finds public pair
`(32047633, 32059651)` with `N//L == U` and `N//U == L`. Emitted under
`resolved_by_carrier_reciprocal_closure`. Status: measured-on-regime-only /
hypothesis. Not a theorem. Not a factorisation claim. First-tail window fixed.
See `experiments/live-solver/rsa-v3/residual_discriminator_v2/` and
`experiments/live-solver/rsa-v3/output/DOCUMENTATION_LOCK_50BIT_V3.md`.

The official 64-bit RSA v2 rung resolves by mutual closure:

```text
case_id = rsa_v2_64bit_static_001
closure_status = endpoint_class_by_mutual_certificate_closure
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

Do not start from Shor, classical factoring speed, candidate search, product
closure, gcd, divisibility, or audit factors.
