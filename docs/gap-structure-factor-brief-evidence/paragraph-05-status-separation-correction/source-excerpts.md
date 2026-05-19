# Paragraph 05 Source Excerpts

## Source: RSA Experiments Route Map

Path: `research/06-cryptology-rsa/experiments/README.md`

Line evidence:

- `31-37`: keeps invalidated solver shapes and archive material separate from
  live inference.
- `39-49`: defines `resolved` as at least one public factor found and then
  checked by audit.
- `51-52`: keeps sidecars diagnostic unless promoted by a public theorem.

## Source: Audit Script

Path: `research/06-cryptology-rsa/experiments/live-solver/rsa-v2/audit_experiment.py`

Line evidence:

- `42-53`: computes public structure separately from `factor_found`.
- `55-67`: emits public endpoint fields and audit factor fields separately.

## Source: Tests

Path: `research/06-cryptology-rsa/tests/test_rsa_v2_scripts.py`

Line evidence:

- `900-907`: checks factor and public-structure results across rows.
- `910-925`: asserts that `factor_found` means at least one actual factor.

