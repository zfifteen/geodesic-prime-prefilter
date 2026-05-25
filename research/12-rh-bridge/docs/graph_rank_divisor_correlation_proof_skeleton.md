# Graph-Rank Divisor-Correlation Proof Skeleton

Date: 2026-05-24

Status: proof skeleton for the graph-rank divisor-correlation estimate.

This note upgrades the graph-rank estimate from a route to a proof skeleton.
The estimate is finite-dimensional because the tuple size is at most four.

## Proposition

Fix `r <= 4` and define

$$
g(n)=\prod_{p\mid n}\left(1+\frac{C}{p}\right).
$$

Then

$$
\sum_{0\le s_1,\ldots,s_r<N}
\prod_{1\le i<j\le r}g(|s_i-s_j|)
\ll_{r,C}
N^r(\log N)^{C_r}.
$$

After diagonal splitting, this gives the singular-series average required in
the fourth-moment route.

## Step 1: Remove Diagonals

Partition tuples by the equivalence relation

$$
i\sim j
\quad\Longleftrightarrow\quad
s_i=s_j.
$$

Each diagonal class reduces the number of distinct offset variables. It is
therefore handled by the same proposition with smaller `r`. It is enough to
prove the bound for tuples with all `s_i` distinct.

For distinct tuples, every difference satisfies

$$
1\le |s_i-s_j|<N.
$$

Thus every divisor appearing in the expansion below is at most `N`.

## Step 2: Expand Pair Factors

Use

$$
g(n)=
\sum_{d\mid n}
a(d),
\qquad
a(d)=\frac{\mu^2(d)C^{\omega(d)}}d.
$$

Then the distinct-tuple contribution is at most

$$
\sum_{\{d_e\}}
\left(\prod_{e}a(d_e)\right)
T(\{d_e\}),
$$

where edges `e={i,j}` range over the complete graph `G_r`, all `d_e <= N`,
and

$$
T(\{d_e\})
=
\#\{0\le s_1,\ldots,s_r<N:
d_e\mid s_i-s_j\text{ for every }e=\{i,j\}\}.
$$

## Step 3: Lattice Index

For a prime `p`, let

$$
E_p=\{e:p\mid d_e\}.
$$

The congruences attached to `p` force equality modulo `p` along the graph
`({1,\ldots,r},E_p)`. Let

$$
\rho_p=r-c(E_p)
$$

be its graph rank. By the Chinese remainder theorem, the full congruence
lattice has index

$$
\mathcal I(\{d_e\})
=
\prod_p p^{\rho_p}.
$$

A standard box count for a lattice of index `I` in fixed dimension gives

$$
T(\{d_e\})
\ll_r
\frac{N^r}{\mathcal I(\{d_e\})}
+N^{r-1}(\log N)^{C_r}.
$$

The second term absorbs boundary effects and cases where a large component
modulus forces equality inside the finite interval.

## Step 4: Main Divisor Sum

The main divisor sum is

$$
\sum_{\{d_e\}}
\left(\prod_e a(d_e)\right)
\frac1{\mathcal I(\{d_e\})}.
$$

It factors prime by prime. For each prime `p`, choose the subset

$$
E\subseteq E(G_r)
$$

of edges whose divisor is divisible by `p`. The local contribution is

$$
C^{|E|}p^{-|E|}p^{-\rho(E)}.
$$

Thus the Euler product is

$$
\prod_{p\le N}
\left(
1+\sum_{\emptyset\ne E\subseteq E(G_r)}
C^{|E|}p^{-|E|-\rho(E)}
\right).
$$

Every nonempty `E` has

$$
|E|\ge1,
\qquad
\rho(E)\ge1,
$$

so each nonempty local term is `O_{r,C}(p^-2)`. Therefore

$$
\prod_{p\le N}(1+O_{r,C}(p^{-2}))
\ll_{r,C}
1.
$$

The main term contributes `O(N^r)`.

## Step 5: Boundary Sum

For the boundary term, use

$$
\sum_{d\le N}a(d)
=
\prod_{p\le N}\left(1+\frac{C}{p}\right)
\ll_C
(\log N)^C.
$$

There are only

$$
\binom r2\le6
$$

edges. Hence

$$
N^{r-1}
\sum_{\{d_e\}}\prod_e a(d_e)
\ll_{r,C}
N^{r-1}(\log N)^{C_r}
\ll
N^r(\log N)^{C_r}.
$$

This completes the divisor-correlation estimate.

## Effective-Rank Obstacles Addressed

**Shared primes across several edges.**
The same prime may divide several `d_e`. The proof handles this by assigning
that prime to the whole edge subset `E_p` and using graph rank
`rho(E_p)`, not the number of edges.

**Cycles.**
A triangle of congruences modulo `p` has three edges but rank two. The local
cost is still at least

$$
p^{-3}p^{-2}=p^{-5},
$$

so cycles are harmless.

**Large component moduli.**
When combined congruences on a component force equality inside `[0,N)`, the
case is diagonal or empty. The proof isolates diagonals first and absorbs the
finite-box boundary in the `N^{r-1}` term.

## Closure

The graph-rank divisor-correlation estimate is proved at proof-skeleton
level. Combined with the collision-product bound, it proves the
polylogarithmic singular-series average for offset tuples of size at most
four.

The remaining bridge obligations are now upstream analytic estimates:

```text
fixed-tuple Selberg upper-bound with uniform remainder;
first-moment endpoint density;
fourth-central-moment assembly for the uncovered survivor count.
```
