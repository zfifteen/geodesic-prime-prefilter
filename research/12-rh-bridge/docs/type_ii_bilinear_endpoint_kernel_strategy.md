# Type II Bilinear Endpoint Kernel Strategy

Date: 2026-05-24

Status: candidate strategy for the Type II bottleneck in the minor-arc
kernel-band estimate.

After Vaughan or Heath-Brown decomposition of the centered endpoint sum, the
hard minor-arc pieces are Type II bilinear forms. The interval kernel and the
fourth-moment convolution force a bilinear estimate in frequency pairs, not
only a one-frequency exponential-sum estimate.

## Type II Shape

A typical Type II piece has the form

$$
S_{A,B}(\alpha)=
\sum_{a\sim A}\alpha_a
\sum_{b\sim B}\beta_b\,e(\alpha ab),
\qquad
AB\asymp X,
$$

with divisor-bounded coefficients coming from the endpoint decomposition.

In a kernel band where

$$
|K_N(\alpha)|\asymp L,
$$

the relevant piece is

$$
L\,S_{A,B}(\alpha)1_{\mathfrak m_L}(\alpha).
$$

The convolution-strength estimate must control sums of the form

$$
\left\|
L_1S_{A,B}1_{\mathfrak m_{L_1}}
*
L_2S_{A',B'}1_{\mathfrak b_{L_2}}
\right\|_2^2
$$

after summing over dyadic `A,B,A',B'` and kernel bands.

## Candidate Bilinear Bound

The needed Type II input is:

> **Kernel-Band Type II Endpoint Bound.**
> For Type II ranges `A,B` and `A',B'` with products comparable to `X`,
> $$
> \sum_{L_1,L_2}
> \left\|
> L_1S_{A,B}1_{\mathfrak m_{L_1}}
> *
> L_2S_{A',B'}1_{\mathfrak b_{L_2}}
> \right\|_2^2
> \ll
> X\left(\frac{N}{\log X}\right)^2(\log X)^{-A_0}
> $$
> after summing over the decomposition pieces, with enough logarithmic saving
> to absorb Type I pieces and transition arcs.

The exact logarithmic exponent can be adjusted; the structural requirement is
Poisson-scale contribution after kernel weighting.

## Candidate Proof Mechanism

1. **Cauchy in one variable.**
   Apply Cauchy-Schwarz in the `a` variable to reduce to correlations of sums
   over `b`.

2. **Large-sieve over product phases.**
   Use the spacing of phases `alpha a b` on minor arcs to bound the resulting
   second moment.

3. **Frequency-pair dispersion.**
   In the convolution norm, frequencies appear as pairs `(alpha,beta)` with
   fixed sum. The proof must show that minor-arc cancellation remains after
   imposing `alpha+beta=xi`.

4. **Kernel-band summation.**
   Sum the estimates with weights `L_1^2 L_2^2`, using the measure and
   location of the bands where `|K_N|` has dyadic size.

## Main Obstacles

**Frequency-pair resonance.**
Even if `alpha` is minor, the paired frequency `xi-alpha` can be close to a
major arc. The bilinear estimate must handle minor-major and minor-minor
pairs separately.

**Balanced Type II ranges.**
The hardest case is `A` and `B` both near `X^{1/2}`. Product phases have less
obvious spacing, and coefficient correlations are strongest.

**Centered unweighted endpoint coefficients.**
The original sequence is `1_P-1/log X`. Passing through Vaughan or
Heath-Brown decomposition introduces log weights and smooth cutoffs; the
centering must survive partial summation.

**Kernel amplification near arc boundaries.**
High `L` bands sit near rationals. These are precisely where Type II estimates
can lose strength, so the major/minor boundary and zero-density transition
input must be coordinated with the band decomposition.

**Summation over decomposition pieces.**
The final bound must survive all dyadic `A,B` ranges and all kernel bands with
only logarithmic loss.

## Required Supporting Estimates

**Type I control.**
The easier Type I sums must be bounded with enough saving that the Type II
piece remains the bottleneck.

**Coefficient divisor bounds.**
The decomposition coefficients must satisfy uniform divisor-type bounds so
large-sieve losses remain logarithmic.

**Transition-zone estimates.**
Moderate-denominator arcs near the major boundary likely need
Bombieri-Vinogradov or zero-density input before Type II estimates are
effective.

## Result

The Type II bottleneck is now a kernel-band bilinear dispersion theorem for
frequency-pair convolutions of endpoint decomposition sums. Solving it would
provide the main minor-arc input for the centered four-point endpoint energy
bound.
