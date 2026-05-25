# Major Projector Core-Radius Verification

Date: 2026-05-24

Status: candidate strategy for verifying that the major projector removes the
kernel-peak core required by the aperture-core mass bound.

The Aperture-Core Mass Lemma requires a removed core radius

$$
\rho_{\mathrm{core}}\ge M_{\Omega}^{-1},
\qquad
M_{\Omega}
=
{\mathcal E_{\mathrm{shift}}
\over
\mathcal S(Q_0,H,\rho_{\max})\mathcal A_{\mathrm{min}}}.
$$

This note states what the major projector must do.

## Relevant Kernel Peaks

Only packet centers whose aperture windows meet a high-mass kernel peak need
core removal. Define the relevant peak set by

$$
\mathcal P_{\mathrm{peak}}
=
\left\{
c:
\int_{|\beta|\le M_{\Omega}^{-1}}
|K_N(c+\beta)|^2\,d\beta
\text{ exceeds the assigned mass budget}
\right\}.
$$

Off-peak centers are handled by the off-peak kernel mass bound and do not
need core removal.

## Literal Support Projector

If the major projector is implemented by support cutoffs, it must include

$$
|\beta|<\rho_c
$$

around each relevant peak center `c`, with

$$
\rho_c\ge M_{\Omega}^{-1}.
$$

It must also satisfy

$$
\rho_c\le \min(\rho_{\mathrm{valid}}(c),c_1Q_0^{-2}).
$$

Thus literal removal is verified by the interval condition

$$
M_{\Omega}^{-1}
\le
\min(\rho_{\mathrm{valid}}(c),c_1Q_0^{-2})
$$

for every `c` in `P_peak`.

## Smooth Cutoff Requirement

The cutoff must be smoothed so that the residual transform has controlled
variation:

$$
\|(1-\chi_c)\Omega_N\|_1
\ll
M_{\Omega},
$$

and the smoothing tails must be charged to the same mass budget. Sharp
cutoffs reintroduce transform variation and should not be used in this proof
surface.

## Orthogonal Projector Alternative

If the major projector is a projection onto packet model functions rather
than support removal, the required condition is

$$
\|(1-P_{\mathrm{maj}})\Omega_N\|_1
\le
M_{\Omega}.
$$

A sufficient frame-style estimate is

$$
\|(1-P_{\mathrm{maj}})\Omega_N\|_2
\le
{M_{\Omega}
\over
|\operatorname{supp}\Omega_N|^{1/2}}.
$$

This replaces geometric core removal by energy capture of the kernel-peak
profile.

## Required Inputs

The verification needs:

1. the list of relevant peak centers `P_peak`;
2. the major validity radius `rho_valid(c)`;
3. rational separation `Q_0^{-2}`;
4. a smooth cutoff or packet-frame construction for `P_maj`;
5. a tail estimate showing the residual mass is at most `M_Omega`.

## Minimal Lemma

> **Major Projector Core-Radius Lemma.**  
> For every relevant kernel peak center `c`, the major projector removes or
> captures the aperture core at radius at least `M_Omega^{-1}` while staying
> inside the valid and disjoint major aperture:
> \[
> M_{\Omega}^{-1}
> \le
> \min(\rho_{\mathrm{valid}}(c),c_1Q_0^{-2}),
> \]
> or else the orthogonal packet projection satisfies
> \[
> \|(1-P_{\mathrm{maj}})\Omega_N\|_1\le M_{\Omega}.
> \]

## Result

The core-removal check is now a major-projector contract. Literal support
removal closes it when the major aperture radius reaches `M_Omega^{-1}` for
every relevant kernel peak. The projection route closes it by proving the
same residual mass bound directly.
