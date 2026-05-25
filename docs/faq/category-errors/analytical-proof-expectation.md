# Why is analytical-proof expectation the wrong frame?

Proof status: non-authoritative research note

## Short Answer

Prime gap structure is not an analytical method. It does not prove RH by
estimating zeros, bounding error terms, or becoming a classical zeta-side
zero-control argument. The current remaining bridge is still a real
source-to-spectral placement theorem: PGS chamber geometry must be shown to
force the continued DNI ratio's nontrivial poles onto the critical line.

## Source Order

```text
divisor counts -> zero-excess returns -> prime gap structure
-> zeta compression -> source-to-spectral placement target -> RH language
```

## Common Mistake

The mistake is to demand a zeta-first proof before checking the source object.
The valid objection is narrower: after accepting the exact DNI quotient, the
source still needs a theorem that places the nontrivial poles of that quotient.

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

After that compression, the admissible objection is source-side and precise:
what theorem carries local chamber structure into spectral placement of
`R(s)`?

The residual checklist still rules out bookkeeping failures:

| Candidate residual | Review question |
| --- | --- |
| Failed identity in $D,K,R$ | Is $D(s)=\zeta(s)^2$, $K(s)=-D'(s)/e^2$, or $R(s)=-\zeta'(s)/\zeta(s)$ wrong? |
| Independent gap-length freedom | Can the gap sequence vary while the same $\tau(n)$ field and $\tau(n)=2$ return chain are preserved? |
| Chamber log-weight residual | Is there a log-weight term outside $\tau(n)\log n$ that survives the DNI quotient? |
| Extra divisor-count field | Is there another multiplicative or factor-pair coefficient supply beyond $\tau(n)$? |
| Global analytic carrier in the same source | Could the same continued quotient carry off-critical poles without an extra coefficient field? |

The first four are closed as bookkeeping failures. The fifth is the live
obstruction to the no-extra-carrier route. It is a mathematical objection
because zeros of a continued Dirichlet series can arise from global
cancellation of the existing source.

When a review returns to zero estimates or prime-counting error terms, keep the
source order intact, but do not dismiss the placement demand. Zero-excess is an
integer-side coordinate, not a zero-control technique. The right question is:

```text
What source-to-spectral placement theorem follows from PGS chamber geometry?
```

If no such theorem is supplied, the RH-facing pole-placement sentence remains
unresolved even though the local PGS source theorems and exact zeta
compression stand.

## Status

- proved theorem: local prime placement and interior ordering are controlled by
  `PROOF.md`.
- exact coordinate reformulation: zero-excess rewrites the source-side DNI
  coordinate without adding a new theorem.
- exact zeta compression: the DNI quotient identifies the downstream analytic
  record of the source.
- source-to-spectral target: the off-critical-pole placement theorem remains
  unresolved.

## Related Docs

- [Is prime gap structure a zeta-side method?](not-a-zeta-method.md)
- [Why is pole placement not the first object?](pole-placement-is-not-first.md)
- [Does analytic opacity weaken the arithmetic source?](analytic-opacity.md)
- [Source-side residual test](../../rh/off-critical-pole-exclusion.md)
