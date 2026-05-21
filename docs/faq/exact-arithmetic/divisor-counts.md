# What role do divisor counts play?

## Short Answer

Divisor counts are the integer data that distinguish primes from composites and
organize the interiors of prime gaps.

## Source Order

```text
divisor counts -> prime gap structure -> zeta compression -> RH language
```

## Common Mistake

The mistake is to treat divisor counts as decoration on top of primes. Divisor
counts are the exact arithmetic condition that marks primes and structures the
composite interior between them.

## Full Answer

The divisor count `tau(n)` is the number of positive divisors of `n`. For
`n>1`, the condition

$$
\tau(n)=2
$$

is exactly the prime condition.

Composite integers have more than two positive divisors. Inside a prime gap,
every interior integer is composite, so every interior divisor count is greater
than two. The ordered list of those counts is not blank space. It is the
interior arithmetic structure of the gap.

The gap-interior theorem uses that structure. It selects the first interior
integer where the smallest divisor count in the gap appears. That point is the
unique maximizer of the logarithmic comparison score used in `PROOF.md`.

## Status

- proved theorem: divisor-count traversal places the next prime.
- proved theorem: the first minimum-divisor interior point is the unique
  maximizer under the stated hypotheses.

## Related Docs

- [Root proof authority](../../../PROOF.md)
- [Why do ordered gap interiors matter?](ordered-gap-interiors.md)
- [What is the source object?](../core-frame/source-object.md)
