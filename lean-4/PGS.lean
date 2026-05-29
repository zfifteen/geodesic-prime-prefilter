/-
Copyright (c) 2026 Velocity Works. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: PGS Project
-/

import PGS.Basic
import PGS.GWR
import PGS.NextPrime

/-!
# Prime Gap Structure (PGS) Formalization Root

This is the root module for the PGS Lean 4 verification library.

**Strict Contract**:
- Downstream machine-checked audit / translation layer only.
- Never used for prime selection, gap generation, or inference.
- All content maintains 1:1 traceability to PROOF.md.
- See LEAN_PGS_VERIFICATION_CONTRACT.md and PGS_LEAN_FORMALIZATION_PLAN.md.
-/
