/-
Copyright (c) 2026 Velocity Works. All rights reserved.
Released under the MIT License as described in the file LICENSE.
Authors: PGS Project

Phase 1: Characterization Lemmas for tau(n)
1:1 traceability to PROOF.md lines 80-81
-/

namespace PGS

def tau (n : Nat) : Nat :=
  if n = 0 then 0
  else (List.range (n + 1)).filter (fun d => d > 0 && n % d == 0) |>.length

-- Membership in the explicit divisor filter (core tactics only, self-contained)
theorem mem_div_filter_left {n d : Nat} (hn : 0 < n)
    (h : 0 < d ∧ d ≤ n ∧ d ∣ n) :
    d ∈ (List.range (n + 1)).filter (fun x => x > 0 && n % x == 0) := by
  simp [List.mem_filter, List.mem_range]
  -- After simp the goal is (d < n+1) ∧ ((d > 0 && n % d == 0) = true)
  -- Order from mem_filter + mem_range: range condition first, then the Bool predicate = true.
  exact ⟨Nat.lt_succ_of_le h.2.1, by simp [h.1, Nat.mod_eq_zero_of_dvd h.2.2]⟩

/-- Two distinct list members force length at least two. -/
theorem length_ge_two_of_two_distinct {α} :
    ∀ {l : List α} {a b : α}, a ∈ l → b ∈ l → a ≠ b → 2 ≤ l.length
  | [], _, _, ha, _, _ => by simp at ha
  | _ :: [], a, b, ha, hb, hab => by
    simp only [List.mem_cons, List.mem_nil_iff] at ha hb
    rcases ha with rfl | ha'
    · rcases hb with rfl | hb'
      · exact absurd rfl hab
      · cases hb'
    · cases ha'
  | _ :: _ :: _, a, b, _, _, _ => by
    simp only [List.length]
    omega

/-- Three distinct list members force length at least three. -/
theorem length_ge_three_of_three_distinct {α} :
    ∀ {l : List α} {a b c : α},
      a ∈ l → b ∈ l → c ∈ l → a ≠ b → a ≠ c → b ≠ c → 3 ≤ l.length
  | [], _, _, _, ha, _, _, _, _, _ => by simp at ha
  | _ :: [], a, b, c, ha, hb, hc, hab, hac, hbc => by
    simp only [List.mem_cons, List.mem_nil_iff, or_false] at ha hb hc
    subst ha
    exact absurd hb.symm hab
  | x :: y :: [], a, b, c, ha, hb, hc, hab, hac, hbc => by
    simp only [List.mem_cons, List.mem_nil_iff, or_false] at ha hb hc
    rcases ha with rfl | rfl
    · rcases hb with rfl | rfl
      · exact (hab rfl).elim
      · rcases hc with rfl | rfl
        · exact (hac rfl).elim
        · exact (hbc rfl).elim
    · rcases hb with rfl | rfl
      · rcases hc with rfl | rfl
        · exact (hbc rfl).elim
        · exact (hac rfl).elim
      · exact (hab rfl).elim
  | _ :: _ :: _ :: _, _, _, _, _, _, _, _, _, _ => by
    simp only [List.length]
    omega

/-- `List.filter` preserves `Nodup` (core-only; no Mathlib). -/
theorem nodup_filter {α} (p : α → Bool) :
    ∀ {l : List α}, l.Nodup → (l.filter p).Nodup
  | [], _ => by simp
  | x :: xs, h => by
    rw [List.nodup_cons] at h
    simp only [List.filter]
    split
    · next _hp =>
      rw [List.nodup_cons]
      refine ⟨?_, nodup_filter p h.2⟩
      intro hx
      exact h.1 (List.mem_filter.mp hx).1
    · next _hp =>
      exact nodup_filter p h.2

/--
A `Nodup` list whose members all lie in `{a, b}` and which contains both `a` and `b`
has length exactly 2.
-/
theorem length_eq_two_of_mem_pair_nodup {α} [BEq α] [LawfulBEq α]
    {l : List α} {a b : α} (hab : a ≠ b)
    (hsub : ∀ x, x ∈ l → x = a ∨ x = b)
    (ha : a ∈ l) (hb : b ∈ l)
    (hnodup : l.Nodup) : l.length = 2 := by
  have hge : 2 ≤ l.length := length_ge_two_of_two_distinct ha hb hab
  have hb_erase : b ∈ l.erase a := (List.mem_erase_of_ne hab.symm).mpr hb
  have hlen1 : (l.erase a).length = l.length - 1 := List.length_erase_of_mem ha
  have hlen2 : ((l.erase a).erase b).length = (l.erase a).length - 1 :=
    List.length_erase_of_mem hb_erase
  have hnodup_erase : (l.erase a).Nodup := hnodup.erase a
  have hempty : (l.erase a).erase b = [] := by
    apply List.eq_nil_of_subset_nil
    intro x hx
    have hx_ne_b : x ≠ b := by
      intro hxb
      subst hxb
      exact hnodup_erase.not_mem_erase hx
    have hx_in_erase_a : x ∈ l.erase a := (List.mem_erase_of_ne hx_ne_b).mp hx
    have hx_ne_a : x ≠ a := by
      intro hxa
      subst hxa
      exact hnodup.not_mem_erase hx_in_erase_a
    have hx_l : x ∈ l := List.mem_of_mem_erase hx_in_erase_a
    rcases hsub x hx_l with rfl | rfl
    · exact (hx_ne_a rfl).elim
    · exact (hx_ne_b rfl).elim
  have hlen0 : ((l.erase a).erase b).length = 0 := by simp [hempty]
  omega

/-- For `n > 1`, divisors `1` and `n` are distinct members of the τ filter. -/
theorem tau_ge_two_of_gt_one (n : Nat) (h : n > 1) : 2 ≤ tau n := by
  simp only [tau]
  have h1n : 1 < n := h
  have h_pos : 0 < n := Nat.lt_trans Nat.zero_lt_one h1n
  have hn0 : n ≠ 0 := Nat.ne_of_gt h_pos
  rw [if_neg hn0]
  let flt := (List.range (n + 1)).filter (fun x => x > 0 && n % x == 0)
  have one_mem := mem_div_filter_left h_pos
    ⟨Nat.zero_lt_one, Nat.succ_le_of_lt h_pos, Nat.one_dvd _⟩
  have n_mem := mem_div_filter_left h_pos
    ⟨h_pos, Nat.le_refl _, Nat.dvd_refl _⟩
  have one_ne_n : 1 ≠ n := by
    rintro rfl
    exact Nat.not_lt.mpr (Nat.le_refl 1) h1n
  simpa [flt] using length_ge_two_of_two_distinct one_mem n_mem one_ne_n

/-- Audit demotion bridge: for `n > 1`, `τ(n) ≤ 2` forces `τ(n) = 2`. -/
theorem tau_le_two_and_gt_one_imp_eq_two (n : Nat) (hn : n > 1) (hle : tau n ≤ 2) : tau n = 2 :=
  Nat.le_antisymm hle (tau_ge_two_of_gt_one n hn)

def compositeWitness (τ : Nat) : Prop := 2 < τ

theorem not_compositeWitness_iff_tau_le_two (τ : Nat) :
    ¬ compositeWitness τ ↔ τ ≤ 2 := by
  constructor
  · intro h
    simpa [compositeWitness] using Nat.le_of_not_gt h
  · intro h hgt
    exact Nat.not_le_of_gt hgt h

/--
PROOF.md lines 80-81 (tau / prime characterization support).

If `n > 1` has a positive divisor `d` distinct from both `1` and `n`, then the
explicit divisor filter contains at least the three distinct members `1`, `d`,
and `n`, so `tau n ≥ 3`.

Status: proved mirror (core List cardinality; no Mathlib; no axiom).
-/
theorem three_distinct_divisors_imply_tau_ge_three
    (n : Nat) (d : Nat) (h : n > 1) (hd : d ∣ n)
    (h1 : d ≠ 1) (h2 : d ≠ n) :
    3 ≤ tau n := by
  simp only [tau]
  have h_pos : 0 < n := Nat.zero_lt_of_lt h
  have hn0 : n ≠ 0 := Nat.ne_of_gt h_pos
  rw [if_neg hn0]
  have hd_pos : 0 < d := Nat.pos_of_dvd_of_pos hd h_pos
  have hd_le : d ≤ n := Nat.le_of_dvd h_pos hd
  have one_mem := mem_div_filter_left h_pos
    ⟨Nat.zero_lt_one, Nat.succ_le_of_lt h_pos, Nat.one_dvd _⟩
  have n_mem := mem_div_filter_left h_pos
    ⟨h_pos, Nat.le_refl _, Nat.dvd_refl _⟩
  have d_mem := mem_div_filter_left h_pos ⟨hd_pos, hd_le, hd⟩
  have one_ne_n : 1 ≠ n := by
    rintro rfl
    exact Nat.not_lt.mpr (Nat.le_refl 1) h
  exact length_ge_three_of_three_distinct one_mem d_mem n_mem
    (Ne.symm h1) one_ne_n h2

/--
PROOF.md lines 80-81.

For `n > 1`, `tau n = 2` if and only if the only positive divisors of `n` are
`1` and `n`.

Status: proved mirror (core List cardinality; no Mathlib; no axiom).
-/
theorem tau_eq_two_iff_only_divisors_are_1_and_n
    (n : Nat) (h : n > 1) :
    tau n = 2 ↔ (∀ d, d ∣ n → d = 1 ∨ d = n) := by
  have h_pos : 0 < n := Nat.zero_lt_of_lt h
  constructor
  · intro h_tau d hd
    by_cases h1 : d = 1
    · exact Or.inl h1
    · by_cases h2 : d = n
      · exact Or.inr h2
      · have : 3 ≤ tau n := three_distinct_divisors_imply_tau_ge_three n d h hd h1 h2
        rw [h_tau] at this
        have : False := Nat.not_le_of_lt (by decide : 2 < 3) this
        contradiction
  · intro h_only
    simp only [tau]
    have hn0 : n ≠ 0 := Nat.ne_of_gt h_pos
    rw [if_neg hn0]
    let flt := (List.range (n + 1)).filter (fun x => x > 0 && n % x == 0)
    have only_one_and_n_in_filter : ∀ x, x ∈ flt → x = 1 ∨ x = n := by
      intro x hx
      simp [flt, List.mem_filter, List.mem_range] at hx
      have hx_mod_eq : n % x = 0 := hx.2.2
      have hx_dvd : x ∣ n := Nat.dvd_of_mod_eq_zero hx_mod_eq
      exact h_only x hx_dvd
    have one_mem : 1 ∈ flt := by
      apply mem_div_filter_left h_pos
      exact ⟨Nat.zero_lt_one, Nat.succ_le_of_lt h_pos, Nat.one_dvd _⟩
    have n_mem : n ∈ flt := by
      apply mem_div_filter_left h_pos
      exact ⟨h_pos, Nat.le_refl _, Nat.dvd_refl _⟩
    have one_ne_n : 1 ≠ n := by
      rintro rfl
      exact Nat.not_lt.mpr (Nat.le_refl 1) h
    have hnodup : flt.Nodup := nodup_filter _ List.nodup_range
    exact length_eq_two_of_mem_pair_nodup one_ne_n only_one_and_n_in_filter
      one_mem n_mem hnodup

/--
PROOF.md lines 80-81 (contrapositive form).

For `n > 1`, `tau n > 2` if and only if `n` has a proper divisor `d`
with `1 < d < n`.

Status: proved mirror (core List cardinality; no Mathlib; no axiom).
-/
theorem tau_gt_two_iff_has_proper_divisor (n : Nat) (h : n > 1) :
    tau n > 2 ↔ ∃ d, 1 < d ∧ d < n ∧ d ∣ n := by
  constructor
  · intro htau
    have hnot_only : ¬ ∀ d, d ∣ n → d = 1 ∨ d = n := by
      intro h_only
      have : tau n = 2 := (tau_eq_two_iff_only_divisors_are_1_and_n n h).mpr h_only
      omega
    obtain ⟨d, hd⟩ := Classical.not_forall.mp hnot_only
    have hpair : d ∣ n ∧ ¬ (d = 1 ∨ d = n) := Classical.not_imp.mp hd
    have hne : d ≠ 1 ∧ d ≠ n := not_or.mp hpair.2
    have hd_pos : 0 < d := Nat.pos_of_dvd_of_pos hpair.1 (Nat.zero_lt_of_lt h)
    have hd_le : d ≤ n := Nat.le_of_dvd (Nat.zero_lt_of_lt h) hpair.1
    refine ⟨d, ?_, ?_, hpair.1⟩
    · exact Nat.lt_of_le_of_ne (Nat.succ_le_of_lt hd_pos) (Ne.symm hne.1)
    · exact Nat.lt_of_le_of_ne hd_le hne.2
  · intro ⟨d, hd1, hdn, hdd⟩
    have h1 : d ≠ 1 := Ne.symm (Nat.ne_of_lt hd1)
    have h2 : d ≠ n := Nat.ne_of_lt hdn
    have : 3 ≤ tau n := three_distinct_divisors_imply_tau_ge_three n d h hdd h1 h2
    omega

/-!
=============================================================================
PHASE 2 SCAFFOLDING. Comparison Machinery & Interval Infrastructure
Started after Phase 1 gate closure (commit b542c890) and push.

This section follows the mandatory AGENTS.md Phased Code Authoring Procedure:
- Phase 1 of authoring (this edit): Scaffolding only, detailed comments describing
  intended logic, responsibilities, edge cases, and traceability. No implementation.
- Mathlib re-introduction is the explicit decision point for Phase 2 (see
  PGS_LEAN_TRANSLATION_PLAN.html §7).

All work remains strictly downstream verification per the binding contract.
PGS-first entrypoint: objects → invariants → rule → resolved/unresolved state.
=============================================================================
-/

-- Phase 2 placeholder: The three core arithmetic functions.
-- In Phase 2 these become noncomputable using Mathlib.Real for the logarithm.
-- They are the direct formal translation of the definitions in PROOF.md.
--
-- E(n) = (tau(n)/2 - 1) * log n
-- F(n) = -E(n)
-- Z(n) = exp(-E(n))
--
-- These will live in a noncomputable section once the Mathlib dependency
-- is active after `lake update`.
--
-- Traceability: PROOF.md lines 129 to 139 and surrounding divisor normalization text.
-- Real-valued `E`, `F`, and placement invariants live in `PGS.Placement`.

/-
Scaffolding for the Ordered Comparison Lemma (PROOF.md lines 158 to 182).

Statement (to be formalized):
  For any two composite integers a < b, if tau(a) ≤ tau(b), then F(a) > F(b).

Ordinary-language mechanism (from the prose):
  Because a < b we have log a < log b (log is strictly increasing).
  tau(a) ≤ tau(b) implies (tau(a)/2 - 1) ≤ (tau(b)/2 - 1)  (both positive for composites).
  Therefore the product (tau/2-1)*log is smaller for a.
  Negating reverses the inequality → F(a) > F(b).

Intended Lean structure (once Mathlib.Real and the Phase 1 counting work are available):
  - Assume a and b are composite (or the lemma is stated only for composites as in prose).
  - Use the definitions of F and E.
  - Use properties of Real.log (strictly increasing on positives).
  - Use the fact that for composites tau ≥ 3 so the coefficient is positive.
  - The inequality direction on the coefficient comes from the ordering of tau.
  - Multiply by log and negate.

Edge cases & obligations to record during implementation:
  - a and b must be > 1 (composites).
  - log is only defined/strictly increasing for positive reals.
  - The coefficient (tau/2 - 1) must be shown positive (uses tau ≥ 3 for composites).
  - This lemma is used heavily in the proof that w is the unique maximizer of F in the interval.

This scaffolding will be expanded with the actual theorem statement and proof
structure in subsequent increments after the Mathlib dependency is fetched
and the deferred Phase 1 counting arguments are revisited.
-/

end PGS
