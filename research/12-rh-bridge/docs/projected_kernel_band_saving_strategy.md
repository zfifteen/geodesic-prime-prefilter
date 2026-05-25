# Projected Kernel-Band Saving Strategy

Date: 2026-05-24

Status: candidate strategy for improving the base kernel-band energy bound.

The base estimate gives

$$
E_A(d,N,L)\ll d^{-1}L^3\mathcal B_d.
$$

If this exceeds the Poisson allowance, the proof needs saving from the
projected kernel band. There are two possible mechanisms:

1. mean-value saving in the projected band weight;
2. cancellation among kernel transforms before absolute squaring.

## Projected Band Mean-Value Saving

Let

$$
w_{N,L}^{\perp}=(1-P_{\mathrm{maj}})w_{N,L}
$$

be the band weight after the major-exclusion projector. The desired saving is

$$
\|w_{N,L}^{\perp}\|_2^2
\ll
L^3\Delta_L,
\qquad
\Delta_L<1.
$$

By Parseval this gives

$$
\sum_t |W_{N,L}^{\perp}(dt)|^2
\ll
d^{-1}L^3\Delta_L.
$$

The saving `Delta_L` is therefore exactly a projected mean-value saving for
the band weight.

## Major-Aperture Condition

Since `w_{N,L}` has size `L^2` on a set of measure `<< L^{-1}`, the estimate

$$
\|w_{N,L}^{\perp}\|_2^2\ll L^3\Delta_L
$$

follows from the residual support bound

$$
|\operatorname{supp} w_{N,L}^{\perp}|
\ll
\Delta_L L^{-1}.
$$

Thus one route is a major-aperture lemma:

> The major projector captures all but a `Delta_L` fraction of the
> `|K_N| asymp L` band energy associated with low-conductor rational packets.

This route is strongest in high-`L` bands, where kernel mass is concentrated
near rational centers. It gives no saving in bands whose support is genuinely
minor and spread out.

## Low-Denominator Orthogonality

A softer route does not require literal support removal. It is enough that the
projector removes the low-dimensional span of rational packet functions that
carry most of the band energy:

$$
\|(1-P_{\mathrm{maj}})w_{N,L}\|_2^2
\le
\Delta_L\|w_{N,L}\|_2^2.
$$

This is an orthogonality statement: the high-energy component of the kernel
band lies in the major packet span. It is a mean-value theorem for the kernel,
not a prime-distribution statement.

## Pre-Squaring Kernel Cancellation

The stronger alternative is to avoid bounding each band separately. Estimate

$$
\sum_t
\left|
\sum_L c_L e(adt/q)W_{N,L}^{\perp}(dt)
\right|^2
$$

directly. Expanding gives cross terms

$$
\sum_t
W_{N,L}^{\perp}(dt)
\overline{W_{N,L'}^{\perp}(dt)}
e\!\left({ad t\over q}-{ad t\over q'}\right).
$$

By Parseval these cross terms are inner products of shifted projected band
weights. They are small if:

1. distinct bands have almost disjoint support;
2. different rational shifts move the supports apart;
3. the projected weights have zero low-frequency component;
4. smoothing gives rapid decay away from the band scale.

This mechanism uses phase information lost in the bandwise estimate
`sum_t |W_{N,L}(dt)|^2`.

## Required Inputs

The next proof needs one of these estimates.

**Projected band support estimate.**

$$
|\operatorname{supp}w_{N,L}^{\perp}|
\ll
\Delta_L L^{-1}.
$$

**Projected band orthogonality estimate.**

$$
\|(1-P_{\mathrm{maj}})w_{N,L}\|_2^2
\ll
\Delta_L L^3.
$$

**Cross-band transform estimate.**

$$
\sum_t
W_{N,L}^{\perp}(dt)
\overline{W_{N,L'}^{\perp}(dt)}
e(\gamma t)
\ll
d^{-1}(LL')^{3/2}\Delta_{L,L'}(\gamma),
$$

with summable `Delta_{L,L'}(gamma)` after the dyadic and rational-shift sums.

## Minimal Saving Statement

The kernel-band branch closes if the following holds.

> **Projected Kernel-Band Saving Lemma.**  
> After major-exclusion, each dyadic band either has projected energy
> `<< L^3 Delta_L` with enough saving to satisfy the Completion Energy Bound,
> or the sum over bands and rational shifts satisfies a cross-transform
> estimate giving the same net saving before absolute squaring.

## Result

The remaining kernel-band problem is now explicit. The base Parseval estimate
is deterministic. Any improvement must be supplied by the major projector
capturing most high-`L` band energy, by orthogonality to low-denominator packet
functions, or by cross-band/rational-shift cancellation before squaring.
