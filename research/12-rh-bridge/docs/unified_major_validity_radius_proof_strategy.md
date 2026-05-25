# Unified Major Validity Radius Proof Strategy

Date: 2026-05-24

Status: candidate proof strategy for major validity at the unified aperture
scale.

For each relevant kernel peak center `c=a/q`, the required aperture radius is

$$
R_{\mathrm{req}}(c,d,N)
=
\max\left(
{c_0\over L_{\mathrm{crit}}(d,N)},
M_{\Omega}^{-1}
\right).
$$

The Unified Major Aperture Radius Lemma needs

$$
R_{\mathrm{req}}(c,d,N)
\le
\rho_{\mathrm{valid}}(c)
$$

and

$$
R_{\mathrm{req}}(c,d,N)\le c_1Q_0^{-2}.
$$

## Pointwise Major Validity

For an individual packet center, prove

$$
B_X(c+\beta)
=
\operatorname{Major}_{c}(\beta)
+
\operatorname{Err}_{c}(\beta),
\qquad
|\beta|\le R_{\mathrm{req}}.
$$

The radius is valid if

$$
\int_{|\beta|\le R_{\mathrm{req}}}
|\operatorname{Err}_{c}(\beta)|^2
|K_N(c+\beta)|^2\,d\beta
\le
\mathcal E_{c,d,N}.
$$

Using AP-error notation, a sufficient condition is

$$
{E_q(X)^2\over(\log X)^2}
I_N(c,R_{\mathrm{req}})
\le
\mathcal E_{c,d,N}.
$$

## Averaged Major Validity

If pointwise control is too strong, use the budget-weighted averaged form:

$$
\sum_{q\le Q_0}\sum_{(a,q)=1}
\int_{|\beta|\le R_{\mathrm{req}}(a/q,d,N)}
|\operatorname{Err}_{a/q}(\beta)|^2
|K_N(a/q+\beta)|^2\,d\beta
\le
\mathcal E_{\mathrm{tot}}(d,N).
$$

This is the kernel-weighted maximal BDH input at the unified aperture scale.

## Analytic Inputs

The proof can use:

1. **Siegel-Walfisz / PNT in AP** for fixed or polylogarithmic `q`;
2. **Bombieri-Vinogradov / BDH** for averaged packet-center control;
3. **zero-density estimates** for transition moduli or exceptional centers;
4. **major-packet subtraction** for principal and exceptional coherent terms;
5. **kernel-window mass bounds** for `I_N(c,R_req)`.

All inputs are measured against the same budget `E_{c,d,N}` or
`E_tot(d,N)`.

## Exceptional Terms

If a real exceptional character creates a coherent term, it must be included
in `Major_c(beta)`. It cannot remain in `Err_c(beta)`, because the aperture
mass estimate treats residual error as minor.

## Minimal Lemma

> **Unified Major Validity Radius Lemma.**  
> For every relevant kernel peak center and failing dyadic slice, the centered
> endpoint major approximation is valid on
> `|beta| <= R_req(c,d,N)` with kernel-weighted error inside the assigned
> budget, either pointwise by PNT-in-AP/zero-density input or on average by
> a kernel-weighted BDH theorem. The same `R_req` also satisfies rational
> separation `R_req <= c1 Q0^{-2}`.

## Result

The major-validity side has one target: prove the centered endpoint major
approximation at the combined radius required simultaneously by failing
kernel bands and kernel-window mass. A kernel-weighted BDH theorem at
`R_req` closes the averaged route; pointwise zero-density input closes
individual exceptional centers.
