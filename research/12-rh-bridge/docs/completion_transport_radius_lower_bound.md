# Completion Transport Radius Lower Bound

Date: 2026-05-24

Status: candidate completion-side estimate for the Chamber-Deconvolved
Reciprocal Balance Lemma.

The combined packet reduction leaves one completion-side target. For a chamber
packet `P(p,q)`, define

$$
x_n=\log\frac{n}{\sqrt{pq}},
\qquad
M_{p,q}=\max_{n\in P(p,q)}|x_n|.
$$

The arithmetic side gives

$$
|D_{p,q}(z)|\le M_{p,q}R_{p,q}(z).
$$

The Aggregate Completion-Cost Bound closes if the completion transport radius
satisfies

$$
\rho_{p,q}(z)\ge M_{p,q}.
$$

This note states the candidate lower bound and the analytic condition that
would prove it.

## Candidate Bound

Let the completion correction assigned to the packet be the signed measure
`\eta_{p,q}`. Let `\eta^-_{p,q,z}` denote the part of the correction that
creates negative folded even cost for the kernel

$$
K_z(x)=\frac{1}{z+x^2}.
$$

Define its negative even cost and odd transport capacity by

$$
C^-_{p,q}(z)=\int K_z(x)\,d\eta^-_{p,q,z}(x),
$$

and

$$
T^-_{p,q}(z)=\int |x|K_z(x)\,d\eta^-_{p,q,z}(x).
$$

The effective transport radius is

$$
\rho_{p,q}(z)=\frac{T^-_{p,q}(z)}{C^-_{p,q}(z)}
$$

when `C^-_{p,q}(z)>0`; if `C^-_{p,q}(z)=0`, the completion cost bound is
already nonnegative.

The candidate lower bound is:

> **Completion Transport Radius Lower Bound.**
> For every chamber packet and every `z > 0`,
> $$
> \rho_{p,q}(z)\ge M_{p,q}.
> $$

## Derivation From Support Separation

The bound follows immediately from the support condition

$$
|x|\ge M_{p,q}
\qquad
\text{on the support of }\eta^-_{p,q,z}.
$$

Indeed, under that condition,

$$
T^-_{p,q}(z)
=
\int |x|K_z(x)\,d\eta^-_{p,q,z}(x)
\ge
M_{p,q}\int K_z(x)\,d\eta^-_{p,q,z}(x)
=
M_{p,q}C^-_{p,q}(z).
$$

Therefore

$$
\rho_{p,q}(z)=\frac{T^-_{p,q}(z)}{C^-_{p,q}(z)}
\ge
M_{p,q}.
$$

Combining this with the weighted-average packet bound gives

$$
|D_{p,q}(z)|
\le
M_{p,q}R_{p,q}(z)
\le
\rho_{p,q}(z)R_{p,q}(z),
$$

which is the Aggregate Completion-Cost Bound.

## Main Analytic Obstacle

The remaining analytic obstacle is the localization of the completion
correction. The completion terms

```text
pole terms + gamma term + main term + trivial-zero contribution
```

are globally defined in the completed quotient. The current packet formalism
has not yet proved that the negative folded cost assigned to an individual
chamber packet is supported only at transport coordinates satisfying

$$
|x|\ge M_{p,q}.
$$

Thus the next proof obligation is not another prime-power packet estimate. It
is a completion-localization theorem:

> The packetwise completion correction can be assigned so that every negative
> folded-cost contribution used to cancel packet drift occurs at transport
> radius at least the packet's maximum centered excursion.

That theorem would supply

$$
\rho_{p,q}(z)\ge M_{p,q}
$$

and therefore close the local Folded Packet Drift Inequality for the chamber.

The formal support-localization statement is recorded in
[Completion Localization Lemma](completion_localization_lemma.md).
