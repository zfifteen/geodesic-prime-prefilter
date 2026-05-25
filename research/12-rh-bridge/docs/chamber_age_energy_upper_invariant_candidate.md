# Chamber Age-Energy Upper Invariant Candidate

Date: 2026-05-24

Status: candidate invariant contract for the Age-Divisor Energy Bound.

The GWR-to-age transfer obstruction shows that local selector information does
not by itself upper-bound full chamber persistence energy. The missing object
is a computable chamber invariant `Psi(p,q)` satisfying two conditions:

$$
\mathcal A(p,q)\le\Psi(p,q),
$$

and

$$
\sum_{X<q\le2X}\Psi(p(q),q)
\le
C X(\log X)^B.
$$

Here

$$
\mathcal A(p,q)
=
\sum_{n=p+1}^{q-1}(n-p)(\tau(n)-2)
$$

is the age-divisor energy of the chamber.

## Candidate 1: Divisor-Channel Age Budget

Every divisor of `n` appears in a divisor channel. Since divisors come in
pairs, the divisor surplus is controlled by proper divisor channels up to
`sqrt(n)`.

Define

$$
\Psi_{\mathrm{div}}(p,q)
=
2
\sum_{d\le\sqrt q}
\sum_{\substack{p<n<q\\ d\mid n\\ d>1}}
(n-p).
$$

This is computable from chamber geometry and divisor channels.

For each interior composite `n`, the proper divisor channels counted up to
`sqrt(n)` dominate `tau(n)-2` up to an absolute factor, so

$$
\mathcal A(p,q)
\le
\Psi_{\mathrm{div}}(p,q).
$$

Thus `Psi_div` is a genuine upper invariant candidate.

### Needed Summation Property

To close the age-energy theorem, one must prove

$$
\sum_{X<q\le2X}\Psi_{\mathrm{div}}(p(q),q)
\le
C X(\log X)^B.
$$

Equivalently, divisor-channel multiples must not carry large zero-excess age
too often:

$$
\sum_{d\le\sqrt{2X}}
\sum_{\substack{X<n\le2X\\ d\mid n}}
a(n)
\le
C X(\log X)^B.
$$

This is a global divisor-channel age orthogonality theorem.

## Candidate 2: GWR-Weighted Chamber Budget

A GWR-shaped invariant would use the selected minimum

$$
w=w(p,q),
\qquad
d=\tau(w),
$$

and define an upper budget in terms of `(g,d,w-p,q-w)`.

The required form would be

$$
\mathcal A(p,q)
\le
\Psi_{\mathrm{gwr}}(g,d,w-p,q-w),
$$

with

$$
\sum_{X<q\le2X}
\Psi_{\mathrm{gwr}}(g(q),d(q),w(q)-p(q),q-w(q))
\le
C X(\log X)^B.
$$

Current GWR data does not supply such a bound. It gives the minimum divisor
count and selector position, but the chamber energy depends on every interior
divisor surplus. A `Psi_gwr` would need a new theorem saying the selected
minimum controls the total age-weighted divisor surplus.

## Candidate 3: Endpoint Geometry Budget

An endpoint-only invariant would attempt to bound chamber energy by a function
of gap width and endpoint scale:

$$
\mathcal A(p,q)\le\Psi_{\mathrm{end}}(g(q),q).
$$

Trivial choices exist, such as using a large divisor-count upper bound, but
they do not have a known dyadic total. To be useful, `Psi_end` must satisfy

$$
\sum_{X<q\le2X}\Psi_{\mathrm{end}}(g(q),q)
\le
C X(\log X)^B.
$$

This again requires a global gap-width or divisor-average theorem beyond the
current local machinery.

## Best Current Candidate

The divisor-channel age budget is the most concrete candidate because it
directly expands the divisor-count source:

```text
age-divisor energy
-> divisor-channel age budget
-> dyadic channel-age orthogonality.
```

It preserves the PGS source object, uses exact divisor channels, and gives an
actual chamberwise upper bound.

Its missing theorem is global:

> **Divisor-Channel Age Orthogonality.**
> The total zero-excess age carried by proper divisor channels in a dyadic
> block is `O(X(log X)^B)`.

## Result

A Chamber Age-Energy Upper Invariant can be stated concretely:

$$
\Psi_{\mathrm{div}}(p,q)
=
2
\sum_{d\le\sqrt q}
\sum_{\substack{p<n<q\\ d\mid n\\ d>1}}
(n-p).
$$

It bounds full chamber age-divisor energy from above. The remaining proof
obligation is the dyadic summation theorem for this invariant.
