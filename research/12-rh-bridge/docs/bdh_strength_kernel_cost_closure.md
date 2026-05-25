# BDH Strength Versus Kernel Cost Closure

Date: 2026-05-24

Status: candidate strength requirement for closing the budget-weighted BV
radius lemma.

The budget-weighted BV route requires

$$
\mathcal M(\rho)
=
\sum_{q\le Q_0}\sum_{(a,q)=1}
\int_{|\beta|\le\rho}
|\operatorname{Err}_{a/q}(\beta)|^2
|K_N(a/q+\beta)|^2\,d\beta
\le
\mathcal E_{\mathrm{tot}}.
$$

The radius needed by aperture removal is

$$
\rho={c_0\over L_{\mathrm{crit}}(d,N)}.
$$

## Square-Mean AP Input

Let

$$
\mathcal B_{\mathrm{AP}}(X,Q_0)
$$

denote a maximal square-mean AP error bound:

$$
\sum_{q\le Q_0}
\sum_{(a,q)=1}
\sup_{x\le2X}
\left|
\psi(x;q,a)-{x\over\varphi(q)}
\right|^2
\le
\mathcal B_{\mathrm{AP}}(X,Q_0).
$$

A BDH-strength input has the schematic size

$$
\mathcal B_{\mathrm{AP}}(X,Q_0)
\ll
XQ_0(\log X)^C
$$

in the range where the theorem is available.

## Kernel Cost

Define the deterministic window cost

$$
\mathcal K_N(\rho,Q_0)
=
\sup_{q\le Q_0,\ (a,q)=1}
\int_{|\beta|\le\rho}
(1+X|\beta|)^2
|K_N(a/q+\beta)|^2\,d\beta .
$$

The crude transfer from AP square mean to the major-window error gives

$$
\mathcal M(\rho)
\ll
{ \mathcal B_{\mathrm{AP}}(X,Q_0)
\mathcal K_N(\rho,Q_0)
\over
(\log X)^2 }.
$$

Thus a sufficient closure condition is

$$
\mathcal B_{\mathrm{AP}}(X,Q_0)
\mathcal K_N(\rho,Q_0)
\le
(\log X)^2\mathcal E_{\mathrm{tot}}.
$$

With BDH-strength input, this becomes

$$
XQ_0(\log X)^{C-2}
\mathcal K_N(\rho,Q_0)
\le
\mathcal E_{\mathrm{tot}}.
$$

## Weighted Improvement

The crude condition uses the supremum of the kernel cost. A sharper
budget-weighted theorem would prove directly that

$$
\sum_{q\le Q_0}\sum_{(a,q)=1}
\mathcal K_{a,q,N}(\rho)
\sup_{x\le2X}
\left|
\psi(x;q,a)-{x\over\varphi(q)}
\right|^2
\le
\mathcal B_{\mathrm{AP}}^{K}(X,Q_0,N,\rho),
$$

where

$$
\mathcal K_{a,q,N}(\rho)
=
\int_{|\beta|\le\rho}
(1+X|\beta|)^2
|K_N(a/q+\beta)|^2\,d\beta .
$$

Then the closure condition is the sharper inequality

$$
{ \mathcal B_{\mathrm{AP}}^{K}(X,Q_0,N,\rho)
\over
(\log X)^2}
\le
\mathcal E_{\mathrm{tot}}.
$$

This is the preferred form because it does not charge every packet center the
worst kernel window.

## Large-Sieve Inputs

The required mean-value inputs are:

1. a maximal BDH theorem or square-mean BV estimate for AP errors up to
   `Q_0`;
2. a weighted variant with kernel-window weights, or a continuous large-sieve
   estimate over `alpha=a/q+beta`;
3. partial-summation stability for `|beta| <= rho`;
4. exceptional-character terms assigned to the major packet model.

## Minimal Strength Lemma

> **Kernel-Weighted BDH Strength Lemma.**  
> At the aperture radius `rho=c0/L_crit(d,N)`, the AP square-mean input and
> deterministic kernel-window cost satisfy
> \[
> { \mathcal B_{\mathrm{AP}}^{K}(X,Q_0,N,\rho)
> \over(\log X)^2}
> \le
> \mathcal E_{\mathrm{tot}}(d,N),
> \]
> or, in the crude supremum form,
> \[
> XQ_0(\log X)^{C-2}\mathcal K_N(\rho,Q_0)
> \le
> \mathcal E_{\mathrm{tot}}(d,N).
> \]

## Result

The averaged major-radius route closes exactly when the square-mean AP error,
weighted by the kernel window at `rho=c0/L_crit`, fits the packet error
budget. The cleanest input is a kernel-weighted BDH theorem; the fallback
sufficient input is standard BDH multiplied by the worst deterministic kernel
cost.
