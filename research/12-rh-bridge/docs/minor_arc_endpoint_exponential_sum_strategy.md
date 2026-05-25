# Minor-Arc Endpoint Exponential-Sum Strategy

Date: 2026-05-24

Status: candidate approaches for the minor-arc input in the centered endpoint
four-energy route.

The major-minor arc decomposition leaves a minor-arc estimate for the centered
endpoint weight after smoothing by the interval kernel. The estimate must be
strong enough after additive convolution, not merely pointwise on the
exponential sum.

## Object

Let

$$
B_X(\alpha)=
\sum_n\left(1_{\mathbb P}(n)-\frac1{\log X}\right)e(\alpha n)
$$

on the relevant dyadic endpoint range, and let

$$
K_N(\alpha)=\widehat{1_{0<t<2N}}(\alpha).
$$

Set

$$
H_N(\alpha)=B_X(\alpha)K_N(\alpha).
$$

The minor-arc task is to prove

$$
\|(H_N)_{\mathfrak m}*H_N\|_2^2
\ll
X\left(\frac{N}{\log X}\right)^2(\log X)^C.
$$

This is the minor-arc part of the centered endpoint four-energy lemma.

## Candidate Inputs

### 1. Vaughan-Type Endpoint Sum Bounds

Replace `1_P` by a partial-summation form of `Lambda/log`, then apply Vaughan
or Heath-Brown decomposition to control

$$
\sum_{n\le X}1_{\mathbb P}(n)e(\alpha n)
$$

on minor arcs.

The required strength is not only

$$
|B_X(\alpha)|\ll X(\log X)^{-A},
$$

but a kernel-weighted form that remains useful after convolution with
`H_N`.

### 2. Large-Sieve Weighted Mean Square

Prove a weighted large-sieve estimate of the form

$$
\int_{\mathfrak m}
|B_X(\alpha)|^2|K_N(\alpha)|^2\,d\alpha
\ll
X\frac{N}{\log X}(\log X)^C,
$$

with additional bilinear control sufficient for the convolution norm.

This route treats the kernel scale directly and avoids relying only on a
pointwise minor-arc bound.

### 3. Zero-Density Near Major Boundaries

For arcs close to rationals with moderately large denominator, use zero-density
or Bombieri-Vinogradov style input to control prime distribution in residue
classes beyond the major-arc range.

This handles the transition region where the kernel is still large but the
major-arc asymptotic is not being used.

## Convolution-Strength Requirement

Pointwise minor-arc cancellation is insufficient unless it is strong enough
after the interval kernel and convolution.

A usable sufficient package would be:

```text
minor-arc L2 bound for B_X K_N
+ minor-arc bilinear/convolution bound for (B_X K_N)_m * (B_X K_N)
-> minor-arc contribution to fourth energy is Poisson-size.
```

The second line is the hard part. The fourth moment sees pairs of frequencies
whose sum is fixed; cancellation must survive that additive coupling.

## Principal Obstacles

**Unweighted endpoint sequence.**
Most strong minor-arc technology is formulated for `Lambda`. Passing to
`1_P` requires partial summation and control of prime powers and log weights.

**Kernel amplification.**
The interval kernel satisfies

$$
|K_N(\alpha)|\ll \min(N,\|\alpha\|^{-1}),
$$

so frequencies near zero or near major rationals are amplified. Minor arcs
must begin far enough from major rationals, or the transition region must be
handled separately.

**Convolution coupling.**
The target involves `H_N * H_N`, so two individually minor frequencies can
combine into a major frequency. The proof must account for this interaction.

**Uniformity in `N`.**
For small `N`, the kernel is broad; for large `N`, it is sharply localized.
The minor-arc estimate must adapt across the nontrivial range.

**Dyadic endpoint restriction.**
The endpoint sum is localized to the dyadic prime range relevant to centers
`M in [X,2X]`. Smooth cutoffs may be needed to avoid boundary artifacts in
Fourier estimates.

## Minimal Minor-Arc Lemma

The required input is:

> **Kernel-Weighted Endpoint Minor-Arc Lemma.**
> For the centered endpoint sum `B_X` and interval kernel `K_N`,
> $$
> \|(B_XK_N)_{\mathfrak m}*(B_XK_N)\|_2^2
> \ll
> X\left(\frac{N}{\log X}\right)^2(\log X)^C
> $$
> uniformly in the nontrivial range of `N`.

This lemma, paired with the major-arc singular calculation, gives the centered
four-point endpoint energy bound.

## Result

The minor-arc task is a kernel-weighted endpoint exponential-sum dispersion
estimate at convolution strength. Candidate tools are Vaughan-type
decomposition, weighted large-sieve estimates, and zero-density input near
major-arc boundaries. The main obstacle is preserving cancellation after the
interval kernel and additive convolution.
