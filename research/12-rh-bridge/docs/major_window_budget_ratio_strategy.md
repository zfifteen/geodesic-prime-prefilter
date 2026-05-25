# Major-Window Budget Ratio Strategy

Date: 2026-05-24

Status: focused strategy for verifying the major-window lower bound
`E_maj / A_2 >= C Q0^4 / log^2 X`, or the corresponding measure
concentration replacement after packet projection.

The major-window branch is the direct continuous-frequency large-sieve step.
After coefficient-level major projection, the residual endpoint sum

$$
A^{\perp}(\alpha)
=
\sum_n a_n^{\perp}e(n\alpha)
$$

is integrated against the kernel-weighted major-window measure.

## Direct Large-Sieve Condition

The direct large sieve gives

$$
\int |A^{\perp}(\alpha)|^2\,d\mu(\alpha)
\le
\left(
X\mathfrak C_{\mu}(1/X)+\mu([0,1])
\right)\mathcal A_2.
$$

The budget condition is

$$
\left(
X\mathfrak C_{\mu}(1/X)+\mu([0,1])
\right)\mathcal A_2
\le
(\log X)^2\mathcal E_{\mathrm{maj}}.
$$

Thus the source task is to bound the operator constant

$$
\mathcal L_{\mu}
=
X\mathfrak C_{\mu}(1/X)+\mu([0,1]).
$$

## Literal Core-Removal Concentration

In the literal branch, rational windows have bounded overlap:

$$
B_{\mathrm{ov}}=O(1),
$$

because

$$
R_{\mathrm{all}}\le c_1Q_0^{-2}.
$$

The major projector removes the kernel core to radius

$$
\rho_{\mathrm{core}}\asymp Q_0^{-2}.
$$

On the residual support,

$$
|K_N(\alpha)|^2\ll \rho_{\mathrm{core}}^{-2}\ll Q_0^4.
$$

The total residual mass satisfies

$$
\mu([0,1])
\ll
B_{\mathrm{ov}}\rho_{\mathrm{core}}^{-1}
\ll
Q_0^2,
$$

and local `1/X` concentration satisfies

$$
\mathfrak C_{\mu}(1/X)
\ll
{B_{\mathrm{ov}}\over X\rho_{\mathrm{core}}^2}
\ll
{Q_0^4\over X}.
$$

Therefore

$$
\mathcal L_{\mu}
\ll
Q_0^4+Q_0^2
\ll
Q_0^4.
$$

Substitution into the direct large-sieve condition gives

$$
{\mathcal E_{\mathrm{maj}}\over \mathcal A_2}
\ge
C_M{Q_0^4\over(\log X)^2}.
$$

This is the required major-window budget ratio.

## Residual Energy Source

The frame projection gives

$$
\mathcal A_2
=
\|(1-P_{\mathrm{maj}})a\|_2^2
\le
C_A\|a\|_2^2.
$$

The endpoint normalization must specify the exact scale of `||a||_2^2`. The
budget ratio is meaningful only after that normalization is fixed. In the
polylog literal route, no sharper `A_2` estimate is required unless the
available major budget is smaller than the threshold above.

## Packet-Projection Measure Replacement

If core support removal fails, the replacement is a direct concentration
theorem for the projected residual measure `mu^perp`:

$$
\left(
X\mathfrak C_{\mu^\perp}(1/X)+\mu^\perp([0,1])
\right)\mathcal A_2
\le
(\log X)^2\mathcal E_{\mathrm{maj}}.
$$

A sufficient pair of estimates is

$$
\mu^\perp([0,1])
\le
M_{\mu},
$$

and

$$
\mathfrak C_{\mu^\perp}(1/X)
\le
{C_{\mu}\over X},
$$

with

$$
(C_{\mu}+M_{\mu})\mathcal A_2
\le
(\log X)^2\mathcal E_{\mathrm{maj}}.
$$

This packet-projection theorem replaces the geometric concentration estimate
`rho_core^{-2}+rho_core^{-1}` by direct residual measure concentration.

## Final Major-Window Inputs

The major-window source closes after the following quantities are fixed:

1. the coefficient-level residual sequence `a^perp`;
2. the residual energy `A_2`;
3. the exact endpoint normalization for `a`;
4. the major-window measure `mu`;
5. bounded overlap `B_ov`;
6. the core radius removed by the major projector;
7. the total mass and local concentration bounds for `mu`;
8. the assigned major-window budget `E_maj`;
9. if literal support fails, the projected measure concentration bounds for
   `mu^perp`.

## Result

The major-window branch has one budget-ratio test:

$$
{\mathcal E_{\mathrm{maj}}\over\mathcal A_2}
\ge
C_M{Q_0^4\over(\log X)^2}.
$$

Literal core removal proves the operator constant
`L_mu << Q0^4`. If this concentration cannot be obtained geometrically, the
packet-frame alternative must prove the same direct large-sieve operator
bound for the projected residual measure `mu^perp`.
