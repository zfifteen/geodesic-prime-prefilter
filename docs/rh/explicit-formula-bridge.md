# Explicit Formula Bridge

The explicit formula belongs downstream of the source order:

```text
divisor counts -> zero-excess returns -> local theorems
-> DNI-to-zeta compression -> source-to-spectral placement target
-> pole placement/RH sentence
```

This page records the downstream analytic bridge surface. It translates the
continued DNI ratio into `Lambda`, `psi`, zero-term, and error-term language.
It also names one equivalent form of the remaining source-to-spectral
placement target.

## Source To Analytic Chain

The established compression starts with divisor counts:

$$
D(s)=\sum_{n\ge1}\frac{\tau(n)}{n^s}=\zeta(s)^2.
$$

The zero-excess coordinate on the integer side is

$$
E(n)=\left(\frac{\tau(n)}{2}-1\right)\log n.
$$

For `n > 1`, prime returns are exactly $E(n)=0$. In a nonempty gap interior,
the local theorem function satisfies $F(n)=-E(n)$, so the selected integer is
the leftmost argmin of $E(n)$. That is the source-side coordinate. It is not
the explicit-formula object.

The bridge load remains

$$
H(n)=\log n+E(n)=\frac{\tau(n)\log n}{2}.
$$

Equivalently, `H(n)=log n+E(n)=tau(n)log(n)/2`.

With the DNI normalization series

$$
K(s)=-\frac{1}{e^2}D'(s),
$$

the normalized ratio is

$$
R(s)=\frac{e^2}{2}\frac{K(s)}{D(s)}
=-\frac{\zeta'(s)}{\zeta(s)}
=\sum_{n\ge1}\frac{\Lambda(n)}{n^s}.
$$

That gives the downstream coefficient chain:

```text
R(s) -> Lambda(n) -> psi(x) -> zero terms
```

The von Mangoldt coefficients define the Chebyshev counting function

$$
\psi(x)=\sum_{n\le x}\Lambda(n).
$$

Classical explicit-formula machinery then rewrites `psi(x)` in terms of the
main term, the pole at `s=1`, trivial-zero terms, and nontrivial-zero terms.
In schematic form,

$$
\psi(x)=x-\sum_{\rho}\frac{x^\rho}{\rho}+\text{elementary terms},
$$

with the sum taken over nontrivial zeros `rho` of `zeta(s)`, subject to the
usual explicit-formula conventions.

## Chamber-Local Counting Error

For a prime gap with consecutive endpoints `p < q`, the chamber contains one
prime endpoint on the right and no primes in the open interval `(p,q)`.

The local logarithmic-integral expectation across the chamber is

$$
\int_p^q \frac{dt}{\log t}.
$$

The chamber-local counting error is therefore

$$
\Delta_{\mathrm{Li}}(p,q)
=1-\int_p^q \frac{dt}{\log t}.
$$

This quantity is a local endpoint-error observable. It is useful because it
connects a PGS chamber object to the analytic prime-counting language, while
preserving the direction of explanation:

```text
fixed chamber endpoints -> local counting error -> explicit-formula shadow
```

## Bridge Claim

The bridge claim is:

- PGS local theorems determine exact source-side chamber structure from divisor
  counts and zero-excess returns.
- DNI-to-zeta compression recovers
  `R(s) = -zeta'(s)/zeta(s)`.
- The coefficients of `R(s)` are `Lambda(n)`.
- Summing `Lambda(n)` gives `psi(x)`.
- The explicit formula translates `psi(x)` into main, trivial, and nontrivial
  zero terms.
- Chamber-local errors such as
  `Delta_Li(p,q)=1-int_p^q dt/log(t)` are downstream analytic shadows of fixed
  prime-gap endpoint structure.

This is a downstream analytic bridge. The local PGS theorems and exact DNI
compression with `H(n)=log n+E(n)=tau(n)log(n)/2` identify the source and the
continued ratio. They do not yet supply the RH-strength placement constraint.

## Translation Status

The explicit formula restates the continued ratio in classical counting
language:

```text
R(s) -> Lambda(n) -> psi(x) -> zero terms -> error-term language
```

The correct status split is:

- exact zeta compression for the identity defining `R(s)`;
- downstream analytic bridge for
  `R(s) -> Lambda(n) -> psi(x) -> zero terms`;
- unresolved source-to-spectral placement for the off-critical-pole exclusion
  recorded in `off-critical-pole-exclusion.md`;
- translation/proof-detail bridge for reviewers who want the RH sentence
  expressed through `psi`, `Lambda`, zero-term, or error-term estimates.

`PROOF.md` controls only the local PGS theorems. The pole-placement sentence
still needs a source-to-spectral theorem, or an equivalent RH-strength
explicit-formula bound derived from the PGS source.
