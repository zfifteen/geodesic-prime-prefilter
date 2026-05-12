# PGS-GEOFAC Clean RSA Calibration Ladder v2

The repaired RSA experiment starts with a clean calibration ladder from 40
through 100 bits.

The purpose is to test whether PGS inference and elimination can contract an
RSA-260 mirror chamber under a clean evidence boundary. The ladder is not an
RSA-260 result. It is the first repaired measurement surface after the withdrawn
side experiment.

The active implementation lives under:

```text
research/06-cryptology-rsa/experiments/rsa/v2
```

The old contaminated artifacts are preserved under:

```text
experiments/rsa/chat-gpt-fraud-and-deception
```

## Boundary

Inference reads only `ladder_cases.jsonl`. That file contains public case data:
`case_id`, `bits`, `N`, `radius`, and configuration fields.

Audit factors are physically separate in `audit_factors.jsonl`. The inference
script does not read that file.

The chamber radius is public and bit-derived:

```text
radius = 2 ** max(10, bits // 5 + 2)
```

Rows that exceed the clean endpoint-measurement budget are reported as
`unresolved`. The script does not widen the chamber from hidden factors.
