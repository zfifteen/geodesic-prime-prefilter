# Shifted Type II Small-Modulus Strategy

Date: 2026-05-24

Status: candidate strategy for shifted Type II estimates after small rational
major-arc phases.

The minor-major resonance reduction requires Type II cancellation for
frequencies shifted by a small rational phase

$$
\alpha=\theta+a/q,
\qquad
q\le Q_0.
$$

The shift carries residue-class structure from the major arc. The Type II
estimate must be uniform in `q` and survive kernel-band weighting.

## Shifted Type II Form

A shifted Type II piece is

$$
S_{A,B}^{a/q}(\theta)=
\sum_{m\sim A}\alpha_m
\sum_{n\sim B}\beta_n
e((\theta+a/q)mn),
\qquad
AB\asymp X.
$$

The balanced range

$$
A\asymp B\asymp X^{1/2}
$$

is the bottleneck.

The needed estimate is uniform for

$$
q\le Q_0,
\qquad
(a,q)=1,
$$

and for `theta` outside the corresponding major arc after the shift.

## Modulus Decomposition

The rational factor is

$$
e(a mn/q).
$$

For small `q`, decompose the variables into residue classes modulo `q`:

$$
m\equiv r\pmod q,
\qquad
n\equiv s\pmod q.
$$

Then `e(a mn/q)` is constant on each pair `(r,s)`, and the remaining phase is

$$
e(\theta mn).
$$

Thus the shifted estimate reduces to Type II sums in arithmetic progressions
modulo `q`, with only polylogarithmic loss if `Q_0` is polylogarithmic.

Equivalently, one may expand the rational factor into Dirichlet characters or
finite additive characters modulo `q`.

## Candidate Large-Sieve Input

After Cauchy-Schwarz in `m`, the inner sums over `n` have frequencies

$$
\theta m+\frac{a m}{q}.
$$

A hybrid large-sieve estimate is needed for these frequencies, uniform in
`q <= Q_0` and in the residue classes of `m`.

A usable form is:

> **Shifted Type II Large-Sieve Bound.**
> For balanced `A,B` and `q <= Q_0`,
> $$
> \int_{\Theta}
> |S_{A,B}^{a/q}(\theta)|^2 w_N(\theta)\,d\theta
> \ll
> X(\log X)^{-A_0}
> $$
> after the appropriate kernel-band weight `w_N`, unless `theta+a/q` lies in
> the major arc already assigned to the major contribution.

The exact right side must be strong enough after summing over `q,a`, dyadic
ranges, and kernel bands.

## Character-Sum Alternative

Expanding modulo `q` gives bilinear sums with congruence restrictions. The
needed estimate can be stated as Type II cancellation in progressions:

$$
\sum_{\substack{m\sim A\\m\equiv r(q)}}\alpha_m
\sum_{\substack{n\sim B\\n\equiv s(q)}}\beta_n
e(\theta mn)
$$

uniformly for `r,s mod q`.

This asks for large-sieve dispersion with small fixed moduli inserted. Since
`q` is small, the main cost is not the modulus itself; it is preserving minor
arc spacing in the balanced range.

## Principal Obstacles

**Spacing after rational shift.**
The frequencies

$$
\theta m+a m/q
$$

can cluster when `m` shares residues modulo `q` or when `theta` is close to a
nearby rational. The proof must use the shifted major-arc exclusion precisely.

**Balanced range.**
When `A` and `B` are both near `X^{1/2}`, neither variable is long enough to
make cancellation automatic after Cauchy.

**Congruence-class coefficients.**
Splitting modulo `q` changes coefficient sequences. Divisor bounds and
centering must remain uniform across residue classes.

**Kernel-band weights.**
The weight `w_N(theta)` is largest near major centers. Estimates must improve
as the major approximation takes over, or transition-zone input must absorb
the loss.

**Summation over small moduli.**
Even polylogarithmic `Q_0` creates sums over `q,a`. The shifted Type II bound
must leave enough logarithmic room for these sums.

## Minimal Shifted Type II Lemma

The resonance route needs:

> **Small-Modulus Shifted Type II Lemma.**
> Uniformly for `q <= Q_0`, `(a,q)=1`, balanced Type II ranges, and dyadic
> kernel bands,
> $$
> S_{A,B}^{a/q}(\theta)
> $$
> satisfies the same minor-arc bilinear/mean-square bounds as the unshifted
> Type II sum, with only polylogarithmic loss, once the arc
> `theta+a/q` has been excluded from the major region.

## Result

The shifted Type II problem is a hybrid large-sieve or character-sum estimate
for balanced endpoint bilinear forms in small moduli. It is the core analytic
input needed to control minor-major resonance in the kernel-weighted
convolution.
