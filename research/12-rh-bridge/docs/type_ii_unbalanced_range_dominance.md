# Type II Unbalanced Range Dominance

Date: 2026-05-24

Status: dominance check showing that the balanced Type II range controls the
summed physical-length load in the polylogarithmic literal branch.

The general Type II load for `AB asymp X` is

$$
\mathcal K_{A,B}(Q_0^2)
=
AX(\log X)^C
\sum_{d\le A}
d^{-3}
\left(1+
{Q_0^2d\over A^2}\left(1+{A\over dB}\right)
+
{Q_0^2\over d}\left(1+{A\over dB}\right)
\right)
\left(1+
{Q_0^2d\over A^2}\left(1+{A\over dB}\right)
\right).
$$

Assume the Type II decomposition is oriented so that

$$
A\le B,
\qquad
AB\asymp X,
$$

and that the Type II floor satisfies

$$
A\ge X^{\theta}
$$

for fixed `theta>0`. Since `Q0` is polylogarithmic,

$$
{Q_0^2\over A^2}=o(1).
$$

## Bounding The Ratios

Because `A <= B`,

$$
{A\over B}\le1,
\qquad
{A\over dB}\le {1\over d}.
$$

Therefore

$$
1+{A\over dB}\ll 1.
$$

The second factor satisfies

$$
1+
{Q_0^2d\over A^2}\left(1+{A\over dB}\right)
\ll
1+{Q_0^2d\over A^2}.
$$

For `d <= A`, the dyadic sum splits at

$$
d_0={A^2\over Q_0^2}.
$$

Since `A >= X^theta` and `Q0` is polylogarithmic, `d_0 >> A` for large `X`.
Thus throughout the actual range `d <= A`,

$$
{Q_0^2d\over A^2}=o(1).
$$

The first factor is then controlled by

$$
1+{Q_0^2\over d}.
$$

## Unbalanced Load Bound

It follows that

$$
\mathcal K_{A,B}(Q_0^2)
\ll
AX(\log X)^C
\sum_{d\le A}
d^{-3}\left(1+{Q_0^2\over d}\right).
$$

The divisor sum is bounded by `O(Q0^2)`, so

$$
\mathcal K_{A,B}(Q_0^2)
\ll
AXQ_0^2(\log X)^C.
$$

Since `A <= X^{1/2}`,

$$
\mathcal K_{A,B}(Q_0^2)
\ll
X^{3/2}Q_0^2(\log X)^C.
$$

Thus the balanced range is the worst Type II range for the physical-length
load.

## Full Type II Band Requirement

After summing over dyadic `A,B` ranges, logarithmic losses are absorbed into
the exponent `C`. Hence

$$
\mathcal E_{\mathrm{band,TypeII}}^{\mathrm{req}}
\ll
X^{3/2}Q_0^8(\log X)^C.
$$

The literal Type II band contribution closes if

$$
\mathcal E_{\mathrm{band}}^{\mathrm{alloc}}
\ge
C X^{3/2}Q_0^8(\log X)^C.
$$

## Packet-Frame Alternative

If this fails, the packet-frame theorem must supply average saving

$$
\overline{\Delta}
\le
{\mathcal E_{\mathrm{band}}^{\mathrm{alloc}}
\over
X^{3/2}Q_0^8(\log X)^C},
$$

or the sharper slice-level condition

$$
\sum_{A,B,d,L\le Q_0^2}
\Delta_L L^3\mathfrak L_{A,B,d,L}
\le
\mathcal E_{\mathrm{band}}^{\mathrm{alloc}}.
$$

## Final Type II Inputs

This dominance argument requires:

1. orientation of Type II ranges with `A <= B`;
2. a fixed Type II floor `A >= X^theta`;
3. polylogarithmic `Q0`;
4. divisor-bounded coefficient norms;
5. dyadic summation over `A,B,d,L`;
6. the allocated band budget or the packet-frame saving law.

## Result

Under the standard Type II floor and `A <= B` orientation, the balanced range
dominates the kernel-band physical load. The full Type II literal band payment
is therefore

$$
\mathcal E_{\mathrm{band,TypeII}}^{\mathrm{req}}
\ll
X^{3/2}Q_0^8(\log X)^C.
$$

If the completion allowance cannot pay this amount, the exact remaining
obligation is packet-frame `Delta_L` saving or a sharper Type II norm theorem.
