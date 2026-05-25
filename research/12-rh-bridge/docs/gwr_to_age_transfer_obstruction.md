# GWR-To-Age Transfer Obstruction

Date: 2026-05-24

Status: local-to-global transfer note for the Age-Divisor Energy Bound.

The Age-Divisor Energy Bound would close the reciprocal gap-energy route if
one could prove

$$
\sum_{X<n\le2X}(n-p(n))(\tau(n)-2)
\le
C X(\log X)^B.
$$

The natural question is whether the GWR selector theorem can transfer local
chamber order into this dyadic age-energy bound.

The answer at the current proof level is no. The obstruction is an orientation
mismatch: GWR controls a chamber minimum, while the age-divisor energy theorem
needs an upper bound on an accumulated whole-chamber positive quantity.

## Chamber Energy

For a chamber `(p,q]`, define

$$
\mathcal A(p,q)
=
\sum_{n=p+1}^{q-1}
(n-p)(\tau(n)-2).
$$

Since every interior integer is composite,

$$
\tau(n)-2\ge1,
$$

so

$$
\mathcal A(p,q)
\ge
\sum_{j=1}^{g(q)-1}j
=
\frac{g(q)(g(q)-1)}2.
$$

Thus chamber age-divisor energy is already a lower bound for gap-square
energy.

The dyadic theorem needs an upper bound after summing chambers:

$$
\sum_{X<q\le2X}\mathcal A(p(q),q)
\le
C X(\log X)^B.
$$

## What GWR Supplies

Let `w` be the GWR selector in the chamber and let

$$
d=\tau(w).
$$

GWR supplies:

```text
w is the leftmost interior point with minimum divisor count.
```

Therefore:

$$
n>w\Rightarrow \tau(n)\ge d,
$$

and

$$
n<w\Rightarrow \tau(n)>d.
$$

This is a lower-ordering statement for divisor counts relative to the selected
minimum.

## Why This Does Not Bound Age Energy

The chamber energy contains positive terms:

$$
(n-p)(\tau(n)-2).
$$

To prove an upper bound on `A(p,q)`, one would need upper control on either
the age factor `n-p`, the divisor surplus `tau(n)-2`, or their aggregate.

GWR gives none of these upper controls.

It identifies the minimum divisor-count point. It does not bound the chamber
width `q-p`. It also does not bound large divisor-count values elsewhere in
the chamber. In fact, the inequalities supplied by GWR point in the opposite
direction:

```text
before w: divisor counts are strictly larger than d
after w: divisor counts are at least d
```

Those facts can increase the age-divisor energy lower bound. They do not cap
it.

## Candidate Transfer Form And Missing Input

A successful GWR-to-age transfer would need a theorem of the form:

$$
\mathcal A(p,q)
\le
\Psi(p,q,w,d),
$$

with a dyadic summation bound

$$
\sum_{X<q\le2X}\Psi(p,q,w,d)
\le
C X(\log X)^B.
$$

Current GWR machinery provides no such `Psi`.

The divisor-average branch in `PROOF.md` gives restricted position control for
earlier integers in one proof branch. It does not bound the full chamber
energy, and it does not sum over all chambers in a dyadic endpoint block.

## Deepest Transfer Obstacle

The local theorem answers:

```text
which interior point minimizes divisor-count load?
```

The energy theorem asks:

```text
how large is the accumulated age-weighted divisor surplus over all chambers?
```

These are not the same invariant. A chamber can have a perfectly valid GWR
selector while carrying large age-divisor energy because the chamber is long.

Therefore the current GWR theorem cannot be the sole source of the
Persistence-Energy Inequality.

## Result

The GWR-to-age route requires a new chamber energy invariant:

> **Chamber Age-Energy Upper Invariant.**
> A computable chamber quantity `Psi(p,q,w,d)` bounds the full age-divisor
> energy from above and has dyadic total `O(X(log X)^B)`.

No such invariant is currently present in the PGS framework.
