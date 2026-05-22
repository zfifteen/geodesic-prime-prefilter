# Why is pole placement not the first object?

## Short Answer

Pole placement is analytic language introduced after zeta compression. The
first object is the integer divisor-count structure that places primes and
orders prime-gap interiors.

## Source Order

```text
divisor counts -> zero-excess returns -> prime gap structure -> zeta compression -> RH language
```

## Common Mistake

The mistake is to begin with the pole sentence and demand that the integer
source re-prove itself in downstream coordinates.

## Full Answer

The prime gap source is concrete. Given a known prime `p`, the next prime is:

$$
q=\min\{n>p:\tau(n)=2\}.
$$

Inside the gap, the divisor counts form a finite ordered profile. The first
place where the smallest interior divisor count occurs is the selected integer
and the unique maximizer of the logarithmic comparison score. In zero-excess
coordinates this is the leftmost argmin of $E$, since $F(n)=-E(n)$.

The pole-placement sentence belongs to the analytic compression of that
structure. It is a coordinate description in the zeta layer. Treating it as the
first object places the shadow before the thing casting it.

The zero-excess floor and the critical line are different objects. The
zero-excess floor is integer-side. The critical line is zeta-side. Pole
placement cannot be made first by renaming the integer-side floor.

The proof burden in prime gap structure is carried by the integer structure:
divisor counts, prime returns, gap interiors, and their exact ordering. Zeta
language records the consequence.

## Status

- proved theorem: source-side local prime placement and interior ordering.
- exact coordinate reformulation: zero-excess restates the integer-side
  comparison.
- exact zeta compression: the DNI ratio recovers the classical analytic
  detector.
- explanatory consequence: pole language is downstream.

## Related Docs

- [Root proof authority](../../../PROOF.md)
- [Why is analytical-proof expectation the wrong frame?](analytical-proof-expectation.md)
- [DNI-to-zeta bridge](../../../research/12-rh-bridge/docs/dni_rh_bridge.md)
- [What should a reviewer check first?](../reviewer-guidance/evaluation-order.md)
