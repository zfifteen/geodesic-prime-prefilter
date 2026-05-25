# Kernel-Weighted Prime-Power Packet Estimate

Date: 2026-05-24

Status: target local arithmetic estimate for the Aggregate Completion-Cost
Bound.

## Objects

Let `p < q` be consecutive primes. Define

$$
I(p,q)=\{p+1,\ldots,q-1\},
$$

and let the GWR selector be

$$
w=\min\{n\in I(p,q):\tau(n)=\min_{m\in I(p,q)}\tau(m)\}.
$$

Write

$$
d=\tau(w).
$$

The deconvolved packet support is

$$
P(p,q)=\{q\}\cup\{n\in I(p,q):n=r^a,\ r\text{ prime},\ a\ge2\}.
$$

The weights are

$$
\lambda(q)=\log q,
\qquad
\lambda(r^a)=\log r.
$$

Use the centered chamber coordinate

$$
x_n=\log\frac{n}{\sqrt{pq}},
$$

and the kernels

$$
J_z(x)=\frac{x}{z+x^2},
\qquad
K_z(x)=\frac{1}{z+x^2}.
$$

Define the packet drift and packet folded reserve by

$$
D_{p,q}(z)=\sum_{n\in P(p,q)}\lambda(n)J_z(x_n),
$$

and

$$
R_{p,q}(z)=\sum_{n\in P(p,q)}\lambda(n)K_z(x_n).
$$

## Target Inequality

> **Kernel-Weighted Prime-Power Packet Estimate.**
> For every consecutive-prime chamber `p < q`,
> $$
> R_{p,q}(z)\ge C_{p,q}(z;w,d)\,|D_{p,q}(z)|,
> $$
> where $C_{p,q}(z;w,d)>0$ depends only on the chamber endpoints, the GWR
> selector `w` and its divisor count $d=\tau(w)$, and the prime-power support
> in $P(p,q)$.

This is the arithmetic input required by the Aggregate Completion-Cost Bound.
It uses only the selector-to-packet coefficient envelope and pointwise
endpoint dominance proved in
`local_control_of_prime_power_packets_by_gwr_ordering.md`.

The packet drift average bound is proved in
`packet_drift_weighted_average_lemma.md`.

The combined reduction with the completion transport radius is recorded in
`combined_reduction_with_weighted_average_lemma.md`.
