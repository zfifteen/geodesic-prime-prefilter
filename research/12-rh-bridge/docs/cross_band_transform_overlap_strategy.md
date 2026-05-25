# Cross-Band Transform Overlap Strategy

Date: 2026-05-24

Status: candidate strategy for estimating cross-band and cross-rational
transform terms after major-exclusion.

The cross-transform object is

$$
\mathcal X_{L,L'}(d,\gamma)
=
\sum_t
W_{N,L}^{\perp}(dt)
\overline{W_{N,L'}^{\perp}(dt)}
e(\gamma t),
$$

where `gamma` records the rational-phase difference between two shifted
pieces. The goal is to bound this by overlap of projected kernel bands.

## Sampling Identity

Write

$$
W_{N,L}^{\perp}(r)
=
\int w_{N,L}^{\perp}(\alpha)e(\alpha r)\,d\alpha .
$$

Then

$$
\mathcal X_{L,L'}(d,\gamma)
=
\sum_t
\int\!\!\int
w_{N,L}^{\perp}(\alpha)
\overline{w_{N,L'}^{\perp}(\beta)}
e(t(d\alpha-d\beta+\gamma))\,d\alpha\,d\beta .
$$

Poisson summation on the sampled lattice gives the schematic identity

$$
\mathcal X_{L,L'}(d,\gamma)
=
{1\over d}
\sum_{\ell\in\mathbb Z}
\int
w_{N,L}^{\perp}(\alpha)
\overline{
w_{N,L'}^{\perp}
\!\left(\alpha+{\gamma-\ell\over d}\right)}
d\alpha ,
$$

with harmless smoothing errors. Thus cross-transform control is a shifted
overlap estimate for projected band weights.

## Normalized Overlap

Define

$$
\Omega_{L,L'}(d,\gamma)
=
\sup_{\ell}
{ \left|
\int
w_{N,L}^{\perp}(\alpha)
\overline{
w_{N,L'}^{\perp}
\!\left(\alpha+{\gamma-\ell\over d}\right)}
d\alpha
\right|
\over
\|w_{N,L}\|_2\|w_{N,L'}\|_2 }.
$$

Since

$$
\|w_{N,L}\|_2\ll L^{3/2},
\qquad
\|w_{N,L'}\|_2\ll (L')^{3/2},
$$

the cross estimate becomes

$$
|\mathcal X_{L,L'}(d,\gamma)|
\ll
d^{-1}(LL')^{3/2}
\Omega_{L,L'}(d,\gamma).
$$

The desired saving is a summable bound for `Omega`.

## Resonant Shifts

Large overlap occurs when

$$
{\gamma-\ell\over d}
$$

moves one projected band onto the other. These are exactly the shifts that
align low-denominator rational packets. The major projector must classify
them as coherent major pieces unless the bands are already genuinely minor
after projection.

The dangerous cases are:

1. `L=L'` and `gamma=0`;
2. nearby dyadic bands with nearly identical support;
3. rational shifts whose denominator is inside the major conductor range;
4. high-`L` bands centered at the same rational packet.

## Nonresonant Overlap Estimate

Away from resonant shifts, the supports of the projected bands have small
intersection. A sufficient estimate is

$$
\operatorname{meas}\left(
\operatorname{supp}w_{N,L}^{\perp}
\cap
\left(
\operatorname{supp}w_{N,L'}^{\perp}
-{\gamma-\ell\over d}
\right)
\right)
\ll
\Delta_{L,L'}(\gamma)\,(LL')^{-1/2}.
$$

With amplitudes `L^2` and `(L')^2`, this gives

$$
\Omega_{L,L'}(d,\gamma)
\ll
\Delta_{L,L'}(\gamma),
$$

after normalizing by the `L^2` norms.

## Limitation of Cross-Band Cancellation

Cross-band estimates control off-diagonal accumulation among bands and
rational shifts. They do not remove the positive diagonal energy

$$
\sum_t |W_{N,L}^{\perp}(dt)|^2
$$

for a single band. Therefore, if the base diagonal energy
`d^{-1}L^3 B_d` already exceeds the Poisson allowance, a cross-band estimate
alone cannot close the Completion Energy Bound.

In that case the proof also needs projected band mean-value saving for the
diagonal term.

## Minimal Cross-Transform Input

> **Projected Shifted-Band Overlap Lemma.**  
> For nonresonant rational shifts after major-exclusion,
> \[
> \Omega_{L,L'}(d,\gamma)
> \ll \Delta_{L,L'}(\gamma)
> \]
> with `Delta_{L,L'}(gamma)` summable over dyadic bands, rational shifts, and
> common-divisor slices. Resonant shifts are assigned to the major projector
> or controlled by the diagonal projected band-energy estimate.

## Result

The cross-transform problem is an overlap problem for projected kernel bands
shifted by `(gamma-ell)/d`. It can prevent off-diagonal band and rational-shift
accumulation, but the diagonal band energy still requires its own projected
mean-value bound if the base `L^3` estimate is too large.
