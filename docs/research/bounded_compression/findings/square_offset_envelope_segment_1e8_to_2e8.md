# Square Offset Envelope Segment 1e8 To 2e8

## Measured Result

The square-branch dynamic-cutoff search found no square-offset counterexample
for odd prime square roots in the segment

```text
100,000,000 <= p <= 200,000,000
```

This is a finite pressure surface for Lemma B:

```text
If the selected witness is r^2 after right-prime q, then r^2 - q < C(q).
```

## Command

```bash
python3 benchmarks/python/predictor/square_branch_dynamic_cutoff_search.py \
  --min-prime 100000000 \
  --max-prime 200000000 \
  --output-dir output/bounded_compression/square_offset_envelope_1e8_to_2e8
```

## Facts

| Field | Value |
|---|---:|
| Root segment requested | `100,000,000 <= p <= 200,000,000` |
| Odd prime squares tested | `5,317,482` |
| First tested prime root | `100,000,007` |
| Last tested prime root | `199,999,991` |
| First counterexample | `none` |
| Max dynamic-cutoff utilization | `0.6784140969162996` |
| Extremal root | `102,017,779` |
| Extremal square | `10,407,627,232,092,841` |
| Previous right prime q | `10,407,627,232,092,379` |
| Square offset | `462` |
| Dynamic cutoff | `681` |
| Elapsed seconds | `85.90383625030518` |

## Branch Maxima

| First-open offset | Root | Previous right prime q | Square offset | Cutoff | Utilization |
|---:|---:|---:|---:|---:|---:|
| `2` | `118,029,731` | `13,931,017,399,931,909` | `452` | `691` | `0.6541244573082489` |
| `4` | `102,017,779` | `10,407,627,232,092,379` | `462` | `681` | `0.6784140969162996` |
| `6` | `181,928,627` | `33,098,025,322,104,653` | `476` | `724` | `0.6574585635359116` |

## Status

This segment did not exceed the earlier square-envelope maximum
`0.8120300751879699` from the `p <= 100,000,000` surface. The square-offset
envelope remains unresolved as a theorem.
