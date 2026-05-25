# Type II Physical Length Assignment

Date: 2026-05-24

Status: derivation of the physical lengths `N_d` and `V_d` from the Type II
decomposition and common-divisor split.

The kernel-band physical-length test left three unexpanded quantities:

$$
U,\qquad \mathcal N_d,\qquad \mathcal V_d.
$$

These come directly from the Type II bilinear ranges.

## Original Type II Ranges

Start with a Type II piece

$$
S_{A,B}(\alpha)
=
\sum_{m\sim A}\alpha_m
\sum_{n\sim B}\beta_n e(\alpha mn),
\qquad
AB\asymp X.
$$

After expanding the shifted mean square, use the common-divisor split

$$
m=du,\qquad m'=dv,\qquad (u,v)=1.
$$

Then

$$
u,v\sim {A\over d}.
$$

Thus the slope/modulus length is

$$
U\asymp {A\over d}.
$$

## Completed `n'` Length

The linearized equation is

$$
un-vn'=t.
$$

For fixed `u,v,t`, the variable `n'` remains in the original Type II interval

$$
n'\sim B,
$$

with an additional smooth cutoff enforcing

$$
n={t+vn'\over u}\sim B.
$$

The intersection has length at most the original `B`-scale and has `B`-scale
in the nondegenerate interior of the dyadic box. Therefore the safe physical
length for completion is

$$
\mathcal N_d\asymp B
$$

for the main dyadic range, with endpoint truncation charged to smoothing
tails.

## Completed Slope Length

The completed slope variable is `v`, and after the common-divisor split it
ranges over

$$
v\sim {A\over d}.
$$

Therefore

$$
\mathcal V_d\asymp U\asymp {A\over d}.
$$

This gives

$$
K_d\ll 1+{U\over\mathcal V_d}\ll 1.
$$

## Derived Support And Norm Laws

Substitution gives:

$$
H_d\ll 1+{U\over \mathcal N_d}
\ll
1+{A\over dB},
$$

$$
K_d\ll 1,
$$

$$
T_d\ll {L\over d}.
$$

The divisor-bounded coefficient norms become

$$
\mathcal B_d\ll B(\log X)^C,
$$

and

$$
E_v(d)\ll {A\over d}(\log X)^C.
$$

These are the Type II support and norm inputs for the kernel-band dyadic
load.

## Resulting Physical Load

Using

$$
U={A\over d},\qquad
\mathcal N_d=B,\qquad
\mathcal V_d={A\over d},
$$

the base prefactor in the physical load is

$$
d^{-1}\mathcal N_dU\mathcal V_d
\asymp
{A^2B\over d^3}
=
{AX\over d^3}.
$$

The dimensionless factors are

$$
A_{d,L}
\ll
{Ld\over A^2}
\left(1+{A\over dB}\right),
$$

$$
B_{d,L}
\ll
{L\over d}
\left(1+{A\over dB}\right),
$$

and

$$
C_d\ll 1.
$$

Thus

$$
\mathfrak L_{d,L}
\ll
{AX\over d^3}
\left(1+
{Ld\over A^2}\left(1+{A\over dB}\right)
+
{L\over d}\left(1+{A\over dB}\right)
\right)
\left(1+
{Ld\over A^2}\left(1+{A\over dB}\right)
\right)
(\log X)^C.
$$

This is the Type II physical-load formula.

## Balanced Diagnostic

In the balanced range

$$
A\asymp B\asymp X^{1/2},
$$

the load becomes

$$
\mathfrak L_{d,L}
\ll
{X^{3/2}\over d^3}
\left(1+{Ld\over X}+{L\over d}\right)
\left(1+{Ld\over X}\right)
(\log X)^C.
$$

The term `L/d` is the visible high-band cost. If this cost makes the dyadic
sum exceed the allocated band budget, the required remedy is not another
support identity; it is projected band saving `Delta_L` or a sharper Type II
coefficient norm.

## Final Type II Inputs

The Type II assignment closes after the project fixes:

1. the dyadic Type II ranges `A,B` with `AB asymp X`;
2. the common-divisor range for `d`;
3. smoothing tails for the `n,n'` box intersections;
4. the divisor-bounded coefficient norms in the chosen endpoint
   decomposition;
5. the dyadic kernel-band range for `L`;
6. the allocated band budget or the packet-frame saving law `Delta_L`.

## Result

The physical lengths are no longer abstract:

$$
U\asymp A/d,\qquad
\mathcal N_d\asymp B,\qquad
\mathcal V_d\asymp A/d.
$$

Substituting them exposes the exact high-band pressure term `L/d`. The
literal route closes only if the resulting dyadic load fits the band
allocation; otherwise the Unified Packet-Frame Source theorem must provide
the corresponding `Delta_L` saving or a sharper Type II norm estimate.
