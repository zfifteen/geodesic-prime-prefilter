# Endpoint-Modulus Age Recurrence Strategy

Date: 2026-05-24

Status: candidate proof route for Divisor-Channel Age Orthogonality.

The Divisor-Channel Age Orthogonality theorem follows from a uniform
endpoint-modulus age recurrence estimate. For each divisor channel `d`, define

$$
A_d(X)=
\sum_{\substack{X<n\le2X\\ d\mid n}}
a(n),
\qquad
a(n)=n-p(n).
$$

The target is

$$
\boxed{
A_d(X)\le C\frac{X}{d}(\log X)^B
}
$$

uniformly for

$$
2\le d\le\sqrt{2X}.
$$

This says that multiples of `d` have average zero-excess age `O(log^B X)` in
the dyadic block.

## Tail Form

For a fixed channel `d`, define

$$
N_{d,X}(H)=
\#\{n:X<n\le2X,\ d\mid n,\ a(n)\ge H\}.
$$

Then

$$
A_d(X)
=
\sum_{H\ge1}N_{d,X}(H).
$$

It is enough to prove a channel tail bound whose sum over `H` is
`O((X/d)(log X)^B)`, for example

$$
N_{d,X}(H)
\le
C\frac{X}{d}\frac{(\log X)^B}{H^{1+\varepsilon}}
$$

for some `epsilon > 0`, or any comparable summable tail.

## Endpoint-Channel Interpretation

Multiples of `d` are divisor-channel points. Except for the prime `d` itself,
they are not zero-excess endpoints.

Thus the recurrence theorem is not saying that endpoints land on the channel.
It says that endpoint resets occur near the channel often enough:

```text
for most multiples n of d, the previous zero-excess endpoint p(n) is within
O(log^B X) on average.
```

This is a proximity theorem between the endpoint chain and the lattice
`dZ`.

## Candidate Mechanism

A proof would need a modulus-sensitive endpoint recurrence statement:

> **Endpoint-Lattice Proximity Law.**
> For every `d <= sqrt(2X)`, the consecutive-prime endpoint chain intersects
> the backward neighborhoods of multiples of `d` with average distance
> `O(log^B X)` in `[X,2X]`.

In concrete terms, the average backward distance

$$
\frac{d}{X}
\sum_{\substack{X<n\le2X\\ d\mid n}}
(n-p(n))
$$

must be polylogarithmic.

## Possible PGS Structures

Three structures could support such a theorem.

1. **Endpoint residue spread.**
   Prime endpoints must occupy enough residue classes near `0 mod d` to keep
   backward distances from multiples of `d` small on average.

2. **Chamber crossing control.**
   Long chambers intersect many divisor channels. A theorem limiting how
   often chambers can cross many channel points at high age would imply the
   recurrence estimate.

3. **Modulus-link closure.**
   A PGS-native modulus-link theorem could connect endpoint returns to divisor
   channel lattices uniformly across `d <= sqrt(2X)`.

## Main Obstacles

**Endpoints avoid the channel.**
For `d > 1`, almost every multiple of `d` is composite. The reset point is
near the channel, not on it. The theorem must control proximity, not equality.

**Uniformity in growing `d`.**
The estimate must hold up to `sqrt(2X)`. Fixed-modulus recurrence is
insufficient.

**Long gaps correlate all channels.**
A single long positive-excess chamber raises the age of every channel with
multiples inside that chamber. This creates positive correlation across
channels rather than cancellation.

**No current PGS endpoint-lattice theorem.**
Existing modulus-link work is not recorded as an all-scale theorem giving
uniform endpoint proximity to divisor-channel lattices.

## Result

The Endpoint-Modulus Age Recurrence theorem can be stated precisely as

$$
\sum_{\substack{X<n\le2X\\ d\mid n}}
(n-p(n))
\ll
\frac{X}{d}(\log X)^B
$$

uniformly for `d <= sqrt(2X)`.

This is the exact modulus-sensitive return theorem needed to prove
Divisor-Channel Age Orthogonality. It is a new global endpoint-chain theorem,
not a consequence of current local GWR ordering.
