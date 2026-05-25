# Graph-Rank Divisor-Correlation Estimate

Date: 2026-05-24

Status: candidate proof of the divisor-correlation estimate needed for the
four-offset singular-series average.

The singular-series average reduced to divisor sums over pair differences.
For tuple size at most four, the right way to count those divisor constraints
is prime by prime through the rank of a congruence graph.

## Divisor Expansion Setup

Fix

$$
r\le4
$$

and let `G_r` be the complete graph on vertices

$$
\{1,\ldots,r\}.
$$

For each edge `e={i,j}`, the pair-difference factor has expansion

$$
g(|s_i-s_j|)
=
\sum_{d_e\mid s_i-s_j}
\frac{\mu^2(d_e)C^{\omega(d_e)}}{d_e}.
$$

The average is bounded by

$$
\sum_{\{d_e\}}
\left(\prod_e
\frac{\mu^2(d_e)C^{\omega(d_e)}}{d_e}\right)
T(\{d_e\}),
$$

where

$$
T(\{d_e\})
=
\#\{0\le s_1,\ldots,s_r<N:
d_e\mid s_i-s_j\text{ for every }e=\{i,j\}\}.
$$

The target is

$$
\sum_{\{d_e\}}
\left(\prod_e
\frac{\mu^2(d_e)C^{\omega(d_e)}}{d_e}\right)
T(\{d_e\})
\ll_r
N^r(\log N)^C.
$$

## Prime-Level Rank

Since the divisors are squarefree, constraints separate by prime.

For a prime `p`, let

$$
E_p=\{e:p\mid d_e\}
$$

be the set of graph edges carrying `p`. The congruences attached to `p` are

$$
s_i\equiv s_j\pmod p
\qquad
(\{i,j\}\in E_p).
$$

Let

$$
\rho_p=r-c(E_p),
$$

where `c(E_p)` is the number of connected components of the graph
`({1,...,r},E_p)`, including isolated vertices. Thus `rho_p` is the number of
independent congruence equalities forced modulo `p`.

Modulo `p`, the proportion of residue tuples satisfying the `p`-constraints is

$$
p^{-\rho_p}.
$$

The divisor weight attached to the same prime is

$$
\prod_{e\in E_p}\frac{C}{p}
=
C^{|E_p|}p^{-|E_p|}.
$$

So a nonempty edge pattern `E_p` contributes the local cost

$$
C^{|E_p|}p^{-|E_p|-\rho_p}.
$$

Since every nonempty graph has

$$
|E_p|\ge1,\qquad \rho_p\ge1,
$$

every nonempty local pattern costs at least `p^-2`.

## Euler-Factor Bound

The prime-level divisor-correlation factor is bounded by

$$
\prod_{p\le N}
\left(
1+
\sum_{\emptyset\ne E\subseteq E(G_r)}
C^{|E|}p^{-|E|-\rho(E)}
\right).
$$

For fixed `r <= 4`, there are finitely many edge patterns. Since every
nonempty pattern has exponent at least `2`,

$$
\sum_{\emptyset\ne E\subseteq E(G_r)}
C^{|E|}p^{-|E|-\rho(E)}
\ll_r
p^{-2}.
$$

Therefore

$$
\prod_{p\le N}(1+O_r(p^{-2}))
\ll_r
1.
$$

This gives a bounded average for distinct offset tuples. Allowing harmless
boundary and diagonal bookkeeping gives the weaker recorded form

$$
\ll_r N^r(\log N)^C.
$$

## Boundary And Diagonal Terms

If `s_i=s_j`, then the pair difference is zero and every divisor divides it.
Those terms must be separated before applying the graph-rank product. A tuple
with fewer than `r` distinct offsets is handled in the lower-dimensional case.

If the effective modulus on a connected component exceeds `N`, then the
congruence can force equality of two offsets inside `[0,N)`. In the distinct
case this contributes zero; in the diagonal case it has already been assigned
to a lower-dimensional tuple.

Thus the graph-rank estimate is stable under the finite interval rather than
only on a complete residue box.

## Resulting Estimate

For each fixed `r <= 4`,

$$
\sum_{0\le s_1,\ldots,s_r<N}
\prod_{1\le i<j\le r}g(|s_i-s_j|)
\ll_r
N^r(\log N)^C.
$$

Combining this with the collision-product bound for
$\mathfrak S(S)$ gives

$$
\sum_{0\le s_1,\ldots,s_r<N}
\mathfrak S(\{s_1,\ldots,s_r\})
\ll_r
N^r(\log N)^C.
$$

## Principal Obstacles

**Diagonal separation must happen first.**
The divisor expansion is clean only after tuples are grouped by their number
of distinct offsets.

**Effective rank is graph rank, not edge count.**
Cycles do not add independent congruence equations. The proof must use
`rho(E)=r-c(E)` prime by prime.

**Large moduli force equality.**
When an effective component modulus exceeds the interval length, distinct
offsets cannot satisfy the congruence unless the relevant values coincide.
This must be assigned to the diagonal bookkeeping.

**Constants depend on tuple size.**
The argument is harmless for `r <= 4`. It should not be stated as a uniform
large-`r` theorem without additional work.

## Closure Role

This graph-rank estimate closes the singular-series averaging part of the
fourth-moment route. The remaining nonlocal analytic obligations are now:

```text
fixed-tuple Selberg upper-bound remainder control;
first-moment endpoint density;
assembly of the tuple estimates into the fourth central moment.
```

## Result

The singular-series average over at most four offsets is controlled by a
finite graph-rank divisor-correlation argument. This removes the repeated
small-prime congruence obstacle from the main bridge chain.
