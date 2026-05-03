# Collatz-PGS Reset Length-Strata Probe

## Strongest Measured Result

Inside exact odd-step strata, witness-contact blocks retain a matched-weighted
mean of stratum median reset-strength advantage, but the sign is not uniform
across strata.

The probe used the `1000000` same-gap scale block rows:

```text
output/collatz_pgs_same_gap_scale_probe/block_rows.jsonl
```

It compared `witness_contact` and `no_witness_contact` blocks only within the
same value of `odd_steps_to_first_descent`.

## Matched-Strata Result

| Measurement | Value |
|---|---:|
| Exact odd-step strata | `103` |
| Strata containing both block classes | `37` |
| Matched witness-contact blocks | `159195` |
| Matched no-witness-contact blocks | `338793` |
| Matched weight total | `117677` |
| Strata where witness-contact median reset is higher | `19` |
| Strata where no-witness-contact median reset is higher | `18` |
| Matched-weighted mean of stratum median reset delta | `0.7056366384084134` |
| Matched-weighted mean of stratum median reset ratio | `1.6163417109769` |
| Matched-weighted mean of stratum P90 reset delta | `-0.028322861082362694` |

The median reset-strength separation survives exact odd-step matching in the
matched-weighted mean of stratum medians. The stratum signs are nearly
balanced, and the P90 aggregate does not show the same positive separation.

## Interpretation

The prior overall reset profile combined two effects:

- witness-contact blocks are longer on average;
- inside matched odd-step strata, high-weight low-step strata still favor
  witness-contact median reset strength.

The reset effect is therefore not only a block-length composition artifact, but
it is not a uniform step-by-step dominance law. The next useful question is
which exact step strata carry the effect and whether those strata have a common
PGS or modular structure.

## Artifact Surface

- Probe: `benchmarks/python/predictor/collatz_pgs_reset_length_strata_probe.py`
- Contract test: `tests/python/predictor/test_collatz_pgs_reset_length_strata_probe.py`
- Summary: `output/collatz_pgs_reset_length_strata_probe/summary.json`
- Strata rows: `output/collatz_pgs_reset_length_strata_probe/strata_rows.jsonl`

## Next Concrete Question

Split the matched reset profile by exact odd-step strata and transition
composition. The direct target is to identify whether the high-weight favorable
strata share a stable `v2` composition or PGS position pattern.
