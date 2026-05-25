# Aperture-Core Removal Mass Strategy

Date: 2026-05-24

Status: candidate strategy for proving the kernel-window mass bound by
removing the high-mass core of the interval-kernel peak.

The Projected Kernel Window Mass Lemma requires

$$
\|\Omega_N\|_1
\le
M_{\Omega},
\qquad
M_{\Omega}
=
{\mathcal E_{\mathrm{shift}}
\over
\mathcal S(Q_0,H,\rho_{\max})\mathcal A_{\mathrm{min}}}.
$$

## Core Removal Geometry

Assume the projected support excludes the core

$$
|\beta|<\rho_{\mathrm{core}}
$$

around a kernel peak. Then

$$
\|\Omega_N\|_1
\le
\int_{\rho_{\mathrm{core}}\le|\beta|\le\rho}
\min(N^2,\|\beta\|^{-2})\,d\beta.
$$

This gives

$$
\|\Omega_N\|_1
\ll
\min\left(N^2\rho,\ N,\ {1\over\rho_{\mathrm{core}}}\right).
$$

The unremoved peak mass is at most `min(N^2 rho, N)`. Core removal is needed
only when this exceeds `M_Omega`.

## Required Core Radius

If the tail term controls the mass, it is enough to require

$$
{1\over\rho_{\mathrm{core}}}
\le
M_{\Omega}.
$$

Equivalently,

$$
\rho_{\mathrm{core}}
\ge
{1\over M_{\Omega}}.
$$

Thus the aperture-core removal condition is

$$
{1\over M_{\Omega}}
\le
\rho_{\mathrm{core}}
\le
\min(\rho_{\mathrm{valid}},cQ_0^{-2}).
$$

The upper bound keeps the removed core inside valid and disjoint major
apertures.

## Support-Removal Route

Literal support removal closes the mass bound if the major projector removes

$$
|\beta|<\rho_{\mathrm{core}}
$$

with

$$
\rho_{\mathrm{core}}\ge M_{\Omega}^{-1}.
$$

Then

$$
\|\Omega_N\|_1\ll M_{\Omega}
$$

up to smoothing tails.

## Projection-Energy Route

If literal support removal cannot reach `rho_core`, an orthogonal projection
can still work. It must prove

$$
\|\Omega_N^{\perp}\|_1
\le M_{\Omega}.
$$

A sufficient `L^2` statement is

$$
\|\Omega_N^{\perp}\|_2
\le
{M_{\Omega}\over |\operatorname{supp}\Omega_N|^{1/2}}.
$$

This is the projection-energy replacement for core support removal.

## Minimal Lemma

> **Aperture-Core Mass Lemma.**  
> The major projector removes the kernel peak core out to a radius
> `rho_core` satisfying
> \[
> {1\over M_{\Omega}}
> \le
> \rho_{\mathrm{core}}
> \le
> \min(\rho_{\mathrm{valid}},cQ_0^{-2}),
> \]
> or else the orthogonal projection residual satisfies
> \[
> \|\Omega_N^{\perp}\|_1\le M_{\Omega}.
> \]

## Result

The mass bound is now a direct aperture-radius condition. If the major
projector removes the peak core to radius at least `1/M_Omega`, the remaining
annular tail has enough mass decay for the post-variation shift-kernel
closure inequality.
