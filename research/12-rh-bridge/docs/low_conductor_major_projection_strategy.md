# Low-Conductor Major Projection Strategy

Date: 2026-05-24

Status: candidate construction of the coefficient-level major subspace and
projection needed by the direct additive large-sieve route.

The direct route needs a coefficient-level residual

$$
a^{\perp}=a-P_{\mathrm{maj}}a
$$

whose Fourier transform reproduces local major packet subtraction on
`|beta| <= R_all`.

## Major Subspace

Work on the coefficient interval `X < n <= 2X`, with a smooth interval weight
if needed. For every low-conductor center

$$
c={a\over q},\qquad q\le Q_0,
$$

define the packet basis vector

$$
\phi_c(n)=e(-cn).
$$

Include:

1. the constant vector `c=0`;
2. additive characters `e(-an/q)` for `q <= Q_0`;
3. periodic exceptional coherent components, represented in the same finite
   additive basis modulo their conductor.

Set

$$
\mathcal V_{\mathrm{maj}}
=
\operatorname{span}\{\phi_c:c\in\mathcal C_{Q_0}\}.
$$

## Projection

Let `P_maj` be the least-squares projection onto `V_maj` in the coefficient
space

$$
\ell^2(X<n\le2X).
$$

Equivalently, solve the Gram system

$$
\sum_{c'}G(c,c')\lambda_{c'}
=
\langle a,\phi_c\rangle,
$$

where

$$
G(c,c')=\sum_{X<n\le2X}\phi_c(n)\overline{\phi_{c'}(n)}.
$$

Then

$$
P_{\mathrm{maj}}a(n)=\sum_c\lambda_c\phi_c(n).
$$

## Gram Control

The diagonal terms satisfy

$$
G(c,c)\asymp X.
$$

For distinct low-conductor centers,

$$
|G(c,c')|
\ll
\|c-c'\|^{-1}
\ll
Q_0^2.
$$

Thus the frame is well conditioned when the total off-diagonal interaction is
small compared with `X`. A sufficient regime is

$$
|\mathcal C_{Q_0}|Q_0^2\ll X,
$$

or any sharper large-sieve frame bound that gives bounded projection norm.

## Reproduction of Local Packets

For `alpha=c+beta`,

$$
\sum_n \phi_c(n)e(\alpha n)
=
\sum_n e(\beta n),
$$

which is the basic major packet shape. Contributions from `c' != c` are

$$
\sum_n e((c-c'+\beta)n),
$$

and are small on `|beta| <= R_all` if

$$
R_{\mathrm{all}}\le c_1Q_0^{-2}
$$

and the Gram/off-center bounds hold.

Therefore `P_maj a` reproduces the finite linear combination of local packet
models with coefficients `lambda_c`, up to cross-packet errors assigned to the
major budget.

## Required Inputs

The projection construction needs:

1. a precise set of low-conductor centers `C_Q0`;
2. smooth coefficient-window weights;
3. Gram matrix or large-sieve frame bounds;
4. coefficient choices matching the major packet amplitudes;
5. exceptional periodic components represented in the same subspace;
6. cross-packet error bounds on `|beta| <= R_all`.

## Minimal Lemma

> **Low-Conductor Major Projection Lemma.**  
> The additive packet vectors `{e(-cn): c in C_Q0}` form a bounded frame on
> `X<n<=2X`, the projection onto their span has bounded operator norm, and
> the Fourier transform of `P_maj a` reproduces the local major packet models
> on every window `|beta| <= R_all`, with cross-packet leakage inside the
> assigned major error budget.

## Result

The coefficient-level major projection can be built from a low-conductor
additive Fourier frame. Its validity is controlled by rational spacing,
Gram-matrix conditioning, and cross-packet leakage on the unified aperture
windows.
