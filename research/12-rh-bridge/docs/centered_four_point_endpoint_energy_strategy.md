# Centered Four-Point Endpoint Energy Strategy

Date: 2026-05-24

Status: candidate strategy for the main analytic burden in the direct
short-interval endpoint fourth moment.

After mean normalization and diagonal accounting, the direct concentration
route needs a centered four-point additive energy bound for prime endpoints at
scale `N`.

## Kernel Form

Let

$$
K_N(t)=1_{0<t<2N}
$$

and define the centered endpoint weight

$$
b_X(n)=1_{\mathbb P}(n)-\frac1{\log X}
$$

on the relevant odd endpoint range. Up to boundary terms,

$$
P_N(M)-\frac{2N}{\log X}
=
\sum_n b_X(n)K_N(M-n).
$$

Write

$$
G_N(M)=(b_X*K_N)(M).
$$

The desired fourth moment is

$$
\sum_{\substack{X\le M\le2X\\2\mid M}}|G_N(M)|^4
\ll
X\left(\frac{N}{\log X}\right)^2(\log X)^C.
$$

## Four-Point Energy Form

Expanding the fourth power gives a centered four-point endpoint energy:

$$
\sum_{p_1,p_2,p_3,p_4}
b_X(p_1)b_X(p_2)b_X(p_3)b_X(p_4)
\,
\Omega_N(p_1,p_2,p_3,p_4),
$$

where

$$
\Omega_N(p_1,p_2,p_3,p_4)
=
\#\{M:p_i<M<p_i+2N\text{ for }1\le i\le4\}
$$

with the dyadic even-center restriction. The overlap factor is nonzero only
when the four endpoints lie in an interval of diameter `<2N`.

The centered energy bound says that this weighted four-endpoint overlap sum is
Poisson-size, not fourth-power-size.

## Fourier Convolution Form

On a finite cyclic model for the dyadic interval,

$$
\widehat{G_N}(\alpha)=\widehat{b_X}(\alpha)\widehat{K_N}(\alpha).
$$

The physical fourth moment is controlled by the additive convolution of the
Fourier transform:

$$
\|G_N\|_4^4
\asymp
\|\widehat{G_N}*\widehat{G_N}\|_2^2
$$

up to the normalization and boundary terms of the finite model.

Thus a sufficient dispersion estimate is an `L^2` bound for

$$
(\widehat{b_X}\widehat{K_N})*
(\widehat{b_X}\widehat{K_N}).
$$

This form makes the cancellation target concrete: centered endpoint
exponential sums, smoothed by the interval kernel, must not concentrate their
additive convolution.

## Candidate Dispersion Mechanisms

### Fourier / Circle Method

On a finite cyclic model,

$$
\widehat{G_N}(\alpha)=\widehat{b_X}(\alpha)\widehat{K_N}(\alpha).
$$

The fourth moment can be bounded by splitting frequencies into major and minor
arcs.

Major arcs must reproduce the mean and diagonal terms, which are removed by
centering. Minor arcs require bounds for prime endpoint exponential sums
weighted by `K_N`.

### Large-Sieve Dispersion

Use large-sieve estimates for the centered endpoint sequence in residue
classes, combined with the Fourier decay of the interval kernel. This targets
the Fourier-convolution norm directly.

### Selberg-Turan Moment Method

Adapt Selberg's method for moments of primes in short intervals to the
unweighted endpoint count. This route packages the major/minor arc and
diagonal bookkeeping into one short-interval moment theorem.

## Principal Obstacles

**Centered cancellation is essential.**
The uncentered four-overlap sum has a large main term. The subtraction
`1/log X` must cancel the independent-density contribution before the desired
Poisson-scale bound appears.

**Major arcs carry arithmetic structure.**
Residue-class biases and small-modulus singular factors must be accounted for,
not bounded crudely as errors.

**Minor arcs require endpoint exponential-sum control.**
The required scale is strong enough to rule out large coherent oscillation of
prime endpoints inside many moving windows.

**Unweighted endpoints are harder than weighted sums.**
The endpoint indicator is sharper than `Lambda`. A weighted theorem needs an
additional transfer step before it can prove endpoint absence bounds.

**Uniformity in `N`.**
The kernel `K_N` changes from very short to dyadic-scale. Small `N` is
absorbed by the trivial range, but the proof must be uniform across the
nontrivial range.

## Minimal Energy Lemma

The direct concentration route needs:

> **Centered Endpoint Four-Energy Lemma.**
> For `1 <= N <= X/2`, outside the trivial small-mean range,
> $$
> \sum_{\substack{X\le M\le2X\\2\mid M}}
> \left|
> \sum_n\left(1_{\mathbb P}(n)-\frac1{\log X}\right)K_N(M-n)
> \right|^4
> \ll
> X\left(\frac{N}{\log X}\right)^2(\log X)^C.
> $$

This lemma implies the direct short-interval endpoint fourth moment.

## Result

The main analytic burden is now a centered endpoint four-energy estimate. The
candidate mechanisms are Fourier/circle-method decomposition, large-sieve
dispersion, or a Selberg-Turan short-interval moment theorem. The core
obstacle is centered off-diagonal cancellation for unweighted prime endpoints.
