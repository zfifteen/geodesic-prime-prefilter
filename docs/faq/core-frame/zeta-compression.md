# What does zeta compression record?

## Short Answer

Zeta compression records the same integer arithmetic in analytic form. It does
not create prime order. It packages divisor counts, prime powers, and related
integer structure into functions of a complex variable. In Zero-Excess DNI
notation, the bridge load is $H(n)=\log n+E(n)=\tau(n)\log(n)/2$.

## Source Order

```text
divisor counts -> zero-excess prime returns -> PGS local theorems
-> DNI-to-zeta compression -> source-side residual closure -> RH language
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

The derivative of this series carries the weighted divisor-count load. In
Zero-Excess DNI notation, define the bridge load by:

$$
H(n)=\log n+E(n)=\frac{\tau(n)\log n}{2}.
$$

Then:

$$
\sum_{n\ge 1}\frac{H(n)}{n^s}=-\frac12D'(s).
$$

Equivalently, with the existing normalization:

$$
K(s)=-\frac{1}{e^2}D'(s).
$$

On the same half-plane, the DNI ratio gives:

$$
R(s)=\frac{e^2}{2}\frac{K(s)}{D(s)}
=-\frac{\zeta'(s)}{\zeta(s)}.
$$

That expression is the classical prime-power detector. The bridge is exact.
The analytic expression is a compressed record of divisor-count arithmetic.
$E(n)$ alone is not the numerator. It is the source-side excess above the prime
floor. The zeta bridge numerator is the full load
$H(n)=\log n+E(n)=\tau(n)\log(n)/2$.

## Status

- exact zeta compression: the bridge identifies the analytic object recovered
  from divisor-count data.
- exact coordinate reformulation: Zero-Excess DNI supplies $E(n)$ and
  $Z(n)=e^{-E(n)}$ as same-source coordinates.
- source-side residual closure: off-critical residual closure is a later
  source-side step, not the divisor-series identity itself.
- explanatory consequence: zeta language reads the source structure after
  compression.

## Related Docs

- [DNI-to-zeta bridge](../../../research/12-rh-bridge/docs/dni_rh_bridge.md)
- [How does the divisor-count series enter zeta language?](../zeta-compression/divisor-series.md)
- [How does the DNI ratio recover the classical prime-power detector?](../zeta-compression/dni-ratio.md)
