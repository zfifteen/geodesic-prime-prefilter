# Kernel-Band Allowance Total Verification

Date: 2026-05-24

Status: dyadic-sum verification strategy for paying the kernel-band
allowance from the total completion budget.

The final completion matrix requires the kernel-band payment

$$
\mathcal E_{\mathrm{band}}^{\mathrm{req}}
=
\sum_{d,N}
C_Ld^{-1}\mathcal B_dQ_0^6
(R_{\mathrm{spec}}^2+H_dT_d)
(R_{\mathrm{spec}}^2+K_d)U E_v(d)
(\log X)^C.
$$

This note isolates the exact summed estimate needed to pay that amount from
the available completion allowance.

## Dyadic Kernel-Band Load

Define

$$
\mathcal D_{d,N}
=
(R_{\mathrm{spec}}^2+H_dT_d)
(R_{\mathrm{spec}}^2+K_d)U E_v(d).
$$

Then

$$
\mathcal E_{\mathrm{band}}^{\mathrm{req}}
=
C_LQ_0^6(\log X)^C
\sum_{d,N}
d^{-1}\mathcal B_d\mathcal D_{d,N}.
$$

The kernel-band source fits inside a band allocation
`\mathcal E_{\mathrm{band}}^{\mathrm{alloc}}` if

$$
\sum_{d,N}
d^{-1}\mathcal B_d\mathcal D_{d,N}
\le
{ \mathcal E_{\mathrm{band}}^{\mathrm{alloc}}
\over
C_LQ_0^6(\log X)^C}.
$$

This is the summed kernel-band verification test.

## Allocation Against `E_tot`

Choose a fixed budget share

$$
\mathcal E_{\mathrm{band}}^{\mathrm{alloc}}
\le
\mathcal E_{\mathrm{tot}}
-
\mathcal E_{\mathrm{shift}}^{\mathrm{req}}
-
\mathcal E_{\mathrm{maj}}^{\mathrm{req}}
-
\mathcal E_{\mathrm{tail}}.
$$

The literal route requires the right side to be positive and the dyadic load
to satisfy the summed test above. Equivalently,

$$
C_LQ_0^6(\log X)^C
\sum_{d,N}
d^{-1}\mathcal B_d\mathcal D_{d,N}
+
\mathcal E_{\mathrm{shift}}^{\mathrm{req}}
+
\mathcal E_{\mathrm{maj}}^{\mathrm{req}}
+
\mathcal E_{\mathrm{tail}}
\le
\mathcal E_{\mathrm{tot}}.
$$

## Parameter Verification

The dyadic kernel-band load is explicit once the following are fixed:

$$
\mathcal B_d,
\quad
H_d,
\quad
T_d,
\quad
K_d,
\quad
U,
\quad
E_v(d),
\quad
R_{\mathrm{spec}}.
$$

The Bessel range estimate gives

$$
R_{\mathrm{spec}}
\le
C_R\left(1+{\sqrt{H_dT_dK_d}\over U}\right).
$$

Substitution turns the load into a finite dyadic sum:

$$
\sum_{d,N}
d^{-1}\mathcal B_d
\left[
\left(1+{H_dT_dK_d\over U^2}+H_dT_d\right)
\left(1+{H_dT_dK_d\over U^2}+K_d\right)
U E_v(d)
\right].
$$

The verification task is to prove this sum is at most

$$
{ \mathcal E_{\mathrm{band}}^{\mathrm{alloc}}
\over
C_LQ_0^6(\log X)^C}.
$$

## Packet-Frame Band Replacement

If the dyadic load is too large, the packet-frame route must prove projected
band saving before the dyadic sum is formed:

$$
\sum_t |W_{N,L}^{\perp}(dt)|^2
\ll
d^{-1}L^3\Delta_L.
$$

The summed replacement condition is

$$
\sum_{d,N,L}
d^{-1}L^3\Delta_L\mathcal B_d\mathcal D_{d,N}
\le
\mathcal E_{\mathrm{band}}^{\mathrm{alloc}}.
$$

This is the exact residual band-energy part of the Unified Packet-Frame
Source theorem.

## Final Kernel-Band Inputs

The kernel-band allowance check closes after these are fixed:

1. the dyadic index set for `d,N,L`;
2. the divisor coefficient norms `B_d`;
3. the completion supports `H_d,T_d,K_d,U`;
4. the slope norm `E_v(d)`;
5. the Bessel range estimate for `R_spec`;
6. the band allocation inside `E_tot`;
7. if needed, the packet-frame saving factors `Delta_L`.

## Result

The kernel-band part of the final budget split is one dyadic-sum estimate:

$$
\sum_{d,N}
d^{-1}\mathcal B_d\mathcal D_{d,N}
\le
{ \mathcal E_{\mathrm{band}}^{\mathrm{alloc}}
\over
C_LQ_0^6(\log X)^C}.
$$

If it holds, the literal route pays `E_band^req`. If it fails, the exact
replacement is the packet-frame residual band-energy sum with factors
`Delta_L`.
