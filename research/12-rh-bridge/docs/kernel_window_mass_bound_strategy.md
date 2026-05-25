# Kernel Window Mass Bound Strategy

Date: 2026-05-24

Status: candidate strategy for bounding `||Omega_N||_1` in the
Post-Variation Shift-Kernel Closure Lemma.

The scalar closure condition is

$$
\|\Omega_N\|_1
\mathcal S(Q_0,H,\rho_{\max})
\mathcal A_{\mathrm{min}}
\le
\mathcal E_{\mathrm{shift}}.
$$

Thus the kernel-window mass must satisfy

$$
\|\Omega_N\|_1
\le
{\mathcal E_{\mathrm{shift}}
\over
\mathcal S(Q_0,H,\rho_{\max})\mathcal A_{\mathrm{min}}}.
$$

## Kernel Mass

The projected aperture weight has mass bounded by

$$
\|\Omega_N\|_1
\le
\int_{\operatorname{supp}\Omega_N}
|K_N(c+\beta)|^2\,d\beta.
$$

Using

$$
|K_N(\alpha)|\ll \min(N,\|\alpha\|^{-1}),
$$

this becomes a support-measure problem.

## Centered Peak Bound

If the aperture window is centered on a kernel peak, the crude mass is

$$
\int_{|\beta|\le\rho}
\min(N^2,\|\beta\|^{-2})\,d\beta
\ll
\min(N^2\rho,N).
$$

This is the largest possible local kernel mass.

## Off-Peak Bound

If the center `c` is separated from the integer lattice by `delta_c` on the
window,

$$
\|c+\beta\|\ge \delta_c,
\qquad |\beta|\le\rho,
$$

then

$$
\|\Omega_N\|_1
\ll
\rho\,\min(N^2,\delta_c^{-2}).
$$

This is much smaller when the packet center is not near a kernel peak.

## Aperture-Core Removal

If the major projector removes the core

$$
|\beta|\le\rho_{\mathrm{core}},
$$

then the residual annular mass satisfies

$$
\int_{\rho_{\mathrm{core}}\le|\beta|\le\rho}
\min(N^2,\|\beta\|^{-2})\,d\beta
\ll
\min(N^2\rho,N,{1\over\rho_{\mathrm{core}}}).
$$

Thus major-aperture removal can reduce the mass from peak scale `N` to tail
scale `rho_core^{-1}`.

## Projection-Energy Alternative

If `P_maj` is an orthogonal projector rather than literal support removal,
the projected weight can be signed. In that case use

$$
\|\Omega_N^{\perp}\|_1
\le
|\operatorname{supp}\Omega_N|^{1/2}
\|\Omega_N^{\perp}\|_2.
$$

The needed input is then an `L^2` projection-energy saving for the aperture
weight, not pointwise support removal.

## Required Inputs

The mass bound needs:

1. the support of the projected aperture weight;
2. whether the packet center is on-peak or off-peak for `K_N`;
3. the major core radius removed by support aperture;
4. or an `L^2` projection-energy estimate for `Omega_N^perp`;
5. comparison with the target
   `E_shift / (S A_min)`.

## Minimal Lemma

> **Projected Kernel Window Mass Lemma.**  
> The projected aperture weight satisfies
> \[
> \|\Omega_N\|_1
> \le
> {\mathcal E_{\mathrm{shift}}
> \over
> \mathcal S(Q_0,H,\rho_{\max})\mathcal A_{\mathrm{min}}},
> \]
> by either literal support removal of the kernel peak core or an
> orthogonal-projection `L^2` energy saving.

## Result

The kernel-window mass is controlled by where the projected aperture support
sits relative to the interval-kernel peak. Removing the high-mass core is the
direct way to make `||Omega_N||_1` small enough for the post-variation
shift-kernel closure inequality.
