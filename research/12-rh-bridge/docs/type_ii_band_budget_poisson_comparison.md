# Type II Band Budget Versus Poisson Allowance

Date: 2026-05-24

Status: comparison of the explicit Type II band payment with the
convolution-scale Poisson allowance.

The Type II band calculation gives

$$
\mathcal E_{\mathrm{band,TypeII}}^{\mathrm{req}}
\ll
X^{3/2}Q_0^8(\log X)^C.
$$

The kernel-band completion framework uses the convolution-scale Poisson
allowance

$$
\mathcal E_{\mathrm{Pois}}
\asymp
X\left({N\over\log X}\right)^2(\log X)^{-A_0},
$$

where `N` is the interval-kernel length in `K_N`.

## Literal Budget Comparison

The literal Type II band payment fits inside the Poisson allowance if

$$
X\left({N\over\log X}\right)^2(\log X)^{-A_0}
\ge
C X^{3/2}Q_0^8(\log X)^C.
$$

Equivalently,

$$
N^2
\ge
C X^{1/2}Q_0^8(\log X)^{C+A_0+2}.
$$

Thus a sufficient kernel-length condition is

$$
N
\ge
C X^{1/4}Q_0^4(\log X)^{C'}.
$$

For `Q0=(log X)^B`, this becomes

$$
N\ge X^{1/4}(\log X)^{4B+C'}.
$$

## Literal Closure Regime

In the range

$$
N\ge X^{1/4}Q_0^4(\log X)^{C'},
$$

the Type II kernel-band payment is compatible with the Poisson allowance,
subject to the already reserved shift, major-window, and tail budgets. The
literal branch then has no remaining Type II band-size obstruction.

## Required Packet-Frame Saving Below The Threshold

If

$$
N<X^{1/4}Q_0^4(\log X)^{C'},
$$

the literal Type II band payment exceeds the Poisson allowance. The required
average projected band saving is

$$
\overline{\Delta}
\le
{ \mathcal E_{\mathrm{Pois}}
\over
X^{3/2}Q_0^8(\log X)^C}
\ll
{N^2\over X^{1/2}Q_0^8(\log X)^{C+A_0+2}}.
$$

The slice-level condition remains

$$
\sum_{A,B,d,L\le Q_0^2}
\Delta_L L^3\mathfrak L_{A,B,d,L}
\le
\mathcal E_{\mathrm{band}}^{\mathrm{alloc}}.
$$

## Final Inputs

This comparison closes after the project fixes:

1. the kernel length `N` in the RH bridge application;
2. the conductor exponent `B` in `Q0=(log X)^B`;
3. the exact logarithmic loss `C'`;
4. the share of Poisson allowance allocated to the band side after shift,
   major-window, and tail reserves;
5. if below threshold, the packet-frame saving profile `Delta_L`.

## Result

The explicit Type II band payment is compatible with the Poisson allowance
whenever

$$
N\ge X^{1/4}Q_0^4(\log X)^{C'}.
$$

Below that kernel-length threshold, the literal route fails on the Type II
band budget and the Unified Packet-Frame Source theorem must provide average
saving

$$
\overline{\Delta}
\ll
{N^2\over X^{1/2}Q_0^8(\log X)^{C'}}.
$$
