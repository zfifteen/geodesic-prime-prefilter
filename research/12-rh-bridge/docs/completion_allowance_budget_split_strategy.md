# Completion Allowance Budget Split Strategy

Date: 2026-05-24

Status: final budget-split strategy for the Direct Full-Radius BDH Assembly
in the polylogarithmic literal route.

The three completion-side source estimates have now been reduced to explicit
requirements:

$$
\mathcal T_{d,N}\ge C_Ld^{-1}\mathcal B_dQ_0^6,
$$

$$
{\mathcal E_{\mathrm{shift}}\over\mathcal A_{\min}}
\ge
C_SQ_0^2\min(H,Q_0^2)\log Q_0,
$$

and

$$
{\mathcal E_{\mathrm{maj}}\over\mathcal A_2}
\ge
C_M{Q_0^4\over(\log X)^2}.
$$

The final literal-route question is whether the available completion allowance
can pay all three at once.

## Band Allowance Requirement

The kernel-band allowance is

$$
\mathcal T_{d,N}
=
{ \mathcal P_{d,N}^2
\over
(R_{\mathrm{spec}}^2+H_dT_d)
(R_{\mathrm{spec}}^2+K_d)U E_v(d)}
(\log X)^{-C}.
$$

Thus the band requirement is equivalently

$$
\mathcal P_{d,N}^2
\ge
C_Ld^{-1}\mathcal B_dQ_0^6
(R_{\mathrm{spec}}^2+H_dT_d)
(R_{\mathrm{spec}}^2+K_d)U E_v(d)
(\log X)^C.
$$

Define the required band allowance by

$$
\mathcal E_{\mathrm{band}}^{\mathrm{req}}
=
\sum_{d,N}
C_Ld^{-1}\mathcal B_dQ_0^6
(R_{\mathrm{spec}}^2+H_dT_d)
(R_{\mathrm{spec}}^2+K_d)U E_v(d)
(\log X)^C,
$$

where the sum runs over the relevant dyadic completion slices. This is the
amount of squared Poisson allowance needed to make `L_crit >= C Q0^2`.

## Shift Allowance Requirement

The shifted-kernel branch requires

$$
\mathcal E_{\mathrm{shift}}^{\mathrm{req}}
=
C_S\mathcal A_{\min}Q_0^2
\min(H,Q_0^2)\log Q_0.
$$

This comes from the literal mass estimate

$$
\|\Omega_N^{\perp}\|_1\ll Q_0^2
$$

and the divisor-window sum

$$
\mathcal S(Q_0,H,\rho_{\max})
\ll
\min(H,Q_0^2)\log Q_0.
$$

## Major Allowance Requirement

The major-window branch requires

$$
\mathcal E_{\mathrm{maj}}^{\mathrm{req}}
=
C_M\mathcal A_2{Q_0^4\over(\log X)^2}.
$$

This comes from the direct large-sieve operator constant

$$
\mathcal L_{\mu}
\ll
Q_0^4
$$

after bounded overlap and core removal.

## Budget Split

Let `E_tot` be the completion-side error allowance remaining after the main
term, trivial-zero terms, coherent major packets, accepted diagonal terms, and
singular terms are removed. The literal direct route requires

$$
\mathcal E_{\mathrm{tot}}
\ge
\mathcal E_{\mathrm{band}}^{\mathrm{req}}
+
\mathcal E_{\mathrm{shift}}^{\mathrm{req}}
+
\mathcal E_{\mathrm{maj}}^{\mathrm{req}}
+
\mathcal E_{\mathrm{tail}},
$$

where `E_tail` absorbs smoothing tails, Gram leakage, and Siegel-Walfisz
amplitude errors. In the fixed polylogarithmic regime, `E_tail` is smaller
than any assigned fixed logarithmic power after choosing the
Siegel-Walfisz exponent sufficiently large.

If this split holds, choose

$$
\mathcal E_{\mathrm{shift}}
\ge
\mathcal E_{\mathrm{shift}}^{\mathrm{req}},
\qquad
\mathcal E_{\mathrm{maj}}
\ge
\mathcal E_{\mathrm{maj}}^{\mathrm{req}},
$$

and choose `P_{d,N}` so that each dyadic band inequality holds. Then

$$
R_{\mathrm{all}}\le\min(\rho_{\mathrm{valid}}^0,c_1Q_0^{-2})
$$

and the Direct Full-Radius BDH Assembly closes in the literal branch.

## Packet-Frame Replacement

If the budget split fails, the route must prove the Unified Packet-Frame
Source theorem. It replaces the three paid literal estimates by direct
residual capture:

$$
\|(1-P_{\mathrm{maj}})w_{N,L}\|_2^2
\le
\Delta_L\|w_{N,L}\|_2^2,
$$

with `Delta_L` small enough to reduce the band requirement;

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

This is not an alternate budget split. It is a stronger projection theorem
that lowers the three required payments by proving the residual quantities
directly.

## Final Inputs

The budget split closes after these quantities are fixed:

1. the total completion allowance `E_tot`;
2. the dyadic band allowances `P_{d,N}`;
3. the kernel-band parameters `B_d,H_d,T_d,K_d,U,E_v(d),R_spec`;
4. the shift quantities `A_min,H,rho_max`;
5. the major-window quantities `A_2,B_ov,E_maj`;
6. the smoothing and amplitude tail budget `E_tail`;
7. if the split fails, the three residual estimates in the Unified
   Packet-Frame Source theorem.

## Result

The direct full-radius BDH route has one final literal check:

$$
\mathcal E_{\mathrm{tot}}
\ge
\mathcal E_{\mathrm{band}}^{\mathrm{req}}
+
\mathcal E_{\mathrm{shift}}^{\mathrm{req}}
+
\mathcal E_{\mathrm{maj}}^{\mathrm{req}}
+
\mathcal E_{\mathrm{tail}}.
$$

Together with the already verified polylog major-radius, frame, amplitude,
kernel-band, shift-kernel, and major-window estimates, this budget split is
the last quantitative gate for the literal branch. Failure of the split
forces the Unified Packet-Frame Source theorem.
