# Age-Divisor Recurrence Potential Candidate

Date: 2026-05-24

Status: candidate PGS recurrence potential for the Persistence-Energy
Inequality.

The Persistence-Energy Inequality needs a global potential that accumulates
quadratic cost during positive-excess runs and resets at zero-excess
endpoints.

The natural PGS-native candidate is age times divisor surplus.

## Definitions

Let

$$
a(n)=n-p(n),
$$

where `p(n)` is the largest prime not exceeding `n`. Thus `a(n)=0` at prime
endpoints and increases by one at each interior point of a chamber.

Define the divisor surplus

$$
\sigma(n)=\tau(n)-2.
$$

For `n > 1`,

$$
\sigma(n)=0
\iff
n\text{ is prime}.
$$

Inside a chamber interior, `sigma(n) >= 1`.

Define the recurrence potential

$$
\Phi(n)=a(n)\sigma(n)=a(n)(\tau(n)-2).
$$

In zero-excess notation,

$$
\sigma(n)=\frac{2E(n)}{\log n},
$$

so

$$
\Phi(n)=\frac{2a(n)E(n)}{\log n}.
$$

This is the normalized age-weighted excess.

## Per-Run Quadratic Cost

In a chamber `(p,q]` of width `g=q-p`, the endpoint `q` has `Phi(q)=0`, while
for interior points

$$
a(p+j)=j,
\qquad
\sigma(p+j)\ge1,
\qquad
1\le j<g.
$$

Therefore the chamber contributes at least

$$
\sum_{j=1}^{g-1}j
=
\frac{g(g-1)}2
$$

to the potential sum.

Thus a dyadic bound

$$
\sum_{X<n\le2X}\Phi(n)
\le
C X(\log X)^B
$$

would imply the dyadic gap second-moment bound

$$
\sum_{X<q\le2X}g(q)^2
\le
C'X(\log X)^B
$$

up to boundary terms.

## Candidate Theorem

> **Age-Divisor Energy Bound.**
> For every dyadic block `[X,2X]`,
> $$
> \sum_{X<n\le2X}
> (n-p(n))(\tau(n)-2)
> \le
> C X(\log X)^B.
> $$

This theorem is sufficient for the Persistence-Energy Inequality and hence for
the Reciprocal Gap-Energy Theorem.

## Divisor-Channel Expansion

The potential can be expanded through divisor channels:

$$
\sum_{X<n\le2X}a(n)\tau(n)
=
\sum_{d\le2X}
\sum_{\substack{X<n\le2X\\ d\mid n}}
a(n).
$$

Thus the age-divisor bound asks for a global estimate on how much
zero-excess age is carried by all divisor channels.

The subtraction of `2a(n)` removes the prime floor contribution:

$$
\sum_{X<n\le2X}a(n)(\tau(n)-2)
=
\sum_{d\le2X}
\sum_{\substack{X<n\le2X\\ d\mid n}}
a(n)
-
2\sum_{X<n\le2X}a(n).
$$

This identity is exact, but it is not yet a bound.

## Structural Ingredients Needed

To prove the Age-Divisor Energy Bound, the framework needs one of the
following.

1. **Divisor-channel age orthogonality.**
   Multiples of each divisor channel must not concentrate at large
   zero-excess ages often enough to violate the dyadic bound.

2. **Age reset recurrence.**
   The endpoint chain must reset age frequently enough, in aggregate, to
   control the divisor-channel weighted age.

3. **GWR-to-age transfer.**
   The selected minimum-excess point must control not only the minimum
   divisor load in a chamber, but also the accumulated age-divisor load of
   the whole chamber.

4. **Chamber energy invariant.**
   Each chamber must carry a computable energy budget whose sum over a dyadic
   block is `O(X(log X)^B)` and whose lower bound is quadratic in the chamber
   width.

## Main Obstacle

Current GWR machinery controls the local minimum of `E(n)` inside a chamber.
The candidate potential depends on the whole chamber:

$$
\sum_{p<n<q}(n-p)(\tau(n)-2).
$$

No theorem currently transfers local minimum-excess ordering into this
age-divisor energy bound.

The age-divisor potential is therefore a precise candidate, but proving its
dyadic total bound requires a new global recurrence argument.

## Result

The bridge target now has a concrete PGS-native recurrence potential:

$$
\Phi(n)=(n-p(n))(\tau(n)-2).
$$

If the Age-Divisor Energy Bound is proved, the endpoint-chain gap-energy
obstruction closes. The present proof state does not yet contain that bound.
