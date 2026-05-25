# Persistence-Energy Inequality Strategy

Date: 2026-05-24

Status: candidate direct second-moment route for reciprocal gap energy.

The reciprocal gap-energy theorem follows from a dyadic second-moment bound:

$$
\sum_{X<q\le2X}g(q)^2
\le
C X(\log X)^B.
$$

A direct PGS-native route is to express gap squares as accumulated
positive-excess age.

## Age Since Last Zero-Excess Return

For an integer `n > 1`, let

$$
p(n)=\max\{p\le n:p\text{ is prime}\},
$$

and define the zero-excess age

$$
a(n)=n-p(n).
$$

At a prime endpoint, `a(n)=0`. Inside a chamber `(p,q)`, the age is

$$
a(p+j)=j
\qquad
1\le j<g(q).
$$

Thus the interior of a chamber of width `g` contributes

$$
\sum_{j=1}^{g-1}j
=
\frac{g(g-1)}2
$$

to the accumulated age before the right endpoint resets the age to zero.

Therefore a dyadic gap-square bound follows from an age-energy bound, up to
absolute constants and boundary chambers:

$$
\boxed{
\sum_{X<n\le2X}a(n)
\le
C X(\log X)^B.
}
$$

Boundary chambers contribute only endpoint errors of the same type as the
largest gap crossing the dyadic boundary.

## Persistence-Energy Inequality

The direct theorem shape is:

> **Persistence-Energy Inequality.**
> The zero-excess age in every dyadic block satisfies
> $$
> \sum_{X<n\le2X}a(n)
> \le
> C X(\log X)^B.
> $$

This inequality is equivalent to saying that positive-excess excursions have
controlled total persistence.

## Divisor-Field Strengthening

Since every interior point has

$$
E(n)\ge\frac12\log n,
$$

an age-weighted excess bound would imply the age-energy bound:

$$
\sum_{X<n\le2X}a(n)E(n)
\le
C X(\log X)^{B+1}.
$$

Indeed, on `[X,2X]`,

$$
E(n)\ge\frac12\log X
$$

for every composite interior point, so

$$
\sum_{X<n\le2X}a(n)
\le
\frac{2}{\log X}
\sum_{X<n\le2X}a(n)E(n).
$$

Thus a PGS-native divisor-field route can target the stronger inequality:

> **Age-Weighted Excess Energy Bound.**
> $$
> \sum_{X<n\le2X}a(n)E(n)
> \le
> C X(\log X)^{B+1}.
> $$

## Candidate Mechanism

A proof would need a recurrence potential that grows during positive-excess
persistence and resets at zero-excess endpoints:

```text
positive-excess age increases
-> divisor-field cost accumulates
-> zero-excess return resets age
-> total dyadic persistence energy is bounded.
```

The local excess `E(n)` is available. The missing part is the global control
of the age-weighted sum.

## Obstacles In Current PGS Framework

Current PGS machinery proves local order, not age-energy.

The GWR selector gives the leftmost minimum-excess point in a chamber. It does
not bound the accumulated age

$$
\sum_{p<n\le q}a(n)
$$

or the age-weighted excess

$$
\sum_{p<n<q}a(n)E(n).
$$

The zero-excess coordinate identifies primes as returns to the floor, but it
does not prove a recurrence rate or persistence energy bound.

The measured grammar surfaces suggest compressed transition structure, but
they do not provide an all-scale inequality for `a(n)` or `a(n)E(n)`.

## Required New Structure

The direct second-moment route needs one new global object:

```text
a PGS recurrence potential whose dyadic total is O(X log^B X) and whose
per-run cost is quadratic in run length.
```

Without that potential, the persistence-energy inequality is not derivable
from current local divisor-count and GWR theorems.

## Result

The reciprocal gap-energy theorem can be reduced to an age-energy theorem:

$$
\sum_{X<n\le2X}a(n)\ll X(\log X)^B.
$$

This is a precise and PGS-native target. It is still a new global recurrence
theorem, not a consequence of the current local chamber-ordering machinery.
