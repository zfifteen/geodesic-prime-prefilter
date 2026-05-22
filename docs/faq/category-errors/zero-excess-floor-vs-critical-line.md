# Is the zero-excess floor the same as the critical line?

## Short Answer

Analogy yes. Identity no. Source-to-compression relation yes. The
zero-excess floor is the integer-side prime return level. The critical line is
the zeta-side coordinate after compression.

## Source Order

```text
divisor counts -> zero-excess prime returns -> PGS local theorems
-> DNI-to-zeta compression -> source-side residual closure -> RH language
```

## Common Mistake

The mistake is to identify two objects because both are centered coordinates.
The zero-excess floor and the critical line are connected by the
source-to-compression reading, but they live on different sides of the bridge.

## Full Answer

The source-side coordinate is:

$$
E(n)=\left(\frac{\tau(n)}{2}-1\right)\log n.
$$

For every integer `n>1`:

$$
E(n)=0 \Longleftrightarrow \tau(n)=2 \Longleftrightarrow n \text{ is prime}.
$$

The value $E(1)=0$ is a boundary artifact from $\log 1=0$. It is not a prime
return.

The RH critical line is the zeta-side coordinate sentence:

$$
\mathrm{Re}(\rho)=\frac12.
$$

The analogy is legitimate: both statements are centered descriptions of the
same arithmetic source after the proper layer is chosen. The identity is false:
one statement is about integer divisor-count returns, and the other is about
zeros of the compressed analytic object.

The source-to-compression relation is exact at the bridge level. The
divisor-count series satisfies:

$$
D(s)=\sum_{n\ge 1}\frac{\tau(n)}{n^s}=\zeta(s)^2
\quad (\mathrm{Re}(s)>1).
$$

In Zero-Excess DNI notation, the bridge load is:

$$
H(n)=\log n+E(n)=\frac{\tau(n)\log n}{2}.
$$

The DNI ratio then recovers:

$$
R(s)=-\frac{\zeta'(s)}{\zeta(s)}.
$$

$E(n)$ alone is not the zeta numerator. It is the source-side residual above
the zero prime floor. The compression numerator uses the full load $H(n)$.

## Status

- exact coordinate reformulation: the zero-excess floor is a same-source
  coordinate for prime returns on the integer side.
- exact zeta compression: $D(s)=\zeta(s)^2$ and the DNI ratio recover
  $-\zeta'(s)/\zeta(s)$ from the divisor-count source.
- source-side residual closure: RH-facing residual closure is a later
  source-side claim after local PGS closure and exact compression.
- explanatory consequence: zero-excess floor and critical line are related by
  source-to-compression structure, not by object identity.

## Related Docs

- [What is the source object?](../core-frame/source-object.md)
- [Why is RH downstream?](../core-frame/rh-downstream.md)
- [What does zeta compression record?](../core-frame/zeta-compression.md)
- [How should claim status be read?](../reviewer-guidance/status-ledger.md)
