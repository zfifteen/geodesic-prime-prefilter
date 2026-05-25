# Direct Full-Radius BDH Polylog Literal Closure

Date: 2026-05-24

Status: assembled literal closure theorem for the Direct Full-Radius BDH
Assembly in the polylogarithmic `Q0` regime, with the Unified Packet-Frame
Source theorem as the fallback.

The direct route has four scalar gates:

$$
\rho_{\mathrm{valid}}^0\ge c_1Q_0^{-2},
$$

$$
L_{\mathrm{crit}}\ge C Q_0^2,
$$

$$
{\mathcal E_{\mathrm{shift}}\over\mathcal A_{\min}}
\ge
C Q_0^2\min(H,Q_0^2)\log Q_0,
$$

and

$$
{\mathcal E_{\mathrm{maj}}\over\mathcal A_2}
\ge
C{Q_0^4\over(\log X)^2}.
$$

This note records the polylogarithmic literal regime in which all four gates
fit inside the completion allowance.

## Regime

Take

$$
Q_0=(\log X)^B,
\qquad
B\le {1\over2}-\varepsilon.
$$

Assume the standard energy envelopes after coefficient-level major
projection:

$$
\mathcal A_2\le X(\log X)^C,
\qquad
\mathcal A_{\min}\le X(\log X)^C.
$$

Assume the convolution-scale completion allowance

$$
\mathcal E_{\mathrm{tot}}
\asymp
X\left({N\over\log X}\right)^2(\log X)^{-A_0}.
$$

Finally assume the kernel length satisfies

$$
N\ge X^{1/4}Q_0^4(\log X)^C.
$$

## Gate 1: Major Radius

For `q <= Q0`, Siegel-Walfisz gives the centered endpoint major approximation
with logarithmic saving. Since the number of centers is `O(Q0^2)`, choosing
the saving exponent large enough gives

$$
\rho_{\mathrm{valid}}^0\ge c_1Q_0^{-2}
$$

with amplitude and Gram leakage absorbed into `E_tail`.

## Gate 2: Kernel-Band Critical Scale

The Type II physical-length analysis gives

$$
\mathcal E_{\mathrm{band,TypeII}}^{\mathrm{req}}
\ll
X^{3/2}Q_0^8(\log X)^C.
$$

The kernel-length condition implies

$$
\mathcal E_{\mathrm{tot}}
\gg
X^{3/2}Q_0^8(\log X)^C
$$

after increasing the harmless logarithmic exponent. Therefore the band
allowance can be chosen so that

$$
L_{\mathrm{crit}}\ge C Q_0^2.
$$

This closes the literal high-band support-removal gate.

## Gate 3: Shift-Kernel Budget

The shift-kernel requirement is

$$
\mathcal E_{\mathrm{shift}}^{\mathrm{req}}
\ll
\mathcal A_{\min}Q_0^2\min(H,Q_0^2)\log Q_0.
$$

Since

$$
\min(H,Q_0^2)\le Q_0^2
$$

and

$$
\mathcal A_{\min}\le X(\log X)^C,
$$

we have

$$
\mathcal E_{\mathrm{shift}}^{\mathrm{req}}
\ll
XQ_0^4(\log X)^C.
$$

In the kernel-length regime above,

$$
\mathcal E_{\mathrm{tot}}
\gg
X^{3/2}Q_0^8(\log X)^C,
$$

so the shift-kernel payment is lower order and can be reserved inside
`E_tot`.

## Gate 4: Major-Window Budget

The major-window requirement is

$$
\mathcal E_{\mathrm{maj}}^{\mathrm{req}}
\ll
\mathcal A_2{Q_0^4\over(\log X)^2}.
$$

Using

$$
\mathcal A_2\le X(\log X)^C
$$

gives

$$
\mathcal E_{\mathrm{maj}}^{\mathrm{req}}
\ll
XQ_0^4(\log X)^C.
$$

This is also lower order relative to the band-side allowance in the stated
kernel-length regime.

## Total Split

The total budget split is

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

The band term is the dominant term. Under

$$
N\ge X^{1/4}Q_0^4(\log X)^C,
$$

the right side is bounded by the available completion allowance after choosing
the logarithmic constants in the major-radius, smoothing, and Gram estimates.

## Literal Closure Statement

> **Polylog Literal Direct Full-Radius BDH Closure.**  
> In the regime
> \[
> Q_0=(\log X)^B,\quad B\le1/2-\varepsilon,\quad
> N\ge X^{1/4}Q_0^4(\log X)^C,
> \]
> with residual energy envelopes
> \[
> \mathcal A_2,\mathcal A_{\min}\le X(\log X)^C
> \]
> and Siegel-Walfisz major validity on
> `|beta| <= c1 Q0^-2`, the four scalar budget/radius gates all hold. Hence
> the Direct Full-Radius BDH Assembly closes by literal support removal.

## Packet-Frame Fallback

If either

$$
N<X^{1/4}Q_0^4(\log X)^C
$$

or one of the residual energy envelopes fails, the literal route must be
replaced by the Unified Packet-Frame Source theorem:

$$
\|(1-P_{\mathrm{maj}})w_{N,L}\|_2^2
\le
\Delta_L\|w_{N,L}\|_2^2,
$$

$$
\|(1-P_{\mathrm{maj}})\Omega_N\|_1
\le
{\mathcal E_{\mathrm{shift}}\over
\mathcal S(Q_0,H,\rho_{\max})\mathcal A_{\min}},
$$

and

$$
\left(
X\mathfrak C_{\mu^\perp}(1/X)+\mu^\perp([0,1])
\right)\mathcal A_2
\le
(\log X)^2\mathcal E_{\mathrm{maj}}.
$$

The first condition supplies the below-threshold Type II saving

$$
\overline{\Delta}
\ll
{N^2\over X^{1/2}Q_0^8(\log X)^C}.
$$

## Result

The direct full-radius BDH route is closed in the stated polylogarithmic
literal regime. Outside that regime, the remaining obligation is not another
budget rearrangement; it is the Unified Packet-Frame Source theorem with the
three simultaneous residual bounds above.
