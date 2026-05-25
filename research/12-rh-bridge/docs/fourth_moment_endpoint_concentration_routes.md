# Fourth-Moment Endpoint Concentration Routes

Date: 2026-05-24

Status: two-route comparison for the Fourth-Moment Endpoint Concentration
Lemma.

The survivor count is not only a sieve variable. For even centers, it is the
number of zero-excess endpoints in a backward short interval. This gives the
cleanest formulation of the remaining concentration input.

## Endpoint Count Form

For `N <= X/2` and even `M in [X,2X]`, the first `N` odd offsets are

$$
M-1,\ M-3,\ \ldots,\ M-(2N-1).
$$

Survival through all odd prime channels up to `sqrt(2X)` is equivalent, away
from the boundary already handled, to primality. Therefore

$$
Z_N(M)
=
\#\{p\in\mathbb P:M-2N<p<M\}
+O(1).
$$

The Fourth-Moment Endpoint Concentration Lemma is therefore a short-interval
prime endpoint moment:

$$
\sum_{\substack{X\le M\le2X\\2\mid M}}
\left|
Z_N(M)-\mu_N
\right|^4
\ll
X\mu_N^2(\log X)^C,
\qquad
\mu_N\asymp N/\log X.
$$

This is the exact input needed for the `H^-2` extinction tail.

## Route 1: Factorial-Moment Asymptotics

Prove, for `2 <= k <= 4`,

$$
F_k=\mathbb E(Z_N)_k
=
\mu_N^k+O_k(\mu_N^{k-1}(\log X)^C).
$$

This is equivalent to average prime-tuple control over all offset sets of size
up to four inside the interval length `2N`.

**Strength.**
It gives the desired fourth central moment by direct algebra.

**Obstacle.**
It requires two-sided prime-tuple information, not just Selberg upper bounds.
Even the pair term asks for genuine average control of endpoint pairs. This is
stronger than the current one-sided sieve machinery.

## Route 2: Direct Short-Interval Concentration

Prove the fourth central moment directly for endpoint counts in moving
intervals:

$$
\sum_{\substack{X\le M\le2X\\2\mid M}}
\left|
\#\{p:M-2N<p<M\}
-\frac{2N}{\log X}
\right|^4
\ll
X\left(\frac{N}{\log X}\right)^2(\log X)^C.
$$

This is a Selberg-Turan style concentration theorem for short intervals.

**Strength.**
It bypasses individual tuple asymptotics and targets exactly the needed
quantity.

**Obstacle.**
It is still a deep distributional statement about endpoints in short
intervals. The proof must control correlations strongly enough to get a
Poisson-scale fourth moment.

## Routes Outside This Note

Two other ideas are deliberately out of scope for this comparison:

```text
weighted von Mangoldt surrogate;
PGS endpoint-chain concentration.
```

Both may become useful later, but the present decision is between the two
routes requested for the survivor count itself: factorial-moment asymptotics
and direct concentration.

## Small-Mean Regime

If

$$
\mu_N\ll1,
$$

then `N` is polylogarithmically small after choosing the final logarithmic
exponent, and the extinction bound can be absorbed by the trivial count. The
concentration theorem is only needed in the range where

$$
\mu_N\gg1.
$$

## Minimal Remaining Lemma

The cleanest statement is:

> **Short-Interval Endpoint Fourth-Moment Lemma.**
> For `1 <= N <= X/2`,
> $$
> \sum_{\substack{X\le M\le2X\\2\mid M}}
> \left|
> \#\{p:M-2N<p<M\}
> -\frac{2N}{\log X}
> \right|^4
> \ll
> X\left(\frac{N}{\log X}\right)^2(\log X)^C
> $$
> in the nontrivial range, with small `N` handled trivially.

This lemma implies the Fourth-Moment Endpoint Concentration Lemma and hence
the shifted-sieve extinction estimate.

## Result

The remaining concentration input is a fourth moment for endpoint counts in
moving short intervals. The two live routes are factorial-moment asymptotics
and direct short-interval concentration. The direct concentration lemma is the
most precise target, while factorial-moment asymptotics give the cleanest
algebraic mechanism if the necessary two-sided endpoint correlations are
available.
