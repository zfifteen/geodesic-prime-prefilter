# Dynamic Cutoff Falsification Surface Through 1e7

## Measured Result

The bounded-compression falsification runner found no dynamic-cutoff failure on
the exact consecutive right-prime surface through `q <= 10,000,000`.

## Command

```bash
python3 benchmarks/python/predictor/bounded_compression_falsification_runner.py \
  --min-right-prime 11 \
  --max-right-prime 10000000 \
  --output-dir output/bounded_compression/falsification_1e7
```

## Facts

| Field | Value |
|---|---:|
| Range tested | `11 <= q <= 10,000,000` |
| First tested q | `11` |
| Last tested q | `9,999,991` |
| Gaps tested | `664,575` |
| First failure | `none` |
| Max witness offset | `60` |
| Max cutoff utilization | `0.6153846153846154` |
| Extremal q by cutoff utilization | `259,033` |
| Commit | containing commit for this finding |

## Extremal Utilization Row

| Field | Value |
|---|---:|
| q | `259,033` |
| Next prime | `259,099` |
| Gap width | `66` |
| Extremal witness | `259,081` |
| Witness offset | `48` |
| Witness divisor count | `3` |
| Cutoff | `78` |
| Cutoff utilization | `0.6153846153846154` |
| First interior prime square | `259,081 = 509^2` |
| Selected witness is prime square | `true` |
| Square offset minus witness offset | `0` |

## Test Status

```text
8 passed in 59.90s
```

## Status

This is a finite measured surface, not a proof of the dynamic cutoff law. It
certifies that this executable falsification run found no counterexample on
the stated range. The maximum-utilization row is square-branch sharp.
