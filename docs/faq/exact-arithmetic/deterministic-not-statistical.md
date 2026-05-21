# Is prime gap structure exact arithmetic or trend language?

## Short Answer

Prime gap structure is exact arithmetic. It reads divisor counts directly from
the integers and uses exact conditions, not candidate scoring or distribution
estimates, to place the next prime.

## Source Order

```text
divisor counts -> prime gap structure -> zeta compression -> RH language
```

## Common Mistake

The mistake is to treat prime placement as if it were inferred from aggregate
frequency. The next prime is placed by an exact divisor-count condition.

## Full Answer

For `n>1`, primality is equivalent to:

$$
\tau(n)=2.
$$

Given a known prime `p`, the next prime is:

$$
q=\min\{n>p:\tau(n)=2\}.
$$

That is an exact integer rule. The rule does not ask how frequently primes
occur on average. It checks the ordered divisor-count field and stops at the
first return to divisor count two.

The Divisor Normalization Identity makes the same fact visible as a fixed
level:

$$
Z(n)=n^{1-\tau(n)/2}.
$$

For `n>1`, primes are exactly the returns to `Z=1`. Composites sit below that
level.

## Status

- proved theorem: the direct next-prime rule is proved in `PROOF.md`.
- explanatory consequence: exact placement precedes density language.

## Related Docs

- [Root proof authority](../../../PROOF.md)
- [How does the next-prime placement rule work?](next-prime-placement.md)
- [What is the difference between density and exact placement?](../local-global/density-vs-placement.md)
