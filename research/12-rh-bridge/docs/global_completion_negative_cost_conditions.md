# Global Completion Negative-Cost Conditions

Date: 2026-05-24

Status: global completion-side consistency note for the Chamber-Deconvolved
Reciprocal Balance Lemma.

The per-chamber reduction now has the following local chain:

```text
Packet Drift Weighted Average Lemma
-> rho_{p,q}(z) >= M_{p,q}
-> Completion Localization Lemma
-> Folded Packet Drift Inequality for the chamber.
```

The zero-radius completion constants are assigned outside the packetwise
negative folded-cost measure. The remaining question is global consistency:
the packetwise completion corrections must assemble into the completed
quotient without creating unassigned negative folded cost.

## Packetwise Measures

For each chamber packet `P(p,q)`, let `eta_{p,q,z}` be the packetwise
completion correction and write

$$
\eta_{p,q,z}=\eta^+_{p,q,z}-\eta^-_{p,q,z}.
$$

The local support condition is

$$
\operatorname{supp}(\eta^-_{p,q,z})
\subseteq
\{x:|x|\ge M_{p,q}\}.
$$

The zero-radius constants are assigned to a global nonnegative folded
background or to packetwise nonnegative parts, never to `eta^-_{p,q,z}`.

## Global Assembly Conditions

The completion side must satisfy four global conditions.

1. **Exact assembly.**
   The completed correction equals the packetwise sum plus the zero-radius
   nonnegative background:
   $$
   \eta_{\mathrm{comp},z}
   =
   \eta_{0,z}^+
   +
   \sum_{(p,q)}\eta_{p,q,z}.
   $$

2. **No negative zero-radius leakage.**
   The background has no negative folded-cost part:
   $$
   \eta_{0,z}^-\equiv0.
   $$

3. **Packetwise localization.**
   Every packet negative part satisfies
   $$
   \operatorname{supp}(\eta^-_{p,q,z})
   \subseteq
   \{x:|x|\ge M_{p,q}\}.
   $$

4. **Controlled summation.**
   The packetwise negative costs are summable in the folded kernel:
   $$
   \sum_{(p,q)}
   \int K_z(x)\,d\eta^-_{p,q,z}(x)
   <\infty
   $$
   on the common domain where the completed folded kernel is evaluated.

## Consequence

Under these four conditions, no global negative folded cost remains outside
the localized packet accounting. Each chamber satisfies

$$
C^-_{p,q}(z)
\le
R_{p,q}(z),
$$

and the global negative folded cost is bounded by the sum of the packet
reserves:

$$
\sum_{(p,q)}C^-_{p,q}(z)
\le
\sum_{(p,q)}R_{p,q}(z).
$$

Thus the completed folded residual is globally compatible with the
nonnegative packetwise Stieltjes representation.

## Remaining Completion-Side Requirement

The remaining completion-side proof obligation is an exact assembly theorem:

> The pole, gamma, main, and trivial-zero completion corrections admit a
> packetwise decomposition satisfying exact assembly, no negative zero-radius
> leakage, packetwise localization, and controlled summation.

This is the global closure condition left after the PGS-side packet arithmetic
and local completion transport reductions.

The formal theorem statement for this assembly is recorded in
[Exact Completion Assembly Theorem](exact_completion_assembly_theorem.md).
