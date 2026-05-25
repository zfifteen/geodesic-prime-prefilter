# Endpoint Log-Gap Summatory Law Candidate

Date: 2026-05-24

Status: candidate PGS-native summatory law for the endpoint drift counterterm.

The Chamber-Centered Von Mangoldt Finite-Part Principle needs a global law for
the endpoint log-gap sum

$$
G(X)=
\sum_{q\le X}
\log q\log\frac{q}{p(q)},
$$

where `p(q)` is the preceding prime endpoint of the chamber ending at `q`.

This sum is the leading endpoint drift in the chamber-centered packet moment.

## Candidate Law

The candidate finite-part theorem is

$$
\boxed{
G(X)=\frac12(\log X)^2+C_{\mathrm{eg}}+o(1)
}
$$

for a finite endpoint-gap constant `C_eg`.

Equivalently,

$$
\operatorname{F.p.}_{X\to\infty}G(X)=C_{\mathrm{eg}},
$$

with the divergent counterterm

$$
\frac12(\log X)^2.
$$

This gives the endpoint piece of the packet finite-part counterterm:

$$
L_X(z)=\frac{G(X)}{2z}
=
\frac{(\log X)^2}{4z}
+
\frac{C_{\mathrm{eg}}}{2z}
+
o(1).
$$

## Endpoint-Chain Covering Route

Write the prime gap ending at `q` as

$$
g(q)=q-p(q).
$$

For small relative gaps,

$$
\log\frac{q}{p(q)}
=
\frac{g(q)}{q}
+
O\left(\frac{g(q)^2}{q^2}\right).
$$

Thus

$$
G(X)
=
\sum_{q\le X}\frac{g(q)\log q}{q}
+
O\left(
\sum_{q\le X}\frac{g(q)^2\log q}{q^2}
\right).
$$

The leading term is an endpoint-chain occupancy sum. Each chamber `(p,q]`
covers `g(q)` integers, and the endpoint weight `log q / q` is the
right-endpoint sample of the slowly varying function

$$
\frac{\log x}{x}.
$$

Therefore the expected PGS-native comparison is

$$
\sum_{q\le X}\frac{g(q)\log q}{q}
\sim
\sum_{2<n\le X}\frac{\log n}{n}
=
\frac12(\log X)^2+O(1).
$$

This route uses the endpoint chain as a partition of the integer line. It does
not require the GWR selector to choose the endpoint. The selector theorem
enters only as local chamber structure after the endpoint chain has been
fixed.

## Error Terms Needed

The proof requires two global error controls.

1. **Endpoint sampling error.**
   The difference between the right-endpoint chamber sample and the harmonic
   integral must have a finite limit:
   $$
   \sum_{q\le X}
   \left[
   \frac{g(q)\log q}{q}
   -
   \sum_{n=p(q)+1}^{q}\frac{\log n}{n}
   \right]
   =
   C_{\mathrm{sample}}+o(1).
   $$

2. **Log-gap nonlinear error.**
   The correction from `g(q)/q` to `log(q/p(q))` must have a finite limit:
   $$
   \sum_{q\le X}
   \log q
   \left[
   \log\frac{q}{p(q)}
   -
   \frac{g(q)}{q}
   \right]
   =
   C_{\mathrm{nonlin}}+o(1).
   $$

Together these give

$$
C_{\mathrm{eg}}
=
C_{\mathrm{harm}}
+
C_{\mathrm{sample}}
+
C_{\mathrm{nonlin}},
$$

where

$$
\sum_{2<n\le X}\frac{\log n}{n}
=
\frac12(\log X)^2+C_{\mathrm{harm}}+o(1).
$$

## Finite Surface

On the exact prime endpoint surface up to `X`, the raw values are:

| X | `G(X)` | `0.5 log(X)^2` | residual |
|---:|---:|---:|---:|
| `10,000` | `42.7218277` | `42.4151849` | `0.3066428` |
| `100,000` | `66.6049372` | `66.2737264` | `0.3312108` |
| `1,000,000` | `95.7662683` | `95.4341660` | `0.3321023` |

This measured surface supports the proposed leading counterterm. It is
implementation evidence only; the theorem requires the two error controls
above.

## What Chamber Or GWR Structure Helps

The endpoint-chain partition is the main PGS-native structure for this law:

```text
consecutive prime endpoints partition the integer line into chambers.
```

GWR contributes local chamber order, but it does not by itself control the
global endpoint sampling error or the nonlinear log-gap error. The needed new
input is a reciprocal endpoint occupancy theorem:

> **Reciprocal Endpoint Occupancy Theorem.**
> The right-endpoint samples `g(q) log q / q` over prime-gap chambers have the
> same finite part as the harmonic integral of `log x / x` over the integer
> line.

Once this theorem is proved, the endpoint drift counterterm in the
chamber-centered von Mangoldt finite part is fixed.
