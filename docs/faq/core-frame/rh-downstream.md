# Why is RH downstream?

## Short Answer

RH is downstream because it is classical analytic language for a structure that
already exists at the integer level. Prime gap structure begins with divisor
counts, zero-excess prime returns, and prime-gap interiors. Zeta language
records that source after compression.

## Source Order

```text
divisor counts -> zero-excess prime returns -> PGS local theorems
-> DNI-to-zeta compression -> source-side residual closure -> RH language
```

## Common Mistake

The mistake is to treat RH as the judge of the source structure. That reverses
the order. The source is the integer pattern. RH is the compressed analytic
description of that pattern.

## Full Answer

The Riemann Hypothesis is usually stated as a claim about the nontrivial zeros
of the zeta function:

$$
\mathrm{Re}(\rho)=\frac12.
$$

That is the classical coordinate sentence. Prime gap structure starts earlier.
It begins with the exact ordered divisor-count field:

$$
q=\min\{n>p:\tau(n)=2\}.
$$

In zero-excess coordinates, the same source-side return condition is:

$$
E(n)=\left(\frac{\tau(n)}{2}-1\right)\log n=0
\quad (n>1).
$$

That rule places the next prime after a known prime. The gap interior then has
an ordered divisor-count profile, and the first occurrence of the smallest
interior divisor count is the unique maximizer of the logarithmic comparison
score.

The zero-excess floor is source-side. It is the integer-side return level where
the divisor-count source reaches prime state. The RH critical line is
zeta-side. It is the analytic coordinate sentence after compression. The two
belong to the same source-to-compression relation, but they are not the same
object.

The zeta function records multiplicative arithmetic in compressed analytic
form. On $\mathrm{Re}(s)>1$, the DNI-to-zeta bridge shows that divisor-count
structure recovers the classical prime-power detector:

$$
R(s)=\frac{e^2}{2}\frac{K(s)}{D(s)}=-\frac{\zeta'(s)}{\zeta(s)}.
$$

That identity puts the analytic language after the integer source. RH is the
zeta-side description of the source, not the origin of the source.

## Status

- proved theorem: exact local prime placement and ordered gap interior theorem.
- exact coordinate reformulation: Zero-Excess DNI rewrites the prime return
  as $E(n)=0$ for `n>1`.
- exact zeta compression: the DNI bridge recovers $-\zeta'(s)/\zeta(s)$.
- source-side residual closure: RH-facing closure belongs after local PGS
  closure and exact DNI-to-zeta compression.
- explanatory consequence: RH language is downstream of the integer source.

## Related Docs

- [DNI-to-zeta bridge](../../../research/12-rh-bridge/docs/dni_rh_bridge.md)
- [The Riemann Hypothesis Is Obsolete](../../essays/the-riemann-hypothesis-is-obsolete.md)
- [What is the source object?](source-object.md)
