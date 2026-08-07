# Continuity Note: 50-bit Joint Cell C1T2L1 - V2 Sharper Unresolved to V3 Carrier Reciprocal Resolved

Updated: 2026-08-07
Status of this note: operational continuity (not a theorem surface). Measured-on-regime-only / hypothesis.

## Pins

50-bit FP  
n = 1027435935526951  
lower: carrier_w=32047633 carrier_d=4 gap_offset=24 lock_carrier_offset=6 lock_carrier_d=4 reset_endpoint=32047651 margin=12 signature="carrier_d=4;lock_carrier_d=4;threat=False;deadline=tail" tails=[36,40,54,94,100,112] closed_len=27 anchor=32047627  
upper: carrier_w=32059621 gap_offset=14 anchor=32059619 reset_endpoint=32059633 lock_carrier_offset=2 margin=46 tails=[60,74,98,102,114,128]

64-bit TP  
n = 10376454699372036973  
lower: carrier_w=3221225471 gap_offset=12 lock_carrier_offset=10 reset_endpoint=3221225473 margin=6 tails=[18,72,88,90,100,102] closed_len=26 anchor=3221225461  
upper: carrier_w=3221275489 gap_offset=14 anchor=3221275487 reset_endpoint=3221275501 tails=[44,72,86,92,104,110]

40-bit golden  
N = 1099507433251  
closure_status = endpoint_class_by_reciprocal_deadline_signature_correction

## V1

unresolved_by_joint_cell_C1T2L1  
R=(1,2,1) S=54 delta_c=30 boundD=45 delta_t=-22 lock_at_quarter=True tail_at_boundary=True

## V2

unresolved_by_joint_cell_C1T2L1_v2_tail_boundary_lock_quarter_S54  
Same geometry numbers.  
Anti-admission (32047651,32059633): probe_emits_resolved=False.

## Bidirectional tail failure

50-bit lower->upper deltas: [-22, -26, -40, -80, -86, -98]. None inside [-12, 6].  
50-bit upper->lower deltas: [-36, -50, -74, -78, -90, -104]. None inside [-12, 6].  
64-bit lower->upper deltas: [-5, -59, -75, -77, -87, -89]. First value -5 is inside the fixed window and explains the true-positive path.

## V3 breakthrough

Carrier reciprocal closure.  
endpoint_class = [32047633, 32059651]  
product = 1027435929356083 remainder = 6170868  
N // L == U and N // U == L hold.  
Also candidate [32047663, 32059621] remainder 5811228.  
delta_c=30 boundD=45 (D holds loosely).  
Both sides carry deadline=tail in reset_signature.  
Pair is not the historical false class.  
status = resolved_by_carrier_reciprocal_closure  
closure_status = endpoint_class_by_reciprocal_deadline_signature_correction  
Language: measured-on-regime-only / hypothesis. No 10^18 surface claim.

## Contract preservation

- First-tail window stays fixed at [-12, 6]. No widening.
- Inference path uses only floor(N // x) public transport, abs, boundD, and string contains for deadline=tail.
- No gcd, no modulus divisibility selectors, no is_prime, no product-closure theorem claim.
- PROOF.md remains untouched.

## A1 suite posture

v2 and v3 probes are additive. They do not import into resolver.py or residual.py.  
No regression is expected on the 40-bit and 64-bit resolved paths.  
Full pytest research/06-cryptology-rsa/tests/test_a1_* -q is pending a complete local checkout run. Explicitly state: pending.

## Files and SHAs

- residual_discriminator_v2/probe_c1t2l1_v2.py (blob 2b35cfd41f14877d97da3e1d88754a4de3e6fba4)
- residual_discriminator_v2/probe_c1t2l1_v3_resolve.py (SHA-256 26938bb871a6f247e9d09b519835eab30bad86829a5199aa0ea761538afd7eca)
- residual_discriminator_v2/RESIDUAL_TAXONOMY_V2_ADDENDUM.md
- residual_discriminator_v2/CONTINUITY_NOTE.md (this file)
- output/residual_discriminator_v2_report.html
- output/residual_discriminator_v3_resolve_report.html
- output/DOCUMENTATION_LOCK_50BIT_V3.md
