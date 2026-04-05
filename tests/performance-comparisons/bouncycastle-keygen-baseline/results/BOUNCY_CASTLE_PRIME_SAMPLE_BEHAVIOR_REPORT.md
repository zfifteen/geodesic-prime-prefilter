# Bouncy Castle Prime Sample Behavior Probe

Date: 2026-04-04

The baseline helper exactly reproduces `BigIntegers.createRandomPrime(bitLength, 1, random)` for the first `1024` outputs on every panel.

The DCI-prefiltered helper is characterized against that matched baseline helper on coarse output metrics. These labels are descriptive only and come from the report's coarse TVD and concentration heuristics.

| Panel | Fidelity | Histogram TVD | Mod 30 TVD | Mod 210 TVD | Visibility | Pattern |
|---|---|---:|---:|---:|---|---|
| `256` bits | `exact` | `0.000000000000` | `0.000000000000` | `0.000000000000` | `not_obvious` | `diffuse` |
| `2048` bits | `exact` | `0.000000000000` | `0.000000000000` | `0.000000000000` | `not_obvious` | `diffuse` |

| Panel | Prefilter Rejects | Raw Starts Mean (Before -> After) | Walk Increments Mean (Before -> After) |
|---|---:|---:|---:|
| `256` bits | `117587` (`113130` primary, `4457` tail) | `15.167602539063 -> 15.167602539063` | `65.230224609375 -> 65.230224609375` |
| `2048` bits | `231725` (`223320` primary, `8405` tail) | `119.761718750000 -> 119.761718750000` | `515.044433593750 -> 515.044433593750` |

## 256-Bit Panel

Coarse drift is `not_obvious`, and the dominant metric is `normalized_histogram` with top-five contribution share `0.000000000000`, so the reported pattern is `diffuse`.

Largest changes in the dominant metric:
- `bucket 0 [0.000000000000, 0.015625000000)`: baseline `258`, after `258`, |delta| `0.000000000000`
- `bucket 1 [0.015625000000, 0.031250000000)`: baseline `248`, after `248`, |delta| `0.000000000000`
- `bucket 2 [0.031250000000, 0.046875000000)`: baseline `216`, after `216`, |delta| `0.000000000000`
- `bucket 3 [0.046875000000, 0.062500000000)`: baseline `248`, after `248`, |delta| `0.000000000000`
- `bucket 4 [0.062500000000, 0.078125000000)`: baseline `227`, after `227`, |delta| `0.000000000000`

## 2048-Bit Panel

Coarse drift is `not_obvious`, and the dominant metric is `normalized_histogram` with top-five contribution share `0.000000000000`, so the reported pattern is `diffuse`.

Largest changes in the dominant metric:
- `bucket 0 [0.000000000000, 0.015625000000)`: baseline `65`, after `65`, |delta| `0.000000000000`
- `bucket 1 [0.015625000000, 0.031250000000)`: baseline `76`, after `76`, |delta| `0.000000000000`
- `bucket 2 [0.031250000000, 0.046875000000)`: baseline `67`, after `67`, |delta| `0.000000000000`
- `bucket 3 [0.046875000000, 0.062500000000)`: baseline `60`, after `60`, |delta| `0.000000000000`
- `bucket 4 [0.062500000000, 0.078125000000)`: baseline `74`, after `74`, |delta| `0.000000000000`

Artifacts:
- [`bcprov-jdk18on-1.83-source-r1rv83-prime-sample-behavior-seed-byte-42.json`](./bcprov-jdk18on-1.83-source-r1rv83-prime-sample-behavior-seed-byte-42.json)
- [`BOUNCY_CASTLE_PRIME_SAMPLE_BEHAVIOR_REPORT.md`](./BOUNCY_CASTLE_PRIME_SAMPLE_BEHAVIOR_REPORT.md)
