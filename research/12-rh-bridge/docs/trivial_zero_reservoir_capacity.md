# Trivial-Zero Reservoir Capacity

Date: 2026-05-24

Status: first structural analysis of the infinite transport reservoir.

The gamma part of the completion correction is

$$
C_\Gamma(s)=-\frac12\frac{\Gamma'}{\Gamma}(s/2).
$$

Using the digamma expansion

$$
\frac{\Gamma'}{\Gamma}(z)
=
-\gamma
+
\sum_{m=0}^{\infty}
\left(
\frac{1}{m+1}-\frac{1}{m+z}
\right),
$$

with `z = s/2`, we get

$$
C_\Gamma(s)
=
\frac{\gamma}{2}
-
\sum_{m=0}^{\infty}\frac{1}{2(m+1)}
+
\sum_{m=0}^{\infty}\frac{1}{s+2m}.
$$

The zero-radius regularization constants are handled separately. The
transport atoms are

$$
\frac{1}{s+2m},
\qquad
m\ge0.
$$

## Centered Transport Atoms

Set

$$
u=s-\frac12.
$$

The atom at `s = -2m` is located at

$$
y_m=-2m-\frac12.
$$

Its completion mass is `+1`, so its signed odd capacity is

$$
O_m(z)=J_z(y_m)
=
\frac{-2m-1/2}{z+(2m+1/2)^2}.
$$

Thus every raw trivial-zero transport atom contributes negative odd capacity:

$$
O_m(z)<0.
$$

Formally,

$$
T^{\mathrm{triv}}_-(z)
=
\sum_{m=0}^{\infty}
\frac{2m+1/2}{z+(2m+1/2)^2},
$$

and

$$
T^{\mathrm{triv}}_+(z)=0.
$$

## Convergence Issue

The raw negative capacity series behaves like

$$
\sum_{m\ge1}\frac{1}{2m},
$$

so it diverges logarithmically. Therefore the trivial-zero transport capacity
cannot be used as an ordinary absolutely convergent positive reservoir without
regularization.

The regularization constants in the digamma expansion have zero odd transport
capacity because they sit at `x = 0`. They regularize the analytic gamma
factor, but they do not directly contribute to the sidewise odd capacity.

## First Structural Consequence

The raw trivial-zero reservoir is one-sided:

```text
trivial zeros supply negative odd capacity only.
```

The positive odd capacity side must come from the pole atom at `u = -1/2` and
any additional completion-side structure not yet represented in the raw
trivial-zero atom list.

The main analytic issue is therefore sharper than convergence alone:

> Define a regularized sign-separated capacity for the gamma/trivial-zero
> reservoir that preserves the completed quotient and explains how the
> positive side of the Transport Capacity Balance Identity is supplied.

Until that regularized sidewise capacity is defined, the infinite
trivial-zero reservoir cannot close the Transport Capacity Balance Identity.

The first one-sided finite-part candidate is recorded in
[Trivial-Zero Capacity Regularization Candidate](trivial_zero_capacity_regularization_candidate.md).
