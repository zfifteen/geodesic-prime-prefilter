# Why is analytical-proof expectation the wrong frame?

Proof status: non-authoritative research note

## Short Answer

Prime gap structure is not an analytical method. It does not prove RH by
estimating zeros, bounding error terms, or becoming a classical zeta-side
zero-control argument.

## Source Order

```text
divisor counts -> zero-excess returns -> prime gap structure -> zeta compression -> RH language
```

## Common Mistake

The mistake is to accept the exact DNI quotient and then demand an analytical
proof that the quotient has no off-critical poles.

## Full Answer

An analytical method starts in the compressed representation. It asks for
control of zeros, contours, error terms, or prime-counting estimates. Prime gap
structure starts before that representation. Its source object is the exact
divisor-count field $\tau(n)$.

The source order fixes the arithmetic carrier first:

- primes are exactly the returns to $\tau(n)=2$;
- for `n>1`, those same returns are the zero-excess returns $E(n)=0$;
- the endpoint chain is fixed by $q=\min\{n>p:\tau(n)=2\}$;
- nonempty gap interiors are ordered by the leftmost minimum-divisor rule;
- the log-weight source is $\tau(n)\log n$;
- in zero-excess notation, the bridge load is
  $H(n)=\log n+E(n)=\tau(n)\log n/2$;
- the DNI quotient compresses the same source into
  $R(s)=(e^2/2)K(s)/D(s)=-\zeta'(s)/\zeta(s)$.

After that compression, the admissible objection is not "where is the
classical analytic exclusion theorem?" The admissible objection is source-side:
what residual remains in $\tau(n)$, $\tau(n)\log n$, $D(s)$, $K(s)$, or
$K(s)/D(s)$ that can carry a nontrivial off-critical pole?

The residual fork is finite:

| Candidate residual | Review question |
| --- | --- |
| Failed identity in $D,K,R$ | Is $D(s)=\zeta(s)^2$, $K(s)=-D'(s)/e^2$, or $R(s)=-\zeta'(s)/\zeta(s)$ wrong? |
| Independent gap-length freedom | Can the gap sequence vary while the same $\tau(n)$ field and $\tau(n)=2$ return chain are preserved? |
| Chamber log-weight residual | Is there a log-weight term outside $\tau(n)\log n$ that survives the DNI quotient? |
| Extra divisor-count field | Is there another multiplicative or factor-pair coefficient supply beyond $\tau(n)$? |
| Conclusion-only residual | Is the objection only that "the whole sequence might carry an off-critical pole" without naming one of the source objects above? |

Only the first four are mathematical objections. The fifth restates the
negation of the RH pole-placement sentence as a possibility. It does not name a
source object that can carry that possibility.

When a review returns to zero estimates, prime-counting error terms, or an
unspecified "global analytic property," stop and correct the frame. The review
has left the source order and is treating prime gap structure as an analytical
method. Zero-excess does not change that: it is an integer-side coordinate, not
a zero-control technique. The right question is:

```text
What source-side residual remains in the exact DNI quotient?
```

If no residual is named, the analytical-proof expectation has not produced an
objection to prime gap structure.

## Status

- proved theorem: local prime placement and interior ordering are controlled by
  `PROOF.md`.
- exact coordinate reformulation: zero-excess rewrites the source-side DNI
  coordinate without adding a new theorem.
- exact zeta compression: the DNI quotient identifies the downstream analytic
  record of the source.
- explanatory consequence: analytical-proof expectation is a category error.

## Related Docs

- [Is prime gap structure a zeta-side method?](not-a-zeta-method.md)
- [Why is pole placement not the first object?](pole-placement-is-not-first.md)
- [Does analytic opacity weaken the arithmetic source?](analytic-opacity.md)
- [Source-side residual test](../../rh/off-critical-pole-exclusion.md)
