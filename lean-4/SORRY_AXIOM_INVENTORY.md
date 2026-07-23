# Lean 4 sorry / axiom inventory

**As of:** 2026-07-23 (commit `a96cb3e7`, M2 closed)  
**Command:** `rg -n 'sorry|axiom ' lean-4/PGS/*.lean`  
**DoD:** `DEFINITION_OF_DONE.md`

## Summary

| Kind | Count | Blocks milestone |
| --- | --- | --- |
| `sorry` in Basic | **0** | M1 **closed** |
| `axiom` in ChamberReset | **0** | M2 **closed** |
| proved M2 walk & replay theorems | **all** | M2 closed (commit `a96cb3e7`) |
| `axiom` in Placement | **1** (`tau_prime_square_eq_three`) | M4 (or earlier if GWR needs it) |
| GWR coverage gap | module placeholder | M3 |

## Basic.lean

| Item | Notes | Target |
| --- | --- | --- |
| `three_distinct_divisors_imply_tau_ge_three` | **proved** (core List cardinality) | M1 done |
| `tau_eq_two_iff_only_divisors_are_1_and_n` | **proved** (both directions) | M1 done |
| `tau_gt_two_iff_has_proper_divisor` | **proved** (classical not-forall + counting) | M1 done |

Supporting lemmas added (no `sorry`, no `axiom`): `length_ge_three_of_three_distinct`, `nodup_filter`, `length_eq_two_of_mem_pair_nodup`.

Build: `cd lean-4 && lake build PGS.Basic` succeeds; `rg sorry PGS/Basic.lean` empty.

D4.1 (tau / DNI coordinates characterization via `tau = 2`) is closed on the Basic path. E/F/Z Real hooks remain in Placement (out of M1 scope).

## ChamberReset.lean

| Item | Notes | Target |
| --- | --- | --- |
| `replay_some_under_hyps` | **proved** (theorem, 0 axioms) | M2 closed |
| `replay_cert_eq_hyps` | **proved** (theorem, 0 axioms) | M2 closed |
| `replay_cert_demoted` | **proved** (theorem, 0 axioms) | M2 closed |
| `carrier_none_means_no_composite` | **proved** (interior no-composite invariant) | M2 support |
| `cOff_offset_le` | **proved** (carrier offset bound) | M2 support |
| `carrier_min_tau_interior` | **proved** (leftmost minimum τ invariant) | M2 support |
| `threat_none_under_hyps` | **proved** (post-lock threat search empty) | M2 support |
| `resolved_list_singleton` | **proved** (singleton resolved survivor) | M2 support |
| `getCount` via `getD` + `getCount_map_of_lt` | **proved** | M2 support |
| `walkStep` / `initWalk` | named fold step (induction surface) | M2 support |
| `unres_zero_of_range_lt` | **proved** foldl unres=0 for `k < gap` | M2 support |
| `unres_one_after_gap` | **proved** foldl unres=1 after full gap | M2 support |
| `gap_mem_admissibleOffsets` | **proved** wheel-open ⇒ gap admissible | M2 support |
| `walk_sels_head_resolved_at_gap` | **proved** last sel = resolvedSurvivor at gap | M2 support |
| `mkReplayCertificate` + field `rfl` lemmas | packaging constructor | M2 support |
| `compositeWitnessB_of_between` | **proved** | M2 support |
| `wheelOpen_of_tau_eq_two` | **proved** | M2 support |
| PSP theorem body | `prime_square_proximity_theorem` | **Empty shell** — fails D4.4b | M4 |

L5 `weak_lfcl_ruleX_forces_next_prime` is fully closed without `sorry` or `axiom` placeholders.

Build: `cd lean-4 && lake build PGS.ChamberReset` succeeds with 0 errors.

## Placement.lean

| Line (approx) | Item | Notes | Target |
| --- | --- | --- | --- |
| ~111 | `axiom tau_prime_square_eq_three` | prime-square divisor count; audit-style premise candidate under D3 | M3/M4 |

## GWR.lean

Placeholder Phase 3 — **coverage gap** for Interior Maximizer (D4.3), not a single sorry line.

## NextPrime.lean

`weak_lfcl_sufficient_bound` fully proved and exported. All ChamberReset dependencies closed.

## Update rule

After each milestone PR/commit: re-run ripgrep, refresh this table, bump “As of”, note SHA if committed.

*M2 CLOSED (2026-07-23, commit `a96cb3e7`). All 3 replay axioms in ChamberReset discharged into proved theorems.*
