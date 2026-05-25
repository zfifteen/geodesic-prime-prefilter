# Direct Full-Radius BDH Closure Certificate

Date: 2026-05-24

Status: closure certificate for the Direct Full-Radius BDH Assembly in the
explicit polylogarithmic literal regime.

This certificate records the completed assignment:

$$
Q_0=(\log X)^{1/4},
\qquad
N=X^{1/4}(\log X)^{1+C_N}.
$$

The constant `C_N` is chosen large enough to absorb the logged losses in the
Type II band estimate, smoothing tails, Gram leakage, and major-arc error.

## Certificate Table

| Gate | Required input | Verification |
| --- | --- | --- |
| Frame | `Q0^4 << X` | immediate from `Q0=(log X)^(1/4)` |
| Major radius | `rho_valid^0 >= c1 Q0^-2` | Siegel-Walfisz for `q <= Q0` |
| Amplitude | total packet error inside `E_tail` | Siegel-Walfisz with large saving exponent |
| Residual energy | `A_2 <= X log^C X` | bounded projection plus endpoint `L2` norm |
| Minor residual mass | `A_min <= X log^C X` | Parseval and bounded projection |
| Type II band | `E_band^alloc >= X^(3/2)Q0^8 log^C X` | follows from assigned `N` and `E_tot` |
| Shift kernel | `E_shift >= A_min Q0^2 min(H,Q0^2)log Q0` | lower order than `E_tot` |
| Major window | `E_maj >= A_2 Q0^4/log^2 X` | lower order than `E_tot` |
| Total split | band + shift + major + tail `<= E_tot` | fixed budget shares with `C_N` large |

## Budget Scale

With the assigned kernel length,

$$
\mathcal E_{\mathrm{tot}}
\asymp
X\left({N\over\log X}\right)^2(\log X)^{-A_0}
\gg
X^{3/2}Q_0^8(\log X)^C.
$$

The Type II band term is dominant. The shift and major-window terms satisfy

$$
\mathcal E_{\mathrm{shift}}^{\mathrm{req}},
\mathcal E_{\mathrm{maj}}^{\mathrm{req}}
\ll
XQ_0^4(\log X)^C,
$$

so both are lower order.

## Closure Consequence

The unified radius satisfies

$$
R_{\mathrm{all}}
\le
\min(\rho_{\mathrm{valid}}^0,c_1Q_0^{-2}).
$$

Therefore the full literal support-removal route closes:

$$
\text{Direct continuous-frequency large sieve}
\Rightarrow
\text{Full-Radius Major Validity}
\Rightarrow
\text{Full Unified Major Aperture}
\Rightarrow
\text{kernel-band completion-energy control}.
$$

This supplies the direct full-radius BDH input needed by the projected
reciprocal-congruence route in the stated regime.

## Boundary

The certificate depends on the bridge permitting the assigned kernel length

$$
N=X^{1/4}(\log X)^{1+C_N}.
$$

If the RH bridge fixes a shorter kernel, the literal certificate does not
apply. The remaining obligation is then the Unified Packet-Frame Source
theorem, with average saving

$$
\overline{\Delta}
\ll
{N^2\over X^{1/2}Q_0^8(\log X)^C}.
$$

## Result

The Direct Full-Radius BDH Assembly is closed by literal support removal in
the explicit polylogarithmic regime above. The only direct-route boundary is
kernel-length admissibility; below that boundary, the packet-frame theorem is
the required replacement.
