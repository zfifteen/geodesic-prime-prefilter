import PGS.Basic
open PGS
theorem test_omega : ∀ n, 3 < n → n < 5 → n = 4 := by
  intro n hn1 hn2
  omega
