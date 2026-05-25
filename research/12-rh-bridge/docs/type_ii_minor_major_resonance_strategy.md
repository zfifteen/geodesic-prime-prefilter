# Type II Minor-Major Resonance Strategy

Date: 2026-05-24

Status: candidate strategy for frequency-pair resonance in the Type II
kernel-band convolution.

In the convolution norm, a minor-arc frequency can be paired with a frequency
near a major arc. This minor-major interaction is the most delicate resonance
case because the major partner can be amplified by the interval kernel and by
small-modulus arithmetic structure.

## Resonant Piece

Write a Type II piece as

$$
S_{A,B}(\alpha)=
\sum_{a\sim A}\alpha_a
\sum_{b\sim B}\beta_b e(\alpha ab),
\qquad
AB\asymp X.
$$

The resonant convolution piece has the form

$$
\left\|
L_1S_{A,B}1_{\mathfrak m_{L_1}}
*
L_2S_{A',B'}1_{\mathfrak M_{q,a,L_2}}
\right\|_2^2,
$$

where `mathfrak m` is minor and `mathfrak M_{q,a,L_2}` is a major-arc band
near

$$
\beta=a/q+\eta.
$$

The sum frequency is

$$
\xi=\alpha+\beta.
$$

The problem is that `beta` has structured arithmetic behavior while `alpha`
must still supply minor-arc cancellation after being coupled to `xi-beta`.

## Major Partner Replacement

On the major arc, replace the second factor by its explicit local
approximation:

$$
S_{A',B'}(\beta)
=
\mathcal M_{q,a}(\eta)
+\mathcal E_{q,a}(\eta).
$$

The error term belongs to the minor/transition estimates. The main term
reduces the resonant convolution to sums of the form

$$
\int_{\mathfrak M_{q,a}}
\mathcal M_{q,a}(\eta)
\,L_1S_{A,B}(\xi-a/q-\eta)
\,L_2
\,d\eta.
$$

Thus the minor Type II sum is tested near shifted frequencies

$$
\xi-a/q-\eta.
$$

The needed cancellation is a Type II estimate uniform after additive shifts by
small rational phases.

## Required Inputs

**Type II in residue classes.**
The minor Type II estimate must hold uniformly with congruence restrictions
modulo `q <= Q_0`, because the major approximation decomposes endpoint
structure by residue class.

**Zero-density transition control.**
For moderate `q` or for `eta` near the edge of a major arc, a zero-density or
Bombieri-Vinogradov type estimate must bound the major error
`\mathcal E_{q,a}` strongly enough after kernel weighting.

**Kernel-band summability.**
The major partner may have

$$
|K_N(\beta)|\asymp L_2
$$

with `L_2` large. The measure of the band and the quality of the major
approximation must compensate for this amplification.

**Balanced Type II dispersion.**
For `A,B ~ X^{1/2}`, the shifted minor estimate must still give logarithmic
saving after the major partner is inserted.

## Candidate Proof Mechanism

1. **Major expansion.**
   Expand the major partner into characters or residue-class main terms
   modulo `q`.

2. **Shifted minor estimate.**
   Prove a Type II bound for
   $$
   S_{A,B}(\theta+a/q)
   $$
   when `theta` lies outside the corresponding major arc after the shift.

3. **Average over major arcs.**
   Sum over `q <= Q_0`, `(a,q)=1`, and kernel bands using the decay and
   measure of `K_N`.

4. **Transition error.**
   Put the major approximation error into a zero-density or
   Bombieri-Vinogradov controlled remainder.

## Principal Obstacles

**Minor status is not invariant under shifting.**
The frequency `alpha` may be minor, but after writing
`alpha=xi-a/q-eta`, the shifted variable can approach another major arc. The
arc decomposition must be stable under this coupling.

**Small moduli amplify structure.**
Major arcs with small `q` carry the largest arithmetic main terms. The minor
partner must be estimated uniformly in those residue classes.

**Kernel amplification.**
Large `L_2` bands occur near major centers, exactly where approximation errors
are most dangerous.

**Balanced products.**
When both Type II variables are near `X^{1/2}`, Cauchy and large-sieve
arguments have the least spare room.

## Minimal Resonance Lemma

The needed input is:

> **Type II Minor-Major Resonance Lemma.**
> For each major arc `q <= Q_0`, after replacing the major partner by its
> explicit local approximation, the convolution with a minor Type II piece
> satisfies
> $$
> \sum_{L_1,L_2,q,a}
> \left\|
> L_1S_{A,B}1_{\mathfrak m_{L_1}}
> *
> L_2\mathcal M_{q,a}1_{\mathfrak M_{q,a,L_2}}
> \right\|_2^2
> \ll
> X\left(\frac{N}{\log X}\right)^2(\log X)^C,
> $$
> with the major approximation errors controlled by transition estimates.

## Result

The minor-major resonance problem reduces to shifted Type II estimates uniform
in small moduli, plus zero-density or Bombieri-Vinogradov control of major-arc
transition errors. This is the sharp resonance subproblem inside the
minor-arc convolution bound.
