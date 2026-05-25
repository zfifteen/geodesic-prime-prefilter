# Polylog Completion Parameter Assignment

Date: 2026-05-24

Status: explicit parameter assignment for the polylogarithmic literal closure
of the Direct Full-Radius BDH Assembly.

The literal closure needs:

$$
Q_0=(\log X)^B,\qquad B<1/2,
$$

residual energy envelopes

$$
\mathcal A_2,\mathcal A_{\min}\le X(\log X)^C,
$$

kernel length

$$
N\ge X^{1/4}Q_0^4(\log X)^C,
$$

and Poisson allowance

$$
\mathcal E_{\mathrm{tot}}
\asymp
X\left({N\over\log X}\right)^2(\log X)^{-A_0}.
$$

This note gives one concrete assignment.

## Assignment

Fix

$$
B={1\over4}
$$

for definiteness, so

$$
Q_0=(\log X)^{1/4}.
$$

Choose

$$
N=X^{1/4}Q_0^4(\log X)^{C_N}
=
X^{1/4}(\log X)^{1+C_N},
$$

with `C_N` large enough to absorb the logged losses in the Type II band
estimate, smoothing tails, and major-arc error terms.

This is an admissible interval-kernel length for large `X` because

$$
1\ll N\ll X.
$$

Assign fixed shares of the Poisson allowance:

$$
\mathcal E_{\mathrm{band}}^{\mathrm{alloc}}={1\over2}\mathcal E_{\mathrm{tot}},
\qquad
\mathcal E_{\mathrm{shift}}={1\over8}\mathcal E_{\mathrm{tot}},
\qquad
\mathcal E_{\mathrm{maj}}={1\over8}\mathcal E_{\mathrm{tot}},
$$

and reserve the remaining allowance for `E_tail`.

## Band Gate

The Type II band requirement is

$$
\mathcal E_{\mathrm{band}}^{\mathrm{req}}
\ll
X^{3/2}Q_0^8(\log X)^C.
$$

With the assigned `N`,

$$
\mathcal E_{\mathrm{tot}}
\asymp
X\left({N\over\log X}\right)^2(\log X)^{-A_0}
\gg
X^{3/2}Q_0^8(\log X)^C
$$

after increasing `C_N`. Hence

$$
\mathcal E_{\mathrm{band}}^{\mathrm{alloc}}
\ge
\mathcal E_{\mathrm{band}}^{\mathrm{req}}.
$$

Thus

$$
L_{\mathrm{crit}}\ge C Q_0^2.
$$

## Shift Gate

Using

$$
\mathcal A_{\min}\le X(\log X)^C,
\qquad
\min(H,Q_0^2)\le Q_0^2,
$$

the shift requirement is

$$
\mathcal E_{\mathrm{shift}}^{\mathrm{req}}
\ll
XQ_0^4(\log X)^C.
$$

The assigned Poisson allowance satisfies

$$
\mathcal E_{\mathrm{shift}}
\asymp
\mathcal E_{\mathrm{tot}}
\gg
X^{3/2}Q_0^8(\log X)^C,
$$

so

$$
\mathcal E_{\mathrm{shift}}
\ge
\mathcal E_{\mathrm{shift}}^{\mathrm{req}}.
$$

## Major-Window Gate

Using

$$
\mathcal A_2\le X(\log X)^C,
$$

the major-window requirement is

$$
\mathcal E_{\mathrm{maj}}^{\mathrm{req}}
\ll
XQ_0^4(\log X)^C.
$$

Again

$$
\mathcal E_{\mathrm{maj}}
\asymp
\mathcal E_{\mathrm{tot}}
\gg
X^{3/2}Q_0^8(\log X)^C,
$$

so

$$
\mathcal E_{\mathrm{maj}}
\ge
\mathcal E_{\mathrm{maj}}^{\mathrm{req}}.
$$

## Major Radius And Frame

Since `Q0` is polylogarithmic, Siegel-Walfisz supplies

$$
\rho_{\mathrm{valid}}^0\ge c_1Q_0^{-2}.
$$

The frame condition is

$$
Q_0^4\ll X,
$$

which is immediate for

$$
Q_0=(\log X)^{1/4}.
$$

Amplitude errors and Gram leakage are absorbed into `E_tail` by choosing the
Siegel-Walfisz saving exponent and `C_N` large enough.

## Closure

With the assignment above:

$$
R_{\mathrm{all}}
\le
\min(\rho_{\mathrm{valid}}^0,c_1Q_0^{-2}),
$$

and the four scalar gates all hold. Therefore the Direct Full-Radius BDH
Assembly closes by literal support removal for this admissible polylogarithmic
parameter regime.

## Boundary

This assignment closes the direct route when the RH bridge permits choosing
the interval-kernel length at or above

$$
N=X^{1/4}Q_0^4(\log X)^C.
$$

If the bridge fixes a shorter kernel length, the literal route fails at the
Type II band budget and the Unified Packet-Frame Source theorem must supply

$$
\overline{\Delta}
\ll
{N^2\over X^{1/2}Q_0^8(\log X)^C}.
$$

## Result

The PGS completion machinery admits an explicit polylogarithmic literal
assignment:

$$
Q_0=(\log X)^{1/4},
\qquad
N=X^{1/4}(\log X)^{1+C_N}.
$$

Under the standard residual energy envelopes and Siegel-Walfisz major
validity, this assignment pays the kernel-band, shift-kernel, major-window,
and tail budgets inside the convolution-scale Poisson allowance.
