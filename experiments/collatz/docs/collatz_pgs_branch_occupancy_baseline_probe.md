# Collatz Branch-Occupancy Baseline Probe

## Summary

The branch-occupancy imbalance is not explained by reset algebra alone. It has
two measured layers:

1. Branch 2 has a divisor-count baseline advantage.
2. Branch 1 leftmost-minimizer successes overwhelmingly fall in terminal-prime
   twin-gap cases, which do not count as below-minimizer Collatz terminal
   source hits.

At odd seeds `s <= 100000000`, branch 2 produced `12218` below-minimizer hits
from `415040` inverse-eligible candidates. Branch 1 produced `41` hits from
`830078` inverse-eligible candidates.

The branch-2 hit rate is:

$$0.029438126445643795$$

The branch-1 hit rate is:

$$0.000049392948614467553$$

The hit-rate ratio is approximately `596x`.

## Divisor-Count Baseline

Branch 1 forces:

$$w \equiv 0 \pmod {18}$$

Branch 2 forces:

$$w \equiv 14 \pmod {18}$$

In the full `100000000` scan, this residue difference appears directly in the
candidate divisor-count profile:

| Branch | Candidates | Median divisor count of `w` | Median lower-divisor competitors | Leftmost-minimizer rate |
|---:|---:|---:|---:|---:|
| `1` | `830078` | `32` | `19` | `0.02420977305747171` |
| `2` | `415040` | `8` | `7` | `0.07427476869699307` |

Branch 2 is about `3.07x` more likely to make `w` the leftmost divisor-count
minimizer in its prime gap.

## Terminal-Source Filter

The large residual appears after minimizer selection. A leftmost minimizer only
becomes a below-minimizer terminal hit when `w-1` is a composite source in the
same prime gap.

Among leftmost-minimizer candidates:

| Branch | Leftmost minimizers | Below-minimizer hits | Hit per leftmost minimizer |
|---:|---:|---:|---:|
| `1` | `20096` | `41` | `0.0020402070063694267` |
| `2` | `30827` | `12218` | `0.39634087001654394` |

This second filter is about `194x` stronger for branch 2.

The reason is visible in the terminal-source strata. Branch-1 leftmost-minimizer
successes mostly occur when `w-1` is prime:

| Branch | `w-1` prime? | Leftmost minimizers | Below-minimizer hits |
|---:|---|---:|---:|
| `1` | `true` | `20055` | `0` |
| `1` | `false` | `41` | `41` |
| `2` | `true` | `18609` | `0` |
| `2` | `false` | `12218` | `12218` |

Branch 1 is not merely losing because its divisor count is higher. It is also
winning the minimizer filter in the wrong geometry: usually with `w` as the
single even interior point of a twin-prime gap, so the terminal source `w-1` is
a prime endpoint instead of a composite Collatz source.

The cross-stratified gap-width rows sharpen this point. Of branch 1's `20055`
terminal-prime leftmost-minimizer cases, `19887` occur in gap width `2`. That
is `99.16230366517078%` of the branch-1 terminal-prime leftmost-minimizer
surface. Branch 1's composite-terminal wins are only `41` total, concentrated
in small non-twin gaps:

| Gap width | Branch-1 composite-terminal hits |
|---:|---:|
| `6` | `37` |
| `8` | `3` |
| `10` | `1` |

Branch 2 has a different geometry. Its `12218` composite-terminal hits spread
across the measured gap-width surface, while `18609` terminal-prime wins are
filtered out. Branch 2 therefore survives both gates at scale: it more often
has low divisor-count rank, and when it wins that rank it much more often has a
composite terminal source.

## Disposition

The divisor-count baseline hypothesis advances, but it does not close the
branch-occupancy explanation by itself. It explains the first layer of the
imbalance: branch 2 has lower divisor-count load and fewer lower-divisor
competitors.

The sharper next target is the terminal-source geometry:

```text
Why does branch 1's leftmost-minimizer success concentrate in terminal-prime
twin-gap geometry, while branch 2 keeps a large composite-terminal surface?
```

This replaces the simpler baseline-only target. The live proof target is now a
two-filter theorem: divisor-count load plus terminal-source eligibility.

## Artifacts

```text
experiments/collatz/scripts/collatz_pgs_branch_occupancy_baseline_probe.py
experiments/collatz/output/collatz_pgs_branch_occupancy_baseline_probe/summary.json
experiments/collatz/output/collatz_pgs_branch_occupancy_baseline_probe/branch_rows.jsonl
experiments/collatz/output/collatz_pgs_branch_occupancy_baseline_probe/terminal_source_rows.jsonl
experiments/collatz/output/collatz_pgs_branch_occupancy_baseline_probe/leftmost_terminal_rows.jsonl
experiments/collatz/output/collatz_pgs_branch_occupancy_baseline_probe/terminal_geometry_rows.jsonl
experiments/collatz/output/collatz_pgs_branch_occupancy_baseline_probe/leftmost_gap_width_rows.jsonl
```
