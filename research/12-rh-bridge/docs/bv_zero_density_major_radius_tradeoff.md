# Bombieri-Vinogradov and Zero-Density Radius Tradeoff

Date: 2026-05-24

Status: candidate strategy for deriving major validity radii from averaged
or zero-density prime-distribution inputs.

The major validity radius `rho_valid(a/q)` is determined by the largest
radius on which the centered endpoint major approximation has
kernel-weighted error inside its assigned budget.

## Error Integral

Let

$$
E_q(X)=
\max_{(r,q)=1}
\sup_{x\le2X}
\left|
\psi(x;q,r)-{x\over\varphi(q)}
\right|.
$$

Partial summation gives the schematic endpoint error

$$
|\operatorname{Err}_{a/q}(\beta)|
\ll
{E_q(X)\over\log X}(1+X|\beta|).
$$

Define the kernel radius integral

$$
I_N(a/q,\rho)
=
\int_{|\beta|\le\rho}
(1+X|\beta|)^2
|K_N(a/q+\beta)|^2\,d\beta .
$$

Then `rho` is valid for the packet `a/q` if

$$
{E_q(X)^2\over(\log X)^2}
I_N(a/q,\rho)
\le
\mathcal E_{a,q,N}.
$$

Thus the radius/error tradeoff is explicit:

$$
\rho_{\mathrm{valid}}(a/q)
=
\sup\left\{
\rho:
{E_q(X)^2\over(\log X)^2}
I_N(a/q,\rho)
\le
\mathcal E_{a,q,N}
\right\}.
$$

## Bombieri-Vinogradov Route

Bombieri-Vinogradov supplies averaged control of `E_q(X)` over
`q <= Q_BV`, typically up to square-root scale with logarithmic loss. For the
kernel-weighted budget, the needed form is a square-mean or budget-weighted
variant:

$$
\sum_{q\le Q_0}
\sum_{(a,q)=1}
{E_q(X)^2\over(\log X)^2}
I_N(a/q,\rho_q)
\le
\sum_{q\le Q_0}\sum_{(a,q)=1}
\mathcal E_{a,q,N}.
$$

If only an `L^1` Bombieri-Vinogradov estimate is available, it must be paired
with a pointwise trivial bound for `E_q(X)` or upgraded to a square-mean
large-sieve form. The aperture argument is naturally quadratic because the
error budget is an `L^2` kernel-weighted budget.

This route proves enough major radius on average over packet centers.

## Zero-Density Route

Zero-density estimates give individual or averaged bounds for
`E_q(X)` through zeros of Dirichlet `L`-functions. Insert the resulting
bound into the same radius inequality:

$$
{E_q(X;\mathcal Z)^2\over(\log X)^2}
I_N(a/q,\rho)
\le
\mathcal E_{a,q,N}.
$$

The zero-density route is useful for transition moduli where the aperture
needs individual control or where BV is too averaged.

If an exceptional real character contributes a coherent term, that term must
be assigned to the major packet model rather than left in the error.

## Kernel Integral Requirement

The tradeoff also needs a deterministic bound for

$$
I_N(a/q,\rho).
$$

Using

$$
|K_N(\alpha)|\ll\min(N,\|\alpha\|^{-1}),
$$

one obtains a radius-dependent bound for each packet center. This bound must
be inserted before comparing with `c0/L_crit(d,N)`.

The aperture feasibility condition becomes:

$$
{c_0\over L_{\mathrm{crit}}(d,N)}
\le
\sup\left\{
\rho:
{E_q(X)^2\over(\log X)^2}
I_N(a/q,\rho)
\le
\mathcal E_{a,q,N}
\right\}.
$$

## Required Inputs

The BV/zero-density radius proof needs:

1. a budget allocation `E_{a,q,N}` over packet centers;
2. a deterministic bound for `I_N(a/q,rho)`;
3. a square-mean BV estimate or large-sieve AP estimate for the quadratic
   budget;
4. zero-density control for transition or individual moduli;
5. explicit treatment of exceptional coherent terms as major packet
   components.

## Minimal Lemma

> **BV/Zero-Density Major Radius Lemma.**  
> For every low-conductor packet center, the AP error estimates and kernel
> integral satisfy
> \[
> {E_q(X)^2\over(\log X)^2}
> I_N(a/q,c_0/L_{\mathrm{crit}}(d,N))
> \le
> \mathcal E_{a,q,N}
> \]
> for every failing dyadic `d`-slice, either pointwise by zero-density input
> or after summation over packet centers by a square-mean
> Bombieri-Vinogradov input.

## Result

The major validity radius is reduced to a quantitative AP-error budget. BV
or zero-density estimates must control `E_q(X)` strongly enough, after the
kernel integral `I_N(a/q,rho)`, to make the radius at least
`c0/L_crit(d,N)` for every band whose base kernel energy fails.
