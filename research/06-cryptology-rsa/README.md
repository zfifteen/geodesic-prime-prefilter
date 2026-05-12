# Cryptology And RSA

## Object

RSA v2/v3, modulus-link, semiprime, reciprocal closure, structural
certificates, and unresolved survivor states.

Primary homes:

- `experiments/rsa/v2/`
- `experiments/rsa/v3/`
- `docs/research/cryptology/`
- `docs/research/semiprime_branch/`
- `output/semiprime_branch/`
- `output/batch_modular_factor_closure_probe/`
- `output/batch_modular_factor_closure_probe_f50000/`
- `benchmarks/python/predictor/pgs_semiprime_backward_*.py`
- `benchmarks/python/predictor/batch_modular_factor_closure_probe.py`

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

RSA v2 currently records certificate-pair probes whose output summary remains
unresolved by the certificate pair:

```text
closure_status: unresolved_by_certificate_pair_not_closed
```

Semiprime backward-law surfaces live under `output/semiprime_branch/`. They are
measured search surfaces and do not constitute factorization results.

## Audit Status

Focused RSA validation passed during Phase 5 finalization:

```text
python3 -m pytest tests/python/test_rsa_v2_scripts.py tests/python/test_rsa_v2_transported_story_law.py tests/python/test_rsa_v2_certificate_commitment_story.py tests/python/predictor/test_pgs_semiprime_backward_law_search.py tests/python/predictor/test_pgs_semiprime_backward_transition_law_search.py tests/python/predictor/test_toy_modulus_backward_chamber_lock.py
102 passed in 248.72s
```

## Invalidated Rules

No unresolved survivor, residual, or blocker state was converted into a
factorization result by this reorganization.

## Unresolved State

The RSA v2 certificate-pair state remains unresolved where the artifacts say
it is unresolved. Scaling remains blocked unless a PGS-native invariant closes
the survivor state without resolver logic.

## Reproduce

Run the focused RSA validation command listed in Audit Status.

## Provenance

Created as a skeleton in Phase 1. Finalized as a mapped cryptology chapter in
Phase 5 of the repository reorganization.
