# Polylog Literal Closure Input Verification

Date: 2026-05-24

Status: verification ledger for the inputs used by the Polylog Literal Direct
Full-Radius BDH Closure.

The literal closure theorem uses four final inputs:

$$
\mathcal A_2\le X(\log X)^C,
\qquad
\mathcal A_{\min}\le X(\log X)^C,
$$

$$
N\ge X^{1/4}Q_0^4(\log X)^C,
$$

$$
\mathcal E_{\mathrm{tot}}
\asymp
X\left({N\over\log X}\right)^2(\log X)^{-A_0},
$$

and

$$
\rho_{\mathrm{valid}}^0\ge c_1Q_0^{-2}.
$$

This note identifies how each input is verified or where it remains a real
bridge parameter.

## Residual Coefficient Energy `A_2`

The coefficient-level major projection gives

$$
a^{\perp}=(1-P_{\mathrm{maj}})a.
$$

For the low-conductor frame in the polylogarithmic regime,

$$
\|1-P_{\mathrm{maj}}\|_{2\to2}\ll 1.
$$

Therefore

$$
\mathcal A_2
=
\|a^{\perp}\|_2^2
\ll
\|a\|_2^2.
$$

For endpoint-normalized von Mangoldt or centered endpoint coefficients on
`X<n<=2X`,

$$
\|a\|_2^2\ll X(\log X)^C.
$$

Thus

$$
\mathcal A_2\le X(\log X)^C.
$$

The remaining bookkeeping input is the exact endpoint normalization used in
the bridge.

## Residual Minor Mass `A_min`

The residual minor mass is an `L2` mass of the same projected endpoint
coefficient sequence on the minor side. By Parseval and projection
boundedness,

$$
\mathcal A_{\min}
\le
\|a^{\perp}\|_2^2
\ll
X(\log X)^C.
$$

Thus

$$
\mathcal A_{\min}\le X(\log X)^C.
$$

This is automatic once `A_min` is defined as a residual minor `L2` mass and
not as a stronger pointwise norm.

## Completion Allowance `E_tot`

The completion framework assigns the convolution-scale Poisson allowance

$$
\mathcal E_{\mathrm{tot}}
\asymp
X\left({N\over\log X}\right)^2(\log X)^{-A_0}.
$$

This is the endpoint four-energy Poisson scale after the main term,
trivial-zero terms, coherent major packets, diagonal terms, and singular
terms have been removed.

The required verification is not a new inequality; it is a normalization
contract: the same `N`, endpoint coefficient normalization, and smoothing
used in the Type II band calculation must be used in the Poisson allowance.

## Kernel Length Threshold

The literal Type II band budget closes when

$$
N\ge X^{1/4}Q_0^4(\log X)^C.
$$

This is the one input that depends on the RH bridge scale. If the folded
completion kernel has this length, the literal band route closes. If the
bridge requires shorter kernels, literal support removal fails at the Type II
band budget and the packet-frame theorem must supply

$$
\overline{\Delta}
\ll
{N^2\over X^{1/2}Q_0^8(\log X)^C}.
$$

## Major Validity Radius

For

$$
Q_0=(\log X)^B
$$

with fixed `B`, Siegel-Walfisz gives for every `A`

$$
E_q(X)\ll_A X(\log X)^{-A}
$$

uniformly for `q<=Q0`. After endpoint normalization and summation over
`O(Q0^2)` centers, the major packet error on

$$
|\beta|\le c_1Q_0^{-2}
$$

is absorbed into `E_tail`. Therefore

$$
\rho_{\mathrm{valid}}^0\ge c_1Q_0^{-2}.
$$

This is an external analytic major-arc input, not a local theorem from
`PROOF.md`.

## Fallback

If the endpoint normalization, kernel length, or Poisson allowance does not
match the literal regime, the direct route must use the Unified Packet-Frame
Source theorem:

$$
\|(1-P_{\mathrm{maj}})w_{N,L}\|_2^2
\le
\Delta_L\|w_{N,L}\|_2^2,
$$

$$
\|(1-P_{\mathrm{maj}})\Omega_N\|_1
\le
{\mathcal E_{\mathrm{shift}}\over
\mathcal S\mathcal A_{\min}},
$$

and

$$
\left(
X\mathfrak C_{\mu^\perp}(1/X)+\mu^\perp([0,1])
\right)\mathcal A_2
\le
(\log X)^2\mathcal E_{\mathrm{maj}}.
$$

## Result

The residual energy envelopes follow from projection boundedness, Parseval,
and endpoint coefficient normalization. The major radius follows from
Siegel-Walfisz in the polylogarithmic conductor range. The completion
allowance is the Poisson-scale normalization contract. The only remaining
literal-route bridge parameter is the kernel length condition

$$
N\ge X^{1/4}Q_0^4(\log X)^C.
$$

If that condition fails, the packet-frame `Delta_L` estimate is the necessary
replacement.
