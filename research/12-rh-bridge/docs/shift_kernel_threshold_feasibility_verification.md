# Shift-Kernel Threshold Feasibility Verification

Date: 2026-05-24

Status: verification strategy for the Shift-Kernel Threshold Feasibility
Lemma.

The threshold lemma asks for `eta_q` satisfying

$$
\sum_{q\le Q_0}
V_q\min\left({H\over q},{1\over\eta_q}\right)
\le
{\mathcal E_{\mathrm{shift}}\over\mathcal A_{\mathrm{min}}},
$$

and

$$
{\eta_q\over q}
\le
\min(\rho_{\mathrm{valid}}(b/q),cQ_0^{-2}).
$$

## Maximal Admissible Threshold

Define

$$
\rho_{\max}(q)
=
\min_{(b,q)=1}
\min(\rho_{\mathrm{valid}}(b/q),cQ_0^{-2}).
$$

The largest admissible threshold is

$$
\eta_q^{\max}=q\rho_{\max}(q).
$$

This choice minimizes the `L^infty` minor bound. Therefore the threshold route
is feasible exactly if

$$
\sum_{q\le Q_0}
V_q
\min\left({H\over q},{1\over q\rho_{\max}(q)}\right)
\le
{\mathcal E_{\mathrm{shift}}\over\mathcal A_{\mathrm{min}}}.
$$

This is the clean threshold verification inequality.

## Quantities to Verify

The inequality needs four inputs:

1. `V_q`, the size/variation cost of `widehat Omega_N(qr)`;
2. `rho_valid(b/q)`, the major validity radius;
3. `A_min`, the residual endpoint minor-arc `L^2` mass;
4. `E_shift`, the aperture error budget assigned to the shifted-kernel branch.

Once these are fixed, no further optimization over `eta_q` is needed.

## Variation Bound for the Kernel Transform

The required kernel-transform input is

$$
V_q
\ge
\operatorname{Var}_{1\le |r|\le H/q}
\widehat\Omega_N(qr)
+
\sup_{1\le |r|\le H/q}
|\widehat\Omega_N(qr)|.
$$

A useful bound should express `V_q` in terms of the aperture scale `H`, the
kernel band, and smoothness of the projected weight. This is a deterministic
Fourier-transform estimate.

## L2 Alternative and Circularity Warning

If the `L^infty` threshold inequality fails, the proposed alternative is

$$
\|F_{\mathrm{min}}\|_2
\|A^{\perp}\|_4^2
\le
\mathcal E_{\mathrm{shift}}.
$$

This route is valid only if the `L^4` bound for `A^perp` is supplied
independently. It must not reuse the endpoint fourth-moment theorem that this
RH bridge chain is trying to prove. Otherwise the argument becomes circular.

An independent `L^4` input would have to come from Type I/II dispersion,
large-sieve fourth moments, or a separate residual minor-arc theorem.

## Minimal Verification Lemma

> **Shift-Kernel Threshold Verification Lemma.**  
> With
> \[
> \eta_q=q\rho_{\max}(q),
> \]
> the divisor-kernel minor bound closes if
> \[
> \sum_{q\le Q_0}
> V_q
> \min\left({H\over q},{1\over q\rho_{\max}(q)}\right)
> \mathcal A_{\mathrm{min}}
> \le
> \mathcal E_{\mathrm{shift}}.
> \]
> If this fails, the replacement `L2` route requires an independent residual
> endpoint `L4` moment, not the endpoint fourth-moment result downstream of
> this bridge.

## Result

Threshold verification has reduced to one explicit inequality. The next
deterministic input is a variation bound for `widehat Omega_N(qr)`, and the
next analytic inputs are the major validity radius and residual endpoint
minor-arc `L^2` mass. The `L2` alternative is available only with an
independent `L4` endpoint moment.
