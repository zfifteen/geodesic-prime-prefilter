# How does the divisor-count series enter zeta language?

## Short Answer

On $\mathrm{Re}(s)>1$, the divisor-count series is the zeta square. That
identity carries the integer-level divisor-count field into analytic language.
In Zero-Excess DNI notation, the derivative load is
$H(n)=\log n+E(n)=\tau(n)\log(n)/2$, not $E(n)$ alone.

## Source Order

```text
divisor counts -> zero-excess prime returns -> PGS local theorems
-> DNI-to-zeta compression -> source-side residual closure -> RH language
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

The derivative load used by the DNI ratio is the full bridge load:

$$
H(n)=\log n+E(n)=\frac{\tau(n)\log n}{2}.
$$

Thus:

$$
\sum_{n\ge 1}\frac{H(n)}{n^s}=-\frac12D'(s).
$$

The numerator is not $E(n)$ alone. $E(n)$ records source-side excess above the
zero prime floor. The zeta compression step carries the divisor-count load
$H(n)$.

## Status

- exact zeta compression: $D(s)=\zeta(s)^2$ for $\mathrm{Re}(s)>1$.
- exact coordinate reformulation: Zero-Excess DNI gives the same source in
  $E(n)$ form.
- source-side residual closure: residual closure is separate from this
  divisor-series identity.
- explanatory consequence: zeta square records divisor-count arithmetic.

## Related Docs

- [DNI-to-zeta bridge](../../../research/12-rh-bridge/docs/dni_rh_bridge.md)
- [How does the DNI ratio recover the classical prime-power detector?](dni-ratio.md)
- [What does zeta compression record?](../core-frame/zeta-compression.md)
