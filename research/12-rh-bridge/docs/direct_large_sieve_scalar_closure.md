# Direct Large-Sieve Scalar Closure

Date: 2026-05-24

Status: scalar closure test for the direct continuous-frequency large-sieve
route after kernel-measure concentration bounds.

The direct route closes if

$$
\left(
X\mathfrak C_{\mu}(1/X)+\mu([0,1])
\right)
\mathcal A_2
\le
(\log X)^2\mathcal E_{\mathrm{maj}}.
$$

After core removal to radius `rho_core`, the concentration lemma gives

$$
X\mathfrak C_{\mu}(1/X)+\mu([0,1])
\ll
B_{\mathrm{ov}}
\left(
\rho_{\mathrm{core}}^{-2}
+
\rho_{\mathrm{core}}^{-1}
\right).
$$

## Scalar Closure Condition

A sufficient condition is

$$
B_{\mathrm{ov}}
\left(
\rho_{\mathrm{core}}^{-2}
+
\rho_{\mathrm{core}}^{-1}
\right)
\mathcal A_2
\le
(\log X)^2\mathcal E_{\mathrm{maj}}.
$$

The quadratic term dominates for small `rho_core`, so it is enough to require

$$
\rho_{\mathrm{core}}
\ge
\left(
{B_{\mathrm{ov}}\mathcal A_2
\over
(\log X)^2\mathcal E_{\mathrm{maj}}}
\right)^{1/2}.
$$

The linear tail also requires

$$
\rho_{\mathrm{core}}
\ge
{B_{\mathrm{ov}}\mathcal A_2
\over
(\log X)^2\mathcal E_{\mathrm{maj}}}.
$$

## Combined Core Radius Demand

The direct large-sieve route adds a new core-radius demand to the previous
aperture requirements. Define

$$
R_{\mathrm{LS}}
=
\max\left(
\left(
{B_{\mathrm{ov}}\mathcal A_2
\over
(\log X)^2\mathcal E_{\mathrm{maj}}}
\right)^{1/2},
{B_{\mathrm{ov}}\mathcal A_2
\over
(\log X)^2\mathcal E_{\mathrm{maj}}}
\right).
$$

The major projector must remove the kernel core at least to radius

$$
\rho_{\mathrm{core}}\ge R_{\mathrm{LS}}.
$$

## Unified Radius Update

The full literal aperture route now requires

$$
R_{\mathrm{all}}
=
\max\left(
{c_0\over L_{\mathrm{crit}}(d,N)},
M_{\Omega}^{-1},
R_{\mathrm{LS}}
\right)
\le
\min(\rho_{\mathrm{valid}}(c),c_1Q_0^{-2}).
$$

This single inequality closes:

1. high-`L` band removal;
2. shift-kernel threshold mass control;
3. direct continuous-frequency large-sieve measure control.

## Required Inputs

The scalar closure needs:

1. residual coefficient energy `A_2`;
2. major budget `E_maj`;
3. bounded overlap `B_ov`;
4. major validity radius `rho_valid(c)`;
5. the previous `L_crit` and `M_Omega` aperture demands.

## Minimal Lemma

> **Direct Large-Sieve Scalar Closure Lemma.**  
> If
> \[
> R_{\mathrm{all}}
> \le
> \min(\rho_{\mathrm{valid}}(c),c_1Q_0^{-2})
> \]
> for every relevant packet center, then the direct continuous-frequency
> large-sieve bound satisfies
> \[
> (X\mathfrak C_{\mu}(1/X)+\mu([0,1]))\mathcal A_2
> \le
> (\log X)^2\mathcal E_{\mathrm{maj}}.
> \]

## Result

After measure concentration, the direct additive large-sieve branch is a
single aperture-radius inequality. The major projector must remove the kernel
core far enough to satisfy the large-sieve operator budget in addition to the
earlier band-energy and shift-kernel mass budgets.
