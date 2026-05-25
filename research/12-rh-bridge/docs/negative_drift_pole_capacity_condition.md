# Negative-Drift Pole Capacity Condition

Date: 2026-05-24

Status: arithmetic test forced by the one-sided trivial-zero regularization
candidate.

The one-sided trivial-zero regularization has

$$
T^{\mathrm{triv,reg}}_+(z)=0.
$$

Therefore the positive odd capacity side of the Transport Capacity Balance
Identity is supplied entirely by the pole pair:

$$
D_-(z)=T^{\mathrm{pole}}_+(z).
$$

Using the explicit pole capacity,

$$
T^{\mathrm{pole}}_+(z)=\frac{1}{2(z+1/4)}.
$$

## Exact Packet-Sum Requirement

For each chamber packet,

$$
D_{p,q}(z)=\sum_{n\in P(p,q)}\lambda(n)J_z(x_n).
$$

The negative-drift demand is

$$
D_-(z)=
\sum_{(p,q):D_{p,q}(z)<0}
|D_{p,q}(z)|.
$$

Thus the one-sided regularization candidate requires

$$
\boxed{
\sum_{(p,q):D_{p,q}(z)<0}
\left|
\sum_{n\in P(p,q)}\lambda(n)J_z(x_n)
\right|
=
\frac{1}{2(z+1/4)}
}.
$$

This is the exact arithmetic test.

## GWR-Envelope Necessary Condition

Let `w` be the GWR selector in `I(p,q)` and let `d = tau(w)`. Split the packet
interior as

$$
P_-=\{n\in P(p,q):n<w\},
\qquad
P_+=\{n\in P(p,q):w<n<q\}.
$$

The existing selector envelope gives

$$
\lambda(n)<\frac{\log w}{d}
\quad(n\in P_-),
\qquad
\lambda(n)<\frac{\log q}{d-1}
\quad(n\in P_+).
$$

Therefore every negative-drift packet satisfies

$$
|D_{p,q}(z)|
\le
\log q\,|J_z(x_q)|
+
\frac{\log w}{d}\sum_{n\in P_-}|J_z(x_n)|
+
\frac{\log q}{d-1}\sum_{n\in P_+}|J_z(x_n)|.
$$

A necessary envelope-level condition for the one-sided regularization is

$$
\frac{1}{2(z+1/4)}
\le
\sum_{(p,q):D_{p,q}(z)<0}
\left[
\log q\,|J_z(x_q)|
+
\frac{\log w}{d}\sum_{n\in P_-}|J_z(x_n)|
+
\frac{\log q}{d-1}\sum_{n\in P_+}|J_z(x_n)|
\right].
$$

## Proof-State Result

The one-sided trivial-zero regularization candidate now has a direct
arithmetic test:

```text
total negative packet drift = pole positive odd capacity.
```

If this equality fails, then the one-sided regularization cannot close the
Transport Capacity Balance Identity. A successful proof would need either an
exact identity for the packet drift sum above or an exact alternative
completion representation that supplies positive trivial-zero transport
capacity.

The class decomposition of the negative-drift side is recorded in
[Negative-Drift Class Decomposition](negative_drift_class_decomposition.md).
