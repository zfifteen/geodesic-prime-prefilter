import PGS.Basic
import PGS.ChamberReset
open PGS PGS.ChamberReset

def check_ce (r m M ell h d : Nat) : Bool :=
  let x_m := r^2 - 2 * m
  tau r == 2 &&
  2 * M < r &&
  1 ≤ m && m ≤ M &&
  2 * m ≤ r^2 &&
  x_m == ell * (r + h + d) &&
  ell == r - h &&
  d ≥ 1 &&
  h^2 + h < r + 2 * m

#eval (List.range 50).any fun r =>
  (List.range 50).any fun m =>
    (List.range 50).any fun M =>
      (List.range 50).any fun ell =>
        (List.range 50).any fun h =>
          (List.range 50).any fun d =>
            check_ce r m M ell h d

