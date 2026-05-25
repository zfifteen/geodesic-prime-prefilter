# Transport Capacity Balance And Exact Assembly Strategy

Date: 2026-05-24

Status: constructive strategy for the remaining transport-capacity balance
and exact completion assembly.

Packetwise localization is now separated from capacity. The remaining task is
to match packet odd drifts with safe completion transport capacity while
preserving the standard completion correction

$$
C_{\mathrm{comp}}(s)
=
-{1\over s}-{1\over s-1}
 +{1\over2}\log\pi
-{1\over2}{\Gamma'\over\Gamma}(s/2).
$$

## Packet Demand

For each packet, define

$$
D_{p,q}(z)
=
\sum_{n\in P(p,q)}\Lambda(n)
J_z\left(\log {n\over\sqrt{pq}}\right).
$$

Let

$$
D_+(z)=\sum_{D_{p,q}>0}D_{p,q}(z),
\qquad
D_-(z)=\sum_{D_{p,q}<0}|D_{p,q}(z)|.
$$

Direct BDH supplies the controlled-summation input needed to interpret these
sums in the same finite-part normalization as the completed quotient.

## Net Finite-Part Balance

The exact deconvolved quotient and completion give a global odd-balance
identity in the folded coordinate:

$$
\operatorname{F.p.}\sum_{(p,q)}D_{p,q}(z)
+
B_{\mathrm{comp}}^{\mathrm{fp}}(z)
=0.
$$

Equivalently,

$$
D_+(z)-D_-(z)
=
-B_{\mathrm{comp}}^{\mathrm{fp}}(z).
$$

This is the packet-side finite-part identity already isolated in the net
finite-part packet sum requirement. It is the analytic normalization that
turns global net cancellation into a theorem rather than an ordinary partial
sum claim.

## Raw Safe Reservoir

Let the safe completion transport reservoir consist of:

```text
pole atoms at +/-1/2
+ trivial-zero atoms at -2m-1/2
```

with zero-radius constants excluded from negative folded cost.

Let the finite-part raw side capacities be

$$
T^{0}_+(z),
\qquad
T^{0}_-(z),
$$

after the chosen finite-part regularization of the trivial-zero side. Exact
assembly fixes the difference

$$
T^{0}_-(z)-T^{0}_+(z)=B_{\mathrm{comp}}^{\mathrm{fp}}(z).
$$

Combining with the packet finite-part identity gives equal side deficits:

$$
\Delta_+(z)=D_-(z)-T^{0}_+(z),
$$

$$
\Delta_-(z)=D_+(z)-T^{0}_-(z),
$$

and

$$
\Delta_+(z)=\Delta_-(z)=:\Delta(z).
$$

## Symmetric Trivial-Zero Split

If

$$
\Delta(z)\ge0,
$$

then a symmetric split of a safe trivial-zero atom supplies the missing
capacity without changing the completion correction. For example, at

$$
y_0=-{1\over2},
$$

use

$$
\delta_{y_0}
=
(1+\alpha_0(z))\delta_{y_0}
-\alpha_0(z)\delta_{y_0},
$$

where

$$
\alpha_0(z)
=
{\Delta(z)\over |J_z(y_0)|}.
$$

This adds `Delta(z)` to each side capacity:

$$
T_+^{\mathrm{new}}=T_+^0+\Delta=D_-,
$$

$$
T_-^{\mathrm{new}}=T_-^0+\Delta=D_+.
$$

Exact assembly is preserved atom by atom because

$$
(1+\alpha_0)\delta_{y_0}-\alpha_0\delta_{y_0}
=
\delta_{y_0}.
$$

Localization is preserved because

$$
|y_0|={1\over2}>M_{p,q}.
$$

The folded negative cost introduced by the split is finite:

$$
\alpha_0(z)K_z(y_0)<\infty.
$$

## Packet Allocation

After the side capacities match, allocate opposite-sign transport capacity
proportionally:

$$
\theta_{p,q,j}^{+}
=
{|D_{p,q}(z)|\over D_-(z)}
$$

for packets with negative drift using positive transport capacity, and

$$
\theta_{p,q,j}^{-}
=
{D_{p,q}(z)\over D_+(z)}
$$

for packets with positive drift using negative transport capacity.

This cancels packet drift exactly and preserves exact assembly because the
allocation weights exhaust the chosen transport reservoir.

## Remaining Checks

The constructive capacity proof now has two exact checks:

1. **Finite-part packet identity.**
   $$
   \operatorname{F.p.}\sum_{(p,q)}D_{p,q}(z)
   =
   -B_{\mathrm{comp}}^{\mathrm{fp}}(z).
   $$

2. **Nonnegative common deficit.**
   $$
   \Delta(z)=D_-(z)-T_+^0(z)=D_+(z)-T_-^0(z)\ge0.
   $$

If both hold, the symmetric trivial-zero split gives sidewise transport
capacity balance, exact assembly, localization, and controlled summation.

## Fallback

If the literal support-removal regime for Direct BDH is not admissible, the
same capacity construction can be used only after the Unified Packet-Frame
Source theorem supplies the three residual bounds needed for controlled
summation.

## Result

Transport capacity balance has been reduced to a finite-part identity plus a
side-deficit sign check. Under those two inputs, a deterministic symmetric
trivial-zero split supplies the missing sidewise capacity while preserving
the standard completion correction exactly.
