# RH Bundle Status Ledger

The status order is fixed:

```text
divisor counts -> PGS local theorems -> DNI-to-zeta compression
-> source-side residual closure -> pole placement/RH sentence
```

Read every RH-facing claim through that order. The integer object comes first.
The analytic sentence comes after compression and source-side residual closure.

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
replacement proof of the local PGS theorems, and `PROOF.md` itself does not
prove RH.

## Source-Side Residual Closure

Status: source-side residual closure, supplied by
[Off-Critical Pole Exclusion](off-critical-pole-exclusion.md).

After local PGS source closure and exact DNI compression, an off-critical
nontrivial pole of `R(s)` would need a surviving source-side residual: a failed
identity in `D,K,R`, independent endpoint or gap-length freedom, a chamber
log-weight remainder, an additional divisor-count field, or another named
source object. The residual-test page closes those source-side carriers in the
active RH bundle.

That closure is source-first. PGS is not an analytical method and does not
require a classical zero-estimate, prime-counting error-term proof, or
explicit-formula estimate to close the PGS-to-RH sentence.

## Explanatory Consequence

Status: explanatory consequence.

The source order changes how RH-facing language is read:

```text
divisor counts -> PGS local theorems -> DNI-to-zeta compression
-> source-side residual closure -> pole placement/RH sentence
```

The pole-placement language is downstream of the source and compression
layers. The RH sentence is the classical analytic wording of the closed
source-side residual state:

$$
\text{every nontrivial pole of } R(s) \text{ lies on } \mathrm{Re}(s)=1/2.
$$

That sentence belongs after the exact compression and source-side residual
closure layers. It does not define the integer source.

## Downstream Explicit-Formula Bridge

Status: downstream analytic translation and proof-detail bridge.

The explicit-formula bridge is not the PGS-to-RH proof path. It is the classical
translation of the already compressed ratio

$$
R(s)=\frac{e^2}{2}\frac{K(s)}{D(s)}
$$

into

```text
R(s) -> Lambda(n) -> psi(x) -> explicit-formula error-term language
```

That bridge remains useful for reviewers who want the result restated in
`psi`, `Lambda`, zero-term, or error-term language. It is downstream analytic
translation, not a prerequisite for the source-side PGS-to-RH closure.

Do not collapse source-side residual closure into the proved local theorems.
Do not claim `PROOF.md` itself proves RH. Do not downgrade the proved local
theorems because explicit-formula translation remains a separate downstream
bridge.
