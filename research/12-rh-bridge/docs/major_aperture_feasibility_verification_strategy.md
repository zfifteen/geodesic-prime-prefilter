# Major-Aperture Feasibility Verification Strategy

Date: 2026-05-24

Status: verification strategy for the Major Aperture Feasibility Lemma.

The feasibility lemma asks for either the literal radius inequality

$$
{c_0\over L_{\mathrm{crit}}(d,N)}
\le
\min(c_1Q_0^{-2},\rho_{\mathrm{valid}}(c)),
$$

or an orthogonal major-packet frame estimate replacing support removal.

## Literal Radius Verification

For each low-conductor center

$$
c={a\over q},\qquad q\le Q_0,
$$

perform three checks.

### 1. Compute the Failing Band Threshold

Determine `L_crit(d,N)` from

$$
d^{-1}L_{\mathrm{crit}}^3\mathcal B_d
\le
{ \mathcal P_{d,N,L_{\mathrm{crit}}}^2
\over
(R_{\mathrm{spec}}^2+H_dT_d)
(R_{\mathrm{spec}}^2+K_d)U E_v(d)}
(\log X)^{-C}.
$$

This identifies the high-`L` bands that require major-aperture removal.

### 2. Fix the Separation Radius

Distinct centers with denominators at most `Q_0` are separated at scale
`Q_0^{-2}`. Set

$$
\rho_{\mathrm{sep}}=c_1Q_0^{-2}.
$$

This is the largest radius allowed by disjointness of low-conductor packets.

### 3. Prove the Major Validity Radius

For each `c=a/q`, prove a major approximation for the centered endpoint
Fourier piece on

$$
|\alpha-c|\le \rho_{\mathrm{valid}}(c),
$$

with error inside the Poisson allowance after kernel weighting. Schematically,

$$
\widehat b_X(c+\beta)
=
\operatorname{Major}_c(\beta)
+O(\operatorname{Err}_c(\beta)),
\qquad
|\beta|\le \rho_{\mathrm{valid}}(c),
$$

and

$$
\int_{|\beta|\le\rho_{\mathrm{valid}}(c)}
|\operatorname{Err}_c(\beta)|^2|K_N(c+\beta)|^2\,d\beta
\le
\text{assigned error budget}.
$$

Then literal aperture removal is verified if

$$
{c_0\over L_{\mathrm{crit}}(d,N)}
\le
\min(\rho_{\mathrm{sep}},\rho_{\mathrm{valid}}(c)).
$$

## Frame Verification Alternative

If the literal interval is empty, define normalized packet model functions
`phi_c` for the coherent major components. The needed lower frame estimate is

$$
\sum_{c:q(c)\le Q_0}
|\langle w_{N,L},\phi_c\rangle|^2
\ge
(1-\Delta_L)\|w_{N,L}\|_2^2.
$$

This route needs:

1. explicit packet model functions `phi_c`;
2. a Gram matrix estimate showing bounded packet overlap;
3. a lower frame bound on high-`L` kernel bands;
4. major approximation validity for projected packet components;
5. summability of the residual `Delta_L` in the Completion Energy Bound.

The frame route proves energy capture without requiring literal support
containment.

## Current Verification Status

The current notes do not yet specify:

1. the numerical or asymptotic choice of `Q_0`;
2. the major approximation validity radius `rho_valid(c)`;
3. the completed coefficient parameters determining `L_crit(d,N)`;
4. the packet model functions `phi_c`.

Therefore the Major Aperture Feasibility Lemma is not yet verified. The next
analytic input is the major-arc validity radius, or else the packet-frame
lower bound.

## Minimal Next Lemma

> **Major Validity Radius Lemma.**  
> For every low-conductor center `c=a/q`, the centered endpoint major
> approximation is valid on a radius `rho_valid(c)` large enough that
> \[
> {c_0\over L_{\mathrm{crit}}(d,N)}
> \le
> \min(c_1Q_0^{-2},\rho_{\mathrm{valid}}(c))
> \]
> for every failing dyadic `d`-slice and kernel band; otherwise the major
> packet model functions satisfy the lower frame bound with residual
> `Delta_L` inside the Completion Energy Bound.

## Result

The feasibility check has become explicit. The literal route needs a
major-arc validity radius large enough to cover the failing high-`L` bands
without violating rational separation. The replacement route needs a major
packet frame theorem that captures the same high-`L` band energy by
orthogonal projection.
