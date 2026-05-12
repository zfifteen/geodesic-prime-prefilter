# Square Offset Envelope Surface From 1e8 To 2e8

## Measured Result

The square-branch dynamic-cutoff search found no square-offset counterexample
for odd prime-square roots in the segment

```text
100,000,001 <= r <= 200,000,000.
```

This is a finite measured square-branch surface. It is not a proof of the
all-scale square-branch theorem.

## Source Artifacts

```text
research/04-bounded-compression/output/square_branch_dynamic_cutoff_search_1e8_2e8/square_branch_dynamic_cutoff_search_summary.json
research/04-bounded-compression/output/square_branch_dynamic_cutoff_search_1e8_2e8/square_branch_dynamic_cutoff_search_frontier.csv
```

## Facts

| Field | Value |
|---|---:|
| Root range requested | `100,000,001 <= r <= 200,000,000` |
| First tested prime root | `100,000,007` |
| Last tested prime root | `199,999,991` |
| Odd prime squares tested | `5,317,482` |
| First counterexample | `none` |
| Max dynamic-cutoff utilization | `0.6784140969162996` |
| Extremal root | `102,017,779` |
| Extremal square | `10,407,627,232,092,841` |
| Previous prime | `10,407,627,232,092,379` |
| Square offset | `462` |
| Dynamic cutoff | `681` |

## Branch Maxima

| First-open offset | Root | Previous prime | Square offset | Cutoff | Utilization |
|---:|---:|---:|---:|---:|---:|
| `2` | `118,029,731` | `13,931,017,399,931,909` | `452` | `691` | `0.6541244573082489` |
| `4` | `102,017,779` | `10,407,627,232,092,379` | `462` | `681` | `0.6784140969162996` |
| `6` | `181,928,627` | `33,098,025,322,104,653` | `476` | `724` | `0.6574585635359116` |

## Status

This segment strengthens the square-branch evidence beyond the retained
`r <= 100,000,000` surface. It does not change theorem status: the
square-branch bound remains unresolved until the prime-square proximity
theorem recorded in `PROOF.md` is proved.
