# Why can the Prime Number Theorem describe density without placing the next prime?

## Short Answer

The Prime Number Theorem describes the average density of primes. It does not
identify the next integer where the divisor count returns to two.

## Source Order

```text
divisor counts -> prime gap structure -> zeta compression -> RH language
```

## Common Mistake

The mistake is to confuse a density description with an exact placement rule.

## Full Answer

The Prime Number Theorem says that the number of primes up to `x` grows like:

$$
\frac{x}{\log x}.
$$

That is a global density statement. It describes the broad rate at which primes
thin out as numbers grow.

Prime gap structure answers a different question. Given a known prime `p`, the
next prime is:

$$
q=\min\{n>p:\tau(n)=2\}.
$$

That rule identifies the exact next return to the prime divisor-count state.
The density theorem does not do that. It gives global scale. The divisor-count
rule gives exact local placement.

## Status

- proved theorem: direct next-prime placement is proved in `PROOF.md`.
- explanatory consequence: density language is downstream from exact
  placement.

## Related Docs

- [Root proof authority](../../../PROOF.md)
- [What is the difference between density and exact placement?](density-vs-placement.md)
- [How does the next-prime placement rule work?](../exact-arithmetic/next-prime-placement.md)
