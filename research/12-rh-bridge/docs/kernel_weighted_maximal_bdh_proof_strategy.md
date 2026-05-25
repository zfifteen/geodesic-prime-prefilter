# Kernel-Weighted Maximal BDH Proof Strategy

Date: 2026-05-24

Status: candidate proof strategy for the kernel-weighted maximal BDH input.

The target estimate is

$$
\sum_{q\le Q_0}\sum_{(a,q)=1}
\int_{|\beta|\le\rho}
|\operatorname{Err}_{a/q}(\beta)|^2
|K_N(a/q+\beta)|^2\,d\beta
\le
\mathcal E_{\mathrm{tot}},
$$

at the aperture scale

$$
\rho={c_0\over L_{\mathrm{crit}}(d,N)}.
$$

The error is taken after subtracting the major packet model.

## Character Decomposition

For the von Mangoldt-weighted version, write the AP error through
nonprincipal characters:

$$
\operatorname{Err}_{a/q}(\beta)
\sim
{1\over\varphi(q)}
\sum_{\chi\bmod q}^{*}
\overline{\chi(a)}
S_{\chi}(\beta),
$$

where

$$
S_{\chi}(\beta)
=
\sum_{X<n\le2X}
\Lambda(n)\chi(n)e(\beta n)
-
\operatorname{Major}_{\chi}(\beta).
$$

The principal and exceptional coherent terms are part of the major packet
model and are removed before this estimate.

## Kernel Weight Obstruction

Without the kernel weight, summing over `a mod q` uses character
orthogonality. With the factor

$$
|K_N(a/q+\beta)|^2,
$$

the `a`-sum is weighted. Exact orthogonality no longer directly diagonalizes
the character expansion.

This is the main adaptation beyond standard BDH.

## Hybrid Large-Sieve Input

A sufficient input is a hybrid character/additive large-sieve estimate:

$$
\sum_{q\le Q_0}
\sum_{\chi\bmod q}^{*}
\int_{|\beta|\le\rho}
|S_{\chi}(\beta)|^2
\Omega_{q,\chi,N}(\beta)\,d\beta
\ll
\mathcal B_{\mathrm{AP}}^K(X,Q_0,N,\rho),
$$

where `Omega` is the kernel-window weight after resolving the `a`-dependent
factor. A schematic strength is

$$
\mathcal B_{\mathrm{AP}}^K
\ll
(X+Q_0^2+\rho^{-1})\,X(\log X)^C
$$

with improvements from prime-distribution input or major-packet subtraction
as needed.

This is a large-sieve theorem over the hybrid frequencies

$$
\alpha={a\over q}+\beta.
$$

The rational spacing and aperture condition `rho <= c Q_0^{-2}` ensure
bounded overlap of the windows.

## Partial Summation and Maximal Control

The endpoint sum uses `1_P` or a centered unweighted prime coefficient, while
character estimates are naturally stated for `Lambda`. The proof needs:

1. partial summation from `Lambda` to the endpoint coefficient;
2. maximal or smoothed control in `x <= 2X`;
3. preservation of the major packet subtraction under partial summation;
4. no loss beyond the logarithmic allowance in the Poisson budget.

## Major-Packet Subtraction

Before applying the large sieve, remove:

1. principal character terms;
2. exceptional coherent terms if present;
3. low-conductor packet model functions;
4. exact centered constant terms.

The estimate is for the residual. If these terms are left inside
`S_chi(beta)`, the kernel-weighted mean square contains coherent major energy
and cannot represent the aperture error.

## Required Closure Strength

The proof closes the radius input when

$$
{ \mathcal B_{\mathrm{AP}}^K(X,Q_0,N,\rho)
\over
(\log X)^2}
\le
\mathcal E_{\mathrm{tot}}(d,N).
$$

If the schematic hybrid large-sieve bound is too large, the missing saving
must come from:

1. stronger prime-distribution mean values for `S_chi(beta)`;
2. sharper use of the kernel weight instead of a worst-case large sieve;
3. cancellation from major-packet subtraction before the `a`-weighted
   character sum is squared.

## Minimal Lemma

> **Kernel-Weighted Maximal BDH Proof Lemma.**  
> After subtracting principal, exceptional, and low-conductor major packet
> components, the residual character sums satisfy a hybrid character/additive
> large-sieve estimate over `alpha=a/q+beta`, `q <= Q_0`, `|beta| <= rho`,
> with the interval-kernel weight included, strong enough that
> `B_AP^K/log^2 X <= E_tot` at `rho=c0/L_crit(d,N)`.

## Result

The kernel-weighted maximal BDH input is a hybrid large-sieve theorem for
major-window residuals. The exact new feature beyond standard BDH is the
`a`-dependent kernel weight; it must be handled either by a weighted character
large sieve or by a direct continuous-frequency large sieve after the major
packet terms are removed.
