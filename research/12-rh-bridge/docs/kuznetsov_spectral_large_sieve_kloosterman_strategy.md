# Kuznetsov Spectral Large-Sieve Strategy

Date: 2026-05-24

Status: candidate strategy for estimating the completed Kloosterman average
created by the reciprocal-congruence route.

After completion, the Kloosterman branch contains sums

$$
S(-ht,k;u)
=
\sum_{v\bmod u}^{*}
e\!\left({-ht\overline v+kv\over u}\right),
$$

with `u` in a balanced dyadic range and with kernel weight in `t`. The next
task is to put these sums into a trace-formula or spectral large-sieve form.

## Collapse the Product Argument

Set

$$
m=-ht.
$$

The completed contribution can be grouped as

$$
\sum_{u\sim U}
\sum_{m,k}
C_m D_k\,S(m,k;u)\,\Phi_{U,N,q}(m,k,u),
$$

where

$$
C_m=\sum_{ht=-m} A_{h,t}
$$

absorbs the completion coefficients and the kernel factor in `t`. The divisor
multiplicity in the collapse is acceptable only if the `L^2` size of `C_m`
remains within the Poisson allowance after summing over dyadic slices.

This collapse is the first concrete spectral bookkeeping requirement.

## Trace-Formula Shape

After inserting the completion normalizations, the desired shape is

$$
\sum_{u}
{1\over u}
\Phi\!\left({u\over U}\right)
S(m,k;u),
$$

summed against coefficient sequences `C_m` and `D_k`. Kuznetsov then converts
the modulus average into spectral sums involving Fourier coefficients of
automorphic forms, plus the Eisenstein spectrum.

The sign of `mk` must be separated:

1. `mk > 0` uses the same-sign Kuznetsov kernel;
2. `mk < 0` uses the opposite-sign kernel;
3. `m=0` or `k=0` is not part of the Kloosterman estimate and belongs to the
   major projection.

## Spectral Large-Sieve Input

The needed analytic estimate is a spectral large-sieve bound for the bilinear
spectral sums produced by Kuznetsov:

$$
\sum_{\mathrm{spec}}
\left|
\sum_m C_m \rho_j(m)
\right|
\left|
\sum_k D_k \rho_j(k)
\right|
\mathcal W_j
\ll
\mathcal P_{U,N}.
$$

By Cauchy, this reduces to two spectral large-sieve estimates for `C_m` and
`D_k`, provided the Bessel transforms `W_j` stay in the admissible range.

The required input is therefore:

$$
\sum_{\mathrm{spec}}
\left|\sum_m C_m\rho_j(m)\right|^2\mathcal W_j
\ll
\mathcal L_C,
\qquad
\sum_{\mathrm{spec}}
\left|\sum_k D_k\rho_j(k)\right|^2\mathcal W_j
\ll
\mathcal L_D,
$$

with

$$
(\mathcal L_C\mathcal L_D)^{1/2}
\le \mathcal P_{U,N}.
$$

## Kernel-Weight Constraints

The kernel weight enters through `C_m` and through the modulus weight
`Phi_{U,N,q}`. To use Kuznetsov cleanly, the proof needs:

1. smooth dyadic weights in `u`;
2. controlled Bessel transforms after the substitution
   `4 pi sqrt(|mk|)/u`;
3. summability over kernel bands;
4. no reintroduction of the removed low-denominator packets through the
   smooth partition.

Sharp cutoff errors must be inside the Poisson allowance, or the interval
weights must be smoothed before completion.

## Major-Exclusion Interface

The spectral estimate applies only to the projected part. The projector must
remove:

1. `m=0`, equivalent to `h=0` or `t=0`;
2. `k=0` terms not covered by the selected spectral input;
3. residue classes where `m` or `k` is zero modulo a large common divisor of
   `u`;
4. low-conductor terms inherited from `q_1=q/(d,q)`;
5. exact product diagonal contributions assigned to the Poisson main term.

After this removal, the Kloosterman average has no remaining Ramanujan-sum or
residue-mean component.

## Minimal Spectral Input

The spectral route closes the Kloosterman branch if the following estimate is
available.

> **Projected Kuznetsov Large-Sieve Bound.**  
> For the collapsed coefficient sequences `C_m` and `D_k` arising from
> additive completion of the reciprocal congruence family, the Kuznetsov
> transform of the projected Kloosterman average over `u sim U` is bounded by
> the assigned Poisson allowance after summing over signs, dyadic `d`-slices,
> and kernel bands.

## Result

The completed Kloosterman average has a standard spectral shape once the
product argument `m=-ht` is collapsed. The next exact quantity to control is
the `L^2` size of the collapsed coefficient sequence `C_m` together with the
spectral large-sieve cost of pairing it against the completed slope sequence
`D_k`.
