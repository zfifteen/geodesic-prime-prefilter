# Reciprocal Gap-Energy Bound Obstruction

Date: 2026-05-24

Status: bound/obstruction note for the Reciprocal Endpoint Occupancy Theorem.

The Reciprocal Endpoint Occupancy Theorem follows if the reciprocal gap-energy
sum converges:

$$
\mathcal E
=
\sum_q\frac{g(q)^2\log q}{q^2}
<\infty,
$$

where

$$
g(q)=q-p(q).
$$

This note states sufficient forms of the required bound and records why the
current local GWR machinery does not prove them.

## Dyadic Sufficient Condition

It is enough to prove a dyadic second-moment bound of the form

$$
\boxed{
\sum_{X<q\le2X}g(q)^2
\le
C X(\log X)^B
}
$$

for fixed constants `C` and `B`.

Indeed, on a dyadic block,

$$
\sum_{X<q\le2X}
\frac{g(q)^2\log q}{q^2}
\le
\frac{\log(2X)}{X^2}
\sum_{X<q\le2X}g(q)^2
\le
\frac{C(\log X)^{B+1}}{X}.
$$

Summing over dyadic `X = 2^k` gives a convergent series.

Thus the reciprocal gap-energy condition does not require a pointwise small
gap theorem. It requires a weighted global second-moment theorem for prime-gap
widths.

## Pointwise Sufficient Conditions

Any eventual pointwise bound

$$
g(q)\le C(\log q)^A
$$

implies the dyadic second-moment bound and hence reciprocal gap-energy
convergence.

More generally, any pointwise bound

$$
g(q)\le Cq^{1/2-\varepsilon}
$$

with `epsilon > 0` also suffices.

These are sufficient conditions only. The desired PGS theorem should be stated
as a reciprocal energy or dyadic second-moment law, since that is exactly what
the endpoint occupancy proof needs.

## Current PGS Inputs

The local machinery supplies:

```text
exact prime endpoint chain,
exact chamber interiors,
GWR selected integer,
local divisor-count order,
finite-base and branch-local records.
```

These inputs do not currently bound

$$
\sum_{X<q\le2X}g(q)^2.
$$

The GWR theorem identifies the leftmost minimum-excess point inside a chamber.
It does not force the next zero-excess return to occur within a dyadic
second-moment budget.

The finite bounded-compression and residual records give finite or
branch-local offset control. They are not all-scale gap-width second-moment
theorems.

## Principal Obstruction

A long prime gap can still have a valid GWR-selected interior minimum near the
left endpoint, near the middle, or near the right endpoint. The selector
location alone does not determine the chamber width.

Therefore current local GWR data does not rule out a hypothetical endpoint
chain with excessive reciprocal gap energy. To prove the required convergence,
one needs an additional global theorem about the endpoint chain itself.

## Required New Statement

The missing theorem can be stated PGS-natively:

> **Reciprocal Gap-Energy Theorem.**
> The consecutive-prime endpoint chain satisfies
> $$
> \sum_q\frac{(q-p(q))^2\log q}{q^2}<\infty.
> $$

or, equivalently for the occupancy proof, the dyadic form

$$
\sum_{X<q\le2X}(q-p(q))^2
\le
C X(\log X)^B.
$$

This theorem is not present in the current local chamber machinery.

## Finite Surface

The exact finite surfaces are consistent with convergence:

| X | reciprocal gap-energy partial |
|---:|---:|
| `10,000` | `2.2020055` |
| `100,000` | `2.2161020` |
| `1,000,000` | `2.2183175` |

This is measured support only. It does not replace the required global
endpoint-chain energy theorem.

## Result

The endpoint occupancy route has now isolated a new global endpoint-chain
obligation:

```text
prove reciprocal gap-energy convergence, or prove endpoint sampling-error
convergence directly.
```

The existing GWR theorem remains necessary for local chamber order, but it is
not sufficient for this global gap-energy estimate.
