# DNI-To-Zeta Compression

[README](README.md) | [Pole placement](pole-placement.md) | [Off-critical pole exclusion](off-critical-pole-exclusion.md) | [Long bridge note](../../research/12-rh-bridge/docs/dni_rh_bridge.md)

The bridge starts with divisor counts on integers, passes through the local
zero-excess returns and local PGS theorems, compresses the same coefficient
field into zeta language, and then applies source-side residual closure before
reading the Riemann
Hypothesis as a pole-placement sentence for the continued DNI ratio.

Required source order:

```text
divisor counts -> zero-excess returns -> local theorems
-> DNI-to-zeta compression -> residual closure -> pole placement/RH sentence
```

## 1. Divisor Counts

Status: arithmetic source and exact zeta compression.

Let $\tau(n)$ be the number of positive divisors of $n$. The square of the
zeta function counts ordered factor pairs:

$$
\zeta(s)^2
= \left(\sum_{a \ge 1}\frac{1}{a^s}\right)
  \left(\sum_{b \ge 1}\frac{1}{b^s}\right)
= \sum_{a,b \ge 1}\frac{1}{(ab)^s}
= \sum_{n \ge 1}\frac{\tau(n)}{n^s}
$$

The coefficient of $n^{-s}$ is the number of ordered pairs $(a,b)$ with
$ab=n$.

| $n$ | ordered factor pairs $(a,b)$ | coefficient |
| --- | --- | --- |
| $1$ | $(1,1)$ | $\tau(1)=1$ |
| $2$ | $(1,2),(2,1)$ | $\tau(2)=2$ |
| $3$ | $(1,3),(3,1)$ | $\tau(3)=2$ |
| $4$ | $(1,4),(2,2),(4,1)$ | $\tau(4)=3$ |
| $6$ | $(1,6),(2,3),(3,2),(6,1)$ | $\tau(6)=4$ |
| $12$ | $(1,12),(2,6),(3,4),(4,3),(6,2),(12,1)$ | $\tau(12)=6$ |

This gives the divisor-count series

$$
D(s)=\sum_{n \ge 1}\frac{\tau(n)}{n^s}=\zeta(s)^2,
\qquad \mathrm{Re}(s)>1.
$$

## 2. Zero-Excess Returns And PGS Local Theorems

Status: exact coordinate reformulation for $E(n)$; proved theorem for the
local PGS results, controlled by [PROOF.md](../../PROOF.md).

The local PGS layer uses the same divisor-count field before any zeta
compression is introduced.

Define the zero-excess coordinate by

$$
E(n)=\left(\frac{\tau(n)}{2}-1\right)\log n.
$$

For `n > 1`, primes are exactly the zero-excess returns:

$$
E(n)=0 \iff \tau(n)=2.
$$

Given a known prime $p$, the direct deterministic next-prime theorem defines
the next prime by

$$
q=\min\{n>p:E(n)=0\}
=\min\{n>p:\tau(n)=2\}.
$$

Inside a nonempty prime-gap interior

$$
I=\{p+1,\ldots,q-1\},
$$

the Interior Maximizer Theorem defines the selected integer

$$
w=\min\{n\in I:\tau(n)=\min_{m\in I}\tau(m)\}
$$

and proves that $w$ is the unique maximizer of

$$
F(n)=\left(1-\frac{\tau(n)}{2}\right)\log n.
$$

Since

$$
F(n)=-E(n),
$$

the same theorem says that $w$ is the leftmost interior argmin of $E(n)$.

These are local integer theorems. They supply the source-side arithmetic
objects that the zeta series records after compression.

## 3. DNI-To-Zeta Compression

Status: exact zeta compression.

The DNI divisor normalization load is

$$
\kappa(n)=\frac{\tau(n)\log n}{e^2}.
$$

Zero-excess does not replace this load. It rewrites the same bridge load as

$$
H(n)=\log n+E(n)=\frac{\tau(n)\log n}{2}.
$$

Equivalently, `H(n)=log n+E(n)=tau(n)log(n)/2`.

Thus $H(n)=(e^2/2)\kappa(n)$. The zeta-compression identities below remain
the `D,K,R` identities; the numerator is not $E(n)$ alone.

Its Dirichlet series is

$$
K(s)=\sum_{n \ge 1}\frac{\kappa(n)}{n^s}
=\frac{1}{e^2}\sum_{n \ge 1}\frac{\tau(n)\log n}{n^s}.
$$

Differentiate the divisor-count series on $\mathrm{Re}(s)>1$:

$$
D'(s)
=-\sum_{n \ge 1}\frac{\tau(n)\log n}{n^s}.
$$

Therefore

$$
K(s)=-\frac{1}{e^2}D'(s).
$$

Using $D(s)=\zeta(s)^2$, the normalized DNI ratio is

$$
R(s)=\frac{e^2}{2}\frac{K(s)}{D(s)}
=-\frac{1}{2}\frac{D'(s)}{D(s)}
=-\frac{\zeta'(s)}{\zeta(s)}.
$$

The quotient $K(s)/D(s)$ is a Dirichlet-series quotient, not coefficientwise
division. The two series are first summed as analytic functions on
$\mathrm{Re}(s)>1$, and the quotient is taken at the function level.

## 4. Pole Placement

Status: explanatory consequence.

The Euler product gives the logarithmic derivative identity

$$
-\frac{\zeta'(s)}{\zeta(s)}
=\sum_{n \ge 1}\frac{\Lambda(n)}{n^s},
\qquad \mathrm{Re}(s)>1,
$$

where

$$
\Lambda(n)=
\begin{cases}
\log p, & n=p^k \text{ for a prime } p \text{ and integer } k\ge 1,\\
0, & \text{otherwise}.
\end{cases}
$$

So the DNI ratio recovers the classical prime-power detector:

$$
R(s)=\sum_{n \ge 1}\frac{\Lambda(n)}{n^s}.
$$

| $n$ | type | $\Lambda(n)$ |
| --- | --- | --- |
| $2$ | prime $2$ | $\log 2$ |
| $3$ | prime $3$ | $\log 3$ |
| $4$ | prime power $2^2$ | $\log 2$ |
| $6$ | ordinary composite | $0$ |
| $8$ | prime power $2^3$ | $\log 2$ |
| $9$ | prime power $3^2$ | $\log 3$ |
| $10$ | ordinary composite | $0$ |
| $12$ | ordinary composite | $0$ |

After meromorphic continuation, the poles of $R(s)$ are the logarithmic
derivative record of the pole and zeros of $\zeta(s)$:

- the pole at $s=1$ gives the prime-number-theorem pole;
- the trivial zeros of $\zeta(s)$ give trivial poles of $R(s)$;
- the nontrivial zeros of $\zeta(s)$ give nontrivial poles of $R(s)$.

## 5. RH Sentence

Status: source-side residual closure read in pole-placement language.

Since

$$
R(s)=\frac{e^2}{2}\frac{K(s)}{D(s)}
=-\frac{\zeta'(s)}{\zeta(s)},
$$

the Riemann Hypothesis becomes the downstream pole-placement statement:

all nontrivial poles of the continued DNI ratio

$$
\frac{e^2}{2}\frac{K(s)}{D(s)}
$$

lie on the critical line

$$
\mathrm{Re}(s)=\frac{1}{2}.
$$

The exact identities are the zeta-compression layer. The pole-placement
sentence is the RH interpretation of that exact compressed ratio after the
source-side residual test closes failed identities, independent gap-length
freedom, chamber log-weight remainders, and extra divisor-count fields.

The zero-excess floor is the integer-side coordinate for prime returns. The
critical line is the zeta-side coordinate for nontrivial pole placement.
Analogy is allowed; identity is not.
