/-
PGS Lean 4 Smoke Test (Phase 1)

Run with:
  cd lean-4 && lake env lean smoke-test.lean
-/

import PGS.Basic

open PGS

#check tau
#check E
#check F
#check Z

#eval tau 1
#eval tau 12
#eval tau 13

-- Phase 1 lemmas (fully stated, partial proofs)
#check tau_eq_two_iff_only_divisors_are_1_and_n
#check tau_gt_two_iff_has_proper_divisor

#check "PGS library smoke test loaded successfully (Phase 1 - characterization lemmas with proof structure)"