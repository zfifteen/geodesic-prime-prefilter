# What role do divisor counts play?

## Short Answer

Divisor counts are the integer data that distinguish primes from composites and
organize the interiors of prime gaps.

## Source Order

```text
divisor counts -> zero-excess returns -> prime gap structure -> zeta compression -> RH language
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

The same condition in Zero-Excess DNI coordinates is:

$$
E(n)=\left(\frac{\tau(n)}{2}-1\right)\log n.
$$

For `n>1`, $E(n)=0$ exactly at primes. The value `n=1` is excluded by that
guard. Zero-excess is an exact coordinate reformulation of divisor counts, not
a new theorem.

Composite integers have more than two positive divisors. Inside a prime gap,
every interior integer is composite, so every interior divisor count is greater
than two. The ordered list of those counts is not blank space. It is the
interior arithmetic structure of the gap.

The gap-interior theorem uses that structure. It selects the first interior
integer where the smallest divisor count in the gap appears. That point is the
unique maximizer of the logarithmic comparison score used in `PROOF.md`. In
zero-excess coordinates, the same comparison is $F(n)=-E(n)$, so the selected
integer is the leftmost interior argmin of $E$.

## Status

- proved theorem: divisor-count traversal places the next prime.
- proved theorem: the first minimum-divisor interior point is the unique
  maximizer under the stated hypotheses.
- exact coordinate reformulation: zero-excess restates the same divisor-count
  source.

## Related Docs

- [Root proof authority](../../../PROOF.md)
- [Why do ordered gap interiors matter?](ordered-gap-interiors.md)
- [What is the source object?](../core-frame/source-object.md)
