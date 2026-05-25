# Direct Short-Interval Endpoint Fourth-Moment Strategy

Date: 2026-05-24

Status: proof-strategy note for the direct concentration route.

The direct route targets the endpoint count in moving intervals, without first
proving individual factorial-moment asymptotics for every offset tuple.

## Object

For even centers `M in [X,2X]` and `N <= X/2`, define

$$
P_N(M)=\#\{p\in\mathbb P:M-2N<p<M\}.
$$

The required concentration estimate is

$$
\sum_{\substack{X\le M\le2X\\2\mid M}}
\left|
P_N(M)-\frac{2N}{\log X}
\right|^4
\ll
X\left(\frac{N}{\log X}\right)^2(\log X)^C
$$

in the nontrivial range. This is the direct short-interval version of the
Fourth-Moment Endpoint Concentration Lemma.

## Moving-Interval Expansion

As `M` varies, each endpoint prime `p` contributes to all centers

$$
p<M<p+2N.
$$

Thus

$$
P_N(M)=
\sum_p 1_{p<M<p+2N}.
$$

The fourth moment expands into overlap counts of four prime-generated
intervals. A product

$$
1_{p_1<M<p_1+2N}\cdots 1_{p_4<M<p_4+2N}
$$

contributes the length of the intersection

$$
(\min_i(p_i+2N)-\max_i p_i)_+,
$$

restricted to even `M in [X,2X]`.

Therefore the direct fourth moment is a centered four-point endpoint
additive-energy estimate at scale `2N`.

## Candidate Proof Shape

The proof should establish a discrete Selberg-integral bound:

> **Endpoint Selberg Fourth Integral.**
> For `1 <= N <= X/2`,
> $$
> \sum_{\substack{X\le M\le2X\\2\mid M}}
> \left|
> P_N(M)-\frac{2N}{\log X}
> \right|^4
> \ll
> X\left(\frac{N}{\log X}\right)^2(\log X)^C.
> $$

A direct proof has three parts.

1. **Mean normalization.**
   Use endpoint density to replace the average of `P_N(M)` by
   `2N/log X` up to an error small enough for the fourth moment.

2. **Centered expansion.**
   Expand the fourth power after subtracting the mean. The main fourth-power
   terms must cancel down to Poisson scale. This is where direct concentration
   differs from one-sided tuple upper bounds.

3. **Endpoint four-energy bound.**
   Bound the centered four-point overlap sum for primes whose pairwise spans
   are at most `2N`.

## Dyadic Even-Center Handling

The even-center restriction changes only constants. Since all relevant primes
are odd, `p<M` with `M` even is the natural parity-compatible endpoint
sampling. The overlap length in `M` is halved up to endpoint error.

The dyadic boundary is already closed:

```text
N <= X/2 -> shifted endpoint-density range applies;
N > X/2  -> complete-cover event is empty by Bertrand half-reset.
```

Thus the direct concentration theorem only needs `N <= X/2`.

## Required Inputs

**Endpoint density with usable error.**
The mean must satisfy

$$
\sum_{2\mid M}P_N(M)
=
\frac{X}{2}\frac{2N}{\log X}
+O\!\left(X^{1/2}\left(\frac{N}{\log X}\right)(\log X)^C\right)
$$

or any error that is harmless in the fourth-moment expansion.

**Centered four-energy estimate.**
The prime endpoint set must satisfy a scale-`N` centered four-point energy
bound strong enough to produce the Poisson-size fourth moment.

**Diagonal accounting.**
Configurations where some primes coincide generate the expected lower-order
Poisson terms. They must be retained with the correct coefficients, not thrown
into a crude error.

**Off-diagonal cancellation or dispersion.**
Four distinct endpoints in overlapping windows must not contribute at the
`mu^4` scale after centering. This is the main analytic burden.

## Obstacles

**The estimate is stronger than an upper-bound sieve.**
A one-sided Selberg upper bound controls how large tuple counts can be. It
does not provide the centered cancellation needed here.

**Short intervals are the hard regime.**
When `N` is near the mean prime spacing scale, fluctuations are large and the
final `log^B` allowance must absorb the small-mean range. The concentration
argument should be reserved for `N/log X` large.

**Unweighted endpoints are required.**
A theorem for weighted `Lambda` sums does not immediately imply the required
unweighted endpoint count unless a transfer step controls prime powers and
large weights.

**Uniformity in `N`.**
The estimate must hold across the dyadic range `1 <= N <= X/2`, with small
`N` handled trivially and large `N` controlled by the fourth-moment theorem.

## Result

The direct concentration route reduces the remaining obstruction to a
short-interval endpoint Selberg fourth integral. Proving that integral supplies
the Fourth-Moment Endpoint Concentration Lemma and closes the uncovered-set
extinction tail.
