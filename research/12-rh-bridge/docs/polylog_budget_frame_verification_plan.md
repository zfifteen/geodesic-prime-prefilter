# Polylog Budget and Frame Verification Plan

Date: 2026-05-24

Status: concrete verification plan for the polylogarithmic `Q0` branch of
the Direct Full-Radius BDH Assembly, with the packet-frame fallback stated as
a single lower-bound theorem.

The polylogarithmic branch reduces the direct route to scalar inequalities.
Set

$$
Q_0=(\log X)^B
$$

with fixed `B`. In this regime rational packet separation, frame conditioning,
and Siegel-Walfisz amplitude reproduction are available before the direct
large-sieve step. The remaining question is whether the completion and budget
quantities force

$$
R_{\mathrm{all}}
\le
\min(\rho_{\mathrm{valid}}^0,c_1Q_0^{-2}).
$$

## Fixed Inputs

Use the noncircular assignment order from the budget strategy:

1. choose `Q0=(log X)^B`;
2. take an external major-radius input `rho_valid^0`;
3. assign budgets `E_maj` and `E_shift`;
4. bound `A_2`, `A_min`, `L_crit`, `M_Omega`, and `R_LS`;
5. verify the final radius inequality.

In the polylogarithmic branch,

$$
B_{\mathrm{ov}}=O(1)
$$

provided

$$
R_{\mathrm{all}}\le c_1Q_0^{-2}.
$$

Thus bounded overlap is a consequence of the same separation inequality that
the route must verify.

## Frame Verification

The low-conductor packet frame has diagonal size `asymp X` and row
off-diagonal size `O(Q0^4)` under the crude rational-spacing bound. Hence the
normalized Gram error satisfies

$$
\|X^{-1}G-I\|_{\mathrm{row}}
\ll
{Q_0^4\over X}.
$$

For `Q0=(log X)^B`,

$$
{Q_0^4\over X}\to0.
$$

Therefore the packet vectors form a bounded Riesz sequence, the projection
`P_maj` is stable, and

$$
\mathcal A_2
=
\|(1-P_{\mathrm{maj}})a\|_2^2
\le
C_A\|a\|_2^2
$$

with `C_A` independent of `X` for large `X`.

## Amplitude Verification

For `q <= Q0`, Siegel-Walfisz gives, for every fixed `A`,

$$
E_q(X)
\ll_A
{X\over(\log X)^A}.
$$

After endpoint normalization and partial summation, the coefficient error at
`a/q` has normalized size

$$
\epsilon_q(X)
\ll_A
(\log X)^{-A}.
$$

The major packet amplitude condition is therefore reduced to

$$
\sum_{q\le Q_0}\sum_{(a,q)=1}
\epsilon_q(X)^2 I_N(a/q,R_{\mathrm{all}})
\le
\mathcal E_{\mathrm{amp}}.
$$

Since

$$
\sum_{q\le Q_0}\varphi(q)\ll Q_0^2,
\qquad
I_N(a/q,R_{\mathrm{all}})\le I_N(a/q,1)\ll N,
$$

the total amplitude error is

$$
\ll_A
N Q_0^2(\log X)^{-2A}.
$$

For fixed `B`, choosing `A` larger than the assigned logarithmic loss makes
this smaller than any budget of the form

$$
\mathcal E_{\mathrm{amp}}
\ge
N(\log X)^{-C}.
$$

Thus frame and amplitude closure are unconditional in the polylogarithmic
low-conductor regime once the budgets are not smaller than a fixed negative
power of `log X`.

## Radius Budget Verification

The unified radius is

$$
R_{\mathrm{all}}
=
\max(c_0/L_{\mathrm{crit}},M_{\Omega}^{-1},R_{\mathrm{LS}}).
$$

The literal support route closes if each component is at most
`c1 Q0^{-2}` and at most `rho_valid^0`.

### Completion Band Term

The band term requires

$$
{c_0\over L_{\mathrm{crit}}}
\le
c_1Q_0^{-2},
$$

equivalently

$$
L_{\mathrm{crit}}
\ge
{c_0\over c_1}Q_0^2.
$$

It also requires

$$
L_{\mathrm{crit}}
\ge
{c_0\over \rho_{\mathrm{valid}}^0}.
$$

### Kernel-Mass Term

Since

$$
M_{\Omega}
=
{\mathcal E_{\mathrm{shift}}
\over
\mathcal S(Q_0,H,\rho_{\max})\mathcal A_{\min}},
$$

the condition

$$
M_{\Omega}^{-1}\le c_1Q_0^{-2}
$$

is exactly

$$
\mathcal E_{\mathrm{shift}}
\ge
{1\over c_1}
\mathcal S(Q_0,H,\rho_{\max})
\mathcal A_{\min}
Q_0^2.
$$

The major-radius condition similarly requires

$$
\mathcal E_{\mathrm{shift}}
\ge
{\mathcal S(Q_0,H,\rho_{\max})\mathcal A_{\min}
\over
\rho_{\mathrm{valid}}^0}.
$$

### Direct Large-Sieve Term

The direct large-sieve radius is

$$
R_{\mathrm{LS}}
=
\max\left(
\left(
{B_{\mathrm{ov}}\mathcal A_2
\over
(\log X)^2\mathcal E_{\mathrm{maj}}}
\right)^{1/2},
{B_{\mathrm{ov}}\mathcal A_2
\over
(\log X)^2\mathcal E_{\mathrm{maj}}}
\right).
$$

The separation condition is therefore implied by

$$
\mathcal E_{\mathrm{maj}}
\ge
{B_{\mathrm{ov}}\mathcal A_2Q_0^4
\over
c_1^2(\log X)^2},
$$

and the full major-radius condition is implied by

$$
\mathcal E_{\mathrm{maj}}
\ge
{B_{\mathrm{ov}}\mathcal A_2
\over
(\log X)^2(\rho_{\mathrm{valid}}^0)^2}.
$$

The quadratic condition dominates the linear one once the right side is
larger than the corresponding first-power demand.

## Polylog Literal Closure Test

The polylogarithmic literal route closes if the following four inequalities
hold:

$$
\rho_{\mathrm{valid}}^0\ge c_1Q_0^{-2},
$$

$$
L_{\mathrm{crit}}
\ge
\max\left({c_0\over c_1}Q_0^2,{c_0\over\rho_{\mathrm{valid}}^0}\right),
$$

$$
\mathcal E_{\mathrm{shift}}
\ge
\max\left(
{1\over c_1}
\mathcal S\mathcal A_{\min}Q_0^2,
{\mathcal S\mathcal A_{\min}\over\rho_{\mathrm{valid}}^0}
\right),
$$

and

$$
\mathcal E_{\mathrm{maj}}
\ge
\max\left(
{B_{\mathrm{ov}}\mathcal A_2Q_0^4
\over
c_1^2(\log X)^2},
{B_{\mathrm{ov}}\mathcal A_2
\over
(\log X)^2(\rho_{\mathrm{valid}}^0)^2}
\right).
$$

These are the exact checks required to finish the polylog branch. Existing
notes already provide the frame and amplitude parts in this regime. The
remaining live quantities are completion-side: `L_crit`, `S A_min`, `A_2`,
and the available split between `E_shift` and `E_maj`.

## Unified Packet-Frame Fallback

If any literal support inequality fails, the route must replace support
containment by a packet-frame lower bound. The needed theorem is:

> **Unified Packet-Frame Lower Bound.**  
> For the low-conductor packet frame at scale `Q0`, the orthogonal projector
> `P_maj` satisfies, simultaneously for every relevant dyadic band and kernel
> window,
> \[
> \|(1-P_{\mathrm{maj}})w_{N,L}\|_2^2
> \le
> \Delta_L\|w_{N,L}\|_2^2,
> \]
> \[
> \|(1-P_{\mathrm{maj}})\Omega_N\|_1
> \le
> M_{\Omega},
> \]
> and
> \[
> \left(
> X\mathfrak C_{\mu^\perp}(1/X)+\mu^\perp([0,1])
> \right)\mathcal A_2
> \le
> (\log X)^2\mathcal E_{\mathrm{maj}},
> \]
> where `mu^perp` is the weighted frequency measure after packet projection.

This theorem replaces the geometric condition

$$
R_{\mathrm{all}}\le c_1Q_0^{-2}
$$

by direct residual capture. It is strictly stronger than frame conditioning:
the ordinary Riesz bound stabilizes coefficients, while this lower bound says
that the specific band energy, kernel mass, and weighted measure
concentration all lie in the low-conductor packet span up to the assigned
budgets.

## Result

For `Q0=(log X)^B`, the frame and amplitude gaps close by diagonal dominance
and Siegel-Walfisz. The literal direct route now depends only on the four
scalar budget/radius inequalities above. If those inequalities fail, the
single replacement theorem is the Unified Packet-Frame Lower Bound, which
must prove residual band-energy, kernel-mass, and measure-concentration
control without disjoint support apertures.
