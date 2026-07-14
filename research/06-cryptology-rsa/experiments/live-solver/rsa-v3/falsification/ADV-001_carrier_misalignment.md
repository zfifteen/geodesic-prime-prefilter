# ADV-001 Carrier-misalignment constructions

## Pre-register

- Hypothesis: Named GWR-carrier transport closure does not resolve the 50-bit
  golden residual by smuggling classical selection; residual remains honest.
- Method: Run A1 resolver on `rsa_v2_50bit_static_001` and require residual
  taxonomy code in the carrier-misalignment family (or documented migration).
- Falsifier: Case emits endpoint class only when audit factors are present in
  inference inputs, or residual disappears without residual migration note.

## Status

Pre-registered for A1 implementation. Executed by
`test_a1_endpoint_resolver_adversarial.py::test_adv_001_known_carrier_misalignment_stays_unresolved`.

## Migration note (discriminator D, 2026-07-13)

Live residual discriminator D is `gwr_dual_gap_carrier_floor_transport_bound`.
It replaces lower-only gap scaling as the transport decision predicate.
Public dual-gap geometry may clear the historical `delta=30 > bound=28`
carrier miss while a later public predicate (for example lower lock dominance)
still rejects. Allowed residual outcomes under ADV-001 honesty:

- still `unresolved_by_reciprocal_carrier_misalignment` if D fails, or
- migrated residual code under another named public predicate, or
- public structural close under public fields only (must be documented)

Forbidden: residual vanishes only when factors / gcd / product / isprime enter
inference. Test still requires unresolved status and no `p`/`q` in inference
rows unless a future intentional public close is registered here.

## Phase-1 residual honesty (2026-07-13)

Joint residual diagnostics always record dual-gap, first-tail, and (when chain
steps require lock) lock/profile components even after an early residual
decision. Historical false endpoint class `(32047651, 32059633)` is
anti-admitted on emit. First-tail window is **not** widened. 50-bit stays
unresolved under ADV-001 honesty.
