# Deconvolution Sign-Regularity From Chamber Ordering

Date: 2026-05-24

Status: proof-strategy note for the Chamber-Deconvolved Reciprocal Balance
Lemma.

This note tests the first local bridge from the proved Interior Maximizer
Theorem to the sign and support pattern of the deconvolved chamber load.

The result is narrow and useful:

```text
chamber order does not by itself give reciprocal balance;
after deconvolution, the local positive mass is exactly prime-power mass;
the GWR-selected point sees that mass only in prime-power-minimum chambers.
```

This is the first checkable consequence of the proposed Deconvolution
Sign-Regularity Input. It also names the additional arithmetic property still
needed.

## Source Layer

For `n > 1`, define

$$
E(n)=\left(\frac{\tau(n)}{2}-1\right)\log n.
$$

Prime returns are exactly

$$
E(n)=0 \iff \tau(n)=2.
$$

The bridge load is

$$
H(n)=\log n+E(n)=\frac{\tau(n)\log n}{2}.
$$

The divisor-count and load series are

$$
D(s)=\sum_{n\ge1}\frac{\tau(n)}{n^s}
=\zeta(s)^2,
$$

and

$$
B(s)=\sum_{n\ge1}\frac{H(n)}{n^s}
=-\frac12D'(s).
$$

The deconvolved load is

$$
\lambda=\tau_{\mathrm{Dir}}^{-1}*H,
$$

so

$$
\sum_{n\ge1}\frac{\lambda(n)}{n^s}
=\frac{B(s)}{D(s)}
=-\frac{\zeta'(s)}{\zeta(s)}.
$$

Therefore

$$
\lambda(n)=\Lambda(n).
$$

This identity is exact. It is the first place where the raw chamber load is
turned into the prime-power detector.

## Chamber Packets

Let `p < q` be consecutive primes and define the closed-right chamber packet

$$
C(p,q)=\{p+1,\ldots,q\}.
$$

The endpoint `q` is included because it is the next zero-excess return and it
always carries positive deconvolved mass:

$$
\lambda(q)=\Lambda(q)=\log q.
$$

Interior points carry deconvolved mass only when they are prime powers:

$$
n\in(p,q),\quad n=r^k
\quad\Longrightarrow\quad
\lambda(n)=\log r.
$$

All other interior composites have

$$
\lambda(n)=0.
$$

So the local support property after deconvolution is:

```text
one positive endpoint mass at q;
positive interior masses exactly at prime powers;
zero mass at all other interior composites.
```

This support rule is stronger than raw divisor-count ordering, but it is not
the folded reciprocal balance needed for the completed `z = u^2` kernel.

## What GWR Adds Locally

The Interior Maximizer Theorem says that inside a nonempty open chamber

$$
I(p,q)=\{p+1,\ldots,q-1\},
$$

the selected integer

$$
w=\min\{n\in I(p,q):\tau(n)=\min_{m\in I(p,q)}\tau(m)\}
$$

is the leftmost minimum of $E(n)$.

This local order gives a visibility rule for deconvolved support:

> **Prime-Power Minimum Visibility.**
> If the GWR-selected integer `w` is a prime power, then `w` carries positive
> deconvolved mass:
> $$
> \lambda(w)=\Lambda(w)>0.
> $$
> If the GWR-selected integer is not a prime power, then
> $$
> \lambda(w)=0.
> $$

For the most important low-divisor case:

$$
\tau(w)=3
\quad\Longleftrightarrow\quad
w=r^2
$$

for a prime `r`, and then

$$
\lambda(w)=\log r.
$$

If the selected point has $\tau(w)=4$ because it is a product of two distinct
primes, then

$$
\lambda(w)=0.
$$

Thus the Interior Maximizer Theorem supplies a local gate:

```text
GWR-selected square -> positive deconvolved interior mass
GWR-selected nonsquare composite -> no deconvolved mass at the selector
```

It does not say that every GWR-selected minimum contributes positive mass.

## First Local Table

The first chambers show the support pattern.

| Chamber | Interior and endpoint deconvolved support |
| --- | --- |
| `(3,5]` | `4: tau=3, lambda=log 2, GWR`; `5: tau=2, lambda=log 5` |
| `(5,7]` | `6: tau=4, lambda=0, GWR`; `7: tau=2, lambda=log 7` |
| `(7,11]` | `8: tau=4, lambda=log 2`; `9: tau=3, lambda=log 3, GWR`; `10: tau=4, lambda=0`; `11: tau=2, lambda=log 11` |
| `(11,13]` | `12: tau=6, lambda=0, GWR`; `13: tau=2, lambda=log 13` |
| `(13,17]` | `14: tau=4, lambda=0, GWR`; `15: tau=4, lambda=0`; `16: tau=5, lambda=log 2`; `17: tau=2, lambda=log 17` |
| `(23,29]` | `24: tau=8, lambda=0`; `25: tau=3, lambda=log 5, GWR`; `26: tau=4, lambda=0`; `27: tau=4, lambda=log 3`; `28: tau=6, lambda=0`; `29: tau=2, lambda=log 29` |

Two facts are visible:

1. Deconvolved mass is nonnegative and prime-power supported.
2. GWR selection and deconvolved support do not coincide in general.

The first fact comes from the quotient algebra. The second fact limits what
the Interior Maximizer Theorem can prove by itself.

## Local Consequence

The first nontrivial consequence is:

> **Local Deconvolved Support Consequence.**
> In every chamber packet `C(p,q)`, the deconvolved chamber-load mass is
> nonnegative and supported exactly on the endpoint prime `q` and any interior
> prime powers. The Interior Maximizer Theorem identifies when the first
> minimum-excess interior point is one of those support points. It does not
> make non-prime-power minima carry deconvolved mass.

This is the short-interval consequence that can be checked locally.

It is strong enough to rule out one false route:

```text
GWR-selected interior minimum
-> always positive deconvolved packet mass
```

That implication is false. The chamber `(5,7]` has selected interior `6`, but
`lambda(6)=0`.

## Why This Does Not Yet Give Spectral Centering

The completed folded object lives in

$$
z=u^2,
\qquad
\Xi(u)=\xi\left(\frac12+u\right).
$$

To force spectral centering, the completed deconvolved mass must become a
nonnegative reciprocal-balanced measure:

$$
\frac{1}{2u}\frac{\Xi'(u)}{\Xi(u)}
=
\int_0^\infty \frac{d\mu(t)}{z+t}.
$$

The local support consequence does not give this. It gives nonnegative support
on prime powers before completion. Reciprocal balance requires more:

```text
prime-power support inside chamber packets
-> completion corrections
-> fold t and -t around u = 0
-> no unmatched one-sided drift
-> nonnegative z-kernel
```

The missing step is the survival of chamber order through this entire chain.

## Minimal Additional Input

The next input cannot be the raw Interior Maximizer Theorem alone. It must be a
deconvolution-sensitive strengthening:

> **Prime-Power Packet Dominance Input.**
> For each chamber packet, the GWR-ordered minimum-excess structure controls
> the prime-power support created by
> $$
> \lambda=\tau_{\mathrm{Dir}}^{-1}*H
> $$
> strongly enough that, after completion, every one-sided log-scale drift is
> paired with a reciprocal packet of at least equal folded weight.

This is the first genuinely PGS-side arithmetic property that would make the
Chamber-Deconvolved Reciprocal Balance Lemma plausible.

A proof must show one of the following:

- the GWR-selected point controls all later prime-power support in its chamber
  packet after deconvolution;
- endpoint mass `log q` and interior prime-power masses combine into a
  reciprocal packet with a nonnegative folded square contribution;
- chambers with zero selected-point deconvolved mass are compensated by an
  adjacent endpoint or prime-power packet under a deterministic chamber-order
  rule;
- deconvolution leakage from non-prime-power minima cancels exactly into the
  zero coefficients of `Lambda(n)` without creating negative folded mass after
  completion.

Each form is local enough to test and strong enough to matter.

## Immediate Checkable Obstruction

The chamber `(5,7]` is the first obstruction to any selector-only proof:

$$
w=6,\qquad \tau(6)=4,\qquad \lambda(6)=0.
$$

So the sign-regularity proof cannot say:

```text
selected minimum carries the positive folded mass
```

The proof must say instead:

```text
selected minimum orders the chamber packet;
deconvolution extracts endpoint and prime-power mass;
completion folds the extracted packet into reciprocal balance.
```

That is the exact bridge still absent.

## Proof-State Result

This note derives the first local consequence of deconvolution sign-regularity:
after deconvolution, chamber packets have nonnegative support at endpoint
primes and interior prime powers, and GWR only detects that support when the
selected minimum is itself a prime power.

The note does not prove reciprocal balance. It shows where the next arithmetic
input must enter: prime-power packet dominance after deconvolution and before
completion.
