# Pole-Pair Odd Capacity

Date: 2026-05-24

Status: explicit finite-capacity calculation for the Transport Capacity
Balance Identity.

The pole-pair completion term is

$$
C_{\mathrm{pole}}(s)=-\frac1s-\frac1{s-1}.
$$

Set

$$
u=s-\frac12.
$$

Then

$$
C_{\mathrm{pole}}(u)
=
-\frac{1}{u+1/2}
-\frac{1}{u-1/2}.
$$

Thus the centered pole atoms are located at

$$
y_-=-\frac12,
\qquad
y_+=\frac12,
$$

and both residues are `-1`.

## Odd Capacities

For

$$
J_z(y)=\frac{y}{z+y^2},
$$

the signed odd capacities are

$$
O_-(z)=(-1)J_z(-1/2)
=
\frac{1/2}{z+1/4},
$$

and

$$
O_+(z)=(-1)J_z(1/2)
=
-\frac{1/2}{z+1/4}.
$$

Therefore the pole pair contributes equal positive and negative capacity:

$$
T^{\mathrm{pole}}_+(z)=\frac{1}{2(z+1/4)},
$$

and

$$
T^{\mathrm{pole}}_-(z)=\frac{1}{2(z+1/4)}.
$$

## Contribution To Balance

The pole pair supplies a symmetric finite transport reservoir:

$$
T^{\mathrm{pole}}_+(z)=T^{\mathrm{pole}}_-(z).
$$

It can pay equal amounts of positive and negative packet drift demand. Any
sidewise imbalance beyond this finite symmetric capacity must be supplied by
the trivial-zero reservoir.

