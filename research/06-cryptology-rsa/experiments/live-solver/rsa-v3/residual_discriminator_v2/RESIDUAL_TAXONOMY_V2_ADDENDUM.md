# Residual Taxonomy V2 Addendum (A1 / rsa-v3)

Status: hypothesis residual map. Measured on named pins only.
No residual-family 10^18 surface. Not a theorem.

This addendum does not overwrite RESIDUAL_TAXONOMY.md. It extends the residual vocabulary for the C1T2L1 joint cell.

| Code | Meaning | Required diagnostics |
| --- | --- | --- |
| `unresolved_by_joint_cell_C1T2L1_v2_tail_boundary_lock_quarter_S54` | Joint cell C1T2L1 sub-cell where tail sits at the -22 boundary (just outside the [-21, -13] rank-1 band), lock sits at the exact quarter threshold (lock == gap // 4), carrier is loose (20 < delta_c <= boundD), pinch S >= 50, and dual-gap D holds loosely. | R, S, delta_c, delta_t, boundD, lock_at_quarter, tail_at_boundary |
| `unresolved_by_joint_cell_C1T2L1_v2_generic` | Joint cell C1T2L1 without the exact tail-boundary + lock-quarter + S>=50 conjunction. | R, S, delta_c, delta_t, boundD |

## Contract notes

- Both codes remain unresolved. They do not emit a public endpoint class.
- First-tail window stays fixed at [-12, 6]. No widening.
- Inference path uses only public floor transport, residual ranks, reset-signature containment, and lock/gap arithmetic.
- Forbidden inside inference: gcd, divisibility selectors, product closure, primality APIs.
- Historical false class (32047651, 32059633) stays anti-admitted.
