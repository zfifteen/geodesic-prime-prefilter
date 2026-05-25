# Kernel-Band Dyadic Load Parameter Strategy

Date: 2026-05-24

Status: parameter-size strategy for verifying the summed kernel-band load
against the allocated completion allowance.

The kernel-band allowance total verification reduced the band side to

$$
\sum_{d,N}
d^{-1}\mathcal B_d\mathcal D_{d,N}
\le
{ \mathcal E_{\mathrm{band}}^{\mathrm{alloc}}
\over
C_LQ_0^6(\log X)^C},
$$

where

$$
\mathcal D_{d,N}
=
(R_{\mathrm{spec}}^2+H_dT_d)
(R_{\mathrm{spec}}^2+K_d)U E_v(d).
$$

The remaining kernel-band task is to bound the dyadic load from the actual
support sizes and coefficient norms.

## Direct Parameter Ledger

For each dyadic completion slice, fix:

$$
d,\quad U,\quad H_d,\quad T_d,\quad K_d,\quad
\mathcal B_d,\quad E_v(d).
$$

The Bessel range input gives

$$
R_{\mathrm{spec}}^2
\ll
1+{H_dT_dK_d\over U^2}.
$$

Thus the load is bounded by

$$
\mathcal D_{d,N}
\ll
\left(1+{H_dT_dK_d\over U^2}+H_dT_d\right)
\left(1+{H_dT_dK_d\over U^2}+K_d\right)
U E_v(d).
$$

The direct verification is therefore:

$$
\sum_{d,N}
d^{-1}\mathcal B_d
\left(1+{H_dT_dK_d\over U^2}+H_dT_d\right)
\left(1+{H_dT_dK_d\over U^2}+K_d\right)
U E_v(d)
\le
{ \mathcal E_{\mathrm{band}}^{\mathrm{alloc}}
\over
C_LQ_0^6(\log X)^C}.
$$

## Exponent Test

For a fast audit, write the dyadic sizes as powers of `X`:

$$
d=X^\delta,\quad
U=X^\upsilon,\quad
H_d=X^\eta,\quad
T_d=X^\tau,\quad
K_d=X^\kappa,
$$

$$
\mathcal B_d=X^\beta,\quad
E_v(d)=X^\epsilon,\quad
\mathcal E_{\mathrm{band}}^{\mathrm{alloc}}=X^\omega.
$$

The Bessel exponent is

$$
r=\max\left(0,{ \eta+\tau+\kappa\over2}-\upsilon\right),
$$

so the dyadic load exponent is bounded by

$$
-\delta+\beta+\upsilon+\epsilon
+\max(2r,\eta+\tau)
+\max(2r,\kappa).
$$

The kernel-band sum has polynomial room if this exponent is strictly below
`\omega` after summing over dyadic slices. The polylog factor `Q0^6 log^C X`
is then absorbed by the exponent margin. If the exponents tie, the proof
needs logarithmic saving from projected band energy or coefficient
cancellation.

## Coefficient-Norm Inputs

The coefficient norms enter through:

$$
\sum_h |B_{d,h,t}|^2\ll\mathcal B_d,
$$

and

$$
E_v(d)=\sum_{v\sim U}|c_v|^2.
$$

For divisor-bounded Type II coefficients, the expected form is a dyadic
length times a polylogarithmic factor. The verification must state the exact
forms used, because the load is multiplicative in `B_d` and `E_v(d)`.

## Packet-Frame Replacement

If the exponent test fails, the required packet-frame saving is determined
slice by slice by

$$
\sum_{d,N,L}
d^{-1}L^3\Delta_L\mathcal B_d\mathcal D_{d,N}
\le
\mathcal E_{\mathrm{band}}^{\mathrm{alloc}}.
$$

Equivalently, for a failing slice,

$$
\Delta_L
\le
{ \mathcal E_{\mathrm{band}}^{\mathrm{alloc}}(d,N,L)
\over
d^{-1}L^3\mathcal B_d\mathcal D_{d,N}}.
$$

This is the residual band-energy requirement in the Unified Packet-Frame
Source theorem.

## Final Kernel-Band Inputs

The kernel-band dyadic load closes after these are fixed:

1. the dyadic ranges for `d,N,L`;
2. the support laws for `H_d,T_d,K_d,U`;
3. the Bessel range bound for `R_spec`;
4. the coefficient norm laws for `B_d` and `E_v(d)`;
5. the allocated band budget `E_band^alloc`;
6. if the direct load is too large, the projected band saving law
   `Delta_L`.

## Result

The kernel-band source has reached an exponent-and-log verification. Once the
support sizes and coefficient norms are fixed, the dyadic load exponent above
decides whether the literal route pays `E_band^req`. If it does not, the
packet-frame branch must supply exactly the displayed `Delta_L` saving.
