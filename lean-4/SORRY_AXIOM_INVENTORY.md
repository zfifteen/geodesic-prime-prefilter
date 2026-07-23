# Lean 4 sorry / axiom inventory

**As of:** 2026-07-23 (M3 closed on `main`, merge `1cfb5e5e` / PR #60)  
**Command:** `rg -n 'sorry|axiom ' lean-4/PGS/*.lean`  
**DoD:** `DEFINITION_OF_DONE.md`

## Summary

| Kind | Count | Blocks milestone |
| --- | --- | --- |
| `sorry` in Basic | **0** | M1 **closed** |
| `axiom` in ChamberReset | **0** | M2 **closed** |
| `sorry` / coverage gap in GWR | **0** (module implemented) | M3 **closed** |
| `axiom` in Placement | **1** (`tau_prime_square_eq_three`) | M4 (or earlier if needed) |
| PSP empty shell | `prime_square_proximity_theorem` | M4 (fails D4.4b) |

## Basic.lean

| Item | Notes | Target |
| --- | --- | --- |
| `three_distinct_divisors_imply_tau_ge_three` | **proved** (core List cardinality) | M1 done |
| `tau_eq_two_iff_only_divisors_are_1_and_n` | **proved** (both directions) | M1 done |
| `tau_gt_two_iff_has_proper_divisor` | **proved** (classical not-forall + counting) | M1 done |

Build: `cd lean-4 && lake build PGS.Basic` succeeds; `rg sorry PGS/Basic.lean` empty.

D4.1 (tau / DNI coordinates characterization via `tau = 2`) is closed on the Basic path.

## ChamberReset.lean

| Item | Notes | Target |
| --- | --- | --- |
| `replay_some_under_hyps` | **proved** (theorem, 0 axioms) | M2 closed |
| `replay_cert_eq_hyps` | **proved** (theorem, 0 axioms) | M2 closed |
| `replay_cert_demoted` | **proved** (theorem, 0 axioms) | M2 closed |
| supporting walk / carrier lemmas | **proved** | M2 support |
| L5 `weak_lfcl_ruleX_forces_next_prime` | **proved** | M2 closed |
| PSP theorem body | `prime_square_proximity_theorem` | **Empty shell** — fails D4.4b | M4 |

Build: `cd lean-4 && lake build PGS.ChamberReset` succeeds with 0 errors.

## GWR.lean

| Item | Notes | Target |
| --- | --- | --- |
| `ordered_comparison` | **proved** (PROOF.md Ordered Comparison Lemma) | M3 done |
| `later_integers_smaller_F` | **proved** (later side via OC) | M3 done |
| `leftmost_min_tau_maximizer` | **proved** under `EarlierSideClosed` hyp | M3 done |
| `leftmost_min_tau_maximizer_prime_square` | **proved** (earlier side discharged for τ(w)=3) | M3 done |
| `prime_square_earlier_smaller_F` | **proved** | M3 support |
| `interior_composite_of_tau_ne_two` | **proved** | M3 support |

**Honesty note (D3 / finite bases):** The general earlier-integer side of PROOF.md
(Witness Threshold + Short Divisor-Average + `gwr_finite_base_v1`) is packaged as
the named hypothesis `EarlierSideClosed`. That is an explicit premise, not a
hidden axiom named like a theorem. The prime-square earlier case is fully
discharged. D4.3 (Ordered Comparison non-`sorry`; maximizer formalized) is closed.

Build: `cd lean-4 && lake build PGS.GWR` succeeds; `rg sorry PGS/GWR.lean` empty.

## Placement.lean

| Line (approx) | Item | Notes | Target |
| --- | --- | --- | --- |
| ~111 | `axiom tau_prime_square_eq_three` | prime-square divisor count; audit-style premise under D3 | M4 |

## NextPrime.lean

`weak_lfcl_sufficient_bound` fully proved and exported. All ChamberReset dependencies closed.

## Update rule

After each milestone PR/commit: re-run ripgrep, refresh this table, bump “As of”, note SHA if committed.

*M3 CLOSED (2026-07-23). GWR Ordered Comparison + maximizer mirror in place; general earlier side named hyp; square case discharged.*
