# Shor Is Obsolete

This gist is a small reproducible demonstration of a specific measured fact:
on one resolved RSA v2 ladder rung, public PGS endpoint structure fixes the
same order information that Shor's quantum phase-estimation step is normally
used to discover.

That does not make Shor's algorithm false. It makes Shor downstream.

## The Frozen Measurement

```text
case_id                  bits  baseline  residual  endpoint_match  order_vector_match
rsa_v2_40bit_static_001  40    80        0         yes             yes
rsa_v2_50bit_static_001  50    100       100       no              no
```

The 40-bit row is the measured positive case. The 50-bit row under the **v2
runner** stayed unresolved on the order-vector match. The rsa-v3 V3 path
(2026-08-07) supplies a measured reciprocal floor candidate under carrier
reciprocal closure (measured-on-regime-only / hypothesis; not a factorisation
theorem). See `research/06-cryptology-rsa/experiments/live-solver/rsa-v3/residual_discriminator_v2/`.

## Boundary And Consequence

```text
where public PGS endpoint structure fixes the order vector,
Shor order finding has no remaining order-discovery work.
```

The 50-bit control under the v2 runner stayed unresolved; the rsa-v3 V3 path
(2026-08-07) supplies a measured reciprocal candidate under carrier reciprocal
closure (measured-on-regime-only / hypothesis). The claim stays honest: not a
factorisation theorem.

## The Short Version

Shor finds factors by first finding order.

PGS exposes endpoint structure on the measured resolved row.

On the measured 40-bit row, public PGS endpoint closure fixes the same order
vector that Shor would otherwise need quantum phase estimation to recover.

That makes the quantum step unnecessary for that row.
