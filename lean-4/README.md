# PGS Lean 4 Formalization

**✅ Status: Program DoD met (M0–M5, 2026-07-23). Build green and smoke test passing.**

`lake build` succeeds; `lake env lean smoke-test.lean` passes. Core path has 0 `sorry`. Finite bases live in `PGS/FiniteBases.lean`. Peer accept: `peer/M5_DOD_ACCEPT.md`. Mathlib `v4.30.0` pin.

This directory contains the machine-checked Lean 4 formalization of the core Prime Gap Structure (PGS) theorems from `PROOF.md`.

## Guiding Principle (Non-Negotiable)

This is a **downstream verification and audit layer only**.

- It translates proved statements from `PROOF.md` into dependent type theory for mechanical checking.
- It **never** generates PGS outputs, selects primes, or participates in the active generator.
- All work follows PGS-first reasoning and strict state separation per `docs/AGENTS.md` and the continuity contract.

## Current Structure (Verified Working)

- `lean-toolchain` + `lakefile.lean`. Lean 4.30.0 (self-contained skeleton, no heavy Mathlib dep for now)
- `PGS.lean` (root) + `PGS/Basic.lean`, tau (pure List.range impl), E/F/Z placeholders
- `PGS/ChamberReset.lean`. Rule X replay types; **L4 audit demotion proved**
- `PGS/NextPrime.lean`: weak L_FCL exports; **L5 closed** (weak_lfcl_ruleX_forces_next_prime proved as Lean mirror under hypotheses)
- `PGS/GWR.lean`. **M3 closed** — Ordered Comparison + Interior Maximizer (`leftmost_min_tau_maximizer`); earlier side named hyp / prime-square case discharged
- `PGS/BoundedCompression.lean`. **M4 closed** — non-vacuous `dynamicCutoff`; UBC + Prime-Square Proximity under named finite-base / capacity premises (empty shell removed)
- `PGS/FiniteBases.lean`. **M5 closed** — certificate-aligned finite-base hypothesis bundles (`FiniteBaseBundle`)
- `smoke-test.lean`. Automated verification that the library loads and basic defs work
- `peer/M5_DOD_ACCEPT.md`. Program D1–D7 peer accept
- Full contract and plan documents
- [`PLACEMENT_FORMALIZATION_ROADMAP.md`](PLACEMENT_FORMALIZATION_ROADMAP.md), closure-order DAG for RH-080/081 ([#49](https://github.com/zfifteen/prime-gap-structure/issues/49))

**Important Note on Dependencies**: The initial attempt to use full Mathlib created repeated source/checkout blockers. The skeleton was made self-contained (pure Lean) to achieve a working, verifiable build. Mathlib will be re-introduced in a controlled manner during Phase 1 expansions.

## How to Build & Verify

**Fresh clone (default, zero extra configuration):**

```bash
cd lean-4
lake build
lake env lean smoke-test.lean
```

Lake creates `lean-4/.lake/` inside the repo automatically. No symlinks, env vars,
or external directories are required.

**Recommended helper (same default paths):**

```bash
bash ../scripts/lean4-cache-build.sh
```

Or manual rebuild:

```bash
cd lean-4
rm -rf .lake/build
lake build
lake env lean smoke-test.lean
```

### Optional: park `.lake` outside the repo (disk / IDE only)

Some machines keep Mathlib and Lake build trees outside the working tree via a
symlink so the checkout stays smaller on disk. **This is optional.** New users
must not run it unless they want that layout.

```bash
# From repo root — only if you want external bulk storage
bash scripts/link-local-bulk.sh
# optional: also link media/
bash scripts/link-local-bulk.sh --with-media
```

Default bulk root: `~/IdeaProjects/pgs-local-bulk` (override with `PGS_LOCAL_BULK`).
After linking, `lake build` still uses `lean-4/.lake` as usual (symlink target).

## Verified Smoke Test Output

```
PGS.tau (n : Nat) : Nat
PGS.E (n : Nat) : Nat
PGS.F (n : Nat) : Nat
PGS.Z (n : Nat) : Nat
1
6
2
"PGS library smoke test loaded successfully"
```

## Traceability

Every definition carries headers linking back to PROOF.md and supporting documents.

See `PGS_LEAN_FORMALIZATION_PLAN.md` for the phased expansion roadmap.

---

**This is a mirror for audit, not a source for new PGS reasoning.**

## Phase 1 Update (2026-05-27)

- Added the two core characterization lemmas with traceability to PROOF.md lines 80-81.
- `tau_eq_two_iff_only_divisors_are_1_and_n` (main lemma)
- `tau_gt_two_iff_has_proper_divisor` (contrapositive / composite form)
- Partial proofs in place. Full bidirectional proofs in active development.
- Build and smoke test verified.
- Proceeding with the original translation plan.

### Phase 1 Update (continued 2026-05-27)

- Proof structure for both characterization lemmas is now in place.
- Forward and reverse directions have clear skeletons.
- The remaining obligations are explicitly the divisor-list length counting arguments.
- Build + smoke test remain green.
- Proceeding with original plan.

## Phase 1 Update (2026-05-27: Active Non-Stop Session)

**Historical note (2026-05/06):** Early Phase-1 iterations deferred the pure-List counting obligations (`three_distinct_divisors_imply_tau_ge_three` and the `length=2` combination step) and recorded them as `sorry`. This was the working state at the 2026-06 gate.

**M1 CLOSED (verified 2026-07-20):** The deferred counting obligations were subsequently completed with core-only tactics — no Mathlib required, no `sorry` remaining. Current state:

- `three_distinct_divisors_imply_tau_ge_three` — **proved** (core List cardinality via `length_ge_three_of_three_distinct`).
- `tau_eq_two_iff_only_divisors_are_1_and_n` — **proved** both directions; reverse direction uses `length_eq_two_of_mem_pair_nodup` + `nodup_filter`.
- `tau_gt_two_iff_has_proper_divisor` — **proved** (contrapositive form).
- `rg 'sorry' lean-4/PGS/Basic.lean` returns **no** matches. D4.1 (tau / DNI coordinates + prime ↔ `tau = 2` characterization) is closed on the Basic path.
- `lake build` + `lake env lean smoke-test.lean` succeed (after the Mathlib vendored-tree corruption was restored — see Build note below).

E/F/Z Real hooks remain in `PGS.Placement` (out of M1 scope; Mathlib re-introduction is now active and the build is green).

**Build note (2026-07-20):** The `lean-4/.lake/packages/mathlib` checkout had been silently corrupted (113 vendored files with mangled Unicode, e.g. `Mathlib/Tactic/Linter/TextBased/UnicodeLinter.lean` failing to parse). Restoring the clean `v4.30.0` checkout (`git -C .lake/packages/mathlib checkout -- .` + rebuild) resolved it. The Mathlib pin and `leanprover/lean4:v4.30.0` toolchain are correctly matched; the breakage was local corruption, not a version skew. Do not re-pin without cause.

