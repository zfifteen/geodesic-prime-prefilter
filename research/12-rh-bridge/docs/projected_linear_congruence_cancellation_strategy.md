# Projected Linear Congruence Cancellation Strategy

Date: 2026-05-24

Status: candidate strategy for the average-cancellation input in the
dispersion-method route.

After common-divisor splitting, the off-diagonal near-product problem is a
family of linear congruence sums

$$
un-vn'=t,\qquad (u,v)=1,\qquad t\ne0.
$$

The major-exclusion projector has already removed the exact diagonal, the
small-conductor residue averages, and the low-denominator kernel packets. The
remaining task is average cancellation over the coprime slope pairs `u,v`.

## Projected Local Error

For fixed `d,u,v`, define the projected local error

$$
\mathcal E_{u,v,d}(t)
=
\sum_{\substack{n,n'\sim B\\ un-vn'=t}}
\beta_n\overline{\beta_{n'}}
-
\operatorname{Maj}_{u,v,d}(t),
$$

where `Maj` is the part removed by the major-exclusion projector. The target
sum is

$$
\sum_d
\sum_{\substack{u,v\sim A/d\\ (u,v)=1}}
\alpha_{du}\overline{\alpha_{dv}}
\sum_{t\ne0}
e\!\left({adt\over q}\right)W_N(dt)
\mathcal E_{u,v,d}(t).
$$

The desired conclusion is that this projected sum lies inside the
Poisson-scale allowance after kernel-band summation, uniformly for `q <= Q_0`.

## Fourier Large-Sieve Route

Fourier expansion gives the fixed-`d` contribution as

$$
\int \widehat W_{N,d}(\xi)
\left|
\sum_{u\sim A/d}
\alpha_{du}
\sum_{n\sim B}
\beta_n e((\xi+ad/q)un)
\right|^2
d\xi
$$

with the projected major packets removed.

This route needs a hybrid large-sieve estimate for the frequency set

$$
(\xi+ad/q)u \pmod 1,\qquad u\sim A/d.
$$

The major projector removes the frequencies for which this set clusters around
small-denominator rationals. Away from those clusters, spacing in `u` should
produce the saving. The required bound is an averaged estimate of the form

$$
\int_{\mathrm{minor}(d,q)}
\left|
\sum_{u\sim A/d}\alpha_{du}B((\xi+ad/q)u)
\right|^2 d\xi
\ll \mathcal P_{d,N},
$$

where

$$
B(\theta)=\sum_{n\sim B}\beta_n e(\theta n),
$$

and `P_{d,N}` denotes the Poisson allowance assigned to the `d`-slice and
kernel band.

## Linear Dispersion Route

The congruences

$$
u n\equiv t\pmod v,\qquad v n'\equiv -t\pmod u
$$

turn the error into a discrepancy of coefficient sums in residue classes whose
moduli are the opposite slope. Averaging over `u,v` gives a bilinear
dispersion problem:

$$
\sum_{\substack{u,v\\(u,v)=1}}
\alpha_{du}\overline{\alpha_{dv}}
\sum_t K_{d,q,N}(t)
\left(
\#_{\beta}(u n-vn'=t)-\operatorname{Maj}_{u,v,d}(t)
\right).
$$

Here

$$
K_{d,q,N}(t)=e(adt/q)W_N(dt).
$$

The needed input is cancellation in the discrepancy after summing over the
slopes. Pointwise control for a single pair `u,v` is not required. The average
over coprime slopes is the source of saving.

## Kloosterman-Type Route

Solving one congruence gives reciprocal phases. For example,

$$
v n'\equiv -t\pmod u.
$$

When `(v,u)=1`, this is

$$
n'\equiv -t\overline v\pmod u.
$$

After additive completion in `n'`, the slope average contains sums with
reciprocal dependence on `v mod u`. These are Kloosterman-type sums averaged
over `u` and `v`.

The required input is not a standalone Weil bound for each modulus. It is a
bilinear Kloosterman average compatible with the divisor-bounded Type II
coefficients and the kernel weight `K_{d,q,N}`.

## Degenerate Conductors

Let `g=(d,q)` and `q_1=q/g`. If `q_1=1`, the phase

$$
e(adt/q)
$$

is constant in `t`. Then all cancellation must come from the projected
coefficient discrepancy. The major projector must remove the complete local
mean in the relevant residue classes. The remaining statement is a pure
linear-dispersion bound.

This case is a diagnostic: if the projected estimate fails here, small-modulus
oscillation was never the real source of cancellation.

## Minimal Cancellation Input

The analytic bridge can now be stated as a single local estimate.

> **Projected Coprime-Slope Dispersion Bound.**  
> For divisor-bounded Type II coefficients in the balanced range, after
> removing exact diagonals, small-conductor residue averages, and
> low-denominator kernel packets, the weighted sum of
> `E_{u,v,d}(t)` over coprime slopes `u,v`, common divisors `d`, and
> nonzero `t` is bounded by the Poisson-scale kernel allowance uniformly for
> `q <= Q_0`.

## What Existing Inputs Would Supply

The hybrid large sieve supplies spacing cancellation for non-clustered
frequencies.

The linear dispersion method supplies residue-class discrepancy cancellation
after averaging over the opposite slope.

Kloosterman-type estimates supply cancellation in the reciprocal congruence
pieces created when the slope variables are completed.

The major-exclusion projector supplies the necessary mean-zero condition. It
does not by itself give cancellation; it identifies the part to which these
three tools may be applied.

## Result

The projected linear family `un-vn'=t` is the first place where the analytic
bridge needs a real average-cancellation theorem. The statement is now local:
prove Poisson-scale cancellation for the mean-zero coprime-slope congruence
family after the major coherent components have been removed.
