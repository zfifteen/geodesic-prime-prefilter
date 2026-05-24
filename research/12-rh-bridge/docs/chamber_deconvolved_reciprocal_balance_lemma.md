# Chamber-Deconvolved Reciprocal Balance Lemma

Date: 2026-05-24

Status: central open target for the PGS-to-RH bridge.

The algebraic compression is exact. The local PGS theorems are proved under
their stated hypotheses. Raw chamber-wise centering is false. The remaining
object is the deconvolved chamber load: the source load after division by the
divisor-count series.

This note states the lemma that must now be owned directly.

## Source Objects

Let

$$
E(n)=\left(\frac{\tau(n)}{2}-1\right)\log n,
$$

so for `n > 1`,

$$
E(n)=0 \iff \tau(n)=2.
$$

The bridge load is

$$
H(n)=\log n+E(n)=\frac{\tau(n)\log n}{2}.
$$

Define the divisor-count series and chamber-load series by

$$
D(s)=\sum_{n\ge1}\frac{\tau(n)}{n^s}
=\zeta(s)^2,
$$

and

$$
B(s)=\sum_{n\ge1}\frac{H(n)}{n^s}
=-\frac12D'(s).
$$

The quotient is

$$
R(s)=\frac{B(s)}{D(s)}
=-\frac12\frac{D'(s)}{D(s)}
=-\frac{\zeta'(s)}{\zeta(s)}.
$$

Let $\lambda$ be the Dirichlet-deconvolved chamber-load coefficient sequence:

$$
\lambda=\tau_{\mathrm{Dir}}^{-1}*H,
$$

so that

$$
\sum_{n\ge1}\frac{\lambda(n)}{n^s}=R(s).
$$

Because $R(s)=-\zeta'(s)/\zeta(s)$,

$$
\lambda(n)=\Lambda(n).
$$

Thus the bridge no longer lives at raw chamber load alone. It lives at:

```text
raw chamber load H
-> Dirichlet deconvolution by D
-> lambda = Lambda
-> completion
-> folded centered coordinate z = u^2
```

## Completed Centered Object

Let

$$
\xi(s)=\frac12s(s-1)\pi^{-s/2}\Gamma(s/2)\zeta(s),
$$

and set

$$
\Xi(u)=\xi\left(\frac12+u\right),
\qquad
z=u^2.
$$

The completed logarithmic derivative is

$$
Q(s)=-\frac{\xi'(s)}{\xi(s)}.
$$

In terms of the deconvolved quotient,

$$
Q(s)=
R(s)
-\frac{1}{s}
-\frac{1}{s-1}
+\frac12\log\pi
-\frac12\frac{\Gamma'}{\Gamma}(s/2).
$$

The main term, pole terms, gamma term, and trivial-zero structure are therefore
not extra PGS source data. They are the completion corrections needed to move
from the quotient $R(s)$ to the nontrivial-zero object.

Define the centered folded logarithmic derivative

$$
S(z)=
-\frac{1}{2u}Q\left(\frac12+u\right)
=
\frac{1}{2u}\frac{\Xi'(u)}{\Xi(u)}.
$$

This is the object whose singularities encode the nontrivial zero placement in
the squared centered coordinate.

## Lemma Statement

> **Chamber-Deconvolved Reciprocal Balance Lemma.**
> The completed deconvolved chamber-load source determines a nonnegative
> measure $\mu$ on $[0,\infty)$ such that
> $$
> S(z)=\int_0^\infty \frac{d\mu(t)}{z+t}
> $$
> on the common domain of the completed quotient. Equivalently, after
> Dirichlet deconvolution by $D(s)$, completion, removal of the main and
> trivial terms, and folding into $z=u^2$, the chamber residual is
> reciprocal-balanced and nonnegative.

In discrete zero language, this is the assertion that

$$
S(z)=\sum_{\gamma>0}\frac{m_\gamma}{z+\gamma^2}
$$

with $m_\gamma>0$ and $\gamma^2\ge0$.

The lemma is strong enough to close the placement step:

```text
nonnegative Stieltjes representation in z
-> singular support only at z = -gamma^2
-> zeros of Xi occur only at u = +/- i gamma
-> zeros of zeta occur only on Re(s)=1/2
```

It is also exact enough for a hostile reviewer to inspect the remaining burden:
the PGS source must supply the nonnegative reciprocal balance after
deconvolution and completion. It is not enough to point to raw positive loads,
raw chamber order, or the quotient identity.

## What The Lemma Must Prove From PGS

The lemma must prove three properties.

1. **Deconvolution survival.**
   The chamber structure is not destroyed by
   $$
   \lambda=\tau_{\mathrm{Dir}}^{-1}*H.
   $$
   The deconvolved coefficients $\lambda(n)=\Lambda(n)$ must still admit a
   chamber-derived decomposition rather than becoming only a global zeta-side
   sequence.

2. **Reciprocal balance.**
   After completion, the deconvolved chamber residual must fold evenly around
   $u=0$. In log-scale language, all nontrivial carriers with real exponent
   $a\ne0$ must cancel:
   $$
   e^{a\log x+i\gamma\log x}
   $$
   cannot survive the completed folded residual.

3. **Nonnegative folded mass.**
   The folded residual must be positive in the Stieltjes sense. Equivalently,
   the final kernel must be a positive measure on the nonnegative `t` axis,
   not a signed symmetric distribution.

These are the missing source-side tasks. The first two are balance tasks. The
third is a positivity task.

## Why Raw Chamber Order Is Not Enough

A raw chamber-centered claim fails immediately in the first nonempty chamber:

$$
p=3,\qquad q=5,\qquad I=\{4\}.
$$

Center in log scale:

$$
t_4=\log\frac{4}{\sqrt{15}}>0.
$$

Since $\tau(4)=3$,

$$
E(4)=\log2.
$$

The first centered odd moment is

$$
M_1=\log2\cdot\log\frac{4}{\sqrt{15}}>0.
$$

Thus raw finite chambers are not individually centered. Any proof of the lemma
must use a global completion or deconvolution mechanism. It cannot say that
each chamber block is already a centered spectral block.

## Proof-Strategy Note

The shortest viable proof path is:

```text
Interior chamber order
-> deconvolution sign-regularity
-> completed reciprocal pairing
-> positive folded z-kernel
-> spectral centering
```

The already-proved Interior Maximizer Theorem contributes only the first item:
inside a nonempty chamber, the leftmost minimum-divisor integer is the ordered
minimum of the zero-excess coordinate. That gives local order. It does not give
reciprocal balance.

The minimal additional input needed from chamber ordering is therefore:

> **Deconvolution Sign-Regularity Input.**
> The ordered chamber minima and endpoint returns force the Dirichlet inverse
> interaction $\tau_{\mathrm{Dir}}^{-1}*H$ to organize into chamber packets
> whose completed log-scale fold has no negative folded mass and no unmatched
> one-sided drift.

This input must be more precise than "chambers are ordered." A usable form
would be one of:

- a chamber-packet square decomposition of the completed Weil or Li quadratic
  form;
- a total-positivity statement for the Dirichlet-deconvolution operator
  restricted to PGS chamber packets;
- an involution pairing the deconvolved post-completion log-coordinate mass at
  `+t` and `-t`, with nonnegative folded weights;
- an exact inequality showing that the GWR-selected chamber minimum dominates
  every deconvolution leakage term that could create an off-center carrier.

The proof should not begin from zeros. It should begin with chamber packets
and show that deconvolution plus completion converts those packets into a
positive folded kernel.

## First Attack Surface

The first concrete attack is finite and deterministic:

1. Compute $\lambda=\tau_{\mathrm{Dir}}^{-1}*H$ exactly on a bounded prefix.
2. Partition $\lambda$ by source chamber, preserving which raw $H(m)$ terms
   feed each $\lambda(n)$ through the divisors of `n`.
3. Apply the explicit completion corrections separately:
   main term, pole terms, and gamma/trivial-zero terms.
4. Fold the resulting packet in the centered log coordinate.
5. Test whether the folded packet has a signed negative part or unmatched odd
   drift.

Failure at step 5 invalidates this route in its current packet form.
Success at step 5 would not prove the lemma, but it would identify the exact
finite algebraic structure that the symbolic proof must explain.

The first local consequence of this attack is recorded in
[Deconvolution Sign-Regularity From Chamber Ordering](deconvolution_sign_regularity_from_chamber_ordering.md).
It shows that deconvolved chamber mass is nonnegative and supported at endpoint
primes plus interior prime powers, while the GWR-selected point carries that
mass only when it is itself a prime power.

## Current Proof State

The lemma is open.

The exact quotient is proved. The local chamber theorems are proved. Raw
chamber-wise centering is invalidated. The live hinge is whether PGS chamber
ordering survives Dirichlet deconvolution and completion as a nonnegative
reciprocal balance in the folded coordinate `z = u^2`.
