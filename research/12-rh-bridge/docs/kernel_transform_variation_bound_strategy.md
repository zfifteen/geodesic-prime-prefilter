# Kernel Transform Variation Bound Strategy

Date: 2026-05-24

Status: candidate deterministic estimate for the variation term `V_q` in the
shift-kernel threshold inequality.

The divisor-kernel minor bound needs a size/variation control for

$$
\widehat\Omega_N(qr),
\qquad
1\le |r|\le H/q,
$$

where

$$
H=\rho^{-1}
$$

is the aperture shift scale.

## Smooth Aperture Weight

Let `Omega_N(beta)` be the projected, smoothed aperture weight whose transform
appears in the shifted kernel:

$$
\widehat\Omega_N(h)
=
\int \Omega_N(\beta)e(\beta h)\,d\beta.
$$

Assume `Omega_N` is supported on `|beta| <= rho` after projection and
smoothing.

## Supremum Bound

The elementary Fourier bound gives

$$
|\widehat\Omega_N(h)|
\le
\|\Omega_N\|_1.
$$

Thus

$$
\sup_{1\le |r|\le H/q}
|\widehat\Omega_N(qr)|
\le
\|\Omega_N\|_1.
$$

## Discrete Variation Bound

For consecutive samples,

$$
\widehat\Omega_N(q(r+1))-\widehat\Omega_N(qr)
=
\int \Omega_N(\beta)e(qr\beta)(e(q\beta)-1)\,d\beta.
$$

Since `|beta| <= rho`,

$$
|e(q\beta)-1|\ll q|\beta|.
$$

Therefore

$$
\sum_{1\le |r|\le H/q}
|\widehat\Omega_N(q(r+1))-\widehat\Omega_N(qr)|
\ll
{H\over q}\,q
\int |\beta|\,|\Omega_N(\beta)|\,d\beta.
$$

Using `H=rho^{-1}` and `|beta| <= rho`,

$$
\sum_{1\le |r|\le H/q}
|\widehat\Omega_N(q(r+1))-\widehat\Omega_N(qr)|
\ll
\|\Omega_N\|_1.
$$

Hence the required variation factor satisfies

$$
V_q\ll \|\Omega_N\|_1
$$

uniformly in `q <= Q_0`.

## Kernel Mass

If

$$
\Omega_N(\beta)
\asymp
|K_N(c+\beta)|^2
$$

on an aperture window, then

$$
\|\Omega_N\|_1
\le
\int_{|\beta|\le\rho}
\min(N^2,\|c+\beta\|^{-2})\,d\beta.
$$

This is the deterministic kernel-window mass already appearing in the
major-radius budget.

## Smoothness Requirement

The argument requires a smoothed aperture cutoff. A sharp cutoff introduces
boundary variation that must either be smoothed away or charged to the
Poisson error budget. With a smooth cutoff, higher derivatives also give
rapid decay of `Omegahat_N(h)` beyond `H`.

## Minimal Lemma

> **Kernel Transform Variation Lemma.**  
> For the smoothed projected aperture weight `Omega_N` supported on
> `|beta| <= rho`, the samples of its transform satisfy
> \[
> V_q
> =
> \sup_{|r|\le H/q}|\widehat\Omega_N(qr)|
> +
> \operatorname{Var}_{|r|\le H/q}\widehat\Omega_N(qr)
> \ll
> \|\Omega_N\|_1
> \]
> uniformly for `q <= Q_0`, with `H=rho^{-1}`.

## Result

The variation input is deterministic. Once the aperture weight is smoothed,
`V_q` is controlled by the `L1` mass of the projected kernel window. The next
threshold check can replace `V_q` by this explicit kernel-window mass.
