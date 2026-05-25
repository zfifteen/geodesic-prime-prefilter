# Shift-Kernel Minor Threshold Selection

Date: 2026-05-24

Status: candidate strategy for choosing the thresholds `eta_q` in the
divisor shift-kernel minor bound.

The shift-kernel minor region is defined by

$$
\|q\alpha\|\ge \eta_q
\qquad (1\le q\le Q_0).
$$

The choice of `eta_q` balances two requirements:

1. larger `eta_q` gives a smaller minor bound for `F_min`;
2. larger `eta_q` expands the major packet region that must be covered by
   valid major-aperture estimates.

## Minor Bound Requirement

The deterministic `L^infty` bound is

$$
\|F_{\mathrm{min}}\|_{\infty}
\ll
\sum_{q\le Q_0}
V_q
\min\left({H\over q},{1\over\eta_q}\right).
$$

Let

$$
\mathcal A_{\mathrm{min}}
=
\int_{\mathfrak m}|A^{\perp}(\alpha)|^2\,d\alpha.
$$

The `L^infty` route closes if

$$
\left(
\sum_{q\le Q_0}
V_q
\min\left({H\over q},{1\over\eta_q}\right)
\right)
\mathcal A_{\mathrm{min}}
\le
\mathcal E_{\mathrm{shift}}.
$$

Thus the thresholds must make

$$
\sum_{q\le Q_0}
V_q
\min\left({H\over q},{1\over\eta_q}\right)
\le
{\mathcal E_{\mathrm{shift}}\over\mathcal A_{\mathrm{min}}}.
$$

## Major Aperture Constraint

The condition

$$
\|q\alpha\|<\eta_q
$$

corresponds to windows

$$
\left|\alpha-{b\over q}\right|<{\eta_q\over q}.
$$

These windows must fit inside the major packet validity aperture:

$$
{\eta_q\over q}
\le
\rho_{\mathrm{valid}}(b/q).
$$

They must also preserve rational separation:

$$
{\eta_q\over q}
\le
cQ_0^{-2}.
$$

Therefore

$$
\eta_q
\le
q\min(\rho_{\mathrm{valid}}(b/q),cQ_0^{-2}).
$$

## Feasibility Interval

Allocate a minor-bound budget `M_q` to each denominator `q`, with

$$
\sum_{q\le Q_0}M_q
\le
{\mathcal E_{\mathrm{shift}}\over\mathcal A_{\mathrm{min}}}.
$$

For the nontrivial branch where `1/eta_q` dominates, it is enough to choose

$$
\eta_q\ge {V_q\over M_q}.
$$

Thus the threshold is feasible if

$$
{V_q\over M_q}
\le
q\min(\rho_{\mathrm{valid}}(b/q),cQ_0^{-2})
$$

for every relevant denominator.

## L2 Alternative

If the `L^infty` thresholds are infeasible, use

$$
\|F_{\mathrm{min}}\|_2^2
\ll
\sum_{0<|h|\le H}
\tau_{Q_0}(h)^2|\widehat\Omega_N(h)|^2.
$$

This route closes if

$$
\|F_{\mathrm{min}}\|_2
\|A^{\perp}\|_4^2
\le
\mathcal E_{\mathrm{shift}}.
$$

It trades aperture-width pressure for a higher moment requirement on the
residual endpoint sum.

## Minimal Lemma

> **Shift-Kernel Threshold Feasibility Lemma.**  
> There exist thresholds `eta_q` and denominator budgets `M_q` such that
> \[
> \sum_{q\le Q_0}M_q
> \le
> {\mathcal E_{\mathrm{shift}}\over\mathcal A_{\mathrm{min}}},
> \qquad
> {V_q\over M_q}
> \le
> q\min(\rho_{\mathrm{valid}}(b/q),cQ_0^{-2}),
> \]
> or else the divisor-square `L^2` route paired with an `L^4` endpoint
> moment closes the same estimate.

## Result

The threshold choice is a concrete compatibility problem. The minor bound
requires `eta_q` large enough to suppress geometric sums; the major theory
requires `eta_q/q` small enough to lie inside valid, disjoint major apertures.
If no such thresholds exist, the proof must switch to the `L^2` divisor-kernel
route and pay for a higher endpoint moment.
