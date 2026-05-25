# Direct Continuous-Frequency Large-Sieve Strategy

Date: 2026-05-24

Status: candidate proof strategy for the weighted additive large-sieve route
at the unified aperture scale.

Instead of decomposing the `a`-dependent kernel weight into characters, treat
the original Fourier frequencies directly:

$$
\alpha={a\over q}+\beta,
\qquad
q\le Q_0,\quad |\beta|\le R_{\mathrm{req}}.
$$

The target is a weighted additive large-sieve estimate for the residual
endpoint sum

$$
A(\alpha)=\sum_{X<n\le2X}a_n e(\alpha n)
$$

after major-packet subtraction.

## Weighted Frequency Measure

Define the measure

$$
d\mu(\alpha)
=
\sum_{q\le Q_0}\sum_{(a,q)=1}
|K_N(\alpha)|^2
\psi_{a,q}\!\left(\alpha-{a\over q}\right)
d\alpha,
$$

where `psi_{a,q}` is a smooth cutoff supported on

$$
\left|\alpha-{a\over q}\right|\le R_{\mathrm{req}}.
$$

The direct estimate is

$$
\int |A^{\perp}(\alpha)|^2\,d\mu(\alpha)
\le
\mathcal L_{\mu}\mathcal A_2.
$$

## Measure Large-Sieve Constant

A continuous large sieve controls `L_mu` by local concentration of `mu`. A
usable concentration norm is

$$
\mathfrak C_{\mu}(1/X)
=
\sup_{\theta}
\mu\left([\theta-1/X,\theta+1/X]\right).
$$

The expected bound has the form

$$
\mathcal L_{\mu}
\ll
X\mathfrak C_{\mu}(1/X)+\mu([0,1]).
$$

Thus the proof reduces to bounding total weighted mass and mass in
`1/X`-scale intervals.

## Frequency Spacing Inputs

The needed spacing facts are:

1. rational centers with `q <= Q_0` are separated by at least `Q_0^{-2}`;
2. the unified aperture radius satisfies `R_req <= cQ_0^{-2}`;
3. therefore the major windows have bounded overlap;
4. smoothing tails do not create high-overlap leakage.

With bounded overlap,

$$
\mu([0,1])
\ll
\sum_{q\le Q_0}\sum_{(a,q)=1}
\int_{|\beta|\le R_{\mathrm{req}}}
|K_N(a/q+\beta)|^2\,d\beta,
$$

and the local concentration is controlled by the largest kernel mass in a
short interval.

## Major-Packet Subtraction

The estimate is applied to `A^perp`, not the raw endpoint sum. Coherent
principal, exceptional, and low-conductor major packet components are removed
before applying the large sieve. The large sieve supplies an operator-norm
bound for the residual sequence.

## Closure Condition

The direct route closes if

$$
\left(
X\mathfrak C_{\mu}(1/X)+\mu([0,1])
\right)
\mathcal A_2
\le
(\log X)^2\mathcal E_{\mathrm{maj}}.
$$

This is the continuous-frequency version of

$$
\mathcal L_{\mathrm{hyb}}^{\Omega}\mathcal A_2
\le
(\log X)^2\mathcal E_{\mathrm{maj}}.
$$

## Minimal Lemma

> **Direct Weighted Additive Large-Sieve Lemma.**  
> For the kernel-weighted measure supported on
> `alpha=a/q+beta`, `q<=Q0`, `|beta|<=R_req`, the residual endpoint sum
> satisfies
> \[
> \int |A^{\perp}(\alpha)|^2d\mu(\alpha)
> \le
> (X\mathfrak C_{\mu}(1/X)+\mu([0,1]))\mathcal A_2,
> \]
> and this bound is at most `(log X)^2 E_maj`.

## Result

The direct continuous-frequency route bypasses the `a`-weighted character
orthogonality problem. It replaces it with a weighted additive large-sieve
constant determined by total kernel-window mass, local `1/X` concentration,
and rational-window spacing at the unified aperture radius.
