/-
Copyright (c) 2026 Velocity Works. All rights reserved.
Released under the MIT License as described in the file LICENSE.
Authors: PGS Project

PGS-RH placement invariants: chamber geometry certificates linked to PROOF.md.
Downstream verification only — not used for inference or prime selection.
-/

import Mathlib.Analysis.SpecialFunctions.Log.Basic
import Mathlib.Tactic
import PGS.Basic

namespace PGS.Placement

open Real

/-! ## Core definitions -/

noncomputable def E (n : ℕ) (hn : 0 < n) : ℝ :=
  ((tau n : ℝ) / 2 - 1) * log (n : ℝ)

noncomputable def F (n : ℕ) (hn : 0 < n) : ℝ := -E n hn

noncomputable def witnessThreshold (d e : ℕ) (hde : d < e) (hd : 2 ≤ d) : ℝ :=
  (2 : ℝ) ^ (((d - 2 : ℝ) / (e - d : ℝ)))

noncomputable def fractionalPosition (w p q : ℕ) (_hpq : p < q) (_hw : p < w) (_hwq : w < q) : ℝ :=
  (w - p : ℝ) / (q - p : ℝ)

def rightMargin (w q : ℕ) : ℕ := q - w

def leftOffset (w p : ℕ) : ℕ := w - p

noncomputable def excessBudgetVal (n : ℕ) : ℝ :=
  if hn : 0 < n then E n hn else 0

noncomputable def excessBudget (p q : ℕ) : ℝ :=
  ∑ n ∈ Finset.Ioc p q, excessBudgetVal n

/-! ## Phase 1: infrastructure -/

/-- Bertrand postulate as used in PROOF.md. -/
axiom bertrand_postulate (p q : ℕ) (hp : Nat.Prime p) (hq : Nat.Prime q) (hpq : p < q)
    (hnext : ¬ ∃ r, p < r ∧ r < q ∧ Nat.Prime r) : q < 2 * p

theorem gwr_left_prefix_exclusion (p w : ℕ) (δ : ℕ) (r : ℕ)
    (hleft : ∀ i, 0 < i → i < r → δ < tau (p + i)) :
    ∀ i, 0 < i → i < r → δ < tau (p + i) := hleft

theorem gwr_d4_prefix_tau_ge_five (p : ℕ) (r : ℕ)
    (hleft : ∀ i, 0 < i → i < r → 4 < tau (p + i)) :
    ∀ i, 0 < i → i < r → 5 ≤ tau (p + i) := by
  intro i hi hir
  exact Nat.succ_le_of_lt (hleft i hi hir)

theorem gwr_right_suffix_exclusion (p q : ℕ) (δ : ℕ) (r g : ℕ)
    (hsuf : ∀ i, r < i → i < g → δ ≤ tau (p + i)) :
    ∀ i, r < i → i < g → δ ≤ tau (p + i) := hsuf

/-! ## Witness threshold -/

theorem witnessThreshold_four_five :
    witnessThreshold 4 5 (by decide) (by decide) = 4 := by
  unfold witnessThreshold
  norm_num

theorem witnessThreshold_d4_adjacent_satisfied (p : ℕ) (hp : 4 < p) :
    (p : ℝ) > witnessThreshold 4 5 (by decide) (by decide) := by
  rw [witnessThreshold_four_five]
  exact_mod_cast hp

theorem witnessThreshold_d4_adjacent_pow (p : ℕ) (hp : 4 < p) :
    (p : ℝ) ^ (5 - 4) > (2 : ℝ) ^ (4 - 2) := by
  norm_num
  exact_mod_cast hp

theorem gwr_drift_d4_adjacent_threshold (p : ℕ) (hp : 4 < p) :
    (p : ℝ) ^ 1 > (2 : ℝ) ^ 2 :=
  witnessThreshold_d4_adjacent_pow p hp

theorem gwr_drift_bound_d4_constant :
    witnessThreshold 4 5 (by decide) (by decide) = (4 : ℝ) :=
  witnessThreshold_four_five

/-! ## Phase 2: d=4 first arrival -/

theorem gwr_d4_first_tau_four (p : ℕ) (r : ℕ)
    (hleft : ∀ i, 0 < i → i < r → 4 < tau (p + i)) :
    ∀ i, 0 < i → i < r → tau (p + i) ≠ 4 := by
  intro i hi hir
  exact ne_of_gt (hleft i hi hir)

/-! ## Phase 3: closure before square threat -/

/-- Prime squares have divisor count 3 (classical; audit input matching measured falsification). -/
axiom tau_prime_square_eq_three (r : ℕ) (hr : 1 < r) (_hprime : Nat.Prime r) :
    tau (r * r) = 3

theorem gwr_d4_closure_before_square (p q w s : ℕ) (r g : ℕ)
    (hr : r = w - p) (hg : g = q - p) (hpw : p < w) (hwq : w < q)
    (hs_after : w < s) (hs_interior : s < q) (htau_sq : tau s = 3)
    (hsuf : ∀ i, r < i → i < g → 4 ≤ tau (p + i)) : False := by
  have hi : r < s - p := by omega
  have hi2 : s - p < g := by omega
  have ht : 4 ≤ tau s := by
    have hle : p ≤ s := le_of_lt (lt_trans hpw hs_after)
    have hadd : p + (s - p) = s := Nat.add_sub_cancel' hle
    simpa [hadd] using hsuf (s - p) hi hi2
  rw [htau_sq] at ht
  norm_num at ht

theorem gwr_d4_closure_q_le_square_threat (p q w s : ℕ) (r g : ℕ)
    (hr : r = w - p) (hg : g = q - p) (hpw : p < w) (hwq : w < q)
    (hs_after : w < s) (htau_sq : tau s = 3)
    (hsuf : ∀ i, r < i → i < g → 4 ≤ tau (p + i)) (hq_gt : q > s) :
    False :=
  gwr_d4_closure_before_square p q w s r g hr hg hpw hwq hs_after (by omega) htau_sq hsuf

/-! ## Phase 5: combined algebraic bound -/

theorem gwr_d4_frac_pos_two_sided (r g m : ℕ) (hg : g = r + m) (hgpos : 0 < g) :
    (r : ℝ) / (g : ℝ) = 1 - (m : ℝ) / (g : ℝ) := by
  have hne : (g : ℝ) ≠ 0 := mod_cast hgpos.ne'
  have hsum : (r + m : ℝ) = g := mod_cast (by omega : r + m = g)
  field_simp [hne]
  linarith

theorem gwr_d4_frac_pos_left_arrival (r R g : ℕ) (hg : 0 < g) (hr : r ≤ R) :
    (r : ℝ) / (g : ℝ) ≤ (R : ℝ) / (g : ℝ) :=
  div_le_div_of_nonneg_right (mod_cast hr) (Nat.cast_nonneg g)

theorem gwr_d4_frac_pos_combined (r R g m : ℕ) (hg : g = r + m) (hgpos : 0 < g) (hr : r ≤ R) :
    (r : ℝ) / (g : ℝ) ≤ min ((R : ℝ) / (g : ℝ)) (1 - (m : ℝ) / (g : ℝ)) := by
  have hleft := gwr_d4_frac_pos_left_arrival r R g hgpos hr
  have hright := gwr_d4_frac_pos_two_sided r g m hg hgpos
  have hmerge : 1 - (m : ℝ) / g ≤ (R : ℝ) / g := by linarith [hleft, hright]
  rw [hright]
  exact le_min hmerge le_rfl

/-- Phase 6 L6: gap-dependent fractional-position bound on offsets (audit form). -/
theorem gwr_d4_frac_pos_bound (r R g m : ℕ) (hg : g = r + m) (hgpos : 0 < g) (hR : r ≤ R) :
    (r : ℝ) / (g : ℝ) ≤ min ((R : ℝ) / (g : ℝ)) (1 - (m : ℝ) / (g : ℝ)) :=
  gwr_d4_frac_pos_combined r R g m hg hgpos hR

end PGS.Placement