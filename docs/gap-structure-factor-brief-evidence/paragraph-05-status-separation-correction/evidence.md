# Paragraph 05 Evidence: Status Separation Correction

## Public Claim To Support

A major accomplishment was cleaning up the language: finding endpoint structure
is not the same thing as finding a factor. The branch now separates public
structure, factor recovery, and audit confirmation.

## Supporting Evidence

- `research/06-cryptology-rsa/experiments/README.md` states the current
  terminology: `resolved` means at least one factor was found by the public
  inference mechanism and then checked downstream by audit.
- The same file states that sidecars describe pressure, blockers, and
  diagnostics, and do not participate in live inference unless promoted by a
  public theorem.
- `research/06-cryptology-rsa/experiments/live-solver/rsa-v2/audit_experiment.py`
  computes `factor_found` by comparing public endpoint classes against audit
  factors after inference.
- `research/06-cryptology-rsa/tests/test_rsa_v2_scripts.py` contains
  `test_audit_factor_found_means_at_least_one_factor`, preserving the contract
  that `factor_found` requires at least one actual factor endpoint.
- Relevant commits:
  - `cbb330b7` - Fix RSA v2 factor reporting semantics
  - `c7c4d755` - Refine RSA v2 closure acceptance and unresolved statuses

## Status Boundary

- Corrected: stale wording that treated endpoint classes as solved factors.
- Live contract: public inference emits structure or unresolved state.
- Audit role: confirms whether the emitted public structure includes a factor.

## Infographic Concept

Three stacked labels with gates between them:
`public structure found` -> `factor endpoint present?` -> `audit confirms`.
The middle gate is the important correction.

