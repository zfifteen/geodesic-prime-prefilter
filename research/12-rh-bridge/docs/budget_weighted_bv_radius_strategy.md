# Budget-Weighted Bombieri-Vinogradov Radius Strategy

Date: 2026-05-24

Status: candidate averaged route for proving major validity radii at the
aperture scale required by failing kernel bands.

For failing dyadic slices, set

$$
\rho_{d,N}={c_0\over L_{\mathrm{crit}}(d,N)}.
$$

The averaged major-radius target is

$$
\sum_{q\le Q_0}\sum_{(a,q)=1}
{E_q(X)^2\over(\log X)^2}
I_N(a/q,\rho_{d,N})
\le
\sum_{q\le Q_0}\sum_{(a,q)=1}
\mathcal E_{a,q,N}.
$$

This is the square-mean form needed to guarantee the radius on average over
low-conductor packet centers.

## Direct Budget-Weighted Form

A cleaner formulation avoids the supremum `E_q(X)` and estimates the actual
major-window error:

$$
\mathcal M(\rho)
=
\sum_{q\le Q_0}\sum_{(a,q)=1}
\int_{|\beta|\le\rho}
|\operatorname{Err}_{a/q}(\beta)|^2
|K_N(a/q+\beta)|^2\,d\beta .
$$

The required bound is

$$
\mathcal M(\rho_{d,N})
\le
\mathcal E_{\mathrm{tot}}(d,N),
$$

where

$$
\mathcal E_{\mathrm{tot}}(d,N)
=
\sum_{q\le Q_0}\sum_{(a,q)=1}\mathcal E_{a,q,N}.
$$

This is the most natural budget-weighted BV statement for the aperture
argument.

## Mean-Square AP Input

The underlying arithmetic input is a Barban-Davenport-Halberstam or
square-mean Bombieri-Vinogradov estimate:

$$
\sum_{q\le Q_0}
\sum_{(a,q)=1}
\left|
\psi(x;q,a)-{x\over\varphi(q)}
\right|^2
\ll
\mathcal B_{\mathrm{AP}}(X,Q_0)
$$

uniformly or maximally in `x <= 2X`.

After partial summation in `beta`, this supplies

$$
\mathcal M(\rho)
\ll
{1\over(\log X)^2}
\mathcal B_{\mathrm{AP}}(X,Q_0)
\cdot
\mathcal K_N(\rho,Q_0),
$$

where `K_N(rho,Q0)` is the deterministic kernel-window cost.

## Kernel-Window Cost

The deterministic factor is

$$
\mathcal K_N(\rho,Q_0)
=
\sup_{q\le Q_0}
\sum_{(a,q)=1}
\int_{|\beta|\le\rho}
(1+X|\beta|)^2
|K_N(a/q+\beta)|^2\,d\beta .
$$

Using

$$
|K_N(\alpha)|\ll \min(N,\|\alpha\|^{-1}),
$$

this factor is explicitly estimable once `rho`, `Q_0`, and the packet centers
are fixed.

## Large-Sieve Interpretation

Equivalently, estimate the major-window mean square directly by a large sieve
over the points

$$
\alpha={a\over q}+\beta,
\qquad
q\le Q_0,\quad |\beta|\le\rho.
$$

The spacing of these windows is controlled by rational separation
`Q_0^{-2}`. The aperture condition already requires

$$
\rho\le cQ_0^{-2},
$$

so the windows are disjoint or have bounded overlap. This makes a
continuous large-sieve estimate compatible with the budget-weighted major
window.

## Required Strength

The averaged BV route closes the aperture radius if

$$
{1\over(\log X)^2}
\mathcal B_{\mathrm{AP}}(X,Q_0)
\mathcal K_N(\rho_{d,N},Q_0)
\le
\mathcal E_{\mathrm{tot}}(d,N)
$$

for every failing dyadic `d`-slice.

If this holds only after excluding a small exceptional set of packet centers,
those exceptional centers must be handled by zero-density input or assigned
to explicit major packet components.

## Minimal Lemma

> **Budget-Weighted BV Radius Lemma.**  
> For each failing aperture scale `rho_{d,N}=c0/L_crit(d,N)`,
> \[
> \sum_{q\le Q_0}\sum_{(a,q)=1}
> \int_{|\beta|\le\rho_{d,N}}
> |\operatorname{Err}_{a/q}(\beta)|^2
> |K_N(a/q+\beta)|^2\,d\beta
> \le
> \mathcal E_{\mathrm{tot}}(d,N).
> \]
> The proof may use a maximal square-mean AP theorem, a continuous large
> sieve over the major windows, and explicit kernel-window bounds.

## Result

The averaged route to `rho_valid` is a budget-weighted mean-square theorem
for major-window errors. Its exact strength is measured by the product of the
AP square-mean bound and the deterministic kernel-window cost at
`rho=c0/L_crit(d,N)`.
