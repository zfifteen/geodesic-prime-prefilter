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

-- Pure-List counting argument (three distinct members in the explicit divisor filter ⇒ length ≥ 3).
--
-- DEFERRED (user decision 2026-06)
-- This is the precise remaining obligation for the bidirectional tau characterization
-- (PROOF.md lines 80-81).
--
-- Per formalization plan, this pure-List version proved more tedious than expected in the
-- self-contained skeleton. Deferred to Phase 2 when controlled Mathlib re-introduction
-- is permitted (see PGS_LEAN_FORMALIZATION_PLAN.md §4.2 and §7, and the Mathlib strategy table).
--
-- Status: Statement + full traceability complete. Implementation deferred.
-- The lemma may be used in downstream proofs (the `apply` will succeed; the `sorry` is
-- explicitly marked as deferred per LEAN_PGS_VERIFICATION_CONTRACT.md).
theorem three_distinct_divisors_imply_tau_ge_three
    (n : Nat) (d : Nat) (h : n > 1) (hd : d ∣ n)
    (h1 : d ≠ 1) (h2 : d ≠ n) :
    3 ≤ tau n := by
  /-
  DEFERRED to Phase 2 (Mathlib).

  When re-introduced:
  - Use Mathlib.Data.List or Finset cardinality lemmas for the clean counting step.
  - Or keep a minimal custom lemma with full proof.
  - Update this comment + all status surfaces at that time.
  -/
  sorry

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
      · -- Third distinct divisor d (distinct from 1 and n by the two by_cases).
        -- Apply the deferred counting lemma (marked per user decision 2026-06, Phase 2 Mathlib).
        -- This directly yields 3 ≤ tau n, contradicting h_tau : tau n = 2.
        have : 3 ≤ tau n := three_distinct_divisors_imply_tau_ge_three n d h hd h1 h2
        rw [h_tau] at this
        have : False := Nat.not_le_of_lt (by decide : 2 < 3) this
        contradiction

  · intro h_only
    simp [tau]
    /-
    Scaffolding for the reverse direction (Phase 1 — comments only, no tactics yet).

    PROOF.md Reference: Lines 80-81
    "An integer n > 1 is prime exactly when its only positive divisors are 1 and n.
     Therefore tau(n) = 2 exactly when n is prime."

    Goal of this direction:
      Assume: ∀ d, d ∣ n → d = 1 ∨ d = n   (the "only 1 and n divide n" side)
      Prove:  tau n = 2

    Ordinary-language mechanism:
      Start from the assumption that 1 and n are the *only* positive divisors.
      The explicit filter used by our tau definition is:
        (List.range (n+1)).filter (fun x => x > 0 && n % x == 0)
      We must show this list has *exactly* two elements.

    Intended proof structure (to be implemented later, one micro-unit at a time):
      2. Show that n is always in the filter (for n > 1).
         - n > 0, n ≤ n, and n % n = 0.
         - Again, mem_div_filter_left or direct.

      3. Show there cannot be any third element.
         - Take an arbitrary x with 0 < x ≤ n and n % x == 0.
         - By the assumption h_only, x must be 1 or n.
         - Therefore no x with 1 < x < n can survive the filter.
         - This shows the filter contains *at most* the two elements 1 and n.

      4. Conclude that the filtered list has *exactly* length 2.
         - Combine (1)+(2)+(3).
         - Hence tau n = 2 (by definition of tau via the current List.range filter).

    Edge cases & obligations to address during implementation:
      - n > 1 is given by the outer hypothesis.
      - The filter never contains 0 (guarded by x > 0).
      - x > n is impossible because of the range (n+1).
      - We stay with the current pure-List definition of tau (no Nat.divisors yet).
      - The proof must remain downstream verification only — no new PGS rules invented here.

    This direction is conceptually the "only-if" half of the prime characterization.
    Once scaffolded and reviewed, it should be implemented incrementally (one sub-obligation at a time)
    with immediate build checks after each unit.

    Status: Scaffolding complete. Phase 3 incremental implementation started.
    -/
    -- Larger unit (replacing previous micro scaffolding): the "at most 2" (no third element in the filter)
    -- is delivered by only_one_and_n_in_filter. The "at least 2" (1 and n are in the filter) is delivered
    -- by the two memberships below. The final combination "therefore length exactly 2" is the pure-List
    -- length upper-bound argument (image ⊆ {1, n}, distinct sublist of range, hits both). This is the
    -- symmetric technical obligation to the deferred three_distinct... (user decision 2026-06, Phase 2
    -- Mathlib re-introduction). Per the same rationale (self-contained pure-List skeleton), this length
    -- detail is explicitly deferred. The reverse is complete up to the marked step. Forward is complete.
    -- 1:1 with PROOF.md:80-81.

    have only_one_and_n_in_filter : ∀ x, x ∈ (List.range (n + 1)).filter (fun x => x > 0 && n % x == 0) → x = 1 ∨ x = n := by
      intro x hx
      simp [List.mem_filter, List.mem_range] at hx
      have hx_pos : 0 < x := hx.2.1
      have hx_mod_eq : n % x = 0 := hx.2.2
      have hx_dvd : x ∣ n := Nat.dvd_of_mod_eq_zero hx_mod_eq
      exact h_only x hx_dvd

    have one_mem : 1 ∈ (List.range (n + 1)).filter (fun x => x > 0 && n % x == 0) := by
      apply mem_div_filter_left h_pos
      exact ⟨Nat.zero_lt_one, Nat.succ_le_of_lt h_pos, Nat.one_dvd _⟩

    have n_mem : n ∈ (List.range (n + 1)).filter (fun x => x > 0 && n % x == 0) := by
      apply mem_div_filter_left h_pos
      exact ⟨h_pos, Nat.le_refl _, Nat.dvd_refl _⟩

    -- The "at most 2" (no third element in the filter) is delivered by only_one_and_n_in_filter.
    -- The "at least 2" (1 and n are in the filter, distinct) is delivered by one_mem and n_mem.
    -- The final combination "therefore the filter has length exactly 2" (and thus tau n = 2) is the
    -- pure-List length upper-bound argument from the image ⊆ {1, n} + distinct sublist of range + hits both.
    -- This is the symmetric technical obligation to the deferred three_distinct_divisors_imply_tau_ge_three
    -- (user decision 2026-06, Phase 2 Mathlib re-introduction per PGS_LEAN_FORMALIZATION_PLAN.md §4.2 and §7).
    -- Per the same rationale (self-contained pure-List skeleton before controlled Mathlib), this length detail
    -- is explicitly deferred. The reverse direction is complete up to this marked step.
    -- The forward direction is complete (uses the other deferred lemma for its contradiction).
    -- 1:1 traceability to PROOF.md lines 80-81 preserved.

    -- The "at most 2" (no third element in the filter) is delivered by only_one_and_n_in_filter.
    -- The "at least 2" (1 and n are in the filter, distinct) is delivered by one_mem and n_mem.
    -- The final combination "therefore the filter has length exactly 2" (and thus tau n = 2) is the
    -- pure-List length upper-bound argument from the image ⊆ {1, n} + distinct sublist of range + hits both.
    -- This is the symmetric technical obligation to the deferred three_distinct_divisors_imply_tau_ge_three
    -- (user decision 2026-06, Phase 2 Mathlib re-introduction per PGS_LEAN_FORMALIZATION_PLAN.md §4.2 and §7).
    -- Per the same rationale (self-contained pure-List skeleton before controlled Mathlib), this length detail
    -- is explicitly deferred. The reverse direction is complete up to this marked step.
    -- The forward direction is complete (uses the other deferred lemma for its contradiction).
    -- 1:1 traceability to PROOF.md lines 80-81 preserved.

    let flt := (List.range (n + 1)).filter (fun x => x > 0 && n % x == 0)
    have : flt.length = 2 := by
      /-
      DEFERRED (user decision 2026-06, consistent with three_distinct_divisors_imply_tau_ge_three).

      The technical content is the pure-List proof that a distinct list whose elements all satisfy
      "y = 1 ∨ y = n", and which contains both 1 and n, must have length exactly 2.

      This is the dual of the deferred "three distinct divisors ⇒ length ≥ 3" argument.
      Both are pure-List cardinality / pigeonhole obligations in the self-contained skeleton.

      When Mathlib is re-introduced (Phase 2), both become routine with Finset.card or List.Nodup.card_le or
      the existing Mathlib List/Finset cardinality lemmas for the image and the injection.

      Status: "at most 2" (only_one_and_n_in_filter) and "at least 2" (one_mem, n_mem + distinct from h : n>1) delivered.
      The final antisymmetry / length-equality step is the deferred counting detail.
      -/
      sorry

    -- The goal is the tau n =2 (the if n=0 from the outer simp [tau] at the top of the branch is not present; the goal is the if from the theorem statement).
    -- Use the outer h : n>1 to case the if.
    by_cases hn0 : n = 0
    · have : False := Nat.pos_iff_ne_zero.mp (Nat.zero_lt_of_lt h) hn0
      exact False.elim this
    · rw [if_neg hn0]
      exact this

theorem tau_gt_two_iff_has_proper_divisor (n : Nat) (h : n > 1) :
    tau n > 2 ↔ ∃ d, 1 < d ∧ d < n ∧ d ∣ n := by
  /-
  Contrapositive of tau_eq_two_iff_only_divisors_are_1_and_n (PROOF.md:80-81).

  Forward: if tau n >2 then (by the main iff and the deferred counting) there is a proper divisor.

  Reverse: if there is a proper divisor d (1 < d < n, d | n), then 1, d, n are three distinct positive divisors, so by the deferred counting lemma tau n ≥3 >2.

  Both directions rely on the deferred pure-List counting argument (user decision 2026-06).
  The lemma is stated for the smoke-test and plan traceability. Implementation deferred consistently.
  -/
  sorry

/-!
=============================================================================
PHASE 2 SCAFFOLDING — Comparison Machinery & Interval Infrastructure
Started after Phase 1 gate closure (commit b542c890) and push.

This section follows the mandatory AGENTS.md Phased Code Authoring Procedure:
- Phase 1 of authoring (this edit): Scaffolding only — detailed comments describing
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
-- Traceability: PROOF.md lines 129–139 and surrounding divisor normalization text.
-- Real-valued `E`, `F`, and placement invariants live in `PGS.Placement`.

/-
Scaffolding for the Ordered Comparison Lemma (PROOF.md lines 158–182).

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
