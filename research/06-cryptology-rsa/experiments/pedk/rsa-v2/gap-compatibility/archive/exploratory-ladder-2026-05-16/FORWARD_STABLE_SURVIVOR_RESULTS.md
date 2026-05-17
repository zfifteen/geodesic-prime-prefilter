# Forward Stable Survivor Results

## Status

This is a measured sidecar result for the PEDK gap compatibility hypothesis.

It is not a theorem. It is not a live PEDK inference rule. It tests whether the
`40` stable held-out survivors preserve on a fresh higher factor band generated
from the same exact PGS endpoint construction.

## Experiment

Script:

```text
forward_stable_survivor_prediction.py
```

Input survivor surface:

```text
output/heldout_phase_exclusion_check/stable_survivor_rows.jsonl
```

Output directory:

```text
output/forward_stable_survivor_prediction/
```

The original compatibility corpus used factors through:

```text
max_factor = 600
```

The forward corpus uses the fresh higher factor band:

```text
min_factor = 601
max_factor = 1000
max_factor_ratio = 4/1
```

This creates a non-overlapping forward factor band while preserving the same
deterministic endpoint construction.

## Measured Result

The forward check produced a sharper survivor surface.

```text
semiprime_triple_count = 1711
stable_survivor_count = 40
tested_pair_count = 40
untested_pair_count = 0
survived_pair_count = 27
falsified_pair_count = 13
falsifying_forward_row_count = 18
```

Every stable survivor pair was tested because every relevant public phase state
appeared in the forward band.

The forward band falsified `13` of the `40` held-out survivors. The remaining
`27` survived the fresh-band test.

## Interpretation

The result strengthens the research program by removing false stability.

The earlier held-out check showed that `40` exclusions survived six
deterministic lower-band to upper-band splits. Grok correctly noted that those
splits are nested and therefore not independent. The fresh-band forward test
answers that critique directly:

- some held-out survivors were finite-band artifacts;
- some survivor structure persists beyond the original factor range;
- the next candidate surface is the `27` forward survivors, not the full `40`.

## Falsification Distribution

Forward falsifications were sparse relative to public phase support. The
falsified pairs had absence rates between:

```text
974 / 1000 and 995 / 1000
```

That means each falsified pair remained rare in the forward band, but one valid
forward observation is enough to remove it from the candidate exclusion set.

The falsification rows are stored in:

```text
output/forward_stable_survivor_prediction/falsification_rows.jsonl
```

## Survivor Distribution

The `27` forward survivors are distributed as:

| public phase state | forward survivor count |
|---|---:|
| `o2_d4_odd|d<=4@late` | 8 |
| `o4_d4_even|d<=4@mid` | 4 |
| `o4_d4_odd|d<=4@early` | 4 |
| `o4_d4_odd|d<=4@late` | 4 |
| `o6_d4_odd|d<=4@late` | 3 |
| `o6_d4_even|d<=4@mid` | 2 |
| `o2_d4_odd|d<=4@early` | 1 |
| `o4_d4_odd|d<=4@mid` | 1 |

Late public phase states remain the strongest source of forward-stable
exclusions.

## Machine-Readable Artifacts

```text
output/forward_stable_survivor_prediction/summary.json
output/forward_stable_survivor_prediction/stable_pair_forward_rows.jsonl
output/forward_stable_survivor_prediction/falsification_rows.jsonl
output/forward_stable_survivor_prediction/forward_phase_state_rows.jsonl
```

## Boundary

The forward corpus still uses known `(N, p, q)` triples to label
factor-neighborhood signatures for sidecar validation. The public phase state
`S(N)` is computed from `N`, but the factor-neighborhood signature `F(p, q)` is
an audit label.

The measured consequence is:

```text
27 phase-state exclusions survive a fresh non-overlapping higher factor band.
```

The unresolved target is to determine whether those `27` survivors preserve
under another fresh band and under public-axis splits such as public gap width,
public phase support, or other PGS-visible structure.
