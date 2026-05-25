# Literal Radius Support-Removal Verification

Date: 2026-05-24

Status: support-removal verification strategy for the Full Unified Major
Aperture Lemma.

The full literal route needs

$$
R_{\mathrm{all}}(c,d,N)
\le
\min(\rho_{\mathrm{valid}}(c),c_1Q_0^{-2})
$$

for every relevant center `c`. This note records the major-arc inputs and
budgets needed to prove that inequality.

## Complete Radius

Recall

$$
R_{\mathrm{all}}
=
\max\left(
{c_0\over L_{\mathrm{crit}}(d,N)},
M_{\Omega}^{-1},
R_{\mathrm{LS}}
\right).
$$

This single radius removes:

1. failing high-`L` band energy;
2. kernel-core mass in the shift-kernel threshold;
3. direct large-sieve measure concentration.

## Rational Separation

The support-removal route first requires

$$
R_{\mathrm{all}}(c,d,N)
\le
c_1Q_0^{-2}.
$$

This is deterministic once `Q_0` and the budgets defining `R_all` are fixed.

If it fails, support apertures around low-conductor centers overlap too much,
and the proof must use the packet-frame route.

## Major Validity Budget

For `c=a/q`, the major approximation must satisfy

$$
B_X(c+\beta)
=
\operatorname{Major}_{c}(\beta)
+
\operatorname{Err}_{c}(\beta)
$$

for

$$
|\beta|\le R_{\mathrm{all}}.
$$

The required pointwise packet budget is

$$
\int_{|\beta|\le R_{\mathrm{all}}}
|\operatorname{Err}_{c}(\beta)|^2
|K_N(c+\beta)|^2\,d\beta
\le
\mathcal E_{c,d,N}.
$$

A sufficient AP-error condition is

$$
{E_q(X)^2\over(\log X)^2}
I_N(c,R_{\mathrm{all}})
\le
\mathcal E_{c,d,N}.
$$

## Averaged BDH Budget

The averaged support-removal route needs

$$
\sum_{q\le Q_0}\sum_{(a,q)=1}
\int_{|\beta|\le R_{\mathrm{all}}(a/q,d,N)}
|\operatorname{Err}_{a/q}(\beta)|^2
|K_N(a/q+\beta)|^2\,d\beta
\le
\mathcal E_{\mathrm{maj}}(d,N).
$$

This is exactly the unified-scale kernel-weighted BDH input.

## Inputs by Range

**Small fixed or polylogarithmic moduli.**
Use Siegel-Walfisz or PNT in AP to prove the pointwise budget.

**Averaged moduli up to `Q_0`.**
Use kernel-weighted BDH/Bombieri-Vinogradov at radius `R_all`.

**Exceptional or transition centers.**
Use zero-density estimates, with coherent exceptional terms included in the
major packet model.

## Minimal Lemma

> **Literal Support-Removal Radius Lemma.**  
> For every relevant center and failing dyadic slice,
> \[
> R_{\mathrm{all}}(c,d,N)\le c_1Q_0^{-2}
> \]
> and the centered endpoint major approximation has kernel-weighted error
> inside its assigned budget on `|beta| <= R_all`, pointwise or on average.

## Result

The support-removal route closes the Full Unified Major Aperture Lemma if the
complete radius `R_all` fits inside rational separation and the major
approximation is valid on that same radius with the assigned kernel-weighted
error budget.
