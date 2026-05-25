# Divisor Shift-Kernel Minor-Arc Bound Strategy

Date: 2026-05-24

Status: candidate strategy for bounding the minor-arc size of the
divisor-weighted shift kernel.

The shift kernel is

$$
F_{Q_0,H,N}(\alpha)
=
\sum_{0<|h|\le H}
\tau_{Q_0}(h)\widehat\Omega_N(h)e(h\alpha),
\qquad
H=\rho^{-1}.
$$

Using

$$
\tau_{Q_0}(h)=\sum_{\substack{q\le Q_0\\q\mid h}}1,
$$

write

$$
F_{Q_0,H,N}(\alpha)
=
\sum_{q\le Q_0}
\sum_{0<|r|\le H/q}
\widehat\Omega_N(qr)e(qr\alpha).
$$

## Major Peaks

For each `q`, the inner sum is large when

$$
\|q\alpha\|
$$

is small, i.e. when `alpha` is near a rational with denominator dividing
`q`. These peaks are low-conductor major packet structure and belong to
`F_maj`.

The minor region for `F` is defined by lower bounds

$$
\|q\alpha\|\ge \eta_q
\qquad
(1\le q\le Q_0).
$$

## Geometric-Sum Bound

If the weight `widehat Omega_N(qr)` has bounded variation in `r`, partial
summation gives

$$
\sum_{0<|r|\le H/q}
\widehat\Omega_N(qr)e(qr\alpha)
\ll
V_q
\min\left({H\over q},{1\over \|q\alpha\|}\right),
$$

where `V_q` records the size and variation of the smoothed kernel transform
on the progression `qr`.

On the `F`-minor region this yields

$$
|F_{\mathrm{min}}(\alpha)|
\ll
\sum_{q\le Q_0}
V_q
\min\left({H\over q},{1\over \eta_q}\right).
$$

This is the basic deterministic minor-arc bound.

## Mean-Square Alternative

Instead of an `L^infty` bound, use a mean-value estimate:

$$
\int_{\mathfrak m}
|F_{\mathrm{min}}(\alpha)|^2\,d\alpha
\ll
\sum_{0<|h|\le H}
\tau_{Q_0}(h)^2
|\widehat\Omega_N(h)|^2.
$$

Since

$$
\tau_{Q_0}(h)\le \tau(h),
$$

this gives a divisor-square cost, typically logarithmic after smoothing. The
mean-square route pairs with an `L^4` or higher moment estimate for
`A^perp`.

## Required Inputs

The divisor-kernel minor estimate needs:

1. decay and bounded variation for `widehat Omega_N(h)`;
2. a minor-region definition giving lower bounds for `||q alpha||`;
3. rational-packet subtraction assigning small `||q alpha||` to `F_maj`;
4. summability of the resulting bound over `q <= Q_0`;
5. if using the mean-square route, a compatible higher moment for the
   residual endpoint sum.

## Closure Test

For the `L^infty` route, the shift-kernel mean-value lemma closes if

$$
\left(
\sum_{q\le Q_0}
V_q
\min\left({H\over q},{1\over \eta_q}\right)
\right)
\int_{\mathfrak m}|A^{\perp}(\alpha)|^2\,d\alpha
\le
\mathcal E_{\mathrm{shift}}.
$$

For the mean-square route, it closes if

$$
\|F_{\mathrm{min}}\|_2
\|A^{\perp}\|_4^2
\le
\mathcal E_{\mathrm{shift}}.
$$

## Minimal Lemma

> **Divisor Shift-Kernel Minor Bound.**  
> After low-conductor packet peaks are assigned to `F_maj`, the residual
> kernel satisfies either an `L^infty` bound from the geometric-sum estimate
> above, or an `L^2` bound with divisor-square cost, strong enough to close
> the weighted minor mean-value estimate for `|A^perp|^2F_min`.

## Result

The minor-arc size of the shift kernel is controlled by elementary
exponential-sum geometry once the low-conductor peaks are removed. The main
quantitative choices are the minor thresholds `eta_q` and the transform
variation bounds for `widehat Omega_N(h)`.
