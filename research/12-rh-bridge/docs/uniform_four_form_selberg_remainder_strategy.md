# Uniform Four-Form Selberg Remainder Strategy

Date: 2026-05-24

Status: candidate proof strategy for the uniform fixed-tuple Selberg upper
bound with summable errors.

The remaining analytic input in the uncovered-set route is a uniform upper
bound for shifted odd linear forms

$$
M-(2s+1)
$$

for distinct offset sets of size at most four. The needed estimate is a
standard finite-level Selberg upper-bound sieve with dyadic parity handled
explicitly.

## Fixed Offset Set

Let

$$
S=\{s_1,\ldots,s_r\},
\qquad
r\le4,
$$

be a set of distinct offsets with `0 <= s_i < N` and `N <= X/2+O(1)`.

For each odd prime `p`, define

$$
\nu_p(S)=
\#\{2s+1\pmod p:s\in S\}.
$$

If `nu_p(S)=p` for some odd prime `p`, then every center hits a forbidden
class modulo `p`, so the sifted count is zero. Assume from now on that `S` is
admissible.

Let

$$
\mathcal N_S(X)
$$

be the number of even `M in [X,2X]` such that no form `M-(2s+1)` has an odd
prime divisor `p <= sqrt(2X)`.

## Finite Sieve Level

Set

$$
z=\sqrt{2X}
$$

and choose a finite Selberg level

$$
D=X^{1/4}.
$$

The sieve uses squarefree odd divisors

$$
d\le D,
\qquad
d\mid P(z)=\prod_{3\le p\le z}p.
$$

For such `d`, the number of even centers in the forbidden classes modulo `d`
is

$$
A_d(S)
=
\frac{X}{2}\frac{\nu_d(S)}d
+R_d(S),
$$

where

$$
\nu_d(S)=\prod_{p\mid d}\nu_p(S)
$$

and, by direct residue counting in the dyadic interval,

$$
R_d(S)\ll_r \nu_d(S)\ll_r r^{\omega(d)}.
$$

Parity is harmless because `d` is odd: each residue class modulo `d`
contains half even and half odd representatives over a full `2d` period, with
only endpoint error.

## Selberg Denominator

For the upper-bound sieve, define

$$
g_S(p)=\frac{\nu_p(S)}{p-\nu_p(S)}
$$

and extend multiplicatively. The Selberg denominator is

$$
G_S(D)=
\sum_{\substack{d\le D\\d\mid P(z)}}
\mu^2(d)g_S(d).
$$

The fixed-dimension lower bound needed is

$$
G_S(D)
\gg_r
\mathfrak S(S)^{-1}(\log D)^r.
$$

Since `log D` is a fixed positive fraction of `log X`, this gives

$$
\frac{X}{G_S(D)}
\ll_r
X\mathfrak S(S)/(\log X)^r.
$$

This is the desired main term.

## Remainder Control

Selberg's quadratic majorant gives

$$
\mathcal N_S(X)
\le
\frac{X}{2G_S(D)}
+E_S(X),
$$

with a remainder bounded by sums of residue-count errors at moduli
`[d_1,d_2]` with `d_1,d_2 <= D`.

Using

$$
R_q(S)\ll_r r^{\omega(q)}
$$

for squarefree odd `q`, one obtains the uniform crude bound

$$
E_S(X)
\ll_r
D^2(\log D)^{C_r}
\ll
X^{1/2}(\log X)^{C_r}.
$$

This is deliberately stronger than needed in structure and weaker than needed
in constants. It is enough because the error must be summed over at most
`N^r` offset tuples:

$$
\sum_{s_1,\ldots,s_r<N}E_S(X)
\ll
N^rX^{1/2}(\log X)^{C_r}.
$$

The target moment scale is

$$
X N^r(\log X)^C/(\log X)^r.
$$

For large `X`, the `X^{1/2}` remainder is absorbed into that target after
increasing the logarithmic exponent. Small `X` belongs to the finite base.

## Resulting Fixed-Tuple Bound

For every admissible distinct offset set `S` with `r <= 4`,

$$
\mathcal N_S(X)
\ll_r
X\mathfrak S(S)/(\log X)^r
+X^{1/2}(\log X)^{C_r}.
$$

After summing over offset tuples and applying the graph-rank singular-series
average, this gives the required raw moment upper bounds through order four.

## Principal Obstacles

**Denominator lower bound with singular factor.**
The proof must show

$$
G_S(D)\gg \mathfrak S(S)^{-1}(\log D)^r
$$

uniformly over all admissible offset sets `S` of size `r <= 4`.

**Remainder summability.**
The finite-level choice must make the accumulated Selberg remainders smaller
than the moment scale after summing over all offset tuples.

**Admissibility detection.**
Tuples with `nu_p(S)=p` for a small odd prime contribute zero and should be
removed before applying the denominator estimate.

**Boundary positivity.**
The range `N <= X/2+O(1)` and Bertrand closure ensure that shifted values are
in the relevant positive endpoint range except for endpoint errors.

**Analytic import status.**
This is a standard Selberg upper-bound sieve input. It is not currently a
theorem of `PROOF.md` unless the Selberg sieve is incorporated into the PGS
bridge as an allowed analytic component.

## Closure Role

This note supplies the strategy for the main remaining tuple input:

```text
finite-level Selberg upper bound
+ summable X^(1/2) remainders
+ graph-rank singular-series average
-> raw moments of uncovered survivor count through order four.
```

The remaining step after this is the algebraic assembly of raw moment bounds
into the fourth central moment required for extinction.
