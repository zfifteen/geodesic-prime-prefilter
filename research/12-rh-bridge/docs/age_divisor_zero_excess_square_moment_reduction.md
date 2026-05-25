# Age-Divisor To Zero-Excess Square-Moment Reduction

Date: 2026-05-24

Status: conditional reduction from the age-divisor energy bound to the
zero-excess return square-moment theorem.

The zero-excess return square moment is the endpoint-chain bound

$$
\sum_{X<q\le2X}g(q)^2
\ll
X(\log X)^B,
$$

where `p(q)<q` are consecutive prime endpoints and

$$
g(q)=q-p(q).
$$

This note records the exact reduction from that theorem to the age-divisor
recurrence potential.

## PGS Objects

For an integer `n`, let

$$
p(n)=\max\{p\le n:p\text{ is prime}\},
\qquad
a(n)=n-p(n).
$$

The zero-excess age `a(n)` is zero at prime endpoints and increases by one
inside a positive-excess chamber.

Let

$$
\sigma(n)=\tau(n)-2.
$$

Inside a chamber interior, `sigma(n) >= 1`. Define the age-divisor potential

$$
\Phi(n)=a(n)\sigma(n)=(n-p(n))(\tau(n)-2).
$$

This is the source-side recurrence potential: age times divisor surplus.

## Conditional Energy Theorem

Assume the dyadic age-divisor energy bound

$$
\boxed{
\sum_{X<n\le2X}\Phi(n)
\ll
X(\log X)^B.
}
$$

Then the zero-excess return square-moment theorem follows.

## Proof

Fix a chamber `(p,q]` with gap `g=q-p`. For `1 <= j < g`,

$$
a(p+j)=j,
\qquad
\sigma(p+j)\ge1.
$$

Therefore the chamber age-divisor energy satisfies

$$
\sum_{j=1}^{g-1}\Phi(p+j)
=
\sum_{j=1}^{g-1}j\,\sigma(p+j)
\ge
\sum_{j=1}^{g-1}j
=
{g(g-1)\over2}.
$$

For every nontrivial prime gap `g >= 2`, this gives

$$
g^2\ll
\sum_{p<n<q}\Phi(n).
$$

Now sum over endpoints `q` in `(X,2X]`. The finite small endpoints are
absorbed into the constant. For all large endpoints, the chamber ending at
`q` lies inside the enlarged dyadic block `(X/2,2X]` by the endpoint
separation `p(q)>q/2`; hence

$$
\sum_{X<q\le2X}g(q)^2
\ll
\sum_{X/2<n\le2X}\Phi(n).
$$

Applying the age-divisor energy bound on `(X/2,X]` and `(X,2X]` gives

$$
\sum_{X<q\le2X}g(q)^2
\ll
X(\log X)^B.
$$

This is the Zero-Excess Return Square-Moment Theorem.

## Role Of GWR Ordering

`PROOF.md` supplies the local GWR structure:

```text
inside a fixed chamber, the selected integer is the leftmost minimum-excess
interior point.
```

That theorem identifies the local minimum of divisor surplus after the chamber
exists. The reduction above uses a different chamberwide fact: every interior
integer carries positive divisor surplus, so the accumulated age-divisor
energy has a quadratic lower cost in the return time.

GWR ordering is compatible with the potential because it names the least-load
interior point. It does not yet prove the required dyadic upper bound on

$$
\sum_{X<n\le2X}\Phi(n).
$$

The missing transmission is from local leftmost minimum-excess ordering to a
global upper bound on accumulated chamber persistence energy.

## Remaining Global Control

The exact remaining PGS invariant is:

> **Age-Divisor Energy Bound.**
> $$
> \sum_{X<n\le2X}(n-p(n))(\tau(n)-2)
> \ll
> X(\log X)^B.
> $$

This can be supplied by any one of the following equivalent or sufficient
global controls:

1. **Persistence-energy decay.**
   Positive-excess chambers have total dyadic age-divisor energy
   `O(X log^B X)`.

2. **Divisor-channel age orthogonality.**
   Uniformly for `2 <= d <= sqrt(2X)`,
   $$
   \sum_{\substack{X<n\le2X\\d\mid n}}(n-p(n))
   \ll
   {X\over d}(\log X)^B.
   $$

3. **Uncovered-set or covering-tail theorem.**
   Complete positive-excess coverage of long intervals by proper-divisor
   channels has an `H^{-2}` dyadic tail.

4. **GWR persistence transfer.**
   The leftmost minimum-excess selector controls the whole chamber's
   age-divisor load in aggregate over a dyadic endpoint block.

The current repository proves the local GWR selector theorem. It does not yet
prove any one of these global controls.

## Bridge Consequence

The leading endpoint counterterm route now has a strict implication chain:

```text
Age-Divisor Energy Bound
-> Zero-Excess Return Square-Moment Theorem
-> Reciprocal Square-Gap Energy Lemma
-> Endpoint log-gap finite part
-> leading finite part C_eg/(2z) of E_X(z).
```

Thus the leading term of the reciprocal endpoint counterterm is reduced to
the age-divisor energy bound. The next proof obligation is a dyadic upper
bound for total age-divisor persistence.
