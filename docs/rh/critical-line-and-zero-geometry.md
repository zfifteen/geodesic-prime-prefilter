# Critical Line And Zero Geometry

The source order is:

```text
divisor counts -> zero-excess returns -> local theorems
-> DNI-to-zeta compression -> residual closure -> pole placement/RH sentence
```

The critical strip and critical line are downstream coordinate language for the
continued analytic object. They are not the source objects of PGS.

The divisor-count field $\tau(n)$ gives the local integer source. The PGS local
theorems use that field to determine prime returns and order gap interiors.
Zero-excess is the integer-side coordinate

$$
E(n)=\left(\frac{\tau(n)}{2}-1\right)\log n.
$$

For `n > 1`, prime returns are exactly $E(n)=0$. Inside a nonempty gap
interior, the proof function satisfies $F(n)=-E(n)$, so the leftmost
argmax of $F$ is the leftmost argmin of $E$. The DNI-to-zeta compression then
builds

$$
D(s)=\sum_{n \ge 1}\frac{\tau(n)}{n^s}=\zeta(s)^2
$$

and

$$
R(s)=\frac{e^2}{2}\frac{K(s)}{D(s)}
=-\frac{\zeta'(s)}{\zeta(s)}.
$$

Only after that compression does it make sense to speak in the coordinate
language of zeta zeros, critical strips, and critical lines.

## Coordinate Language

The nontrivial zero geometry of $\zeta(s)$ is usually described inside the
critical strip:

$$
0<\mathrm{Re}(s)<1.
$$

The critical line is the vertical line

$$
\mathrm{Re}(s)=\frac{1}{2}.
$$

In the DNI-ratio translation, those same zeta zeros are read as poles of

$$
R(s)=-\frac{\zeta'(s)}{\zeta(s)}.
$$

Thus the critical strip is the downstream coordinate band where nontrivial
poles of the continued DNI ratio are located. The critical line is the
placement line after source-side residual closure.

The zero-excess floor is integer-side. The critical line is zeta-side. The
analogy is permitted because both are distinguished coordinates in their own
domains; identity is not permitted.

## Exact Translation

The exact translation is:

1. The divisor-count series gives $D(s)=\zeta(s)^2$ on
   $\mathrm{Re}(s)>1$.
2. The zero-excess bridge load is
   $H(n)=\log n+E(n)=\tau(n)\log n/2$, equivalently
   `H(n)=log n+E(n)=tau(n)log(n)/2`, preserving the original `D,K,R`
   bridge rather than replacing it with $E(n)$ alone.
3. The DNI load series satisfies $K(s)=-D'(s)/e^2$ on the same half-plane.
4. The normalized ratio continues as
   $R(s)=(e^2/2)K(s)/D(s)=-\zeta'(s)/\zeta(s)$.
5. Zeros of $\zeta(s)$ become poles of $R(s)$.
6. Nontrivial zeros of $\zeta(s)$ become nontrivial poles of $R(s)$ in the
   critical strip.

Therefore RH translates exactly into this pole-placement sentence:

all nontrivial poles of the continued DNI ratio

$$
R(s)=\frac{e^2}{2}\frac{K(s)}{D(s)}
$$

lie on the critical line

$$
\mathrm{Re}(s)=\frac{1}{2}.
$$

This is the classical RH statement read through the continued DNI-ratio object
after source-side residual closure. It is not a probability statement or a
numerical restatement.

## Source-Side Closure

The translation identifies the exact object whose nontrivial pole placement is
RH. Placement is closed by the source-side residual test, not by a classical
zero-estimate or error-term argument.

A nontrivial pole off

$$
\mathrm{Re}(s)=\frac{1}{2}.
$$

would have to be carried by a surviving source residual in `D,K,R`, the
endpoint chain, the chamber log-weight source, or the divisor-count field. The
residual test closes those carriers. A conclusion-only assertion that the whole
sequence might carry an off-critical pole does not name a source object.

The local PGS theorems are source-side arithmetic theorems about divisor
counts, prime returns, and ordered gap interiors. `PROOF.md` controls those
local theorem claims. The zeta-compressed statement is the downstream RH
sentence after source-side residual closure.

## Geometry Ledger

| Object | Source role | DNI-ratio role |
| --- | --- | --- |
| divisor counts $\tau(n)$ | integer-level source field | coefficient source for $D(s)$ |
| zero-excess floor $E(n)=0$ for `n > 1` | integer-side prime-return coordinate | source-side analogy only |
| local PGS theorems | prime returns and gap-interior order | upstream arithmetic structure |
| $D(s)=\zeta(s)^2$ | divisor-count compression | denominator of the DNI ratio |
| $R(s)=-\zeta'(s)/\zeta(s)$ | continued normalized ratio | pole-carrying analytic object |
| source-side residual closure | exclusion of leftover carriers in the exact quotient | off-critical-pole exclusion |
| critical strip | downstream zeta coordinate band | nontrivial pole band |
| critical line | downstream zeta coordinate line | RH pole-placement line |

This ledger keeps the direction fixed. PGS does not begin by searching for
zeros. The zero geometry is read after the divisor-count source has been
compressed into the continued DNI ratio.

## Links

- [RH bundle README](README.md)
- [DNI-to-zeta compression](dni-to-zeta-compression.md)
- [Pole placement](pole-placement.md)
- [Off-critical pole exclusion](off-critical-pole-exclusion.md)
- [Status ledger](status-ledger.md)
- [Full DNI-RH bridge note](../../research/12-rh-bridge/docs/dni_rh_bridge.md)
