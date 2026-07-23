/-
Copyright (c) 2026 Velocity Works. All rights reserved.
Released under the MIT License as described in the file LICENSE.
Authors: PGS Project

M3 — GWR / Interior Maximizer (DoD D4.3)
Mirror of PROOF.md §§Interior Maximizer Theorem, Ordered Comparison Lemma,
Later Integers, and the maximizer packaging that uses the earlier-integer side.

Status labels:
- proved mirror: Ordered Comparison, later-integer closure, maximizer under
  earlier-side hypothesis (or discharged prime-square earlier case)
- earlier-side general case: packaged as an explicit hypothesis matching the
  PROOF.md earlier-integer argument (Witness Threshold + Short Divisor-Average
  + finite base `gwr_finite_base_v1`). Lean does not silently assume that base.

Downstream verification only. Never used for prime selection or inference.
-/

import Mathlib.Analysis.SpecialFunctions.Log.Basic
import Mathlib.Tactic
import PGS.Basic
import PGS.Placement

namespace PGS.GWR

open Real PGS PGS.Placement

/-! ## Comparison coordinates (PROOF.md)

`E` and `F` are defined in `PGS.Placement` as the zero-excess and dual
logarithmic comparison coordinates:

```
E(n) = (τ(n)/2 - 1) * log n
F(n) = -E(n) = (1 - τ(n)/2) * log n
```

Maximizing `F` is the same ordered comparison as minimizing `E`.
-/

/-- Coefficient of `log n` in the excess coordinate: `τ/2 - 1 = (τ - 2)/2`. -/
noncomputable def excessCoeff (τ : ℕ) : ℝ := (τ : ℝ) / 2 - 1

theorem excessCoeff_eq (τ : ℕ) : excessCoeff τ = ((τ : ℝ) - 2) / 2 := by
  unfold excessCoeff
  ring

theorem excessCoeff_pos_of_tau_ge_three {τ : ℕ} (h : 3 ≤ τ) : 0 < excessCoeff τ := by
  rw [excessCoeff_eq]
  have hτ : (3 : ℝ) ≤ τ := by exact_mod_cast h
  have : (0 : ℝ) < ((τ : ℝ) - 2) := by linarith
  positivity

/-- `τ n ≥ 3` forces `n > 1` (so `log n` is positive under the comparison lemmas). -/
theorem one_lt_of_tau_ge_three {n : ℕ} (h : 3 ≤ tau n) : 1 < n := by
  by_contra hne
  have hnle : n ≤ 1 := Nat.not_lt.mp hne
  have htau : tau n ≤ 1 := by
    match n with
    | 0 => simp [tau]
    | 1 =>
      -- divisors of 1: only 1, so length 1
      simp only [tau, if_neg (by decide : (1 : ℕ) ≠ 0)]
      native_decide
    | _ + 2 => omega
  omega

theorem E_eq_coeff_mul_log (n : ℕ) (hn : 0 < n) :
    E n hn = excessCoeff (tau n) * log (n : ℝ) := by
  rfl

theorem F_eq_neg_E (n : ℕ) (hn : 0 < n) : F n hn = -E n hn := rfl

theorem F_eq_neg_coeff_mul_log (n : ℕ) (hn : 0 < n) :
    F n hn = -(excessCoeff (tau n) * log (n : ℝ)) := by
  rfl

/-! ## Interval and selected-witness predicates -/

/-- Nonempty open interior of a consecutive-prime gap `(p, q)`. -/
def GapInterior (p q : ℕ) : Prop := p + 1 < q

/-- `w` is an interior point of the gap `(p, q)`. -/
def InGapInterior (p q w : ℕ) : Prop := p < w ∧ w < q

/--
Leftmost minimum-`τ` witness inside `(p, q)`.

Mirrors PROOF.md:

```
w = min { n ∈ I : τ(n) = min_{m ∈ I} τ(m) }
```

with `I = {p+1, …, q-1}`.
-/
def IsLeftmostMinTau (p q w : ℕ) : Prop :=
  InGapInterior p q w ∧
  (∀ n, p < n → n < q → tau w ≤ tau n) ∧
  (∀ n, p < n → n < w → tau w < tau n)

/-- Every interior integer is composite (`τ ≥ 3`). Holds under next-prime hypotheses. -/
def InteriorComposite (p q : ℕ) : Prop :=
  ∀ n, p < n → n < q → 3 ≤ tau n

/--
Earlier-integer side of the maximizer proof (PROOF.md §Earlier Integers).

For every earlier interior `k < w`, `F(k) < F(w)`. In prose this is closed by
the prime-square case, Witness Threshold, Short Divisor-Average, and the
finite premise `gwr_finite_base_v1`. This hypothesis packages that side so the
maximizer theorem is a pure combination of Ordered Comparison (later side)
plus the named earlier side — no silent finite-base smuggling.
-/
def EarlierSideClosed (p q w : ℕ) : Prop :=
  ∀ k (hpk : p < k) (hkw : k < w),
    F k (Nat.zero_lt_of_lt hpk) <
      F w (Nat.zero_lt_of_lt (lt_trans hpk hkw))

/-! ## Ordered Comparison Lemma (PROOF.md)

For composite `a < b` with `τ(a) ≤ τ(b)`, `F(a) > F(b)`.
-/

/--
**Ordered Comparison Lemma** (PROOF.md).

For composite integers `a < b` (`τ ≥ 3`) with `τ(a) ≤ τ(b)`, the logarithmic
comparison satisfies `F(a) > F(b)`.

Proof mechanism:
1. Coefficients `τ/2 - 1` are positive and nondecreasing in `τ`.
2. `log` is strictly increasing on positives, so `log a < log b`.
3. Products of positive factors preserve the strict inequality on the log side.
4. Negating reverses the inequality for `F = -E`.
-/
theorem ordered_comparison
    {a b : ℕ} (ha1 : 1 < a) (hb1 : 1 < b) (hab : a < b)
    (hta : 3 ≤ tau a) (htb : 3 ≤ tau b) (hle : tau a ≤ tau b) :
    F a (Nat.zero_lt_of_lt ha1) > F b (Nat.zero_lt_of_lt hb1) := by
  have ha0 : (0 : ℝ) < a := by exact_mod_cast Nat.zero_lt_of_lt ha1
  have hb0 : (0 : ℝ) < b := by exact_mod_cast Nat.zero_lt_of_lt hb1
  have hlog_lt : log (a : ℝ) < log (b : ℝ) := log_lt_log ha0 (by exact_mod_cast hab)
  have hlog_a_pos : 0 < log (a : ℝ) := log_pos (by exact_mod_cast ha1)
  have hca : 0 < excessCoeff (tau a) := excessCoeff_pos_of_tau_ge_three hta
  have hcb : 0 < excessCoeff (tau b) := excessCoeff_pos_of_tau_ge_three htb
  have hcoeff_le : excessCoeff (tau a) ≤ excessCoeff (tau b) := by
    rw [excessCoeff_eq, excessCoeff_eq]
    have : (tau a : ℝ) ≤ tau b := by exact_mod_cast hle
    linarith
  -- E a = ca * log a ≤ cb * log a < cb * log b = E b
  have hEa_le : excessCoeff (tau a) * log (a : ℝ) ≤
      excessCoeff (tau b) * log (a : ℝ) :=
    mul_le_mul_of_nonneg_right hcoeff_le (le_of_lt hlog_a_pos)
  have hEa_lt_mid : excessCoeff (tau b) * log (a : ℝ) <
      excessCoeff (tau b) * log (b : ℝ) :=
    mul_lt_mul_of_pos_left hlog_lt hcb
  have hE : E a (Nat.zero_lt_of_lt ha1) < E b (Nat.zero_lt_of_lt hb1) := by
    simp only [E_eq_coeff_mul_log]
    exact lt_of_le_of_lt hEa_le hEa_lt_mid
  -- F = -E reverses the inequality
  simp only [F_eq_neg_E]
  exact neg_lt_neg_iff.mpr hE

/-! ## Later Integers (PROOF.md)

Every integer after the leftmost min-`τ` witness has weakly larger `τ`, so
Ordered Comparison forces strictly smaller `F`.
-/

/--
**Later Integers.** If `w` is a leftmost min-`τ` interior point and `n` is a
strictly later interior point, then `F(n) < F(w)`.
-/
theorem later_integers_smaller_F
    {p q w n : ℕ}
    (hw : IsLeftmostMinTau p q w)
    (hn : InGapInterior p q n)
    (hnw : w < n)
    (hcomp : InteriorComposite p q) :
    F n (Nat.zero_lt_of_lt hn.1) < F w (Nat.zero_lt_of_lt hw.1.1) := by
  have hwI := hw.1
  have hmin := hw.2.1
  have htau_le : tau w ≤ tau n := hmin n hn.1 hn.2
  have hta : 3 ≤ tau w := hcomp w hwI.1 hwI.2
  have htb : 3 ≤ tau n := hcomp n hn.1 hn.2
  have ha1 : 1 < w := one_lt_of_tau_ge_three hta
  have hb1 : 1 < n := one_lt_of_tau_ge_three htb
  exact ordered_comparison ha1 hb1 hnw hta htb htau_le

/-! ## Prime-square earlier case (PROOF.md §Prime-Square Case)

When `τ(w) = 3` (prime-square witness), every earlier interior integer has
`τ ≥ 4`, and `k > √w` forces `F(k) < F(w)`.
-/

/--
Under consecutive-prime gap hypotheses with `τ(w) = 3`, every earlier interior
point has `τ ≥ 4` (no earlier prime square can share the min count).
-/
theorem earlier_tau_ge_four_of_min_three
    {p q w k : ℕ}
    (hw : IsLeftmostMinTau p q w)
    (hk : p < k) (hkw : k < w)
    (hw3 : tau w = 3) :
    4 ≤ tau k := by
  have hstrict := hw.2.2 k hk hkw
  -- tau w < tau k and tau w = 3 ⇒ 4 ≤ tau k
  omega

/--
**Prime-square earlier comparison.** If `τ(w) = 3` and earlier `k` satisfies
`k * k > w` (which holds when `k > √w`, true for gap interiors with `r ≤ p < k`),
and `τ(k) ≥ 4`, then `F(k) < F(w)`.

This formalizes the log comparison
`F(k) ≤ -log k` and `F(w) = -(1/2) log w` with `log k > (1/2) log w`.
-/
theorem prime_square_earlier_smaller_F
    {w k : ℕ}
    (hw1 : 1 < w) (hk1 : 1 < k)
    (hw3 : tau w = 3) (hk4 : 4 ≤ tau k)
    (hsq : w < k * k) :
    F k (Nat.zero_lt_of_lt hk1) < F w (Nat.zero_lt_of_lt hw1) := by
  have hw0 : (0 : ℝ) < w := by exact_mod_cast Nat.zero_lt_of_lt hw1
  have hk0 : (0 : ℝ) < k := by exact_mod_cast Nat.zero_lt_of_lt hk1
  have hlog_w : 0 < log (w : ℝ) := log_pos (by exact_mod_cast hw1)
  have hlog_k : 0 < log (k : ℝ) := log_pos (by exact_mod_cast hk1)
  -- coeff(w) = 3/2 - 1 = 1/2
  have hcw : excessCoeff (tau w) = (1 : ℝ) / 2 := by
    rw [hw3, excessCoeff_eq]
    norm_num
  -- coeff(k) ≥ 4/2 - 1 = 1
  have hck_ge : (1 : ℝ) ≤ excessCoeff (tau k) := by
    rw [excessCoeff_eq]
    have : (4 : ℝ) ≤ tau k := by exact_mod_cast hk4
    linarith
  -- log k > (1/2) log w  from  k^2 > w  ⇒  2 log k > log w
  have hkk : (w : ℝ) < (k : ℝ) * k := by exact_mod_cast hsq
  have hlog_kk : log (w : ℝ) < log ((k : ℝ) * k) := log_lt_log hw0 hkk
  have hlog_mul : log ((k : ℝ) * k) = log (k : ℝ) + log (k : ℝ) := by
    rw [log_mul (ne_of_gt hk0) (ne_of_gt hk0)]
  have h2log : log (w : ℝ) < 2 * log (k : ℝ) := by
    have : log (w : ℝ) < log (k : ℝ) + log (k : ℝ) := by
      rwa [hlog_mul] at hlog_kk
    rwa [← two_mul] at this
  have hhalf : (1 / 2 : ℝ) * log (w : ℝ) < log (k : ℝ) := by
    have h2pos : (0 : ℝ) < (2 : ℝ) := by norm_num
    calc
      (1 / 2 : ℝ) * log (w : ℝ) = log (w : ℝ) / 2 := by ring
      _ < (2 * log (k : ℝ)) / 2 :=
        (div_lt_div_iff_of_pos_right h2pos).mpr h2log
      _ = log (k : ℝ) := by ring
  -- E w = (1/2) log w
  have hEw : E w (Nat.zero_lt_of_lt hw1) = (1 / 2 : ℝ) * log (w : ℝ) := by
    simp only [E_eq_coeff_mul_log, hcw]
  -- E k ≥ 1 * log k = log k
  have hEk_ge : log (k : ℝ) ≤ E k (Nat.zero_lt_of_lt hk1) := by
    simp only [E_eq_coeff_mul_log]
    calc
      log (k : ℝ) = (1 : ℝ) * log (k : ℝ) := by ring
      _ ≤ excessCoeff (tau k) * log (k : ℝ) :=
        mul_le_mul_of_nonneg_right hck_ge (le_of_lt hlog_k)
  -- E w < log k ≤ E k  ⇒  E w < E k  ⇒  F k < F w
  have hE : E w (Nat.zero_lt_of_lt hw1) < E k (Nat.zero_lt_of_lt hk1) := by
    rw [hEw]
    exact lt_of_lt_of_le hhalf hEk_ge
  simp only [F_eq_neg_E]
  exact neg_lt_neg_iff.mpr hE

/-! ## Interior Maximizer Theorem (PROOF.md)

The leftmost min-`τ` interior integer uniquely maximizes `F` on the gap
interior once the earlier-integer side is closed.
-/

/--
**Interior Maximizer (later + self).**

On `{w} ∪ {n ∈ I : n > w}`, the leftmost min-`τ` point uniquely maximizes `F`.
This side is closed solely by Ordered Comparison — no finite base required.
-/
theorem leftmost_min_tau_maximizes_on_right
    {p q w : ℕ}
    (hw : IsLeftmostMinTau p q w)
    (hcomp : InteriorComposite p q)
    {n : ℕ} (hpn : p < n) (hnq : n < q) (hwn : w < n) :
    F n (Nat.zero_lt_of_lt hpn) < F w (Nat.zero_lt_of_lt hw.1.1) :=
  later_integers_smaller_F hw ⟨hpn, hnq⟩ hwn hcomp

/--
**Interior Maximizer Theorem** (PROOF.md mirror).

Let `w` be the leftmost interior min-`τ` integer in a consecutive-prime gap
with composite interior. Assume the earlier-integer side is closed
(`EarlierSideClosed`, packaging PROOF.md §Earlier Integers + finite base).
Then `w` is the unique maximizer of `F` on the gap interior:

for every other interior `n ≠ w`, `F(n) < F(w)`.
-/
theorem leftmost_min_tau_maximizer
    {p q w : ℕ}
    (hw : IsLeftmostMinTau p q w)
    (hcomp : InteriorComposite p q)
    (hearlier : EarlierSideClosed p q w)
    {n : ℕ} (hpn : p < n) (hnq : n < q) (hne : n ≠ w) :
    F n (Nat.zero_lt_of_lt hpn) < F w (Nat.zero_lt_of_lt hw.1.1) := by
  rcases lt_trichotomy n w with hlt | heq | hgt
  · exact hearlier n hpn hlt
  · exact (hne heq).elim
  · exact later_integers_smaller_F hw ⟨hpn, hnq⟩ hgt hcomp

/--
**Interior maximizer under prime-square earlier discharge.**

When `τ(w) = 3` and every earlier interior `k` satisfies `w < k * k`
(the PROOF.md square-case geometric relation `k > √w`), the earlier side is
discharged analytically and the maximizer theorem holds with no extra hypothesis.
-/
theorem leftmost_min_tau_maximizer_prime_square
    {p q w : ℕ}
    (hw : IsLeftmostMinTau p q w)
    (hcomp : InteriorComposite p q)
    (hw3 : tau w = 3)
    (hsq : ∀ k, p < k → k < w → w < k * k)
    {n : ℕ} (hpn : p < n) (hnq : n < q) (hne : n ≠ w) :
    F n (Nat.zero_lt_of_lt hpn) < F w (Nat.zero_lt_of_lt hw.1.1) := by
  refine leftmost_min_tau_maximizer hw hcomp ?_ hpn hnq hne
  intro k hpk hkw
  have hk4 : 4 ≤ tau k := earlier_tau_ge_four_of_min_three hw hpk hkw hw3
  have hw1 : 1 < w := one_lt_of_tau_ge_three (by omega : 3 ≤ tau w)
  have hk1 : 1 < k := one_lt_of_tau_ge_three (Nat.le_trans (by decide : 3 ≤ 4) hk4)
  exact prime_square_earlier_smaller_F hw1 hk1 hw3 hk4 (hsq k hpk hkw)

/--
Composite interior follows from next-prime / tau-scan hypotheses:
every interior integer has `τ ≠ 2`, and for `n > 1` that forces `τ ≥ 3`.
-/
theorem interior_composite_of_tau_ne_two
    {p q : ℕ}
    (hp1 : 1 < p)
    (hnext : ∀ n, p < n → n < q → tau n ≠ 2) :
    InteriorComposite p q := by
  intro n hpn hnq
  have hne : tau n ≠ 2 := hnext n hpn hnq
  have hn1 : 1 < n := lt_trans hp1 hpn
  have hge : 2 ≤ tau n := tau_ge_two_of_gt_one n hn1
  omega

end PGS.GWR
