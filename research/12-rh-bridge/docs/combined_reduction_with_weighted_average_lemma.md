# Combined Reduction With Weighted Average Lemma

Date: 2026-05-24

Status: integration note for the Chamber-Deconvolved Reciprocal Balance
Lemma.

Let `p < q` be consecutive primes and let

$$
P(p,q)=\{q\}\cup\{n\in(p,q):n=r^a,\ r\text{ prime},\ a\ge2\}.
$$

Use the centered coordinate

$$
x_n=\log\frac{n}{\sqrt{pq}},
$$

and define

$$
M_{p,q}=\max_{n\in P(p,q)}|x_n|.
$$

For `z > 0`, let

$$
J_z(x)=\frac{x}{z+x^2},
\qquad
K_z(x)=\frac{1}{z+x^2},
$$

and

$$
D_{p,q}(z)=\sum_{n\in P(p,q)}\lambda(n)J_z(x_n),
\qquad
R_{p,q}(z)=\sum_{n\in P(p,q)}\lambda(n)K_z(x_n).
$$

## Combined Inequality

The Packet Drift Weighted Average Lemma gives

$$
|D_{p,q}(z)|\le M_{p,q}R_{p,q}(z).
$$

The Aggregate Completion-Cost Bound closes the local folded packet inequality
whenever

$$
|D_{p,q}(z)|\le \rho_{p,q}(z)R_{p,q}(z).
$$

Therefore the local arithmetic and completion reductions combine to:

$$
\rho_{p,q}(z)\ge M_{p,q}
\quad\Longrightarrow\quad
|D_{p,q}(z)|\le \rho_{p,q}(z)R_{p,q}(z).
$$

Equivalently, a sharpened arithmetic estimate

$$
|D_{p,q}(z)|\le \theta_{p,q}(z)M_{p,q}R_{p,q}(z),
\qquad
0<\theta_{p,q}(z)\le1,
$$

would require only

$$
\rho_{p,q}(z)\ge \theta_{p,q}(z)M_{p,q}.
$$

## Reduced Target

For a fixed chamber packet, the Chamber-Deconvolved Reciprocal Balance route
now reduces to the completion-side condition

$$
\rho_{p,q}(z)\ge\max_{n\in P(p,q)}|x_n|.
$$

This condition is entirely about the completion transport assignment. The
PGS-side packet arithmetic has supplied:

```text
nonnegative prime-power packet weights
+ centered packet coordinates
+ weighted-average drift bound.
```

## Remaining Analytic Task

The remaining task is to prove that the completion correction assigned to the
same packet has transport radius at least

$$
M_{p,q}=\max_{n\in P(p,q)}|x_n|
$$

while canceling the packet's odd drift. In the notation of the Aggregate
Completion-Cost Bound, this is the estimate

$$
C^-_{p,q}(z)
\le
\frac{|D_{p,q}(z)|}{\rho_{p,q}(z)}
\le
R_{p,q}(z).
$$

Once this completion transport radius estimate is proved, the Folded Packet
Drift Inequality holds for the chamber packet.

The candidate lower bound for the completion transport radius is recorded in
[Completion Transport Radius Lower Bound](completion_transport_radius_lower_bound.md).
