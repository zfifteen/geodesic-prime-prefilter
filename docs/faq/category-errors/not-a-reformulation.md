# Is prime gap structure only another wording of RH?

## Short Answer

No. Prime gap structure is the source-side arithmetic object. RH is the
zeta-side language that records that object after compression.

## Source Order

```text
divisor counts -> prime gap structure -> zeta compression -> RH language
```

## Common Mistake

The mistake is to collapse the source and the compressed description into the
same layer. They are not the same layer.

## Full Answer

The source-side object is built from exact divisor counts on the integer line.
It places primes by the condition `tau(n)=2`, orders the interior of each prime
gap, and centers the prime state through the divisor normalization:

$$
Z(n)=n^{1-\tau(n)/2}.
$$

The classical RH sentence belongs to the analytic layer. It speaks in the
coordinates of zeta zeros. That sentence is a compressed description of the
integer structure, not the source of the structure.

Calling the whole source mechanism another wording of RH loses the carrier
object. The object being carried is the exact divisor-count field. Zeta records
that field in analytic language.

## Status

- proved theorem: the local source laws are proved in `PROOF.md`.
- exact zeta compression: the bridge identifies the analytic expression
  recovered from the source.
- explanatory consequence: RH is read after the source is fixed.

## Related Docs

- [What is the source object?](../core-frame/source-object.md)
- [Why is RH downstream?](../core-frame/rh-downstream.md)
- [Root proof authority](../../../PROOF.md)
