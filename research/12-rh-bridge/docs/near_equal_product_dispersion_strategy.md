# Near-Equal Product Dispersion Strategy

Date: 2026-05-24

Status: candidate strategy for the product-difference core of the shifted Type
II estimate.

After expanding the shifted Type II mean square, the central object is a
kernel-weighted count of near-equal products

$$
mn\approx m'n'
$$

with a small-modulus oscillation from the rational shift `a/q`.

## Product-Difference Sum

In the balanced range

$$
m,m'\sim A,\qquad n,n'\sim B,\qquad A\asymp B\asymp X^{1/2},
$$

the expanded mean square contains sums of the form

$$
\sum_{m,m'\sim A}
\sum_{n,n'\sim B}
\alpha_m\overline{\alpha_{m'}}
\beta_n\overline{\beta_{n'}}
e\!\left(\frac{a(mn-m'n')}{q}\right)
W_N(mn-m'n'),
$$

where `W_N` is the transform of the theta/kernel-band weight. It is
concentrated on product differences in a band determined by the reciprocal
frequency width.

The task is to show that this sum has Poisson-scale size after the diagonal
terms are separated.

## Diagonal Terms

The exact diagonal

$$
mn=m'n'
$$

is controlled by divisor-energy bounds for the multiplication table:

$$
\#\{m n=m'n':m,m'\sim A,\ n,n'\sim B\}
\ll
X(\log X)^C.
$$

These diagonal terms contribute to the expected Poisson lower-order terms and
must be retained, not discarded as error.

## Off-Diagonal Dispersion

For

$$
r=mn-m'n'\ne0,
$$

the off-diagonal contribution is weighted by

$$
e(ar/q)W_N(r).
$$

A dispersion proof should:

1. split by common divisors of `m` and `m'`;
2. rewrite the relation as a congruence or short linear equation in `n,n'`;
3. use oscillation in `e(ar/q)` and coefficient cancellation to control the
   sum over `r`;
4. exploit that major-arc exclusion prevents the theta integral from selecting
   a coherent rational progression.

## Character-Sum Form

After splitting residue classes modulo `q`, the rational phase can be
absorbed into characters or finite additive sums. The off-diagonal problem
becomes a family of bilinear character sums over near-product equations.

The needed input is a bound of the form:

$$
\sum_{r\ne0}
W_N(r)e(ar/q)
\mathcal C_{A,B}(r)
\ll
X(\log X)^{-A_0}
$$

after kernel-band summation, where

$$
\mathcal C_{A,B}(r)
=
\sum_{mn-m'n'=r}
\alpha_m\overline{\alpha_{m'}}
\beta_n\overline{\beta_{n'}}.
$$

## Principal Obstacles

**High multiplicative energy.**
Balanced products have many near-collisions. A crude count of
`mn approx m'n'` is too large.

**Small modulus gives weak oscillation.**
Since `q <= Q_0`, the phase `e(ar/q)` alone cannot provide enough
cancellation. It must be combined with coefficient dispersion and major-arc
exclusion.

**Kernel window width.**
The support width of `W_N` depends on the kernel band. Wide windows admit many
near-products; narrow windows are more diagonal but can have larger kernel
weights.

**Major-arc leakage.**
If product differences align with a rational structure assigned to the major
arcs, the off-diagonal sum can carry a main term. The minor condition must
remove this coherent part before dispersion is applied.

**Coefficient structure.**
Vaughan or Heath-Brown coefficients are divisor-bounded but not random. The
proof must use their bilinear structure rather than assume independence.

## Candidate Inputs

**Multiplicative large sieve.**
Control near-product correlations for bilinear coefficient sequences in the
balanced range.

**Dispersion method.**
After Cauchy, transform the near-product condition into congruence sums and
apply additive character cancellation.

**Kloosterman-type estimates.**
If the congruence transformation produces reciprocal phases, use
Kloosterman-sum bounds to control off-diagonal terms.

**Major-exclusion projector.**
Subtract or project away the rational structures already assigned to major
arcs before estimating the off-diagonal product sum.

## Minimal Product-Dispersion Lemma

The shifted Type II route needs:

> **Kernel-Weighted Product Dispersion Lemma.**
> In balanced Type II ranges and for `q <= Q_0`, the off-diagonal sum over
> `r=mn-m'n'` with weight `e(ar/q)W_N(r)` is bounded by the Poisson-scale
> allowance after summing over kernel bands, once the major-arc coherent
> component is removed.

## Result

The hybrid large-sieve core has sharpened to a near-equal-product dispersion
problem. The main task is to control off-diagonal multiplicative energy with
small-modulus oscillation and major-arc exclusion in the balanced range.
