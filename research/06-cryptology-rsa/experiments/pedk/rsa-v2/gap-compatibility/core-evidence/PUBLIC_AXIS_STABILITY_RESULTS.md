# Public Axis Stability Results

## Status

This is a measured sidecar result for the PEDK gap compatibility hypothesis.

It is not a theorem. It is not a live PEDK inference rule. It tests whether the
`27` forward-stable phase exclusions remain stable when the fresh forward corpus
is partitioned by a public PGS object of `gap(N)`.

## Experiment

Script:

```text
public_axis_stability_check.py
```

Input survivor surface:

```text
output/forward_stable_survivor_prediction/stable_pair_forward_rows.jsonl
```

Output directory:

```text
output/public_axis_stability_check/
```

The check uses the `27` pairs that survived the fresh-band forward test:

```text
S(N) = reduced_state(gap(N)) @ phase(N inside gap(N))
F(p, q) = excluded factor-neighborhood signature
```

It partitions the same fresh forward corpus by the public width of the gap
containing `N`:

```text
width_006_016
width_018_032
width_034_048
width_050_plus
```

The public axis is:

```text
n_containing_gap_width
```

## Measured Result

The forward-stable exclusions remained stable across the tested public
gap-width cells.

```text
fresh_band = factors 601..1000
semiprime_triple_count = 1711
forward_survivor_count = 27
public_width_bucket_count = 4
pair_width_cell_count = 108
tested_pair_width_cell_count = 104
untested_pair_width_cell_count = 4
fully_width_covered_pair_count = 23
falsified_pair_width_cell_count = 0
falsifying_forward_row_count = 0
```

The four untested cells all come from `o4_d4_odd|d<=4@early` in the smallest
public width bucket:

```text
width_006_016
```

That means the phase state had no forward rows in that public width bucket. The
remaining `104` survivor-by-width cells were tested and none were falsified.

## Public Width Support

The fresh forward corpus had public gap-width support:

| public width bucket | forward rows |
|---|---:|
| `width_006_016` | 463 |
| `width_018_032` | 789 |
| `width_034_048` | 332 |
| `width_050_plus` | 127 |

The survivor surface is therefore not confined to one width regime. It remains
visible across small, middle, large, and very large public gap widths wherever
the corresponding public phase state appears.

## Interpretation

The public-axis check answers the next objection after the fresh-band forward
test.

The `27` forward-stable exclusions are not merely stable in the aggregate fresh
band. They remain stable after the forward corpus is split by a public PGS
object of `gap(N)`.

The result is stronger than the forward aggregate count because it shows that
the survivor surface is not being carried by one public gap-width region.

## Machine-Readable Artifacts

```text
output/public_axis_stability_check/summary.json
output/public_axis_stability_check/pair_width_stability_rows.jsonl
output/public_axis_stability_check/public_width_bucket_rows.jsonl
output/public_axis_stability_check/falsification_rows.jsonl
```

The falsification file is empty in this run because no tested public width cell
falsified a forward-stable exclusion.

## Boundary

The public axis is computed from `N` and the public gap containing `N`.
Factor-neighborhood signatures remain downstream audit labels used only to
measure whether a candidate exclusion is falsified.

The measured consequence is:

```text
27 forward-stable phase exclusions survive 104 tested public gap-width cells.
```

The unresolved target is to test the same `27` survivor surface against
state-local public width quantiles and then against another fresh factor band.
