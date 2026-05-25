# Pole Placement

The source object is the divisor-count field, read through the zero-excess
coordinate on the integer side.

For each positive integer `n`, let $\tau(n)$ be the number of positive
divisors of `n`, and define

$$
E(n)=\left(\frac{\tau(n)}{2}-1\right)\log n.
$$

For `n > 1`, primes are exactly the returns to $E(n)=0$, equivalently
$\tau(n)=2$. A prime gap is the finite interval between two consecutive
zero-excess returns. The local PGS theorems begin there: exact divisor counts
determine the next prime, and the gap interior is ordered by the leftmost
minimum-divisor rule.

The RH-facing language enters only after this integer source is compressed
into Dirichlet-series form.

```text
divisor counts -> zero-excess returns -> local theorems
-> DNI-to-zeta compression -> source-to-spectral target
-> pole placement/RH sentence
```

## Source-To-Pole Ladder

The ladder is:

$$
\tau(n) \to D(s) \to K(s) \to R(s)=-\frac{\zeta'(s)}{\zeta(s)}
\to \text{source-to-spectral placement target} \to \text{pole placement}.
$$

Start with the divisor-count Dirichlet series on $\mathrm{Re}(s)>1$:

$$
D(s)=\sum_{n \ge 1}\frac{\tau(n)}{n^s}=\zeta(s)^2.
$$

The DNI load is

$$
\kappa(n)=\frac{\tau(n)\log n}{e^2}.
$$

In zero-excess notation the bridge load is

$$
H(n)=\log n+E(n)=\frac{\tau(n)\log n}{2}.
$$

Equivalently, `H(n)=log n+E(n)=tau(n)log(n)/2`.

This preserves the existing bridge. `H(n)` is the scaled load behind `K(s)`;
`E(n)` alone is not substituted for the `D,K,R` identities.

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
has been compressed. The source-side residual test closes bookkeeping
failures in the bridge; it does not yet prove off-critical pole exclusion.

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
divisor counts, zero-excess returns, local PGS theorems, DNI-to-zeta
compression, the source-to-spectral placement target, then pole-placement/RH
language. The zero-excess floor is integer-side; the critical line is
zeta-side. Analogy is permitted, identity is not. A proof of the RH sentence
still requires a theorem that transmits PGS chamber geometry into pole
placement for the continued DNI ratio.

## Links

- [RH bundle README](README.md)
- [DNI-to-zeta compression](dni-to-zeta-compression.md)
- [Off-critical pole exclusion](off-critical-pole-exclusion.md)
- [Critical line and zero geometry](critical-line-and-zero-geometry.md)
- [Status ledger](status-ledger.md)
- [Full DNI-RH bridge note](../../research/12-rh-bridge/docs/dni_rh_bridge.md)
