# Weighted Minor-Arc Shift-Kernel Mean-Value Strategy

Date: 2026-05-24

Status: candidate strategy for bounding the Fourier mean value associated to
the divisor-weighted shifted-correlation branch.

The Fourier form of the shifted-correlation estimate is

$$
\mathcal C(H)
=
\int_0^1
|A(\alpha)|^2
F_{Q_0,H,N}(\alpha)\,d\alpha,
$$

where

$$
A(\alpha)=\sum_{X<n\le2X}a_n e(\alpha n)
$$

is the residual endpoint sum after major-packet subtraction, and

$$
F_{Q_0,H,N}(\alpha)
=
\sum_{0<|h|\le H}
\tau_{Q_0}(h)\widehat\Omega_N(h)e(h\alpha).
$$

Here `H=rho^{-1}`.

## Structure of the Shift Kernel

Using

$$
\tau_{Q_0}(h)=\sum_{\substack{q\le Q_0\\q\mid h}}1,
$$

write

$$
F_{Q_0,H,N}(\alpha)
=
\sum_{q\le Q_0}
\sum_{0<|r|\le H/q}
\widehat\Omega_N(qr)e(qr\alpha).
$$

Thus `F` has large peaks near rationals with denominator at most `Q_0`.
These are the same low-conductor packets removed from `A`.

## Major/Minor Split for F

Decompose

$$
F=F_{\mathrm{maj}}+F_{\mathrm{min}},
$$

where `F_maj` is supported near low-conductor rational packets and `F_min`
is the residual divisor exponential sum.

The major-packet subtraction should make

$$
\int |A^{\perp}(\alpha)|^2F_{\mathrm{maj}}(\alpha)\,d\alpha
$$

fit the major error budget. The minor task is

$$
\int_{\mathfrak m}
|A^{\perp}(\alpha)|^2
F_{\mathrm{min}}(\alpha)\,d\alpha
\ll
\mathcal E_{\mathrm{shift}}.
$$

## Mean-Value Route

A sufficient bound is

$$
\|F_{\mathrm{min}}\|_{\infty}
\int_{\mathfrak m}|A^{\perp}(\alpha)|^2\,d\alpha
\ll
\mathcal E_{\mathrm{shift}}.
$$

The two required estimates are:

1. a minor-arc mean square for the residual endpoint sum `A^perp`;
2. a minor-arc bound for the divisor-weighted shift kernel `F_min`.

If `||F_min||_infty` is too large, use an `L^p` estimate:

$$
\|F_{\mathrm{min}}\|_p
\|A^{\perp}\|_{2p/(p-1)}^2
\ll
\mathcal E_{\mathrm{shift}}.
$$

## Divisor Exponential-Sum Input

The kernel `F` is a smoothed truncated divisor exponential sum. On minor arcs,
the needed estimate has the form

$$
F_{\mathrm{min}}(\alpha)
\ll
H(\log X)^C\Delta_{\mathrm{div}}(\alpha),
$$

where `Delta_div` is small away from rationals with denominator at most
`Q_0`.

This is a deterministic or classical exponential-sum estimate for the
truncated divisor weight, coupled to the decay of `widehat Omega_N(h)`.

## Endpoint Sum Input

For `A^perp`, the required input is the same residual minor-arc estimate
used earlier in the Type II route:

$$
\int_{\mathfrak m}|A^{\perp}(\alpha)|^2\,d\alpha
\ll
\mathcal A_{\mathrm{min}}.
$$

If this estimate is not available at the required strength, apply Vaughan or
Heath-Brown decomposition and prove Type I/II bounds with the multiplier
`F_min`.

## Minimal Lemma

> **Shift-Kernel Weighted Minor Mean Lemma.**  
> After major-packet subtraction,
> \[
> \int_{\mathfrak m}
> |A^{\perp}(\alpha)|^2
> F_{Q_0,H,N}^{\mathrm{min}}(\alpha)\,d\alpha
> \le
> \mathcal E_{\mathrm{shift}}
> \]
> at `H=rho^{-1}`, using either a minor-arc `L^2` bound for `A^perp` times a
> divisor-kernel minor bound, or a Type I/II dispersion estimate with the
> multiplier included.

## Result

The Fourier mean-value branch reduces the shifted-correlation problem to two
objects: residual endpoint minor-arc mass and minor-arc size of the
divisor-weighted shift kernel. Low-denominator peaks of the shift kernel are
major packet structure; after subtracting them, the remaining estimate is a
minor-arc mean-value or Type I/II dispersion problem.
