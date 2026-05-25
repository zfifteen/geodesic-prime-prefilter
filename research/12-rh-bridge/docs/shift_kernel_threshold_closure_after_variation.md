# Shift-Kernel Threshold Closure After Variation

Date: 2026-05-24

Status: closure test after substituting the deterministic variation bound
`V_q << ||Omega_N||_1`.

The threshold feasibility inequality was

$$
\sum_{q\le Q_0}
V_q
\min\left({H\over q},{1\over q\rho_{\max}(q)}\right)
\mathcal A_{\mathrm{min}}
\le
\mathcal E_{\mathrm{shift}}.
$$

The Kernel Transform Variation Lemma gives

$$
V_q\ll \|\Omega_N\|_1
$$

uniformly in `q`.

## Substituted Closure Test

After substitution, the `L^infty` route closes if

$$
\|\Omega_N\|_1
\left[
\sum_{q\le Q_0}
\min\left({H\over q},{1\over q\rho_{\max}(q)}\right)
\right]
\mathcal A_{\mathrm{min}}
\le
\mathcal E_{\mathrm{shift}}.
$$

Define

$$
\mathcal S(Q_0,H,\rho_{\max})
=
\sum_{q\le Q_0}
{1\over q}
\min\left(H,{1\over\rho_{\max}(q)}\right).
$$

Then the test is

$$
\|\Omega_N\|_1
\mathcal S(Q_0,H,\rho_{\max})
\mathcal A_{\mathrm{min}}
\le
\mathcal E_{\mathrm{shift}}.
$$

## Favorable Radius Regime

If the major validity radii satisfy

$$
\rho_{\max}(q)\ge \rho=H^{-1}
$$

for every `q <= Q_0`, then

$$
\mathcal S(Q_0,H,\rho_{\max})
\le
H\sum_{q\le Q_0}{1\over q}
\ll
H\log Q_0.
$$

A sufficient condition becomes

$$
\|\Omega_N\|_1\,H(\log Q_0)\,\mathcal A_{\mathrm{min}}
\le
\mathcal E_{\mathrm{shift}}.
$$

This is the cleanest form of the threshold closure.

## Kernel Mass Input

The deterministic mass is

$$
\|\Omega_N\|_1
\le
\int_{|\beta|\le\rho}
|K_N(c+\beta)|^2\,d\beta
$$

for the relevant packet center or projected window. Using

$$
|K_N(\alpha)|\ll \min(N,\|\alpha\|^{-1}),
$$

this mass is explicit once `c` and `rho` are fixed.

## Remaining Inputs

The `L^infty` closure now needs:

1. a kernel-window mass bound for `||Omega_N||_1`;
2. major validity radii large enough to control `rho_max(q)`;
3. a residual endpoint minor-arc mass bound `A_min`;
4. the shifted-kernel budget `E_shift`.

No additional divisor-kernel exponential-sum input remains after the
variation lemma.

## If the Test Fails

If

$$
\|\Omega_N\|_1
\mathcal S(Q_0,H,\rho_{\max})
\mathcal A_{\mathrm{min}}
>
\mathcal E_{\mathrm{shift}},
$$

then the `L^infty` threshold route is insufficient. The remaining options are:

1. improve the kernel mass by projected aperture cancellation;
2. improve `A_min` by stronger residual minor-arc estimates;
3. use the `L^2` divisor-kernel route with an independent residual endpoint
   `L^4` moment.

## Minimal Lemma

> **Post-Variation Shift-Kernel Closure Lemma.**  
> At `H=rho^{-1}`, after substituting
> `V_q << ||Omega_N||_1`, the shifted-kernel minor contribution is bounded by
> the aperture budget if
> \[
> \|\Omega_N\|_1
> \mathcal S(Q_0,H,\rho_{\max})
> \mathcal A_{\mathrm{min}}
> \le
> \mathcal E_{\mathrm{shift}}.
> \]

## Result

The divisor-kernel minor branch has been reduced to one scalar inequality.
The remaining quantities are kernel-window mass, admissible major radius,
residual endpoint minor `L2` mass, and the shifted-error budget.
