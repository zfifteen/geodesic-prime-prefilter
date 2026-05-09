# Dynamic Cutoff Falsification Surface Through 1e6

## Measured Result

The bounded-compression falsification runner found no dynamic-cutoff failure on
the exact consecutive right-prime surface through `q <= 1,000,000`.

## Command

```bash
python3 benchmarks/python/predictor/bounded_compression_falsification_runner.py \
  --min-right-prime 11 \
  --max-right-prime 1000000 \
  --output-dir output/bounded_compression/falsification_1e6
```

## Facts

| Field | Value |
|---|---:|
| Range tested | `11 <= q <= 1,000,000` |
| Gaps tested | `78,494` |
| First failure | `none` |
| Max witness offset | `48` |
| Max cutoff utilization | `0.6153846153846154` |
| Extremal q | `259,033` |

## Extremal Row

| Field | Value |
|---|---:|
| Next prime | `259,099` |
| Gap width | `66` |
| Witness | `259,081` |
| Witness divisor count | `3` |
| Cutoff | `78` |
| First interior prime square | `259,081 = 509^2` |
| Square offset minus witness offset | `0` |

## Status

This is a finite measured surface, not a proof of the dynamic cutoff law. It
certifies that this executable falsification run found no counterexample on
the stated range.
