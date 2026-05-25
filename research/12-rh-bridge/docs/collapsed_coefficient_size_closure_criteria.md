# Collapsed Coefficient Size Closure Criteria

Date: 2026-05-24

Status: conditional closure criteria for the spectral large-sieve bottleneck.

The Collapsed Coefficient Size Condition asks for

$$
\bigl((R_{\mathrm{spec}}^2+M)\|C\|_2^2\bigr)^{1/2}
\bigl((R_{\mathrm{spec}}^2+K)\|D\|_2^2\bigr)^{1/2}
\le
\mathcal P_{U,N}.
$$

This note records the explicit sufficient conditions for the projected
reciprocal-congruence coefficients.

## Dyadic Parameters

Fix a common-divisor slice `d` and set

$$
U\asymp A/d.
$$

Let:

$$
H_d=\text{dual support from completing }n',
$$

$$
T_d=\text{effective support of the kernel variable }t,
$$

$$
K_d=\text{dual support from completing the }v\text{-interval}.
$$

After collapsing

$$
m=-ht,
$$

the effective support of `C_m` satisfies

$$
M_d\le H_dT_d.
$$

## Norm Bounds Already Available

Cauchy and divisor multiplicity give

$$
\|C\|_2^2
\ll
(\log X)^C
\sum_{h,t}|A_{h,t}|^2.
$$

Write

$$
E_A(d,N)=\sum_{h,t}|A_{h,t}|^2.
$$

Plancherel for the completed `v`-interval gives

$$
\|D\|_2^2
\ll
U E_v(d),
$$

where

$$
E_v(d)=\sum_{v\sim U}|c_v|^2.
$$

These two estimates are unconditional bookkeeping once the completion weights
are fixed and smoothed.

## Explicit Closure Inequality

Substituting the available norm bounds into the spectral condition gives the
sufficient inequality

$$
\Bigl((R_{\mathrm{spec}}^2+H_dT_d)(\log X)^C E_A(d,N)\Bigr)^{1/2}
\Bigl((R_{\mathrm{spec}}^2+K_d)U E_v(d)\Bigr)^{1/2}
\le
\mathcal P_{d,N}.
$$

Equivalently,

$$
(R_{\mathrm{spec}}^2+H_dT_d)
(R_{\mathrm{spec}}^2+K_d)
U E_A(d,N)E_v(d)
\ll
(\log X)^{-C}
\mathcal P_{d,N}^2 .
$$

This is the exact size test for the spectral Kloosterman branch at the
dyadic `d`-slice and kernel band.

## Bessel-Range Requirement

The spectral parameter `R_spec` is determined by the Bessel transform at

$$
{4\pi\sqrt{|mk|}\over u}.
$$

Since

$$
|m|\le H_dT_d,\qquad |k|\le K_d,\qquad u\asymp U,
$$

the transform must satisfy

$$
R_{\mathrm{spec}}^2
\lesssim
\mathcal R(U,H_d,T_d,K_d)^2
$$

with

$$
\mathcal R(U,H_d,T_d,K_d)
$$

small enough for the closure inequality above. If the transition range
`sqrt(|mk|) approx U` forces `R_spec` beyond this budget, the spectral
large-sieve route needs additional cancellation in `C_m`, `D_k`, or the
kernel-band sum.

## What Would Close with Current Bookkeeping

The current bookkeeping closes the spectral branch under these three
conditions:

1. `E_A(d,N)` has the kernel normalization predicted by the Poisson allowance;
2. `E_v(d)` is divisor-bounded in the Type II coefficient norm;
3. the Bessel transform keeps `R_spec` in the range allowed by the explicit
   closure inequality.

No extra cancellation from the divisor collapse is needed under these
conditions. The collapse contributes only a divisor-power loss.

## If the Inequality Fails

Failure of the explicit closure inequality identifies the next required
input. There are only three possible sources of additional saving:

1. **product-collapse cancellation:** improve
   `||C||_2^2 << log^C E_A` by using cancellation among representations
   `m=ht`;
2. **slope-completion cancellation:** improve the Plancherel bound for `D_k`
   using oscillation in the projected slope coefficients;
3. **kernel-band cancellation:** sum over kernel bands before taking absolute
   values, using oscillation of `W_N(dt)` and the rational phase.

These are additional analytic obligations. They are not consequences of the
large sieve alone.

## Minimal Remaining Estimate

The spectral route therefore needs the following quantitative input.

> **Completion Energy Bound.**  
> For every dyadic `d`-slice and kernel band, the completion energies
> `E_A(d,N)` and `E_v(d)`, together with the Bessel-selected range
> `R_spec`, satisfy
> \[
> ((R_{\mathrm{spec}}^2+H_dT_d)(\log X)^C E_A(d,N))^{1/2}
> ((R_{\mathrm{spec}}^2+K_d)U E_v(d))^{1/2}
> \le \mathcal P_{d,N}.
> \]

## Result

The coefficient-size bottleneck has been reduced to a concrete completion
energy inequality. Cauchy, divisor multiplicity, and Plancherel supply the
structural bounds; the remaining work is to verify that the kernel
normalization and Bessel spectral range place those bounds inside the
Poisson allowance.
