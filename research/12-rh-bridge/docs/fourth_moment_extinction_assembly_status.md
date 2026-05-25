# Fourth-Moment Extinction Assembly Status

Date: 2026-05-24

Status: assembly note integrating endpoint-density, boundary closure, and the
remaining tuple-sieve inputs.

The uncovered-set route now has its first-moment and boundary pieces separated.
The remaining task is to assemble them with tuple-sieve bounds into the
`H^-2` odd-offset covering tail.

## Target Tail

For even centers `M in [X,2X]`, let

$$
a(M)=M-p(M).
$$

The odd-offset covering tail asks for

$$
\#\{M\in[X,2X]:2\mid M,\ a(M)\ge H\}
\ll
X(\log X)^B/H^2.
$$

Write

$$
H=2N+O(1).
$$

If `a(M) >= H`, then the first `N` odd offsets behind `M` contain no
zero-excess endpoint. In uncovered-set notation,

$$
Z_N(M)=0.
$$

So it is enough to prove

$$
\#\{M:Z_N(M)=0\}
\ll
X(\log X)^B/N^2.
$$

## Accepted Inputs Now In Place

### First-Moment Endpoint Density

For the interior range

$$
N\le X/2+O(1),
$$

the shifted endpoint-density note gives

$$
\sum_{2\mid M}Z_N(M)
\gg
\frac{XN}{\log X}.
$$

Thus

$$
\mu_N=
\frac{2}{X}\sum_{2\mid M}Z_N(M)
\gg
\frac{N}{\log X}.
$$

This input is analytic unless reproved from PGS endpoint-chain structure.

### Long-Offset Boundary Closure

Bertrand's postulate gives

$$
p(M)>M/2,
$$

so for `M in [X,2X]`,

$$
a(M)<X.
$$

Therefore the extinction event for `H >= X` is empty, and the fourth-moment
argument only needs the range

$$
N\le X/2+O(1).
$$

This closes the dyadic boundary attached to the first-moment input.

### Singular-Series Average

For tuple size at most four, singular-series averaging has been reduced to and
controlled by the graph-rank divisor-correlation skeleton:

$$
\sum_{s_1,\ldots,s_k<N}
\mathfrak S(\{s_1,\ldots,s_k\})
\ll_k
N^k(\log N)^C
\qquad (k\le4).
$$

This removes the repeated-small-prime collision obstacle at the level needed
for fourth moments.

## Remaining Main Input

The central unresolved analytic input is now the fixed-tuple Selberg upper
bound for shifted odd forms:

> **Uniform Four-Form Selberg Bound.**
> For every distinct offset set `S` with `r <= 4`,
> $$
> \mathcal N_S(X)
> \ll_r
> X\mathfrak S(S)/(\log X)^r
> +E_S(X),
> $$
> with total error over `s_i<N` absorbed into the fourth-moment scale.

Here `N_S(X)` counts even centers for which every form

$$
M-(2s+1),
\qquad s\in S,
$$

survives all odd prime channels up to `sqrt(2X)`.

Once this fixed-tuple bound is available, the singular-series average gives
raw moment bounds for

$$
Z_N(M)=\sum_{s<N}I_s(M)
$$

through order four.

## Moment Assembly

The needed assembly statement is:

> **Fourth Central Moment Assembly.**
> From the first-moment lower bound and the tuple bounds for `k <= 4`, prove
> $$
> \frac1X\sum_{2\mid M}|Z_N(M)-\mu_N|^4
> \ll
> \mu_N^2(\log X)^C
> $$
> for the nontrivial range of `N`.

Then extinction gives

$$
\#\{M:Z_N(M)=0\}
\le
X\frac{\mu_N^2(\log X)^C}{\mu_N^4}
\ll
X(\log X)^{C+2}/N^2.
$$

For small `N`, where the right side exceeds the trivial bound `O(X)`, no
moment input is needed after increasing `B`.

## Precise Remaining Inputs

1. **Uniform fixed-tuple Selberg upper bound.**
   This is the main analytic theorem still not written as a proof.

2. **Total Selberg remainder control.**
   The fixed-tuple error terms must remain summable over all offset tuples
   with `k <= 4`.

3. **Fourth central moment algebra.**
   Raw tuple moment estimates must be assembled into the centered fourth
   moment with the correct `mu_N^2` scale.

4. **Source-status decision.**
   Endpoint density and Bertrand can be imported analytically or restated as
   PGS endpoint-chain lemmas. They are not consequences of the local GWR
   theorem in `PROOF.md`.

## Bridge Consequence

If the remaining fixed-tuple Selberg and moment-assembly inputs are supplied,
then the chain becomes:

```text
four-form Selberg bounds
+ graph-rank singular average
+ endpoint-density mean
+ Bertrand boundary closure
-> fourth central moment for uncovered survivors
-> shifted-sieve extinction estimate
-> essential shifted-cover weight
-> canonical least-divisor word entropy
-> odd divisor-covering H^-2 tail
-> even-channel age recurrence
-> zero-excess square-moment bound
-> reciprocal endpoint occupancy
-> finite-part packet balance route
```

## Result

The remaining bridge inside the uncovered-set route is now sharply isolated:
prove the uniform fixed-tuple Selberg upper bound with summable remainders and
perform the fourth-central-moment assembly. The first-moment and long-offset
boundary pieces are no longer the active obstruction.
