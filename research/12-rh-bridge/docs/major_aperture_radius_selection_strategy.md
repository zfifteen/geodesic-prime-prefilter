# Major-Aperture Radius Selection Strategy

Date: 2026-05-24

Status: candidate strategy for fixing major aperture radii around
low-conductor packet centers.

For each low-conductor center

$$
c={a\over q},\qquad q\le Q_0,
$$

the major aperture radius `rho_c` must do two jobs:

1. remove the high-`L` kernel bands whose diagonal energy is too large;
2. remain inside the range where the major packet approximation is valid and
   distinct rational packets stay separated.

## Critical Band Scale

For a dyadic `d`-slice, the base projected kernel energy is

$$
E_A(d,N,L)\ll d^{-1}L^3\mathcal B_d.
$$

Let `L_crit(d,N)` be the largest band scale that can be handled without
major-aperture saving, defined by the closure inequality

$$
d^{-1}L_{\mathrm{crit}}^3\mathcal B_d
\le
{ \mathcal P_{d,N,L_{\mathrm{crit}}}^2
\over
(R_{\mathrm{spec}}^2+H_dT_d)
(R_{\mathrm{spec}}^2+K_d)U E_v(d)}
(\log X)^{-C}.
$$

Bands with

$$
L>L_{\mathrm{crit}}(d,N)
$$

must be removed by the major projector or controlled by a stronger
orthogonality theorem.

## Radius Lower Bound

A band of scale `L` is removed by support aperture when

$$
L^{-1}\le c_0\rho_c.
$$

Therefore support removal of all failing bands requires

$$
\rho_c
\ge
{c_0\over L_{\mathrm{crit}}(d,N)}
$$

for every `d`-slice whose failing bands occur near the packet center `c`.

## Radius Upper Bounds

The radius also satisfies two upper constraints.

**Rational separation.**
Distinct centers with denominators at most `Q_0` are separated by at least
`Q_0^{-2}`. To keep apertures disjoint it is enough to impose

$$
\rho_c\le c_1Q_0^{-2}.
$$

**Major approximation validity.**
Let `rho_valid(c)` be the radius on which the major packet approximation for
the centered endpoint sum is valid with an error inside the Poisson allowance.
Then

$$
\rho_c\le \rho_{\mathrm{valid}}(c).
$$

This is the analytic major-arc input. It comes from PNT-in-progressions,
Bombieri-Vinogradov, zero-density estimates, or whatever major approximation
the endpoint Fourier route uses.

## Feasibility Condition

Literal aperture removal closes the high-`L` diagonal kernel energy when

$$
{c_0\over L_{\mathrm{crit}}(d,N)}
\le
\rho_c
\le
\min(c_1Q_0^{-2},\rho_{\mathrm{valid}}(c))
$$

for all relevant packet centers and `d`-slices.

If this interval is nonempty, choose `rho_c` in it and set

$$
\Delta_L(c)=0
$$

for bands with `L>L_crit`, up to smoothing tails.

## Orthogonal Projection Alternative

If the feasible radius interval is empty, literal support removal is not
enough. The alternative is a packet-frame estimate. Let `phi_c` be the major
packet model function at center `c`. The needed theorem is

$$
\sum_{c:q(c)\le Q_0}
|\langle w_{N,L},\phi_c\rangle|^2
\ge
(1-\Delta_L)\|w_{N,L}\|_2^2
$$

for failing high-`L` bands. This captures coherent energy by projection even
when the aperture radius cannot cover the full band support.

The projection route needs:

1. a normalized major packet frame `{phi_c}`;
2. bounded overlap between packet functions;
3. a frame lower bound on high-`L` kernel bands;
4. major approximation validity for the projected packet components.

## Minimal Radius Lemma

> **Major Aperture Feasibility Lemma.**  
> For every dyadic `d`-slice and low-conductor center `c`, the critical band
> scale `L_crit(d,N)` and the major validity radius `rho_valid(c)` satisfy
> \[
> {c_0\over L_{\mathrm{crit}}(d,N)}
> \le
> \min(c_1Q_0^{-2},\rho_{\mathrm{valid}}(c)),
> \]
> or else the major packet functions obey the orthogonal projection lower
> bound with enough `Delta_L` saving to replace literal aperture removal.

## Result

The aperture radius problem is now a compatibility check. Major arcs must be
wide enough to remove exactly the kernel bands whose base `L^3` energy fails,
and narrow enough to preserve rational separation and valid major packet
asymptotics. If that interval is empty, the proof must use the orthogonal
major-packet projection theorem instead of support removal.
