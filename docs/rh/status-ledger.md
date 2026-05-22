# RH Bundle Status Ledger

The status order is fixed:

```text
divisor counts -> PGS local theorems -> DNI-to-zeta compression -> pole placement -> RH sentence
```

Read every RH-facing claim through that order. The integer object comes first.
The analytic sentence comes after compression.

## Sources

- [Root proof authority](../../PROOF.md)
- [Reviewer status ledger](../faq/reviewer-guidance/status-ledger.md)
- [DNI-to-zeta bridge](../../research/12-rh-bridge/docs/dni_rh_bridge.md)

## Proved Theorem

Status: proved under the hypotheses stated in [PROOF.md](../../PROOF.md).

The proved source layer is local and arithmetic:

- for a known prime `p`, exact divisor-count traversal returns
  `q = min { n > p : tau(n) = 2 }`;
- inside a nonempty prime-gap chamber, the leftmost integer with minimum
  interior divisor count uniquely maximizes
  `F(n) = (1 - tau(n)/2) log(n)`.

These are PGS local theorems. They begin with divisor counts and ordered gap
interiors. Zeta, pole placement, zero geometry, PNT, and RH are not inputs to
these theorems.

## Exact Zeta Compression

Status: exact identity on `Re(s) > 1`, with the same meromorphic continuation
through the zeta identity, as recorded in the
[DNI-to-zeta bridge](../../research/12-rh-bridge/docs/dni_rh_bridge.md).

The divisor-count series is

$$
D(s)=\sum_{n\ge1}\frac{\tau(n)}{n^s}=\zeta(s)^2.
$$

With

$$
K(s)=-\frac{1}{e^2}D'(s),
$$

the normalized DNI ratio is

$$
R(s)=\frac{e^2}{2}\frac{K(s)}{D(s)}
=-\frac{\zeta'(s)}{\zeta(s)}
=\sum_{n\ge1}\frac{\Lambda(n)}{n^s}.
$$

This is an exact zeta compression of the divisor-count source. It is not a
replacement proof of the local PGS theorems, and it is not by itself a proof
that all nontrivial poles lie on the critical line.

## Explanatory Consequence

Status: explanatory consequence.

The source order changes how RH-facing language is read:

```text
divisor counts -> PGS local theorems -> DNI-to-zeta compression -> pole placement -> RH sentence
```

The pole-placement language is downstream. The RH sentence is the classical
analytic wording of what the continued ratio would say about nontrivial poles:

$$
\text{every nontrivial pole of } R(s) \text{ lies on } \mathrm{Re}(s)=1/2.
$$

That sentence belongs after the exact compression layer. It does not define the
integer source.

## Proof Target / Needs Proof

Status: proof target unless supplied by a complete proof in the active doc.

The remaining global analytic target is to prove, from the PGS source and the
exact DNI-to-zeta compression, that the continued ratio

$$
R(s)=\frac{e^2}{2}\frac{K(s)}{D(s)}
$$

has all nontrivial poles on

$$
\mathrm{Re}(s)=1/2.
$$

Equivalently, after identifying `R(s)` with `-zeta'(s)/zeta(s)`, the proof
target is the RH pole-placement statement for the nontrivial zeros of
`zeta(s)`.

Do not collapse this target into the proved local theorems. Do not downgrade
the proved local theorems because this global pole-placement proof target is
separate.
