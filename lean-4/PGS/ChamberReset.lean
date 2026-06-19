/-
Copyright (c) 2026 Velocity Works. All rights reserved.
Released under the MIT License as described in the file LICENSE.
Authors: PGS Project

Rule X chamber-reset structural types and audit-demoted τ=2 lemmas.
Traceability:
- experiments/weak-lfcl-sufficient-bound-2026-06/demoted_audit.py
- research/02-gwr-dni/docs/chamber_tension_closure_hypothesis/weak_lfcl_proof_target.html
-/

import PGS.Basic

namespace PGS.ChamberReset

/-! ## Selection-time semantics (mirrors production Rule X replay) -/

inductive CandidateStatus
  | rejected
  | unresolved
  | resolvedSurvivor
  deriving DecidableEq, Repr

structure SelectionRecord where
  offset : Nat
  status : CandidateStatus
  compositeWitnessAtSelection : Bool
  unresolvedWheelOpenBefore : Nat
  deriving Repr

structure ReplayCertificate where
  p : Nat
  gapOffset : Nat
  q : Nat
  resolvedCount : Nat
  selection : SelectionRecord
  wheelOpen : Bool
  deriving Repr

def structuralUniqueResolved (c : ReplayCertificate) : Prop :=
  c.resolvedCount = 1

structure DemotedZeroExcessSignature (c : ReplayCertificate) where
  statusResolved : c.selection.status = .resolvedSurvivor
  nonCompositeWitness : ¬ compositeWitness (tau c.q)
  noPriorUnresolved : c.selection.unresolvedWheelOpenBefore = 0
  wheelOpenOk : c.wheelOpen
  offsetOk : c.q = c.p + c.gapOffset
  qGtOne : c.q > 1

/-! ## Audit-demoted τ=2 (proved) -/

/-- **Lemma L4 (audit demotion).** Non-composite-witness class at `q > 1` implies `τ(q) = 2`. -/
theorem audit_demoted_tau2 (n : Nat) (hn : n > 1) (hncw : ¬ compositeWitness (tau n)) :
    tau n = 2 := by
  have hle : tau n ≤ 2 := (not_compositeWitness_iff_tau_le_two (tau n)).mp hncw
  exact tau_le_two_and_gt_one_imp_eq_two n hn hle

theorem audit_demoted_tau2_of_demoted_signature {c : ReplayCertificate}
    (h : DemotedZeroExcessSignature c) : tau c.q = 2 :=
  audit_demoted_tau2 c.q h.qGtOne h.nonCompositeWitness

/-! ## Rule X state machine (Phase 4 — open obligations) -/

def wheelOpenResidues : List Nat :=
  [1, 7, 11, 13, 17, 19, 23, 29]

def wheelOpen (p offset : Nat) : Bool :=
  ((p + offset) % 30) ∈ wheelOpenResidues

/--
**Theorem target L5 (OPEN).** Rule X replay at `B = gap` constructs a demoted replay certificate
for the next prime. Measured: 78 493/78 493 on R2 (`weak-lfcl-sufficient-bound-2026-06`).
-/
theorem weak_lfcl_ruleX_forces_next_prime (p q gap : Nat)
    (hp : p ≥ 11)
    (hnext : ∀ n, p < n → n < q → tau n ≠ 2)
    (hq : tau q = 2)
    (hgap : q = p + gap) :
    ∃ c : ReplayCertificate,
      ∃ h : DemotedZeroExcessSignature c,
        c.p = p ∧ c.q = q ∧ structuralUniqueResolved c := by
  /-
  OPEN (Phase 4).

  Route:
  1. Translate `certificate_replay.py` to `ruleXReplay : Nat → Nat → Option ReplayCertificate`.
  2. Prove soundness vs next-prime hypotheses.
  3. Prove uniqueness of resolved survivor.
  -/
  sorry

end PGS.ChamberReset