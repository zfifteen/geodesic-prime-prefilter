# Exact Completion Assembly Theorem

Date: 2026-05-24

Status: completion-side theorem statement for the Chamber-Deconvolved
Reciprocal Balance Lemma.

The completed logarithmic derivative decomposes as

$$
Q(s)=R(s)+C_{\mathrm{comp}}(s),
$$

where

$$
C_{\mathrm{comp}}(s)
=
-\frac1s
-\frac1{s-1}
+\frac12\log\pi
-\frac12\frac{\Gamma'}{\Gamma}(s/2).
$$

The exact assembly theorem states the completion-side property still needed
after the packet arithmetic reductions.

## Theorem Statement

> **Exact Completion Assembly Theorem.**
> The standard completion correction `C_comp(s)` admits a packetwise
> decomposition
> $$
> \eta_{\mathrm{comp},z}
> =
> \eta^+_{0,z}
> +
> \sum_{(p,q)}\eta_{p,q,z}
> $$
> in the centered folded coordinate such that the following four conditions
> hold.

1. **Explicit-formula compatibility.**
   The transform of the assembled correction is exactly
   $$
   C_{\mathrm{comp}}(s)
   =
   -\frac1s
   -\frac1{s-1}
   +\frac12\log\pi
   -\frac12\frac{\Gamma'}{\Gamma}(s/2),
   $$
   on the common domain of the completed quotient.

2. **No negative zero-radius leakage.**
   The zero-radius completion constants are assigned to
   `eta^+_{0,z}` or to packetwise nonnegative folded parts:
   $$
   \eta^-_{0,z}\equiv0.
   $$

3. **Packetwise localization.**
   For each chamber packet `P(p,q)`, with
   $$
   M_{p,q}=\max_{n\in P(p,q)}|x_n|,
   $$
   the negative part of the packet correction satisfies
   $$
   \operatorname{supp}(\eta^-_{p,q,z})
   \subseteq
   \{x:|x|\ge M_{p,q}\}.
   $$

4. **Controlled summation.**
   The packetwise negative folded costs are summable:
   $$
   \sum_{(p,q)}
   \int K_z(x)\,d\eta^-_{p,q,z}(x)
   <\infty
   $$
   on the common folded-kernel domain.

## Consequence

If the Exact Completion Assembly Theorem holds, then every packet has
completion transport radius

$$
\rho_{p,q}(z)\ge M_{p,q}.
$$

The Packet Drift Weighted Average Lemma gives

$$
|D_{p,q}(z)|\le M_{p,q}R_{p,q}(z),
$$

so

$$
|D_{p,q}(z)|\le \rho_{p,q}(z)R_{p,q}(z).
$$

Thus the Aggregate Completion-Cost Bound holds packetwise, the Folded Packet
Drift Inequality holds packetwise, and the assembled completed residual is
compatible with a nonnegative reciprocal-balanced folded measure.

## Remaining Proof Obligation

The theorem statement is completion-side. Its proof must construct the
packetwise measures from the pole pair, gamma factor, main term, and
trivial-zero correction while preserving exact-formula compatibility. The
construction must not introduce hidden negative folded cost at zero radius or
inside any packet excursion.

The candidate proof route is recorded in
[Exact Completion Assembly Strategy](exact_completion_assembly_strategy.md).
