# Square Offset Envelope Segment 5e8 To 6e8

## Measured Result

The square-branch dynamic-cutoff search found no square-offset counterexample
for odd prime square roots in the segment

```text
500,000,000 <= p <= 600,000,000
```

This segment did not create a new square-envelope utilization record.

## Command

```bash
python3 benchmarks/python/predictor/square_branch_dynamic_cutoff_search.py \
  --min-prime 500000000 \
  --max-prime 600000000 \
  --output-dir output/bounded_compression/square_offset_envelope_5e8_to_6e8
```

## Facts

| Field | Value |
|---|---:|
| Root segment requested | `500,000,000 <= p <= 600,000,000` |
| Odd prime squares tested | `4,968,836` |
| First tested prime root | `500,000,003` |
| Last tested prime root | `599,999,971` |
| First counterexample | `none` |
| Max dynamic-cutoff utilization | `0.6691449814126395` |
| Extremal root | `526,336,897` |
| Extremal square | `277,030,529,143,588,609` |
| Previous right prime q | `277,030,529,143,588,069` |
| Square offset | `540` |
| Dynamic cutoff | `807` |
| Elapsed seconds | `86.49722003936768` |

## Branch Maxima

| First-open offset | Root | Previous right prime q | Square offset | Cutoff | Utilization |
|---:|---:|---:|---:|---:|---:|
| `2` | `559,790,419` | `313,365,313,204,195,019` | `542` | `812` | `0.6674876847290641` |
| `4` | `526,336,897` | `277,030,529,143,588,069` | `540` | `807` | `0.6691449814126395` |
| `6` | `547,836,239` | `300,124,544,761,664,633` | `488` | `810` | `0.6024691358024692` |

## Status

This segment does not falsify the Dynamic Cutoff Conjecture. It preserves the
standing square-envelope utilization record `0.9341772151898734` from the
`4e8` to `5e8` segment.
