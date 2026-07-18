# Lean 4 sorry / axiom inventory

**As of:** 2026-07-18 (Hermes owner, M2 partial — foldl unres + resolved-head)  
**Command:** `rg -n 'sorry|axiom ' lean-4/PGS/*.lean`  
**DoD:** `DEFINITION_OF_DONE.md`

## Summary

| Kind | Count (approx) | Blocks milestone |
| --- | --- | --- |
| `sorry` in Basic | **0** | M1 **closed** |
| `axiom` in ChamberReset | **3** (unchanged count) | M2 in progress |
| proved M2 foldl walk lemmas | several | support only; axioms remain |
| `axiom` in Placement | 1 | M4 (or earlier if GWR needs it) |
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
| `axiom replay_some_under_hyps` | still axiom; residual = threat/post → `isSome` | M2 |
| `axiom replay_cert_eq_hyps` | still axiom; needs resolved list shape | M2 |
| `axiom replay_cert_demoted` | still axiom; sig fields from walk record | M2 |
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

L5 `weak_lfcl_ruleX_forces_next_prime` remains a D3.4 packaging wrapper around the three replay axioms.

**Honest residual for isSome:** walk proves the resolved survivor is recorded at gap with `unresBefore=0`. Closing `replay_some_under_hyps` still needs (1) `threatOff = none` under min-d carrier invariant, (2) post-filter `resolved` non-empty, (3) optional `0 < gap` from next-prime packaging.

Build: `cd lean-4 && lake build PGS.ChamberReset` succeeds. Smoke + `#eval` replay on p=11/gap=2 and p=73/gap=6 return expected certs.

## Placement.lean

| Line (approx) | Item | Notes | Target |
| --- | --- | --- | --- |
| ~111 | `axiom tau_prime_square_eq_three` | prime-square divisor count; audit-style premise candidate under D3 | M3/M4 |

## GWR.lean

Placeholder Phase 3 — **coverage gap** for Interior Maximizer (D4.3), not a single sorry line.

## NextPrime.lean

Depends on ChamberReset discharge; re-scan after M2 axioms become theorems.

## Update rule

After each milestone PR/commit: re-run ripgrep, refresh this table, bump “As of”, note SHA if committed.

*Hermes M2 partial: foldl unres + resolved-head proved; 3 replay axioms remain (threat/post residual).*
