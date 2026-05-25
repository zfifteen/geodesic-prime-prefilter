# Shift-Kernel Budget Ratio Strategy

Date: 2026-05-24

Status: focused strategy for verifying the shift-kernel lower bound
`E_shift / A_min >= C Q0^2 min(H,Q0^2) log Q0`, or the packet-frame
replacement for kernel-window mass.

The shift-kernel branch controls the divisor-weighted shifted-congruence
kernel after major projection. After the variation lemma, it has one scalar
form:

$$
\|\Omega_N^{\perp}\|_1
\mathcal S(Q_0,H,\rho_{\max})
\mathcal A_{\min}
\le
\mathcal E_{\mathrm{shift}}.
$$

Thus the source task is to bound `||Omega_N^perp||_1` and
`S(Q0,H,rho_max)` from PGS kernel geometry after major projection.

## Literal Core-Removal Mass

In the polylogarithmic literal route, the major aperture removes the kernel
peak core to radius

$$
\rho_{\mathrm{core}}\asymp Q_0^{-2}.
$$

The interval kernel satisfies

$$
|K_N(\beta)|\ll\min(N,\|\beta\|^{-1}).
$$

Since `Q0` is polylogarithmic, `rho_core >> N^{-1}` for large `X`. Therefore
the annular tail satisfies

$$
\|\Omega_N^{\perp}\|_1
\ll
\int_{\rho_{\mathrm{core}}\le|\beta|\le 1/2}
{d\beta\over \beta^2}
\ll
\rho_{\mathrm{core}}^{-1}
\ll
Q_0^2.
$$

This is the mass source for the shift-kernel budget.

## Divisor-Window Sum

With the same major-radius input,

$$
\rho_{\max}(q)\ge c_1Q_0^{-2}
$$

for every `q <= Q0`. Hence

$$
\mathcal S(Q_0,H,\rho_{\max})
=
\sum_{q\le Q_0}{1\over q}
\min\left(H,{1\over\rho_{\max}(q)}\right)
\ll
\min(H,Q_0^2)\log Q_0.
$$

Combining the mass bound and the divisor-window sum gives

$$
\|\Omega_N^{\perp}\|_1
\mathcal S(Q_0,H,\rho_{\max})
\mathcal A_{\min}
\ll
\mathcal A_{\min}Q_0^2\min(H,Q_0^2)\log Q_0.
$$

Thus the literal branch closes the shift-kernel budget if

$$
{\mathcal E_{\mathrm{shift}}\over \mathcal A_{\min}}
\ge
C_SQ_0^2\min(H,Q_0^2)\log Q_0.
$$

## Variation Input

The variation lemma supplies

$$
V_q\ll \|\Omega_N^{\perp}\|_1
$$

uniformly for `q <= Q0`. No additional divisor exponential-sum estimate is
needed after the core-removal mass bound, because all denominator dependence
has been moved into `S(Q0,H,rho_max)`.

## Packet-Frame Mass Replacement

If the literal aperture cannot remove the core to `rho_core ~ Q0^{-2}`, the
replacement is the direct mass theorem

$$
\|\Omega_N^{\perp}\|_1
\le
{\mathcal E_{\mathrm{shift}}
\over
\mathcal S(Q_0,H,\rho_{\max})\mathcal A_{\min}}.
$$

A sufficient projection-energy form is

$$
\|\Omega_N^{\perp}\|_2
\le
{\mathcal E_{\mathrm{shift}}
\over
\mathcal S(Q_0,H,\rho_{\max})
\mathcal A_{\min}
|\operatorname{supp}\Omega_N|^{1/2}}.
$$

The corresponding packet-frame lower bound is that the low-conductor packet
span captures the kernel-window core with residual `L1` mass at most the
right-hand side above.

## Final Shift-Kernel Inputs

The shift-kernel source closes after the following quantities are fixed:

1. the exact projected kernel-window weight `Omega_N^perp`;
2. the core radius removed or captured by the major projector;
3. the annular tail estimate for `||Omega_N^perp||_1`;
4. the variation bound `V_q << ||Omega_N^perp||_1`;
5. the effective shift length `H`;
6. the major-radius lower bound determining `rho_max(q)`;
7. the residual endpoint minor mass `A_min`;
8. the assigned shifted-kernel budget `E_shift`;
9. if literal support fails, the packet-frame mass lower bound.

## Result

The shift-kernel branch has one budget-ratio test:

$$
{\mathcal E_{\mathrm{shift}}\over \mathcal A_{\min}}
\ge
C_SQ_0^2\min(H,Q_0^2)\log Q_0.
$$

Literal aperture removal proves the kernel-window mass factor
`||Omega_N^perp||_1 << Q0^2`. If this mass estimate cannot be obtained by
support geometry, the packet-frame alternative must prove the same `L1`
residual bound directly.
