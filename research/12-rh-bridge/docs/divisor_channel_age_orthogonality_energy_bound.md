# Divisor-Channel Age Orthogonality Energy Bound

Date: 2026-05-24

Status: conditional reduction from divisor-channel age orthogonality to the
Age-Divisor Energy Bound.

The Age-Divisor Energy Bound is

$$
\sum_{X<n\le2X}(n-p(n))(\tau(n)-2)
\ll
X(\log X)^B.
$$

This note records the exact divisor-channel estimate that implies it.

## Objects

Let

$$
a(n)=n-p(n),
\qquad
\sigma(n)=\tau(n)-2,
\qquad
\Phi(n)=a(n)\sigma(n).
$$

For a divisor channel `d`, define its dyadic age load

$$
A_d(X)=
\sum_{\substack{X<n\le2X\\d\mid n}}a(n).
$$

The required channel statement is:

> **Divisor-Channel Age Orthogonality.**
> Uniformly for `2 <= d <= sqrt(2X)`,
> $$
> A_d(X)
> \ll
> {X\over d}(\log X)^B.
> $$

## Conditional Reduction

Assume Divisor-Channel Age Orthogonality. Then

$$
\sum_{X<n\le2X}\Phi(n)
\ll
X(\log X)^{B+1}.
$$

Thus it proves the Age-Divisor Energy Bound, with one harmless logarithmic
loss in the exponent.

## Proof

For every composite `n`, proper divisors larger than `sqrt(n)` pair with
proper divisors smaller than `sqrt(n)`. Therefore

$$
\tau(n)-2
\le
2
\sum_{\substack{2\le d\le\sqrt n\\d\mid n}}1.
$$

Multiplying by `a(n)` and summing over the dyadic block gives

$$
\sum_{X<n\le2X}a(n)(\tau(n)-2)
\le
2
\sum_{X<n\le2X}
a(n)
\sum_{\substack{2\le d\le\sqrt n\\d\mid n}}1.
$$

Interchanging the finite sums and enlarging `sqrt(n)` to `sqrt(2X)`,

$$
\sum_{X<n\le2X}\Phi(n)
\le
2
\sum_{2\le d\le\sqrt{2X}}
\sum_{\substack{X<n\le2X\\d\mid n}}a(n).
$$

By Divisor-Channel Age Orthogonality,

$$
\sum_{X<n\le2X}\Phi(n)
\ll
\sum_{2\le d\le\sqrt{2X}}
{X\over d}(\log X)^B.
$$

Since

$$
\sum_{2\le d\le\sqrt{2X}}{1\over d}
\ll
\log X,
$$

we get

$$
\sum_{X<n\le2X}\Phi(n)
\ll
X(\log X)^{B+1}.
$$

This is the desired age-divisor energy bound after renaming the logarithmic
exponent.

## PGS Interpretation

The divisor surplus `tau(n)-2` is the number of proper divisor channels
active at `n`. The age `a(n)` is the distance from the previous zero-excess
endpoint. Therefore the total age-divisor energy is bounded by the sum of
zero-excess age carried across all small proper divisor channels.

The orthogonality theorem says that no divisor channel `d` carries average
zero-excess age larger than a polylogarithm on its natural population
`X/d`.

## Existing Inputs

Current PGS machinery supplies the exact chamber and divisor objects:

- the zero-excess endpoint chain;
- positive-excess chamber interiors;
- divisor surplus `tau(n)-2`;
- the GWR leftmost minimum-excess selector inside each chamber.

These inputs identify the channel loads. They do not prove the uniform
channel-age estimate

$$
A_d(X)\ll {X\over d}(\log X)^B
$$

for every `d <= sqrt(2X)`.

## Remaining Gate

The leading endpoint counterterm is now reduced through the chain

```text
Divisor-Channel Age Orthogonality
-> Age-Divisor Energy Bound
-> Zero-Excess Return Square-Moment Theorem
-> Reciprocal Square-Gap Energy Lemma
-> endpoint log-gap finite part
-> C_eg/(2z).
```

The exact remaining global input at this level is the uniform channel-age
orthogonality theorem. A proof must show that multiples of each divisor
channel return to the zero-excess endpoint floor with polylogarithmic average
age, uniformly through `d <= sqrt(2X)`.
