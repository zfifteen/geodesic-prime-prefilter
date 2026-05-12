# Collatz Branch-Occupancy Baseline Probe

## Summary

The focused terminal-geometry pass closes the measured explanation for the
current scan surface.

Branch 1 concentration is explained by automatic twin-gap terminal-prime wins
plus a fully enumerated small composite-terminal exception family. Branch 2's
composite-terminal surface persists across nontrivial gaps.

At odd seeds `s <= 100000000`, branch 2 produced `12218` below-minimizer hits
from `415040` inverse-eligible candidates. Branch 1 produced `41` hits from
`830078` inverse-eligible candidates.

The branch-2 hit rate is:

$$0.029438126445643795$$

The branch-1 hit rate is:

$$0.000049392948614467553$$

The hit-rate ratio is approximately `596x`.

## Terminal Geometry

A leftmost divisor-count minimizer becomes a below-minimizer terminal hit only
when `w-1` is composite. If `w-1` is prime, the Collatz terminal source is a
prime endpoint, not a composite interior source below the minimizer.

Among leftmost-minimizer successes, the measured surface splits as follows:

| Branch | Automatic twin terminal-prime | Terminal-prime non-twin | Composite below-minimizer | Total leftmost |
|---:|---:|---:|---:|---:|
| `1` | `19887` | `168` | `41` | `20096` |
| `2` | `0` | `18609` | `12218` | `30827` |

For branch 1, `19887 / 20096` leftmost successes are automatic twin-gap
terminal-prime wins. That is `98.9609872611465%` of the branch-1 leftmost
surface. Among branch-1 terminal-prime leftmost successes, `19887 / 20055`
are twin-gap cases, or `99.16230366517078%`.

Branch 2 has no automatic twin-gap channel in the measured leftmost surface.
Its `12218` composite-terminal leftmost successes are `39.634087001654394%`
of branch-2 leftmost wins.

The branch-1 composite-terminal exceptions are fully enumerated in the output.
All `41` have `terminal_geometry = composite_below_minimizer` and
`witness_tau = 12`.

| Gap width | Branch-1 composite-terminal exceptions |
|---:|---:|
| `6` | `37` |
| `8` | `3` |
| `10` | `1` |

This answers the focused question for the measured `s <= 100000000`, `k=4`
and `k=8` surface:

```text
Branch 1 mostly wins the minimizer filter in twin gaps, where w is the only
interior integer and w-1 is a prime endpoint. Branch 2 wins in nontrivial
gaps often enough that w-1 remains a composite interior terminal source.
```

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

The measured explanation is closed as a bounded certificate. Branch 1's
terminal-prime concentration is not vague; it is the automatic twin-gap channel
plus `168` non-twin terminal-prime wins and `41` fully enumerated
composite-terminal exceptions. Branch 2 keeps a large composite-terminal
surface because its leftmost-minimizer wins are not dominated by the twin
endpoint channel.

This is not yet a universal theorem. The next theorem target is branch-1 only:
prove symbolically why the composite-terminal exception family is restricted
to $w=18u$ with $u$ prime, divisor count `12`, and gap width `6`, `8`, or `10`.
The branch-2 nontrivial-gap occupancy mechanism stays parked until that
obstruction is resolved.

## Artifacts

```text
research/08-collatz/scripts/collatz_pgs_branch_occupancy_baseline_probe.py
research/08-collatz/output/collatz_pgs_branch_occupancy_baseline_probe/summary.json
research/08-collatz/output/collatz_pgs_branch_occupancy_baseline_probe/branch_rows.jsonl
research/08-collatz/output/collatz_pgs_branch_occupancy_baseline_probe/terminal_source_rows.jsonl
research/08-collatz/output/collatz_pgs_branch_occupancy_baseline_probe/leftmost_terminal_rows.jsonl
research/08-collatz/output/collatz_pgs_branch_occupancy_baseline_probe/terminal_geometry_rows.jsonl
research/08-collatz/output/collatz_pgs_branch_occupancy_baseline_probe/leftmost_geometry_rows.jsonl
research/08-collatz/output/collatz_pgs_branch_occupancy_baseline_probe/leftmost_gap_width_rows.jsonl
research/08-collatz/output/collatz_pgs_branch_occupancy_baseline_probe/branch1_composite_exception_rows.jsonl
research/08-collatz/output/collatz_pgs_branch_occupancy_baseline_probe/branch1_exception_symbolic_summary.json
```
