# Endpoint-Lattice Closure Invariant Obstruction

Date: 2026-05-24

Status: closure-invariant obstruction for the Modulus-Link Endpoint-Lattice
route.

The modulus-link route asks for a global invariant controlling endpoint
residual sequences against divisor-channel lattices:

$$
\sum_{X<q\le2X}A_d(p(q),q)
\ll
\frac{X}{d}(\log X)^B
$$

uniformly for

$$
d\le\sqrt{2X}.
$$

The natural closure invariant is the lattice crossing energy itself. The
principal obstruction is that the first nontrivial channel, `d = 2`, already
contains the full gap-square problem.

## Natural Closure Invariant

For a fixed `d`, define

$$
\mathfrak C_d(X)
=
\sum_{X<q\le2X}
\sum_{\substack{1\le j<q-p(q)\\ p(q)+j\equiv0\pmod d}}
j.
$$

This is the endpoint-lattice crossing energy of the endpoint chain against
the divisor-channel lattice `dZ`.

The Endpoint-Modulus Age Recurrence theorem is precisely

$$
\mathfrak C_d(X)
\ll
\frac{X}{d}(\log X)^B
$$

uniformly for all divisor channels in range.

## The `d = 2` Obstruction

For all odd prime endpoints `p`, the next odd prime endpoint `q` has even gap

$$
g=q-p=2h.
$$

The multiples of `2` inside `(p,q)` occur at odd offsets

$$
j=1,3,5,\ldots,2h-1.
$$

Their crossing age sum is

$$
1+3+5+\cdots+(2h-1)=h^2=\frac{g^2}{4}.
$$

Therefore

$$
\mathfrak C_2(X)
=
\frac14
\sum_{X<q\le2X}g(q)^2
$$

up to boundary and the initial endpoint exception.

Thus the modulus-link closure estimate for `d = 2` is already equivalent to
the dyadic reciprocal gap-energy bound.

## Consequence

The growing modulus range is a real difficulty, but it is not the first
difficulty. The first difficulty is long-gap amplification in the smallest
proper divisor channel.

Any endpoint-lattice closure invariant that dominates crossing age must
already prove

$$
\sum_{X<q\le2X}g(q)^2
\ll
X(\log X)^B.
$$

So the modulus-link route cannot bypass the Zero-Excess Return-Time Tail
Theorem. It restates that theorem in lattice-crossing language.

## Candidate Invariant Contract

A usable global closure invariant would need:

1. **Chamber domination.**
   For every `d`,
   $$
   A_d(p,q)\le \Omega_d(p,q).
   $$

2. **Dyadic closure bound.**
   $$
   \sum_{X<q\le2X}\Omega_d(p(q),q)
   \le
   C\frac{X}{d}(\log X)^B.
   $$

3. **Small-channel strength.**
   For `d = 2`, the invariant must control
   $$
   \sum_{X<q\le2X}g(q)^2.
   $$

4. **Uniform large-channel compatibility.**
   The same construction must remain valid up to `d <= sqrt(2X)`.

No such invariant is currently present in the PGS framework.

## Principal Analytic Difficulty

Long gaps amplify every lattice-crossing invariant. The amplification is not a
large-modulus artifact. It appears immediately in the even channel.

Thus the central analytic difficulty is:

```text
prove a global square-moment bound for zero-excess return times.
```

Endpoint residual closure, modulus-link language, and divisor-channel
lattices can express this difficulty cleanly. They do not remove it.

## Result

The modulus-link endpoint-lattice route has reduced to the same global theorem
as the persistence-energy route:

$$
\sum_{X<q\le2X}g(q)^2
\ll
X(\log X)^B.
$$

This is now the unavoidable endpoint-chain obstruction behind the
Chamber-Centered Von Mangoldt finite-part program.
