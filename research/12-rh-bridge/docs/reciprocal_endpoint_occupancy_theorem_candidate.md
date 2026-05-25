# Reciprocal Endpoint Occupancy Theorem Candidate

Date: 2026-05-24

Status: candidate sampling theorem for the endpoint log-gap summatory law.

The endpoint log-gap law reduces to a sampling statement over prime-gap
chambers. Each chamber `(p,q]` has width

$$
g(q)=q-p.
$$

The right endpoint samples the function

$$
f(x)=\frac{\log x}{x}
$$

at `q` and assigns that value to the whole chamber.

## Theorem Candidate

Define the endpoint occupancy sum

$$
O(X)=
\sum_{q\le X}g(q)\frac{\log q}{q}.
$$

Define the harmonic reference sum

$$
H(X)=
\sum_{2<n\le X}\frac{\log n}{n}.
$$

The candidate theorem is:

> **Reciprocal Endpoint Occupancy Theorem.**
> The right-endpoint chamber samples have the same finite part as the harmonic
> reference sum:
> $$
> O(X)-H(X)\to C_{\mathrm{occ}}
> $$
> for a finite constant `C_occ`.

Since

$$
H(X)=\frac12(\log X)^2+C_{\mathrm{harm}}+o(1),
$$

this implies

$$
O(X)=\frac12(\log X)^2+C_{\mathrm{harm}}+C_{\mathrm{occ}}+o(1).
$$

## Exact Sampling Error

The sampling error is

$$
O(X)-H(X)
=
\sum_{q\le X}
\sum_{n=p(q)+1}^{q}
\left(
\frac{\log q}{q}
-
\frac{\log n}{n}
\right).
$$

For all sufficiently large chambers, `f(x)=log x / x` is decreasing. Therefore
each chamber contribution is nonpositive.

Using the derivative

$$
f'(x)=\frac{1-\log x}{x^2},
$$

the magnitude of the chamber error is bounded by

$$
\left|
\sum_{n=p(q)+1}^{q}
\left(f(q)-f(n)\right)
\right|
\le
C
\frac{g(q)^2\log q}{q^2}
$$

for all large `q`.

## Sufficient Gap-Energy Condition

A sufficient PGS-native condition for the theorem is the reciprocal gap-energy
summability condition

$$
\boxed{
\sum_q
\frac{g(q)^2\log q}{q^2}
<\infty.
}
$$

Under this condition, the chamber sampling errors are absolutely summable, so
`O(X)-H(X)` has a finite limit.

This is the clean arithmetic condition behind the endpoint occupancy theorem.

## Finite Surface

On the exact prime endpoint surface up to `X`, the sampling quantities are:

| X | `O(X)` | `H(X)` | `O(X)-H(X)` | reciprocal gap energy |
|---:|---:|---:|---:|---:|
| `10,000` | `41.4206293` | `41.9713592` | `-0.5507299` | `2.2020055` |
| `100,000` | `65.2966855` | `65.8533583` | `-0.5566728` | `2.2161020` |
| `1,000,000` | `94.4569087` | `95.0145486` | `-0.5576399` | `2.2183175` |

This finite surface is consistent with a finite sampling-error constant and a
convergent reciprocal gap-energy sum.

## Chamber And GWR Leverage

The theorem is PGS-native because it uses the chamber endpoint chain:

```text
prime endpoints partition the integer line into consecutive chambers.
```

The current GWR theorem supplies local interior ordering once a chamber is
fixed. It does not by itself prove the reciprocal gap-energy condition. To use
GWR here, one would need an additional theorem converting divisor-count
chamber structure into a global bound on

$$
\sum_q\frac{g(q)^2\log q}{q^2}.
$$

That is a new endpoint-chain energy statement, not a consequence of the
current local selector theorem.

## Result

The Reciprocal Endpoint Occupancy Theorem reduces the endpoint drift
counterterm to one precise additional arithmetic obligation:

```text
prove reciprocal square-gap energy is finite, or prove the sampling error
has a finite limit directly.
```

This is the first global endpoint-chain theorem needed for the
Chamber-Centered Von Mangoldt Finite-Part Principle.
