# Documentation Lock: 50-bit Carrier Reciprocal Breakthrough

Updated: 2026-08-07  
Status: measured-on-regime-only / hypothesis. No 10^18 surface claim. PROOF.md untouched.

## Summary of V2 → V3 transition

V2 named the exact residual geometry of the 50-bit joint cell C1T2L1 under residual code joint_cell_C1T2L1_v2_tail_boundary_lock_quarter_S54. All ordered tail offsets (first and secondary, both directions) miss the fixed window [-12, 6].

V3 discovers a public reciprocal floor pair from the GWR carrier itself:

- L = 32047633 (carrier_w)
- U = N // L = 32059651
- N // U returns L exactly
- remainder = 6170868
- delta_c = 30 ≤ boundD = 45
- both reset signatures contain deadline=tail
- pair is not the historical false class (32047651, 32059633)

The same closure_status used by the 40-bit golden is therefore available: endpoint_class_by_reciprocal_deadline_signature_correction. The first-tail window stays fixed. No classical gates enter the inference path.

## Why tail-only fails

Lower→upper deltas on the 50-bit pin: -22, -26, -40, -80, -86, -98.  
Upper→lower deltas: -36, -50, -74, -78, -90, -104.  
None land inside [-12, 6]. Secondary transport therefore cannot close the residual under the existing first-tail contract.

## Why carrier reciprocal works

The carrier is already a PGS object (GWR leftmost minimum). Floor transport of that single integer yields a reciprocal partner that satisfies the verifier’s mutual-floor test and the dual-gap bound. The historical false pair is blocked by an explicit anti-admission set. The resulting candidate is therefore admissible under the reciprocal-deadline signature correction path.

## What remains pending

- Integration of the v3 probe logic into resolver.py (still additive only).
- Full local pytest research/06-cryptology-rsa/tests/test_a1_* -q (pending complete checkout).
- Human review before any promotion of residual geometry language into PROOF.md.

## Contract statements that stay true

- First-tail window fixed at [-12, 6].
- No gcd, no modulus divisibility selectors, no primality APIs inside the probe inference path.
- Status language remains measured-on-regime-only / hypothesis.
- PROOF.md is not modified by this documentation lock.
