/-
Copyright (c) 2026 Velocity Works. All rights reserved.
Released under the MIT License as described in the file LICENSE.
Authors: PGS Project

M5 — Named finite-base hypothesis packages (DoD D3.2 / D4.6)

Packages the three certified finite premises from PROOF.md §Certified Finite
Bases as explicit Lean hypothesis bundles. Lean does **not** re-run the
exhaustions and does not claim to have proved them from nothing.

Certificate paths (repo root relative):
- docs/proof-enhancements/certificates/gwr_finite_base_v1.json
- docs/proof-enhancements/certificates/bounded_compression_base_v1.json
- docs/proof-enhancements/certificates/residual_k128_v1.json

Status labels: **finite-base hypothesis** (D3.2b). Downstream audit only.
-/

import PGS.Basic
import PGS.GWR

namespace PGS.FiniteBases

open PGS PGS.GWR

/-! ## Certificate identity (static metadata)

These constants pin the certificate IDs and ranges used by PROOF.md. They are
documentation-bearing Lean values for traceability, not runtime loaders.
-/

/-- Certificate id `gwr_finite_base_v1`. -/
def gwrFiniteBaseId : String := "gwr_finite_base_v1"

/-- Preceding-prime window exclusive upper bound from the certificate. -/
def gwrFiniteBasePMaxExclusive : ℕ := 5000000001

/-- Repo-relative certificate path. -/
def gwrFiniteBaseCertPath : String :=
  "docs/proof-enhancements/certificates/gwr_finite_base_v1.json"

/-- Artifact hash from committed certificate JSON. -/
def gwrFiniteBaseArtifactHash : String :=
  "sha256:222398f59d1ab1e6f6a7b17c691ebc44a96038a713f5218ea407f1bb5a5cff57"

/-- Certificate id `bounded_compression_base_v1`. -/
def boundedCompressionBaseId : String := "bounded_compression_base_v1"

/-- `q < ceil(exp(16)) = 8_886_111` from the certificate. -/
def boundedCompressionQMax : ℕ := 8886111

def boundedCompressionCertPath : String :=
  "docs/proof-enhancements/certificates/bounded_compression_base_v1.json"

def boundedCompressionArtifactHash : String :=
  "sha256:fb20894f92320a7547014b37d4dfd7727b7f75f7e92054ddd883d51345d14514"

/-- Certified offset ceiling on the finite base (`w − p ≤ 60`). -/
def boundedCompressionOffsetCap : ℕ := 60

/-- Certificate id `residual_k128_v1`. -/
def residualK128Id : String := "residual_k128_v1"

/-- First-d4 window parameter K from the certificate. -/
def residualK128Max : ℕ := 128

def residualK128CertPath : String :=
  "docs/proof-enhancements/certificates/residual_k128_v1.json"

def residualK128ArtifactHash : String :=
  "sha256:ed3afeadc81475850a64331d1f008c8ac8af8afe084659f4b37f5a56f77e1e29"

/-! ## Hypothesis packages (D4.6)

Each package is a Prop (or structure of Props) that a caller may assume when
assembling a headline theorem. They encode the **meaning** of the finite
certificate, not a silent `True` smuggle of the universal bound.
-/

/--
**`gwr_finite_base_v1` hypothesis.**

On the certified window `p < 5_000_000_001`, the earlier-integer side of the
GWR maximizer is closed (`EarlierSideClosed`). Outside the window, this
package is vacuous (implication antecedent false).
-/
def GwrFiniteBaseV1 (p q w : ℕ) : Prop :=
  p < gwrFiniteBasePMaxExclusive → EarlierSideClosed p q w

/--
**`bounded_compression_base_v1` hypothesis.**

On consecutive-prime gaps with selected witness `w` and
`q < 8_886_111`, the offset satisfies `w − p ≤ 60`.
-/
def BoundedCompressionBaseV1 (p q w : ℕ) : Prop :=
  q < boundedCompressionQMax → w - p ≤ boundedCompressionOffsetCap

/--
**`residual_k128_v1` hypothesis content.**

On the retained residual odd-adjacent branches of PROOF.md, the K=128
first-d4 window eliminates the listed high-τ witness candidates (certificate
table). Packaged as an opaque Prop so assembly theorems can require an
explicit assumption token without Lean re-enumerating residual catalogs.
-/
opaque ResidualK128Holds : Prop

/-- Explicit assumption token for the residual k128 certificate. -/
structure ResidualK128Premise where
  /-- Caller asserts the residual certificate content. -/
  holds : ResidualK128Holds

/--
**Unified finite-base bundle** for a single gap instance `(p, q, w)`.

Carries all three PROOF.md finite premises required by the UBC assembly DAG.
Lean never invents these; the caller supplies them from the certificate layer.
-/
structure FiniteBaseBundle (p q w : ℕ) where
  /-- `gwr_finite_base_v1` -/
  gwr : GwrFiniteBaseV1 p q w
  /-- `bounded_compression_base_v1` -/
  boundedCompression : BoundedCompressionBaseV1 p q w
  /-- `residual_k128_v1` -/
  residual : ResidualK128Premise

/-- Project the GWR finite base from a bundle. -/
theorem FiniteBaseBundle.gwr_proj {p q w : ℕ} (b : FiniteBaseBundle p q w) :
    GwrFiniteBaseV1 p q w :=
  b.gwr

/-- Project the bounded-compression finite base from a bundle. -/
theorem FiniteBaseBundle.bc_proj {p q w : ℕ} (b : FiniteBaseBundle p q w) :
    BoundedCompressionBaseV1 p q w :=
  b.boundedCompression

/-- Project the residual premise from a bundle. -/
theorem FiniteBaseBundle.residual_proj {p q w : ℕ} (b : FiniteBaseBundle p q w) :
    ResidualK128Premise :=
  b.residual

/--
On the finite base range, the bundle implies the offset cap `w − p ≤ 60`.
This is pure unpacking of `BoundedCompressionBaseV1` — not a universal bound.
-/
theorem offset_cap_of_bundle
    {p q w : ℕ} (b : FiniteBaseBundle p q w)
    (hq : q < boundedCompressionQMax) :
    w - p ≤ boundedCompressionOffsetCap :=
  b.boundedCompression hq

/--
Inside the GWR finite window, the bundle implies `EarlierSideClosed`.
-/
theorem earlier_side_of_bundle
    {p q w : ℕ} (b : FiniteBaseBundle p q w)
    (hp : p < gwrFiniteBasePMaxExclusive) :
    EarlierSideClosed p q w :=
  b.gwr hp

end PGS.FiniteBases
