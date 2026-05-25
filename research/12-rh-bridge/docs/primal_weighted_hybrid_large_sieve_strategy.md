# Primal Weighted Hybrid Large-Sieve Strategy

Date: 2026-05-24

Status: candidate primal proof strategy for the weighted hybrid
character/additive large sieve at the unified aperture scale.

The direct target is

$$
\sum_{q\le Q_0}
\sum_{\chi\bmod q}^{*}
\int_{|\beta|\le R_{\mathrm{req}}}
\left|
\sum_{X<n\le2X}a_n\chi(n)e(\beta n)
\right|^2
\Omega_{q,\chi,N}(\beta)\,d\beta
\le
\mathcal L_{\mathrm{hyb}}^{\Omega}\mathcal A_2.
$$

The closure condition is

$$
\mathcal L_{\mathrm{hyb}}^{\Omega}\mathcal A_2
\le
(\log X)^2\mathcal E_{\mathrm{maj}}.
$$

## Weighted Measure View

The weights define a measure on the hybrid family

$$
(q,\chi,\beta),
\qquad
q\le Q_0,\quad |\beta|\le R_{\mathrm{req}}.
$$

The large-sieve constant is governed by the local concentration of the
frequencies

$$
\alpha={a\over q}+\beta
$$

after resolving the character and packet weights. A weighted theorem should
charge the actual mass of the kernel windows, not the worst possible peak at
every packet center.

## Sufficient Hybrid Large-Sieve Form

A usable theorem has the form

$$
\mathcal L_{\mathrm{hyb}}^{\Omega}
\ll
X
+
\mathcal C_{\mathrm{mult}}(Q_0,\Omega)
+
\mathcal C_{\mathrm{add}}(R_{\mathrm{req}},\Omega),
$$

where:

1. `X` is sequence length;
2. `C_mult` is the weighted multiplicative conductor concentration;
3. `C_add` is the weighted additive-window concentration.

In the unweighted case this recovers the schematic constant

$$
X+Q_0^2+R_{\mathrm{req}}^{-1}.
$$

## Handling the `a`-Dependent Kernel Weight

The factor

$$
|K_N(a/q+\beta)|^2
$$

depends on the residue `a`. There are two proof paths.

**Direct continuous-frequency large sieve.**
Treat the points `a/q+beta` as the primary frequencies and prove a weighted
spacing bound for their measure.

**Character-weight decomposition.**
Expand the `a`-dependent weight into additive characters modulo `q` and use
character orthogonality with controlled off-diagonal character couplings.

The direct continuous-frequency route is cleaner because the kernel is a
function of the actual Fourier frequency.

## Major-Packet Subtraction

Major-packet subtraction is applied before the estimate. It removes coherent
principal and exceptional components from `a_n`, reducing `A_2` and ensuring
that the large sieve is bounding residual oscillation rather than major
structure.

The operator norm itself does not prove the subtraction; it uses the residual
sequence produced by the subtraction.

## Required Inputs

The primal proof needs:

1. a weighted hybrid large-sieve theorem for character sums with additive
   twists;
2. a frequency-measure concentration bound for the weighted windows
   `a/q+beta`;
3. smoothing of aperture windows at `R_req`;
4. character bookkeeping for primitive/imprimitive and exceptional terms;
5. a residual coefficient energy bound `A_2`.

## Minimal Lemma

> **Primal Weighted Hybrid Large-Sieve Lemma.**  
> The weighted hybrid family at aperture radius `R_req` satisfies
> \[
> \sum_{q\le Q_0}\sum_{\chi\bmod q}^{*}
> \int_{|\beta|\le R_{\mathrm{req}}}
> \left|\sum_{X<n\le2X}a_n\chi(n)e(\beta n)\right|^2
> \Omega_{q,\chi,N}(\beta)d\beta
> \le
> \mathcal L_{\mathrm{hyb}}^{\Omega}\mathcal A_2
> \]
> with
> \[
> \mathcal L_{\mathrm{hyb}}^{\Omega}\mathcal A_2
> \le
> (\log X)^2\mathcal E_{\mathrm{maj}}.
> \]

## Result

The primal weighted large-sieve proof is an operator-norm estimate for the
actual kernel-weighted frequency measure. Its decisive inputs are weighted
frequency spacing, hybrid character/additive large sieve, and the residual
coefficient energy after major-packet subtraction.
