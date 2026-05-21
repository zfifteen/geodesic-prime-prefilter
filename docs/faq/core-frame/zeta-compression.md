# What does zeta compression record?

## Short Answer

Zeta compression records the same integer arithmetic in analytic form. It does
not create prime order. It packages divisor counts, prime powers, and related
integer structure into functions of a complex variable.

## Source Order

```text
divisor counts -> prime gap structure -> zeta compression -> RH language
```

## Common Mistake

The mistake is to treat the analytic package as if it owns the arithmetic it
records. The carrier object remains the integer structure.

## Full Answer

The divisor-count series is:

$$
D(s)=\sum_{n\ge 1}\frac{\tau(n)}{n^s}.
$$

For $\mathrm{Re}(s)>1$, it equals:

$$
D(s)=\zeta(s)^2.
$$

The derivative of this series carries the weighted divisor-count load. With

$$
K(s)=-\frac{1}{e^2}D'(s),
$$

on the same half-plane, the DNI ratio gives:

$$
R(s)=\frac{e^2}{2}\frac{K(s)}{D(s)}
=-\frac{\zeta'(s)}{\zeta(s)}.
$$

That expression is the classical prime-power detector. The bridge is exact.
The analytic expression is a compressed record of divisor-count arithmetic.

## Status

- exact zeta compression: the bridge identifies the analytic object recovered
  from divisor-count data.
- explanatory consequence: zeta language reads the source structure after
  compression.

## Related Docs

- [DNI-to-zeta bridge](../../../research/12-rh-bridge/docs/dni_rh_bridge.md)
- [How does the divisor-count series enter zeta language?](../zeta-compression/divisor-series.md)
- [How does the DNI ratio recover the classical prime-power detector?](../zeta-compression/dni-ratio.md)
