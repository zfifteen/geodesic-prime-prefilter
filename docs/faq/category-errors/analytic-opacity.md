# Does analytic opacity weaken the arithmetic source?

## Short Answer

No. Difficulty reading a structure through analytic continuation does not erase
the integer structure being recorded.

## Source Order

```text
divisor counts -> zero-excess returns -> prime gap structure -> zeta compression -> RH language
```

## Common Mistake

The mistake is to confuse opacity in the compressed representation with absence
in the source.

## Full Answer

The integer source is the divisor-count field. It is not defined by how easily
one reads it through a complex function. It is defined by exact arithmetic on
the integers.

Zeta compression is powerful because it packages multiplicative arithmetic into
analytic form. That compression also changes the view. A property that is
plainly carried by the integer field can become hard to see after analytic
continuation.

That difficulty belongs to the representation. It is not evidence that the
source is incomplete. Prime gap structure keeps the carrier object in view:
divisor counts place primes, order gap interiors, and produce the analytic
object later read in zeta language.

Zero-excess sharpens the carrier object without moving it into the analytic
layer. It rewrites the same divisor-count source as
$E(n)=((\tau(n)/2)-1)\log n$, with prime returns at $E(n)=0$ only under the
`n>1` guard.

## Status

- explanatory consequence: analytic opacity is a property of the compressed
  view.
- exact coordinate reformulation: zero-excess is integer-side, not an analytic
  opacity claim.
- exact zeta compression: the bridge identifies what the compressed view
  records.

## Related Docs

- [What does zeta compression record?](../core-frame/zeta-compression.md)
- [Does zeta have its own arithmetic supply?](../zeta-compression/no-private-arithmetic-supply.md)
- [Why does the carrier object matter?](../analogies/carrier-object-car-wash.md)
