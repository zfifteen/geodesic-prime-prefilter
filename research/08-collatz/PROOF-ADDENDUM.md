# Collatz Fork Efficiency Channel Addendum

Proof status: non-authoritative research note

## Channel Efficiency Framing

The exact 3-step first-descent algebra creates two terminal branches with the
same visible orbit shape:

```text
rise -> rise -> reset
```

Both branches begin from the same accelerated odd Collatz rule, both use the
same terminal-source notation `n = w - 1`, and both end by applying the
terminal exponent:

$$k = v_2(3w - 2)$$

The fork is therefore not a difference in orbit length or terminal notation.
It is a difference in how much descent is obtained for the arithmetic burden
needed to enter the branch.

Branch 1 has middle exponent `1` and terminal residue:

$$w \equiv 0 \pmod {18}$$

Its fixed-`k`, large-`w` reset scale is:

$$\frac{2^{k+2}}{27}$$

Branch 2 has middle exponent `2` and terminal residue:

$$w \equiv 14 \pmod {18}$$

Its fixed-`k`, large-`w` reset scale is:

$$\frac{2^{k+3}}{27}$$

Thus branch 2 has exactly twice the asymptotic reset scale of branch 1 at fixed
`k`. That is the proved Collatz reset advantage.

On the prime-gap minimizer surface, the branch split has a second effect.
Branch 1 requires `w` to be divisible by `18`, so every branch-1 witness carries
the forced divisor structure of an even multiple of `9`. Branch 2 requires
`w = 14 mod 18`, so it preserves evenness while avoiding divisibility by `3`.

A leftmost divisor-count minimizer inside a prime gap is selected for low
divisor count relative to nearby integers. The branch-2 residue class is
therefore more compatible with the minimizer condition than the branch-1
residue class. The larger reset scale and the avoided factor-of-three burden
point in the same direction.

This is the efficiency channel:

```text
branch 2 = larger reset per terminal exponent
         + lighter divisor burden under the prime-gap minimizer condition
```

The measured occupancy certificate in `PROOF.md` shows the combined effect.
In the scanned `k = 4` surface, branch 2 has half as many candidates but about
`639.4` times the hit rate. In the scanned `k = 8` surface, branch 2 again has
about half as many candidates but about `283.2` times the hit rate.

The current proof status is precise. The branch formulas, residue classes, and
reset-scale factor are proved Collatz inverse algebra. The hundreds-fold
branch-occupancy advantage is a computed certificate on the scanned prime-gap
surface. The proposed next theorem is to prove that the prime-gap
divisor-count minimizer condition amplifies the branch-2 reset advantage
because `w = 14 mod 18` avoids the heavier branch-1 divisor path `w = 0 mod
18`.
