# Hybrid Large-Sieve Closure at the Unified Scale

Date: 2026-05-24

Status: operator-norm closure strategy for the unified-scale
kernel-weighted BDH input.

The unified-scale character-sum target is

$$
\sum_{q\le Q_0}
\sum_{\chi\bmod q}^{*}
\int_{|\beta|\le R_{\mathrm{req}}}
\left|
\sum_{X<n\le2X}a_n\chi(n)e(\beta n)
\right|^2
\Omega_{q,\chi,N}(\beta)\,d\beta
\le
\mathcal B_{\mathrm{AP}}^K.
$$

It must satisfy

$$
{\mathcal B_{\mathrm{AP}}^K\over(\log X)^2}
\le
\mathcal E_{\mathrm{maj}}.
$$

## Operator-Norm Bound

Let

$$
\mathcal A_2=\sum_{X<n\le2X}|a_n|^2
$$

be the residual coefficient energy after major-packet subtraction.

A weighted hybrid large sieve with aperture radius `R_req` should give

$$
\mathcal B_{\mathrm{AP}}^K
\ll
\mathcal L_{\mathrm{hyb}}(X,Q_0,R_{\mathrm{req}},\Omega_N)
\mathcal A_2.
$$

The crude unweighted constant is

$$
\mathcal L_{\mathrm{hyb}}
\asymp
X+Q_0^2+R_{\mathrm{req}}^{-1},
$$

with an additional kernel-window factor if the weight is handled by a
supremum bound.

## Direct Closure Condition

The hybrid large-sieve route closes if

$$
\mathcal L_{\mathrm{hyb}}(X,Q_0,R_{\mathrm{req}},\Omega_N)
\mathcal A_2
\le
(\log X)^2\mathcal E_{\mathrm{maj}}.
$$

This is the direct operator-norm sufficiency test.

## Weighted Improvement

The preferred proof does not multiply by the worst kernel mass. It proves a
weighted large-sieve constant adapted to the windows

$$
\alpha={a\over q}+\beta,
\qquad
|\beta|\le R_{\mathrm{req}},
$$

and the projected kernel weight. The expected improvement comes from:

1. bounded overlap of the windows from `R_req <= cQ_0^{-2}`;
2. major-packet subtraction removing coherent packet energy;
3. using the actual kernel mass distribution instead of its supremum;
4. smoothing the aperture weights.

## Character Orthogonality

If the kernel weight is independent of `a`, ordinary character orthogonality
reduces the sum to the usual hybrid large sieve. The dependence of
`|K_N(a/q+\beta)|^2` on `a` requires either:

1. decomposing the weight into additive characters modulo `q`; or
2. using a direct continuous-frequency large sieve over the points
   `a/q+beta`.

The second route avoids complicated weighted character algebra.

## Failure Mode

If the operator-norm condition fails, the proof must use the dual
shifted-congruence route:

$$
n\equiv m\pmod q,
\qquad
|n-m|\lesssim R_{\mathrm{req}}^{-1}.
$$

That route has already been reduced to the post-variation scalar closure
condition for the shift kernel.

## Minimal Lemma

> **Unified Hybrid Large-Sieve Closure Lemma.**  
> At aperture radius `R_req`, after major-packet subtraction, the residual
> coefficients satisfy
> \[
> \mathcal B_{\mathrm{AP}}^K
> \le
> \mathcal L_{\mathrm{hyb}}(X,Q_0,R_{\mathrm{req}},\Omega_N)\mathcal A_2
> \le
> (\log X)^2\mathcal E_{\mathrm{maj}}.
> \]

## Result

The direct hybrid large-sieve branch has one scalar closure condition:
weighted large-sieve constant times residual coefficient energy must fit the
combined major budget. If it does not, the proof has to proceed through the
dual shifted-congruence and shift-kernel threshold machinery.
