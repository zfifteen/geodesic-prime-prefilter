# Square Offset Envelope Segment 4e8 To 5e8

## Measured Result

The square-branch dynamic-cutoff search found no square-offset counterexample
for odd prime square roots in the segment

```text
400,000,000 <= p <= 500,000,000
```

This segment created a new square-envelope utilization record below `1`.

## Command

```bash
python3 benchmarks/python/predictor/square_branch_dynamic_cutoff_search.py \
  --min-prime 400000000 \
  --max-prime 500000000 \
  --output-dir output/bounded_compression/square_offset_envelope_4e8_to_5e8
```

## Facts

| Field | Value |
|---|---:|
| Root segment requested | `400,000,000 <= p <= 500,000,000` |
| Odd prime squares tested | `5,019,541` |
| First tested prime root | `400,000,009` |
| Last tested prime root | `499,999,993` |
| First counterexample | `none` |
| Max dynamic-cutoff utilization | `0.9341772151898734` |
| Extremal root | `424,171,123` |
| Extremal square | `179,921,141,587,081,129` |
| Previous right prime q | `179,921,141,587,080,391` |
| Square offset | `738` |
| Dynamic cutoff | `790` |
| Elapsed seconds | `89.23751616477966` |

## Branch Maxima

| First-open offset | Root | Previous right prime q | Square offset | Cutoff | Utilization |
|---:|---:|---:|---:|---:|---:|
| `2` | `468,917,503` | `219,883,624,619,754,467` | `542` | `798` | `0.6791979949874687` |
| `4` | `482,342,527` | `232,654,313,352,745,243` | `486` | `800` | `0.6075` |
| `6` | `424,171,123` | `179,921,141,587,080,391` | `738` | `790` | `0.9341772151898734` |

## Status

This segment does not falsify the Dynamic Cutoff Conjecture. It updates the
standing square-envelope utilization record from `0.8120300751879699` to
`0.9341772151898734`.
