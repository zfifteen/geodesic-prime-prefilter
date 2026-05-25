# Aggregate Completion-Cost Bound

Date: 2026-05-24

Status: bounding note for the Folded Packet Drift Inequality.

The Folded Packet Drift Inequality reduced the local RH-facing bridge to one
estimate:

$$
-\int K_z(x)\,d\eta_{p,q}(x)\le R_{p,q}(z),
$$

where

$$
K_z(x)=\frac{1}{z+x^2}
$$

and

$$
R_{p,q}(z)=\sum_{n\in P(p,q)}\lambda(n)K_z(x_n).
$$

This note bounds the left side using the packet controls already extracted
from GWR ordering.

## Packet Drift And Transport Cost

Use the centered coordinate

$$
x_n=\log\frac{n}{\sqrt{pq}},
$$

and the odd kernel

$$
J_z(x)=\frac{x}{z+x^2}=xK_z(x).
$$

The packet drift is

$$
D_{p,q}(z)=\sum_{n\in P(p,q)}\lambda(n)J_z(x_n).
$$

To cancel this drift, the completion correction must satisfy

$$
\int J_z(x)\,d\eta_{p,q}(x)=-D_{p,q}(z).
$$

Let `rho_{p,q}(z)` be an effective completion transport radius for this
packet: every unit of negative folded cost used by the completion correction
can cancel at least `rho_{p,q}(z)` units of odd drift. Equivalently, the
odd/even efficiency available to the correction is bounded below by
`rho_{p,q}(z)`.

Then the aggregate negative even folded cost satisfies the transport bound

$$
C^-_{p,q}(z)
:=
\max\left(0,-\int K_z(x)\,d\eta_{p,q}(x)\right)
\le
\frac{|D_{p,q}(z)|}{\rho_{p,q}(z)}.
$$

Thus the Aggregate Completion-Cost Bound closes if

$$
|D_{p,q}(z)|\le \rho_{p,q}(z)R_{p,q}(z).
$$

This is the exact reduced inequality.

## Insert The GWR Packet Envelope

Let

$$
w=\min\{n\in(p,q):\tau(n)=\min_{m\in(p,q)}\tau(m)\},
\qquad
d=\tau(w).
$$

Split the interior packet into

$$
P_-=\{n\in P(p,q):n<w\},
\qquad
P_+=\{n\in P(p,q):w<n<q\}.
$$

The packet endpoint is `q`, and

$$
\lambda(q)=\log q.
$$

The selector-to-packet coefficient envelope gives

$$
n\in P_-\Rightarrow \lambda(n)<\frac{\log w}{d},
$$

and

$$
n\in P_+\Rightarrow \lambda(n)<\frac{\log q}{d-1}.
$$

Therefore

$$
|D_{p,q}(z)|
\le
\log q\,|J_z(x_q)|
+
\frac{\log w}{d}\sum_{n\in P_-}|J_z(x_n)|
+
\frac{\log q}{d-1}\sum_{n\in P_+}|J_z(x_n)|.
$$

Combining this with the transport bound gives the explicit aggregate
completion-cost estimate

$$
C^-_{p,q}(z)
\le
\frac{1}{\rho_{p,q}(z)}
\left[
\log q\,|J_z(x_q)|
+
\frac{\log w}{d}\sum_{n\in P_-}|J_z(x_n)|
+
\frac{\log q}{d-1}\sum_{n\in P_+}|J_z(x_n)|
\right].
$$

This is the strongest aggregate upper bound supplied by the current GWR packet
controls.

## Coarse Count Form

The universal kernel bound

$$
|J_z(x)|\le\frac{1}{2\sqrt z}
$$

gives the coarser chamber-count estimate

$$
C^-_{p,q}(z)
\le
\frac{1}{2\rho_{p,q}(z)\sqrt z}
\left[
\log q
+
\frac{\log w}{d}|P_-|
+
\frac{\log q}{d-1}|P_+|
\right].
$$

Pointwise endpoint dominance supplies

$$
\lambda(n)<\lambda(q)
$$

for every interior prime-power carrier, but this remains atomwise. The count
form shows exactly why pointwise dominance does not close the aggregate bound:
the number and kernel positions of the interior carriers still matter.

## What PROOF.md Controls

The current proof machinery contributes these pieces.

**Threshold lemmas.** The threshold comparison proves that earlier integers
cannot beat the selected GWR minimum in the ordered comparison. It does not
count prime powers, estimate their kernel positions, or bound

$$
\sum_{n\in P_\pm}|J_z(x_n)|.
$$

**Divisor-average branch.** In the large-divisor branch, the proof gives

$$
n<w\Rightarrow
0<\log\frac{w}{n}<\frac{\log w}{d-1}
$$

for pre-selector interior points. This controls the location of atoms in
`P_-` relative to `w`. It does not bound the post-selector packet `P_+`, and
it does not bound the aggregate kernel-weighted mass of `P_-`.

**Finite base.** The finite base certifies the maximizer theorem below
`5,000,000,001`. It does not record the packet sums

$$
\sum_{n\in P_-}|J_z(x_n)|,
\qquad
\sum_{n\in P_+}|J_z(x_n)|,
$$

so it does not close this completion-cost inequality as presently stated.

Therefore the Aggregate Completion-Cost Bound does not close from the existing
`PROOF.md` machinery alone.

## Exact Remaining Local Estimate

The smallest additional arithmetic estimate is the following.

> **Kernel-Weighted Prime-Power Packet Estimate.**
> For every consecutive-prime chamber `p < q` and every `z > 0`,
> $$
> \log q\,|J_z(x_q)|
> +
> \frac{\log w}{d}\sum_{n\in P_-}|J_z(x_n)|
> +
> \frac{\log q}{d-1}\sum_{n\in P_+}|J_z(x_n)|
> \le
> \rho_{p,q}(z)R_{p,q}(z).
> $$

In expanded form, the right side is

$$
\rho_{p,q}(z)
\left[
\log q\,K_z(x_q)
+
\sum_{n\in P(p,q),\,n<q}\lambda(n)K_z(x_n)
\right].
$$

This is a prime-power spacing and mass estimate inside the chamber. It says
that the endpoint plus interior prime-power folded reserve is large enough,
at the actual kernel locations of the prime powers, to pay for the odd-drift
transport cost.

Once the completion assignment fixes a lower bound for `rho_{p,q}(z)`, this is
a purely local arithmetic estimate about the kernel-weighted placement and
mass of prime powers inside the chamber.

With this estimate,

$$
C^-_{p,q}(z)\le R_{p,q}(z),
$$

and the Folded Packet Drift Inequality follows.

## Proof-State Result

The local arithmetic bridge has been reduced one step further.

The current machinery proves the coefficient side:

```text
pointwise endpoint dominance
+ selector-to-packet envelope
+ restricted pre-selector position bound.
```

Those imply the explicit aggregate cost bound above. They do not bound the
kernel-weighted prime-power sums. The remaining local theorem is exactly the
Kernel-Weighted Prime-Power Packet Estimate.

The packet drift average bound needed for that estimate is recorded in
[Packet Drift Weighted Average Lemma](packet_drift_weighted_average_lemma.md).

The combined reduction with the completion transport radius is recorded in
[Combined Reduction With Weighted Average Lemma](combined_reduction_with_weighted_average_lemma.md).
