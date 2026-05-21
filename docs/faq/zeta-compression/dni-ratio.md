# How does the DNI ratio recover the classical prime-power detector?

## Short Answer

The DNI bridge builds a ratio from the divisor-count series and its derivative.
That ratio is exactly `-\zeta'(s)/\zeta(s)`, the classical detector of prime
powers.

## Source Order

```text
divisor counts -> prime gap structure -> zeta compression -> RH language
```

## Common Mistake

The mistake is to read the final analytic ratio as the source. The ratio is the
compressed analytic form of divisor-count arithmetic.

## Full Answer

Start with the divisor-count series. On its half-plane of convergence
`\mathrm{Re}(s)>1`, it satisfies:

$$
D(s)=\sum_{n\ge 1}\frac{\tau(n)}{n^s}=\zeta(s)^2.
$$

Define the weighted load:

$$
K(s)=-\frac{1}{e^2}D'(s).
$$

Then the DNI ratio is:

$$
R(s)=\frac{e^2}{2}\frac{K(s)}{D(s)}.
$$

On the same half-plane, `D(s)=\zeta(s)^2`, so this gives:

$$
R(s)=-\frac12\frac{D'(s)}{D(s)}
=-\frac{\zeta'(s)}{\zeta(s)}.
$$

The right-hand side is the classical prime-power detector. The bridge shows
that this detector is recovered from the divisor-count source.

## Status

- exact zeta compression: the DNI ratio recovers `-\zeta'(s)/\zeta(s)`.
- explanatory consequence: the classical detector is downstream of the
  divisor-count source.

## Related Docs

- [DNI-to-zeta bridge](../../../research/12-rh-bridge/docs/dni_rh_bridge.md)
- [How does the divisor-count series enter zeta language?](divisor-series.md)
- [Does zeta have its own arithmetic supply?](no-private-arithmetic-supply.md)
