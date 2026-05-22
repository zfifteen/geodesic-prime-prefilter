# Pole Placement

The source object is the divisor-count field.

For each positive integer `n`, let $\tau(n)$ be the number of positive
divisors of `n`. Primes are exactly the returns to $\tau(n)=2$, and a prime
gap is the finite interval between two consecutive returns. The local PGS
theorems begin there: exact divisor counts determine the next prime, and the
gap interior is ordered by the leftmost minimum-divisor rule.

The RH-facing language enters only after this integer source is compressed into
Dirichlet-series form.

```text
divisor counts -> PGS local theorems -> DNI-to-zeta compression
-> source-side residual closure -> pole placement/RH sentence
```

## Source-To-Pole Ladder

The ladder is:

$$
\tau(n) \to D(s) \to K(s) \to R(s)=-\frac{\zeta'(s)}{\zeta(s)}
\to \text{source-side residual closure} \to \text{pole placement}.
$$

Start with the divisor-count Dirichlet series on $\mathrm{Re}(s)>1$:

$$
D(s)=\sum_{n \ge 1}\frac{\tau(n)}{n^s}=\zeta(s)^2.
$$

The DNI load is

$$
\kappa(n)=\frac{\tau(n)\log n}{e^2}.
$$

Its Dirichlet series is

$$
K(s)=\sum_{n \ge 1}\frac{\kappa(n)}{n^s}
=\frac{1}{e^2}\sum_{n \ge 1}\frac{\tau(n)\log n}{n^s}.
$$

Since

$$
D'(s)=-\sum_{n \ge 1}\frac{\tau(n)\log n}{n^s},
$$

the DNI load series satisfies

$$
K(s)=-\frac{1}{e^2}D'(s).
$$

At the repository normalization scaling parameter $v=e^2/2$, the continued DNI
ratio is

$$
R(s)=\frac{e^2}{2}\frac{K(s)}{D(s)}
=-\frac{1}{2}\frac{D'(s)}{D(s)}
=-\frac{\zeta'(s)}{\zeta(s)}.
$$

So pole placement is not an extra zeta-side object added to PGS. It is the
singularity geometry of the continued DNI ratio after the divisor-count source
has been compressed and the source-side residual test has closed off-critical
carriers.

## Singularity Ledger

The ledger for

$$
R(s)=-\frac{\zeta'(s)}{\zeta(s)}
$$

is exact.

| Location | Source in $\zeta(s)$ | Effect in $R(s)$ |
| --- | --- | --- |
| $s=1$ | simple pole of $\zeta(s)$ | the PNT pole of $R(s)$ |
| $s=-2,-4,-6,\ldots$ | trivial zeros of $\zeta(s)$ | trivial poles of $R(s)$ |
| $0<\mathrm{Re}(s)<1$ | nontrivial zeros of $\zeta(s)$ | nontrivial poles of $R(s)$ |

The pole at $s=1$ is the prime-number-theorem pole. The trivial zeros of
$\zeta(s)$ become trivial poles of $R(s)$. The nontrivial zeros become
nontrivial poles.

## Local Pole Proof

Let $\rho$ be a zero of $\zeta(s)$ of multiplicity $m$. Locally write

$$
\zeta(s)=(s-\rho)^m g(s),
$$

where $g(\rho)\neq 0$.

Then

$$
\frac{\zeta'(s)}{\zeta(s)}
=\frac{m}{s-\rho}+\frac{g'(s)}{g(s)}.
$$

Therefore

$$
-\frac{\zeta'(s)}{\zeta(s)}
=-\frac{m}{s-\rho}-\frac{g'(s)}{g(s)}.
$$

The second term is holomorphic at $\rho$ because $g(\rho)\neq 0$. The first
term has a pole at $\rho$. Hence every zero of $\zeta(s)$ becomes a pole of
$R(s)$, with residue determined by its multiplicity.

The same local computation also explains why this page uses pole language
instead of zero language: the DNI ratio does not carry zeros of $\zeta(s)$ as
zeros. It carries them as poles of its logarithmic derivative.

## RH Sentence

In the continued DNI-ratio language, the Riemann Hypothesis is the statement
that every nontrivial pole of

$$
R(s)=\frac{e^2}{2}\frac{K(s)}{D(s)}
$$

lies on

$$
\mathrm{Re}(s)=\frac{1}{2}.
$$

This sentence is downstream coordinate language. The source order remains:
divisor counts, local PGS theorems, DNI-to-zeta compression, source-side
residual closure, then pole-placement/RH language. PGS is not an analytical
method and does not require a classical zero-estimate or error-term proof to
close this sentence.

## Links

- [RH bundle README](README.md)
- [DNI-to-zeta compression](dni-to-zeta-compression.md)
- [Off-critical pole exclusion](off-critical-pole-exclusion.md)
- [Critical line and zero geometry](critical-line-and-zero-geometry.md)
- [Status ledger](status-ledger.md)
- [Full DNI-RH bridge note](../../research/12-rh-bridge/docs/dni_rh_bridge.md)
