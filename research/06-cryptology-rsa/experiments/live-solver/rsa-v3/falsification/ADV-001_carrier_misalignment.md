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
