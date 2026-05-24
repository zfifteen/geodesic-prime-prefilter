# Prime-Power Packet Dominance Under Chamber Ordering

Date: 2026-05-24

Status: local proof-strategy note for the Chamber-Deconvolved Reciprocal
Balance Lemma.

The current obstruction is precise. After Dirichlet deconvolution, the chamber
load no longer lives on every low-excess interior integer. It lives on prime
powers:

$$
\lambda=\tau_{\mathrm{Dir}}^{-1}*H,
\qquad
\lambda(n)=\Lambda(n).
$$

The Interior Maximizer Theorem orders the raw chamber by the leftmost minimum
of $E(n)$. It does not say that the selected point is a prime power. Therefore
the next local target is not selector positivity. The target is prime-power
packet dominance.

## Source And Packet

Let `p < q` be consecutive primes. The open chamber is

$$
I(p,q)=\{p+1,\ldots,q-1\}.
$$

The closed-right packet is

$$
C(p,q)=\{p+1,\ldots,q\}.
$$

The deconvolved packet support is

$$
P(p,q)=\{q\}\cup\{n\in I(p,q):n=r^k,\ r\text{ prime},\ k\ge2\}.
$$

Its weights are

$$
\lambda(n)=\Lambda(n)
=
\begin{cases}
\log r,& n=r^k,\\
0,& \text{otherwise}.
\end{cases}
$$

The endpoint `q` always contributes:

$$
\lambda(q)=\log q.
$$

Interior composites contribute only when they are prime powers.

## GWR Selector

The Interior Maximizer Theorem selects

$$
w=\min\{n\in I(p,q):\tau(n)=\min_{m\in I(p,q)}\tau(m)\}.
$$

Equivalently, `w` is the leftmost minimum of the zero-excess coordinate

$$
E(n)=\left(\frac{\tau(n)}{2}-1\right)\log n.
$$

The selector can be a prime power, but it need not be. If it is a prime power,
then it carries deconvolved mass. If it is not a prime power, then

$$
\lambda(w)=0.
$$

So the proof cannot use:

```text
selected minimum -> positive deconvolved mass at the selected point
```

That implication is false.

## What Dominance Must Mean

Prime-power packet dominance must be a statement about the packet
`P(p,q)`, not about the selector alone.

At the deconvolved coefficient level, dominance means:

> The GWR-ordered chamber structure controls the endpoint and interior
> prime-power packet strongly enough that, after completion and folding into
> `z = u^2`, all one-sided log-coordinate drift from the packet is paired by
> reciprocal mass with nonnegative folded weight.

In local terms, the packet must satisfy a condition of this shape:

```text
GWR order of I(p,q)
-> control of P(p,q)
-> completion/folding pairs packet drift at +t and -t
-> no negative folded mass in z = u^2
```

The control cannot be raw mass positivity. The packet weights are already
nonnegative because $\Lambda(n)\ge0$. The missing property is reciprocal
balance after completion.

A usable local dominance theorem would need to prove one of these:

1. Endpoint dominance: the endpoint mass `log q` absorbs every unmatched
   interior prime-power drift created by `P(p,q)`.
2. Selector-to-packet dominance: even when `lambda(w)=0`, the selected
   minimum bounds where later packet support can occur and how much folded
   drift it can create.
3. Adjacent-packet dominance: chambers whose selector carries no deconvolved
   mass are balanced by deterministic endpoint or prime-power packets in
   neighboring chambers.

The current proved theorems in `PROOF.md` give the selector and the chamber
order. They do not yet prove any of these dominance statements.

## Diagnostic Examples

### Endpoint-Only Selector Obstruction: `(5,7]`

The open chamber is

$$
I(5,7)=\{6\}.
$$

The GWR-selected point is

$$
w=6,
\qquad
\tau(6)=4.
$$

But `6` is not a prime power, so

$$
\lambda(6)=0.
$$

The packet is endpoint-only:

$$
P(5,7)=\{7\},
\qquad
\lambda(7)=\log7.
$$

This is the first clear failure of selector positivity. Any dominance proof
must explain how an endpoint-only packet can still become a balanced folded
piece after completion.

### Later Prime-Power Packet: `(13,17]`

The open chamber is

$$
I(13,17)=\{14,15,16\}.
$$

The selected point is

$$
w=14,
\qquad
\tau(14)=4,
\qquad
\lambda(14)=0.
$$

But the chamber contains the later prime power

$$
16=2^4,
\qquad
\lambda(16)=\log2.
$$

The packet is

$$
P(13,17)=\{16,17\}.
$$

So GWR sees the first low-excess point at `14`, while deconvolution places the
interior positive mass at `16`. A dominance theorem must prove that the
ordered position of `14` controls the later support at `16`, or else provide
another chamber-local mechanism that does.

### Larger Later Prime-Power Packet: `(31,37]`

The open chamber is

$$
I(31,37)=\{32,33,34,35,36\}.
$$

The selected point is

$$
w=33,
\qquad
\tau(33)=4,
\qquad
\lambda(33)=0.
$$

The packet contains

$$
32=2^5,
\qquad
\lambda(32)=\log2,
$$

and the endpoint

$$
\lambda(37)=\log37.
$$

Here the positive interior prime-power mass lies before the selected point,
while the endpoint lies after it. This case rules out any one-directional
claim such as "positive packet mass always appears after the selector."

Dominance must be packet-level and folded, not left-to-right selector-level.

## First Consequence

The first local consequence is:

> **Packet-Support Consequence.**
> In every chamber packet, deconvolved positive mass is supported on the
> endpoint prime and any interior prime powers. The GWR selector orders the
> raw zero-excess chamber, but it does not by itself locate the deconvolved
> packet support.

This consequence follows from the exact quotient algebra and the Interior
Maximizer Theorem together. The quotient algebra gives support on prime
powers. The Interior Maximizer Theorem identifies the selector whose relation
to that support must be controlled.

It does not yet prove reciprocal balance.

## Required Additional Local Statement

The additional arithmetic statement still needed is:

> **Prime-Power Packet Dominance Input.**
> For every chamber packet `C(p,q)`, the GWR-ordered zero-excess structure
> controls the deconvolved packet
> $$
> P(p,q)=\{q\}\cup\{n\in I(p,q):n=r^k\}
> $$
> so that, after completion and folding into `z = u^2`, the packet contributes
> nonnegative reciprocal-balanced mass.

This is not currently proved in `PROOF.md`.

The known theorem gives:

```text
leftmost min-E selector
```

The missing local statement must give:

```text
selector-ordered chamber -> controlled prime-power packet -> folded balance
```

## Proof-State Result

Prime-Power Packet Dominance is now the minimal local arithmetic obligation.

The current chamber theorems do not supply it directly. They provide the order
that such a theorem must use. The deconvolution algebra provides the packet
support. The bridge still needs the dominance step that connects those two
objects before completion and folding.
