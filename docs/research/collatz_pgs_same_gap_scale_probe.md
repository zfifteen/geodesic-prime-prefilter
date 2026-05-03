# Collatz-PGS Same-Gap Scale Probe

## Strongest Measured Result

For odd Collatz seeds `3 <= s <= 999999`, PGS-selected same-gap witness contact
remains enriched above the containing-gap background.

The `1000000` surface measured:

| Measurement | Value |
|---|---:|
| Odd seed count | `499999` |
| Total source states | `1741404` |
| Composite source states | `1392978` |
| Maximum value seen | `18997161173` |
| Source witness hit rate | `0.17430354248236513` |
| Same-gap background witness hit rate | `0.09882741025533583` |
| Source versus same-gap witness ratio | `1.7637165846198448` |
| Prime endpoint hit rate | `0.2000833809960239` |

The same-gap witness ratio by transition `v2` stratum is:

| `v2(3n+1)` stratum | Source composite count | Same-gap background composite count | Ratio |
|---|---:|---:|---:|
| `1` | `696237` | `7978539` | `1.9275212321500066` |
| `2` | `348242` | `3998463` | `1.5582563147270216` |
| `3-4` | `261136` | `2990912` | `1.6324415254370295` |
| `>=5` | `87363` | `997687` | `1.659162945066948` |

The same-gap enrichment increased from the `200000` gate run, where the overall
ratio was `1.698705042224337`.

## Reset Profile

Blocks are classified as `witness_contact` when at least one composite source
state is at odd-projected PGS witness distance `0`.

| Block class | Block count | Median reset strength | P90 reset strength | Median steps | P90 steps | Final-source witness rate |
|---|---:|---:|---:|---:|---:|---:|
| `witness_contact` | `161206` | `2.078632113914513` | `10.666610934626316` | `4.0` | `16.0` | `0.43563515005644954` |
| `no_witness_contact` | `338793` | `1.8728822607686915` | `10.666656987717413` | `1.0` | `4.0` | `0.0` |

Witness-contact blocks have higher median reset strength and longer first-
descent blocks. The upper reset tail is mixed: `no_witness_contact` has the
larger maximum reset strength, while `witness_contact` has the larger P99 reset
strength.

## Artifact Surface

- Probe: `benchmarks/python/predictor/collatz_pgs_same_gap_scale_probe.py`
- Contract test: `tests/python/predictor/test_collatz_pgs_same_gap_scale_probe.py`
- Summary: `output/collatz_pgs_same_gap_scale_probe/summary.json`
- Block rows: `output/collatz_pgs_same_gap_scale_probe/block_rows.jsonl`
- V2 rows: `output/collatz_pgs_same_gap_scale_probe/v2_rows.jsonl`

`block_rows.jsonl` contains `499999` rows and is `272M` locally.

## Next Concrete Question

Separate the reset-profile effect from block-length. Compare witness-contact
and no-witness-contact blocks within matched odd-step strata.
