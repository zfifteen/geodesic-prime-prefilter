# How does the divisor-count series enter zeta language?

## Short Answer

The divisor-count series is the zeta square. That identity carries the
integer-level divisor-count field into analytic language.

## Source Order

```text
divisor counts -> prime gap structure -> zeta compression -> RH language
```

## Common Mistake

The mistake is to treat the zeta square as an independent source. It is the
analytic record of divisor-count arithmetic.

## Full Answer

The divisor-count series is:

$$
D(s)=\sum_{n\ge 1}\frac{\tau(n)}{n^s}.
$$

For $\mathrm{Re}(s)>1$, the classical identity is:

$$
D(s)=\zeta(s)^2.
$$

The reason is arithmetic. The coefficient `tau(n)` counts the number of ways
to write `n` as an ordered product of two positive integers. Multiplying two
copies of the zeta series counts the same choices.

This puts divisor-count structure directly into zeta language. The analytic
object records the integer source.

## Status

- exact zeta compression: $D(s)=\zeta(s)^2$ for $\mathrm{Re}(s)>1$.
- explanatory consequence: zeta square records divisor-count arithmetic.

## Related Docs

- [DNI-to-zeta bridge](../../../research/12-rh-bridge/docs/dni_rh_bridge.md)
- [How does the DNI ratio recover the classical prime-power detector?](dni-ratio.md)
- [What does zeta compression record?](../core-frame/zeta-compression.md)
