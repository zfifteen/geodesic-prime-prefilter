# Four Interface Inputs Status Ledger

Date: 2026-05-24

Status: status ledger for the four interface inputs left by the
Chamber-Deconvolved Balance reduction assembly.

The reduction assembly isolated four interface inputs:

1. direct-route admissibility or Unified Packet-Frame Source fallback;
2. finite-part packet identity;
3. nonnegative common side deficit;
4. exact assembly compatibility.

This note maps each input to the existing notes and records what remains.

## 1. Direct-Route Admissibility Or Packet-Frame Fallback

**Location.**

- `direct_full_radius_bdh_closure_certificate.md`
- `polylog_completion_parameter_assignment.md`
- `type_ii_band_budget_poisson_comparison.md`
- `direct_route_literal_support_closure_plan.md`

**Status.**

Closed conditionally in the explicit polylogarithmic literal regime:

$$
Q_0=(\log X)^{1/4},
\qquad
N=X^{1/4}(\log X)^{1+C_N}.
$$

The four scalar gates are paid inside the Poisson allowance if the bridge
permits this kernel length.

**Remaining input.**

Verify kernel-length admissibility for the RH bridge application. If the
bridge fixes a shorter `N`, prove the Unified Packet-Frame Source theorem:

$$
\|(1-P_{\mathrm{maj}})w_{N,L}\|_2^2
\le
\Delta_L\|w_{N,L}\|_2^2,
$$

$$
\|(1-P_{\mathrm{maj}})\Omega_N\|_1
\le
{\mathcal E_{\mathrm{shift}}\over\mathcal S\mathcal A_{\min}},
$$

and

$$
\left(
X\mathfrak C_{\mu^\perp}(1/X)+\mu^\perp([0,1])
\right)\mathcal A_2
\le
(\log X)^2\mathcal E_{\mathrm{maj}}.
$$

**Side.** Analytic completion / kernel-parameter side.

## 2. Finite-Part Packet Identity

**Location.**

- `net_finite_part_packet_sum_requirement.md`
- `transport_capacity_balance_assembly_strategy.md`
- `chamber_deconvolved_balance_reduction_assembly.md`

**Required identity.**

$$
\operatorname{F.p.}\sum_{(p,q)}D_{p,q}(z)
=
-B_{\mathrm{comp}}^{\mathrm{fp}}(z).
$$

Equivalently, in the earlier trivial-zero notation,

$$
\operatorname{F.p.}
\sum_{n=r^a}
\Lambda(n)
J_z\left(\log{n\over\sqrt{p(n)q(n)}}\right)
=
-{1\over2}
\left(
\operatorname{Re}\psi\left({1\over4}+{i\sqrt z\over2}\right)
+\gamma
\right).
$$

**Status.**

Open. Ordinary partial sums do not converge to this value; the target is a
completion-compatible finite part, not a finite accumulation law.

Direct BDH supplies controlled summation for the analytic residual, but it
does not by itself prove the packet finite-part identity.

**Remaining input.**

Prove that the chamber packet decomposition of `lambda=Lambda`, regularized
by the same completion finite part, has global first moment equal to the
centered gamma/trivial-zero finite part.

**Side.** Mixed PGS completion side: packet arithmetic plus analytic
finite-part regularization.

## 3. Nonnegative Common Side Deficit

**Location.**

- `transport_capacity_balance_assembly_strategy.md`
- `symmetric_trivial_zero_capacity_requirements.md`
- `one_sided_regularization_lower_production_failure.md`

**Required sign check.**

Let

$$
\Delta(z)=D_-(z)-T_+^0(z)=D_+(z)-T_-^0(z).
$$

The symmetric split construction requires

$$
\Delta(z)\ge0.
$$

**Status.**

Open. The net finite-part identity makes the two deficits equal, but it does
not prove that the common deficit is nonnegative. Earlier one-sided
regularization failed because local GWR envelopes do not produce the needed
sidewise lower-production identity.

**Remaining input.**

Either:

1. prove the raw finite-part transport reservoir is minimal sidewise, so the
   packet demand exceeds the raw side capacities; or
2. choose a canonical finite-part normalization of `T_+^0,T_-^0` for which
   the common deficit is nonnegative; or
3. replace the literal capacity split by a stronger canonical symmetric
   trivial-zero transport theorem.

**Side.** Completion-capacity side, with a global packet-demand input.

## 4. Exact Assembly Compatibility

**Location.**

- `exact_completion_assembly_theorem.md`
- `exact_completion_assembly_strategy.md`
- `transport_capacity_balance_assembly_strategy.md`
- `packetwise_completion_localization_strategy.md`

**Required compatibility.**

The packet allocations and symmetric split must assemble to exactly

$$
-{1\over s}-{1\over s-1}
 +{1\over2}\log\pi
-{1\over2}{\Gamma'\over\Gamma}(s/2)
$$

on the common domain.

**Status.**

Partially reduced. The symmetric split preserves exact assembly atom by atom,
and zero-radius constants are excluded from negative folded cost. The
remaining compatibility issue is global: the `z`-dependent packet allocation
must define the same completed correction after summing over packets and
transport atoms.

**Remaining input.**

Prove convergence and analytic compatibility of the packet allocation:

$$
\eta_{\mathrm{comp},z}
=
\eta_{0,z}^+
+
\sum_{(p,q)}\eta_{p,q,z},
$$

with no negative zero-radius leakage and with the standard completion
correction recovered on the common analytic domain.

**Side.** Analytic completion assembly side.

## Current Center

The direct BDH route and packetwise localization are no longer the main
obstructions in the explicit polylog literal regime. The live center is now:

```text
finite-part packet identity
+ nonnegative common side deficit
+ exact assembly compatibility
```

If kernel-length admissibility fails, the Unified Packet-Frame Source theorem
returns as the analytic prerequisite before these completion-capacity inputs
can be used.

## Result

The four interface inputs are now mapped. The next highest-leverage target is
the finite-part packet identity, because it is required before the common
side deficit is even well-defined as a single `Delta(z)`.
