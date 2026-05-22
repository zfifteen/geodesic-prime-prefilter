# What counts as a real objection?

## Short Answer

A real objection must engage the source object: divisor counts, zero-excess
returns, the direct next-prime theorem, ordered gap interiors, or the exact
zeta-compression bridge.

## Source Order

```text
divisor counts -> zero-excess returns -> prime gap structure -> zeta compression -> RH language
```

## Common Mistake

The mistake is to object from the downstream analytic frame while leaving the
source object untouched.

## Full Answer

A real objection would identify a concrete fault in one of these places:

- the definition or use of $\tau(n)$;
- the zero-excess coordinate, if it fails to be the exact reformulation
  $E(n)=((\tau(n)/2)-1)\log n$;
- the proof of the direct next-prime rule;
- the proof of the gap-interior maximizer theorem;
- the identity $D(s)=\zeta(s)^2$ on $\mathrm{Re}(s)>1$;
- the DNI ratio computation that recovers $-\zeta'(s)/\zeta(s)$;
- a status claim that assigns a result to the wrong category.

An objection misses the target when it starts by demanding that prime gap
structure behave like a zeta-side method. That demand does not address the
integer carrier object.

The right review question is direct: where does the source-side arithmetic
fail? If it does not fail, then the zeta language must be read as downstream
compression of that source.

## Status

- explanatory consequence: valid review must engage the source object.
- proved theorem: local source laws are controlled by `PROOF.md`.
- exact coordinate reformulation: zero-excess objections must target the
  coordinate, not RH pole placement.
- exact zeta compression: the analytic bridge is controlled by the RH bridge
  documentation.

## Related Docs

- [What should a reviewer check first?](evaluation-order.md)
- [How should claim status be read?](status-ledger.md)
- [Why is analytical-proof expectation the wrong frame?](../category-errors/analytical-proof-expectation.md)
- [What is the source object?](../core-frame/source-object.md)
