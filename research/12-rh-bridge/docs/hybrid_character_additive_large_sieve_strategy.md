# Hybrid Character-Additive Large-Sieve Strategy

Date: 2026-05-24

Status: candidate proof strategy for the large-sieve input behind the
kernel-weighted maximal BDH lemma.

The target large-sieve estimate has the form

$$
\sum_{q\le Q_0}
\sum_{\chi\bmod q}^{*}
\int_{|\beta|\le\rho}
\left|
\sum_{X<n\le2X}
a_n\chi(n)e(\beta n)
\right|^2
\Omega_{q,\chi,N}(\beta)\,d\beta
\ll
\mathcal B_{\mathrm{AP}}^K.
$$

Here `a_n` is the residual centered prime or von Mangoldt coefficient after
major-packet subtraction.

## Primal Large-Sieve Route

Ignore the weight first. A hybrid character/additive large sieve should give

$$
\sum_{q\le Q_0}\sum_{\chi\bmod q}^{*}
\int_{|\beta|\le\rho}
\left|\sum_n a_n\chi(n)e(\beta n)\right|^2d\beta
\ll
(X+Q_0^2+\rho^{-1})\sum_n|a_n|^2.
$$

The terms have the usual meanings:

1. `X` is sequence length;
2. `Q_0^2` is the multiplicative character conductor cost;
3. `rho^{-1}` is the additive frequency-window cost.

The interval-kernel weight is then inserted by dyadic decomposition or by a
weighted large-sieve inequality.

## Weighted Window Handling

The weight `Omega` comes from `|K_N(a/q+beta)|^2` after resolving the
`a`-dependent packet weights. Two sufficient treatments are available.

**Dyadic weight decomposition.**
Split `Omega` into levels where `Omega asymp L^2`, apply the unweighted
hybrid large sieve on each level, and sum with the measured support of that
level.

**Weighted large sieve.**
Prove directly

$$
\sum_{q,\chi}
\int
|S_{\chi}(\beta)|^2\Omega_{q,\chi,N}(\beta)\,d\beta
\ll
(X+\mathcal Q_{\Omega})
\sum_n|a_n|^2,
$$

where `Q_Omega` is the reciprocal spacing/overlap cost of the weighted
windows.

## Dual Expansion

Expanding the square gives

$$
\sum_{n,m}
a_n\overline{a_m}
\sum_{q\le Q_0}\sum_{\chi\bmod q}^{*}
\chi(n)\overline{\chi(m)}
\int_{|\beta|\le\rho}
\Omega_{q,\chi,N}(\beta)e(\beta(n-m))\,d\beta .
$$

Character orthogonality imposes congruence structure between `n` and `m`,
while the beta integral localizes the additive difference `n-m` at scale
`rho^{-1}`.

Thus the dual form is a weighted shifted-congruence correlation:

$$
n\equiv m\pmod q,
\qquad
|n-m|\lesssim \rho^{-1},
$$

with kernel weights. This is the exact mean-value object behind the hybrid
large sieve.

## Major-Packet Subtraction

The coefficient `a_n` must have the principal, exceptional, and coherent
low-conductor components removed before the large sieve is applied. Otherwise
the dual diagonal and low-conductor congruence classes contain major energy
that belongs to the packet model, not to the residual error.

After subtraction, the large sieve estimates residual oscillation.

## Required Inputs

The proof needs:

1. multiplicative large sieve for primitive and imprimitive characters up to
   `Q_0`;
2. additive large sieve or Gallagher-type window estimate for
   `|beta| <= rho`;
3. weighted-window control for `|K_N|^2`;
4. dyadic decomposition with bounded overlap of rational windows;
5. character bookkeeping for principal and exceptional terms removed into
   the major packet model.

## Minimal Lemma

> **Hybrid Kernel-Weighted Large-Sieve Lemma.**  
> For residual endpoint coefficients after major-packet subtraction,
> \[
> \sum_{q\le Q_0}\sum_{\chi\bmod q}^{*}
> \int_{|\beta|\le\rho}
> \left|\sum_{X<n\le2X}a_n\chi(n)e(\beta n)\right|^2
> \Omega_{q,\chi,N}(\beta)\,d\beta
> \]
> is bounded by the kernel-weighted BDH budget at
> `rho=c0/L_crit(d,N)`.

## Result

The hybrid large-sieve input is a combined multiplicative/additive
mean-value theorem. In primal form it estimates character sums over
continuous windows. In dual form it controls shifted congruence correlations
`n == m mod q` with `|n-m|` limited by the aperture width, after coherent
major packet components have been removed.
