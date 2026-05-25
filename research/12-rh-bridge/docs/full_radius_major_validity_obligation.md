# Full-Radius Major Validity Obligation

Date: 2026-05-24

Status: consolidated theorem obligation for closing the literal
support-removal route.

The literal support-removal route now depends on one analytic input:

$$
\text{major validity at } R_{\mathrm{all}}.
$$

Here

$$
R_{\mathrm{all}}
=
\max\left(
{c_0\over L_{\mathrm{crit}}(d,N)},
M_{\Omega}^{-1},
R_{\mathrm{LS}}
\right).
$$

## Required Estimate

For every relevant center `c=a/q`, prove either pointwise or on average that

$$
\int_{|\beta|\le R_{\mathrm{all}}}
|\operatorname{Err}_{c}(\beta)|^2
|K_N(c+\beta)|^2\,d\beta
\le
\mathcal E_{c,d,N}.
$$

The averaged version is

$$
\sum_{q\le Q_0}\sum_{(a,q)=1}
\int_{|\beta|\le R_{\mathrm{all}}(a/q,d,N)}
|\operatorname{Err}_{a/q}(\beta)|^2
|K_N(a/q+\beta)|^2\,d\beta
\le
\mathcal E_{\mathrm{maj}}(d,N).
$$

Together with

$$
R_{\mathrm{all}}\le c_1Q_0^{-2},
$$

this closes the literal support-removal branch of the Full Unified Major
Aperture Lemma.

## Route 1: Pointwise AP / Zero-Density

Use pointwise estimates for

$$
\psi(x;q,a)-{x\over\varphi(q)}
$$

to prove

$$
{E_q(X)^2\over(\log X)^2}
I_N(a/q,R_{\mathrm{all}})
\le
\mathcal E_{a,q,N}.
$$

This route is appropriate for fixed or small `q`, and for exceptional centers
handled by zero-density estimates. Coherent exceptional terms must be included
in `Major_{a/q}` rather than left in the error.

## Route 2: Kernel-Weighted BDH

Prove the averaged major-window square mean directly:

$$
\mathcal M(R_{\mathrm{all}})
\le
\mathcal E_{\mathrm{maj}}(d,N).
$$

This is the kernel-weighted maximal BDH theorem at the full unified radius.
It can be attacked by character decomposition plus weighted hybrid large
sieve, or by the direct continuous-frequency large sieve.

## Route 3: Direct Continuous-Frequency Large Sieve

Use the measure concentration bound:

$$
(X\mathfrak C_{\mu}(1/X)+\mu([0,1]))\mathcal A_2
\le
(\log X)^2\mathcal E_{\mathrm{maj}}.
$$

After core removal this is implied by

$$
B_{\mathrm{ov}}
(\rho_{\mathrm{core}}^{-2}+\rho_{\mathrm{core}}^{-1})
\mathcal A_2
\le
(\log X)^2\mathcal E_{\mathrm{maj}},
$$

which is exactly why `R_LS` is included in `R_all`.

## Combined Budget Contract

The budgets must be assigned so that:

1. `E_maj` pays for major-window square-mean error;
2. `E_shift` pays for the shift-kernel threshold branch;
3. `M_Omega=E_shift/(S A_min)` is compatible with `E_maj` through `R_LS`;
4. all three demands are included in `R_all`;
5. the same `R_all` remains within `rho_valid` and rational separation.

## Minimal Lemma

> **Full-Radius Major Validity Lemma.**  
> At the radius
> \[
> R_{\mathrm{all}}
> =
> \max(c_0/L_{\mathrm{crit}},M_{\Omega}^{-1},R_{\mathrm{LS}}),
> \]
> the centered endpoint major approximation has kernel-weighted error inside
> the assigned budget, pointwise or on average, and
> `R_all <= c1 Q0^{-2}`.

## Result

This is the literal support-removal theorem obligation. Proving it closes the
major-aperture side of the projected reciprocal-congruence route. If it fails,
the only remaining path is the packet-frame alternative that captures band
energy, kernel mass, and measure concentration without literal support
apertures.
