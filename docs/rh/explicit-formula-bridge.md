# Explicit Formula Bridge

The explicit formula belongs downstream of the source order:

```text
divisor counts -> PGS local theorems -> DNI-to-zeta compression -> pole placement -> RH sentence
```

This page records the analytic bridge surface. It does not prove a new RH
theorem. Unless a full proof is written here, the explicit-formula material is
a proof target and translation layer.

## Source To Analytic Chain

The established compression starts with divisor counts:

$$
D(s)=\sum_{n\ge1}\frac{\tau(n)}{n^s}=\zeta(s)^2.
$$

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
  counts.
- DNI-to-zeta compression recovers
  `R(s) = -zeta'(s)/zeta(s)`.
- The coefficients of `R(s)` are `Lambda(n)`.
- Summing `Lambda(n)` gives `psi(x)`.
- The explicit formula translates `psi(x)` into main, trivial, and nontrivial
  zero terms.
- Chamber-local errors such as
  `Delta_Li(p,q)=1-int_p^q dt/log(t)` are downstream analytic shadows of fixed
  prime-gap endpoint structure.

This is a downstream analytic bridge. It is not, by itself, a proof that the
nontrivial zero terms obey the RH critical-line constraint.

## Proof Target / Needs Proof

To promote this page from bridge to theorem, a proof must show how the PGS
source structure and exact DNI compression force the nontrivial zero-term
geometry in the explicit formula, equivalently:

$$
\text{every nontrivial pole of } R(s) \text{ lies on } \mathrm{Re}(s)=1/2.
$$

Until that proof is written, the correct status is:

- exact zeta compression for the identity defining `R(s)`;
- downstream analytic bridge for
  `R(s) -> Lambda(n) -> psi(x) -> zero terms`;
- proof target for the critical-line placement of the nontrivial zero terms.
