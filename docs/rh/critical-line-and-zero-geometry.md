# Critical Line And Zero Geometry

The source order is:

```text
divisor counts -> PGS local theorems -> DNI-to-zeta compression -> pole placement -> RH sentence
```

The critical strip and critical line are downstream coordinate language for the
continued analytic object. They are not the source objects of PGS.

The divisor-count field $\tau(n)$ gives the local integer source. The PGS local
theorems use that field to determine prime returns and order gap interiors. The
DNI-to-zeta compression then builds

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
poles of the continued DNI ratio are located. The critical line is the proposed
placement line for all of those nontrivial poles.

## Exact Translation

The exact translation is:

1. The divisor-count series gives $D(s)=\zeta(s)^2$ on
   $\mathrm{Re}(s)>1$.
2. The DNI load series satisfies $K(s)=-D'(s)/e^2$ on the same half-plane.
3. The normalized ratio continues as
   $R(s)=(e^2/2)K(s)/D(s)=-\zeta'(s)/\zeta(s)$.
4. Zeros of $\zeta(s)$ become poles of $R(s)$.
5. Nontrivial zeros of $\zeta(s)$ become nontrivial poles of $R(s)$ in the
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

This is a translation of the classical RH statement into the continued
DNI-ratio object. It is not a probability statement or a numerical
restatement.

## Proof Target

The translation itself does not place the poles. It identifies the exact object
whose nontrivial pole placement is RH.

A proof must establish, from the source-side divisor-count and PGS structure
after DNI-to-zeta compression, that the continued ratio has no nontrivial poles
off

$$
\mathrm{Re}(s)=\frac{1}{2}.
$$

The local PGS theorems are source-side arithmetic theorems about divisor
counts, prime returns, and ordered gap interiors. The zeta-compressed statement
is the downstream RH sentence. The proof target is the bridge from that local
source structure to global nontrivial pole placement.

## Geometry Ledger

| Object | Source role | DNI-ratio role |
| --- | --- | --- |
| divisor counts $\tau(n)$ | integer-level source field | coefficient source for $D(s)$ |
| local PGS theorems | prime returns and gap-interior order | upstream arithmetic structure |
| $D(s)=\zeta(s)^2$ | divisor-count compression | denominator of the DNI ratio |
| $R(s)=-\zeta'(s)/\zeta(s)$ | continued normalized ratio | pole-carrying analytic object |
| critical strip | downstream zeta coordinate band | nontrivial pole band |
| critical line | downstream zeta coordinate line | RH pole-placement line |

This ledger keeps the direction fixed. PGS does not begin by searching for
zeros. The zero geometry is read after the divisor-count source has been
compressed into the continued DNI ratio.

## Links

- [RH bundle README](README.md)
- [DNI-to-zeta compression](dni-to-zeta-compression.md)
- [Pole placement](pole-placement.md)
- [Status ledger](status-ledger.md)
- [Full DNI-RH bridge note](../../research/12-rh-bridge/docs/dni_rh_bridge.md)
