# PGS Completion Budget Source Ledger

Date: 2026-05-24

Status: source ledger for verifying the three completion-side lower bounds
in the polylogarithmic direct route.

The direct literal route now needs three PGS-side estimates:

$$
\mathcal T_{d,N}\ge C_Ld^{-1}\mathcal B_dQ_0^6,
$$

$$
\mathcal E_{\mathrm{shift}}
\ge
C_S\mathcal A_{\min}Q_0^2
\min(H,Q_0^2)\log Q_0,
$$

and

$$
{\mathcal E_{\mathrm{maj}}\over\mathcal A_2}
\ge
C_M{Q_0^4\over(\log X)^2}.
$$

The major-radius and frame-amplitude inputs already close in the
polylogarithmic range. The remaining work is to identify the PGS completion
quantities that supply these three inequalities.

## 1. Kernel-Band Source For `T_{d,N}`

The kernel-band source is the transformed product-difference weight after
major projection:

$$
W_{N,L}^{\perp}(r)
=
\int w_{N,L}^{\perp}(\alpha)e(\alpha r)\,d\alpha .
$$

The current base estimate is

$$
\sum_t |W_{N,L}^{\perp}(dt)|^2
\ll
d^{-1}L^3\Delta_L,
$$

where `Delta_L=1` is the Parseval bound and `Delta_L<1` is projected
kernel-band saving.

The completion allowance is

$$
\mathcal T_{d,N}
=
{ \mathcal P_{d,N}^2
\over
(R_{\mathrm{spec}}^2+H_dT_d)
(R_{\mathrm{spec}}^2+K_d)U E_v(d)}
(\log X)^{-C}.
$$

Thus the literal branch requires

$$
{ \mathcal P_{d,N}^2
\over
(R_{\mathrm{spec}}^2+H_dT_d)
(R_{\mathrm{spec}}^2+K_d)U E_v(d)}
(\log X)^{-C}
\ge
C_Ld^{-1}\mathcal B_dQ_0^6.
$$

If this fails with `Delta_L=1`, the exact replacement estimate is

$$
\Delta_L
\le
{ \mathcal T_{d,N}
\over
C_Ld^{-1}\mathcal B_dQ_0^6}.
$$

The final quantities required here are:

- the smoothed band weight `w_{N,L}`;
- the projected transform norm of `W_{N,L}^perp(dt)`;
- the completion support sizes `H_d,T_d,K_d`;
- the Bessel-selected spectral range `R_spec`;
- the Type II slope norm `E_v(d)`;
- the divisor coefficient norm `B_d`;
- the Poisson allowance `P_{d,N}`.

## 2. Shift-Kernel Source For `E_shift`

The shift branch enters through

$$
\|\Omega_N^{\perp}\|_1
\mathcal S(Q_0,H,\rho_{\max})
\mathcal A_{\min}
\le
\mathcal E_{\mathrm{shift}}.
$$

In the literal aperture branch, core removal gives

$$
\|\Omega_N^{\perp}\|_1\ll Q_0^2
$$

at the separation radius. With

$$
\rho_{\max}(q)\ge c_1Q_0^{-2},
$$

the divisor-window sum satisfies

$$
\mathcal S(Q_0,H,\rho_{\max})
\ll
\min(H,Q_0^2)\log Q_0.
$$

Therefore the source estimate to prove is

$$
{\mathcal E_{\mathrm{shift}}\over\mathcal A_{\min}}
\ge
C_SQ_0^2\min(H,Q_0^2)\log Q_0.
$$

The final quantities required here are:

- the residual endpoint minor mass `A_min`;
- the effective shift length `H`;
- the major-radius lower bound controlling `rho_max`;
- the actual projected kernel-window mass
  `||Omega_N^perp||_1`;
- the budget assigned to the shifted-kernel branch.

If the literal mass estimate fails, the packet-frame theorem must prove

$$
\|\Omega_N^{\perp}\|_1
\le
{\mathcal E_{\mathrm{shift}}
\over
\mathcal S\mathcal A_{\min}}
$$

directly, without using support containment.

## 3. Major-Window Source For `E_maj/A_2`

The direct continuous-frequency large sieve gives the major-window residual
estimate if

$$
{\mathcal E_{\mathrm{maj}}\over\mathcal A_2}
\ge
C_M{Q_0^4\over(\log X)^2}.
$$

For

$$
Q_0=(\log X)^B,
$$

this is

$$
{\mathcal E_{\mathrm{maj}}\over\mathcal A_2}
\ge
C_M(\log X)^{4B-2}.
$$

If the available major budget has the form

$$
{\mathcal E_{\mathrm{maj}}\over\mathcal A_2}
\ge
(\log X)^{-\eta},
$$

then the literal branch allows

$$
B\le {2-\eta\over4}-\varepsilon.
$$

The clean fixed-fraction case is `eta=0`, giving

$$
B\le {1\over2}-\varepsilon.
$$

The final quantities required here are:

- the residual coefficient energy `A_2`;
- the available major-window budget `E_maj`;
- the overlap constant `B_ov`;
- the core-removal or packet-frame concentration constant;
- the exact endpoint normalization for the deconvolved coefficient sequence.

## 4. Budget Split Condition

Let `E_tot` denote the completion-side error allowance available after the
main term, trivial-zero terms, and accepted diagonal/singular contributions
are removed. The literal route requires a split

$$
\mathcal E_{\mathrm{tot}}
\ge
\mathcal E_{\mathrm{shift}}^{\mathrm{req}}
+
\mathcal E_{\mathrm{maj}}^{\mathrm{req}}
+
\mathcal E_{\mathrm{band}}^{\mathrm{req}},
$$

where `E_band^req` is the amount of Poisson allowance needed to make
`T_{d,N} >= C d^{-1} B_d Q0^6` over all relevant dyadic `d,L` slices.

This is the final budget-consistency check. It is separate from the
major-radius input and from frame conditioning.

## Unified Packet-Frame Source

If the budget split fails, the fallback is not another choice of radii. It is
the unified packet-frame theorem:

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

This theorem proves directly that the low-conductor packet span captures the
same three objects that literal support removal was designed to capture:
kernel-band energy, kernel-window mass, and weighted measure concentration.

## Result

The completion side has been reduced to a finite source ledger. To close the
Direct Full-Radius BDH Assembly in the polylogarithmic literal branch, the
project must compute or prove the kernel-band allowance `T_{d,N}`, the
shift-kernel budget ratio `E_shift/A_min`, and the major-window budget ratio
`E_maj/A_2`. If these do not fit the available completion allowance, the
single remaining replacement is the Unified Packet-Frame Lower Bound.
