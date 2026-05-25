# Major Projection Amplitude Reproduction Strategy

Date: 2026-05-24

Status: candidate strategy for matching coefficient-level major projection
amplitudes with classical major packet amplitudes.

The frame projection gives coefficients

$$
P_{\mathrm{maj}}a(n)=\sum_{c\in\mathcal C_{Q_0}}\lambda_c e(-cn).
$$

The arithmetic task is to show that the coefficients `lambda_c` reproduce the
classical major packet amplitudes on

$$
|\beta|\le R_{\mathrm{all}}.
$$

## Correlation Coefficients

For

$$
c={a\over q},
$$

the raw packet correlation is

$$
\langle a,\phi_c\rangle
=
\sum_{X<n\le2X}a_n e(cn).
$$

For a von Mangoldt-weighted coefficient, PNT in AP gives

$$
\sum_{X<n\le2X}\Lambda(n)e\!\left({a n\over q}\right)
\approx
{\mu(q)\over\varphi(q)}X
$$

after smoothing and endpoint normalization. For unweighted endpoints,
partial summation transfers this to the `1_P` coefficient with logarithmic
normalization.

## Gram Inversion

The projection coefficients are not exactly the raw correlations; they solve

$$
\sum_{c'}G(c,c')\lambda_{c'}
=
\langle a,\phi_c\rangle.
$$

If the Gram matrix is well conditioned and off-diagonal leakage is inside the
major error budget, then

$$
\lambda_c
=
{1\over X}
\langle a,\phi_c\rangle
+\text{controlled cross-packet correction}.
$$

Thus the classical amplitude follows from AP estimates plus frame
conditioning.

## Local Reproduction

Near `alpha=c+beta`,

$$
\sum_n \lambda_c e(-cn)e((c+\beta)n)
=
\lambda_c\sum_n e(\beta n).
$$

Therefore the local major packet is reproduced if

$$
\lambda_c
\approx
{\mu(q)\over\varphi(q)}
$$

with the correct endpoint normalization and centering.

Cross terms from `c' != c` are controlled by rational spacing and the
`R_all <= cQ_0^{-2}` aperture condition.

## Exceptional and Principal Components

The principal component supplies the expected density and centered constant
term. If an exceptional real character contributes a coherent term, include
its periodic sequence in `V_maj` and reproduce its amplitude by the same
correlation/Gram method.

## Required Inputs

The amplitude reproduction proof needs:

1. PNT in AP or Siegel-Walfisz for `q <= Q_0`, or zero-density input for
   exceptional/transition centers;
2. partial summation from `Lambda` to endpoint coefficients;
3. Gram conditioning of the low-conductor frame;
4. cross-packet leakage bounds on `|beta| <= R_all`;
5. centering normalization for the constant packet.

## Minimal Lemma

> **Major Projection Amplitude Lemma.**  
> The projection coefficients `lambda_c` of the endpoint coefficient sequence
> onto the low-conductor packet frame satisfy
> \[
> \lambda_{a/q}
> =
> {\mu(q)\over\varphi(q)}
> +O(\operatorname{AmpErr}_{a/q})
> \]
> with endpoint normalization and centering, and the induced local Fourier
> packet error on `|beta| <= R_all` is inside the assigned major budget.

## Result

Amplitude reproduction is the arithmetic part of coefficient-level major
projection. Frame conditioning supplies stable coefficients; PNT in AP and
zero-density inputs identify those coefficients with the classical major
packet amplitudes.
