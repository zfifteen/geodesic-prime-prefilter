# Left-Excess Drift Envelope Against Pole Capacity

Date: 2026-05-24

Status: GWR-envelope bound for the left-dominant part of the
Negative-Drift Pole Capacity Condition.

The left-dominant class consists of negative-drift chamber packets whose
largest interior prime power lies left of the completed center. Thus every
interior prime-power carrier in the packet has negative centered coordinate.

This removes the right-interior correction term from the general
negative-drift envelope. The packet contribution is exactly the excess of
left interior prime-power drift over endpoint drift.

## Packet-Level Envelope

Let `p < q` be consecutive primes, let `w` be the GWR selector in
`I(p,q)`, and let

$$
d=\tau(w).
$$

For a left-dominant packet define

$$
E_{p,q}^L(z)
=
\sum_{\substack{n\in P(p,q)\\ n<q}}
\lambda(n)|J_z(x_n)|
-
\lambda(q)J_z(x_q).
$$

The packet has negative drift exactly when

$$
E_{p,q}^L(z)>0,
$$

and then

$$
|D_{p,q}(z)|=E_{p,q}^L(z).
$$

Split the interior prime-power support into

$$
P_{<}=\{n\in P(p,q):n<w\},
\qquad
P_{=}=\{w\}\cap P(p,q),
\qquad
P_{>}=\{n\in P(p,q):w<n<q\}.
$$

In the left-dominant class all of these interior support points satisfy

$$
x_n<0.
$$

The GWR selector envelope gives

$$
\lambda(n)<\frac{\log w}{d}\quad(n\in P_<),
$$

$$
\lambda(w)=\frac{\log w}{d-1}\quad(w\in P_=),
$$

and

$$
\lambda(n)<\frac{\log q}{d-1}\quad(n\in P_>).
$$

Therefore every left-dominant negative-drift packet satisfies

$$
E_{p,q}^L(z)
\le
B_{p,q}^L(z),
$$

where

$$
B_{p,q}^L(z)
=
\frac{\log w}{d}
\sum_{n\in P_<}|J_z(x_n)|
+
\frac{\log w}{d-1}
\sum_{n\in P_=}|J_z(x_n)|
+
\frac{\log q}{d-1}
\sum_{n\in P_>}|J_z(x_n)|
-
\log q\,J_z(x_q).
$$

This is sharper than the general class bound because no right-of-center
interior prime-power term appears with positive sign. The only positive
right-side packet contribution is the endpoint.

## Aggregate Compatibility Test

Let

$$
\mathcal L(z)=
\{(p,q):D_{p,q}(z)<0,\ \text{largest interior prime power has }x<0\}.
$$

Then

$$
D_-^L(z)
=
\sum_{(p,q)\in\mathcal L(z)}E_{p,q}^L(z)
\le
\sum_{(p,q)\in\mathcal L(z)}B_{p,q}^L(z).
$$

Equivalently, using the positive part to make the test purely one-sided,

$$
D_-^L(z)
\le
\sum_{(p,q)\in\mathcal L(z)}\max\{B_{p,q}^L(z),0\}.
$$

The one-sided trivial-zero regularization candidate requires

$$
D_-^L(z)
=
\frac{1}{2(z+1/4)}
-
D_-^R(z).
$$

Hence the GWR envelope imposes the necessary compatibility inequality

$$
\boxed{
\frac{1}{2(z+1/4)}
-
D_-^R(z)
\le
\sum_{(p,q)\in\mathcal L(z)}
\max\{B_{p,q}^L(z),0\}.
}
$$

If all negative drift is left-dominant, this reduces to

$$
\boxed{
\frac{1}{2(z+1/4)}
\le
\sum_{(p,q)\in\mathcal L(z)}
\max\{B_{p,q}^L(z),0\}.
}
$$

This is the first explicit pole-capacity compatibility test supplied by the
current chamber machinery.

## What The Bound Does Not Supply

The same inputs do not give a positive lower bound for `D_-^L(z)`.

The selector envelope controls each interior prime-power coefficient from
above. It does not force the left interior sum to exceed the endpoint by a
fixed amount. A packet can satisfy the structural inequalities while the
left-excess

$$
E_{p,q}^L(z)
$$

is arbitrarily close to zero at the level of the present inequalities.

Thus the current chamber technology supplies:

```text
upper envelope for possible left-excess drift
```

but not:

```text
lower production theorem for the pole capacity
```

The missing estimate is a lower-production statement or an exact summation
identity for left-dominant packet excess.

## Finite Diagnostic Surface

On the deterministic packet diagnostic surface `q <= 1,000,000`, the
left-dominant negative-drift contribution is visible only at the smallest
tested local scale in the grid:

| z | pole capacity | finite `D_-^L(z)` | finite envelope | contributing packets |
|---:|---:|---:|---:|---:|
| `0.0001` | `1.99920032` | `17.3329686` | `17.3329686` | `1` |
| `0.001` | `1.99203187` | `0` | `0` | `0` |
| `0.01` | `1.92307692` | `0` | `0` | `0` |
| `0.1` | `1.42857143` | `0` | `0` | `0` |
| `1` | `0.4` | `0` | `0` | `0` |
| `10` | `0.0487804878` | `0` | `0` | `0` |

At `z = 0.0001`, the single contributing chamber is

$$
(47,53],
\qquad
w=49,
\qquad
d=3,
\qquad
49=7^2.
$$

The measured finite surface is not a proof of the global regularized identity.
It shows a sharper obstruction: the pole-only positive-side condition is not
a monotone finite accumulation law. At one scale the finite left-dominant
partial sum already exceeds the pole capacity, while at larger tested scales
the finite surface contributes no negative drift at all.

## Resulting Local Obligation

The pole-only regularization route now requires one of two exact inputs:

```text
an exact regularized summation identity for D_-^L(z) + D_-^R(z)
```

or

```text
a revised completion capacity representation that supplies positive
trivial-zero transport capacity as well as pole transport capacity.
```

The GWR ordering and selector envelopes alone give the necessary upper
compatibility inequality above. They do not generate the finite pole capacity
from left-dominant packets.
