# How does the DNI ratio recover the classical prime-power detector?

## Short Answer

The DNI bridge builds a ratio from the divisor-count series and its derivative.
That ratio is exactly $-\zeta'(s)/\zeta(s)$, the classical detector of prime
powers. In Zero-Excess DNI notation, the bridge numerator uses
$H(n)=\log n+E(n)=\tau(n)\log(n)/2$, not $E(n)$ alone.

## Source Order

```text
divisor counts -> zero-excess prime returns -> PGS local theorems
-> DNI-to-zeta compression -> source-side residual closure -> RH language
```

## Common Mistake

The mistake is to read the final analytic ratio as the source. The ratio is the
compressed analytic form of divisor-count arithmetic.

## Full Answer

Start with the divisor-count series. On its half-plane of convergence
$\mathrm{Re}(s)>1$, it satisfies:

$$
D(s)=\sum_{n\ge 1}\frac{\tau(n)}{n^s}=\zeta(s)^2.
$$

Define the weighted load:

$$
K(s)=-\frac{1}{e^2}D'(s).
$$

In zero-excess coordinates, the same derivative load is:

$$
H(n)=\log n+E(n)=\frac{\tau(n)\log n}{2}.
$$

So:

$$
\sum_{n\ge 1}\frac{H(n)}{n^s}=-\frac12D'(s).
$$

Then the DNI ratio is:

$$
R(s)=\frac{e^2}{2}\frac{K(s)}{D(s)}.
$$

On the same half-plane, $D(s)=\zeta(s)^2$, so this gives:

$$
R(s)=-\frac12\frac{D'(s)}{D(s)}
=-\frac{\zeta'(s)}{\zeta(s)}.
$$

The right-hand side is the classical prime-power detector. The bridge shows
that this detector is recovered from the divisor-count source. $E(n)$ alone is
not the numerator. It is the residual excess coordinate. The numerator carries
the full bridge load $H(n)$.

## Status

- exact zeta compression: the DNI ratio recovers $-\zeta'(s)/\zeta(s)$.
- exact coordinate reformulation: Zero-Excess DNI supplies the same source
  through $E(n)$ and $Z(n)=e^{-E(n)}$.
- source-side residual closure: RH-facing residual closure is distinct from
  this exact ratio identity.
- explanatory consequence: the classical detector is downstream of the
  divisor-count source.

## Related Docs

- [DNI-to-zeta bridge](../../../research/12-rh-bridge/docs/dni_rh_bridge.md)
- [How does the divisor-count series enter zeta language?](divisor-series.md)
- [Does zeta have its own arithmetic supply?](no-private-arithmetic-supply.md)
