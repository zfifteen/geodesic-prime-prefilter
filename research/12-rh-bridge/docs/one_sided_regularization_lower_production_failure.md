# One-Sided Regularization Lower-Production Failure

Date: 2026-05-24

Status: proof-state decision note for the one-sided trivial-zero
regularization route.

The GWR selector envelopes and the left-of-center position constraint do not
produce a positive lower bound for the left-excess drift. They also do not
produce an exact identity equating negative packet drift with finite pole
capacity.

This decides the one-sided trivial-zero regularization route at the present
proof level.

## Inputs Available From Chamber Ordering

For a left-dominant negative-drift packet,

$$
E_{p,q}^L(z)
=
\sum_{\substack{n\in P(p,q)\\ n<q}}
\lambda(n)|J_z(x_n)|
-
\lambda(q)J_z(x_q).
$$

The left-dominant condition gives

$$
x_n<0
\qquad(n<q,\ n\in P(p,q)).
$$

The GWR selector envelope gives only coefficient upper bounds:

$$
n<w\Rightarrow \lambda(n)<\frac{\log w}{d},
$$

$$
n=w\Rightarrow \lambda(n)=\frac{\log w}{d-1},
$$

and

$$
w<n<q\Rightarrow \lambda(n)<\frac{\log q}{d-1}.
$$

These inputs imply the upper envelope recorded in
[Left-Excess Drift Envelope Against Pole Capacity](left_excess_drift_envelope.md).

They do not imply

$$
E_{p,q}^L(z)\ge c_{p,q}(z)>0
$$

for any explicit chamber-local quantity supplied by current PGS machinery.

## Why No Lower Bound Follows

The available inequalities control the possible size of the left interior
prime-power coefficients from above. A lower-production theorem would need to
force the strict excess

$$
\sum_{\substack{n\in P(p,q)\\ n<q}}
\lambda(n)|J_z(x_n)|
-
\lambda(q)J_z(x_q)
$$

to be bounded below by a positive expression.

The present chamber inputs do not do that.

At inequality level, the interior side can approach the endpoint side with
arbitrarily small positive slack. The sign condition `x_n < 0` fixes which
side of the folded center the carrier occupies, but it does not force a
positive amount of excess over the endpoint contribution.

Thus the existing GWR machinery proves:

```text
if a left-dominant packet contributes negative drift, its contribution is
bounded above by the selector envelope.
```

It does not prove:

```text
left-dominant packets produce a prescribed positive amount of negative drift.
```

## Why No Exact Production Identity Follows

The one-sided trivial-zero regularization requires

$$
D_-(z)=\frac{1}{2(z+1/4)}.
$$

After class decomposition this becomes

$$
D_-^L(z)+D_-^R(z)=\frac{1}{2(z+1/4)}.
$$

The right side is the finite pole capacity. It is an exact rational function
of `z`.

The left side is a global sign-selected sum of local prime-power packet
drifts:

$$
D_-^L(z)+D_-^R(z)
=
\sum_{D_{p,q}(z)<0}
\left|
\sum_{n\in P(p,q)}\lambda(n)J_z(x_n)
\right|.
$$

The selector envelopes are local coefficient inequalities. They contain no
summation law that can identify this sign-selected global function with the
pole rational function.

An exact identity of this type would be a new global analytic theorem, not a
consequence of the current local chamber-ordering theorems.

## Finite-Surface Obstruction

On the deterministic finite diagnostic surface `q <= 1,000,000`, the
one-sided pole identity does not behave like a monotone local production law.

At

$$
z=0.0001,
$$

the single chamber `(47,53]` contributes

$$
D_-^L(z)=17.3329686,
$$

while the pole capacity is

$$
\frac{1}{2(z+1/4)}=1.99920032.
$$

At

$$
z\in\{0.001,0.01,0.1,1,10\},
$$

the same finite surface has no negative packet drift, while the pole capacity
remains positive.

This measured surface is not a proof against a regularized infinite identity.
It does rule out the interpretation that the current chamber ordering supplies
the pole capacity by monotone finite accumulation of left-dominant packets.

## Proof-State Decision

The one-sided trivial-zero regularization route cannot be closed from the
current GWR selector envelopes and left-of-center position constraint.

The remaining choices are exact:

```text
1. prove a new independent global identity for D_-^L(z)+D_-^R(z);
```

or

```text
2. abandon the one-sided regularization as the bridge route and use a
completion representation in which the trivial-zero reservoir supplies
positive transport capacity as well as negative transport capacity.
```

The second path is now the live continuation of the Chamber-Deconvolved
Reciprocal Balance Lemma program. It moves the burden from local GWR lower
production to a symmetric or sign-regularized completion-capacity
decomposition.
