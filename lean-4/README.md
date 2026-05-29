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
- `PGS/GWR.lean` and `PGS/NextPrime.lean` — Phase 3/4 placeholders
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

**Current focus**: Closing the divisor counting arguments in `PGS/Basic.lean` until the two main characterization lemmas have zero `sorry` in their theorem bodies.

**Status**:
- Statement of `tau_eq_two_iff_only_divisors_are_1_and_n` is solid and traceable to PROOF.md:80-81.
- Forward direction has complete setup showing that a third distinct divisor produces three members in the explicit filter.
- The precise remaining gap is the pure-Lean proof that "three distinct members in the filtered list ⇒ length ≥ 3".
- Reverse direction skeleton is present.
- Multiple iterations completed this session on exactly this counting obligation.
- Build succeeds on structure; the mathematical counting steps remain as explicit `sorry`.

**Honest note**: The bare-List version of the "three distinct elements imply length ≥ 3" fact is more tedious than expected in a self-contained skeleton. Work continues on the user's explicit goal.

