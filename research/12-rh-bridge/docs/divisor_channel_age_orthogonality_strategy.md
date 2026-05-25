# Divisor-Channel Age Orthogonality Strategy

Date: 2026-05-24

Status: candidate proof route for the dyadic summation of the chamber
age-energy upper invariant.

The Chamber Age-Energy Upper Invariant reduces the persistence problem to a
global channel-age bound:

$$
\sum_{d\le\sqrt{2X}}
\sum_{\substack{X<n\le2X\\ d\mid n}}
a(n)
\le
C X(\log X)^B.
$$

This is the Divisor-Channel Age Orthogonality theorem.

## Channel-Wise Sufficient Bound

It is enough to prove a uniform channel-wise estimate:

$$
\boxed{
\sum_{\substack{X<n\le2X\\ d\mid n}}
a(n)
\le
C\frac{X}{d}(\log X)^B
}
$$

for every

$$
2\le d\le\sqrt{2X}.
$$

Summing over `d` gives

$$
\sum_{d\le\sqrt{2X}}
C\frac{X}{d}(\log X)^B
\le
C'X(\log X)^{B+1}.
$$

Thus the global orthogonality theorem follows with one additional logarithm.

## PGS-Native Meaning

For a fixed divisor channel `d`, the inner sum is the total zero-excess age
carried by multiples of `d` in the dyadic block:

$$
\sum_{\substack{X<n\le2X\\ d\mid n}}(n-p(n)).
$$

The required estimate says:

```text
multiples of d do not concentrate at unusually large ages since the last
zero-excess endpoint.
```

This is an endpoint-chain recurrence statement relative to each divisor
channel.

## Candidate Mechanism

A proof would need to show that prime endpoints reset age often enough across
all divisor channels. For each `d`, one wants a bound of the form:

```text
average age of multiples of d in [X,2X] = O(log^B X).
```

Since there are about `X/d` multiples of `d`, this gives the channel-wise
estimate.

In chamber language, the theorem asserts that a divisor channel cannot spend
too much of a dyadic block inside long positive-excess tails.

## Required Endpoint-Modulus Recurrence

A sufficient structural theorem is:

> **Endpoint-Modulus Age Recurrence.**
> For every divisor channel `d <= sqrt(2X)`, the endpoint chain resets
> zero-excess age along the multiples of `d` with average waiting time
> `O(log^B X)` in `[X,2X]`.

This is a modulus-sensitive return-time theorem. It is stronger than the
unweighted endpoint-chain recurrence because it must hold simultaneously for
all divisor channels up to `sqrt(2X)`.

## Obstacles

**Channel correlation in long gaps.**
Long positive-excess chambers raise the age of every divisor channel that has
multiples inside the chamber. The channel sums are positively correlated, so
orthogonality is not automatic.

**Growing modulus range.**
The theorem must hold for all `d <= sqrt(2X)`. Fixed-modulus behavior is not
enough.

**No current endpoint-modulus theorem.**
Existing PGS machinery records exact endpoint chains and local chamber
ordering. It does not prove that endpoints reset age evenly across divisor
channels or residue classes.

**GWR is chamber-local.**
The selected minimum-excess point can identify a low-load interior position,
but it does not control the average age of all multiples of `d` over a dyadic
block.

## Result

Divisor-Channel Age Orthogonality reduces to a clear endpoint-modulus
recurrence principle:

$$
\sum_{\substack{X<n\le2X\\ d\mid n}}a(n)
\ll
\frac{X}{d}(\log X)^B
$$

uniformly for `d <= sqrt(2X)`.

This is the next global arithmetic theorem needed for the chamber
age-energy route. It is not currently implied by local GWR or divisor-count
ordering.
