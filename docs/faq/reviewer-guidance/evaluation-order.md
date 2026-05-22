# What should a reviewer check first?

## Short Answer

A reviewer should start with the integer source: divisor counts, zero-excess
returns, next-prime placement, ordered gap interiors, and then zeta
compression.

## Source Order

```text
divisor counts -> zero-excess returns -> prime gap structure -> zeta compression -> RH language
```

## Common Mistake

The mistake is to open from the classical RH sentence and treat every source
claim as a request for permission from that sentence.

## Full Answer

The correct review order is:

1. Check the divisor-count definitions.
2. Check the zero-excess coordinate as an exact reformulation, not a new
   theorem.
3. Check the direct next-prime theorem in `PROOF.md`.
4. Check the gap-interior maximizer theorem in `PROOF.md`, including the
   $F(n)=-E(n)$ leftmost argmin translation.
5. Check the DNI-to-zeta bridge.
6. Read RH language as the compressed analytic description.

That order keeps the carrier object intact. It also prevents the most common
misreading: treating a source-side arithmetic claim as an analytic method that
must begin from zeros or poles.

The integer object comes first. The analytic expression comes after
compression.

## Status

- proved theorem: local source laws are proved in `PROOF.md`.
- exact coordinate reformulation: zero-excess belongs before theorem-status
  review, not after zeta.
- exact zeta compression: the bridge identifies the downstream analytic object.
- explanatory consequence: review starts at the source.

## Related Docs

- [Root proof authority](../../../PROOF.md)
- [DNI-to-zeta bridge](../../../research/12-rh-bridge/docs/dni_rh_bridge.md)
- [How should claim status be read?](status-ledger.md)
