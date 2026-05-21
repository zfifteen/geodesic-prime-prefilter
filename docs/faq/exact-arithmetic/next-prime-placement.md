# How does the next-prime placement rule work?

## Short Answer

Starting from a known prime `p`, inspect the integers greater than `p` in
order. The next prime `q` is the first integer with exactly two positive
divisors.

## Source Order

```text
divisor counts -> prime gap structure -> zeta compression -> RH language
```

## Common Mistake

The mistake is to treat next-prime placement as a prediction from a density law.
The placement rule is an exact first-return rule in the divisor-count field.

## Full Answer

The next-prime rule is:

$$
q=\min\{n>p:\tau(n)=2\}.
$$

Every integer between `p` and `q` is composite and therefore has divisor count
greater than two. The integer `q` has divisor count two. Because the integers
are inspected in order, the first return to divisor count two is the next
prime.

The normalized version says the same thing through the Divisor Normalization
Identity:

$$
Z(n)=n^{1-\tau(n)/2}.
$$

The next prime is the first return to `Z=1` after `p`.

## Status

- proved theorem: `PROOF.md` proves the direct deterministic next-prime rule.
- explanatory consequence: the rule explains exact placement before density
  language enters.

## Related Docs

- [Root proof authority](../../../PROOF.md)
- [What role do divisor counts play?](divisor-counts.md)
- [Why can the Prime Number Theorem describe density without placing the next prime?](../local-global/pnt-vs-exact-placement.md)
