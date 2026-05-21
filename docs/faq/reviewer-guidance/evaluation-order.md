# What should a reviewer check first?

## Short Answer

A reviewer should start with the integer source: divisor counts, next-prime
placement, ordered gap interiors, and then zeta compression.

## Source Order

```text
divisor counts -> prime gap structure -> zeta compression -> RH language
```

## Common Mistake

The mistake is to open from the classical RH sentence and treat every source
claim as a request for permission from that sentence.

## Full Answer

The correct review order is:

1. Check the divisor-count definitions.
2. Check the direct next-prime theorem in `PROOF.md`.
3. Check the gap-interior maximizer theorem in `PROOF.md`.
4. Check the DNI-to-zeta bridge.
5. Read RH language as the compressed analytic description.

That order keeps the carrier object intact. It also prevents the most common
misreading: treating a source-side arithmetic claim as an analytic method that
must begin from zeros or poles.

The integer object comes first. The analytic expression comes after
compression.

## Status

- proved theorem: local source laws are proved in `PROOF.md`.
- exact zeta compression: the bridge identifies the downstream analytic object.
- explanatory consequence: review starts at the source.

## Related Docs

- [Root proof authority](../../../PROOF.md)
- [DNI-to-zeta bridge](../../../research/12-rh-bridge/docs/dni_rh_bridge.md)
- [How should claim status be read?](status-ledger.md)
