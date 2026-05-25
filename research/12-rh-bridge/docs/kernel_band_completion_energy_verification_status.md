# Kernel-Band Completion Energy Verification Status

Date: 2026-05-24

Status: verification pass for the Completion Energy Bound against the current
kernel-band normalization in the RH bridge notes.

The current notes supply the kernel-band framework:

$$
|K_N(\alpha)|\asymp L,
\qquad
1\le L\le N,
$$

and the convolution-scale Poisson target

$$
\sum_{L_1,L_2}
\left\|
L_1S_{A,B}1_{\mathfrak m_{L_1}}
*
L_2S_{A',B'}1_{\mathfrak b_{L_2}}
\right\|_2^2
\ll
X\left({N\over\log X}\right)^2(\log X)^{-A_0}.
$$

They also identify the product-difference kernel `W_N` created by integrating
the shifted Type II mean square against the kernel-band weight.

## What Is Already Fixed

The current bridge notes fix these structural facts:

1. the interval kernel obeys
   $$
   |K_N(\alpha)|\ll \min(N,\|\alpha\|^{-1});
   $$
2. dyadic bands are indexed by `L`;
3. Type II pieces are weighted by `L` on each band;
4. the expanded mean square localizes product differences through a weight
   `W_N(mn-m'n')`;
5. after common-divisor splitting, the reciprocal-congruence branch leads to
   completion coefficients `A_{h,t}` and `D_k`.

These facts are enough to state the spectral Kloosterman route. They are not
yet enough to verify its coefficient-size inequality.

## What Is Not Yet Fixed

The current notes do not yet define:

1. the exact smoothed band weight `w_{N,L}(\theta)`;
2. the transform norms of the product-difference weight:
   $$
   \|W_{N,L}\|_1,\qquad \|W_{N,L}\|_2,\qquad
   \operatorname{supp}_{\mathrm{eff}} W_{N,L};
   $$
3. the completion support sizes `H_d`, `T_d`, and `K_d`;
4. the Bessel-selected spectral range `R_spec`;
5. the actual energy
   $$
   E_A(d,N,L)=\sum_{h,t}|A_{h,t}|^2
   $$
   after the major projector is applied.

Without these quantities, the Completion Energy Bound cannot be verified as a
proved estimate.

## Present Verification Result

The current kernel-band normalization does not yet close the spectral branch
by itself. What is proved at this stage is conditional:

$$
\Bigl((R_{\mathrm{spec}}^2+H_dT_d)(\log X)^C E_A(d,N,L)\Bigr)^{1/2}
\Bigl((R_{\mathrm{spec}}^2+K_d)U E_v(d)\Bigr)^{1/2}
\le
\mathcal P_{d,N,L}
$$

would close the projected reciprocal-congruence Kloosterman route for that
dyadic slice and kernel band.

The repository currently contains the left-hand structure, but not the exact
kernel-transform energy estimate needed to compare it with
`\mathcal P_{d,N,L}`.

## Which Extra Source Is Needed

Among the three possible extra sources,

1. product-collapse cancellation;
2. slope-completion cancellation;
3. kernel-band cancellation,

the first required source is **kernel-band cancellation / kernel-band
completion-energy control**.

Reason: Cauchy already reduces the product collapse to divisor powers, and
Plancherel already controls the completed slope sequence once the `v` weight
is fixed. The unfixed quantity is the energy carried by `W_{N,L}` into
`A_{h,t}` and the Bessel range it forces.

Thus the next minimal estimate is not a stronger divisor-collapse bound. It
is a kernel-transform estimate.

## Minimal New Lemma

> **Kernel-Band Completion Energy Lemma.**  
> For every dyadic kernel band `L` and common-divisor slice `d`, after the
> major-exclusion projector is applied, the transformed product-difference
> weight supplies completion coefficients satisfying
> \[
> E_A(d,N,L)
> \le
> { \mathcal P_{d,N,L}^2
> \over
> (R_{\mathrm{spec}}^2+H_dT_d)
> (R_{\mathrm{spec}}^2+K_d)U E_v(d)}
> (\log X)^{-C},
> \]
> with `R_spec` in the Bessel range allowed by the same inequality.

This lemma is exactly the kernel-band input needed before the spectral
Kloosterman route can be asserted from the current normalization.

## Result

The current notes do not yet verify the Completion Energy Bound. They reduce
the failure point to one local analytic estimate: control the
kernel-transform energy of `W_{N,L}` after major-exclusion strongly enough
that the completed coefficients `A_{h,t}` fit inside the Poisson allowance.
