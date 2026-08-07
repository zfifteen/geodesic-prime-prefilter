# Residual Taxonomy V2 Addendum (A1 / rsa-v3)

Status: hypothesis residual map. Measured on named pins only.
No residual-family 10^18 surface. Not a theorem.

This addendum does not overwrite RESIDUAL_TAXONOMY.md. It extends the residual vocabulary for the C1T2L1 joint cell and the carrier-reciprocal resolve path.

| Code | Meaning | Required diagnostics |
| --- | --- | --- |
| `joint_cell_C1T2L1_v2_tail_boundary_lock_quarter_S54` | Joint cell C1T2L1 sub-cell where tail sits at the -22 boundary (just outside the [-21, -13] rank-1 band), lock sits at the exact quarter threshold (lock == gap // 4), carrier is loose (20 < delta_c <= boundD), pinch S >= 50, and dual-gap D holds loosely. | R, S, delta_c, delta_t, boundD, lock_at_quarter, tail_at_boundary |
| `joint_cell_C1T2L1_v2_generic` | Joint cell C1T2L1 without the exact tail-boundary + lock-quarter + S>=50 conjunction. | R, S, delta_c, delta_t, boundD |
| `resolved_by_carrier_reciprocal_closure` | Public reciprocal floor pair found from GWR carrier (or ordered candidates) that satisfies N//L == U and N//U == L, lies within boundD of a carrier, carries deadline=tail on both signatures, and is not the historical false class. Emitted under closure_status endpoint_class_by_reciprocal_deadline_signature_correction. | R, S, delta_c, boundD, remainder, reciprocal_holds, historical_false_blocked, endpoint_class, closure_status, reset_signature |

## Condition for resolved_by_carrier_reciprocal_closure

R == (1, 2, 1)  
and lock_at_quarter  
and tail_at_boundary  
and S >= 50  
and there exists L in {carrier_w, anchor, reset_endpoint} union (reset_endpoint + tails)  
such that U = N // L and N // U == L  
and abs(U - upper.carrier_w) <= boundD  
and (L, U) is not (32047651, 32059633)  
and "deadline=tail" appears in the reset signature  
=> emit resolved.

## Contract notes

- V2 codes name residual geometry only. They do not emit a public endpoint class.
- V3 resolve code emits a candidate endpoint class under the reciprocal-deadline signature correction path.
- First-tail window stays fixed at [-12, 6]. No widening.
- Inference path uses only public floor transport, residual ranks, reset-signature containment, boundD, and lock/gap arithmetic.
- Forbidden inside inference: gcd, divisibility selectors, product-closure theorem claims, primality APIs.
- Historical false class (32047651, 32059633) stays anti-admitted.
- Status: measured-on-regime-only / hypothesis. Not a theorem. No 10^18 claim.
