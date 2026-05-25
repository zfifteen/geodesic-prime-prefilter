# Negative-Drift Class Decomposition

Date: 2026-05-24

Status: class decomposition note for the Negative-Drift Pole Capacity
Condition.

The one-sided trivial-zero regularization requires

$$
D_-(z)=\frac{1}{2(z+1/4)}.
$$

This note decomposes `D_-(z)` by chamber class.

## Class Labels

For a chamber packet `P(p,q)`, let `w` be the GWR selector.

The selector type is

```text
selector_prime_power
selector_composite
```

depending on whether `w` is a prime power.

The interior prime-power position class is

```text
no_interior_prime_power
largest_pp_left_of_center
largest_pp_right_of_center
largest_pp_at_center.
```

The position is determined by the largest interior prime power `r` in the
packet, using

$$
x_r=\log\frac{r}{\sqrt{pq}}.
$$

## Decomposition

For selector class `sigma` and position class `beta`, define

$$
\mathcal C_{\sigma,\beta}(z)
=
\{(p,q):D_{p,q}(z)<0,\ (p,q)\text{ has class }(\sigma,\beta)\}.
$$

Then

$$
D_-(z)=
\sum_{\sigma,\beta}
D_-^{\sigma,\beta}(z),
$$

where

$$
D_-^{\sigma,\beta}(z)
=
\sum_{(p,q)\in\mathcal C_{\sigma,\beta}(z)}
|D_{p,q}(z)|.
$$

The pole-only condition becomes

$$
\sum_{\sigma,\beta}
D_-^{\sigma,\beta}(z)
=
\frac{1}{2(z+1/4)}.
$$

## Structural Constraints

### Endpoint-Only Packets

If a chamber has no interior prime-power packet mass, then

$$
P(p,q)=\{q\}.
$$

Since

$$
x_q=\log\frac{q}{\sqrt{pq}}>0,
$$

we have

$$
D_{p,q}(z)=\lambda(q)J_z(x_q)>0.
$$

Therefore

$$
D_-^{\sigma,\mathrm{no\_interior\_prime\_power}}(z)=0.
$$

Endpoint-only packets never contribute to negative drift.

### Left-Dominance Requirement

For any packet to have negative drift, its left-of-center interior prime-power
mass must dominate the endpoint and all right-of-center interior mass:

$$
\sum_{\substack{n\in P(p,q)\\ x_n<0}}
\lambda(n)|J_z(x_n)|
>
\lambda(q)J_z(x_q)
+
\sum_{\substack{n\in P(p,q)\\ 0<x_n< x_q}}
\lambda(n)J_z(x_n).
$$

Thus every negative-drift chamber contains at least one interior prime power
left of center.

### Largest-Prime-Power Position

If the largest interior prime power is left of center, then all interior
prime-power support lies left of center. The negative-drift condition reduces
to

$$
\sum_{n\in P(p,q),\,n<q}
\lambda(n)|J_z(x_n)|
>
\lambda(q)J_z(x_q).
$$

If the largest interior prime power is right of center, then negative drift is
possible only if earlier left-of-center prime powers dominate both the endpoint
and the later right-of-center prime powers.

## GWR-Envelope Class Bound

For a negative-drift packet in class `(\sigma,\beta)`, the existing
selector-to-packet envelope gives

$$
|D_{p,q}(z)|
\le
\log q\,|J_z(x_q)|
+
\frac{\log w}{d}\sum_{n\in P_-}|J_z(x_n)|
+
\frac{\log q}{d-1}\sum_{n\in P_+}|J_z(x_n)|.
$$

Thus each class contribution satisfies

$$
D_-^{\sigma,\beta}(z)
\le
\sum_{(p,q)\in\mathcal C_{\sigma,\beta}(z)}
\left[
\log q\,|J_z(x_q)|
+
\frac{\log w}{d}\sum_{n\in P_-}|J_z(x_n)|
+
\frac{\log q}{d-1}\sum_{n\in P_+}|J_z(x_n)|
\right].
$$

## Resulting Constraint

The pole-only positive-side condition can receive contributions only from
classes with left-of-center interior prime-power mass. The exact class
identity is

$$
\sum_{\sigma}
\left(
D_-^{\sigma,\mathrm{largest\_pp\_left\_of\_center}}(z)
+
D_-^{\sigma,\mathrm{largest\_pp\_right\_of\_center}}(z)
\right)
=
\frac{1}{2(z+1/4)}.
$$

The `no_interior_prime_power` class is excluded identically.

The left-of-center dominant class is isolated in
[Left-Dominant Negative-Drift Condition](left_dominant_negative_drift_condition.md).
