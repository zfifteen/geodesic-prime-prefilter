# Direct Route Literal Support Closure Plan

Date: 2026-05-24

Status: top-level closure plan for the direct full-radius BDH route, with the
packet-frame alternative identified.

The direct route closes the major-aperture side if the literal support
condition

$$
R_{\mathrm{all}}
\le
\min(\rho_{\mathrm{valid}}^{0}(c),c_1Q_0^{-2})
$$

holds after noncircular budget assignment.

## Literal Support Route

The proof chain is:

1. choose `Q_0`, external `rho_valid^0`, and budgets `E_maj,E_shift`;
2. prove low-conductor frame conditioning;
3. prove amplitude reproduction by PNT-in-AP or zero-density input;
4. construct coefficient-level residual `a^perp`;
5. bound residual energy `A_2`;
6. use measure concentration after core removal;
7. choose
   $$
   R_{\mathrm{all}}=\max(c_0/L_{\mathrm{crit}},M_{\Omega}^{-1},R_{\mathrm{LS}});
   $$
8. verify
   $$
   R_{\mathrm{all}}\le\min(\rho_{\mathrm{valid}}^{0},c_1Q_0^{-2});
   $$
9. apply the direct continuous-frequency large sieve.

Then the kernel-weighted maximal BDH estimate at `R_all` follows.

## What This Closes

The direct route closes:

$$
\text{Full-Radius Major Validity}
\Rightarrow
\text{Full Unified Major Aperture}
\Rightarrow
\text{kernel-band completion-energy control}
\Rightarrow
\text{projected reciprocal-congruence major side}.
$$

It supplies the major-aperture and kernel-weighted BDH part of the projected
reciprocal-congruence route.

## Remaining Literal-Route Gaps

The literal route still requires quantitative verification of:

1. `Budget-Radius Feasibility Lemma`;
2. `Frame-Amplitude Closure Lemma`;
3. residual coefficient energy `A_2` in the chosen endpoint normalization;
4. completion-side quantities defining `L_crit`, `M_Omega`, and `R_LS`.

These are parameter and estimate checks, not new structural reductions.

## Packet-Frame Alternative

If

$$
R_{\mathrm{all}}>
\min(\rho_{\mathrm{valid}}^{0},c_1Q_0^{-2}),
$$

literal support apertures fail. The replacement is a packet-frame theorem
that directly proves:

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

This avoids literal support containment by proving energy capture directly.

## Minimal Closure Statement

> **Direct Route Literal Support Closure.**  
> The direct full-radius BDH route closes if the budget/radius assignment,
> low-conductor frame conditioning, amplitude reproduction, residual energy,
> and measure concentration estimates all hold. If the radius condition fails,
> a packet-frame theorem must replace support removal by direct residual
> energy, mass, and concentration bounds.

## Result

The direct route is now a finite checklist. The remaining work is to verify
the quantitative estimates in the chosen `Q_0` and budget regime. If that
check fails, the project must switch to the packet-frame alternative rather
than restating the literal aperture route.
