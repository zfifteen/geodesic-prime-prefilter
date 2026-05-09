# Bounded Compression Findings

The bounded-compression conjecture uses

```text
C(q) = max(64, ceil(0.5 * log(q)^2))
```

as the finite window for the exact GWR/DNI selected witness.

## Falsification Surfaces

| Surface | Gaps | First failure | Max witness offset | Max cutoff utilization | Extremal witness |
|---|---:|---|---:|---:|---|
| [`1e6`](./dynamic_cutoff_falsification_surface_1e6.md) | `78,494` | `none` | `48` | `0.6153846153846154` | `509^2` |
| [`1e7`](./dynamic_cutoff_falsification_surface_1e7.md) | `664,575` | `none` | `60` | `0.6153846153846154` | `509^2` |

## Current Read

The tested surface grew by an order of magnitude from `1e6` to `1e7`.
The maximum witness offset increased from `48` to `60`, but the maximum
cutoff utilization stayed fixed at `0.6153846153846154`.

The current sharp observed obstruction is the same prime-square witness:

```text
q = 259,033
witness = 259,081 = 509^2
offset = 48
cutoff = 78
utilization = 0.6153846153846154
```

This is measured evidence, not a proof of the dynamic cutoff law.
