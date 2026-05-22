# Is prime gap structure a zeta-side method?

## Short Answer

No. Prime gap structure does not start inside the zeta frame. It starts with
the exact divisor-count structure of the integers.

## Source Order

```text
divisor counts -> zero-excess returns -> prime gap structure -> zeta compression -> RH language
```

## Common Mistake

The mistake is to ask how prime gap structure functions as a new analytic
technique for controlling zeros. That starts in the wrong place.

## Full Answer

A zeta-side method begins with analytic objects, such as zeros, poles, contour
integrals, or bounds on analytic error terms. Prime gap structure begins with
integer objects:

- the divisor-count field `tau(n)`;
- the prime return condition `tau(n)=2`;
- the zero-excess coordinate
  $E(n)=\left(\frac{\tau(n)}{2}-1\right)\log n$;
- the ordered composite interior between consecutive primes;
- the first interior point with the minimum divisor count.

Those objects define prime placement before zeta language enters. The zeta
bridge then records this source in analytic form.

Zero-excess does not turn PGS into an analytical method. It is the integer-side
coordinate in which, for `n>1`, prime returns sit at $E(n)=0$.

That direction matters. A method inside the zeta frame asks the analytic layer
to explain prime order. Prime gap structure uses the integer source to explain
why the analytic layer has the form it has.

## Status

- proved theorem: exact local placement and ordered gap interior structure.
- exact coordinate reformulation: zero-excess is a source-side coordinate.
- exact zeta compression: zeta language records the source after compression.
- explanatory consequence: prime gap structure is source-side arithmetic.

## Related Docs

- [Why is analytical-proof expectation the wrong frame?](analytical-proof-expectation.md)
- [Why is RH downstream?](../core-frame/rh-downstream.md)
- [What does zeta compression record?](../core-frame/zeta-compression.md)
- [RH bridge research home](../../../research/12-rh-bridge/README.md)
