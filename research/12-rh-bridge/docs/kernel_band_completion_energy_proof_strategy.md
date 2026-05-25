# Kernel-Band Completion Energy Proof Strategy

Date: 2026-05-24

Status: candidate proof strategy for the kernel-band completion-energy input.

The required lemma bounds

$$
E_A(d,N,L)=\sum_{h,t}|A_{h,t}|^2
$$

for the completion coefficients created by the product-difference kernel
`W_{N,L}` after major-exclusion.

## Smoothed Band Weight

Replace the sharp band

$$
\mathfrak m_L=\{\alpha:L<|K_N(\alpha)|\le 2L\}
$$

by a smooth weight `psi_{N,L}` supported on the same dyadic band and outside
the removed major packets. In the product-difference expansion the relevant
weight is

$$
w_{N,L}(\alpha)\asymp L^2\psi_{N,L}(\alpha).
$$

Define

$$
W_{N,L}(r)=\int w_{N,L}(\alpha)e(\alpha r)\,d\alpha .
$$

The major projector is applied before this definition, so `W_{N,L}` is the
transform of the projected band weight.

## Deterministic Kernel Energy

The interval kernel satisfies

$$
|K_N(\alpha)|\ll \min(N,\|\alpha\|^{-1}).
$$

Hence a dyadic band with `|K_N| asymp L` has measure

$$
|\mathfrak m_L|\ll L^{-1}
$$

away from harmless endpoint smoothing. Since `w_{N,L}` has size `L^2` on this
band,

$$
\|w_{N,L}\|_2^2
\ll
L^4|\mathfrak m_L|
\ll
L^3.
$$

By Parseval,

$$
\sum_r |W_{N,L}(r)|^2
\ll
L^3.
$$

After common-divisor splitting, the kernel is sampled at `r=dt`, so

$$
\sum_t |W_{N,L}(dt)|^2
\ll
d^{-1}L^3
$$

up to smoothing constants. This is the base kernel-energy estimate.

## Completion Coefficient Energy

The completion coefficients have the schematic form

$$
A_{h,t}=W_{N,L}(dt)\,B_{d,h,t},
$$

where `B_{d,h,t}` contains the completed `n'` coefficient, Type II weights,
and harmless smooth cutoffs. Plancherel in the completed variable gives

$$
\sum_h |B_{d,h,t}|^2\ll \mathcal B_d
$$

uniformly in `t`, with `B_d` determined by the divisor-bounded Type II
coefficient norm.

Therefore the base completion-energy bound is

$$
E_A(d,N,L)
\ll
d^{-1}L^3\mathcal B_d.
$$

The major projector can only reduce this `L^2` energy, provided it is an
orthogonal or bounded projection on the band-weighted space.

## Closure Test

Substituting this into the Completion Energy Bound gives the sufficient
condition

$$
d^{-1}L^3\mathcal B_d
\le
{ \mathcal P_{d,N,L}^2
\over
(R_{\mathrm{spec}}^2+H_dT_d)
(R_{\mathrm{spec}}^2+K_d)U E_v(d)}
(\log X)^{-C}.
$$

This is the first concrete kernel-band size test. If it holds after summing
over `d` and `L`, the spectral Kloosterman route closes with no additional
oscillatory input beyond Kuznetsov and the spectral large sieve.

## If Base Energy Is Too Large

The rational phase `e(adt/q)` has modulus one and does not improve
`E_A(d,N,L)` after absolute squaring. Any improvement must come from one of
two places.

**Projected band mean-value saving.**
Major-exclusion may remove a positive fraction, or logarithmically strong
fraction, of the band energy:

$$
\|w_{N,L}^{\perp}\|_2^2
\ll
L^3\Delta_L,
\qquad
\Delta_L<1.
$$

This directly improves `E_A`.

**Kernel-band oscillation before squaring.**
Instead of bounding `E_A` band by band, sum the projected kernel bands before
taking absolute values and use cancellation among the transforms
`W_{N,L}(dt)`.

This is a stronger route because it uses phase information lost in the
bandwise energy estimate.

## Minimal Mean-Value Input

The proof strategy needs the following deterministic or analytic estimate.

> **Projected Kernel Energy Estimate.**  
> For every dyadic band `L` and common-divisor slice `d`, the projected
> product-difference transform satisfies
> \[
> \sum_t |W_{N,L}^{\perp}(dt)|^2
> \ll d^{-1}L^3\Delta_L
> \]
> with `Delta_L` small enough that
> \[
> d^{-1}L^3\Delta_L\mathcal B_d
> \]
> satisfies the Completion Energy Bound after summing over `d` and `L`.

The base Parseval estimate corresponds to `Delta_L=1`. Any required saving
beyond that is precisely kernel-band cancellation.

## Result

The Kernel-Band Completion Energy Lemma reduces to a concrete transform-energy
estimate. The deterministic kernel facts give

$$
E_A(d,N,L)\ll d^{-1}L^3\mathcal B_d.
$$

The remaining question is whether this base energy fits the Poisson allowance.
If not, the exact added input is projected kernel-band mean-value saving, or
equivalently cancellation among the kernel-band transforms before absolute
squaring.
