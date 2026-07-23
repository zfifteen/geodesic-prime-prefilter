# Lean 4 sorry / axiom inventory

**As of:** 2026-07-23 (M4 closed on branch `lean/m4-ubc-psp`)  
**Command:** `rg -n 'sorry|axiom ' lean-4/PGS/*.lean`  
**DoD:** `DEFINITION_OF_DONE.md`

## Summary

| Kind | Count | Blocks milestone |
| --- | --- | --- |
| `sorry` in Basic | **0** | M1 **closed** |
| `axiom` in ChamberReset | **0** | M2 **closed** |
| `sorry` in GWR | **0** | M3 **closed** |
| empty-shell PSP | **removed** | M4 **closed** |
| `axiom` in Placement | **1** (`tau_prime_square_eq_three`) | audit premise (D3.2); not a UBC/PSP smuggle |

## Basic.lean

M1 closed: tau characterization path fully proved. D4.1 closed.

## ChamberReset.lean

M2 closed: replay axioms discharged. Empty-shell `prime_square_proximity_theorem` **removed**; non-vacuous PSP lives in `PGS/BoundedCompression.lean`. `near_root_exclusion_bound` remains proved geometric support for the square-branch spine.

## GWR.lean

M3 closed: `ordered_comparison` + `leftmost_min_tau_maximizer` (earlier side named hyp / square case discharged).

## BoundedCompression.lean (M4)

| Item | Notes | Target |
| --- | --- | --- |
| `dynamicCutoff` | `max(64, ⌈½ (log n)²⌉)` — non-vacuous C(n) | M4 done |
| `full_row_activation` | algebraic Step A: `d > C`, `m ≤ ⌊C/2⌋` ⇒ `2m < d` | M4 done |
| `two_mul_halfCutoff_le` | `2·⌊C/2⌋ ≤ C` | M4 done |
| `prime_square_proximity_theorem` | `r*r - p ≤ C(r*r)` under `SquareBranchCapacityContra` | M4 done (D4.4b) |
| `universal_bounded_compression` | `w - p ≤ C(q)` under base + residual + analytic packages | M4 done |
| `ubc_of_finite_base` | `q < 8_886_111` ⇒ ≤60 ≤ C(q) from `BoundedCompressionBaseV1` | M4 done |
| `ubc_square_from_psp` | PSP + mono lifts square branch to `C(q)` | M4 done |
| `dynamicCutoff_mono` | cutoff monotone for `1 < a ≤ b` | M4 support |
| Named hyps | `BoundedCompressionBaseV1`, `GwrFiniteBaseV1`, `ResidualK128Premise`, `SquareBranchCapacityContra`, `AnalyticUBCClosure` | D3.2 / D4.6 packaging |

**Honesty:** Finite bases and Corollary 4c.3 capacity discharge are **named premises** matching PROOF.md certificates; Lean does not re-run exhaustions or `audit_square_branches.py`. Bound shape is concrete `C(n)`, not `∃ C, dist ≤ C := dist`.

## Placement.lean

| Item | Notes | Target |
| --- | --- | --- |
| `axiom tau_prime_square_eq_three` | CL-003 classical import; **audit premise only** (D3.2) | stays labeled; does not smuggle UBC/PSP |

## NextPrime.lean

`weak_lfcl_sufficient_bound` proved (M2).

## Update rule

After each milestone PR/commit: re-run ripgrep, refresh this table, bump “As of”, note SHA if committed.

*M4 CLOSED (2026-07-23). Non-vacuous UBC + PSP under named finite/analytic premises; empty shell removed.*
