# Kernel-Weighted BDH Known-Form Strategy

Date: 2026-05-24

Status: closest-known-form note for the kernel-weighted square-mean
Bombieri-Vinogradov input.

The required estimate is

$$
{ \mathcal B_{\mathrm{AP}}^{K}(X,Q_0,N,\rho)
\over
(\log X)^2}
\le
\mathcal E_{\mathrm{tot}}(d,N),
\qquad
\rho={c_0\over L_{\mathrm{crit}}(d,N)}.
$$

This is a kernel-weighted, continuous-window, square-mean AP estimate. It is
closest to BDH/Bombieri-Vinogradov mean-square theory, but it is not identical
to the standard statement.

## Closest Standard Inputs

**BDH square-mean AP estimates.**
The standard Barban-Davenport-Halberstam form controls

$$
\sum_{q\le Q}\sum_{(a,q)=1}
\left|
\psi(X;q,a)-{X\over\varphi(q)}
\right|^2.
$$

This supplies the correct square-mean AP object, but not the continuous
`beta` integration or kernel-window weights required here.

**Large sieve / continuous frequency estimates.**
Large-sieve estimates control mean squares over separated frequencies. They
are the natural source for passing from discrete packet centers `a/q` to
windows `a/q+beta`.

**Large-moduli BV refinements.**
Modern BV-type mean-value theorems can extend the modulus range or handle
structured moduli, but they still must be adapted to the kernel-weighted
window budget.

## Required Adaptation

The needed theorem should estimate

$$
\sum_{q\le Q_0}\sum_{(a,q)=1}
\int_{|\beta|\le\rho}
\left|
B_X\!\left({a\over q}+\beta\right)
-\operatorname{Major}_{a/q}(\beta)
\right|^2
|K_N(a/q+\beta)|^2\,d\beta .
$$

The standard BDH theorem gives the AP variance at fixed endpoints. The
adaptation must add:

1. maximal or smoothed control in `x`;
2. partial summation uniform in `beta`;
3. kernel-window weights `|K_N|^2`;
4. bounded overlap of continuous windows using rational spacing;
5. explicit treatment of coherent exceptional terms as major packet
   components.

## Large-Sieve Proof Route

A direct proof should avoid the intermediate supremum `E_q(X)`. Expand the
windowed error into character sums and apply a large-sieve mean value to

$$
\sum_n a_n\chi(n)e(\beta n)
$$

integrated over `|beta| <= rho` with weight `|K_N(a/q+beta)|^2`.

The required input has the shape

$$
\sum_{q\le Q_0}
\sum_{\chi\bmod q}^{*}
\int_{|\beta|\le\rho}
\left|
\sum_{X<n\le2X}
a_n\chi(n)e(\beta n)
\right|^2
\omega_{q,\chi,N}(\beta)\,d\beta
\ll
\mathcal B_{\mathrm{AP}}^{K}.
$$

Here `a_n` is the centered prime or von Mangoldt coefficient and
`omega` packages the kernel window and packet decomposition. This is a
kernel-weighted large-sieve theorem.

## Gap to Existing BDH-Type Theorems

The gap is not the existence of AP square-mean control. The gap is the exact
weighted form:

$$
\text{BDH variance}
\quad+\quad
\text{continuous } \beta \text{ window}
\quad+\quad
|K_N|^2 \text{ aperture weight}
\quad+\quad
\text{major-packet subtraction}.
$$

If a known weighted/maximal BDH theorem supplies this package, it can be
inserted directly. Otherwise the bridge needs a local proof using large sieve
plus partial summation.

## Source Pointers

Relevant known-form families include:

- Gallagher's large-sieve framework:
  [The large sieve](https://www.cambridge.org/core/services/aop-cambridge-core/content/view/4DC1EC8072D840195F1EF81F5828BB0F/S0025579300007968a.pdf/large_sieve.pdf).
- BDH refinements:
  [On the Barban-Davenport-Halberstam Theorem: IV](https://academic.oup.com/jlms/article-pdf/s2-11/4/399/2633890/s2-11-4-399.pdf).
- Large-moduli BV refinements:
  [Primes in arithmetic progressions to large moduli III](https://arxiv.org/abs/2006.08250).

These locate the analytic neighborhood. The exact kernel-weighted aperture
form remains an input to prove or cite in a sharper version.

## Minimal Lemma

> **Kernel-Weighted Maximal BDH Lemma.**  
> For the centered endpoint coefficient sequence and every aperture radius
> `rho=c0/L_crit(d,N)`, the major-window square mean after major-packet
> subtraction satisfies
> \[
> \sum_{q\le Q_0}\sum_{(a,q)=1}
> \int_{|\beta|\le\rho}
> |\operatorname{Err}_{a/q}(\beta)|^2
> |K_N(a/q+\beta)|^2\,d\beta
> \le
> \mathcal E_{\mathrm{tot}}(d,N).
> \]

## Result

The closest known machinery is BDH plus the large sieve. The exact bridge
requires a kernel-weighted maximal BDH form: square-mean AP control integrated
over major windows, with the interval-kernel weight and major-packet
subtraction included before comparing to the aperture error budget.
