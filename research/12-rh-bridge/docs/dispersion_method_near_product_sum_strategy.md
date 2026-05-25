# Dispersion Method for the Near-Product Sum

Date: 2026-05-24

Status: candidate strategy for converting the kernel-weighted near-product
target into a dispersion-method estimate.

The current off-diagonal object is

$$
S_{\mathrm{off}}
=
\sum_{\substack{m,m'\sim A\\ n,n'\sim B\\ mn\ne m'n'}}
\alpha_m\overline{\alpha_{m'}}
\beta_n\overline{\beta_{n'}}
e\!\left({a(mn-m'n')\over q}\right)
W_N(mn-m'n'),
$$

with

$$
A\asymp B\asymp X^{1/2},\qquad q\le Q_0,\qquad (a,q)=1.
$$

The diagonal `mn=m'n'` is part of the Poisson term. The dispersion task is to
bound the remaining part after the major-arc coherent component has been
removed.

## Common-Divisor Linearization

Split

$$
m=du,\qquad m'=dv,\qquad (u,v)=1.
$$

Then

$$
mn-m'n'=d(un-vn').
$$

The off-diagonal sum becomes a sum over coprime slopes `u,v` and a linear
difference variable

$$
t=un-vn'\ne 0.
$$

For fixed `d,u,v`, the local contribution has the form

$$
\sum_{n,n'\sim B}
\beta_n\overline{\beta_{n'}}
e\!\left({ad(un-vn')\over q}\right)
W_N(d(un-vn')).
$$

This is the point where the product equation becomes a family of linear
congruence problems.

## Congruence Forms

The equation

$$
un-vn'=t
$$

imposes

$$
u n\equiv t\pmod v,
\qquad
v n'\equiv -t\pmod u.
$$

Since `(u,v)=1`, each nonzero `t` selects one residue class for `n` modulo
`v` and one residue class for `n'` modulo `u`. The rational phase contributes

$$
e\!\left({adt\over q}\right).
$$

Writing `g=(d,q)` and `q_1=q/g`, the phase has conductor dividing `q_1`.
When `q_1=1`, the rational oscillation is absent; the estimate must then come
entirely from coefficient dispersion and major-exclusion. This is the first
degenerate case the proof must handle explicitly.

## Additive-Character Expansion

Detect the linear equation with additive characters, or equivalently Fourier
transform the kernel-weighted function of `t`:

$$
e\!\left({adt\over q}\right)W_N(dt)
=
\int \widehat W_{N,d}(\xi)\,
e\bigl((\xi+ad/q)t\bigr)\,d\xi .
$$

The fixed-slope contribution factors into

$$
\int \widehat W_{N,d}(\xi)
\left(\sum_{n\sim B}\beta_n e((\xi+ad/q)un)\right)
\overline{
\left(\sum_{n'\sim B}\beta_{n'} e((\xi+ad/q)vn')\right)}
d\xi .
$$

Thus the dispersion estimate is a mean-square statement for coefficient sums
at the paired frequencies

$$
u(\xi+ad/q),\qquad v(\xi+ad/q),
$$

summed over coprime slopes `u,v` and common divisor `d`.

## Major-Exclusion Handling

The rational phase alone is too weak for small `q`. The coherent part must be
removed before the dispersion estimate is invoked.

The major-exclusion projector should remove three sources:

1. the exact product diagonal `mn=m'n'`;
2. residue-class averages modulo the small conductor `q_1`;
3. low-denominator frequency packets selected by the kernel transform.

After this subtraction, the remaining coefficient sums must have zero local
mean in the residue classes that the phase cannot distinguish. The dispersion
input is then applied to the mean-zero remainder, not to the raw coefficient
sequence.

## Required Additive Inputs

**Hybrid large-sieve input.**
For the frequencies `u(\xi+ad/q)` and `v(\xi+ad/q)`, control the average
over slopes and small moduli after the major projector has been removed.

**Linear dispersion input.**
For coprime `u,v`, bound the discrepancy of the shifted residue-class count

$$
\sum_{\substack{n,n'\sim B\\ un-vn'=t}}
\beta_n\overline{\beta_{n'}}
-
\operatorname{Main}_{u,v,d,q}(t)
$$

after summing against `e(adt/q)W_N(dt)`.

**Kloosterman-type input.**
When one solves the congruence for `n` or `n'`, reciprocal phases appear in
the moduli `u` and `v`. The needed bound is cancellation on average over the
coprime slope pairs, not a pointwise bound for each pair.

**Degenerate-conductor input.**
For `q_1=1` or very small `q_1`, the proof must show that the major projector
has removed the whole coherent part. The remaining estimate is then a pure
bilinear dispersion estimate.

## Minimal Dispersion Statement

The next analytic input can be stated as follows.

> **Projected Kernel Dispersion Lemma.**  
> Let the Type II coefficients be divisor-bounded and let the major-exclusion
> projector remove the exact diagonal, the small-conductor residue averages,
> and the low-denominator kernel packets. In the balanced range
> `A asymp B asymp X^{1/2}`, the projected off-diagonal near-product sum is
> bounded by the Poisson-scale allowance after summing over kernel bands,
> uniformly for `q <= Q_0`.

The lemma is the exact dispersion-method bridge needed by the shifted Type II
minor-arc route. It does not follow from the product-difference formulation
alone. It requires a genuine average cancellation estimate for the projected
linear congruence family `un-vn'=t`.

## Result

The near-product problem has been converted into a dispersion-method target:
common-divisor splitting turns `mn-m'n'` into `d(un-vn')`, additive Fourier
expansion turns the kernel into paired slope frequencies, and major-exclusion
must remove every coherent small-conductor component before the bilinear
dispersion estimate is applied.
