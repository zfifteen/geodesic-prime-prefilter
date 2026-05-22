# What is the source object?

## Short Answer

The source object is the ordered divisor-count structure of the integers,
especially inside prime gaps. Each integer has a divisor count. In
zero-excess coordinates, every integer `n>1` with excess zero is a prime
return. The gap between consecutive primes is a finite ordered run of
positive-excess composites.

## Source Order

```text
divisor counts -> zero-excess prime returns -> PGS local theorems
-> DNI-to-zeta compression -> source-side residual closure -> RH language
```

## Common Mistake

The mistake is to start with zeros, poles, or analytic coordinates and then ask
whether the integer structure has earned permission to exist. The integer
structure is already the carrier object.

## Full Answer

For a positive integer `n`, let $\tau(n)$ be the number of positive divisors of
`n`. A prime has exactly two positive divisors, `1` and itself, so primes are
exactly the integers where $\tau(n)=2$.

The zero-excess coordinate for the same divisor-count source is:

$$
E(n)=\left(\frac{\tau(n)}{2}-1\right)\log n.
$$

For every integer `n>1`, $\log n>0$, so:

$$
E(n)=0 \Longleftrightarrow \tau(n)=2 \Longleftrightarrow n \text{ is prime}.
$$

The value $E(1)=0$ is a boundary artifact from $\log 1=0$. It is not a prime
return.

Given consecutive primes `p` and `q`, every integer between them is composite.
That interior has an ordered divisor-count profile:

$$
\tau(p+1),\tau(p+2),\ldots,\tau(q-1).
$$

Prime gap structure studies this ordered integer object. Zero-Excess DNI
centers the same object on the prime level:

$$
Z(n)=n^{1-\tau(n)/2}=e^{-E(n)}.
$$

For `n>1`, primes land exactly on $E=0$ and $Z=1$. Composites land at $E>0$
and $Z<1$. The source object is not an analytic estimate of prime behavior. It
is the exact divisor-count field that places the primes and orders the
interiors between them.

## Status

- proved theorem: `PROOF.md` proves the direct next-prime rule and the
  gap-interior maximizer theorem.
- exact coordinate reformulation: Zero-Excess DNI rewrites the same source as
  $E(n)=0$ prime returns for `n>1`; $E(1)=0$ is boundary-only.
- exact zeta compression: the bridge uses the load
  $H(n)=\log n+E(n)=\tau(n)\log(n)/2$, not $E(n)$ alone.
- source-side residual closure: RH-facing residual closure is separate from
  the coordinate reformulation and from exact zeta compression.
- explanatory consequence: RH language records this source after zeta
  compression.

## Related Docs

- [Root proof authority](../../../PROOF.md)
- [Why is RH downstream?](rh-downstream.md)
- [How should claim status be read?](../reviewer-guidance/status-ledger.md)
