# Fourth Central Moment Assembly Obstruction

Date: 2026-05-24

Status: algebraic assembly note for converting tuple bounds into extinction.

The fixed-tuple Selberg bounds and graph-rank singular averages give raw upper
bounds for tuple counts. The extinction argument needs a centered fourth
moment. That conversion is not automatic: central moments require cancellation
between raw moments, not only upper bounds for them.

## Normalization

Let the probability space be even centers

$$
M\in[X,2X].
$$

Write

$$
Z(M)=\sum_{0\le s<N}I_s(M),
$$

where `I_s(M)` is the survivor indicator for the shifted odd form
`M-(2s+1)`.

Let

$$
\mu=\mathbb E Z.
$$

The endpoint-density input gives

$$
\mu\gg N/\log X
$$

in the non-boundary range.

The desired centered estimate is

$$
\mathbb E|Z-\mu|^4
\ll
\mu^2(\log X)^C.
$$

Then

$$
\mathbb P(Z=0)
\le
\frac{\mathbb E|Z-\mu|^4}{\mu^4}
\ll
\frac{(\log X)^C}{\mu^2}
\ll
\frac{(\log X)^{C+2}}{N^2}.
$$

## Factorial Moment Algebra

Use falling factorials

$$
(Z)_k=Z(Z-1)\cdots(Z-k+1)
$$

and write

$$
F_k=\mathbb E (Z)_k.
$$

The raw powers satisfy

$$
\mathbb E Z^2=F_1+F_2,
$$

$$
\mathbb E Z^3=F_1+3F_2+F_3,
$$

and

$$
\mathbb E Z^4=F_1+7F_2+6F_3+F_4.
$$

The centered fourth moment is

$$
\mathbb E(Z-\mu)^4
=
\mathbb E Z^4
-4\mu\,\mathbb E Z^3
+6\mu^2\,\mathbb E Z^2
-3\mu^4.
$$

Thus the desired bound follows if the factorial moments have Poisson-scale
accuracy through order four:

$$
F_k=\mu^k+O_k(\mu^{k-1}(\log X)^C)
\qquad
(2\le k\le4).
$$

Under these estimates all fourth-power terms cancel and the remainder is
`O(mu^2 log^C X)`.

## What Selberg Upper Bounds Give

The fixed-tuple Selberg upper bound plus singular-series average gives
upper bounds of the form

$$
F_k\ll_k
\mu^k(\log X)^C
+
\text{diagonal terms}.
$$

This is not enough by itself. Substituting only upper bounds into the raw
moment formula gives at best

$$
\mathbb E(Z-\mu)^4\ll \mu^4(\log X)^C,
$$

which yields no inverse-square extinction tail.

The assembly therefore needs one additional ingredient beyond upper-bound
sieve estimates.

## Candidate Assembly Inputs

### 1. Factorial Moment Asymptotics

Prove two-sided estimates

$$
F_k=\mu^k+O_k(\mu^{k-1}(\log X)^C)
\qquad
(2\le k\le4).
$$

This is the cleanest algebraic input. It is also the strongest: for `k=2`,
it includes pair-correlation information for shifted endpoints.

### 2. Direct Fourth-Moment Sieve Inequality

Prove directly that

$$
\sum_{2\mid M}|Z(M)-\mu|^4
\ll
X\mu^2(\log X)^C
$$

using a Selberg-Turan or large-sieve style concentration estimate. This avoids
stating individual factorial-moment asymptotics, but it must still supply the
same cancellation.

### 3. Weighted Endpoint Surrogate

Replace prime indicators by a weighted endpoint majorant or von Mangoldt-type
weight whose fourth moment is accessible, then transfer back to zero-excess
endpoint existence. This changes the object and would need a careful
majorization step to preserve the extinction implication.

## Obstacles

**Upper bounds do not center.**
The current tuple Selberg estimates are one-sided. Centering requires either
matching lower/asymptotic information or a direct concentration theorem.

**Prime-pair information enters.**
Even the second factorial moment asks how often two shifted odd forms survive
together. A pure upper-bound sieve does not determine this frequency.

**Diagonal terms must match the mean.**
The identities for `Z^k` include lower-order diagonal terms. These are
harmless only if they are kept with the correct coefficients in the factorial
moment expansion.

**Small-mean regime.**
When `mu` is small, the desired `H^-2` bound can be trivial after increasing
the logarithmic exponent. The central-moment assembly should be applied only
in the nontrivial range where `mu` is large enough.

## Minimal Remaining Statement

The exact missing assembly input is:

> **Fourth-Moment Endpoint Concentration Lemma.**
> In the range `N <= X/2` where `mu >> N/log X`, the survivor count satisfies
> $$
> \mathbb E|Z-\mu|^4
> \ll
> \mu^2(\log X)^C.
> $$

This lemma can be proved either by factorial-moment asymptotics through order
four or by a direct concentration inequality. It is not supplied by upper-bound
Selberg estimates alone.

## Result

The algebraic assembly step exposes a new precise obstruction. The remaining
work is not just fixed-tuple upper bounds; it is fourth-moment concentration
for endpoint survivors. Once that concentration lemma is supplied, the
uncovered-set extinction tail follows immediately.
