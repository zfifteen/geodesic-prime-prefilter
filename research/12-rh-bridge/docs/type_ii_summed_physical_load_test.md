# Type II Summed Physical Load Test

Date: 2026-05-24

Status: summed Type II physical-load test for the literal kernel-band
payment, with the packet-frame saving target stated when the sum is too
large.

The Type II physical length assignment gives, for `AB asymp X`,

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

The literal branch pays the bands up to the critical scale

$$
L_*=Q_0^2
$$

after major-aperture removal handles larger failing bands.

## General Summed Load

Summing dyadically over `L <= L_*` and over the common-divisor range
`1 <= d <= A`, it is enough to bound

$$
\mathcal K_{A,B}(L_*)
=
AX(\log X)^C
\sum_{d\le A}
d^{-3}
\left(1+
{L_*d\over A^2}\left(1+{A\over dB}\right)
+
{L_*\over d}\left(1+{A\over dB}\right)
\right)
\left(1+
{L_*d\over A^2}\left(1+{A\over dB}\right)
\right).
$$

This is the physical-length load that enters

$$
\mathcal E_{\mathrm{band}}^{\mathrm{req}}
\ll
Q_0^6(\log X)^C\mathcal K_{A,B}(Q_0^2).
$$

## Balanced Range

For

$$
A\asymp B\asymp X^{1/2},
$$

and polylogarithmic

$$
L_*=Q_0^2,
$$

the factor

$$
{L_*d\over A^2}
\ll
{Q_0^2d\over X}
$$

is negligible throughout `d <= A` up to logarithmic loss. The visible term is

$$
{L_*\over d}.
$$

Therefore

$$
\mathcal K_{\mathrm{bal}}(Q_0^2)
\ll
X^{3/2}(\log X)^C
\sum_{d\le X^{1/2}}d^{-3}\left(1+{Q_0^2\over d}\right)
\ll
X^{3/2}Q_0^2(\log X)^C.
$$

Consequently, the balanced Type II band payment is bounded by

$$
\mathcal E_{\mathrm{band,bal}}^{\mathrm{req}}
\ll
X^{3/2}Q_0^8(\log X)^C.
$$

This is the explicit budget size required by the literal kernel-band route in
the balanced diagnostic range.

## Literal Closure Test

The literal balanced Type II band contribution closes if

$$
\mathcal E_{\mathrm{band}}^{\mathrm{alloc}}
\ge
C X^{3/2}Q_0^8(\log X)^C
$$

after the shift, major-window, and tail budgets have already been reserved.

For unbalanced Type II ranges, use the general sum
`\mathcal K_{A,B}(Q0^2)` and sum over the dyadic `A,B` decomposition.

## Packet-Frame Saving Target

If the allocated band budget is smaller than the literal sum, the required
average saving is

$$
\overline{\Delta}
\le
{\mathcal E_{\mathrm{band}}^{\mathrm{alloc}}
\over
Q_0^6(\log X)^C\mathcal K_{A,B}(Q_0^2)}.
$$

Slice by slice, the sharper target is

$$
\sum_{d,L\le Q_0^2}
\Delta_L L^3\mathfrak L_{d,L}
\le
\mathcal E_{\mathrm{band}}^{\mathrm{alloc}}.
$$

This is the Type II version of the residual band-energy requirement in the
Unified Packet-Frame Source theorem.

## Final Type II Inputs

The Type II band sum closes after the project fixes:

1. the dyadic Type II range list `(A,B)`;
2. the common-divisor range for `d`;
3. the paid kernel-band ceiling `L_*`;
4. the allocated band budget after shift, major, and tail reserves;
5. the unbalanced-range analogues of the balanced sum;
6. if needed, the average or slice-level `Delta_L` saving.

## Result

The balanced Type II diagnostic requires band budget

$$
\mathcal E_{\mathrm{band,bal}}^{\mathrm{req}}
\ll
X^{3/2}Q_0^8(\log X)^C.
$$

This is the first fully expanded kernel-band payment. If the available
completion allowance cannot pay it, the direct literal route must use the
packet-frame `Delta_L` saving or improve the Type II coefficient norm.
