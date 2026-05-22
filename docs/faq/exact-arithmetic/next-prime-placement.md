# How does the next-prime placement rule work?

## Short Answer

Starting from a known prime `p`, inspect the integers greater than `p` in
order. The next prime `q` is the first integer with exactly two positive
divisors.

## Source Order

```text
divisor counts -> zero-excess returns -> prime gap structure -> zeta compression -> RH language
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
E(n)=\left(\frac{\tau(n)}{2}-1\right)\log n.
$$

For `n>1`, $E(n)=0$ exactly when $\tau(n)=2$. The next prime is the first
zero-excess return after `p`. This is the same exact placement rule in a
different coordinate.

The dual multiplicative coordinate is $Z(n)=e^{-E(n)}$.

## Status

- proved theorem: `PROOF.md` proves the direct deterministic next-prime rule.
- exact coordinate reformulation: zero-excess restates first return to
  $\tau(n)=2$.
- explanatory consequence: the rule explains exact placement before density
  language enters.

## Related Docs

- [Root proof authority](../../../PROOF.md)
- [What role do divisor counts play?](divisor-counts.md)
- [Why can the Prime Number Theorem describe density without placing the next prime?](../local-global/pnt-vs-exact-placement.md)
