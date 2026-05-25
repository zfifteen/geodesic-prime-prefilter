# Divisor-Weighted Shifted-Correlation Strategy

Date: 2026-05-24

Status: candidate strategy for the explicit shifted-correlation branch of the
dual hybrid large-sieve estimate.

If the large-sieve operator norm does not fit the aperture budget, the dual
form requires a shifted-correlation estimate for residual endpoint
coefficients:

$$
\mathcal C(H)
=
\sum_{0<|h|\le H}
\tau_{Q_0}(h)\widehat\Omega_N(h)
\sum_{X<m,m+h\le2X}
a_{m+h}\overline{a_m},
\qquad
H\asymp \rho^{-1}.
$$

Here

$$
\tau_{Q_0}(h)=\#\{q\le Q_0:q\mid h\},
$$

and `a_n` is the residual coefficient after major-packet subtraction.

## Divisor-Weight Decomposition

Use

$$
\tau_{Q_0}(h)=\sum_{\substack{q\le Q_0\\q\mid h}}1.
$$

Then

$$
\mathcal C(H)
=
\sum_{q\le Q_0}
\sum_{0<|r|\le H/q}
\widehat\Omega_N(qr)
\sum_m
a_{m+qr}\overline{a_m}.
$$

This is an average of shifted correlations over arithmetic-progressed shifts.
It is the same information as the dual congruence condition, written without
characters.

## Fourier Form

Let

$$
A(\alpha)=\sum_{X<n\le2X}a_n e(\alpha n).
$$

Then the shifted sum is

$$
\mathcal C(H)
=
\int_0^1
|A(\alpha)|^2
F_{Q_0,H,N}(\alpha)\,d\alpha,
$$

where

$$
F_{Q_0,H,N}(\alpha)
=
\sum_{0<|h|\le H}
\tau_{Q_0}(h)\widehat\Omega_N(h)e(h\alpha).
$$

Major-packet subtraction should remove the parts of `A(alpha)` that correlate
with the large low-denominator peaks of `F`.

## Dispersion Route

Apply Vaughan or Heath-Brown decomposition to `a_n`. The shifted correlation
then splits into:

1. Type I shifted divisor sums;
2. Type II bilinear shifted sums;
3. diagonal and near-diagonal terms assigned to the Poisson model;
4. transition terms near major packets.

The Type II part returns to bilinear dispersion and Kloosterman-type
estimates. This is consistent with the earlier Kloosterman branch, not a new
unrelated problem.

## Mean-Value Route

The Fourier form can be bounded by a weighted mean-value theorem:

$$
\int_{\mathfrak m}
|A(\alpha)|^2F_{Q_0,H,N}(\alpha)\,d\alpha
\ll
\mathcal E_{\mathrm{shift}},
$$

after the major packet part of `A` is removed. This is a minor-arc mean-square
estimate with a divisor-weighted kernel.

The mean-value route is preferable if `F` has controlled `L^1` or `L^\infty`
norm after major projection.

## Required Inputs

The shifted-correlation proof needs:

1. divisor-weight control for `tau_{Q0}(h)`;
2. decay or summability of `widehat Omega_N(h)`;
3. major-packet subtraction for low-denominator peaks of `A(alpha)`;
4. Type I/II dispersion estimates for residual coefficients;
5. a treatment of shifted-prime correlations averaged over `q|h`, not
   pointwise in each fixed shift.

## Minimal Lemma

> **Kernel-Weighted Divisor-Shift Correlation Lemma.**  
> For residual endpoint coefficients after major-packet subtraction and
> `H=rho^{-1}`, the divisor-weighted shifted correlation
> \[
> \sum_{0<|h|\le H}
> \tau_{Q_0}(h)\widehat\Omega_N(h)
> \sum_m a_{m+h}\overline{a_m}
> \]
> is bounded by the aperture error budget, either by Fourier mean-value
> control of `|A(alpha)|^2F(alpha)` or by Type I/II dispersion after Vaughan
> or Heath-Brown decomposition.

## Result

The explicit shifted-correlation route is a divisor-weighted average of
prime-pair correlations. It is weaker than proving each shift individually,
but stronger than the large-sieve operator norm. The analytic tools are
weighted minor-arc mean values, Type I/II dispersion, and the same bilinear
Kloosterman machinery already isolated in the reciprocal-congruence branch.
