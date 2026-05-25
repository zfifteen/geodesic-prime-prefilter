# Full Unified Major Aperture Verification Strategy

Date: 2026-05-24

Status: master verification strategy for the literal major-aperture route and
its packet-frame alternative.

The combined aperture demand is

$$
R_{\mathrm{all}}
=
\max\left(
{c_0\over L_{\mathrm{crit}}(d,N)},
M_{\Omega}^{-1},
R_{\mathrm{LS}}
\right).
$$

The literal support route closes if

$$
R_{\mathrm{all}}
\le
\min(\rho_{\mathrm{valid}}(c),c_1Q_0^{-2})
$$

for every relevant low-conductor center `c` and failing dyadic slice.

## What `R_all` Covers

The three terms have distinct jobs.

**`c0/L_crit`.**
Removes high-`L` kernel bands whose base energy does not fit the Completion
Energy Bound.

**`M_Omega^{-1}`.**
Removes the kernel peak core so the shift-kernel threshold closure has
`||Omega_N||_1` small enough.

**`R_LS`.**
Removes the kernel peak core far enough that the direct continuous-frequency
large-sieve measure concentration satisfies the major-window budget.

## Verification Procedure

For each relevant center `c`:

1. compute `L_crit(d,N)` from the Completion Energy Bound;
2. compute `M_Omega=E_shift/(S A_min)`;
3. compute `R_LS` from `A_2`, `E_maj`, and `B_ov`;
4. form `R_all`;
5. verify rational separation:
   $$
   R_{\mathrm{all}}\le c_1Q_0^{-2};
   $$
6. verify major validity:
   $$
   R_{\mathrm{all}}\le \rho_{\mathrm{valid}}(c).
   $$

The major validity step is proved by pointwise PNT-in-AP/zero-density input
or by the unified-scale kernel-weighted BDH theorem.

## Literal Route Closure

If the two inequalities hold, the following chain closes:

$$
\text{major aperture}
\Rightarrow
\text{kernel-band energy control}
\Rightarrow
\text{shift-kernel mass control}
\Rightarrow
\text{direct weighted large sieve}
\Rightarrow
\text{kernel-weighted BDH at }R_{\mathrm{all}}.
$$

This closes the averaged major-validity side of the projected reciprocal
congruence route.

## Packet-Frame Alternative

If `R_all` exceeds the valid or separated aperture radius, literal support
removal fails. The replacement is a packet-frame theorem that proves all
three residual bounds directly:

$$
\|(1-P_{\mathrm{maj}})w_{N,L}\|_2^2
\le
\Delta_L\|w_{N,L}\|_2^2,
$$

$$
\|(1-P_{\mathrm{maj}})\Omega_N\|_1
\le
M_{\Omega},
$$

and

$$
X\mathfrak C_{\mu^{\perp}}(1/X)+\mu^{\perp}([0,1])
\le
{(\log X)^2\mathcal E_{\mathrm{maj}}\over\mathcal A_2}.
$$

This frame theorem can replace support removal without requiring literal
apertures of radius `R_all`.

## Minimal Lemma

> **Full Unified Major Aperture Lemma.**  
> For every relevant low-conductor center and failing dyadic slice, either
> \[
> R_{\mathrm{all}}
> \le
> \min(\rho_{\mathrm{valid}}(c),c_1Q_0^{-2}),
> \]
> or the major packet frame satisfies the three residual bounds for band
> energy, kernel-window mass, and weighted-measure concentration.

## Result

The literal major-aperture route is now a single radius inequality. The
packet-frame route is the only alternative if the required aperture radius is
too large for major validity or rational separation.
