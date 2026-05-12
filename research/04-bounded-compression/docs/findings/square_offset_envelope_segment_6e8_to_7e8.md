# Square Offset Envelope Segment 6e8 To 7e8

## Measured Result

The square-branch dynamic-cutoff search found no square-offset counterexample
for odd prime square roots in the segment

```text
600,000,000 <= p <= 700,000,000
```

This segment did not create a new square-envelope utilization record.

## Command

```bash
python3 research/04-bounded-compression/scripts/square_branch_dynamic_cutoff_search.py \
  --min-prime 600000000 \
  --max-prime 700000000 \
  --output-dir output/bounded_compression/square_offset_envelope_6e8_to_7e8
```

## Facts

| Field | Value |
|---|---:|
| Root segment requested | `600,000,000 <= p <= 700,000,000` |
| Odd prime squares tested | `4,928,228` |
| First tested prime root | `600,000,001` |
| Last tested prime root | `699,999,953` |
| First counterexample | `none` |
| Max dynamic-cutoff utilization | `0.7161997563946407` |
| Extremal root | `622,805,873` |
| Extremal square | `387,887,155,443,292,129` |
| Previous right prime q | `387,887,155,443,291,541` |
| Square offset | `588` |
| Dynamic cutoff | `821` |
| Elapsed seconds | `90.63133597373962` |

## Branch Maxima

| First-open offset | Root | Previous right prime q | Square offset | Cutoff | Utilization |
|---:|---:|---:|---:|---:|---:|
| `2` | `624,487,471` | `389,984,601,435,975,311` | `530` | `821` | `0.6455542021924482` |
| `4` | `696,038,383` | `484,469,430,609,254,149` | `540` | `830` | `0.6506024096385542` |
| `6` | `622,805,873` | `387,887,155,443,291,541` | `588` | `821` | `0.7161997563946407` |

## Status

This segment does not falsify the Dynamic Cutoff Conjecture. It preserves the
standing square-envelope utilization record `0.9341772151898734` from the
`4e8` to `5e8` segment.
