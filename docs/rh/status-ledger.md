# RH Bundle Status Ledger

The status order is fixed:

```text
divisor counts -> PGS local theorems -> DNI-to-zeta compression
-> source-to-spectral placement target -> pole placement/RH sentence
```

Read every RH-facing claim through that order. The integer object comes first.
The analytic sentence comes after exact compression and the unresolved
source-to-spectral placement target.

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

## Exact Coordinate Reformulation

Status: exact coordinate reformulation.

Zero-Excess DNI is an integer-side coordinate reformulation of the same
divisor-count source. The zero-excess floor is the integer-side coordinate
$E(n)=0$ under the $n>1$ prime guard. The critical line is zeta-side coordinate
language after compression. The floor and the critical line may be compared by
analogy, but they are not the same object.

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

In Zero-Excess DNI notation, the bridge load is
$H(n)=\log n+E(n)=\tau(n)\log n/2$, not $E(n)$ alone.

This is an exact zeta compression of the divisor-count source. It is not a
replacement proof of the local PGS theorems, and `PROOF.md` itself does not
prove RH.

## Source-To-Spectral Placement Target

Status: unresolved proof target, with obstruction recorded by
[Off-Critical Pole Exclusion](off-critical-pole-exclusion.md) and
[Off-Axis Pair Carrier Lemma Resolution](../../research/12-rh-bridge/docs/off_axis_pair_carrier_lemma_resolution.md).

After local PGS source closure and exact DNI compression, failed identities in
`D,K,R`, independent endpoint or gap-length freedom, chamber log-weight
remainders, and additional divisor-count fields are closed as bookkeeping
failures. That does not yet exclude off-critical nontrivial poles of `R(s)`.
Such poles could be global analytic properties of the same zeta-compressed
source rather than signs of an extra source object.

The remaining bridge is source-first but genuinely analytic: derive a
source-to-spectral placement theorem from PGS chamber geometry and the
$Z=1$ / $E=0$ return law, or derive an equivalent RH-strength constraint such
as a sharp bound for `psi(x)-x`.

## Explanatory Consequence

Status: explanatory consequence.

The source order changes how RH-facing language is read:

```text
divisor counts -> PGS local theorems -> DNI-to-zeta compression
-> source-to-spectral placement target -> pole placement/RH sentence
```

The pole-placement language is downstream of the source and compression
layers. The RH sentence is the classical analytic wording of the unresolved
source-to-spectral target:

$$
\text{every nontrivial pole of } R(s) \text{ lies on } \mathrm{Re}(s)=1/2.
$$

That sentence belongs after the exact compression layer. It does not define
the integer source, and it is not yet proved by the no-extra-carrier residual
test.

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
translation, and it names one equivalent form of the missing placement
constraint.

Do not collapse source-to-spectral placement into the proved local theorems.
Do not claim `PROOF.md` itself proves RH. Do not downgrade the proved local
theorems because explicit-formula translation remains a separate downstream
bridge.
