# Paragraph 04 Evidence: Current Live Runner

## Public Claim To Support

The current live runner has three committed ladder cases: the 40-bit and 64-bit
rows recover a factor endpoint after public endpoint inference and downstream
audit; the 50-bit row remains unresolved before audit.

## Supporting Evidence

- `research/06-cryptology-rsa/experiments/live-solver/rsa-v2/README.md`
  records current official rungs:
  - `rsa_v2_40bit_static_001 -> endpoint_class_by_reciprocal_deadline_signature_correction`
  - `rsa_v2_50bit_static_001 -> unresolved_by_reciprocal_carrier_misalignment`
  - `rsa_v2_64bit_static_001 -> endpoint_class_by_mutual_certificate_closure`
- The same README states that the runner does not read audit factors, and that
  downstream audit reports `factor_found = true` for the 40-bit and 64-bit
  rows while the 50-bit row remains unresolved before audit.
- `research/06-cryptology-rsa/experiments/live-solver/rsa-v2/output/audit_results.csv`
  records:
  - 40-bit: `factor_found=true`, `inference_audit_pass`
  - 50-bit: `factor_found=false`, `inference_audit_fail`
  - 64-bit: `factor_found=true`, `inference_audit_pass`
- `research/06-cryptology-rsa/experiments/live-solver/rsa-v2/output/inference_rows.jsonl`
  records public endpoint classes for the 40-bit and 64-bit rows and
  `status = unresolved` for the 50-bit row.

## Status Boundary

- Measured and implemented: current runner emits public inference rows.
- Audit-confirmed on committed fixtures: 40-bit and 64-bit factor endpoints.
- Unresolved: 50-bit fixture under the current live rule.
- Not claimed: general factorization theorem.

## Infographic Concept

A three-row ladder:
`40-bit -> public closure -> audit pass`,
`50-bit -> carrier misalignment -> unresolved`,
`64-bit -> mutual certificate closure -> audit pass`.
Use separate columns for public inference and downstream audit.

