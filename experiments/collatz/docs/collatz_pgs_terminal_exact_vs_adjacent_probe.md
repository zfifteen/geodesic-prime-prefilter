# Collatz-PGS Terminal Exact Versus Adjacent Probe

## Strongest Measured Result

Exact terminal witness hits do not carry the terminal reset profile more
strongly than adjacent projected terminal hits on the measured surface.

The probe used the `1000000` same-gap scale block rows:

```text
output/collatz_pgs_same_gap_scale_probe/block_rows.jsonl
```

It split terminal witness-contact blocks into:

- exact terminal witness hit: final source equals the PGS witness;
- adjacent projected terminal witness hit: final source equals the odd cell
  immediately beside the PGS witness.

All comparisons were matched inside exact
`(odd_steps_to_first_descent, final_v2)` strata.

## Exact Versus Adjacent Result

| Measurement | Value |
|---|---:|
| Exact terminal blocks | `54669` |
| Adjacent projected terminal blocks | `15558` |
| Nonterminal witness-contact blocks | `90979` |
| No-witness-contact blocks | `338793` |
| Exact-vs-adjacent matched strata | `227` |
| Exact-vs-adjacent matched weight | `15524` |
| Exact higher strata | `98` |
| Adjacent higher strata | `129` |
| Weighted mean of stratum median reset delta | `-0.29644357588214204` |
| Weighted mean of stratum median reset ratio | `0.9803814153462154` |
| Weighted mean of stratum P90 reset delta | `0.13356896780162025` |

The negative median-reset delta means adjacent projected terminal hits have the
stronger median reset profile than exact terminal hits after exact-step and
final-`v2` matching.

## Comparison Against No-Witness Blocks

| Comparison | Matched strata | Matched weight | Median reset delta | Median reset ratio |
|---|---:|---:|---:|---:|
| Exact terminal vs no-witness | `259` | `53361` | `0.22135903401835988` | `1.0430527903690756` |
| Adjacent terminal vs no-witness | `199` | `15473` | `0.4047035698439424` | `1.0756384568540225` |

Both terminal subclasses remain positive against no-witness blocks. The
adjacent subclass is smaller, but it is the sharper median-reset subclass in
this matched comparison.

## Disposition

This is a good correction. The previous terminal-geometry result said positive
terminal carriers were more exact-witness-centered than negative carriers. That
remains true as a carrier-composition fact. The direct subclass comparison says
something different: once exact and adjacent terminal hits are compared inside
the same exact step and final-`v2` strata, adjacent projected hits carry the
stronger median reset profile.

The signal did not vanish under the split. It moved. Terminal contact remained
live, but the cleanest follow-on target was no longer exact terminal
specificity. It became adjacent-side geometry: determine whether the adjacent
advantage was carried by sources immediately below the witness, immediately
above the witness, or both.

## Follow-On Side Result

The follow-on adjacent-side probe found that the adjacent projected terminal
advantage is carried by final sources at `witness - 1`. Below-witness terminal
hits beat above-witness terminal hits directly with weighted mean of stratum
median reset delta `0.9934374958512522`, and remained positive against
no-witness blocks with delta `0.48311171458205104`. Above-witness terminal
hits did not carry the median-reset delta against no-witness blocks; their
delta was `-0.20290860147945028`.

## Second-Opinion Check

A second-opinion pressure pass agreed that the estimand supports the measured
read: adjacent projected terminal hits carry the stronger median reset profile
under the current exact-step and final-`v2` matching. It identified the same
main residual risk: the adjacent class mixes the `witness - 1` and `witness + 1`
cells. The follow-on side split resolved that mixture in favor of
`witness - 1`.

## Artifact Surface

- Probe: `scripts/collatz_pgs_terminal_exact_vs_adjacent_probe.py`
- Contract test: `tests/test_collatz_pgs_terminal_exact_vs_adjacent_probe.py`
- Summary: `output/collatz_pgs_terminal_exact_vs_adjacent_probe/summary.json`
- Strata rows: `output/collatz_pgs_terminal_exact_vs_adjacent_probe/strata_rows.jsonl`
