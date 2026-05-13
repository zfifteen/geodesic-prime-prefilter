# Cryptology And RSA

## Object

RSA v2/v3, modulus-link, semiprime, reciprocal closure, structural
certificates, and unresolved survivor states.

Primary homes:

- `research/06-cryptology-rsa/experiments/rsa/v2/`
- `research/06-cryptology-rsa/experiments/rsa/v3/`
- `research/06-cryptology-rsa/docs/cryptology/`
- `research/06-cryptology-rsa/docs/shor_order_entropy/`
- `research/06-cryptology-rsa/docs/semiprime_branch/`
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

## Measured Evidence

The PGS-Shor order entropy sidecar records a measured collapse on the resolved
40-bit RSA v2 ladder rung:

```text
rsa_v2_40bit_static_001: 80 baseline phase bits -> 0 residual phase bits
rsa_v2_50bit_static_001: 100 baseline phase bits -> 100 residual phase bits
```

The 40-bit row is measured and audit-confirmed after public PGS endpoint-class
inference. The 50-bit row remains unresolved and preserves the ordinary Shor
burden. See `docs/shor_order_entropy/index.html`.

RSA v2 records mixed certificate-pair state on the committed ladder:

```text
rsa_v2_40bit_static_001: resolved_by_reciprocal_deadline_signature_correction
rsa_v2_50bit_static_001: unresolved_by_certificate_pair_not_closed
```

Semiprime backward-law surfaces live under `research/06-cryptology-rsa/output/semiprime_branch/`. They are
measured search surfaces and do not constitute factorization results.

## Audit Status

Focused RSA validation passed during Phase 5 finalization:

```text
python3 -m pytest research/06-cryptology-rsa/tests/test_rsa_v2_scripts.py research/06-cryptology-rsa/tests/test_rsa_v2_transported_story_law.py research/06-cryptology-rsa/tests/test_rsa_v2_certificate_commitment_story.py research/06-cryptology-rsa/tests/test_pgs_semiprime_backward_law_search.py research/06-cryptology-rsa/tests/test_pgs_semiprime_backward_transition_law_search.py research/06-cryptology-rsa/tests/test_toy_modulus_backward_chamber_lock.py
102 passed in 248.72s
```

## Invalidated Rules

No unresolved survivor, residual, or blocker state was converted into a
factorization result by this reorganization.

## Unresolved State

The RSA v2 certificate-pair state remains unresolved where the artifacts say
it is unresolved. The 50-bit order-entropy row remains unresolved. Scaling
remains blocked unless a PGS-native invariant closes the survivor state without
resolver logic.

## Reproduce

Run the focused RSA validation command listed in Audit Status. For the
PGS-Shor order entropy sidecar, run:

```text
python3 research/06-cryptology-rsa/experiments/rsa/v2/shor_order_entropy_probe.py
python3 -m pytest research/06-cryptology-rsa/tests/test_rsa_v2_scripts.py -q
```

## Provenance

Created as a skeleton in Phase 1. Finalized as a mapped cryptology chapter in
Phase 5 of the repository reorganization.
