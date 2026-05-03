# Collatz-PGS Source-Position Carrier Probe

## Strongest Measured Result

Favorable carrier strata place PGS witness contact much closer to the reset
transition than unfavorable strata.

The probe used the `1000000` same-gap scale block rows:

```text
output/collatz_pgs_same_gap_scale_probe/block_rows.jsonl
```

For each block, it reconstructed the accelerated odd Collatz source sequence,
attached exact PGS state to every source, and measured where witness contact
occurred inside each exact `odd_steps_to_first_descent` stratum.

## Source-Position Result

| Measurement | Favorable strata | Unfavorable strata |
|---|---:|---:|
| Matched weight share | `0.7457362101345207` | `0.25426378986547926` |
| Weighted mean of stratum median reset delta | `1.3772930090459092` | `-1.2642800241919034` |
| Weighted mean of stratum median final-`v2` delta | `0.5953211176443776` | `0.004912937401824805` |
| Weighted mean witness final-source hit rate | `0.6330294377004576` | `0.2518013666558681` |
| Weighted mean witness first-source hit rate | `0.6977704292513435` | `0.30488752138390346` |
| Weighted mean witness exact-hit rate | `0.7143871575993003` | `0.7488605397709371` |
| Weighted mean no-witness median nearest distance | `4.6576188522722095` | `2.7171551752949434` |

The strongest source-position distinction is terminal contact. Favorable
strata have a matched-weighted final-source witness hit rate more than twice
the unfavorable rate, and they carry a positive median final-`v2` delta.

## Top Carrier Rows

The top favorable exact-step carriers are:

| Odd steps | Median reset delta | Median final-`v2` delta | Final-source hit rate | First-source hit rate |
|---:|---:|---:|---:|---:|
| `1` | `1.3333020663826418` | `1.0` | `1.0` | `1.0` |
| `2` | `1.777651765298709` | `1.0` | `0.4100495489772583` | `0.6464871045610469` |
| `3` | `1.18490479060067` | `0.0` | `0.3673174258857556` | `0.43498787801454636` |

The top unfavorable exact-step carriers are:

| Odd steps | Median reset delta | Median final-`v2` delta | Final-source hit rate | First-source hit rate |
|---:|---:|---:|---:|---:|
| `4` | `-1.5789816202632885` | `0.0` | `0.2873520365364899` | `0.3502656351943331` |
| `5` | `-1.0531645196398938` | `0.0` | `0.2508537085097664` | `0.2944952875290261` |
| `6` | `-1.40452199173247` | `0.0` | `0.21138211382113822` | `0.2768506632434745` |

## Disposition

The reset line has advanced from class enrichment to a source-position
mechanism candidate. Favorable blocks are not merely witness-contact blocks;
their contact is more often at the source that performs the first-descent
reset, and that source more often has a larger terminal `v2` than the matched
no-witness class.

The next direct question is whether the terminal witness-contact effect alone
accounts for the favorable reset profile, or whether nonterminal witness
contact still carries independent reset information after exact-step and
final-`v2` matching.

## Artifact Surface

- Probe: `benchmarks/python/predictor/collatz_pgs_source_position_carrier_probe.py`
- Contract test: `tests/python/predictor/test_collatz_pgs_source_position_carrier_probe.py`
- Summary: `output/collatz_pgs_source_position_carrier_probe/summary.json`
- Source-position rows: `output/collatz_pgs_source_position_carrier_probe/source_position_rows.jsonl`
