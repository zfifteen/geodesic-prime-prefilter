# Exact Completion Assembly Strategy

Date: 2026-05-24

Status: proof-strategy note for the Exact Completion Assembly Theorem.

The Exact Completion Assembly Theorem requires a packetwise decomposition of
the standard completion correction

$$
C_{\mathrm{comp}}(s)
=
-\frac1s
-\frac1{s-1}
+\frac12\log\pi
-\frac12\frac{\Gamma'}{\Gamma}(s/2)
$$

that satisfies exact assembly, no negative zero-radius leakage, packetwise
localization, and controlled summation.

## Candidate Construction

The candidate construction separates the completion correction into two
reservoirs.

1. **Zero-radius reservoir.**
   The gamma regularization constants and the scale/main constant are assigned
   to the global nonnegative folded background or to packetwise nonnegative
   parts. They are not assigned to any packetwise negative folded-cost
   measure.

2. **Transport reservoir.**
   The pole pair and the trivial-zero transport atoms have centered radius at
   least `1/2`. Since every chamber packet satisfies
   $$
   M_{p,q}<\frac12,
   $$
   any negative folded-cost mass drawn from this reservoir is automatically
   localized outside the packet excursion.

For each transport atom `y_j` in the completion correction, choose packet
allocation weights

$$
\theta_{p,q,j}(z)\ge0,
\qquad
\sum_{(p,q)}\theta_{p,q,j}(z)=1.
$$

The packet correction receives the share

$$
\theta_{p,q,j}(z)\,\eta_j.
$$

This preserves exact assembly atom by atom. It also preserves localization,
because every transport atom in this reservoir has

$$
|y_j|\ge\frac12>M_{p,q}.
$$

## Drift Matching Requirement

The allocation weights must be chosen so that each packet correction cancels
the packet odd drift:

$$
\int J_z(x)\,d\eta_{p,q,z}(x)=-D_{p,q}(z).
$$

At the same time, the negative folded cost assigned to the packet must remain
bounded by the packet reserve:

$$
C^-_{p,q}(z)\le R_{p,q}(z).
$$

The weighted-average lemma and localization reduce this to the transport
radius condition already isolated:

$$
\rho_{p,q}(z)\ge M_{p,q}.
$$

## Main Analytic Difficulties

1. **Exact signed reservoir identification.**
   The proof must identify the negative folded-cost part of the pole and
   gamma/trivial-zero reservoirs without changing the completed logarithmic
   derivative.

2. **Drift-matching allocation.**
   The packet weights `theta_{p,q,j}(z)` must simultaneously preserve the
   original completion atoms and cancel each packet's odd drift.

3. **Zero-radius nonnegativity.**
   The regularization/main constants must be assigned without creating
   packetwise negative folded cost at `x = 0`.

4. **Infinite summation.**
   The gamma/trivial-zero reservoir is infinite. The allocation must converge
   in the folded kernel and permit summation over all chamber packets.

5. **Analytic compatibility in `z`.**
   The packet allocations may depend on `z` at the folded-kernel level, but
   they must still assemble to the same completed quotient correction on the
   common analytic domain.

## Strategy Result

The proof of the Exact Completion Assembly Theorem is reduced to constructing
a nonnegative allocation of the pole and trivial-zero transport reservoir that
matches packet odd drift while preserving exact assembly. The zero-radius
terms are not part of the negative transport budget.

The candidate allocation rule is recorded in
[Transport Reservoir Allocation Rule](transport_reservoir_allocation_rule.md).
