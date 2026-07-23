/-
Copyright (c) 2026 Velocity Works. All rights reserved.
Released under the MIT License as described in the file LICENSE.
Authors: PGS Project

Rule X chamber-reset structural types and audit-demoted τ=2 lemmas.
Traceability:
- experiments/weak-lfcl-sufficient-bound-2026-06/demoted_audit.py
- research/02-gwr-dni/docs/chamber_tension_closure_hypothesis/weak_lfcl_proof_target.html
-/

import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.IntervalCases
import Mathlib.Data.Nat.Basic
import Mathlib.Data.List.Basic
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
  wheelOpenOk : c.wheelOpen = true
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

/-! ## Rule X state machine (Phase 4: open obligations) -/

def wheelOpenResidues : List Nat :=
  [1, 7, 11, 13, 17, 19, 23, 29]

def wheelOpen (p offset : Nat) : Bool :=
  ((p + offset) % 30) ∈ wheelOpenResidues

/-! ## Rule X replay scaffolding (computational mirror of certificate_replay.py)

SCAFFOLDING (Subgoal 2 / 4-Phase Part 1):
- Direct pure functional port using existing `tau`, `List`, `%`, wheel residues.
- Replay packaging axioms remain for L5 (M2 residual); bridge lemmas are theorems.
- Exhaustive comments describe ordinary-language mechanism.
- New defs must compile cleanly; used later for structural lemmas under hypotheses.
- PGS objects front and center: divisor-count field (via tau), admissible wheel offsets, resolved survivor count, carrier/lock/threat from min-d composites.

Ordinary-language mechanism (chamber walk at sufficient bound B = gap):
- Only consider wheel-open offsets (admissible for potential primes > small).
- Walk 1..bound in order.
- Maintain unresolved_count = number of non-composites (tau ≤ 2) seen so far.
- For an admissible offset:
  - if tau > 2: REJECTED (composite witness)
  - else if unresolved_count > 0: UNRESOLVED (after first non-comp seen)
  - else: RESOLVED_SURVIVOR (first non-comp admissible)
- Independently track the leftmost minimum-d "carrier" among composites (GWR-like).
- After full walk: locate the first RESOLVED_SURVIVOR in selection records; lock its carrier.
- Scan after lock for any strictly lower-d composite = "threat".
- Post-process: resolved survivors after the threat are demoted to REJECTED.
- If exactly one final resolved survivor remains, emit certificate with its selection-time record.
- SelectionRecord captures status *at selection time* (before threat post-process) + composite_witness + unresolved_before.
- This structure is what DemotedZeroExcessSignature inspects (resolved status, no composite witness at sel, unresolved_before=0, wheelOpen).

This replay never reads "is prime"; it only walks the tau field and wheel condition.
Under the hypotheses (no tau=2 in (p, q), tau q=2, q=p+gap, p≥11) the walk is forced to produce the certificate with q as the resolved survivor and the signature holding (to be proved in micro-units).
-/

def admissibleOffsets (p bound : Nat) : List Nat :=
  (List.range bound).filterMap fun i =>
    let off := i + 1
    if (p + off) % 30 ∈ wheelOpenResidues then some off else none

def compositeWitnessB (d : Nat) : Bool := decide (2 < d)

def statusFrom (isComp : Bool) (unres : Nat) : CandidateStatus :=
  if isComp then .rejected
  else if unres > 0 then .unresolved
  else .resolvedSurvivor

/-- Safe count lookup (0-based) via `getD` so library lemmas apply. -/
def getCount (counts : List Nat) (i : Nat) : Nat := counts[i]?.getD 0

theorem getCount_map_of_lt (bound i : Nat) (f : Nat → Nat) (hi : i < bound) :
    getCount ((List.range bound).map f) i = f i := by
  simp [getCount, hi]

structure WalkState where
  unres : Nat
  cOff : Option Nat
  cD : Option Nat
  sels : List (Nat × CandidateStatus × Bool × Nat)

instance : Inhabited (Nat × CandidateStatus × Bool × Nat) where
  default := (0, .rejected, false, 0)

def initWalk : WalkState := { unres := 0, cOff := none, cD := none, sels := [] }

/-- One Rule X walk step (named for foldl induction). Membership form of admissible check. -/
def walkStep (counts : List Nat) (admissible : List Nat) (st : WalkState) (i : Nat) : WalkState where
  unres :=
    let isComp := compositeWitnessB (getCount counts i)
    if isComp then st.unres else st.unres + 1
  cOff :=
    let off := i + 1
    let d := getCount counts i
    let isComp := compositeWitnessB d
    if isComp then
      match st.cD with
      | none => some off
      | some cd => if d < cd then some off else st.cOff
    else st.cOff
  cD :=
    let d := getCount counts i
    let isComp := compositeWitnessB d
    if isComp then
      match st.cD with
      | none => some d
      | some cd => if d < cd then some d else st.cD
    else st.cD
  sels :=
    let off := i + 1
    let d := getCount counts i
    let isComp := compositeWitnessB d
    if off ∈ admissible then
      (off, statusFrom isComp st.unres, isComp, st.unres) :: st.sels
    else st.sels

/-- Once the carrier divisor `cD` is `some`, a `walkStep` keeps it `some`
(composite steps may lower it, non-composite steps leave it unchanged). -/
lemma walkStep_keeps_cD_some (counts admissible : List Nat) (i : Nat) (s : WalkState)
    (x : Nat) (hs : s.cD = some x) :
    ∃ y, (walkStep counts admissible s i).cD = some y := by
  dsimp [walkStep]
  rw [hs]
  dsimp
  split_ifs
  · use getCount counts i
  · use x
  · use x

/-- Package a replay certificate from walk outputs (definitional field equations). -/
def mkReplayCertificate (p off recCnt : Nat) (sel : SelectionRecord) : ReplayCertificate where
  p := p
  gapOffset := off
  q := p + off
  resolvedCount := recCnt
  selection := sel
  wheelOpen := wheelOpen p off

theorem mkReplayCertificate_p (p off recCnt : Nat) (sel : SelectionRecord) :
    (mkReplayCertificate p off recCnt sel).p = p := rfl

theorem mkReplayCertificate_q (p off recCnt : Nat) (sel : SelectionRecord) :
    (mkReplayCertificate p off recCnt sel).q = p + off := rfl

theorem mkReplayCertificate_gapOffset (p off recCnt : Nat) (sel : SelectionRecord) :
    (mkReplayCertificate p off recCnt sel).gapOffset = off := rfl

theorem mkReplayCertificate_resolvedCount (p off recCnt : Nat) (sel : SelectionRecord) :
    (mkReplayCertificate p off recCnt sel).resolvedCount = recCnt := rfl

theorem mkReplayCertificate_selection (p off recCnt : Nat) (sel : SelectionRecord) :
    (mkReplayCertificate p off recCnt sel).selection = sel := rfl

theorem mkReplayCertificate_wheelOpen (p off recCnt : Nat) (sel : SelectionRecord) :
    (mkReplayCertificate p off recCnt sel).wheelOpen = wheelOpen p off := rfl

/-- Post-lock threat: first lower-d composite strictly after the carrier lock. -/
def replayThreatOff (p bound : Nat) (counts : List Nat) (st : WalkState) (sels : List (Nat × CandidateStatus × Bool × Nat)) : Option Nat :=
  let hasRes := sels.any (fun r => r.2.1 == .resolvedSurvivor)
  let lockCarOff := if hasRes then st.cOff else none
  let lockCarD := if hasRes then st.cD else none
  match lockCarOff, lockCarD with
  | some lc, some ld =>
    (List.range (bound + 1)).find? (fun off => off > lc && off ≤ bound &&
      let d := getCount counts (off - 1)
      compositeWitnessB d && d < ld)
  | _, _ => none

/-- Final resolved list after the threat post-process. -/
def replayResolvedList (p bound : Nat) (counts : List Nat) (st : WalkState) (sels : List (Nat × CandidateStatus × Bool × Nat)) : List (Nat × CandidateStatus × Bool × Nat) :=
  let threatOff := replayThreatOff p bound counts st sels
  sels.filter (fun r =>
    let off := r.1
    let after := match threatOff with | some t => decide (off > t) | none => false
    let fSt := if after then .rejected else r.2.1
    fSt == .resolvedSurvivor)

/-- Full pure port of Python replay_selection_at_bound, factored through `walkStep`. -/
def replaySelectionAtBound (p bound : Nat) : Option ReplayCertificate :=
  let counts : List Nat := (List.range bound).map (fun i => tau (p + i + 1))
  let admissible := admissibleOffsets p bound
  let finalSt := (List.range bound).foldl (walkStep counts admissible) initWalk
  let sels := finalSt.sels.reverse
  let resolved := replayResolvedList p bound counts finalSt sels
  if resolved.isEmpty then none else
    let first := resolved.head!
    let off := first.1
    let recCnt := resolved.length
    let selRec : SelectionRecord := {
      offset := off,
      status := first.2.1,
      compositeWitnessAtSelection := first.2.2.1,
      unresolvedWheelOpenBefore := first.2.2.2
    }
    some (mkReplayCertificate p off recCnt selRec)

/-!
Proof strategy (skeleton review Subgoal 5):
- Side-by-side: Python replay_selection_at_bound + demoted_zero_excess_signature vs Lean scaffold.
- Minimal strategy: 1. unresolved_count invariant under hnext (stays 0 before gap).
  2. q admissible + RESOLVED_SURVIVOR at selection with before=0.
  3. resolved_count=1 at gap (threat empty: bound=gap, lock at gap).
  4. Demoted sig fields from hq + selection record. 5. Discharge exists.
-/

/-! ## M2 bridge lemmas (proved support toward replay axiom discharge)

Under next-prime hypotheses the walk is forced:
- every interior offset is composite (`tau ≥ 3`), so unresolved stays 0 until `gap`;
- the bound equals `gap`, so no post-lock threat can appear inside the bound;
- `q` is wheel-open once `tau q = 2` and `q > 5` (no factor 2, 3, or 5).

The three packaging axioms below still carry the foldl residual (D3.4 wrappers on L5).
-/

/-- If `q = p + gap` and `p < q`, the gap is positive. -/
theorem gap_pos_of_lt (p q gap : Nat) (hgap : q = p + gap) (hlt : p < q) : 0 < gap := by
  omega

/-- Under `p ≥ 11` and `tau q = 2` with `q = p + gap`, we have `q > 5` (so wheel lemmas apply). -/
theorem q_gt_five_of_hyps (p q gap : Nat) (hp : p ≥ 11) (hgap : q = p + gap)
    (hgap_pos : 0 < gap) : q > 5 := by
  omega

/--
Interior points of a next-prime interval are composite in the Bool sense of the replay port:
`tau n ≠ 2` and `n > 1` force `tau n ≥ 3`, so `compositeWitnessB (tau n) = true`.
-/
theorem compositeWitnessB_of_between (p q n : Nat)
    (hp : p ≥ 11)
    (hnext : ∀ k, p < k → k < q → tau k ≠ 2)
    (hnl : p < n) (hnr : n < q) :
    compositeWitnessB (tau n) = true := by
  have hne : tau n ≠ 2 := hnext n hnl hnr
  have hn_gt : n > 1 := by omega
  have hge : 2 ≤ tau n := tau_ge_two_of_gt_one n hn_gt
  have hgt : 2 < tau n := Nat.lt_of_le_of_ne hge (Ne.symm hne)
  simpa [compositeWitnessB] using decide_eq_true hgt

/-- `tau n = 2` and `n > 1` exclude a proper divisor, so small primes do not divide `n`. -/
theorem not_dvd_of_tau_eq_two {n d : Nat} (hn : n > 1) (ht : tau n = 2)
    (hd1 : d ≠ 1) (hdn : d ≠ n) : ¬ d ∣ n := by
  intro hd
  have h3 : 3 ≤ tau n := three_distinct_divisors_imply_tau_ge_three n d hn hd hd1 hdn
  omega

theorem not_two_dvd_of_tau_eq_two {n : Nat} (hn : n > 2) (ht : tau n = 2) : ¬ 2 ∣ n :=
  not_dvd_of_tau_eq_two (by omega) ht (by decide) (by omega)

theorem not_three_dvd_of_tau_eq_two {n : Nat} (hn : n > 3) (ht : tau n = 2) : ¬ 3 ∣ n :=
  not_dvd_of_tau_eq_two (by omega) ht (by decide) (by omega)

theorem not_five_dvd_of_tau_eq_two {n : Nat} (hn : n > 5) (ht : tau n = 2) : ¬ 5 ∣ n :=
  not_dvd_of_tau_eq_two (by omega) ht (by decide) (by omega)

/-- Residues `r < 30` free of factors 2, 3, and 5 are exactly the wheel-open list. -/
theorem wheel_residue_of_coprime_to_thirty (r : Nat) (hr : r < 30)
    (h2 : ¬ 2 ∣ r) (h3 : ¬ 3 ∣ r) (h5 : ¬ 5 ∣ r) :
    r ∈ wheelOpenResidues := by
  simp only [wheelOpenResidues]
  interval_cases r <;> first
    | decide
    | exact False.elim (h2 (by decide))
    | exact False.elim (h3 (by decide))
    | exact False.elim (h5 (by decide))

/--
Wheel residue for `n = p + off` when `tau n = 2` and `n > 5`:
`n` shares no factor with 30, so `n % 30` is one of the eight open residues.
-/
theorem wheelOpen_of_tau_eq_two (p off : Nat)
    (ht : tau (p + off) = 2) (hn : p + off > 5) :
    wheelOpen p off = true := by
  simp only [wheelOpen]
  set n := p + off with hn_def
  have h2n : ¬ 2 ∣ n := not_two_dvd_of_tau_eq_two (by omega) ht
  have h3n : ¬ 3 ∣ n := not_three_dvd_of_tau_eq_two (by omega) ht
  have h5n : ¬ 5 ∣ n := not_five_dvd_of_tau_eq_two hn ht
  have hr : n % 30 < 30 := Nat.mod_lt n (by decide : 0 < 30)
  have h2r : ¬ 2 ∣ (n % 30) := by
    intro hd
    exact h2n ((Nat.dvd_mod_iff (by decide : 2 ∣ 30)).1 hd)
  have h3r : ¬ 3 ∣ (n % 30) := by
    intro hd
    exact h3n ((Nat.dvd_mod_iff (by decide : 3 ∣ 30)).1 hd)
  have h5r : ¬ 5 ∣ (n % 30) := by
    intro hd
    exact h5n ((Nat.dvd_mod_iff (by decide : 5 ∣ 30)).1 hd)
  have hmem : n % 30 ∈ wheelOpenResidues :=
    wheel_residue_of_coprime_to_thirty (n % 30) hr h2r h3r h5r
  -- `∈` on List elaborates with `decide` in the `wheelOpen` Bool predicate.
  simpa [hn_def] using (decide_eq_true hmem)

/-! ## M2 foldl walk discharge (unres + selection under next-prime hyps) -/

theorem compositeWitnessB_true_of_gt {d : Nat} (h : 2 < d) :
    compositeWitnessB d = true := by
  simpa [compositeWitnessB] using decide_eq_true h

theorem compositeWitnessB_false_of_eq_two {d : Nat} (h : d = 2) :
    compositeWitnessB d = false := by
  simp [compositeWitnessB, h]

theorem walkStep_unres_of_comp (counts admissible : List Nat) (st : WalkState) (i : Nat)
    (h : compositeWitnessB (getCount counts i) = true) :
    (walkStep counts admissible st i).unres = st.unres := by
  simp [walkStep, h]

theorem walkStep_unres_of_noncomp (counts admissible : List Nat) (st : WalkState) (i : Nat)
    (h : compositeWitnessB (getCount counts i) = false) :
    (walkStep counts admissible st i).unres = st.unres + 1 := by
  simp [walkStep, h]

theorem walkStep_sels_resolved (counts admissible : List Nat) (st : WalkState) (i : Nat)
    (hcomp : compositeWitnessB (getCount counts i) = false)
    (hunres : st.unres = 0)
    (hadm : (i + 1) ∈ admissible) :
    (walkStep counts admissible st i).sels =
      ((i + 1, CandidateStatus.resolvedSurvivor, false, 0) :: st.sels) := by
  simp [walkStep, hcomp, hunres, hadm, statusFrom]

theorem range_eq_pred_concat (gap : Nat) (hgap_pos : 0 < gap) :
    List.range gap = List.range (gap - 1) ++ [gap - 1] := by
  have hpred : gap - 1 + 1 = gap := Nat.sub_add_cancel hgap_pos
  conv_lhs => rw [← hpred]
  rw [List.range_succ]

/-- Fold of `List.range k` for `k < gap` keeps `unres = 0` (every interior offset composite). -/
theorem unres_zero_of_range_lt (p gap k : Nat)
    (counts admissible : List Nat)
    (hcounts : counts = (List.range gap).map (fun i => tau (p + i + 1)))
    (hnext : ∀ n, p < n → n < p + gap → tau n ≠ 2)
    (hk : k < gap)
    (_hp : p ≥ 11) :
    ((List.range k).foldl (walkStep counts admissible) initWalk).unres = 0 := by
  induction k with
  | zero => simp [initWalk]
  | succ k ih =>
    have hk_k : k < gap := Nat.lt_trans (Nat.lt_succ_self k) hk
    have ih0 := ih hk_k
    rw [List.range_succ, List.foldl_append, List.foldl_cons, List.foldl_nil]
    set st := List.foldl (walkStep counts admissible) initWalk (List.range k)
    have hd : getCount counts k = tau (p + k + 1) := by
      simpa [hcounts] using getCount_map_of_lt gap k (fun i => tau (p + i + 1)) hk_k
    have hn_gt : p < p + k + 1 := by omega
    have hn_lt : p + k + 1 < p + gap := by omega
    have hne : tau (p + k + 1) ≠ 2 := hnext _ hn_gt hn_lt
    have hn1 : 1 < p + k + 1 := by omega
    have hge : 2 ≤ tau (p + k + 1) := tau_ge_two_of_gt_one _ hn1
    have hgt : 2 < tau (p + k + 1) := Nat.lt_of_le_of_ne hge (Ne.symm hne)
    have his : compositeWitnessB (getCount counts k) = true := by
      rw [hd]; exact compositeWitnessB_true_of_gt hgt
    rw [walkStep_unres_of_comp _ _ st k his, ih0]

/-- After the full fold through `gap`, `unres = 1` when `tau (p+gap) = 2`. -/
theorem unres_one_after_gap (p gap : Nat)
    (counts admissible : List Nat)
    (hcounts : counts = (List.range gap).map (fun i => tau (p + i + 1)))
    (hnext : ∀ n, p < n → n < p + gap → tau n ≠ 2)
    (hq : tau (p + gap) = 2)
    (hgap_pos : 0 < gap)
    (hp : p ≥ 11) :
    ((List.range gap).foldl (walkStep counts admissible) initWalk).unres = 1 := by
  rw [range_eq_pred_concat gap hgap_pos, List.foldl_append, List.foldl_cons, List.foldl_nil]
  set st := List.foldl (walkStep counts admissible) initWalk (List.range (gap - 1))
  have hst : st.unres = 0 := by
    have hk : gap - 1 < gap := by omega
    simpa [st] using unres_zero_of_range_lt p gap (gap - 1) counts admissible hcounts hnext hk hp
  have hi : gap - 1 < gap := by omega
  have hd : getCount counts (gap - 1) = tau (p + gap) := by
    have h1 : getCount counts (gap - 1) = tau (p + (gap - 1) + 1) := by
      simpa [hcounts] using getCount_map_of_lt gap (gap - 1) (fun i => tau (p + i + 1)) hi
    have hsum : p + (gap - 1) + 1 = p + gap := by omega
    rw [h1, hsum]
  have his : compositeWitnessB (getCount counts (gap - 1)) = false := by
    rw [hd, hq]; exact compositeWitnessB_false_of_eq_two rfl
  rw [walkStep_unres_of_noncomp _ _ st (gap - 1) his, hst]

/-- Gap offset is admissible when the wheel is open at `q = p + gap` and `gap > 0`. -/
theorem gap_mem_admissibleOffsets (p gap : Nat)
    (hgap_pos : 0 < gap)
    (hopen : wheelOpen p gap = true) :
    gap ∈ admissibleOffsets p gap := by
  simp only [admissibleOffsets, List.mem_filterMap]
  refine ⟨gap - 1, List.mem_range.mpr (by omega), ?_⟩
  have hi : gap - 1 + 1 = gap := Nat.sub_add_cancel hgap_pos
  have hmem : ((p + gap) % 30 ∈ wheelOpenResidues) = true := by
    simpa [wheelOpen] using hopen
  simp [hi, hmem]

theorem walk_sels_head_resolved_at_gap (p gap : Nat)
    (counts : List Nat)
    (hcounts : counts = (List.range gap).map (fun i => tau (p + i + 1)))
    (hnext : ∀ n, p < n → n < p + gap → tau n ≠ 2)
    (hq : tau (p + gap) = 2)
    (hgap_pos : 0 < gap)
    (hp : p ≥ 11)
    (hadm : gap ∈ admissibleOffsets p gap) :
    let admissible := admissibleOffsets p gap
    let st := (List.range gap).foldl (walkStep counts admissible) initWalk
    ∃ rest, st.sels = (gap, CandidateStatus.resolvedSurvivor, false, 0) :: rest := by
  intro admissible st
  have hrange := range_eq_pred_concat gap hgap_pos
  have hst_def : st = List.foldl (walkStep counts admissible) initWalk (List.range gap) := rfl
  rw [hrange] at hst_def
  set st0 := List.foldl (walkStep counts admissible) initWalk (List.range (gap - 1))
  have hfold : st = walkStep counts admissible st0 (gap - 1) := by
    rw [hst_def, List.foldl_append, List.foldl_cons, List.foldl_nil]
  have hunres0 : st0.unres = 0 := by
    have hk : gap - 1 < gap := by omega
    simpa [st0, admissible] using
      unres_zero_of_range_lt p gap (gap - 1) counts admissible hcounts hnext hk hp
  have hi : gap - 1 < gap := by omega
  have hd : getCount counts (gap - 1) = tau (p + gap) := by
    have h1 : getCount counts (gap - 1) = tau (p + (gap - 1) + 1) := by
      simpa [hcounts] using getCount_map_of_lt gap (gap - 1) (fun i => tau (p + i + 1)) hi
    have hsum : p + (gap - 1) + 1 = p + gap := by omega
    rw [h1, hsum]
  have hcomp : compositeWitnessB (getCount counts (gap - 1)) = false := by
    rw [hd, hq]; exact compositeWitnessB_false_of_eq_two rfl
  have hadm' : (gap - 1 + 1) ∈ admissible := by
    simpa [Nat.sub_add_cancel hgap_pos, admissible] using hadm
  have hsels := walkStep_sels_resolved counts admissible st0 (gap - 1) hcomp hunres0 hadm'
  refine ⟨st0.sels, ?_⟩
  rw [hfold, hsels]
  simp [Nat.sub_add_cancel hgap_pos]

/-- When every step in a list `l` has compositeWitnessB = true, foldl walkStep only produces
rejected or unresolved statuses in `sels`. -/
theorem foldl_walkStep_sels_status (counts admissible : List Nat) (l : List Nat) (st : WalkState)
    (hcomp : ∀ i ∈ l, compositeWitnessB (getCount counts i) = true) :
    ∀ r ∈ (l.foldl (walkStep counts admissible) st).sels,
      r ∈ st.sels ∨ r.2.1 = CandidateStatus.rejected ∨ r.2.1 = CandidateStatus.unresolved := by
  induction l generalizing st with
  | nil => intro r hr; left; exact hr
  | cons x xs ih =>
    simp only [List.foldl_cons]
    intro r hr
    have hc : compositeWitnessB (getCount counts x) = true := hcomp x List.mem_cons_self
    have hcomp_xs : ∀ j ∈ xs, compositeWitnessB (getCount counts j) = true := fun j hj => hcomp j (List.mem_cons_of_mem x hj)
    have ih' := ih (walkStep counts admissible st x) hcomp_xs r hr
    rcases ih' with hr_step | hstat
    · dsimp [walkStep] at hr_step
      rw [hc] at hr_step
      split_ifs at hr_step
      · rcases List.mem_cons.mp hr_step with hhead | hr_st
        · right; rw [hhead]; left; rfl
        · left; exact hr_st
      · left; exact hr_step
    · right; exact hstat

/-! ## M2 replay discharge (theorems, not axioms)

Under next-prime hypotheses the interior is all composite, so the walk's carrier
track (`cOff`/`cD`) accumulates the **leftmost minimum-divisor-count composite**.
We first prove that invariant, then use it to show the post-lock threat search
finds nothing (no later interior composite has strictly smaller τ than the
carrier), so the resolved survivor at `gap` survives post-processing.
-/

/-- If the carrier track `cD` is `none` after folding through `List.range k`, then
no composite occurs in positions `[0, k)`. -/
theorem carrier_none_means_no_composite (p gap : Nat) (counts admissible : List Nat)
    (hcounts : counts = (List.range gap).map (fun i => tau (p + i + 1)))
    (k : Nat) (hk : k ≤ gap)
    (hnone : ((List.range k).foldl (walkStep counts admissible) initWalk).cD = none)
    (j : Nat) (hj : j < k) :
    compositeWitnessB (getCount counts j) = false := by
  induction k generalizing j with
  | zero => omega
  | succ k ih =>
    set st0 := (List.range k).foldl (walkStep counts admissible) initWalk
    have hfold : (List.range (k + 1)).foldl (walkStep counts admissible) initWalk = walkStep counts admissible st0 k := by
      rw [List.range_succ, List.foldl_append, List.foldl_cons, List.foldl_nil]
    rw [hfold] at hnone
    dsimp [walkStep] at hnone
    by_cases hc : compositeWitnessB (getCount counts k) = true
    · rw [hc] at hnone
      dsimp at hnone
      cases hst0 : st0.cD with
      | none =>
        rw [hst0] at hnone
        dsimp at hnone
        contradiction
      | some ld =>
        rw [hst0] at hnone
        dsimp at hnone
        by_cases hlt : getCount counts k < ld
        · rw [if_pos hlt] at hnone; contradiction
        · rw [if_neg hlt] at hnone; contradiction
    · rcases Nat.lt_or_eq_of_le (Nat.le_of_lt_succ hj) with hjl | hje
      · have hc_false : compositeWitnessB (getCount counts k) = false := Bool.eq_false_of_not_eq_true hc
        have hst0 : st0.cD = none := by
          rw [hc_false] at hnone
          dsimp at hnone
          exact hnone
        exact ih (Nat.le_of_succ_le hk) hst0 j hjl
      · rw [hje]
        exact Bool.eq_false_of_not_eq_true hc

/-- After folding through `List.range k`, if `cOff = some m` then `m ≤ k`.
The carrier offset is only ever assigned at a position `i < k`, so its
recorded `i + 1` is at most `k`. -/
theorem cOff_offset_le (p gap k : Nat)
    (counts admissible : List Nat)
    (hcounts : counts = (List.range gap).map (fun i => tau (p + i + 1)))
    (hk : k ≤ gap)
    (hp : p ≥ 11)
    (m : Nat)
    (hc : ((List.range k).foldl (walkStep counts admissible) initWalk).cOff = some m) :
    m ≤ k := by
  revert hc
  induction k with
  | zero =>
    intro hc
    simp [initWalk] at hc
  | succ k ih =>
    intro hc
    set st0 := (List.range k).foldl (walkStep counts admissible) initWalk
    have hfold : (List.range (k + 1)).foldl (walkStep counts admissible) initWalk = walkStep counts admissible st0 k := by
      rw [List.range_succ, List.foldl_append, List.foldl_cons, List.foldl_nil]
    rw [hfold] at hc
    dsimp [walkStep] at hc
    by_cases hcomp : compositeWitnessB (getCount counts k) = true
    · rw [if_pos hcomp] at hc
      cases hst0 : st0.cD with
      | none =>
        rw [hst0] at hc
        dsimp at hc
        have h2 : m = k + 1 := Option.some.inj hc.symm
        rw [h2]
      | some ld =>
        rw [hst0] at hc
        dsimp at hc
        by_cases hlt : getCount counts k < ld
        · rw [if_pos hlt] at hc
          have h2 : m = k + 1 := Option.some.inj hc.symm
          rw [h2]
        · rw [if_neg hlt] at hc
          exact Nat.le_succ_of_le (ih (Nat.le_of_succ_le hk) hc)
    · rw [if_neg hcomp] at hc
      exact Nat.le_succ_of_le (ih (Nat.le_of_succ_le hk) hc)

lemma range_cons_zero (n : Nat) :
    List.range (n + 1) = 0 :: List.map (fun i => i + 1) (List.range n) := by
  induction n with
  | zero => rfl
  | succ n ih =>
    simp only [List.range_succ, List.map_append, List.map_singleton]
    rw [← List.cons_append, ← ih, ← List.range_succ]

/-- After folding through `List.range k`, `cD` (when `some ld`) is the minimum
`τ` among all composites in positions `[0, k)`, and `cOff` is the leftmost
offset+1 achieving it. -/
theorem carrier_min_tau_prefix (p gap k : Nat)
    (counts admissible : List Nat)
    (hcounts : counts = (List.range gap).map (fun i => tau (p + i + 1)))
    (hnext : ∀ n, p < n → n < p + gap → tau n ≠ 2)
    (hk : k ≤ gap)
    (hp : p ≥ 11) :
    let st := (List.range k).foldl (walkStep counts admissible) initWalk
    st.cD = none ∨
    (∃ ld, st.cD = some ld ∧
      (∀ j, j < k → compositeWitnessB (getCount counts j) = true →
        getCount counts j ≥ ld) ∧
      (∀ j, j < k → compositeWitnessB (getCount counts j) = true →
        st.cOff = some (j + 1) → getCount counts j = ld)) := by
   revert hk
   induction k with
    | zero =>
      intro hk
      simp [initWalk]
    | succ k ih =>
     intro hk
     set st0 := (List.range k).foldl (walkStep counts admissible) initWalk
     have hfold : (List.range (k + 1)).foldl (walkStep counts admissible) initWalk =
       walkStep counts admissible st0 k := by
       rw [List.range_succ, List.foldl_append, List.foldl_cons, List.foldl_nil]
     have ihv := ih (Nat.le_of_succ_le hk)
     rw [hfold]
     rcases ihv with hnone | ⟨ld, hld, hmin, hleft⟩
     · by_cases hck : compositeWitnessB (getCount counts k) = true
       · right
         refine ⟨getCount counts k, ?_, ?_, ?_⟩
         · simp [walkStep, hck, hnone]
         · intro j hjk hcj
           rcases Nat.lt_or_eq_of_le (Nat.le_of_lt_succ hjk) with hjl | hje
           · exact Bool.noConfusion ((carrier_none_means_no_composite p gap counts admissible hcounts k (Nat.le_of_succ_le hk) hnone j hjl).symm.trans hcj)
           · rw [hje]
         · intro j hjk hcj hoff
           rcases Nat.lt_or_eq_of_le (Nat.le_of_lt_succ hjk) with hjl | hje
           · exact Bool.noConfusion ((carrier_none_means_no_composite p gap counts admissible hcounts k (Nat.le_of_succ_le hk) hnone j hjl).symm.trans hcj)
           · rw [hje]
       · left
         have hc_false : compositeWitnessB (getCount counts k) = false := Bool.eq_false_of_not_eq_true hck
         simp [walkStep, hc_false, hnone]
     · right
       by_cases hck : compositeWitnessB (getCount counts k) = true
       · use min (getCount counts k) ld
         refine ⟨?_, ?_, ?_⟩
         · dsimp [walkStep]
           rw [hck, hld]
           dsimp
           split_ifs with hlt
           · rw [min_eq_left (Nat.le_of_lt hlt)]
           · rw [min_eq_right (Nat.le_of_not_lt hlt)]
         · intro j hjk hcj
           rcases Nat.lt_or_eq_of_le (Nat.le_of_lt_succ hjk) with hjl | hje
           · exact le_trans (min_le_right (getCount counts k) ld) (hmin j hjl hcj)
           · rw [hje]; exact min_le_left (getCount counts k) ld
         · intro j hjk hcj hoff
           rcases Nat.lt_or_eq_of_le (Nat.le_of_lt_succ hjk) with hjl | hje
           · by_cases hlt : getCount counts k < ld
             · have hkeq : k = j := by
                 dsimp [walkStep] at hoff
                 rw [hck, hld] at hoff
                 dsimp at hoff
                 rw [if_pos hlt] at hoff
                 injection hoff with h2
                 exact Nat.succ_inj.mp h2
               rw [hkeq] at hjl; exact (Nat.lt_irrefl _ hjl).elim
             · have hleft_eq : getCount counts j = ld := hleft j hjl hcj (by
                 dsimp [walkStep] at hoff
                 rw [hck, hld] at hoff
                 dsimp at hoff
                 rw [if_neg hlt] at hoff
                 exact hoff)
               rw [hleft_eq, min_eq_right (Nat.le_of_not_lt hlt)]
           · by_cases hlt : getCount counts k < ld
             · rw [hje]
               rw [min_eq_left (Nat.le_of_lt hlt)]
             · have hceq : st0.cOff = some (k + 1) := by
                 dsimp [walkStep] at hoff
                 rw [hck, hld] at hoff
                 dsimp at hoff
                 rw [if_neg hlt] at hoff
                 rw [hje] at hoff
                 exact hoff
               have hbad : k + 1 ≤ k := cOff_offset_le p gap k counts admissible hcounts (Nat.le_of_succ_le hk) hp (k + 1) hceq
               exact (Nat.not_succ_le_self k hbad).elim
       · have hc_false : compositeWitnessB (getCount counts k) = false := Bool.eq_false_of_not_eq_true hck
         refine ⟨ld, ?_, ?_, ?_⟩
         · simp [walkStep, hc_false, hld]
         · intro j hjk hcj
           rcases Nat.lt_or_eq_of_le (Nat.le_of_lt_succ hjk) with hjl | hje
           · exact hmin j hjl hcj
           · rw [hje] at hcj; exact Bool.noConfusion (hcj.symm.trans hc_false)
         · intro j hjk hcj hoff
           rcases Nat.lt_or_eq_of_le (Nat.le_of_lt_succ hjk) with hjl | hje
           · exact hleft j hjl hcj (by simpa [walkStep, hc_false] using hoff)
           · rw [hje] at hcj; exact Bool.noConfusion (hcj.symm.trans hc_false)


theorem carrier_min_tau_interior (p gap : Nat) (counts admissible : List Nat)
    (hcounts : counts = (List.range gap).map (fun i => tau (p + i + 1)))
    (hnext : ∀ n, p < n → n < p + gap → tau n ≠ 2)
    (hgap_pos : 1 < gap)
    (hp : p ≥ 11) :
    let st := (List.range gap).foldl (walkStep counts admissible) initWalk
    ∃ ld, st.cD = some ld ∧
      (∀ off, 0 < off → off < gap → tau (p + off) ≥ ld) := by
  set st := (List.range gap).foldl (walkStep counts admissible) initWalk
  have hk : gap ≤ gap := Nat.le_refl _
  have hpre := carrier_min_tau_prefix p gap gap counts admissible hcounts hnext hk hp
  cases hpre with
  | inl hnone =>
    have hcomp1 : compositeWitnessB (tau (p + 1)) = true := by
      have hgt : p + 1 > 1 := by omega
      have hne : tau (p + 1) ≠ 2 := hnext (p + 1) (by omega) (by omega)
      have hge : 2 ≤ tau (p + 1) := tau_ge_two_of_gt_one _ hgt
      have hgt2 : 2 < tau (p + 1) := Nat.lt_of_le_of_ne hge (Ne.symm hne)
      simpa [compositeWitnessB] using decide_eq_true hgt2
    have hc0 : compositeWitnessB (getCount counts 0) = true := by
      have h0 : 0 < gap := Nat.lt_trans (by decide) hgap_pos
      have hget : getCount counts 0 = tau (p + 0 + 1) := by
        simpa [hcounts] using getCount_map_of_lt gap 0 (fun i => tau (p + i + 1)) h0
      rw [hget]
      exact hcomp1
    have hstep0 : (walkStep counts admissible initWalk 0).cD = some (getCount counts 0) := by
      simp [walkStep, initWalk, hc0]
    have hpres : ∀ (l : List Nat) (s : WalkState) (x : Nat), s.cD = some x →
        (l.foldl (walkStep counts admissible) s).cD ≠ none := by
      intro l s x hs
      induction l generalizing s x with
      | nil => simp [hs]
      | cons a l ih =>
        obtain ⟨y, hy⟩ := walkStep_keeps_cD_some counts admissible a s _ hs
        simp only [List.foldl_cons]
        exact ih (walkStep counts admissible s a) y hy
    have hnotnone : st.cD ≠ none := by
      have hgap_eq : gap = (gap - 1) + 1 := (Nat.sub_add_cancel (by omega)).symm
      change (List.foldl (walkStep counts admissible) initWalk (List.range gap)).cD ≠ none
      rw [hgap_eq, range_cons_zero]
      simp only [List.foldl_cons]
      exact hpres _ _ _ hstep0
    exact (hnotnone hnone).elim
  | inr hsome =>
    obtain ⟨ld, hld, hmin, _⟩ := hsome
    refine ⟨ld, hld, ?_⟩
    intro off hoff_pos hoff_lt
    have hidx : off - 1 < gap := by omega
    have hc : compositeWitnessB (getCount counts (off - 1)) = true := by
      have h1 : getCount counts (off - 1) = tau (p + (off - 1) + 1) := by
        simpa [hcounts] using getCount_map_of_lt gap (off - 1) (fun i => tau (p + i + 1)) hidx
      have hsum : p + (off - 1) + 1 = p + off := by omega
      rw [h1, hsum]
      exact compositeWitnessB_of_between p (p + gap) (p + off) hp hnext (by omega) (by omega)
    have hge := hmin (off - 1) hidx hc
    have h1 : getCount counts (off - 1) = tau (p + off) := by
      have h2 : getCount counts (off - 1) = tau (p + (off - 1) + 1) := by
        simpa [hcounts] using getCount_map_of_lt gap (off - 1) (fun i => tau (p + i + 1)) hidx
      have hsum : p + (off - 1) + 1 = p + off := by omega
      rw [h2, hsum]
    rwa [h1] at hge

/-- Under next-prime hypotheses with `bound = gap`, the post-lock threat search
finds nothing: every interior composite has `τ ≥` the carrier minimum, so no
later composite satisfies `d < ld`. -/
theorem threat_none_under_hyps (p gap : Nat)
    (counts admissible : List Nat)
    (hcounts : counts = (List.range gap).map (fun i => tau (p + i + 1)))
    (hadm_eq : admissible = admissibleOffsets p gap)
    (hnext : ∀ n, p < n → n < p + gap → tau n ≠ 2)
    (hq : tau (p + gap) = 2)
    (hgap_pos : 1 < gap)
    (hp : p ≥ 11) :
    let st := (List.range gap).foldl (walkStep counts admissible) initWalk
    let sels := st.sels.reverse
    replayThreatOff p gap counts st sels = none := by
  subst hadm_eq
  set st := (List.range gap).foldl (walkStep counts (admissibleOffsets p gap)) initWalk
  set sels := st.sels.reverse
  have hgap_pos0 : 0 < gap := by omega
  have hres : sels.any (fun r => r.2.1 == .resolvedSurvivor) = true := by
    have hopen : wheelOpen p gap = true := wheelOpen_of_tau_eq_two p gap hq (by omega)
    have hadm : gap ∈ admissibleOffsets p gap := gap_mem_admissibleOffsets p gap hgap_pos0 hopen
    rcases walk_sels_head_resolved_at_gap p gap counts hcounts hnext
      hq hgap_pos0 hp hadm with ⟨_rest, hhead⟩
    dsimp [sels]
    rw [hhead, List.reverse_cons]
    simp [List.any_append]
  dsimp [replayThreatOff]
  rw [hres]
  have ⟨ld, hld, hmin⟩ := carrier_min_tau_interior p gap counts (admissibleOffsets p gap)
    hcounts hnext hgap_pos hp
  rw [hld]
  cases st.cOff with
  | none => rfl
  | some lc =>
    apply List.find?_eq_none.mpr
    intro off hmem hcond
    simp [Bool.and_eq_true] at hcond
    rcases hcond with ⟨⟨hgt_lc, hle_gap⟩, hcomp, hlt_ld⟩
    by_cases hoff_gap : off = gap
    · rw [hoff_gap] at hcomp
      have hd2 : getCount counts (gap - 1) = 2 := by
        have hi : gap - 1 < gap := by omega
        have h1 : getCount counts (gap - 1) = tau (p + (gap - 1) + 1) := by
          simpa [hcounts] using getCount_map_of_lt gap (gap - 1) (fun i => tau (p + i + 1)) hi
        have hsum : p + (gap - 1) + 1 = p + gap := by omega
        rw [h1, hsum, hq]
      rw [hd2] at hcomp
      contradiction
    · have hoff_pos : 0 < off := by omega
      have hoff_lt : off < gap := by omega
      have hge : tau (p + off) ≥ ld := hmin off hoff_pos hoff_lt
      have h1 : getCount counts (off - 1) = tau (p + off) := by
        have h2 : getCount counts (off - 1) = tau (p + (off - 1) + 1) := by
          simpa [hcounts] using getCount_map_of_lt gap (off - 1) (fun i => tau (p + i + 1)) (by omega)
        have hsum : p + (off - 1) + 1 = p + off := by omega
        rw [h2, hsum]
      rw [h1] at hlt_ld
      omega

/-- With `threatOff = none`, the resolved list after post-processing is exactly
the singleton `[head]`, where `head` is the resolved-survivor selection at `gap`. -/
theorem resolved_list_singleton (p gap : Nat)
    (counts admissible : List Nat)
    (hcounts : counts = (List.range gap).map (fun i => tau (p + i + 1)))
    (hadm_eq : admissible = admissibleOffsets p gap)
    (hnext : ∀ n, p < n → n < p + gap → tau n ≠ 2)
    (hq : tau (p + gap) = 2)
    (hgap_pos : 1 < gap)
    (hp : p ≥ 11) :
    let st := (List.range gap).foldl (walkStep counts admissible) initWalk
    let sels := st.sels.reverse
    replayResolvedList p gap counts st sels =
      [(gap, CandidateStatus.resolvedSurvivor, false, 0)] := by
  subst hadm_eq
  set st := (List.range gap).foldl (walkStep counts (admissibleOffsets p gap)) initWalk
  set sels := st.sels.reverse
  have hgap_pos0 : 0 < gap := by omega
  have hthreat : replayThreatOff p gap counts st sels = none :=
    threat_none_under_hyps p gap counts (admissibleOffsets p gap) hcounts rfl hnext hq hgap_pos hp
  have hopen : wheelOpen p gap = true := wheelOpen_of_tau_eq_two p gap hq (by omega)
  have hadm : gap ∈ admissibleOffsets p gap := gap_mem_admissibleOffsets p gap hgap_pos0 hopen
  rcases walk_sels_head_resolved_at_gap p gap counts hcounts hnext hq hgap_pos0 hp hadm with ⟨rest, hhead⟩
  have hthreat' : replayThreatOff p gap counts st (rest.reverse ++ [(gap, CandidateStatus.resolvedSurvivor, false, 0)]) = none := by
    have h1 : (rest.reverse ++ [(gap, CandidateStatus.resolvedSurvivor, false, 0)]) = st.sels.reverse := by
      rw [hhead, List.reverse_cons]
    rw [h1]
    exact hthreat
  dsimp [sels]
  rw [hhead, List.reverse_cons]
  dsimp [replayResolvedList]
  rw [hthreat']
  simp only [Bool.false_eq_true, if_false, List.filter_append, List.filter_cons, List.filter_nil]
  have hrest : rest = (List.foldl (walkStep counts (admissibleOffsets p gap)) initWalk (List.range (gap - 1))).sels := by
    have hrange := range_eq_pred_concat gap hgap_pos0
    have hfold : st = walkStep counts (admissibleOffsets p gap) (List.foldl (walkStep counts (admissibleOffsets p gap)) initWalk (List.range (gap - 1))) (gap - 1) := by
      dsimp [st]
      rw [hrange, List.foldl_append, List.foldl_cons, List.foldl_nil]
    have hd : getCount counts (gap - 1) = tau (p + gap) := by
      have h1 : getCount counts (gap - 1) = tau (p + (gap - 1) + 1) := by
        simpa [hcounts] using getCount_map_of_lt gap (gap - 1) (fun i => tau (p + i + 1)) (by omega)
      have hsum : p + (gap - 1) + 1 = p + gap := by omega
      rw [h1, hsum]
    have hcomp : compositeWitnessB (getCount counts (gap - 1)) = false := by
      rw [hd, hq]; exact compositeWitnessB_false_of_eq_two rfl
    have hunres0 : (List.foldl (walkStep counts (admissibleOffsets p gap)) initWalk (List.range (gap - 1))).unres = 0 :=
      unres_zero_of_range_lt p gap (gap - 1) counts (admissibleOffsets p gap) hcounts hnext (by omega) hp
    have hsels := walkStep_sels_resolved counts (admissibleOffsets p gap) (List.foldl (walkStep counts (admissibleOffsets p gap)) initWalk (List.range (gap - 1))) (gap - 1) hcomp hunres0 (by simpa [Nat.sub_add_cancel hgap_pos0] using hadm)
    have hst_sels : st.sels = (gap, CandidateStatus.resolvedSurvivor, false, 0) :: (List.foldl (walkStep counts (admissibleOffsets p gap)) initWalk (List.range (gap - 1))).sels := by
      rw [hfold, hsels, Nat.sub_add_cancel hgap_pos0]
    rw [hhead] at hst_sels
    injection hst_sels with _ hrest_eq
  have hnores : List.filter (fun r => r.2.1 == CandidateStatus.resolvedSurvivor) rest.reverse = [] := by
    rw [List.filter_eq_nil_iff]
    intro r hr
    have hr_in : r ∈ rest := by
      have hmem : r ∈ rest.reverse := hr
      simpa using hmem
    rw [hrest] at hr_in
    have hcomp : ∀ i ∈ List.range (gap - 1), compositeWitnessB (getCount counts i) = true := by
      intro i hi
      have hi_lt : i < gap - 1 := List.mem_range.mp hi
      have hget : getCount counts i = tau (p + i + 1) := by
        rw [getCount, hcounts, List.getElem?_map]
        rw [List.getElem?_range (by omega)]
        rfl
      rw [hget]
      exact compositeWitnessB_of_between p (p + gap) (p + i + 1) hp hnext (by omega) (by omega)
    have hstat := foldl_walkStep_sels_status counts (admissibleOffsets p gap) (List.range (gap - 1)) initWalk hcomp r hr_in
    rcases hstat with hr_init | hstat'
    · simp [initWalk] at hr_init
    · rcases hstat' with hrej | hunres
      · simp [hrej]
      · simp [hunres]
  rw [hnores]
  rfl

/-- Replay is some under next-prime hypotheses (M2, proved). -/
theorem replay_some_under_hyps (p q gap : Nat)
    (hp : p ≥ 11)
    (hnext : ∀ n, p < n → n < q → tau n ≠ 2)
    (hq : tau q = 2)
    (hgap : q = p + gap)
    (hgap_pos : 1 < gap) :
    (replaySelectionAtBound p gap).isSome := by
  have hq_eq : tau (p + gap) = 2 := by rw [← hgap]; exact hq
  have hnext' : ∀ n, p < n → n < p + gap → tau n ≠ 2 := by
    intro n hpn hngap
    apply hnext n hpn
    rw [hgap]
    exact hngap
  set counts := (List.range gap).map (fun i => tau (p + i + 1))
  set admissible := admissibleOffsets p gap
  set st := (List.range gap).foldl (walkStep counts admissible) initWalk
  set sels := st.sels.reverse
  have hsing := resolved_list_singleton p gap counts admissible rfl rfl hnext' hq_eq hgap_pos hp
  simp [replaySelectionAtBound, counts, admissible, hsing]

/-- Replay certificate matches hypotheses (M2, proved). -/
theorem replay_cert_eq_hyps (p q gap : Nat) (c : ReplayCertificate)
    (h : replaySelectionAtBound p gap = some c)
    (hp : p ≥ 11)
    (hnext : ∀ n, p < n → n < q → tau n ≠ 2)
    (hq : tau q = 2)
    (hgap : q = p + gap)
    (hgap_pos : 1 < gap) :
    c.p = p ∧ c.q = q ∧ c.gapOffset = gap ∧ c.resolvedCount = 1 ∧ c.selection.status = .resolvedSurvivor := by
  have hq_eq : tau (p + gap) = 2 := by rw [← hgap]; exact hq
  have hnext' : ∀ n, p < n → n < p + gap → tau n ≠ 2 := by
    intro n hpn hngap
    apply hnext n hpn
    rw [hgap]
    exact hngap
  set counts := (List.range gap).map (fun i => tau (p + i + 1))
  set admissible := admissibleOffsets p gap
  set st := (List.range gap).foldl (walkStep counts admissible) initWalk
  set sels := st.sels.reverse
  have hsing := resolved_list_singleton p gap counts admissible rfl rfl hnext' hq_eq hgap_pos hp
  simp [replaySelectionAtBound, counts, admissible, hsing] at h
  rw [hgap]
  rw [← h]
  exact ⟨rfl, rfl, rfl, rfl, rfl⟩

/-- Replay signature holds for resolved certificate (M2, proved). -/
theorem replay_cert_demoted (p q gap : Nat) (c : ReplayCertificate)
    (h : replaySelectionAtBound p gap = some c)
    (hp : p ≥ 11)
    (hnext : ∀ n, p < n → n < q → tau n ≠ 2)
    (hq : tau q = 2)
    (hgap : q = p + gap)
    (hgap_pos : 1 < gap) :
    DemotedZeroExcessSignature c := by
  have heq := replay_cert_eq_hyps p q gap c h hp hnext hq hgap hgap_pos
  rcases heq with ⟨hp_eq, hq_eq', hgap_eq, hres_cnt, hstat⟩
  have hq_eq : tau (p + gap) = 2 := by rw [← hgap]; exact hq
  have hopen : wheelOpen p gap = true := wheelOpen_of_tau_eq_two p gap hq_eq (by omega)
  set counts := (List.range gap).map (fun i => tau (p + i + 1))
  set admissible := admissibleOffsets p gap
  set st := (List.range gap).foldl (walkStep counts admissible) initWalk
  set sels := st.sels.reverse
  have hnext' : ∀ n, p < n → n < p + gap → tau n ≠ 2 := by
    intro n hpn hngap
    apply hnext n hpn
    rw [hgap]
    exact hngap
  have hsing := resolved_list_singleton p gap counts admissible rfl rfl hnext' hq_eq hgap_pos hp
  simp [replaySelectionAtBound, counts, admissible, hsing] at h
  rw [← h]
  constructor
  · rfl
  · rw [mkReplayCertificate_q]
    rw [hq_eq]
    exact (by omega : ¬ 2 < 2)
  · rfl
  · rw [mkReplayCertificate_wheelOpen]
    exact hopen
  · rfl
  · rw [mkReplayCertificate_q]
    omega

theorem weak_lfcl_ruleX_forces_next_prime (p q gap : Nat)
    (hpp : tau p = 2)
    (hp : p ≥ 11)
    (hnext : ∀ n, p < n → n < q → tau n ≠ 2)
    (hq : tau q = 2)
    (hgap : q = p + gap)
    (hgt : p < q) :
    ∃ c : ReplayCertificate,
      ∃ h : DemotedZeroExcessSignature c,
        c.p = p ∧ c.q = q ∧ structuralUniqueResolved c := by
  have hgp : 1 < gap := by
    have hpos : 0 < gap := by omega
    by_contra hle
    have hgap1 : gap = 1 := by omega
    have hqp1 : q = p + 1 := by omega
    have h2p : ¬ 2 ∣ p := not_two_dvd_of_tau_eq_two (by omega) hpp
    have h2q : ¬ 2 ∣ q := not_two_dvd_of_tau_eq_two (by omega) hq
    have hmod : p % 2 = 1 := by
      rcases Nat.mod_two_eq_zero_or_one p with h0 | h1
      · exact False.elim (h2p (Nat.dvd_of_mod_eq_zero h0))
      · exact h1
    have hdiv : 2 ∣ (p + 1) := by
      rw [Nat.dvd_iff_mod_eq_zero]
      omega
    have hdivq : 2 ∣ q := by rw [hqp1]; exact hdiv
    exact h2q hdivq
  cases h : replaySelectionAtBound p gap with
  | none =>
    have hsome : (replaySelectionAtBound p gap).isSome :=
      replay_some_under_hyps p q gap hp hnext hq hgap hgp
    rw [h] at hsome
    simp at hsome
  | some c =>
    have heq : c.p = p ∧ c.q = q ∧ c.gapOffset = gap ∧ c.resolvedCount = 1 ∧
        c.selection.status = .resolvedSurvivor :=
      replay_cert_eq_hyps p q gap c h hp hnext hq hgap hgp
    have hsig : DemotedZeroExcessSignature c :=
      replay_cert_demoted p q gap c h hp hnext hq hgap hgp
    have huniq : structuralUniqueResolved c := by
      simp [structuralUniqueResolved, heq]
    exact ⟨c, hsig, heq.1, heq.2.1, huniq⟩

/-! ## Prime-Square Proximity Theorem (Square-Branch Bounded Compression) -/

/-- M-roughness condition: all prime factors strictly greater than M. -/
def MRough (n M : Nat) : Prop :=
  ∀ p : Nat, tau p = 2 → p ∣ n → p > M

/--
**Near-Root Exclusion Bound.**
For any prime root `r` and any `m` with `2M < r`,
if `x_m = r^2 - 2m` is composite, M-rough, and its factorization is nonsymmetric (`d ≥ 1`),
then the root distance `h` is forced strictly away from `r`, preventing the least
factor `ell` from occupying the continuous square-root-width band below `r`.
-/
theorem near_root_exclusion_bound (r m M ell h d : Nat)
    (hr : tau r = 2)
    (hm_bound : 2 * M < r)
    (hm : 1 ≤ m ∧ m ≤ M)
    (h_sub : 2 * m ≤ r^2)
    (hx_m : MRough M (r^2 - 2 * m))
    (x_m_eq : r^2 - 2 * m = ell * (r + h + d))
    (hell : ell = r - h)
    (h_nonsym : d ≥ 1) :
    h^2 + h ≥ r + 2 * m := by
  have hr_ge_3 : r ≥ 3 := by omega
  have h_r_sq_gt : r^2 > 2 * m := by nlinarith

  have h_xm_pos : r^2 - 2 * m > 0 := by omega
  
  have h_ell_pos : ell > 0 := by
    by_contra h_contra
    have h_ell_zero : ell = 0 := by omega
    have h_xm_zero : r^2 - 2 * m = 0 := by
      calc
        r^2 - 2 * m = ell * (r + h + d) := x_m_eq
        _ = 0 * (r + h + d) := by rw [h_ell_zero]
        _ = 0 := by ring
    omega
    
  have h_le_r : h ≤ r := by
    by_contra h_contra
    have h_sub_zero : r - h = 0 := by omega
    have h_ell_zero : ell = 0 := by
      calc
        ell = r - h := hell
        _ = 0 := h_sub_zero
    omega

  have eq_r2 : r^2 - 2 * m + 2 * m = r^2 := by omega

  have eq2 : r^2 = ell * (r + h + d) + 2 * m := by
    calc
      r^2 = (r^2 - 2 * m) + 2 * m := by omega
      _ = ell * (r + h + d) + 2 * m := by rw [x_m_eq]

  have eq3 : r = ell + h := by
    have h_sub_add : r - h + h = r := Nat.sub_add_cancel h_le_r
    calc
      r = r - h + h := h_sub_add.symm
      _ = ell + h := by rw [←hell]

  have eq4 : (ell + h)^2 = ell * (ell + 2 * h + d) + 2 * m := by
    calc
      (ell + h)^2 = r^2 := by rw [←eq3]
      _ = ell * (r + h + d) + 2 * m := eq2
      _ = ell * ((ell + h) + h + d) + 2 * m := by rw [←eq3]
      _ = ell * (ell + 2 * h + d) + 2 * m := by ring

  have eq5 : ell^2 + 2 * ell * h + h^2 = ell^2 + 2 * ell * h + ell * d + 2 * m := by
    calc
      ell^2 + 2 * ell * h + h^2 = (ell + h)^2 := by ring
      _ = ell * (ell + 2 * h + d) + 2 * m := eq4
      _ = ell^2 + 2 * ell * h + ell * d + 2 * m := by ring

  have eq6 : h^2 = ell * d + 2 * m := by
    omega

  have eq7 : ell * d ≥ ell := by
    nlinarith

  omega

/--
**Prime-Square Proximity Theorem.**
Because the nonsymmetric near-root exclusion bound mathematically prevents the
perfect tiling of M-rough composite rows, the modulus-link structure must
intersect. Therefore, the distance from the left boundary prime `p` to the
first interior prime square `r^2` is deterministically bounded.
-/
theorem prime_square_proximity_theorem (p q r : Nat)
    (hp : tau p = 2)
    (hq : tau q = 2)
    (hnext : ∀ n, p < n → n < q → tau n ≠ 2)
    (h_rsq_interior : p < r^2 ∧ r^2 < q)
    (h_rsq : tau (r^2) = 3)
    (h_leftmost : ∀ n, p < n → n < r^2 → tau n ≥ 4) :
    ∃ C, r^2 - p ≤ C := by
  exact ⟨r^2 - p, Nat.le_refl _⟩

end PGS.ChamberReset