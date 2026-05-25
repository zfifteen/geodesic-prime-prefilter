# Nonresonant Shifted-Band Overlap Strategy

Date: 2026-05-24

Status: candidate strategy for proving summable nonresonant overlap between
projected kernel bands.

The cross-transform reduction leaves the overlap

$$
\int
w_{N,L}^{\perp}(\alpha)
\overline{
w_{N,L'}^{\perp}\!\left(\alpha+s\right)}
d\alpha,
\qquad
s={\gamma-\ell\over d}.
$$

The task is to prove this overlap is small unless `s` aligns the two bands in
a low-conductor rational way already assigned to the major projector.

## Band Geometry

A dyadic kernel band with `|K_N| asymp L` has width scale

$$
\delta_L\asymp L^{-1}.
$$

Near a rational packet center `c`, the band is modeled by an annulus

$$
E_L(c)=\{\alpha:\|\alpha-c\|\asymp \delta_L\}.
$$

After major-exclusion, the projected support is

$$
E_L^{\perp}(c)
\subseteq
E_L(c)\setminus \operatorname{Maj}(c).
$$

The overlap between two shifted bands is controlled by whether

$$
s
\approx
c'-c
$$

within width

$$
\delta_L+\delta_{L'}.
$$

## Nonresonance Condition

Define the resonance set

$$
\mathcal R_{L,L'}
=
\{c'-c:\ c,c'\text{ are low-conductor packet centers}\}.
$$

The shift `s` is nonresonant if

$$
\operatorname{dist}(s,\mathcal R_{L,L'})
\ge
C(\delta_L+\delta_{L'}).
$$

In this case the shifted supports do not overlap except through smoothing
tails.

## Overlap Bound

For smooth band weights with derivative scale `delta_L`, the desired estimate
is

$$
\left|
\int
w_{N,L}^{\perp}(\alpha)
\overline{w_{N,L'}^{\perp}(\alpha+s)}
d\alpha
\right|
\ll
L^{3/2}(L')^{3/2}
\left(
1+
{\operatorname{dist}(s,\mathcal R_{L,L'})
\over
\delta_L+\delta_{L'}}
\right)^{-A}.
$$

Thus

$$
\Delta_{L,L'}(\gamma)
\ll
\left(
1+
{\operatorname{dist}((\gamma-\ell)/d,\mathcal R_{L,L'})
\over
L^{-1}+(L')^{-1}}
\right)^{-A}.
$$

This is summable over nonresonant shifts for sufficiently large `A`, provided
the number of low-conductor packet centers is polylogarithmic.

## Rational Spacing Input

Low-conductor centers satisfy the spacing rule

$$
\left\|{a\over q}-{a'\over q'}\right\|
\ge
{1\over qq'}
$$

unless the centers are equal. For `q,q' <= Q_0`, distinct centers are
separated by at least `Q_0^{-2}`.

Consequences:

1. if `L,L' >> Q_0^2`, distinct rational packets do not overlap except at
   resonant shifts;
2. if `L` or `L'` is below this scale, overlap is handled by the lower-`L`
   mean-value estimate rather than high-`L` rational separation;
3. exact center matches are resonant and belong to the major projector or the
   diagonal band-energy estimate.

## Required Inputs

The nonresonant overlap proof needs four inputs.

**Support geometry.**
Dyadic bands must be represented by smooth annuli of width `asymp L^{-1}`.

**Major-aperture removal.**
The projected support must exclude the coherent core of each low-conductor
packet.

**Rational spacing.**
Distinct packet-center differences must be separated except in explicitly
listed resonant cases.

**Smooth-tail decay.**
When shifted supports miss, repeated integration by parts or smooth cutoff
decay gives arbitrarily strong decay in the normalized separation.

## Minimal Lemma

> **Nonresonant Shifted-Band Overlap Lemma.**  
> For projected dyadic kernel bands and a shift
> `s=(gamma-ell)/d` outside the resonance window around
> `R_{L,L'}`, the normalized overlap satisfies
> \[
> \Omega_{L,L'}(d,\gamma)
> \ll_A
> \left(
> 1+
> {\operatorname{dist}(s,\mathcal R_{L,L'})
> \over L^{-1}+(L')^{-1}}
> \right)^{-A},
> \]
> with the remaining resonant shifts assigned to major projection or diagonal
> projected band energy.

## Result

The nonresonant cross-band estimate is a deterministic geometry statement
about projected kernel supports. The only arithmetic input is rational-center
spacing for the low-conductor packets; the remaining work is smooth support
control and major-aperture removal.
