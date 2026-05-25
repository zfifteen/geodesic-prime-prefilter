# Collapsed Coefficient Spectral Size Control

Date: 2026-05-24

Status: candidate size ledger for the Kuznetsov/spectral large-sieve route.

The spectral route reduces the completed Kloosterman branch to coefficient
sequences

$$
C_m=\sum_{ht=-m} A_{h,t},
\qquad
D_k,
$$

paired through sums `S(m,k;u)` over moduli `u sim U`. The next task is to
control the spectral large-sieve cost of `C_m` and `D_k` after the
major-exclusion projector and kernel weights have been applied.

## Collapsed Product Coefficient

The product collapse `m=-ht` creates divisor multiplicity. By Cauchy,

$$
|C_m|^2
\le
\tau(|m|)
\sum_{ht=-m}|A_{h,t}|^2.
$$

Therefore

$$
\sum_m |C_m|^2
\ll
(\log X)^C
\sum_{h,t}|A_{h,t}|^2
$$

for divisor-bounded ranges. This is acceptable if the uncollapsed completion
coefficients `A_{h,t}` already carry the kernel-band normalization assigned
to the `d`-slice.

The collapse itself costs only divisor powers. It does not create a new main
term unless `h=0` or `t=0`, and those cases belong to the major projection.

## Completed Slope Coefficient

The coefficient `D_k` comes from completing the finite `v`-interval and slope
weight. With smooth weights, Plancherel gives a bound of the form

$$
\sum_k |D_k|^2
\ll
U\,\sum_{v\sim U}|c_v|^2
$$

up to harmless smooth-weight factors. If the `v`-weight is not smoothed before
completion, boundary frequencies must be counted inside the Poisson allowance.

Thus the two coefficient norms required by the spectral large sieve are:

$$
\|C\|_2^2
\ll
(\log X)^C\|A\|_2^2,
\qquad
\|D\|_2^2
\ll
U\|c\|_2^2.
$$

## Spectral Large-Sieve Cost

Let `R_spec` denote the effective spectral parameter range selected by the
Bessel transform of the modulus weight. A usable spectral large-sieve bound
has the schematic form

$$
\sum_{\mathrm{spec}(R_{\mathrm{spec}})}
\left|\sum_m C_m\rho_j(m)\right|^2
\ll
(R_{\mathrm{spec}}^2+M)\|C\|_2^2,
$$

and similarly

$$
\sum_{\mathrm{spec}(R_{\mathrm{spec}})}
\left|\sum_k D_k\rho_j(k)\right|^2
\ll
(R_{\mathrm{spec}}^2+K)\|D\|_2^2.
$$

Here `M` and `K` are the effective supports of `C_m` and `D_k`. The
Kuznetsov branch closes for a dyadic slice if

$$
\bigl((R_{\mathrm{spec}}^2+M)\|C\|_2^2\bigr)^{1/2}
\bigl((R_{\mathrm{spec}}^2+K)\|D\|_2^2\bigr)^{1/2}
\le
\mathcal P_{U,N}.
$$

This inequality is the concrete spectral size condition.

## Bessel-Transform Constraints

The modulus average has the trace-formula scale

$$
{4\pi\sqrt{|mk|}\over u}.
$$

The Bessel transform must satisfy four constraints:

1. smooth dyadic `u` weights so the transform decays rapidly outside its
   spectral window;
2. separate treatment of same-sign and opposite-sign `mk`;
3. uniform control through the transition range
   `sqrt(|mk|) approx U`;
4. summability over dyadic `d`-slices and kernel bands.

If the transform creates a spectral range `R_spec` too large for the
large-sieve inequality above, the Kloosterman route does not close without an
additional cancellation input in the coefficients.

## Major-Projection Requirements

The coefficient norms above apply only after removal of:

1. `m=0`, hence `h=0` or `t=0`;
2. `k=0` pieces not covered by the spectral estimate;
3. residue-class means with conductor `q_1=q/(d,q)`;
4. low-denominator kernel packets;
5. exact product diagonals.

Once these are removed, the remaining coefficients have no forced local mean,
and the spectral large sieve is estimating genuine oscillation.

## Minimal Coefficient Condition

The spectral branch reduces to the following coefficient condition.

> **Collapsed Coefficient Size Condition.**  
> For every dyadic `d`-slice and kernel band, the collapsed product
> coefficients `C_m` and completed slope coefficients `D_k` satisfy the
> spectral large-sieve inequality
> \[
> ((R_{\mathrm{spec}}^2+M)\|C\|_2^2)^{1/2}
> ((R_{\mathrm{spec}}^2+K)\|D\|_2^2)^{1/2}
> \le \mathcal P_{U,N},
> \]
> after the major projector removes zero-frequency, residue-mean, and
> diagonal components.

## Result

The Kloosterman/spectral route now has a quantitative local bottleneck. The
collapse `m=-ht` costs only divisor powers by Cauchy, and the completed slope
sequence is controlled by Plancherel, but the Bessel-selected spectral range
must be small enough that the spectral large-sieve cost remains within the
Poisson allowance.
