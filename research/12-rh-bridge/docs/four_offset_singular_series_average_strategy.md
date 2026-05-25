# Four-Offset Singular-Series Average Strategy

Date: 2026-05-24

Status: candidate combinatorial proof route for the singular-series average
needed by the four-tuple sifted moment bound.

The fixed-tuple Selberg bound leaves one finite averaging problem: singular
factors must not become large too often when the offsets range over
`0 <= s_i < N`. For tuples of size at most four, this is controlled by
pairwise congruence collisions.

## Target

For an offset set

$$
S=\{s_1,\ldots,s_r\},
\qquad
r\le4,
$$

define

$$
\nu_p(S)=\#\{2s+1\pmod p:s\in S\}
$$

and

$$
\mathfrak S(S)=
\prod_{p>2}
\left(1-\frac{\nu_p(S)}p\right)
\left(1-\frac1p\right)^{-r}.
$$

The needed bound is

$$
\sum_{0\le s_1,\ldots,s_r<N}
\mathfrak S(\{s_1,\ldots,s_r\})
\ll_r
N^r(\log N)^C.
$$

Repeated offsets reduce the distinct dimension and are lower-order diagonal
terms.

## Collision Product Bound

Let

$$
\Delta(S)=
\prod_{1\le i<j\le r}|s_i-s_j|
$$

for distinct offsets.

For primes `p` not dividing `Delta(S)` and `p > r`, all offsets are distinct
modulo `p`, so

$$
\nu_p(S)=r
$$

and the local factor is

$$
\left(1-\frac rp\right)\left(1-\frac1p\right)^{-r}
=
1+O_r(p^{-2}).
$$

These non-collision primes contribute a bounded product.

If `p | Delta(S)`, then at least two offsets collide modulo `p`. The local
factor is bounded by

$$
1+O_r(1/p)
$$

up to an absolute factor depending only on `r`.

Therefore

$$
\mathfrak S(S)
\ll_r
\prod_{p\mid\Delta(S)}
\left(1+\frac{C_r}{p}\right).
$$

Equivalently, for a multiplicative function

$$
g(n)=\prod_{p\mid n}\left(1+\frac{C_r}{p}\right),
$$

one has

$$
\mathfrak S(S)
\ll_r
\prod_{1\le i<j\le r}g(|s_i-s_j|).
$$

This reduces singular-series averaging to a divisor-correlation estimate over
pair differences.

## Divisor Expansion

The pair factor has the squarefree divisor expansion

$$
g(n)=
\sum_{d\mid n}
\frac{\mu^2(d)C_r^{\omega(d)}}{d}.
$$

Thus the average of the product over pairs expands into sums over edge
divisors

$$
d_{ij}\mid s_i-s_j
\qquad
(1\le i<j\le r).
$$

For fixed edge divisors, the congruences define a graph on at most four
vertices. The number of offset tuples satisfying those congruences is bounded
by

$$
O_r(N^r/Q(d_{ij})+N^{r-1}(\log N)^C),
$$

where `Q(d_ij)` is the effective modulus rank forced by the graph. Since
`r <= 4`, the resulting divisor sums are finite-polylogarithmic:

$$
\sum_{d_{ij}}
\prod_{i<j}\frac{\mu^2(d_{ij})C_r^{\omega(d_{ij})}}{d_{ij}}
\frac1{Q(d_{ij})}
\ll_r
(\log N)^C.
$$

This gives

$$
\sum_{s_1,\ldots,s_r<N}
\mathfrak S(S)
\ll_r
N^r(\log N)^C.
$$

## Gallagher-Type Interpretation

This is the same structural content as the classical average-singular-series
phenomenon: over a large box of shifts, the singular series has bounded mean
for fixed tuple size. The present proof only needs the weak polylogarithmic
upper bound for `r <= 4`, not an asymptotic formula.

## Principal Obstacles

**Diagonal bookkeeping.**
Repeated offsets make `Delta(S)=0`. These cases must be split by the number
of distinct offsets before applying the collision-product bound.

**Small inadmissible primes.**
If the offsets cover every residue modulo `p`, the singular series is zero.
The proof should remove these tuples or let the zero factor handle them before
using upper bounds.

**Graph congruence rank.**
When several edge divisors share primes, the congruence constraints are not
independent. The divisor-expansion proof must use the effective rank of the
congruence graph rather than multiply pair constraints as if independent.

**Uniform constants.**
The bound must be uniform for all `N` in the dyadic tail argument. Since
`r <= 4`, all constants can depend on `r` but not on `N` or `X`.

## Closure Role

Once this singular-series average is combined with the fixed-tuple Selberg
upper bound, the four-tuple sifted moment estimate follows:

$$
\sum_{s_1,\ldots,s_k<N}
\mathcal N_{\{s_1,\ldots,s_k\}}(X)
\ll_k
X N^k(\log X)^C/(\log X)^k
\qquad
(k\le4).
$$

That is the tuple input needed for the fourth central moment of the uncovered
survivor count.

## Result

The singular-series average is not the main obstruction. For tuple size at
most four it reduces to a finite pair-collision divisor estimate, or
equivalently to a weak Gallagher average. The harder analytic inputs remain
the fixed-tuple Selberg upper bound, the first-moment endpoint density, and
the assembly of those estimates into the fourth central moment.
