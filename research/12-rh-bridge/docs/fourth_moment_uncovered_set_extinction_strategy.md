# Fourth-Moment Uncovered-Set Extinction Strategy

Date: 2026-05-24

Status: candidate analytic route for the Shifted Sieve Extinction Estimate.

The second moment of the uncovered set gives at best an inverse-mean
extinction bound. The required tail has an inverse-square shape. The natural
analytic route is therefore a fourth-moment bound for the uncovered-set
survivor count.

## Survivor Count

Let

$$
Y=\sqrt{2X}
$$

and define

$$
Z(M)=|U_Y(M)|
$$

for even centers `M in [X,2X]`. Equivalently, `Z(M)` is the number of odd
offsets

$$
M-(2s+1),
\qquad
0\le s<N,
$$

with no odd prime divisor up to `sqrt(2X)`. Away from the harmless `1`
boundary, these are exactly odd zero-excess endpoints in the backward window.

The extinction event is

$$
Z(M)=0.
$$

The expected size has sieve scale

$$
\mu
\asymp
\frac{N}{\log X}.
$$

## Fourth Moment Suffices

If one can prove

$$
\frac1X\sum_{\substack{M\in[X,2X]\\2\mid M}}
|Z(M)-\mu|^4
\ll
\mu^2(\log X)^C,
$$

then every extinct center contributes `mu^4` to the left side. Therefore

$$
\#\{M:Z(M)=0\}
\ll
X\frac{\mu^2(\log X)^C}{\mu^4}
=
X\frac{(\log X)^{C+2}}{N^2}.
$$

This is exactly the Shifted Sieve Extinction Estimate, with a larger
logarithmic exponent.

This is the first moment order that has the correct power. A variance bound
would give only

$$
X\log X/N,
$$

which is the earlier `H^-1` obstruction.

## Tuple Expansion

Expand

$$
Z(M)=\sum_{0\le s<N} I_s(M),
$$

where `I_s(M)=1` if `M-(2s+1)` survives all odd prime channels up to `Y`.

Moments of `Z` reduce to tuple sums over offsets. For a tuple

$$
\mathbf s=(s_1,\ldots,s_k),
\qquad
k\le 4,
$$

let

$$
\nu_p(\mathbf s)
=
\#\{s_1,\ldots,s_k\}\pmod p.
$$

The local sieve factor for simultaneous survival is

$$
\prod_{3\le p\le Y}
\left(1-\frac{\nu_p(\mathbf s)}p\right).
$$

For primes not dividing any difference `s_i-s_j`, one has
`\nu_p(\mathbf s)=k`. Collision primes create the singular-series correction.

The needed analytic estimate is:

> **Four-Tuple Sifted Moment Bound.**
> For `k <= 4`,
> $$
> \sum_{0\le s_1,\ldots,s_k<N}
> \mathfrak S(\mathbf s)
> \ll_k
> N^k(\log X)^C,
> $$
> where `S(s)` is the singular product coming from the collision primes, and
> the associated dyadic center count is bounded by
> $$
> \ll
> X\mathfrak S(\mathbf s)/(\log X)^k.
> $$

Together with the first-moment main term, this yields Poisson-size fourth
central moment and hence the extinction tail.

## Dyadic Arithmetic Form

The tuple-counting statement can be written without probability:

$$
\#\{M\in[X,2X]:
M-(2s_i+1)\text{ has no odd divisor }p\le Y
\text{ for }1\le i\le k\}
$$

is bounded by

$$
C_k X\mathfrak S(\mathbf s)/(\log X)^k
$$

for all offset tuples with `k <= 4`.

This is a Selberg-sieve upper-bound shape for the shifted odd linear forms

$$
M-(2s_i+1).
$$

The first moment also needs a lower bound of size

$$
\sum_{s<N}\sum_M I_s(M)
\gg
XN/\log X
$$

in the relevant range. That lower bound is what gives the positive mean
`mu`.

## Why This Is The Right Analytic Target

The previous reductions require

$$
\#\{M:U_Y(M)=\varnothing\}
\ll
X(\log X)^B/N^2.
$$

The fourth-moment strategy proves exactly this if the survivor count has
Poisson-scale fluctuations through order four. It does not require a
Cramer-strength exponential gap bound. It needs only enough fourth-moment
control to turn extinction into an inverse-square event.

## Principal Obstacles

**First-moment lower bound.**
The proof needs many surviving offsets on average:

$$
\mu\asymp N/\log X.
$$

In classical language this is a prime-counting input for the shifted odd
forms. In PGS language it is an endpoint-return density input.

**Four-tuple upper-bound sieve.**
The moment expansion needs uniform Selberg-type upper bounds for up to four
shifted forms. This is stronger than local divisor-count ordering and is not
recorded in `PROOF.md`.

**Singular-series averaging.**
Tuples with many repeated congruence classes modulo small primes have larger
local factors. The proof must show that the average singular-series weight
over all offset tuples remains polylogarithmic.

**Dyadic boundary and parity.**
The forms are odd and the center `M` is even. Boundary terms from
`M-(2s+1)<=1` and dyadic endpoints must be separated as finite or lower-order
contributions.

**Source-status separation.**
This route imports analytic sieve estimates unless those estimates are
reproved from PGS divisor-channel structure. It would close the entropy tail
as an analytic bridge, but it is not currently a consequence of the proved
GWR local theorem.

## Minimal Closure Statement

The next lemma to prove or import is:

> **Fourth-Moment Shifted-Sieve Lemma.**
> For `Y=sqrt(2X)` and odd-offset length `N`, the survivor count `Z(M)` over
> even centers `M in [X,2X]` satisfies
> $$
> \frac1X\sum_{2\mid M}|Z(M)-\mu|^4
> \ll
> \mu^2(\log X)^C,
> \qquad
> \mu\asymp N/\log X.
> $$

This lemma implies the Shifted Sieve Extinction Estimate, then the Essential
Shifted-Cover Weight Lemma, then the Canonical Least-Divisor Word Entropy
Theorem.

## Result

The shifted-sieve extinction problem has a concrete analytic attack:
prove a fourth central moment bound for the uncovered-set survivor count. This
is the first route in the current chain that naturally produces the required
`N^-2` tail.
