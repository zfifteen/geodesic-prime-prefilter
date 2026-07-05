# Square Offset Envelope Segment 3e8 To 4e8

## Measured Result

The square-branch dynamic-cutoff search found no square-offset counterexample
for odd prime square roots in the segment

```text
300,000,000 <= p <= 400,000,000
```

This is a finite pressure surface for Lemma B:

```text
If the selected witness is r^2 after right-prime q, then r^2 - q < C(q).
```

## Command

```bash
python3 research/04-bounded-compression/scripts/square_branch_dynamic_cutoff_search.py \
  --min-prime 300000000 \
  --max-prime 400000000 \
  --output-dir output/bounded_compression/square_offset_envelope_3e8_to_4e8
```

## Facts

| Field | Value |
|---|---:|
| Root segment requested | `300,000,000 <= p <= 400,000,000` |
| Odd prime squares tested | `5,084,001` |
| First tested prime root | `300,000,007` |
| Last tested prime root | `399,999,959` |
| First counterexample | `none` |
| Max dynamic-cutoff utilization | `0.7036082474226805` |
| Extremal root | `358,018,553` |
| Extremal square | `128,177,284,292,213,809` |
| Previous right prime q | `128,177,284,292,213,263` |
| Square offset | `546` |
| Dynamic cutoff | `776` |
| Elapsed seconds | `89.7235472202301` |

## Branch Maxima

| First-open offset | Root | Previous right prime q | Square offset | Cutoff | Utilization |
|---:|---:|---:|---:|---:|---:|
| `2` | `389,358,323` | `151,599,903,689,371,817` | `512` | `783` | `0.6538952745849298` |
| `4` | `358,018,553` | `128,177,284,292,213,263` | `546` | `776` | `0.7036082474226805` |
| `6` | `349,413,007` | `122,089,449,460,781,573` | `476` | `774` | `0.6149870801033591` |

## Status

This segment did not exceed the earlier square-envelope maximum
`0.8120300751879699` from the `p <= 100,000,000` surface. The square-offset
envelope is proved in `PROOF.md` (Prime-Square Proximity Theorem, 2026-07-05).
This segment provides audit corroboration on the tested regime.

Against the record table through `p <= 300,000,000`, this segment preserves
the standing record. It does not create a new square-envelope utilization
record.
