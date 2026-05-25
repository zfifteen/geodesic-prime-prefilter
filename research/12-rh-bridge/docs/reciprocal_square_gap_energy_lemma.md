# Reciprocal Square-Gap Energy Lemma

Date: 2026-05-24

Status: conditional endpoint-counterterm lemma and proof-state reduction.

The leading endpoint counterterm is controlled by consecutive zero-excess
returns. For consecutive prime endpoints `p(q)<q`, write

$$
g(q)=q-p(q).
$$

The endpoint drift leading term is

$$
E_X^{(1)}(z)
=
{1\over 2z}
\sum_{q\le X}\log q\log {q\over p(q)}.
$$

The required leading finite part follows from one reciprocal energy estimate.

## Lemma

Assume

$$
\boxed{
\sum_q {g(q)^2\log q\over q^2}<\infty.
}
$$

Then the endpoint log-gap summatory law has a finite part:

$$
G(X):=
\sum_{q\le X}\log q\log {q\over p(q)}
=
{1\over2}(\log X)^2+C_{\mathrm{eg}}+o(1).
$$

Consequently,

$$
\operatorname{F.p.}E_X^{(1)}(z)
=
{C_{\mathrm{eg}}\over 2z}.
$$

## Proof

Set

$$
f(x)={\log x\over x}.
$$

The endpoint occupancy sum is

$$
O(X)=\sum_{q\le X}g(q)f(q).
$$

The harmonic reference is

$$
H(X)=\sum_{2<n\le X}f(n)
=
{1\over2}(\log X)^2+C_{\mathrm{harm}}+o(1).
$$

On each chamber `(p,q]`, the sampling error is

$$
\sum_{n=p+1}^{q}(f(q)-f(n)).
$$

Since

$$
f'(x)={1-\log x\over x^2},
$$

the mean-value theorem gives, for all sufficiently large `q`,

$$
\left|
\sum_{n=p+1}^{q}(f(q)-f(n))
\right|
\ll
{g(q)^2\log q\over q^2}.
$$

The assumed reciprocal square-gap energy therefore makes

$$
O(X)-H(X)
$$

converge to a finite constant `C_occ`.

The log-gap nonlinear correction is

$$
N(X)=
\sum_{q\le X}\log q
\left[
\log {q\over p(q)}-{g(q)\over q}
\right].
$$

For consecutive prime endpoints, `g(q)/q` is bounded away from `1` after the
finite base. The Taylor remainder for `-\log(1-u)` gives

$$
\left|
\log {q\over p(q)}-{g(q)\over q}
\right|
\ll
{g(q)^2\over q^2}.
$$

Thus the same reciprocal square-gap energy makes `N(X)` converge to a finite
constant `C_nonlin`.

Combining the harmonic reference, endpoint sampling error, and nonlinear
log-gap correction gives

$$
G(X)
=
H(X)+C_{\mathrm{occ}}+C_{\mathrm{nonlin}}+o(1)
=
{1\over2}(\log X)^2+C_{\mathrm{eg}}+o(1),
$$

with

$$
C_{\mathrm{eg}}
=
C_{\mathrm{harm}}+C_{\mathrm{occ}}+C_{\mathrm{nonlin}}.
$$

This proves the leading endpoint finite part.

## Dyadic Form

It is sufficient to prove the dyadic zero-excess return square moment

$$
\sum_{X<q\le2X}g(q)^2
\ll
X(\log X)^B
$$

for a fixed exponent `B`. On a dyadic block,

$$
\sum_{X<q\le2X}{g(q)^2\log q\over q^2}
\ll
{(\log X)^{B+1}\over X}.
$$

The sum over `X=2^k` converges. Thus the dyadic square-moment theorem implies
the reciprocal square-gap energy lemma.

## PGS Reduction

In PGS language, primes are zero-excess endpoints and `g(q)` is the return
time from one zero-excess endpoint to the next. The missing arithmetic input is

> **Zero-Excess Return Square-Moment Theorem.**
> $$
> \sum_{X<q\le2X}(q-p(q))^2
> \ll
> X(\log X)^B.
> $$

This is the exact global invariant needed for the leading endpoint finite
part. It is stronger than local GWR ordering because it counts how often long
positive-excess chambers occur across a dyadic block.

The strongest current source-side route is the age-divisor recurrence
potential

$$
\Phi(n)=(n-p(n))(\tau(n)-2).
$$

Inside a chamber, `n-p(n)` is the zero-excess age and `tau(n)-2` is positive.
A dyadic bound

$$
\sum_{X<n\le2X}\Phi(n)
\ll
X(\log X)^B
$$

would dominate the quadratic chamber-age cost and imply the zero-excess
return square-moment theorem, up to dyadic boundary terms.

## Existing Inputs

`PROOF.md` supplies the universal local facts needed to identify the chamber
objects:

- primes are exactly the zero-excess integers;
- chamber interiors are positive-excess integers;
- the GWR selector is the leftmost interior minimum-excess point.

The endpoint-chain and reciprocal-transport notes supply the correct global
coordinate for the counterterm. They do not prove a frequency theorem for long
zero-excess return times.

Therefore the leading endpoint finite part is reduced to one remaining PGS
arithmetic gate:

```text
prove the Zero-Excess Return Square-Moment Theorem,
or prove the endpoint sampling and nonlinear log-gap finite parts directly.
```

The age-divisor energy bound is the cleanest current candidate for proving
that gate from PGS source data.
