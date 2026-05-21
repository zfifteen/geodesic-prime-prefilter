# How should claim status be read?

## Short Answer

Every claim should be assigned to its correct status. A proved source theorem,
an exact zeta compression, a measurement, an unresolved bounded-compression
obligation, and an invalidated route are different kinds of statements.

## Source Order

```text
divisor counts -> prime gap structure -> zeta compression -> RH language
```

## Common Mistake

The mistake is to flatten all claims into one bucket. That either downgrades
proved arithmetic or overstates an implementation measurement.

## Full Answer

Use these labels:

- proved theorem: a universal result proved under stated hypotheses.
- exact zeta compression: an identity or bridge that carries integer structure
  into analytic language.
- measured implementation evidence: a finite implementation or benchmark
  surface.
- unresolved bounded-compression obligation: a separate compression or
  implementation obligation that is not a limit on the source theorem.
- invalidated route: a route that has been tested or argued false and must not
  be revived as live support.
- explanatory consequence: a conclusion about source order, interpretation, or
  downstream language.

`PROOF.md` controls theorem status. The RH bridge controls the exact
zeta-compression identity. Benchmarks and audits certify implementation
surfaces. They do not define the source laws.

## Status

- proved theorem: controlled by `PROOF.md`.
- exact zeta compression: controlled by the DNI-to-zeta bridge.
- measured implementation evidence: attached to implementation surfaces.
- unresolved bounded-compression obligation: separate from the universal local
  theorems.
- invalidated route: not live support.
- explanatory consequence: source-first reading of RH language.

## Related Docs

- [Root proof authority](../../../PROOF.md)
- [DNI-to-zeta bridge](../../../research/12-rh-bridge/docs/dni_rh_bridge.md)
- [Documentation correction project](../../../research/15-documentation-correction/README.md)
