# Square Offset Envelope Surface Through 1e8

## Measured Result

The square-branch dynamic-cutoff search found no square-offset counterexample
for odd prime squares with root `p <= 100,000,000`.

This is a pressure surface for Lemma B in the bounded-compression proof
skeleton:

```text
If the selected witness is r^2 after right-prime q, then r^2 - q < C(q).
```

## Source Artifacts

```text
research/02-gwr-dni/output/gwr_proof/square_branch_dynamic_cutoff_search_1e8/square_branch_dynamic_cutoff_search_summary.json
research/02-gwr-dni/output/gwr_proof/square_branch_dynamic_cutoff_search_1e8/square_branch_dynamic_cutoff_search_frontier.csv
```

## Facts

| Field | Value |
|---|---:|
| Root range tested | `3 <= p <= 100,000,000` |
| Odd prime squares tested | `5,761,454` |
| First tested prime root | `3` |
| Last tested prime root | `99,999,989` |
| First counterexample | `none` |
| Max dynamic-cutoff utilization | `0.8120300751879699` |
| Extremal root | `82,357,433` |
| Extremal square | `6,782,746,770,349,489` |
| Previous right prime q | `6,782,746,770,348,949` |
| Square offset | `540` |
| Dynamic cutoff | `665` |

## Branch Maxima

| First-open offset | Root | Previous right prime q | Square offset | Cutoff | Utilization |
|---:|---:|---:|---:|---:|---:|
| `2` | `1,487,539` | `2,212,772,276,237` | `284` | `404` | `0.7029702970297029` |
| `4` | `82,357,433` | `6,782,746,770,348,949` | `540` | `665` | `0.8120300751879699` |
| `6` | `33,701,407` | `1,135,784,833,779,203` | `446` | `601` | `0.7420965058236273` |

## Status

This is a finite measured square-branch surface, not a proof of the dynamic
cutoff law. It strengthens the empirical pressure on the square-offset
envelope by pushing the obstruction family far beyond the full `q <= 10^7`
right-prime surface.
