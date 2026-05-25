# Kernel-Band Physical-Length Closure Test

Date: 2026-05-24

Status: physical-length substitution for the kernel-band dyadic load.

The final kernel-band inputs give:

$$
H_d\ll 1+{U\over \mathcal N_d},
\qquad
K_d\ll 1+{U\over \mathcal V_d},
\qquad
T_d\ll {L\over d},
$$

and, with divisor-bounded smooth coefficients,

$$
\mathcal B_d\ll \mathcal N_d(\log X)^C,
\qquad
E_v(d)\ll \mathcal V_d(\log X)^C.
$$

This note substitutes those laws into the dyadic load.

## Substituted Bessel Factor

The Bessel factor is

$$
{H_dT_dK_d\over U^2}
\ll
{L\over dU^2}
\left(1+{U\over\mathcal N_d}\right)
\left(1+{U\over\mathcal V_d}\right).
$$

The other two large-sieve support factors are

$$
H_dT_d
\ll
{L\over d}\left(1+{U\over\mathcal N_d}\right),
\qquad
K_d
\ll
1+{U\over\mathcal V_d}.
$$

Therefore

$$
\mathcal D_{d,L}
\ll
\left(
1+
{L\over dU^2}
\left(1+{U\over\mathcal N_d}\right)
\left(1+{U\over\mathcal V_d}\right)
+
{L\over d}\left(1+{U\over\mathcal N_d}\right)
\right)
\left(
1+
{L\over dU^2}
\left(1+{U\over\mathcal N_d}\right)
\left(1+{U\over\mathcal V_d}\right)
+
1+{U\over\mathcal V_d}
\right)
U\mathcal V_d(\log X)^C.
$$

## Physical-Length Load

Multiplying by `d^{-1} B_d` gives the dyadic contribution

$$
\mathfrak L_{d,L}
\ll
d^{-1}\mathcal N_dU\mathcal V_d
\left(
1+
{L\over dU^2}
\left(1+{U\over\mathcal N_d}\right)
\left(1+{U\over\mathcal V_d}\right)
+
{L\over d}\left(1+{U\over\mathcal N_d}\right)
\right)
\left(
1+
{L\over dU^2}
\left(1+{U\over\mathcal N_d}\right)
\left(1+{U\over\mathcal V_d}\right)
+
1+{U\over\mathcal V_d}
\right)
(\log X)^C.
$$

The literal kernel-band payment is verified if

$$
\sum_{d,L}
\mathfrak L_{d,L}
\le
{ \mathcal E_{\mathrm{band}}^{\mathrm{alloc}}
\over
C_LQ_0^6(\log X)^C}.
$$

This is the physical-length closure test.

## Dominant Terms

The three dimensionless ratios controlling the load are:

$$
A_{d,L}={L\over dU^2}
\left(1+{U\over\mathcal N_d}\right)
\left(1+{U\over\mathcal V_d}\right),
\qquad
B_{d,L}={L\over d}\left(1+{U\over\mathcal N_d}\right),
\qquad
C_d=1+{U\over\mathcal V_d}.
$$

Then

$$
\mathfrak L_{d,L}
\ll
d^{-1}\mathcal N_dU\mathcal V_d
(1+A_{d,L}+B_{d,L})(1+A_{d,L}+C_d)
(\log X)^C.
$$

Thus the literal route closes when the weighted sum of these dimensionless
products fits inside the allocated band budget.

## Packet-Frame Delta Requirement

If the physical-length load is too large, the packet-frame replacement must
insert `Delta_L` into the transform-energy factor:

$$
\sum_{d,L}
\Delta_L L^3\,\mathfrak L_{d,L}
\le
\mathcal E_{\mathrm{band}}^{\mathrm{alloc}}.
$$

Equivalently, a slice-level sufficient condition is

$$
\Delta_L
\le
{ \mathcal E_{\mathrm{band}}^{\mathrm{alloc}}(d,L)
\over
L^3\mathfrak L_{d,L}}.
$$

This is the exact projected band-energy saving demanded by the Unified
Packet-Frame Source theorem after physical-length substitution.

## Final Physical Inputs

The physical-length test closes after the project fixes:

1. `U` as a function of the original Type II ranges and `d`;
2. `N_d`, the completed `n'` interval length;
3. `V_d`, the completed `v` interval length;
4. the dyadic kernel scale `L`;
5. the dyadic summation range for `d,L`;
6. the allocated band budget;
7. if needed, the packet-frame saving law `Delta_L`.

## Result

The kernel-band source is now a physical-length inequality. The only
unexpanded quantities are `U`, `N_d`, `V_d`, the dyadic ranges, and the
allocated band budget. Once those are fixed by the Type II decomposition,
the literal band payment is checked by the displayed sum; if it fails, the
required packet-frame saving is
`Delta_L <= E_band^alloc(d,L)/(L^3 mathfrak L_{d,L})`.
