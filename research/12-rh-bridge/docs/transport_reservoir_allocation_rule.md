# Transport Reservoir Allocation Rule

Date: 2026-05-24

Status: candidate allocation rule for the Exact Completion Assembly Theorem.

The transport reservoir consists of the completion atoms whose centered
transport radii are at least `1/2`: the pole pair and the trivial-zero
transport atoms. The zero-radius constants are not part of the negative
transport budget.

For each chamber packet, let

$$
D_{p,q}(z)=\sum_{n\in P(p,q)}\lambda(n)J_z(x_n)
$$

be its odd drift. The packet correction must contribute `-D_{p,q}(z)`.

## Reservoir Split

Split packet drift by sign:

$$
\mathcal P_+(z)=\{(p,q):D_{p,q}(z)>0\},
\qquad
\mathcal P_-(z)=\{(p,q):D_{p,q}(z)<0\}.
$$

Define total drift demand:

$$
D_+(z)=\sum_{(p,q)\in\mathcal P_+(z)}D_{p,q}(z),
$$

and

$$
D_-(z)=\sum_{(p,q)\in\mathcal P_-(z)}|D_{p,q}(z)|.
$$

Split the transport reservoir into atoms with positive and negative odd
capacity. For a transport atom `y_j` with completion mass `a_j(z)`, its odd
capacity is

$$
O_j(z)=a_j(z)J_z(y_j).
$$

Let

$$
\mathcal T_+(z)=\{j:O_j(z)>0\},
\qquad
\mathcal T_-(z)=\{j:O_j(z)<0\}.
$$

The total available capacities are

$$
T_+(z)=\sum_{j\in\mathcal T_+(z)}O_j(z),
\qquad
T_-(z)=\sum_{j\in\mathcal T_-(z)}|O_j(z)|.
$$

## Proportional Opposite-Sign Allocation

Packets with positive drift must receive negative odd correction. Packets with
negative drift must receive positive odd correction.

For $(p,q)\in\mathcal P_+(z)$ and $j\in\mathcal T_-(z)$, set

$$
\theta_{p,q,j}(z)=\frac{D_{p,q}(z)}{D_+(z)}.
$$

For $(p,q)\in\mathcal P_-(z)$ and $j\in\mathcal T_+(z)$, set

$$
\theta_{p,q,j}(z)=\frac{|D_{p,q}(z)|}{D_-(z)}.
$$

All other packet-atom allocation weights are zero.

This rule is deterministic and nonnegative. For each transport atom, the
packet weights on the relevant side sum to `1`, so exact assembly is preserved
atom by atom.

## Drift Cancellation Condition

The rule cancels packet drift exactly if the reservoir capacities match the
packet demands:

$$
T_-(z)=D_+(z),
\qquad
T_+(z)=D_-(z).
$$

Under these two identities, every packet receives exactly the required
opposite-sign odd correction:

$$
\int J_z(x)\,d\eta_{p,q,z}(x)=-D_{p,q}(z).
$$

Localization holds because every allocated transport atom has radius at least
`1/2`, while every packet excursion satisfies

$$
M_{p,q}<\frac12.
$$

Controlled summation follows from the summability of the transport reservoir
in the folded kernel.

## Primary Obstruction

The primary obstruction is the capacity identity:

$$
T_-(z)=D_+(z),
\qquad
T_+(z)=D_-(z).
$$

This is the exact global odd-balance statement needed to turn the proportional
allocation rule into a proof. If the transport reservoir has surplus capacity,
the surplus must be assigned to a nonnegative folded background without
changing the completed quotient. If it has deficient capacity, the candidate
allocation rule cannot cancel packet drift.

Thus the next completion-side target is the **Transport Capacity Balance
Identity** for the pole-pair and trivial-zero reservoir.

The identity is stated in
[Transport Capacity Balance Identity](transport_capacity_balance_identity.md).
