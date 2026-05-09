# Square Offset Envelope Segment 2e8 To 3e8

## Measured Result

The square-branch dynamic-cutoff search found no square-offset counterexample
for odd prime square roots in the segment

```text
200,000,000 <= p <= 300,000,000
```

This is a finite pressure surface for Lemma B:

```text
If the selected witness is r^2 after right-prime q, then r^2 - q < C(q).
```

## Command

```bash
python3 benchmarks/python/predictor/square_branch_dynamic_cutoff_search.py \
  --min-prime 200000000 \
  --max-prime 300000000 \
  --output-dir output/bounded_compression/square_offset_envelope_2e8_to_3e8
```

## Facts

| Field | Value |
|---|---:|
| Root segment requested | `200,000,000 <= p <= 300,000,000` |
| Odd prime squares tested | `5,173,388` |
| First tested prime root | `200,000,033` |
| Last tested prime root | `299,999,977` |
| First counterexample | `none` |
| Max dynamic-cutoff utilization | `0.7209612817089452` |
| Extremal root | `251,066,071` |
| Extremal square | `63,034,172,007,377,041` |
| Previous right prime q | `63,034,172,007,376,501` |
| Square offset | `540` |
| Dynamic cutoff | `749` |
| Elapsed seconds | `86.04056406021118` |

## Branch Maxima

| First-open offset | Root | Previous right prime q | Square offset | Cutoff | Utilization |
|---:|---:|---:|---:|---:|---:|
| `2` | `247,133,951` | `61,075,189,736,869,949` | `452` | `747` | `0.6050870147255689` |
| `4` | `248,209,931` | `61,608,169,847,024,239` | `522` | `748` | `0.6978609625668449` |
| `6` | `251,066,071` | `63,034,172,007,376,501` | `540` | `749` | `0.7209612817089452` |

## Status

This segment did not exceed the earlier square-envelope maximum
`0.8120300751879699` from the `p <= 100,000,000` surface. The square-offset
envelope remains unresolved as a theorem.
