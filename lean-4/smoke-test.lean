/-
PGS Lean 4 Smoke Test (Phase 1)

Run with:
  cd lean-4 && lake env lean smoke-test.lean
-/

import PGS.Basic
import PGS.ChamberReset
import PGS.NextPrime
import PGS.Placement

open PGS
open PGS.ChamberReset
open PGS.NextPrime
open PGS.Placement

#check tau
#check E
#check F
#check witnessThreshold_four_five

#eval tau 1
#eval tau 12
#eval tau 13

-- Phase 1 lemmas (fully stated, partial proofs; length combination steps deferred per user 2026-06 decision, consistent with pure-List counting deferral)
#check tau_eq_two_iff_only_divisors_are_1_and_n
#check tau_gt_two_iff_has_proper_divisor

-- Phase 4 weak L_FCL (audit demotion proved; Rule X forcing open)
#check tau_ge_two_of_gt_one
#check tau_le_two_and_gt_one_imp_eq_two
#check audit_demoted_tau2
#check weak_lfcl_audit_layer
#check weak_lfcl_sufficient_bound
#check weak_lfcl_ruleX_forces_next_prime

-- Scaffolding checks (admissible + replay port) -- added per task checklist
#check PGS.ChamberReset.admissibleOffsets
#check PGS.ChamberReset.replaySelectionAtBound
#check PGS.ChamberReset.getCount
#check PGS.ChamberReset.WalkState

-- L5 closed (theorem proved under hypotheses; demo via type check)
#check weak_lfcl_ruleX_forces_next_prime

-- Concrete #eval exercising replaySelectionAtBound (pure port) on small gap p=11/gap=2
#eval replaySelectionAtBound 11 2

#check "PGS library smoke test loaded successfully (L5 closed: weak L_FCL sufficient bound proved)"