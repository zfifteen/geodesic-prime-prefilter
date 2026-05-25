# Kernel-Band Support, Norm, and Transform Inputs

Date: 2026-05-24

Status: final input ledger for the kernel-band dyadic load estimate.

The dyadic load estimate needs concrete laws for:

$$
H_d,\quad T_d,\quad K_d,\quad U,\quad
\mathcal B_d,\quad E_v(d),\quad R_{\mathrm{spec}},
$$

plus the sampled transform estimate for `W_{N,L}^perp(dt)`.

## Physical Lengths And Dual Supports

For a common-divisor slice `d`, let:

$$
U\asymp \text{modulus length after the slope split},
$$

$$
\mathcal N_d
=
\text{physical length of the completed } n'\text{-interval},
$$

and

$$
\mathcal V_d
=
\text{physical length of the completed } v\text{-interval}.
$$

With smooth cutoffs, Poisson completion gives the dual support laws

$$
H_d\ll 1+{U\over \mathcal N_d},
\qquad
K_d\ll 1+{U\over \mathcal V_d},
$$

up to logarithmic smoothing tails. These two inequalities are the support
inputs for the completed variables.

## Kernel Transform Support

For the dyadic interval-kernel band

$$
|K_N(\alpha)|\asymp L,
$$

the band lies on frequency scale `||alpha|| ~ L^{-1}` and has smooth width
`asymp L^{-1}`. Therefore the transform

$$
W_{N,L}^{\perp}(r)
=
\int w_{N,L}^{\perp}(\alpha)e(\alpha r)\,d\alpha
$$

has rapid decay for

$$
|r|\gg L
$$

after smoothing. Since the sampled variable is `r=dt`, the effective kernel
support is

$$
T_d\ll {L\over d}.
$$

This support law is separate from the energy estimate

$$
\sum_t |W_{N,L}^{\perp}(dt)|^2
\ll
d^{-1}L^3\Delta_L.
$$

The first controls the support size in the spectral large-sieve cost; the
second controls coefficient energy.

## Coefficient Norm Laws

The completed `n'` coefficient norm must supply

$$
\sum_h |B_{d,h,t}|^2
\ll
\mathcal B_d.
$$

With divisor-bounded coefficients and smooth completion, the target law is

$$
\mathcal B_d
\ll
\mathcal N_d(\log X)^C,
$$

or the exact Plancherel-normalized variant produced by the chosen completion.

The completed slope coefficient satisfies

$$
E_v(d)
=
\sum_{v\sim \mathcal V_d}|c_v|^2
\ll
\mathcal V_d(\log X)^C
$$

for divisor-bounded Type II coefficients.

The verification must state the exact normalization used for both norms,
because these factors multiply the dyadic load.

## Bessel Range

The Kuznetsov Bessel argument is

$$
{4\pi\sqrt{|mk|}\over u},
$$

with

$$
|m|\le H_dT_d,
\qquad
|k|\le K_d,
\qquad
u\asymp U.
$$

Thus the required Bessel support estimate is

$$
R_{\mathrm{spec}}
\ll
1+{\sqrt{H_dT_dK_d}\over U}.
$$

This estimate must include rapid decay outside the stated range and
summability over dyadic slices.

## Resulting Load

After substituting these inputs, the dyadic load becomes

$$
d^{-1}\mathcal B_d
\left(1+{H_dT_dK_d\over U^2}+H_dT_d\right)
\left(1+{H_dT_dK_d\over U^2}+K_d\right)
U E_v(d).
$$

With

$$
H_d\ll 1+U/\mathcal N_d,
\qquad
K_d\ll 1+U/\mathcal V_d,
\qquad
T_d\ll L/d,
$$

and divisor-norm laws for `B_d` and `E_v(d)`, this expression becomes a
finite dyadic function of the physical lengths

$$
d,\quad L,\quad U,\quad \mathcal N_d,\quad \mathcal V_d.
$$

That function is the final object to compare with

$$
{ \mathcal E_{\mathrm{band}}^{\mathrm{alloc}}
\over
C_LQ_0^6(\log X)^C}.
$$

## Packet-Frame Replacement

If the resulting load is too large, the only remaining band-side replacement
is

$$
\sum_t |W_{N,L}^{\perp}(dt)|^2
\ll
d^{-1}L^3\Delta_L
$$

with

$$
\sum_{d,N,L}
d^{-1}L^3\Delta_L\mathcal B_d\mathcal D_{d,N}
\le
\mathcal E_{\mathrm{band}}^{\mathrm{alloc}}.
$$

This is the band-energy part of the Unified Packet-Frame Source theorem.

## Final Kernel-Band Obligations

To close the kernel-band side, the project must prove:

1. the physical length laws for `N_d` and `V_d`;
2. the Poisson support laws for `H_d` and `K_d`;
3. the transform support law `T_d << L/d`;
4. the sampled transform energy lemma;
5. the coefficient norm laws for `B_d` and `E_v(d)`;
6. the Bessel range bound for `R_spec`;
7. the dyadic load sum against `E_band^alloc`, or the packet-frame
   `Delta_L` saving law.

## Result

The kernel-band branch has reached its final local input list. Nothing else
is hidden in `D_{d,N}`: it is determined by physical support, coefficient
norms, Bessel range, and sampled transform energy. Verifying those inputs
closes the literal band payment; failing that, the required packet-frame
saving is exactly the displayed `Delta_L` estimate.
