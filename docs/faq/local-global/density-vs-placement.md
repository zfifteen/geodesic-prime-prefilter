# What is the difference between density and exact placement?

## Short Answer

Density describes how many primes appear at a scale. Exact placement identifies
which integer is the next prime.

## Source Order

```text
divisor counts -> prime gap structure -> zeta compression -> RH language
```

## Common Mistake

The mistake is to use a global count as though it were a local placement rule.

## Full Answer

Density language answers questions like:

```text
How many primes appear up to x?
How large is the average gap near x?
How far is a counting function from a smooth approximation?
```

Exact placement answers a different question:

```text
Starting from this prime p, which integer is the next prime q?
```

The divisor-count rule answers exact placement:

$$
q=\min\{n>p:\tau(n)=2\}.
$$

Prime gap structure also reads the ordered composite interior between `p` and
`q`. That interior structure is not supplied by an average density law. It is
read directly from the integer divisor-count field.

## Status

- proved theorem: exact next-prime placement and gap-interior ordering.
- explanatory consequence: density descriptions do not replace the source
  structure.

## Related Docs

- [Why can the Prime Number Theorem describe density without placing the next prime?](pnt-vs-exact-placement.md)
- [How does the next-prime placement rule work?](../exact-arithmetic/next-prime-placement.md)
- [Why do ordered gap interiors matter?](../exact-arithmetic/ordered-gap-interiors.md)
