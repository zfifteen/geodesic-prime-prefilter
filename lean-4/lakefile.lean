import Lake
open Lake DSL

/-!
PGS Lean 4 Formalization

This is the downstream machine-checked verification layer for the
Prime Gap Structure (PGS) theorems proved in PROOF.md.

It is strictly an audit/translation surface. It does not generate
PGS outputs and must never be used for inference or selection.

Phase 2 entry point (2026-06): Controlled re-introduction of Mathlib begins here
for Real analysis (E/F/Z) and supporting lemmas. Usage is kept minimal and
judicious per the Mathlib Strategy table in PGS_LEAN_TRANSLATION_PLAN.html.
-/

package «pgs» where
  leanOptions := #[
    ⟨`autoImplicit, false⟩,
    ⟨`relaxedAutoImplicit, false⟩
  ]

@[default_target]
lean_lib PGS where
  roots := #[`PGS]
  leanOptions := #[
    ⟨`linter.unusedVariables, false⟩  -- allow for structured proofs
  ]

-- Phase 2: Controlled Mathlib dependency (Real for log + basic supporting theory).
-- See PGS_LEAN_TRANSLATION_PLAN.html §7 "Mathlib Strategy" for rationale and limits.
-- Pinned to a compatible revision for v4.30.0 toolchain.
require mathlib from git "https://github.com/leanprover-community/mathlib4.git" @ "v4.30.0"
