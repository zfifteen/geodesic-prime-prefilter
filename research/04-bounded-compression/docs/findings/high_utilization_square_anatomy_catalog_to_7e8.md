# High-Utilization Square Anatomy Catalog Through 7e8

## Measured Result

This catalog records every square-envelope row with utilization at least
`0.80` through

```text
p <= 700,000,000
```

where `p` is the prime root of the square witness candidate `p^2`.

The scan tested `36,252,930` odd prime roots through `699,999,953` and found
exactly `2` rows with utilization `>= 0.80`.

## Catalog

| Root p | p^2 | Previous prime q | Next prime after q | Gap size | Square offset | Cutoff | Margin | Utilization | d=4 carriers before square | Lower-than-4 carriers before square | First d=4 offset | Selected witness |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `424,171,123` | `179,921,141,587,081,129` | `179,921,141,587,080,391` | `179,921,141,587,081,189` | `798` | `738` | `790` | `52` | `0.9341772151898734` | `96` | `0` | `3` | `179,921,141,587,081,129` |
| `82,357,433` | `6,782,746,770,349,489` | `6,782,746,770,348,949` | `6,782,746,770,349,577` | `628` | `540` | `665` | `125` | `0.8120300751879699` | `63` | `0` | `10` | `6,782,746,770,349,489` |

## Shared Mechanism

Both high-utilization rows have the same measured structure:

```text
many d=4 carriers before the square
zero lower-than-4 carriers before the square
late prime square with d=3
selected witness is the square
```

So on the documented surface through `p <= 700,000,000`, the dangerous square
records do not expose a second obstruction type. They repeat the same local
mechanism as the active record:

```text
many early d=4 carriers -> late prime square with d=3 -> square wins inside cutoff
```

## Status

This is a finite measured catalog, not a proof of the square-offset envelope.
It sharpens the remaining proof target: bound how late prime squares can occur
inside prime gaps relative to `C(q)`.
