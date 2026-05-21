# What is the source object?

## Short Answer

The source object is the ordered divisor-count structure of the integers,
especially inside prime gaps. Each integer has a divisor count. Primes are the
integers with divisor count two. The gap between consecutive primes is a finite
ordered run of composite divisor counts.

## Source Order

```text
divisor counts -> prime gap structure -> zeta compression -> RH language
```

## Common Mistake

The mistake is to start with zeros, poles, or analytic coordinates and then ask
whether the integer structure has earned permission to exist. The integer
structure is already the carrier object.

## Full Answer

For a positive integer `n`, let `tau(n)` be the number of positive divisors of
`n`. A prime has exactly two positive divisors, `1` and itself, so primes are
exactly the integers where `tau(n)=2`.

Given consecutive primes `p` and `q`, every integer between them is composite.
That interior has an ordered divisor-count profile:

$$
\tau(p+1),\tau(p+2),\ldots,\tau(q-1).
$$

Prime gap structure studies this ordered integer object. The Divisor
Normalization Identity centers the same object on the prime level:

$$
Z(n)=n^{1-\tau(n)/2}.
$$

Primes land exactly on `Z=1`. Composites land below it. The source object is not
an analytic estimate of prime behavior. It is the exact divisor-count field
that places the primes and orders the interiors between them.

## Status

- proved theorem: `PROOF.md` proves the direct next-prime rule and the
  gap-interior maximizer theorem.
- explanatory consequence: RH language records this source after zeta
  compression.

## Related Docs

- [Root proof authority](../../../PROOF.md)
- [Why is RH downstream?](rh-downstream.md)
- [How should claim status be read?](../reviewer-guidance/status-ledger.md)
