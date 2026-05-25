# Net Finite-Part Packet Sum Requirement

Date: 2026-05-24

Status: packet-side translation of the trivial-zero finite-part balance.

The finite-part analysis of the centered trivial-zero reservoir gives the net
condition

$$
D_+(z)-D_-(z)=B^{\mathrm{fp}}_{\mathrm{triv}}(z).
$$

In packet language this is an exact global first-moment identity for the
deconvolved prime-power packet load. It is not supplied by the current local
GWR selector envelopes.

## Explicit Packet Sum

For each consecutive-prime chamber `(p,q]`, define

$$
D_{p,q}(z)
=
\sum_{n\in P(p,q)}
\lambda(n)
J_z\left(\log\frac{n}{\sqrt{pq}}\right),
$$

where

$$
P(p,q)
=
\{q\}
\cup
\{n:p<n<q,\ n=r^a,\ r\text{ prime},\ a\ge2\},
$$

and

$$
\lambda(n)=\Lambda(n).
$$

If all sums were absolutely convergent, then

$$
D_+(z)-D_-(z)
=
\sum_{(p,q)}D_{p,q}(z).
$$

The required packet-side form of the finite-part balance is therefore

$$
\boxed{
\operatorname{F.p.}
\sum_{(p,q)}
\sum_{n\in P(p,q)}
\Lambda(n)
J_z\left(\log\frac{n}{\sqrt{pq}}\right)
=
B^{\mathrm{fp}}_{\mathrm{triv}}(z).
}
$$

Using the explicit finite part from the centered trivial-zero side,

$$
\boxed{
\operatorname{F.p.}
\sum_{(p,q)}
\sum_{n\in P(p,q)}
\Lambda(n)
J_z\left(\log\frac{n}{\sqrt{pq}}\right)
=
-\frac12
\left(
\operatorname{Re}\psi\left(\frac14+\frac{i\sqrt z}{2}\right)
+
\gamma
\right).
}
$$

This is the exact net finite-part packet sum requirement.

## Prime-Power Indexed Form

Equivalently, let `p(n) < q(n)` be the consecutive-prime endpoints of the
unique chamber containing the prime power `n` with `p(n) < n <= q(n)`. Then
the requirement is

$$
\boxed{
\operatorname{F.p.}
\sum_{n=r^a}
\Lambda(n)
J_z\left(\log\frac{n}{\sqrt{p(n)q(n)}}\right)
=
B^{\mathrm{fp}}_{\mathrm{triv}}(z).
}
$$

Endpoint primes are included by the case `n=q(n)`.

## Ordinary Partial Sums Are Not The Target

The unregularized packet partial sums do not show convergence to the
trivial-zero finite part. On the deterministic surface `q <= 1,000,000`, the
ordinary partial sums are:

| z | ordinary packet partial sum | `B^fp_triv(z)` |
|---:|---:|---:|
| `0.0001` | `385590.539` | `1.82431096` |
| `0.001` | `42223.6274` | `1.81706783` |
| `0.01` | `4512.43105` | `1.74736711` |
| `0.1` | `469.31337` | `1.24549940` |
| `1` | `47.4954157` | `0.151600321` |
| `10` | `4.75722881` | `-0.515482403` |

This measured surface separates the theorem target from ordinary finite
accumulation. The required identity is a finite-part identity, not a limit of
positive endpoint-dominated packet partial sums.

## Principal Obstruction

The existing PGS chamber and GWR machinery gives local information:

```text
selector position,
divisor-count minimum,
endpoint mass,
prime-power coefficient envelopes,
left/right packet position.
```

The net finite-part packet sum requires a global analytic summation law:

```text
regularized sum of all deconvolved packet first moments
= centered digamma finite part.
```

No theorem currently recorded in `PROOF.md` or in the RH bridge notes converts
the local GWR ordering into this global finite-part identity.

The obstruction has three parts.

1. **Divergent ordinary accumulation.**
   Endpoint terms dominate ordinary partial sums. A finite-part subtraction or
   completion-compatible regularization is necessary.

2. **Missing chamber-to-gamma summation law.**
   The GWR selector envelopes bound local coefficients. They do not produce
   the digamma expression
   $$
   -\frac12
   \left(
   \operatorname{Re}\psi\left(\frac14+\frac{i\sqrt z}{2}\right)
   +
   \gamma
   \right).
   $$

3. **Selector invisibility in the target identity.**
   The net packet sum is determined by deconvolved prime-power support and
   chamber centers. The GWR selector controls support indirectly through
   divisor-count order, but it does not appear in the final finite-part
   expression.

## Resulting Lemma Target

The completion-side obstruction is now equivalent to the following statement.

> **Packet Net Finite-Part Balance Lemma.**
> For every `z > 0` in the folded-kernel domain, the finite-part regularized
> global sum of deconvolved packet first moments equals the centered
> trivial-zero finite part:
> $$
> \operatorname{F.p.}
> \sum_{(p,q)}D_{p,q}(z)
> =
> B^{\mathrm{fp}}_{\mathrm{triv}}(z).
> $$

This lemma is not a local packet dominance theorem. It is a global
regularized summation theorem linking PGS chamber assignment to the completed
gamma factor.
