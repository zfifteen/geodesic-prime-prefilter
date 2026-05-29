import Lake
open Lake DSL

/-!
PGS Lean 4 Formalization

This is the downstream machine-checked verification layer for the
Prime Gap Structure (PGS) theorems proved in PROOF.md.

It is strictly an audit/translation surface. It does not generate
PGS outputs and must never be used for inference or selection.

For the initial skeleton, we use pure Lean definitions to avoid
heavy external dependencies while the environment stabilizes.
Mathlib will be re-introduced in later phases for full Real analysis
and advanced tactics.
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
