# Finite-Part Packet Identity Arithmetic Requirement

Date: 2026-05-24

Status: isolation of the remaining PGS arithmetic requirement behind the
finite-part packet identity.

The transport-capacity assembly now requires the finite-part identity

$$
\operatorname{F.p.}
\sum_{(p,q)}
D_{p,q}(z)
=
-B_{\mathrm{comp}}^{\mathrm{fp}}(z),
$$

where

$$
D_{p,q}(z)
=
\sum_{n\in P(p,q)}
\Lambda(n)
J_z\left(\log {n\over\sqrt{pq}}\right).
$$

Equivalently, with `p(n)<q(n)` the chamber endpoints of the prime power `n`,

$$
\operatorname{F.p.}
\sum_{n=r^a}
\Lambda(n)
J_z\left(\log {n\over\sqrt{p(n)q(n)}}\right)
=
-B_{\mathrm{comp}}^{\mathrm{fp}}(z).
$$

## Analytic Side

The analytic finite part is fixed by the completion correction. The centered
trivial-zero/gamma side gives

$$
B_{\mathrm{comp}}^{\mathrm{fp}}(z)
=
{1\over2}
\left(
\operatorname{Re}\psi\left({1\over4}+{i\sqrt z\over2}\right)
+\gamma
\right)
$$

up to the sign convention chosen for packet drift. Once the convention is
fixed, this side is not adjustable.

Direct Full-Radius BDH supplies controlled summation for residual analytic
terms. It does not identify the packet finite part by itself.

## PGS Arithmetic Requirement

The PGS side must prove a global chamber-packet first-moment law:

> **Chamber-Deconvolved Finite-Part First-Moment Law.**  
> The deconvolved prime-power packet sum admits a canonical
> completion-compatible finite part, and that finite part equals the centered
> completion finite part above.

In cutoff form, this asks for an explicit counterterm `C_X(z)` such that

$$
\lim_{X\to\infty}
\left[
\sum_{\substack{n=r^a\\ n\le X}}
\Lambda(n)
J_z\left(\log {n\over\sqrt{p(n)q(n)}}\right)
-C_X(z)
\right]
=
-B_{\mathrm{comp}}^{\mathrm{fp}}(z).
$$

The counterterm must be derived from PGS chamber data, not inserted from the
gamma side after the fact.

## Obstruction From Local Envelopes

Current local PGS inputs supply:

```text
prime-power packet support
+ nonnegative lambda(n)=Lambda(n)
+ GWR selector order
+ selector-to-packet coefficient envelopes
+ packet weighted-average drift bound
```

These are local inequalities. They do not imply a global finite-part
summation law.

The obstruction has three concrete forms:

1. ordinary packet partial sums diverge and do not approach the gamma finite
   part;
2. GWR envelopes are upper bounds, not signed first-moment identities;
3. the selector is often not itself a prime power, while the finite-part sum
   is supported only on prime powers.

Thus the required identity cannot be obtained by restating chamber ordering.
It needs a new global invariant.

## Minimal Additional PGS Invariants

One of the following must be proved.

1. **Reciprocal endpoint counterterm law.**
   A PGS-native formula for `C_X(z)` in terms of endpoint returns and chamber
   centers, with convergence to the centered gamma finite part.

2. **Chamber-centered von Mangoldt finite-part law.**
   The chamber-centered first moment of the deconvolved packet load has a
   completion-compatible finite part equal to the gamma/trivial-zero finite
   part.

3. **Transport-reservoir matching law.**
   The packet drift finite part is defined by a canonical transport rule whose
   exact assembly with the pole/trivial-zero reservoir forces the identity.

4. **Packet-frame finite-part theorem.**
   The Unified Packet-Frame Source theorem is strengthened from residual
   bounds to an exact finite-part identity for the projected residual measure.

## Packet-Frame Byproduct Condition

The Unified Packet-Frame Source theorem supplies the finite-part identity as
a byproduct only if it proves more than bounded residual energy. It must also
prove exact convergence of the projected packet first moment:

$$
\operatorname{F.p.}
\sum_{(p,q)}
D_{p,q}^{\perp}(z)
=
\text{the missing completion finite part}.
$$

The existing packet-frame statement controls band energy, kernel-window mass,
and measure concentration. That is enough for Direct BDH. It is not enough
for the finite-part packet identity unless an exact first-moment component is
added.

## Result

The finite-part packet identity is the live PGS arithmetic obligation. It is
not local packet dominance and not a BDH bound. It is a global
completion-compatible first-moment law for the deconvolved prime-power packet
load. The minimal next target is a PGS-native counterterm or transport rule
that turns the divergent ordinary packet sum into the centered gamma finite
part.
