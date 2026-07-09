# SRGP-v1 Subgoal 1: Failure Forensics

**Verdict: `prime`.** On all three official 127-bit audit failures
(`s127_moderate_112`, `s127_moderate_127`, `s127_archived_shape_112`), center-out
prime-walk on the rung-2 `best_window_rank` 0.25-bit window recovers the small
factor at budget 16384; seed recovery (budgets 64 to 1024) and residue-ranked
recovery (top 10 at budget 1024) never place the true factor in the tested
candidate lists. **Subgoal 2 (hybrid seed-first spec) is blocked** because
`seed_recovery_1024_hit` is false on every case.

## Executive summary

The three cases share one failure shape: routing places the small factor inside
the final 0.25-bit window (`factor_in_final_window=true`, `best_window_rank=1`),
but PGS seed clustering does not surface that prime within the rung-2
`local_seed_budget` (1024). Prime-walk from the window midpoint does. Two cases
hit at budget 256; `s127_moderate_127` needs the full rung-2
`router_only_prime_budget` (16384, 6810 divisibility tests) because budgets
256/1024/4096 all miss. Re-running the shipped `_evaluate_case` on current
`pgs_geofac_scaleup.py` recovers all three on the official path (134, 6810, and
253 `local_prime_tests` respectively), consistent with prime-walk-only recovery
at the committed budget.

## Per-case mechanism matrix

| case_id | prime @256 | prime @16384 | seed @1024 | residue top-10 @1024 |
|---|---|---|---|---|
| `s127_moderate_112` | hit (134 tests) | hit | miss (30 tests) | miss |
| `s127_moderate_127` | miss | hit (6810 tests) | miss (14 tests) | miss |
| `s127_archived_shape_112` | hit (253 tests) | hit | miss (37 tests) | miss |

Window intervals (rung 2, `audited_family_prior`, seed 0) are recorded in
`failure_forensics.json`. Midpoints sit near but do not equal the small factor;
prime-walk center-out ordering reaches the factor before budget exhaustion on
the factor window.

## Interpretation

1. **Seed recovery is not the fix.** `_pgs_seed_recovery_in_interval` never
   recovers despite exercising the shipped cluster + residue-rank ordering. The
   residue-ranked top-10 primes are tightly clustered around a wrong anchor
   (~1.4×10¹⁶ offset from the true factor on the 112-bit moderate case), not
   near `small_factor`.

2. **Prime-walk is the only probed mechanism that closes the gap** on the routed
   window. The marginal case `s127_moderate_127` demonstrates budget sensitivity:
   sub-16384 prime budgets fail even though the factor remains inside the same
   0.25-bit window.

3. **Committed audit rows vs current harness.** The official audit artifact
   (`pgs_127_official_audit_rows.jsonl`, 9/12 recovery) predates or differs from
   the current prime-walk-only `_local_pgs_search` (which deletes
   `local_seed_budget`). Forensics on today's harness shows these three cases are
   recoverable without any seed path; the documented 25% gap is not reproduced
   by seed-first hybridization:it is a prime-budget / search-order phenomenon on
   the shipped path.

## Recommendation (blocks Subgoal 2)

Do **not** proceed to hybrid seed-first `_local_pgs_search` (Subgoal 2). Next
leverage is a **prime-budget / window-width study**: quantify minimum
`router_only_prime_budget` per family at 0.25-bit width, and whether narrowing
width or reordering windows reduces the 6810-test tail on `s127_moderate_127`
without lowering recall on the nine current successes.

## Artifacts

- Probe: `failure_forensics_probe.py`
- Machine output: `failure_forensics.json`
- Run log: goal scratch `failure_forensics_run.log`