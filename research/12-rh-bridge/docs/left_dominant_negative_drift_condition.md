# Left-Dominant Negative-Drift Condition

Date: 2026-05-24

Status: dominant-class reduction for the Negative-Drift Pole Capacity
Condition.

The negative-drift class decomposition shows that endpoint-only packets never
contribute to

$$
D_-(z).
$$

The dominant structural class is:

```text
largest interior prime power left of center.
```

In this class, all interior prime-power packet mass lies left of center.

## Class Definition

Let

$$
\mathcal L(z)=
\{(p,q):D_{p,q}(z)<0,\ \text{largest interior prime power has }x<0\}.
$$

For $(p,q)\in\mathcal L(z)$, the packet drift is

$$
D_{p,q}(z)
=
\lambda(q)J_z(x_q)
+
\sum_{\substack{n\in P(p,q)\\ n<q}}
\lambda(n)J_z(x_n),
$$

with

$$
x_q>0,
\qquad
x_n<0
\quad(n<q,\ n\in P(p,q)).
$$

Thus

$$
|D_{p,q}(z)|
=
\sum_{\substack{n\in P(p,q)\\ n<q}}
\lambda(n)|J_z(x_n)|
-
\lambda(q)J_z(x_q).
$$

## Restricted Pole-Only Equality

Let `D_-^L(z)` be the left-dominant contribution:

$$
D_-^L(z)=
\sum_{(p,q)\in\mathcal L(z)}
\left[
\sum_{\substack{n\in P(p,q)\\ n<q}}
\lambda(n)|J_z(x_n)|
-
\lambda(q)J_z(x_q)
\right].
$$

If all negative-drift demand comes from the left-dominant class, the one-sided
regularization requires

$$
\boxed{
D_-^L(z)=\frac{1}{2(z+1/4)}
}.
$$

In the general class decomposition, the precise condition is

$$
D_-^L(z)
=
\frac{1}{2(z+1/4)}
-
D_-^R(z),
$$

where `D_-^R(z)` is the negative-drift contribution from packets whose largest
interior prime power is right of center but whose earlier left-of-center mass
still dominates.

## Selector Split

Split the left-dominant class by selector type:

$$
D_-^L(z)=D_-^{L,\mathrm{pp}}(z)+D_-^{L,\mathrm{comp}}(z).
$$

Here `pp` means the GWR selector is itself a prime power, and `comp` means the
selector is composite and carries no deconvolved mass.

The pole-only equality becomes

$$
D_-^{L,\mathrm{pp}}(z)
+
D_-^{L,\mathrm{comp}}(z)
=
\frac{1}{2(z+1/4)}
-
D_-^R(z).
$$

## Structural Constraint

A left-dominant packet contributes only its excess of left interior
prime-power drift over endpoint drift:

```text
left interior prime-power drift - endpoint drift.
```

Thus the class can satisfy the pole-only equality only if the aggregate
left-excess over all left-dominant packets equals the finite pole capacity
after subtracting any right-largest negative-drift contribution.

This imposes a weighted-sum constraint:

$$
\sum_{(p,q)\in\mathcal L(z)}
\sum_{\substack{n\in P(p,q)\\ n<q}}
\lambda(n)|J_z(x_n)|
=
\sum_{(p,q)\in\mathcal L(z)}
\lambda(q)J_z(x_q)
+
\frac{1}{2(z+1/4)}
-
D_-^R(z).
$$

The left side is controlled only by interior prime-power placement and mass.
The right side is endpoint drift plus finite pole capacity. This is the
dominant-class arithmetic burden.
