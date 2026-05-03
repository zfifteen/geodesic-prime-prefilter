# Collatz-PGS Reset Carrier-Strata Probe

## Strongest Measured Result

The matched reset-strength effect is carried mainly by exact odd-step strata
`1`, `2`, and `3`.

The probe used the `1000000` same-gap scale block rows:

```text
output/collatz_pgs_same_gap_scale_probe/block_rows.jsonl
```

It reconstructed each seed's accelerated odd Collatz transition exponents and
measured which exact `odd_steps_to_first_descent` strata contribute most to
the matched-weighted mean of stratum median reset deltas.

## Carrier Result

| Measurement | Value |
|---|---:|
| Matched exact odd-step strata | `37` |
| Matched weight total | `117677` |
| Net weighted mean of stratum median reset delta | `0.7056366384084134` |
| Positive delta contribution sum | `1.0270972688106665` |
| Negative delta contribution sum | `-0.32146063040225314` |
| Favorable strata | `19` |
| Favorable matched weight share | `0.7457362101345207` |
| Unfavorable strata | `18` |
| Unfavorable matched weight share | `0.25426378986547926` |

The top favorable exact-step carriers are:

| Odd steps | Matched weight share | Median reset delta | Delta contribution |
|---:|---:|---:|---:|
| `1` | `0.3286878489424441` | `1.3333020663826418` | `0.4382401881898264` |
| `2` | `0.1337729547830077` | `1.777651765298709` | `0.23780172921923806` |
| `3` | `0.19979265276987007` | `1.18490479060067` | `0.23673527139383527` |

The top unfavorable exact-step carriers are:

| Odd steps | Matched weight share | Median reset delta | Delta contribution |
|---:|---:|---:|---:|
| `4` | `0.09117329639606721` | `-1.5789816202632885` | `-0.14396095926820723` |
| `5` | `0.1079310315524699` | `-1.0531645196398938` | `-0.11366913299919518` |
| `6` | `0.03999932017301597` | `-1.40452199173247` | `-0.056179924837349154` |

## Transition Composition

The favorable strata have matched-weighted mean stratum `v2`-sum delta
`0.016813586258384344`. The unfavorable strata have matched-weighted mean
stratum `v2`-sum delta `-0.01430564096329122`.

The coarse `v2`-bin rate deltas are small:

| Carrier group | `v2=1` | `v2=2` | `v2=3-4` | `v2>=5` |
|---|---:|---:|---:|---:|
| Favorable | `-0.0015549370599237846` | `-0.0023711822305293373` | `0.0027984961308922685` | `0.0011276231595608816` |
| Unfavorable | `-0.0002497367803061564` | `0.0007675503981730652` | `-0.00030337775731017417` | `-0.0002144358605567675` |

The current signal localizes to exact step strata more strongly than to coarse
transition-bin composition.

## Follow-On Result

The follow-on source-position carrier probe measured where witness contact
occurs inside each exact-step block:

```text
docs/collatz_pgs_source_position_carrier_probe.md
```

Favorable strata have matched-weighted final-source witness hit rate
`0.6330294377004576`; unfavorable strata have `0.2518013666558681`. Favorable
strata also carry matched-weighted median final-`v2` delta
`0.5953211176443776`, while unfavorable strata are nearly flat at
`0.004912937401824805`.

## Disposition

The reset-profile line has advanced from a global class comparison to an
identified carrier surface and then to a source-position mechanism candidate.
The positive matched reset effect is concentrated in short first-descent blocks
where witness contact is more often terminal and the final transition has a
larger `v2`.

The next direct question is whether terminal witness contact alone accounts
for the favorable reset profile after exact-step and final-`v2` matching.

## Artifact Surface

- Probe: `scripts/collatz_pgs_reset_carrier_strata_probe.py`
- Contract test: `tests/test_collatz_pgs_reset_carrier_strata_probe.py`
- Summary: `output/collatz_pgs_reset_carrier_strata_probe/summary.json`
- Carrier rows: `output/collatz_pgs_reset_carrier_strata_probe/carrier_rows.jsonl`
