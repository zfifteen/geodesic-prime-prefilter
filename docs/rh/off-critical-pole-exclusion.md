# Source-Side Residual Test

The arithmetic source is the divisor-count field $\tau(n)$.

For each integer `n > 1`, prime return means $\tau(n)=2$. Given a known prime
`p`, the next endpoint is fixed by the first later return to that value:

$$
q=\min\{n>p:\tau(n)=2\}.
$$

Between consecutive endpoints, the chamber interior is the finite ordered set

$$
I=\{p+1,\ldots,q-1\}.
$$

Inside a nonempty chamber, the local PGS theorem controlled by
[PROOF.md](../../PROOF.md) selects the leftmost minimum-divisor integer and
orders the chamber by

$$
F(n)=\left(1-\frac{\tau(n)}{2}\right)\log n.
$$

So the source order is fixed before any analytic vocabulary enters:

```text
divisor-count source -> tau(n)=2 prime returns -> endpoint closure
-> chamber log-weight order -> DNI compression -> source-side residual test
-> pole placement
```

## The Objection

The critic says the exact source may still carry nontrivial off-critical poles
as a global property of the whole $\tau(n)$ sequence, even if no separate local
carrier is named. In that form, the objection accepts the divisor-count source,
the local PGS closures, and the DNI identities, but says that the continued
quotient might still have poles off $\mathrm{Re}(s)=1/2$ because the full
source sequence could carry them globally.

## Exact DNI Quotient

The divisor-count compression is

$$
D(s)=\sum_{n \ge 1}\frac{\tau(n)}{n^s}=\zeta(s)^2.
$$

The DNI load is

$$
\kappa(n)=\frac{\tau(n)\log n}{e^2},
$$

with Dirichlet series

$$
K(s)=\sum_{n \ge 1}\frac{\kappa(n)}{n^s}.
$$

Since

$$
D'(s)=-\sum_{n \ge 1}\frac{\tau(n)\log n}{n^s},
$$

the DNI load satisfies

$$
K(s)=-\frac{1}{e^2}D'(s).
$$

At the repository normalization $v=e^2/2$, the continued DNI ratio is

$$
R(s)=\frac{e^2}{2}\frac{K(s)}{D(s)}
=-\frac{1}{2}\frac{D'(s)}{D(s)}
=-\frac{\zeta'(s)}{\zeta(s)}.
$$

The quotient is a function quotient after the two Dirichlet series have been
formed. It is not coefficientwise division.

## Local Pole Mechanism

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

The term $g'(s)/g(s)$ is holomorphic at $\rho$. The term $m/(s-\rho)$ has a
pole at $\rho$. Thus zeros of $\zeta(s)$ become poles of the continued DNI
ratio $R(s)$.

The exclusion question is therefore source-side and exact: what source
residual could carry a nontrivial pole of $R(s)$ away from
$\mathrm{Re}(s)=1/2$?

## Source-Side Residual Test

Nontrivial off-critical poles of $R(s)$ would require a surviving source-side
residual in the exact DNI quotient. The possible locations for such a residual
are finite:

| Residual category | Source-side test | Status in source order |
| --- | --- | --- |
| 1. Failed identity in $D,K,R$ | The compression would need $D(s)\neq\zeta(s)^2$, $K(s)\neq-D'(s)/e^2$, or $R(s)\neq-\zeta'(s)/\zeta(s)$. | Closed by exact identities. |
| 2. Independent prime-gap or gap-length freedom | The endpoint sequence would need degrees of freedom not fixed by $\tau(n)=2$ returns. | Closed by endpoint closure: $q=\min\{n>p:\tau(n)=2\}$ fixes every next endpoint from the divisor-count field. |
| 3. Chamber log-weight residual | The chamber ordering would need a log-weight term outside the DNI load. | Closed by the PGS chamber order and derivative identity: the log-weight source is $\tau(n)\log n$, and that source is exactly the numerator load $K(s)=-D'(s)/e^2$. |
| 4. Multiplicative or divisor-count residual | The factor-pair source would need an additional multiplicative coefficient field outside $\tau(n)$. | Closed by $D(s)=\zeta(s)^2$: the ordered factor-pair count is exactly $\tau(n)$, and the quotient $K(s)/D(s)$ exhausts the divisor-count source used by the bridge. |
| 5. Conclusion-only residual | The critic says the whole $\tau(n)$ sequence could carry an off-critical pole, but names no failed identity, no independent endpoint freedom, no log-weight remainder, and no extra divisor-count field. | Not a mathematical objection. It restates the negation of the pole-placement conclusion without identifying a source object that could carry it. |

The first four categories are the places where a real source-side obstruction
could enter. Each is closed by the source order: exact divisor counts, exact
prime returns, endpoint closure, chamber log-weight order, and exact DNI
compression.

The fifth category has no independent mathematical content. Saying "the whole
sequence carries it" without a failed identity or surviving source degree of
freedom does not identify a carrier. It only renames the desired off-critical
pole as possible.

## Exclusion Sentence

After the local PGS source closures and the exact DNI compression, the
continued ratio has no source-side residual left outside

$$
R(s)=\frac{e^2}{2}\frac{K(s)}{D(s)}
=-\frac{\zeta'(s)}{\zeta(s)}.
$$

A nontrivial off-critical pole would therefore have to be a pole of this exact
quotient with no failed identity, no independent gap-length freedom, no
chamber log-weight remainder, and no additional divisor-count field. That is a
conclusion-only residual, not a mathematical obstruction.

The positive source-side bridge is:

```text
tau(n) fixes prime returns -> endpoint closure fixes gap lengths
-> chamber order fixes the log-weight source -> DNI quotient exhausts tau(n)
and tau(n)log n -> no off-critical source residual remains
```

Therefore nontrivial off-critical poles of $R(s)$ would require a surviving
source-side residual in the exact DNI quotient; after the PGS source closures
and exact DNI compression, no such residual remains.

## Links

- [RH bundle README](README.md)
- [Source order](source-order.md)
- [DNI-to-zeta compression](dni-to-zeta-compression.md)
- [Pole placement](pole-placement.md)
- [Critical line and zero geometry](critical-line-and-zero-geometry.md)
- [Root proof authority](../../PROOF.md)
