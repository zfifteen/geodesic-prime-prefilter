# How should claim status be read?

## Short Answer

Every claim should be assigned to its exact status label: proved theorem, exact
coordinate reformulation, exact zeta compression, source-side residual closure,
measured implementation evidence, unresolved bounded-compression obligation,
invalidated route, downstream translation bridge, or explanatory consequence.

## Source Order

```text
divisor counts -> PGS local theorems -> DNI-to-zeta compression
-> source-side residual closure -> pole placement/RH sentence
```

## Common Mistake

The mistake is to flatten all claims into one bucket. That either downgrades
proved arithmetic or overstates an implementation measurement.

## Full Answer

Use these labels:

- proved theorem: a universal result proved under stated hypotheses.
- exact coordinate reformulation: a same-source coordinate change, including
  Zero-Excess DNI, that does not add a new theorem.
- exact zeta compression: an identity or bridge that carries integer structure
  into analytic language. In Zero-Excess DNI notation, the bridge load is
  $H(n)=\log n+E(n)$, not $E(n)$ alone.
- source-side residual closure: the off-critical-pole residual test after local
  PGS closure and exact DNI compression.
- measured implementation evidence: a finite implementation or benchmark
  surface.
- unresolved bounded-compression obligation: a separate compression or
  implementation obligation that is not a limit on the source theorem.
- invalidated route: a route that has been tested or argued false and must not
  be revived as live support.
- downstream translation bridge: explicit-formula movement from `R(s)` to
  `Lambda`, `psi`, zero-term, and error-term language.
- explanatory consequence: a conclusion about source order, interpretation, or
  downstream language.

`PROOF.md` controls local PGS theorem status. It does not itself prove RH. The
RH bridge controls the exact zeta-compression identity. The source-side
residual test controls off-critical-pole residual closure in the RH bundle.
Benchmarks and audits certify implementation surfaces. They do not define the
source laws.

The zero-excess floor is integer-side. The critical line is zeta-side. Treat
that relation as an analogy after compression, not an identity of objects.

PGS is not an analytical method. It does not require a classical zero-estimate
or explicit-formula error-term proof to close the source-side RH sentence.
Those explicit-formula objects remain downstream translation/proof-detail
bridges.

## Status

- proved theorem: controlled by `PROOF.md`.
- exact coordinate reformulation: controlled by the zero-excess notation
  contract and root-doc migration scope.
- exact zeta compression: controlled by the DNI-to-zeta bridge.
- source-side residual closure: controlled by the RH off-critical-pole
  residual test.
- measured implementation evidence: attached to implementation surfaces.
- unresolved bounded-compression obligation: separate from the universal local
  theorems.
- invalidated route: not live support.
- downstream translation bridge: explicit-formula language for `Lambda`,
  `psi`, zero terms, and error terms.
- explanatory consequence: source-first reading of RH language.

## Related Docs

- [Root proof authority](../../../PROOF.md)
- [DNI-to-zeta bridge](../../../research/12-rh-bridge/docs/dni_rh_bridge.md)
- [Documentation correction project](../../../research/15-documentation-correction/README.md)
