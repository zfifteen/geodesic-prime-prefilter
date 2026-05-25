# First-Moment Endpoint Density For Shifted Offsets

Date: 2026-05-24

Status: candidate analytic input for the fourth-moment uncovered-set strategy.

The fourth-moment extinction argument needs a positive mean for the uncovered
survivor count. In PGS language this is endpoint-return density. In classical
analytic language it is a first-moment prime-counting lower bound for shifted
odd linear forms.

## Target

For even centers `M in [X,2X]`, define

$$
Z(M)=
\#\{0\le s<N:
M-(2s+1)\text{ has no odd prime divisor }\le\sqrt{2X}\}.
$$

Except for the `1` boundary, the surviving values are odd primes. The needed
mean is

$$
\sum_{\substack{X\le M\le2X\\2\mid M}}Z(M)
\gg
\frac{XN}{\log X}.
$$

Equivalently,

$$
\mu=\frac{2}{X}\sum_{2\mid M}Z(M)
\gg
\frac{N}{\log X}.
$$

## Shifted Prime Count

Fix an offset

$$
h=2s+1.
$$

The condition that `M-h` is an odd prime is equivalent to

$$
M=p+h
$$

with `p` odd prime. Since `h` is odd, `p+h` is even. Therefore parity imposes
no additional loss.

The count for this offset is

$$
\#\{M\in[X,2X]:2\mid M,\ M-h\in\mathbb P\}
=
\pi(2X-h)-\pi(X-h)+O(1),
$$

with the lower endpoint truncated at `2` when `X-h<2`.

For

$$
h\le X,
$$

the interval `[X-h,2X-h]` has length `X` and upper endpoint at least `X`.
The prime number theorem, or any Chebyshev-strength lower bound in dyadic
intervals, gives

$$
\pi(2X-h)-\pi(X-h)
\gg
\frac{X}{\log X}
$$

uniformly in this range.

Thus for

$$
2N-1\le X,
$$

one obtains

$$
\sum_{s<N}\#\{M:M-(2s+1)\in\mathbb P\}
\gg
\frac{XN}{\log X}.
$$

This supplies the required first moment in the interior offset regime
`N <= X/2`.

## Boundary Regime

When

$$
2s+1>X,
$$

the shifted interval has upper endpoint below `X`, and for offsets near `2X`
the positive part becomes short. The uniform lower bound

$$
\gg X/\log X
$$

per offset is no longer true.

This is a boundary issue in the dyadic parameterization, not a parity issue.
Possible treatments are:

1. restrict the fourth-moment argument to `N <= X/2` and handle longer
   offsets by a separate very-long-gap estimate;
2. re-dyadize centers relative to the shifted prime variable `M-h`;
3. use a known global prime-gap upper-tail input for the extreme range.

The RH bridge chain should keep this boundary case explicit.

## PGS Interpretation

In PGS terms, the lower bound says:

```text
among the first N odd offsets behind even centers in [X,2X],
zero-excess endpoints occur with total density at least XN/log X.
```

This is not supplied by the local GWR selected-minimum theorem. It is an
endpoint-return density input. If the bridge must remain PGS-internal, this
input must be reproved from the PGS endpoint chain rather than imported from
classical prime counting.

## Obstacles

**Analytic import.**
The clean proof uses the prime number theorem or a comparable lower bound for
primes in length-`X` intervals. That is external to `PROOF.md`.

**Uniform shift range.**
The lower bound is immediate for `h <= X`. Larger shifts require boundary
handling.

**Endpoint versus survivor language.**
Survival after sieving to `sqrt(2X)` is equivalent to primality only for
positive values. The `M-h <= 1` boundary must be removed before translating
survivors to zero-excess endpoints.

**Dyadic assembly.**
The fourth-moment note uses a single dyadic center block. If the offset length
is comparable to the block location, the proof may need a second dyadic
decomposition in the shifted prime variable.

## Minimal Input

The needed lemma is:

> **Shifted Endpoint Density Lemma.**
> For `N <= X/2`,
> $$
> \sum_{0\le s<N}
> \#\{M\in[X,2X]:2\mid M,\ M-(2s+1)\in\mathbb P\}
> \gg
> \frac{XN}{\log X}.
> $$

This gives the positive mean required for the fourth central moment
extinction argument in the interior offset regime.

## Result

The first-moment input is straightforward in the interior range: it is exactly
prime endpoint density for shifted odd forms. The remaining issue is not
parity; it is the long-offset dyadic boundary and whether this density input
is imported analytically or proved from PGS endpoint structure.
