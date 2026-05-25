# Major-Aperture Kernel-Band Removal Strategy

Date: 2026-05-24

Status: candidate strategy for removing high-energy coherent cores of
kernel bands around low-conductor rational packets.

The diagonal projected band energy is controlled by

$$
\|w_{N,L}^{\perp}\|_2^2
=
\|(1-P_{\mathrm{maj}})w_{N,L}\|_2^2.
$$

The major-aperture task is to show that the projector removes a large fraction
of the coherent core of high-`L` bands.

## Band Around a Packet Center

Let

$$
c={a\over q},\qquad q\le Q_0,
$$

be a low-conductor packet center. A dyadic band around `c` has scale

$$
E_L(c)=\{\alpha:\|\alpha-c\|\asymp L^{-1}\}.
$$

Let the major aperture around `c` have radius `rho_c`. The literal support
removed is

$$
\operatorname{Maj}(c)=\{\alpha:\|\alpha-c\|\le \rho_c\}.
$$

## Aperture-Band Coupling

The overlap of `E_L(c)` with the major aperture is deterministic.

If

$$
L^{-1}\le c_0\rho_c,
$$

then the band lies inside the major aperture up to smoothing tails, and the
projected support is negligible:

$$
\|w_{N,L}^{\perp}\|_2^2\approx0.
$$

If

$$
L^{-1}\gg \rho_c,
$$

the aperture removes little of that band, and no diagonal mean-value saving
follows from support removal alone.

In the transition regime,

$$
L^{-1}\asymp\rho_c,
$$

one obtains only a constant-factor saving unless the projector is stronger
than literal aperture removal.

## Support-Measure Saving

Since `w_{N,L}` has size `L^2` on a set of measure `<< L^{-1}`, support
removal gives

$$
\|w_{N,L}^{\perp}\|_2^2
\ll
L^4 |E_L(c)\setminus \operatorname{Maj}(c)|.
$$

Thus

$$
\Delta_L(c)
\asymp
{ |E_L(c)\setminus \operatorname{Maj}(c)| \over |E_L(c)| }.
$$

The needed diagonal saving is exactly a bound on this residual fraction.

## Orthogonal Projector Alternative

If `P_maj` is not literal support restriction, it can still remove the
coherent core by orthogonal projection. The required statement is

$$
\|P_{\mathrm{maj}}w_{N,L}\|_2^2
\ge
(1-\Delta_L)\|w_{N,L}\|_2^2.
$$

This means the high-energy component of the band lies in the span of the
major packet model functions. It is stronger than aperture removal because it
can remove coherent profiles even when their support leaks beyond the chosen
major interval.

## Required Inputs

The major-aperture proof needs:

1. explicit major radii `rho_c` for each low-conductor packet center;
2. smooth band cutoffs with controlled tails;
3. a residual-measure bound for `E_L(c)\setminus Maj(c)`;
4. or an orthogonal projection theorem showing the packet span captures
   `1-Delta_L` of the band energy.

The current notes identify the major packets but do not yet fix the aperture
radii tightly enough to derive `Delta_L`.

## Minimal Lemma

> **Aperture-Band Coupling Lemma.**  
> For each low-conductor rational packet center `c`, the major aperture radius
> `rho_c` and dyadic band scale `L^{-1}` satisfy
> \[
> \|(1-P_{\mathrm{maj}})w_{N,L,c}\|_2^2
> \ll L^3\Delta_L(c),
> \]
> where `Delta_L(c)` is summable in the Completion Energy Bound. In
> particular, high-`L` bands with `L^{-1} <= c_0 rho_c` are removed up to
> smoothing tails.

## Result

Major-aperture removal is a deterministic support or projection-energy
statement. It closes the diagonal high-`L` kernel energy only if the major
apertures are coupled to the dyadic band scale: bands whose radius falls
inside the coherent major core must be removed before the spectral
Kloosterman energy estimate is applied.
