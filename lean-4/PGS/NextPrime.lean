/-
Copyright (c) 2026 Velocity Works. All rights reserved.
Released under the MIT License as described in the file LICENSE.
Authors: PGS Project

Direct next-prime theorem + weak L_FCL (Phase 4).
Traceability: PROOF.md §§1 to 2, weak_lfcl_proof_target.html
-/

import PGS.Basic
import PGS.ChamberReset

namespace PGS.NextPrime

open PGS.ChamberReset

/-! ## Direct τ-scan next prime (PROOF.md) -/

/-- Proved selection rule from PROOF.md: formal definition deferred to Phase 4b. -/
def IsNextPrime (p q : Nat) : Prop :=
  (∀ n, p < n → n < q → tau n ≠ 2) ∧ tau q = 2

/-! ## Weak L_FCL exports -/

theorem audit_demoted_tau2_of_certificate {c : ReplayCertificate}
    (h : DemotedZeroExcessSignature c) : tau c.q = 2 :=
  audit_demoted_tau2_of_demoted_signature h

/-- Audit layer: demoted structural signature implies `τ(q) = 2`. -/
theorem weak_lfcl_audit_layer {c : ReplayCertificate}
    (h : DemotedZeroExcessSignature c) : tau c.q = 2 :=
  audit_demoted_tau2_of_demoted_signature h

/-- Package next-prime hypotheses once Rule X replay is formalized. -/
theorem weak_lfcl_sufficient_bound (p q gap : Nat)
    (hpp : tau p = 2)
    (hp : p ≥ 11)
    (hnext : ∀ n, p < n → n < q → tau n ≠ 2)
    (hq : tau q = 2)
    (hgap : q = p + gap)
    (hgt : p < q) :
    ∃ c : ReplayCertificate,
      ∃ h : DemotedZeroExcessSignature c,
        c.p = p ∧ c.q = q ∧ structuralUniqueResolved c := by
  rcases weak_lfcl_ruleX_forces_next_prime p q gap hpp hp hnext hq hgap hgt with
    ⟨c, h, hp', hq', huniq⟩
  exact ⟨c, h, hp', hq', huniq⟩

end PGS.NextPrime