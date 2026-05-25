# Modulus-Link Endpoint-Lattice Closure Strategy

Date: 2026-05-24

Status: candidate modulus-link route for Endpoint-Modulus Age Recurrence.

The Endpoint-Modulus Age Recurrence theorem requires, for every divisor
channel `d <= sqrt(2X)`,

$$
\sum_{\substack{X<n\le2X\\ d\mid n}}
(n-p(n))
\ll
\frac{X}{d}(\log X)^B.
$$

This note formulates the modulus-link closure statement that would imply this
bound.

## Channel Age Inside One Chamber

Fix a chamber `(p,q]` and a divisor channel `d`. The multiples of `d` inside
the chamber occur at offsets

$$
j\equiv -p\pmod d,
\qquad
1\le j<g(q).
$$

The channel age contribution of this chamber is

$$
A_d(p,q)
=
\sum_{\substack{1\le j<g(q)\\ p+j\equiv0\pmod d}}j.
$$

The global endpoint-modulus recurrence target is

$$
\sum_{X<q\le2X}A_d(p(q),q)
\ll
\frac{X}{d}(\log X)^B
$$

uniformly for `d <= sqrt(2X)`.

## Candidate Closure Law

The needed modulus-link theorem is:

> **Endpoint-Lattice Closure Law.**
> For every dyadic block `[X,2X]` and every divisor channel
> `2 <= d <= sqrt(2X)`, the endpoint residual sequence modulo `d` has bounded
> lattice crossing energy:
> $$
> \sum_{X<q\le2X}
> \sum_{\substack{1\le j<q-p(q)\\ p(q)+j\equiv0\pmod d}}
> j
> \le
> C\frac{X}{d}(\log X)^B.
> $$

This is exactly the endpoint-modulus age recurrence theorem written in
residual-offset language.

## PGS Mechanism

The mechanism would read:

```text
endpoint p has residual p mod d
the divisor-channel lattice dZ crosses the chamber at predictable offsets
modulus-link closure controls how much crossing age can accumulate
endpoint q resets the age before the next chamber
```

The theorem says that the endpoint chain closes against every divisor-channel
lattice often enough that crossing ages remain polylogarithmic on average.

## Relation To Existing Modulus-Link Work

The existing cryptology/RSA modulus-link work studies transported endpoint
structure through a public modulus and reciprocal closure surfaces. It is
useful vocabulary and evidence that endpoint-chain transport carries real
structure.

It does not currently prove the Endpoint-Lattice Closure Law.

The present target is different:

```text
all prime endpoints in a dyadic block
all divisor-channel moduli d <= sqrt(2X)
uniform age/crossing-energy bound
no hidden factor, no candidate search, no audit endpoint.
```

This is a global endpoint-chain theorem, not an RSA-specific closure probe.

## Principal Obstacles

**Uniform growing-modulus range.**
The law must hold simultaneously for every divisor channel up to `sqrt(2X)`.
This is much stronger than fixed-modulus closure.

**Crossing-energy, not just residue occurrence.**
It is not enough for endpoints to occupy residue classes. The theorem must
bound the weighted ages of lattice crossings inside chambers.

**Long-gap amplification.**
A long chamber contributes large crossing age to many divisor channels. Any
closure theorem must suppress this correlated amplification globally.

**No current closure invariant.**
Existing modulus-link closure artifacts do not define a global invariant whose
dyadic sum is `O(X(log X)^B)` and whose chamber contribution dominates
`A_d(p,q)`.

## Result

The modulus-link route is viable only if it becomes a theorem about endpoint
residual sequences against divisor-channel lattices:

$$
\sum_{X<q\le2X}A_d(p(q),q)
\ll
\frac{X}{d}(\log X)^B.
$$

This is the exact closure statement needed for Endpoint-Modulus Age
Recurrence. It remains a new global PGS theorem obligation.
