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

def E (n : Nat) : Nat := 0
def F (n : Nat) : Nat := 0
def Z (n : Nat) : Nat := 0

-- Membership in the explicit divisor filter (one direction sufficient for current proof)
theorem mem_div_filter_left {n d : Nat} (hn : 0 < n)
    (h : 0 < d ∧ d ≤ n ∧ d ∣ n) :
    d ∈ (List.range (n + 1)).filter (fun x => x > 0 && n % x == 0) := by
  simp [List.mem_filter, List.mem_range]
  aesop

-- The exact counting argument the session is working to close
theorem three_distinct_divisors_imply_tau_ge_three
    (n : Nat) (d : Nat) (h : n > 1) (hd : d ∣ n)
    (h1 : d ≠ 1) (h2 : d ≠ n) :
    3 ≤ tau n := by
  -- 1, d, n are three distinct positive divisors of n.
  -- In the calling context we have shown they all belong to the filter.
  -- A list with three distinct elements has length ≥ 3.
  -- This pure-List counting step is the current focus.
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
      · -- Third distinct divisor → contradiction
        have h1_dvd : 1 ∣ n := Nat.one_dvd _
        have hn_dvd : n ∣ n := Nat.dvd_refl _

        have h1_in : 1 ∈ (List.range (n+1)).filter (fun x => x > 0 && n % x == 0) := by
          apply mem_div_filter_left h_pos
          exact ⟨Nat.zero_lt_one, Nat.succ_le_of_lt h, h1_dvd⟩

        have hd_in : d ∈ (List.range (n+1)).filter (fun x => x > 0 && n % x == 0) := by
          apply mem_div_filter_left h_pos
          have : d ≤ n := Nat.le_of_dvd h hd
          exact ⟨Nat.lt_of_le_of_ne (Nat.succ_le_of_lt h_pos) h1, this, hd⟩

        have hn_in : n ∈ (List.range (n+1)).filter (fun x => x > 0 && n % x == 0) := by
          apply mem_div_filter_left h_pos
          exact ⟨h, Nat.le_refl _, hn_dvd⟩

        -- Apply the counting lemma (the focused obligation)
        have h_ge3 : 3 ≤ tau n := by
          apply three_distinct_divisors_imply_tau_ge_three n d h hd h1 h2

        rw [← h_tau] at h_ge3
        contradiction

  · intro h_only
    simp [tau]
    -- Only 1 and n divide n → filter contains exactly 1 and n → tau = 2
    sorry

end PGS
