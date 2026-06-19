# PGS Lean 4 Formalization

**✅ Status: Skeleton complete and verified (2026-05-27).**

Build succeeds cleanly. Smoke test passes. Self-contained pure-Lean implementation for reliable operation.

This directory contains the machine-checked Lean 4 formalization of the core Prime Gap Structure (PGS) theorems from `PROOF.md`.

## Guiding Principle (Non-Negotiable)

This is a **downstream verification and audit layer only**.

- It translates proved statements from `PROOF.md` into dependent type theory for mechanical checking.
- It **never** generates PGS outputs, selects primes, or participates in the active generator.
- All work follows PGS-first reasoning and strict state separation per `AGENTS.md` and the continuity contract.

## Current Structure (Verified Working)

- `lean-toolchain` + `lakefile.lean` — Lean 4.30.0 (self-contained skeleton, no heavy Mathlib dep for now)
- `PGS.lean` (root) + `PGS/Basic.lean` — tau (pure List.range impl), E/F/Z placeholders
- `PGS/ChamberReset.lean` — Rule X replay types; **L4 audit demotion proved**
- `PGS/NextPrime.lean` — weak L_FCL exports; **L5 open** (`sorry`)
- `PGS/GWR.lean` — Phase 3 placeholder
- `smoke-test.lean` — Automated verification that the library loads and basic defs work
- Full contract and plan documents

**Important Note on Dependencies**: The initial attempt to use full Mathlib created repeated source/checkout blockers. The skeleton was made self-contained (pure Lean) to achieve a working, verifiable build. Mathlib will be re-introduced in a controlled manner during Phase 1 expansions.

## How to Build & Verify

```bash
# Recommended
bash ../lean4-cache-build.sh

# Or manual
cd lean-4
rm -rf .lake/build
lake build
lake env lean smoke-test.lean
```

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

## Phase 1 Update (2026-05-27 — Active Non-Stop Session)

**Status update (2026-06)**: The pure-List counting argument (`three_distinct_divisors_imply_tau_ge_three`) has been explicitly deferred to Phase 2 (Mathlib re-introduction) per user decision. Forward direction of the main lemma now compiles against the deferred lemma. Work continues on the reverse direction and contrapositive (still Phase 1). See `PGS/Basic.lean` for the deferral comment and the formalization plan for details.

**Status**:
- Statement of `tau_eq_two_iff_only_divisors_are_1_and_n` is solid and traceable to PROOF.md:80-81.
- Forward direction has complete setup showing that a third distinct divisor produces three members in the explicit filter.
- The precise remaining gap is the pure-Lean proof that "three distinct members in the filtered list ⇒ length ≥ 3".
- Reverse direction skeleton is present.
- Multiple iterations completed this session on exactly this counting obligation.
- Build succeeds on structure; the mathematical counting steps remain as explicit `sorry`.

**Honest note**: The bare-List version of the "three distinct elements imply length ≥ 3" fact is more tedious than expected in a self-contained skeleton. Work continues on the user's explicit goal.

**Status update (larger unit, 2026-06)**: Reverse direction larger unit delivered: `only_one_and_n_in_filter` (∀ x ∈ filter → x=1 ∨ x=n under h_only) + concrete one_mem + n_mem. The "at most 2" and "at least 2" are in place. The final length=2 combination step (image ⊆ {1,n}, distinct sublist of range, hits both) is the symmetric pure-List counting obligation and is explicitly deferred (2026-06, consistent with the forward deferral and user decision). Contrapositive `tau_gt_two_iff_has_proper_divisor` stated (with deferral note). Smoke-test updated. Build clean (only the two marked deferred sorries). 1:1 PROOF.md:80-81 traceability preserved. PGS-first, downstream-only, per contract.

**Phase 1 Gate Closed (2026-06)**: Per the "update before new phase" rule in the translation plan, Phase 1 is now formally closed with the honest boundary documented in PGS_LEAN_TRANSLATION_PLAN.html (core non-counting work delivered; the two counting obligations deferred to Phase 2). All living surfaces updated. No new phase work (E/F/Z, ordered comparison) begins until this gate is acknowledged. Build remains the verification surface.

