# Unified Major Aperture Radius Verification

Date: 2026-05-24

Status: consolidated radius check for major-aperture removal and
kernel-window mass control.

Two independent demands require major-aperture radius:

1. failing high-`L` bands need
   $$
   \rho_c\ge {c_0\over L_{\mathrm{crit}}(d,N)};
   $$
2. kernel peak core removal needs
   $$
   \rho_c\ge M_{\Omega}^{-1}.
   $$

These combine into one required radius.

## Required Radius

For a relevant packet center `c`, define

$$
R_{\mathrm{req}}(c,d,N)
=
\max\left(
{c_0\over L_{\mathrm{crit}}(d,N)},
M_{\Omega}^{-1}
\right).
$$

The literal aperture route requires

$$
R_{\mathrm{req}}(c,d,N)
\le
\rho_c
\le
\min(\rho_{\mathrm{valid}}(c),c_1Q_0^{-2}).
$$

Thus it closes exactly when

$$
R_{\mathrm{req}}(c,d,N)
\le
\min(\rho_{\mathrm{valid}}(c),c_1Q_0^{-2})
$$

for every relevant peak center and failing dyadic slice.

## Major Validity Check

The major validity radius must be proved at the combined scale:

$$
\rho_{\mathrm{valid}}(c)\ge R_{\mathrm{req}}(c,d,N).
$$

In AP-error terms, this asks for

$$
{E_q(X)^2\over(\log X)^2}
I_N(c,R_{\mathrm{req}})
\le
\mathcal E_{c,N}.
$$

This is the same major-radius theorem as before, evaluated at the larger of
the band-removal and mass-removal radii.

## Rational Separation Check

The same required radius must respect packet separation:

$$
R_{\mathrm{req}}(c,d,N)
\le
c_1Q_0^{-2}.
$$

If this fails, literal support apertures overlap too much. The route must use
a packet-frame projection rather than disjoint support removal.

## Packet-Frame Alternative

If the literal radius condition fails, the frame route must prove both:

$$
\|(1-P_{\mathrm{maj}})w_{N,L}\|_2^2
\le
\Delta_L\|w_{N,L}\|_2^2
$$

for failing high-`L` band energy, and

$$
\|(1-P_{\mathrm{maj}})\Omega_N\|_1
\le
M_{\Omega}
$$

for kernel-window mass.

This is a stronger projection theorem but avoids literal radius containment.

## Minimal Lemma

> **Unified Major Aperture Radius Lemma.**  
> For every relevant low-conductor packet center `c` and failing dyadic slice,
> \[
> \max(c_0/L_{\mathrm{crit}}(d,N),M_{\Omega}^{-1})
> \le
> \min(\rho_{\mathrm{valid}}(c),c_1Q_0^{-2}),
> \]
> or else the major packet frame captures both the high-`L` band energy and
> the kernel-window mass with residuals inside their assigned budgets.

## Result

The aperture side of the shifted-kernel branch has one combined radius check.
The same major validity radius must cover the failing kernel bands and the
kernel peak core whose mass would otherwise violate the post-variation
closure inequality.
