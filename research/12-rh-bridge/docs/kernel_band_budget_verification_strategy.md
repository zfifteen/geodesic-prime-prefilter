# Kernel-Band Budget Verification Strategy

Date: 2026-05-24

Status: focused strategy for verifying the kernel-band lower bound
`T_{d,N} >= C d^{-1} B_d Q0^6`, or the corresponding packet-frame residual
band-energy estimate.

The kernel-band estimate is the first completion-side source in the direct
route. It controls the failing high-`L` bands that force major-aperture
removal.

## Normalized Band Object

Use a smooth dyadic partition of the interval kernel:

$$
|K_N(\alpha)|\asymp L.
$$

Set

$$
w_{N,L}(\alpha)=L^2\psi_{N,L}(\alpha),
$$

and after major projection set

$$
w_{N,L}^{\perp}=(1-P_{\mathrm{maj}})w_{N,L},
$$

$$
W_{N,L}^{\perp}(r)
=
\int w_{N,L}^{\perp}(\alpha)e(\alpha r)\,d\alpha .
$$

The deterministic kernel estimate is

$$
\|w_{N,L}\|_2^2\ll L^3.
$$

The projected band-energy target is

$$
\|w_{N,L}^{\perp}\|_2^2
\ll
L^3\Delta_L,
$$

with `Delta_L=1` for the base Parseval route and `Delta_L<1` for
packet-frame capture.

## Sampling Lemma

The first kernel-band input is the sampled transform estimate

$$
\sum_t |W_{N,L}^{\perp}(dt)|^2
\ll
d^{-1}L^3\Delta_L.
$$

This follows from Parseval plus lattice sampling for smoothed weights when
`Delta_L=1`. For `Delta_L<1`, it follows from the same sampling argument
after proving the packet-frame energy bound for `w_{N,L}`.

With the completed coefficient factor

$$
A_{h,t}=W_{N,L}^{\perp}(dt)B_{d,h,t},
$$

and

$$
\sum_h |B_{d,h,t}|^2\ll\mathcal B_d,
$$

the completion energy is

$$
E_A(d,N,L)
\ll
d^{-1}L^3\Delta_L\mathcal B_d.
$$

## Spectral Allowance Ratio

Define the dimensionless kernel-band allowance ratio

$$
\Xi_{d,N}
=
{ d\mathcal P_{d,N}^2
\over
\mathcal B_d
(R_{\mathrm{spec}}^2+H_dT_d)
(R_{\mathrm{spec}}^2+K_d)U E_v(d)}
(\log X)^{-C}.
$$

Then

$$
L_{\mathrm{crit}}(d,N)
=
\Xi_{d,N}^{1/3}.
$$

The direct literal branch requires

$$
\Xi_{d,N}\ge C Q_0^6.
$$

Equivalently,

$$
{ \mathcal P_{d,N}^2
\over
(R_{\mathrm{spec}}^2+H_dT_d)
(R_{\mathrm{spec}}^2+K_d)U E_v(d)}
(\log X)^{-C}
\ge
C d^{-1}\mathcal B_dQ_0^6.
$$

This is the exact verification test for the kernel-band source.

## Bessel-Range Input

The Bessel transform is evaluated at

$$
{4\pi\sqrt{|mk|}\over u},
$$

with

$$
|m|\le H_dT_d,\qquad |k|\le K_d,\qquad u\asymp U.
$$

A usable range bound is therefore

$$
R_{\mathrm{spec}}
\le
C_R\left(1+{\sqrt{H_dT_dK_d}\over U}\right)
$$

with rapid decay outside this range. This estimate must be proved for the
chosen smooth modulus and band weights before the allowance ratio can be
checked numerically or symbolically.

## Literal Verification Path

The literal kernel-band path is:

1. define the smoothed band weight `w_{N,L}`;
2. prove the sampled transform estimate with `Delta_L=1`;
3. compute or bound `H_d,T_d,K_d,U,E_v(d),B_d,P_{d,N}`;
4. prove the Bessel range bound for `R_spec`;
5. verify
   $$
   \Xi_{d,N}\ge C Q_0^6
   $$
   for every relevant `d,N` slice.

If this holds, then

$$
L_{\mathrm{crit}}(d,N)\ge C Q_0^2,
$$

and the kernel-band part of the literal route closes.

## Packet-Frame Band-Energy Path

If

$$
\Xi_{d,N}<C Q_0^6,
$$

the required projected saving on a failing band of scale `L` is

$$
\Delta_L
\le
{ \Xi_{d,N}\over L^3 }.
$$

The corresponding packet-frame lower bound is

$$
\sum_{c:q(c)\le Q_0}
|\langle w_{N,L},\phi_c\rangle|^2
\ge
(1-\Delta_L)\|w_{N,L}\|_2^2,
$$

with the frame normalized so that the right side measures the actual
orthogonal projection energy. This bound says that the low-conductor packet
span captures the high-mass kernel band even when literal support apertures
cannot be made wide enough.

## Final Kernel-Band Inputs

The kernel-band source closes after the following quantities are fixed:

1. the exact smooth dyadic band partition for `K_N`;
2. the projection convention defining `w_{N,L}^perp`;
3. the sampled transform lemma for `W_{N,L}^perp(dt)`;
4. the support sizes `H_d,T_d,K_d,U`;
5. the Type II coefficient norms `E_v(d)` and `B_d`;
6. the Poisson allowance `P_{d,N}`;
7. the Bessel range bound for `R_spec`;
8. if needed, the packet-frame lower bound giving `Delta_L`.

## Result

The kernel-band completion source has one verification inequality:

$$
\Xi_{d,N}\ge C Q_0^6.
$$

If it holds, `L_crit >= C Q0^2` and the literal direct route keeps its
support-removal aperture. If it fails, the exact replacement is the residual
band-energy estimate with

$$
\Delta_L\le\Xi_{d,N}/L^3.
$$

No other kernel-band obstruction remains in this branch.
