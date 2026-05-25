# Transport Capacity Balance Identity

Date: 2026-05-24

Status: completion-side target identity for the Transport Reservoir Allocation
Rule.

The proportional opposite-sign allocation rule cancels packet drift exactly if
the signed packet drift demands match the signed capacities of the completion
transport reservoir.

## Packet Drift Demands

For each chamber packet, define

$$
D_{p,q}(z)=\sum_{n\in P(p,q)}\lambda(n)J_z(x_n).
$$

Split packets by drift sign:

$$
\mathcal P_+(z)=\{(p,q):D_{p,q}(z)>0\},
\qquad
\mathcal P_-(z)=\{(p,q):D_{p,q}(z)<0\}.
$$

Define total signed demands:

$$
D_+(z)=\sum_{(p,q)\in\mathcal P_+(z)}D_{p,q}(z),
$$

and

$$
D_-(z)=\sum_{(p,q)\in\mathcal P_-(z)}|D_{p,q}(z)|.
$$

## Transport Reservoir Capacities

Let the pole-pair and trivial-zero transport reservoir consist of atoms
`(y_j,a_j(z))`, where `|y_j| >= 1/2`. Define their odd capacities by

$$
O_j(z)=a_j(z)J_z(y_j).
$$

Split by capacity sign:

$$
\mathcal T_+(z)=\{j:O_j(z)>0\},
\qquad
\mathcal T_-(z)=\{j:O_j(z)<0\}.
$$

Define total capacities:

$$
T_+(z)=\sum_{j\in\mathcal T_+(z)}O_j(z),
$$

and

$$
T_-(z)=\sum_{j\in\mathcal T_-(z)}|O_j(z)|.
$$

## Identity Statement

> **Transport Capacity Balance Identity.**
> For every `z > 0` in the common folded-kernel domain,
> $$
> T_-(z)=D_+(z),
> \qquad
> T_+(z)=D_-(z).
> $$

This identity is the exact condition required by the proportional allocation
rule. It says that the negative odd capacity of the completion transport
reservoir exactly pays for all positive packet drift, and the positive odd
capacity exactly pays for all negative packet drift.

## Required Analytic Conditions

To prove the identity, the completion side must supply four facts.

1. **Exact global odd balance.**
   The packet drift and transport reservoir assemble to zero odd drift in the
   completed coordinate:
   $$
   \sum_{(p,q)}D_{p,q}(z)+\sum_jO_j(z)=0.
   $$

2. **Sidewise balance.**
   Net cancellation is not enough. The positive and negative sides must match
   separately:
   $$
   T_-(z)=D_+(z),
   \qquad
   T_+(z)=D_-(z).
   $$

3. **Zero-radius neutrality.**
   The zero-radius gamma regularization and main constants contribute no odd
   capacity:
   $$
   J_z(0)=0.
   $$

4. **Convergent exchange of sums.**
   The packet and transport sums converge strongly enough to permit the sign
   splits and the packetwise allocation.

## Proof-State Result

The remaining obstruction is no longer prime-power packet arithmetic. It is
the sidewise completion identity above. Once it is proved, the proportional
opposite-sign allocation rule gives exact packet drift cancellation while
preserving exact assembly, localization, and controlled summation.

The pole-pair and trivial-zero parts of this identity are separated in
[Pole And Trivial-Zero Capacity Decomposition](pole_trivial_capacity_decomposition.md).
