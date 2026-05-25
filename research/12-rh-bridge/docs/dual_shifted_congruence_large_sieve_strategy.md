# Dual Shifted-Congruence Large-Sieve Strategy

Date: 2026-05-24

Status: candidate strategy for the dual form of the hybrid character/additive
large sieve.

The hybrid large-sieve dual form controls correlations

$$
n\equiv m\pmod q,
\qquad
|n-m|\lesssim \rho^{-1},
$$

with kernel weights and residual coefficients after major-packet subtraction.

## Shift Variable

Set

$$
h=n-m.
$$

The congruence `n == m mod q` becomes

$$
q\mid h.
$$

The additive beta window contributes a transform weight

$$
\widehat\Omega_{q,N}(h),
$$

which is concentrated at

$$
|h|\lesssim \rho^{-1}.
$$

The dual correlation has schematic form

$$
\sum_{|h|\lesssim\rho^{-1}}
\left(\sum_{\substack{q\le Q_0\\ q\mid h}}w_q(h)\right)
\widehat\Omega_{q,N}(h)
\sum_{X<m,m+h\le2X}
a_{m+h}\overline{a_m}.
$$

## Large-Sieve Positivity Route

The first route is not to estimate shifted prime correlations individually.
Use the duality principle of the large sieve to bound the whole quadratic
form by its operator norm:

$$
\mathcal Q(a)
\le
(X+Q_0^2+\rho^{-1})\sum_n|a_n|^2
$$

with the kernel-weighted overlap cost replacing the crude spacing term when
available.

This route is sufficient if the resulting bound fits
`\mathcal E_tot`.

## Shifted-Correlation Route

If large-sieve positivity is too weak, the exact additional input is a
weighted shifted-correlation estimate:

$$
\sum_{0<|h|\lesssim\rho^{-1}}
\tau_{Q_0}(h)
\widehat\Omega_N(h)
\sum_{X<m,m+h\le2X}
a_{m+h}\overline{a_m}
\ll
\mathcal E_{\mathrm{shift}},
$$

where

$$
\tau_{Q_0}(h)=\#\{q\le Q_0:q\mid h\}.
$$

This is a much stronger arithmetic input. For prime or von Mangoldt
coefficients it is a shifted-prime correlation estimate after major packet
components have been subtracted.

## Diagonal and Coherent Terms

The shift `h=0` is the large-sieve diagonal. It contributes

$$
\sum_n|a_n|^2
$$

times the total local window weight. This must either fit the budget or be
accounted for as part of the Poisson main term.

For `h != 0`, low-conductor coherent correlations belong to the major packet
model. The residual estimate is applied only after those components are
removed.

## Kernel-Weight Role

The kernel transform determines:

1. the shift length `H=rho^{-1}`;
2. the decay of `widehat Omega_N(h)`;
3. the weight of shifts with many small divisors;
4. the distinction between diagonal, resonant, and nonresonant shifts.

Sharper decay of `widehat Omega_N(h)` reduces the shifted-correlation burden.

## Required Inputs

The dual proof needs one of:

1. a kernel-weighted large-sieve operator norm strong enough for the budget;
2. a shifted-prime correlation estimate with divisor weight `tau_{Q0}(h)`;
3. a hybrid approach where large sieve handles generic shifts and explicit
   major-packet subtraction handles resonant shifts.

## Minimal Lemma

> **Dual Shifted-Congruence Bound.**  
> After major-packet subtraction, the kernel-weighted quadratic form over
> `n == m mod q` and `|n-m| <= rho^{-1}` is bounded by the aperture error
> budget, either by the hybrid large-sieve operator norm or by an explicit
> divisor-weighted shifted-correlation estimate for the residual endpoint
> coefficients.

## Result

The dual form exposes the exact arithmetic content of the hybrid large sieve.
If the large-sieve operator norm fits the Poisson budget, no individual
shifted-prime theorem is needed. If it does not fit, the next input is a
kernel-weighted shifted-prime correlation bound with small-divisor weights.
