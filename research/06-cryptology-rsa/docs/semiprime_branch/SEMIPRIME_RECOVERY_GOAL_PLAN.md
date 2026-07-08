# Semiprime Recovery Goal Plan (SRGP-v1)

**Date:** 2026-07-08  
**Parent surface:** `research/06-cryptology-rsa/docs/semiprime_branch/`  
**Harness:** `research/06-cryptology-rsa/scripts/pgs_geofac_scaleup.py`  
**Tests:** `research/06-cryptology-rsa/tests/test_pgs_geofac_scaleup.py`

## Master objective

Close the 127-bit semiprime recovery gap: routing already lands the true factor
scale in the top window (12/12), but exact recovery stops at 9/12 (75%). Deliver
a PGS-native hybrid recovery path that uses the already-implemented seed recovery
(`_pgs_seed_recovery_in_interval` / `gwr_predict`) before the prime-walk fallback,
prove it on the three failing cases, pass the official 127 audit at rung 2 with
**12/12** exact recovery, then run a bounded 160-bit smoke without widening scope
into RSA v2 or PROOF.md.

## Optimization for `/goal` mode

- One master goal + **6 sequential sub-goals** (do not parallelize the core path).
- Each sub-goal: mandatory entry reads → bounded actions → exact commands →
  success criteria → handoff line for `update_goal`.
- Edit scope is explicit per sub-goal; everything else is read-only.
- Gate command after every code-changing sub-goal:

```bash
PYTHONPATH=src/python python3 -m pytest \
  research/06-cryptology-rsa/tests/test_pgs_geofac_scaleup.py -q
```

- Full official audit (slow, ~90–120s):

```bash
PYTHONPATH=src/python python3 research/06-cryptology-rsa/scripts/pgs_geofac_scaleup.py \
  --scale-bits 127 --rung 2 --seed 0 \
  --output-dir research/06-cryptology-rsa/output/semiprime_branch
```

Or from tests: `test_official_127_audit_passes_on_first_passing_rung`.

**Activation pattern:**

```
/goal SRGP-v1 Subgoal 1 — Failure Forensics
... work ...
/goal status
/goal SRGP-v1 Subgoal 2 — Seed Recovery Probe
```

## Contracts (binding)

- PGS-first: recovery ranks `gwr_predict` clusters; `N % p == 0` is audit hit
  label only (already documented in harness).
- Do **not** edit: `PROOF.md`, `src/python/z_band_prime_predictor/simple_pgs_generator*.py`,
  `experiments/live-solver/rsa-v2/ALGORITHM.md`.
- Do **not** claim blind factorization or RSA break in artifacts.
- Status separation: measured / audited only unless a new theorem is actually proved.
- Super-Signal / twin-gap collapse: **out of scope** (0/12 on 127 corpus).

## Execution log

_(Sub-goal completions appended here with timestamp.)_

---

## Subgoal 1 — Failure Forensics (read-only)

**Hypothesis under test:** The three failures (`s127_moderate_112`,
`s127_moderate_127`, `s127_archived_shape_112`) have `factor_in_final_window=true`
but prime-walk exhausts budget; seed recovery may succeed in the same window.

**Entry reads (order):**

1. `docs/AGENTS.md` (cryptology framing)
2. `research/06-cryptology-rsa/README.md`
3. `research/06-cryptology-rsa/output/semiprime_branch/pgs_127_official_audit_rows.jsonl`
4. `research/06-cryptology-rsa/scripts/pgs_geofac_scaleup.py` — `_local_pgs_search`,
   `_pgs_seed_recovery_in_interval`, `_local_router_only_prime_walk`
5. `research/06-cryptology-rsa/tests/test_pgs_geofac_scaleup.py` — seed recovery tests

**Actions:**

1. Create `experiments/semiprime-recovery-hybrid-2026-07/` with:
   - `FINDINGS.md` (conclusion-first)
   - `failure_forensics_probe.py` — for each failing `case_id`:
     - Re-run `_route_case(..., rung=2, router_mode="audited_family_prior")`
     - Take `best_window_rank` window; emit `low, high, midpoint`
     - Run `_local_router_only_prime_walk` with budgets `[256, 1024, 4096, 16384]`
     - Run `_pgs_seed_recovery_in_interval` with `local_seed_budget` `[64, 256, 1024]`
     - Run `_recovery_ranked_recovered_primes_in_interval` (top 10 primes)
     - Record whether `case.small_factor` appears in each ranked list
   - `failure_forensics.json` — machine output

2. Run probe; no production code changes.

**Success criteria:**

- JSON lists all 3 failing cases with boolean flags:
  `prime_walk_16384_hit`, `seed_recovery_1024_hit`, `residue_rank_contains_factor`
- `FINDINGS.md` states which mechanism would fix the 25% gap (one sentence lead).
- If seed recovery does **not** hit on any failure, STOP plan and mark Subgoal 2
  blocked — escalate to prime-budget / window-width study instead.

**Handoff:** `Subgoal 1 complete — <timestamp> — forensic verdict: <seed|prime|both|neither>`

---

## Subgoal 2 — Hybrid Recovery Spec (design-only)

**Prerequisite:** Subgoal 1 verdict is `seed` or `both`.

**Actions:**

1. Add `research/06-cryptology-rsa/docs/semiprime_branch/hybrid_recovery_spec.md`
   (≤80 lines) defining `_local_pgs_search` contract:

   **Order per routed window (best rank first):**

   1. `_pgs_seed_recovery_in_interval(case, low, high, local_seed_budget)`
   2. If miss: `_recovery_ranked_recovered_primes_in_interval` + divisibility
      (cap tests = `local_seed_budget`, no new ranking logic)
   3. If miss: `_local_router_only_prime_walk` (existing fallback)

   **Invariants:**

   - `local_seed_budget` from `RUNG_CONFIGS[rung]` must be used (currently deleted
     via `del local_seed_budget` — that line removed).
   - Count `local_prime_tests` as sum across strategies.
   - Deterministic: same inputs → same row outputs (existing test helpers).

2. Pre-register falsification: if hybrid lowers recall on any of the 9 current
   successes, revert and narrow strategy.

**Success criteria:**

- Spec reviewed against Subgoal 1 JSON (each failure has a covered code path).
- No implementation yet.

**Handoff:** `Subgoal 2 complete — <timestamp> — spec locked`

---

## Subgoal 3 — Implement Hybrid `_local_pgs_search`

**Scope:** Only `pgs_geofac_scaleup.py` + tests.

**Actions:**

1. Replace `_local_pgs_search` per spec.
2. Add row fields (optional, if useful for audit):
   `recovery_strategy` ∈ `{seed, residue_rank, prime_walk}`.
3. Add tests:
   - `test_three_failures_recover_under_hybrid_at_rung_2` (parametrize case_ids)
   - `test_nine_successes_still_recover_at_rung_2` (regression guard)
   - `test_local_pgs_search_uses_local_seed_budget` (budget not ignored)

**Success criteria:**

- `pytest research/06-cryptology-rsa/tests/test_pgs_geofac_scaleup.py -q` — all pass.
- `run_127_official_audit(0)` → `exact_recovery_recall == 1.0` (12/12).
- `router_top4_recall` unchanged at 1.0.
- `stage_passed` true at `official_rung == 2` (no rung 3 required).

**Handoff:** `Subgoal 3 complete — <timestamp> — 12/12 at rung 2`

---

## Subgoal 4 — Tighten Acceptance + Artifact Refresh

**Scope:** `_stage_acceptance`, breakthrough doc, committed JSONL/JSON outputs.

**Actions:**

1. Raise 127-bit `exact_recovery_threshold` in `_stage_acceptance` from `0.75` to
   `1.0` **only if** Subgoal 3 achieved 12/12 (otherwise keep 0.75 and document).
2. Update `pgs_127_official_gate_breakthrough.md` with hybrid path wording
   (routing unchanged; recovery = seed-first hybrid).
3. Re-run CLI audit; commit refreshed
   `output/semiprime_branch/pgs_127_official_audit_summary.json` and rows JSONL.

**Success criteria:**

- Docs match code: no claim that official path is prime-walk-only.
- Acceptance threshold aligns with measured 12/12.
- `test_official_127_audit_passes_on_first_passing_rung` updated if threshold changes.

**Handoff:** `Subgoal 4 complete — <timestamp> — artifacts refreshed`

---

## Subgoal 5 — 160-Bit Smoke (bounded scale)

**Prerequisite:** Subgoal 3 at 12/12.

**Actions:**

1. Run official scale-up on committed `160` corpus (8 cases):

```bash
PYTHONPATH=src/python python3 research/06-cryptology-rsa/scripts/pgs_geofac_scaleup.py \
  --scale-bits 160 --rung 2 --seed 0 \
  --output-dir research/06-cryptology-rsa/output/semiprime_branch
```

2. Add `experiments/semiprime-recovery-hybrid-2026-07/FINDINGS_160.md` with
   router_top4 + exact_recovery counts; no code changes unless recall < 0.50.

3. If 160-bit recall < 0.50: open Subgoal 5b (integer window from family center
   using `C(q)` offset bound on **estimated** right endpoint — probe only, no
   theorem claim). Mapping:

   ```text
   half_width_int ≈ max(64, ceil(0.5 * log2(center)^2))  # integer, not bit width
   ```

   Compare vs fixed `0.25` bit windows on failing 160 rows only.

**Success criteria:**

- 160-bit `router_top4_recall >= 0.75` (existing `_stage_acceptance` threshold).
- 160-bit `exact_recovery_recall >= 0.50` with hybrid path at rung 2.
- FINDINGS_160 lead sentence: pass / partial / fail.

**Handoff:** `Subgoal 5 complete — <timestamp> — 160-bit: <recall>`

---

## Subgoal 6 — Closeout & Continuity

**Actions:**

1. Append execution log timestamps to this file.
2. Update `research/06-cryptology-rsa/README.md` measured evidence bullet (one line:
   hybrid recovery + 12/12 if achieved).
3. Write continuity handoff in `experiments/semiprime-recovery-hybrid-2026-07/FINDINGS.md`:
   - What changed in recovery vs routing
   - Whether 160-bit needs C(q) integer windows
   - Explicit non-claims (RSA-2048, blind factoring)

**Success criteria:**

- Single reproducible command block in FINDINGS.md.
- No scope creep into RSA v2 endpoint law.

**Handoff:** `SRGP-v1 complete — <timestamp>`

---

## Self-review optimizations (applied)

| Original move | Optimization |
|---------------|--------------|
| Fix 25% gap | Forensic probe **before** code; falsify seed hypothesis early |
| Wire `C(q)` into windows | **Deferred** to Subgoal 5b only if 160-bit fails; integer offset ≠ bit width |
| Scale corpus | **160-bit only** after 12/12; 256+ still prime-walk-only in harness |
| Super-Signal | **Removed** from plan (irrelevant to semiprime track) |
| Parallel work | **Forbidden** on Subgoals 1–4 |
| Acceptance at 75% | **Raise to 100%** once demonstrated; don't lower bar preemptively |
| `_local_pgs_search` ignores `local_seed_budget` | Root bug; fixing is core of Subgoal 3 |
| Residue-first tests already exist | Fold into hybrid tier 2 instead of new ranking logic |

## Risk register

| Risk | Mitigation |
|------|------------|
| Seed recovery fails on same 3 cases | Subgoal 1 stops plan; study window integer width + prime budget |
| Hybrid hurts 9 successes | Regression test subgoal 3; revert |
| 127 audit runtime | Run subset tests during dev; full audit once per sub-goal |
| Accidental theorem upgrade | FINDINGS.md conclusion-first; README status = measured |

## Out of scope (entire plan)

- RSA v2 reciprocal endpoint transport
- Blind factoring / unknown-factor corpora
- Twin-Prime Resonance generator optimization
- PROOF.md / Lean changes
- `256+` scale-up recovery path (harness still router-only prime walk at ≥256)

---

**End of plan.** Ready for `/goal SRGP-v1 Subgoal 1 — Failure Forensics`.