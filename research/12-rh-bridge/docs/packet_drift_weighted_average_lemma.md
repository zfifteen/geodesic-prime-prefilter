# Packet Drift Weighted Average Lemma

Date: 2026-05-24

Status: local arithmetic lemma for the Kernel-Weighted Prime-Power Packet
Estimate.

## Statement

Let `P` be a finite packet with coordinates `x_n`, nonnegative weights
`\lambda(n)`, and at least one positive weight. For `z > 0`, define

$$
K_z(x)=\frac{1}{z+x^2},
\qquad
J_z(x)=xK_z(x).
$$

Let

$$
D(z)=\sum_{n\in P}\lambda(n)J_z(x_n),
\qquad
R(z)=\sum_{n\in P}\lambda(n)K_z(x_n).
$$

Then

$$
\frac{|D(z)|}{R(z)}\le\max_{n\in P}|x_n|.
$$

## Proof

Since `z > 0`, `K_z(x_n) > 0` for every packet coordinate. Since the weights
are nonnegative and at least one is positive,

$$
R(z)>0.
$$

Define

$$
\alpha_n=\frac{\lambda(n)K_z(x_n)}{R(z)}.
$$

Then

$$
\alpha_n\ge0,
\qquad
\sum_{n\in P}\alpha_n=1.
$$

Using `J_z(x)=xK_z(x)`,

$$
\frac{D(z)}{R(z)}
=
\sum_{n\in P}\alpha_nx_n.
$$

Thus `D(z)/R(z)` is a weighted average of the packet coordinates. Therefore

$$
\left|\frac{D(z)}{R(z)}\right|
\le
\max_{n\in P}|x_n|.
$$

This proves the lemma.

## Corollary

For a prime-power packet `P(p,q)`, the Kernel-Weighted Prime-Power Packet
Estimate holds with

$$
C_{p,q}(z;w,d)=
\left(\max_{n\in P(p,q)}|x_n|\right)^{-1}.
$$

Equivalently, any positive lower bound on

$$
\left(\max_{n\in P(p,q)}|x_n|\right)^{-1}
$$

gives an admissible arithmetic constant in

$$
R_{p,q}(z)\ge C_{p,q}(z;w,d)|D_{p,q}(z)|.
$$
