# Full-Radius BDH Direct Proof Plan

Date: 2026-05-24

Status: concrete proof plan for the kernel-weighted maximal BDH validity at
the full unified radius.

The selected route is the **direct continuous-frequency large sieve**. The
character-weighted and dual shifted-congruence routes remain backups, but the
direct route now has the cleanest closure condition.

## Route Choice

Use the residual endpoint exponential sum

$$
A^{\perp}(\alpha)=\sum_{X<n\le2X}a_n e(\alpha n)
$$

after major-packet subtraction, and estimate it over the weighted measure on

$$
\alpha={a\over q}+\beta,
\qquad
|\beta|\le R_{\mathrm{all}}.
$$

## Direct Large-Sieve Step

The continuous large sieve gives

$$
\int |A^{\perp}(\alpha)|^2\,d\mu(\alpha)
\le
\left(
X\mathfrak C_{\mu}(1/X)+\mu([0,1])
\right)\mathcal A_2.
$$

After core removal to radius `R_all`, the measure concentration bound gives

$$
X\mathfrak C_{\mu}(1/X)+\mu([0,1])
\ll
B_{\mathrm{ov}}(R_{\mathrm{all}}^{-2}+R_{\mathrm{all}}^{-1}).
$$

## Built-In Budget Closure

By definition, `R_all` contains

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

Therefore

$$
B_{\mathrm{ov}}(R_{\mathrm{all}}^{-2}+R_{\mathrm{all}}^{-1})\mathcal A_2
\le
(\log X)^2\mathcal E_{\mathrm{maj}}
$$

up to fixed constants. This proves the required BDH-strength estimate once
the aperture support removal is valid at radius `R_all`.

## Remaining Quantitative Gaps

The direct proof plan has four remaining quantitative inputs.

1. **Residual coefficient energy.**
   Prove or assign
   $$
   \mathcal A_2=\sum|a_n|^2
   $$
   after major-packet subtraction.

2. **Budget allocation.**
   Fix `E_maj`, `E_shift`, `M_Omega`, and `L_crit` consistently.

3. **Major validity radius.**
   Prove
   $$
   R_{\mathrm{all}}\le \rho_{\mathrm{valid}}(c)
   $$
   by pointwise AP/zero-density input or averaged kernel-weighted BDH input
   outside this direct large-sieve operator step.

4. **Rational separation.**
   Verify
   $$
   R_{\mathrm{all}}\le c_1Q_0^{-2}.
   $$

## Literal Support Closure

If the four inputs hold, the direct route proves

$$
\sum_{q\le Q_0}\sum_{(a,q)=1}
\int_{|\beta|\le R_{\mathrm{all}}}
|\operatorname{Err}_{a/q}(\beta)|^2
|K_N(a/q+\beta)|^2\,d\beta
\le
\mathcal E_{\mathrm{maj}}.
$$

This closes the literal support-removal branch of the Full Unified Major
Aperture Lemma.

## Minimal Lemma

> **Direct Full-Radius BDH Lemma.**  
> After major-packet subtraction, if `A_2`, the major budgets, major validity
> radius, and rational separation satisfy the four inputs above, then the
> direct continuous-frequency large sieve proves kernel-weighted maximal BDH
> validity at `R_all`.

## Result

The chosen proof path is direct continuous-frequency large sieve. The
large-sieve budget itself is closed by including `R_LS` in `R_all`; the
remaining work is to verify the residual coefficient energy, budget
assignment, major validity radius, and rational separation.
