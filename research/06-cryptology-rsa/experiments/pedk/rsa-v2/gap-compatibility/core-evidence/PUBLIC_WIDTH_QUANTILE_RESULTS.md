# Public Width Quantile Results

## Status

This is a measured sidecar result for the PEDK gap compatibility hypothesis.

It is not a theorem. It is not a live PEDK inference rule. It tests whether the
`27` forward-stable exclusions survive a fresh higher band when that band is
split by state-local public gap-width quantiles.

## Experiment

Script:

```text
public_width_quantile_stability_check.py
```

Input survivor surface:

```text
output/forward_stable_survivor_prediction/stable_pair_forward_rows.jsonl
```

Output directory:

```text
output/public_width_quantile_stability_check/
```

The check uses the `27` exclusions that survived the first fresh forward band
over factors `601..1000`.

It tests those exclusions on a second fresh factor band:

```text
min_factor = 1001
max_factor = 1400
max_factor_ratio = 4/1
```

Within each public phase state, the public widths of the gap containing `N` are
split into four deterministic state-local width quantiles:

```text
q1_low_width
q2_midlow_width
q3_midhigh_width
q4_high_width
```

## Measured Result

The second fresh band reduced the candidate surface again.

```text
semiprime_triple_count = 1431
forward_survivor_count = 27
tested_pair_quantile_cell_count = 108
untested_pair_quantile_cell_count = 0
falsified_pair_count = 13
falsified_pair_quantile_cell_count = 21
falsifying_forward_row_count = 29
stable_quantile_survivor_count = 14
```

All `27` candidates were fully tested across four state-local public width
quantiles. The fresh higher band falsified `13` candidates and left `14`
standing.

## Interpretation

This is a strong pruning result.

The sequence so far is:

```text
raw phased candidate exclusions: 64
held-out stable exclusions: 40
fresh 601..1000 forward survivors: 27
fresh 1001..1400 state-local width-quantile survivors: 14
```

The candidate rule surface is getting smaller under stricter tests instead of
expanding. That is the desired direction for deriving real compatibility and
incompatibility rules.

## Falsification Pattern

The `13` falsified candidates were not confined to one quantile:

| state-local width quantile | falsified cells |
|---|---:|
| `q4_high_width` | 8 |
| `q2_midlow_width` | 6 |
| `q1_low_width` | 4 |
| `q3_midhigh_width` | 3 |

The high-width quantile produced the most falsified cells, but every quantile
participated. The surviving `14` are therefore a sharper candidate surface than
the aggregate `27`.

## Machine-Readable Artifacts

```text
output/public_width_quantile_stability_check/summary.json
output/public_width_quantile_stability_check/stable_quantile_survivor_rows.jsonl
output/public_width_quantile_stability_check/pair_quantile_stability_rows.jsonl
output/public_width_quantile_stability_check/falsification_rows.jsonl
output/public_width_quantile_stability_check/state_width_threshold_rows.jsonl
output/public_width_quantile_stability_check/state_quantile_support_rows.jsonl
```

The file `stable_quantile_survivor_rows.jsonl` is the current strongest
candidate rule surface.

## Boundary

The public width quantiles are validation partitions over a measured research
corpus. They are not live PEDK inference rules.

Factor-neighborhood signatures remain downstream audit labels. The public side
of the test is the phase state of `gap(N)` and the public width of `gap(N)`.

The measured consequence is:

```text
14 phase-state exclusions survived a second fresh factor band and four
state-local public width quantiles.
```

The unresolved target is to test whether those `14` candidates survive another
fresh band and whether they collapse into a smaller symbolic grammar rule.
