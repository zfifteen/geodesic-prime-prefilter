# Collatz-PGS Terminal Adjacent Side Probe

## Strongest Measured Result

The adjacent projected terminal advantage is one-sided on the measured surface.
It is carried by final sources at `witness - 1`, not by final sources at
`witness + 1`.

The probe used the `1000000` same-gap scale block rows:

```text
output/collatz_pgs_same_gap_scale_probe/block_rows.jsonl
```

It split adjacent projected terminal witness contact into:

- below-witness terminal hit: final source equals `witness - 1`;
- above-witness terminal hit: final source equals `witness + 1`.

Exact terminal witness hits were counted for conservation, but excluded from
the side comparison. All comparisons were matched inside exact
`(odd_steps_to_first_descent, final_v2)` strata.

## Side Result

| Measurement | Value |
|---|---:|
| Below-witness terminal blocks | `12876` |
| Above-witness terminal blocks | `2682` |
| Exact terminal blocks | `54669` |
| Nonterminal witness-contact blocks | `90979` |
| No-witness-contact blocks | `338793` |
| Below-vs-above matched strata | `112` |
| Below-vs-above matched weight | `2254` |
| Below higher strata | `73` |
| Above higher strata | `39` |
| Weighted mean of stratum median reset delta | `0.9934374958512522` |
| Weighted mean of stratum median reset ratio | `1.1600562928929092` |
| Weighted mean of stratum P90 reset delta | `0.9997759684812527` |

The positive below-vs-above delta means final sources at `witness - 1` reset
harder than final sources at `witness + 1` under the current exact-step and
final-`v2` matching.

## Comparison Against No-Witness Blocks

| Comparison | Matched strata | Matched weight | Median reset delta | Median reset ratio | P90 reset delta |
|---|---:|---:|---:|---:|---:|
| Below-witness vs no-witness | `175` | `12813` | `0.48311171458205104` | `1.0866506651606216` | `-0.06565152576687666` |
| Above-witness vs no-witness | `133` | `2667` | `-0.20290860147945028` | `1.0062749350113096` | `-1.4323717805223977` |

The below-witness side remains positive against no-witness blocks on the
primary median-reset delta. The above-witness side does not: its weighted mean
of stratum median reset deltas is negative, even though its weighted mean of
stratum median reset ratios is slightly above `1.0`.

## Disposition

This is the cleanest localization so far. The terminal signal first survived
the final-source control, then moved from exact terminal specificity into
adjacent terminal geometry, and now lands mostly on one side of the witness.
The Collatz reset geometry is not merely touching the PGS witness neighborhood;
it prefers the odd cell immediately before the witness.

The upper tail is less clean. Below-witness blocks beat no-witness blocks on
median reset delta, but their P90 delta against no-witness blocks is slightly
negative. That makes the next question a stability question rather than a
broader enrichment question.

## Follow-On Stability Result

The follow-on below-witness stability probe found that below-witness terminal
contact is stable against above-witness terminal contact across median, P90,
and P99 reset comparisons. Against no-witness blocks, the median signal
survives with weighted mean delta `0.48311171458205104`, but the tails reverse:
P90 delta is `-0.06565152576687666` and P99 delta is
`-0.08685398078967067`.

The next direct question is an exact carrier-family decomposition of the
below-vs-no-witness comparison.

## Second-Opinion Check

A second-opinion pressure pass agreed that the estimand supports the measured
read: the adjacent projected terminal advantage is carried by `witness - 1`,
not `witness + 1`, under the current matching. It flagged the same residual
risk: below-vs-no-witness has a positive median-reset delta but a negative P90
delta. The follow-on stability check confirmed that split.

## Artifact Surface

- Probe: `scripts/collatz_pgs_terminal_adjacent_side_probe.py`
- Contract test: `tests/test_collatz_pgs_terminal_adjacent_side_probe.py`
- Summary: `output/collatz_pgs_terminal_adjacent_side_probe/summary.json`
- Strata rows: `output/collatz_pgs_terminal_adjacent_side_probe/strata_rows.jsonl`
