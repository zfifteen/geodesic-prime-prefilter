# Why do ordered gap interiors matter?

## Short Answer

The integers between consecutive primes carry an ordered divisor-count profile.
That profile is part of the structure of prime placement, not empty space
between endpoints.

## Source Order

```text
divisor counts -> zero-excess returns -> prime gap structure -> zeta compression -> RH language
```

## Common Mistake

The mistake is to treat a prime gap as only a distance between two endpoints.
The interior is a finite ordered arithmetic object.

## Full Answer

Let `p` and `q` be consecutive primes. The gap interior is:

$$
I=\{p+1,\ldots,q-1\}.
$$

Every integer in `I` is composite. Each has a divisor count. The interior
therefore has a finite ordered profile:

$$
\tau(p+1),\tau(p+2),\ldots,\tau(q-1).
$$

Inside a nonempty gap, there is a smallest divisor count. The first interior
integer where that smallest count appears is selected. `PROOF.md` proves that
this selected integer uniquely maximizes:

$$
F(n)=\left(1-\frac{\tau(n)}{2}\right)\log n.
$$

In Zero-Excess DNI coordinates,

$$
E(n)=\left(\frac{\tau(n)}{2}-1\right)\log n,
$$

so $F(n)=-E(n)$. The theorem status is unchanged: the selected integer is the
leftmost interior argmin of $E$, equivalently the leftmost interior argmax of
$F$.

That theorem is the ordered interior structure. It shows that prime gaps are
not explained by endpoints alone.

## Status

- proved theorem: the gap-interior maximizer theorem is proved in `PROOF.md`.
- exact coordinate reformulation: zero-excess translates the theorem as a
  leftmost minimum-excess statement.
- explanatory consequence: the gap interior carries ordered structure.

## Related Docs

- [Root proof authority](../../../PROOF.md)
- [What role do divisor counts play?](divisor-counts.md)
- [What is the source object?](../core-frame/source-object.md)
