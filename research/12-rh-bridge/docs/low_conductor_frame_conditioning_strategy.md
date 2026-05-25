# Low-Conductor Frame Conditioning Strategy

Date: 2026-05-24

Status: candidate strategy for frame bounds, projection norm, and residual
energy in the low-conductor major projection.

The packet frame is

$$
\phi_c(n)=e(-cn),
\qquad
c\in\mathcal C_{Q_0},
\qquad
X<n\le2X.
$$

The projection `P_maj` is the orthogonal projection onto

$$
\mathcal V_{\mathrm{maj}}=\operatorname{span}\{\phi_c\}.
$$

## Upper Frame Bound

The additive large sieve gives

$$
\sum_{c\in\mathcal C_{Q_0}}
\left|
\sum_{X<n\le2X}u_n e(cn)
\right|^2
\ll
(X+Q_0^2)\sum_{X<n\le2X}|u_n|^2,
$$

using rational spacing at scale `Q_0^{-2}`.

This controls packet correlations for arbitrary coefficient sequences.

## Gram Conditioning

The Gram matrix is

$$
G(c,c')=\sum_{X<n\le2X}e((c'-c)n).
$$

The diagonal satisfies

$$
G(c,c)\asymp X.
$$

For `c != c'`,

$$
|G(c,c')|\ll \|c-c'\|^{-1}\ll Q_0^2.
$$

A simple diagonal-dominance condition is

$$
|\mathcal C_{Q_0}|Q_0^2\ll X.
$$

Sharper large-sieve/Riesz sequence estimates may improve this, but this
condition is a transparent sufficient regime.

## Projection Norm and Residual Energy

As an orthogonal projection in coefficient `L^2`,

$$
\|P_{\mathrm{maj}}\|\le1,
\qquad
\|a^{\perp}\|_2^2
\le
\|a\|_2^2.
$$

Therefore

$$
\mathcal A_2
=
\sum|a_n^{\perp}|^2
\le
\sum|a_n|^2.
$$

For centered endpoint coefficients, this gives the expected baseline size
`A_2` from the chosen coefficient normalization.

## Arithmetic Reproduction Is Separate

Frame conditioning alone does not prove that `P_maj a` has the classical
major packet amplitudes. It only gives a bounded projection and residual
energy.

Matching the amplitudes

$$
{\mu(q)\over\varphi(q)}
$$

or exceptional coherent components requires AP information about the original
prime coefficient sequence. That input belongs to the major validity theorem,
not to frame conditioning.

## Required Inputs

The frame step needs:

1. rational spacing for centers in `C_Q0`;
2. a large-sieve upper frame bound;
3. a Gram lower bound or Riesz sequence estimate;
4. the coefficient normalization determining `||a||_2^2`;
5. separate AP input for classical major amplitudes.

## Minimal Lemma

> **Low-Conductor Frame Conditioning Lemma.**  
> The packet vectors `{e(-cn): c in C_Q0}` form a bounded Riesz sequence on
> `X<n<=2X`, so the orthogonal projection onto their span has stable
> coefficients and residual energy
> `A_2 <= ||a||_2^2`. The reproduction of classical major amplitudes is then
> supplied separately by major-arc AP estimates.

## Result

The frame-conditioning step is mostly analytic linear algebra plus the
additive large sieve. It controls projection stability and residual energy.
It does not replace the arithmetic major-arc theorem needed to identify the
packet amplitudes.
