# Cryptology And RSA

## Object

RSA v2/v3, modulus-link, semiprime, reciprocal closure, structural
certificates, and unresolved survivor states.

Primary homes:

- `research/06-cryptology-rsa/experiments/live-solver/rsa-v2/`
- `research/06-cryptology-rsa/experiments/live-solver/rsa-v3/`
- `research/06-cryptology-rsa/docs/cryptology/`
- `research/06-cryptology-rsa/docs/endpoint_structure_law.md`
- `research/06-cryptology-rsa/docs/semiprime_branch/`
- `research/06-cryptology-rsa/archive/2026-05-13-shor-order-entropy-sidecar/`
- `research/06-cryptology-rsa/output/semiprime_branch/`
- `research/06-cryptology-rsa/output/batch_modular_factor_closure_probe/`
- `research/06-cryptology-rsa/output/batch_modular_factor_closure_probe_f50000/`
- `research/06-cryptology-rsa/scripts/pgs_semiprime_backward_*.py`
- `research/06-cryptology-rsa/scripts/batch_modular_factor_closure_probe.py`

## Invariant Or Rule

The required cryptology frame is:

```text
locked PGS endpoint chain -> floor transport through modulus -> reciprocal endpoint closure -> modulus-link residual -> structural certificate or unresolved state
```

Classical factorization, `gcd`, product closure, hidden factors, and primality
APIs are audit or comparison tools only. They are not PGS inference mechanisms.

## Proof Status

No RSA-scale resolver theorem is claimed in this chapter.

## Endpoint Structure Law

RSA moduli do expose deterministic endpoint structure. The live RSA v2 law is
reciprocal deadline-signature correction:

```text
z = floor(N / upper.reset_endpoint)
c = previous_public_endpoint_before(z)
d = upper.reset_deadline_value

resolve iff:
  c < lower.anchor
  d > upper.reset_endpoint
  floor(N / c) == d
  floor(N / d) == c
  corrected_lower.reset_signature == upper.reset_signature
```

See `docs/endpoint_structure_law.md`.

## Measured Evidence

RSA v2 records public endpoint structure and a separate factor verdict on the
committed ladder:

```text
rsa_v2_40bit_static_001: factor_found = true
rsa_v2_50bit_static_001: factor_found = false
rsa_v2_64bit_static_001: factor_found = true
```

The 40-bit row is measured and audit-confirmed after public PGS endpoint-class
inference. The 64-bit row is measured and audit-confirmed after public mutual
certificate closure. The 50-bit row is unresolved before audit and emits no
public endpoint class.

256-bit expansion added rsa_v2_128bit_static_001 and rsa_v2_256bit_static_001
(curated from scaleup corpus). Both return unresolved_by_missing_lower_certificate
(C high-scale exercised via _c; no public endpoint class emitted, as expected baseline).
Old verdicts preserved. Real outputs from shipped run. See output/ and plan.html.

Erratum: earlier OECC_LINEAR_V1 and OECC_RECURSIVE_V2 wording used `resolved`
and `p` / `q` for audit-failing endpoint classes. That wording is invalidated.
The historical 50-bit mutual-closure result is a rejected public-structure
candidate, not a factor solve. The current live runner preserves the
audit-confirmed 64-bit endpoint class and rejects the 50-bit false positive.

The former PGS-Shor HTML documentation is archived at
`archive/2026-05-13-shor-order-entropy-sidecar/` because Shor is downstream
comparison context, not the active RSA v2 research object.

Semiprime backward-law surfaces live under `research/06-cryptology-rsa/output/semiprime_branch/`. They are
measured search surfaces and do not constitute factorization results.

## Audit Status

Focused RSA validation passed during Phase 5 finalization:

```text
python3 -m pytest research/06-cryptology-rsa/tests/test_rsa_v2_scripts.py research/06-cryptology-rsa/tests/test_rsa_v2_transported_story_law.py research/06-cryptology-rsa/tests/test_rsa_v2_certificate_commitment_story.py research/06-cryptology-rsa/tests/test_pgs_semiprime_backward_law_search.py research/06-cryptology-rsa/tests/test_pgs_semiprime_backward_transition_law_search.py research/06-cryptology-rsa/tests/test_toy_modulus_backward_chamber_lock.py
102 passed in 248.72s
```

## Invalidated Rules

No unresolved survivor, residual, blocker state, or public endpoint class is a
factorization result unless downstream audit reports `factor_found = true`.

## Unresolved State

The RSA v2 factor-pair state remains unresolved where the audit says
`factor_found = false`. The 50-bit row is unresolved before audit and is not a
factor solve. The active task is to find the PGS-native discriminator that
separates the factor endpoint class from rejected public closure candidates.

## Reproduce

Run the focused RSA validation command listed in Audit Status. For the live RSA
v2 endpoint law, run:

```text
python3 -m pytest research/06-cryptology-rsa/tests/test_rsa_v2_scripts.py -q
```

## Provenance

Created as a skeleton in Phase 1. Finalized as a mapped cryptology chapter in
Phase 5 of the repository reorganization.
