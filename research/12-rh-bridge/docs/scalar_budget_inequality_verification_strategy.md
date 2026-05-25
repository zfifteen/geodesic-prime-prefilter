# Scalar Budget Inequality Verification Strategy

Date: 2026-05-24

Status: verification strategy for the four scalar inequalities in the
polylogarithmic `Q0` branch.

The direct literal branch is now controlled by four scalar conditions:

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
{1\over c_1}\mathcal S\mathcal A_{\min}Q_0^2,
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

For `Q0=(log X)^B`, these are not independent. The first condition makes the
second term in the `E_shift` and `E_maj` bounds comparable to the separation
terms. Thus the polylog literal route reduces to three completion-side lower
bounds plus one major-arc input.

## Major-Radius Input

The required major-radius input is:

> **Polylog Major Validity Input.**  
> For every `q <= Q0` and every reduced `a/q`, the centered endpoint major
> approximation is valid on
> \[
> |\beta|\le c_1Q_0^{-2}
> \]
> with total kernel-weighted error inside the amplitude and major budgets.

For fixed `B`, Siegel-Walfisz gives

$$
\epsilon_q(X)\ll_A(\log X)^{-A}
$$

for the normalized packet coefficient error. Since the number of centers is
`O(Q0^2)` and `I_N(a/q,cQ0^{-2}) <= O(N)`, the total amplitude error is

$$
\ll_A NQ_0^2(\log X)^{-2A}.
$$

Choosing `A` larger than the assigned log loss proves

$$
\rho_{\mathrm{valid}}^0\ge c_1Q_0^{-2}
$$

in the polylogarithmic low-conductor range. This part is a standard
major-arc input, not a new PGS-side arithmetic obligation.

## Completion-Band Input

The base completion-energy estimate gives

$$
E_A(d,N,L)\ll d^{-1}L^3\mathcal B_d.
$$

Let `T_{d,N}` denote the allowed right side in the spectral closure test
after removing the `E_A` factor:

$$
\mathcal T_{d,N}
=
{ \mathcal P_{d,N}^2
\over
(R_{\mathrm{spec}}^2+H_dT_d)
(R_{\mathrm{spec}}^2+K_d)U E_v(d)}
(\log X)^{-C}.
$$

The base energy closes for all bands

$$
L\le
L_{\mathrm{crit}}(d,N)
:=
\left({d\mathcal T_{d,N}\over\mathcal B_d}\right)^{1/3}.
$$

Thus the literal route needs

$$
\mathcal T_{d,N}
\ge
C_L d^{-1}\mathcal B_d Q_0^6.
$$

This is the exact completion-side lower bound behind
`L_crit >= C Q0^2`. If it fails, the required replacement is projected
kernel-band saving

$$
E_A(d,N,L)\ll d^{-1}L^3\Delta_L\mathcal B_d
$$

with

$$
\Delta_L
\le
{\mathcal T_{d,N}\over C_L d^{-1}L^3\mathcal B_d}
$$

on the failing bands.

## Shift-Budget Input

Under the major-radius input, take

$$
\rho_{\max}(q)\ge c_1Q_0^{-2}.
$$

Then

$$
\mathcal S(Q_0,H,\rho_{\max})
=
\sum_{q\le Q_0}{1\over q}
\min\left(H,{1\over\rho_{\max}(q)}\right)
\ll
\min(H,Q_0^2)\log Q_0.
$$

The shift inequality is implied by

$$
\mathcal E_{\mathrm{shift}}
\ge
C_S\mathcal A_{\min}Q_0^2
\min(H,Q_0^2)\log Q_0.
$$

This is the completion-side shift budget required to remove the kernel peak
core far enough for the post-variation divisor-kernel estimate.

If this fails, the packet-frame fallback must prove the mass estimate
directly:

$$
\|(1-P_{\mathrm{maj}})\Omega_N\|_1
\le
{\mathcal E_{\mathrm{shift}}
\over
\mathcal S\mathcal A_{\min}}.
$$

## Major-Budget Input

With

$$
\rho_{\mathrm{valid}}^0\ge c_1Q_0^{-2},
$$

the `R_LS` inequality is implied by

$$
\mathcal E_{\mathrm{maj}}
\ge
C_M{B_{\mathrm{ov}}\mathcal A_2Q_0^4\over(\log X)^2}.
$$

Since `B_ov=O(1)` in the separated literal branch and

$$
\mathcal A_2\le C_A\|a\|_2^2,
$$

the major budget requirement is the ratio condition

$$
{\mathcal E_{\mathrm{maj}}\over\mathcal A_2}
\ge
C_M{Q_0^4\over(\log X)^2}.
$$

For `Q0=(log X)^B`, this reads

$$
{\mathcal E_{\mathrm{maj}}\over\mathcal A_2}
\ge
C_M(\log X)^{4B-2}.
$$

Consequently, if the available major budget is only a fixed positive fraction
of the residual energy, the clean literal large-sieve branch requires

$$
B\le {1\over2}-\varepsilon
$$

for a logarithmic margin. If `B > 1/2`, the literal route needs either a
larger major budget relative to `A_2`, a sharper concentration estimate than
`rho_core^{-2}`, or the packet-frame measure theorem.

## Combined Polylog Closure

The direct literal branch closes in the clean conductor range

$$
Q_0\le(\log X)^{1/2-\varepsilon}
$$

provided the completion side supplies:

$$
\mathcal T_{d,N}
\ge
C_Ld^{-1}\mathcal B_dQ_0^6,
$$

$$
\mathcal E_{\mathrm{shift}}
\ge
C_S\mathcal A_{\min}Q_0^2
\min(H,Q_0^2)\log Q_0,
$$

and

$$
\mathcal E_{\mathrm{maj}}
\ge
C_M\mathcal A_2Q_0^4(\log X)^{-2}.
$$

The major-arc side supplies

$$
\rho_{\mathrm{valid}}^0\ge c_1Q_0^{-2}
$$

by Siegel-Walfisz in the same polylog range.

## Packet-Frame Alternative

If the budget ratio forces `B > 1/2`, or if the completion-side lower bounds
do not fit the available Poisson allowance, the literal support route must be
replaced by the Unified Packet-Frame Lower Bound. The proof must supply:

$$
\|(1-P_{\mathrm{maj}})w_{N,L}\|_2^2
\le
\Delta_L\|w_{N,L}\|_2^2
$$

with `Delta_L` small enough to replace the missing `T_{d,N}` margin,

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

This fallback is exact: it replaces the three failed literal radius uses by
the three residual estimates those radii were meant to deliver.

## Result

The polylog literal branch is now a quantitative verification problem with a
visible conductor threshold. Major validity at radius `c1 Q0^{-2}` follows
from Siegel-Walfisz for fixed `B`; frame conditioning follows from
`Q0^4/X -> 0`. The remaining completion-side estimates are the lower bound
for `T_{d,N}`, the shifted-kernel budget bound, and the major-budget ratio
bound. Without those estimates, the unified packet-frame lower bound is the
only noncircular replacement.
