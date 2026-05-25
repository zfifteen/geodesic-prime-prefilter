# Major Validity Radius Strategy

Date: 2026-05-24

Status: candidate strategy for proving the major-arc validity radius needed by
the Major Aperture Feasibility Lemma.

Let

$$
B_X(\alpha)=
\sum_{X<n\le 2X}
b_X(n)e(\alpha n)
$$

be the centered endpoint Fourier sum, with `b_X` the centered endpoint
weight used in the RH bridge notes. For a low-conductor center

$$
c={a\over q},\qquad q\le Q_0,
$$

the major validity radius `rho_valid(c)` is the largest radius on which
`B_X(c+beta)` is approximated by its major packet model with error inside the
kernel-weighted Poisson budget.

## Major Packet Approximation

The required approximation has the form

$$
B_X\!\left({a\over q}+\beta\right)
=
\operatorname{Major}_{a/q}(\beta)
+
\operatorname{Err}_{a/q}(\beta),
\qquad
|\beta|\le \rho.
$$

The centered constant term is explicit: its Fourier transform is a geometric
sum or smooth integral and contributes no prime-distribution error. The prime
part is controlled by primes in arithmetic progressions modulo `q`.

For a von Mangoldt-weighted version, the model is governed by

$$
\psi(x;q,r)-{x\over \varphi(q)}.
$$

For the unweighted endpoint sum, partial summation transfers the same input
to `1_P` with logarithmic weights.

## Error Budget Definition

Define `rho_valid(a/q)` by the condition

$$
\int_{|\beta|\le \rho}
|\operatorname{Err}_{a/q}(\beta)|^2
|K_N(a/q+\beta)|^2\,d\beta
\le
\mathcal E_{a,q,N},
$$

where `E_{a,q,N}` is the error budget assigned to this major packet inside
the centered four-energy and Type II aperture argument.

The radius is valid for aperture removal if

$$
{c_0\over L_{\mathrm{crit}}(d,N)}
\le
\rho_{\mathrm{valid}}(a/q)
$$

for every failing `d`-slice attached to that packet.

## Inputs by Modulus Range

**PNT in arithmetic progressions.**
For fixed or polylogarithmic `q`, a Siegel-Walfisz strength estimate gives
errors small enough for major packets whose aperture radius is not too large
for the kernel budget.

**Bombieri-Vinogradov.**
If `Q_0` grows beyond the fixed/polylogarithmic range, averaged control over
`q <= Q_0` can supply the major packet approximation on average over packet
centers.

**Zero-density estimates.**
For transition arcs or larger moduli near the major/minor boundary,
zero-density estimates provide a radius/error tradeoff when individual PNT
in AP is not strong enough.

## Radius From Error Growth

Let

$$
E_q(X)=
\max_{(r,q)=1}
\sup_{x\le 2X}
\left|
\psi(x;q,r)-{x\over\varphi(q)}
\right|.
$$

Partial summation gives the schematic bound

$$
|\operatorname{Err}_{a/q}(\beta)|
\ll
{E_q(X)\over \log X}(1+X|\beta|)
$$

for the unweighted endpoint sum, with the usual logarithmic modifications for
smooth weights.

Thus the validity radius is determined by the largest `rho` for which

$$
\int_{|\beta|\le \rho}
\left({E_q(X)\over \log X}\right)^2
(1+X|\beta|)^2
|K_N(a/q+\beta)|^2\,d\beta
\le
\mathcal E_{a,q,N}.
$$

This turns major validity into a direct radius/error-budget comparison.

## Minimal Lemma

> **Centered Endpoint Major Radius Lemma.**  
> For every low-conductor center `a/q`, the centered endpoint Fourier sum has
> a major packet approximation on `|beta| <= rho_valid(a/q)` with
> kernel-weighted error inside `E_{a,q,N}`, and this radius satisfies
> \[
> {c_0\over L_{\mathrm{crit}}(d,N)}
> \le
> \rho_{\mathrm{valid}}(a/q)
> \]
> for every failing dyadic `d`-slice and kernel band, unless the orthogonal
> packet-frame route is used.

## Result

The major validity radius is an analytic major-arc estimate for the centered
endpoint Fourier sum. The needed inputs are PNT in AP for small moduli,
Bombieri-Vinogradov for averaged small-conductor packets, and zero-density
control in transition ranges, all measured against the same kernel-weighted
Poisson error budget used by the aperture feasibility lemma.
