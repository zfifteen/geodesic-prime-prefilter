# Kernel-Weighted BDH at the Unified Aperture Scale

Date: 2026-05-24

Status: candidate theorem statement and proof strategy for the averaged
major-validity input at the unified aperture radius.

The unified aperture radius is

$$
R_{\mathrm{req}}(c,d,N)
=
\max\left(
{c_0\over L_{\mathrm{crit}}(d,N)},
M_{\Omega}^{-1}
\right).
$$

The averaged route needs kernel-weighted major-window square-mean control at
this radius.

## Target Estimate

Let `Err_{a/q}(beta)` be the centered endpoint major approximation error after
principal, exceptional, and low-conductor packet components have been removed.
The target is

$$
\sum_{q\le Q_0}\sum_{(a,q)=1}
\int_{|\beta|\le R_{\mathrm{req}}(a/q,d,N)}
|\operatorname{Err}_{a/q}(\beta)|^2
|K_N(a/q+\beta)|^2\,d\beta
\le
\mathcal E_{\mathrm{maj}}(d,N).
$$

The budget `E_maj(d,N)` must cover both:

1. high-`L` band aperture removal;
2. kernel-core mass removal for the shift-kernel threshold closure.

## Character-Sum Form

After character decomposition and major-packet subtraction, the estimate
reduces to a weighted hybrid mean value

$$
\sum_{q\le Q_0}
\sum_{\chi\bmod q}^{*}
\int_{|\beta|\le R_{\mathrm{req}}}
\left|
\sum_{X<n\le2X}a_n\chi(n)e(\beta n)
\right|^2
\Omega_{q,\chi,N}(\beta)\,d\beta
\ll
\mathcal B_{\mathrm{AP}}^K.
$$

The required strength is

$$
{\mathcal B_{\mathrm{AP}}^K
\over
(\log X)^2}
\le
\mathcal E_{\mathrm{maj}}(d,N).
$$

## Large-Sieve Route

A sufficient large-sieve bound has schematic size

$$
\mathcal B_{\mathrm{AP}}^K
\ll
(X+Q_0^2+R_{\mathrm{req}}^{-1})
X(\log X)^C
\cdot
\mathcal W_K,
$$

where `W_K` records the weighted-window improvement or loss from
`|K_N|^2`.

The proof must exploit:

1. rational spacing of `a/q` windows at radius `R_req`;
2. kernel-weighted rather than worst-window averaging;
3. major-packet subtraction before squaring;
4. partial summation from `Lambda` to endpoint coefficients.

## Dual Route

The dual form is the shifted-congruence estimate at

$$
H=R_{\mathrm{req}}^{-1}.
$$

The already isolated post-variation closure condition is

$$
\|\Omega_N\|_1
\mathcal S(Q_0,H,\rho_{\max})
\mathcal A_{\mathrm{min}}
\le
\mathcal E_{\mathrm{shift}}.
$$

Thus the BDH proof at `R_req` can close either by the hybrid large-sieve
operator norm or by the divisor-shift mean-value branch already reduced to
kernel mass and threshold feasibility.

## Required Inputs

The unified-scale BDH theorem needs:

1. kernel-weighted hybrid character/additive large sieve at
   `rho=R_req`;
2. major-packet subtraction for coherent principal and exceptional terms;
3. deterministic kernel-window mass at `R_req`;
4. residual endpoint minor `L2` mass `A_min`;
5. budget allocation between `E_maj` and `E_shift`.

## Minimal Lemma

> **Unified-Scale Kernel-Weighted BDH Lemma.**  
> At
> \[
> R_{\mathrm{req}}=\max(c_0/L_{\mathrm{crit}},M_{\Omega}^{-1}),
> \]
> the centered endpoint major-window error satisfies the kernel-weighted
> square-mean bound
> \[
> \sum_{q\le Q_0}\sum_{(a,q)=1}
> \int_{|\beta|\le R_{\mathrm{req}}}
> |\operatorname{Err}_{a/q}(\beta)|^2|K_N(a/q+\beta)|^2\,d\beta
> \le \mathcal E_{\mathrm{maj}},
> \]
> with strength sufficient for both unified aperture removal and
> shift-kernel threshold closure.

## Result

The averaged major-validity route has one theorem left at this level:
kernel-weighted BDH at the unified radius `R_req`. Its proof is either a
hybrid character/additive large sieve with packet subtraction, or the dual
shift-kernel mean-value route whose scalar closure condition has already been
isolated.
