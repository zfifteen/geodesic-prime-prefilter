# Held-Out Phase Exclusion Results

## Status

This is a measured sidecar result for the PEDK gap compatibility hypothesis.

It is not a theorem. It is not a live PEDK inference rule. It tests whether
candidate phase-state exclusions learned from lower factor bands survive in
deterministic held-out upper factor bands.

## Experiment

Script:

```text
heldout_phase_exclusion_check.py
```

Input corpus:

```text
output/gap_compatibility_search/corpus_rows.jsonl
```

Output directory:

```text
output/heldout_phase_exclusion_check/
```

The check uses the existing public phase state:

```text
S(N) = reduced_state(gap(N)) @ phase(N inside gap(N))
```

and the existing downstream factor-neighborhood label:

```text
F(p, q) = unordered factor-neighborhood signature
```

For each deterministic split, the training band is:

```text
q <= q_ceiling
```

and the held-out band is:

```text
q > q_ceiling
```

The `q` value is used only to partition the known corpus for sidecar
validation. It is not public live inference.

## Deterministic Splits

The first held-out check used:

```text
q_ceiling in {360, 400, 420, 450, 480, 500}
min_support = 50
```

For each split, the script:

1. learns candidate exclusions from the training band;
2. tests those exclusions against the held-out band;
3. records every exclusion falsified by at least one held-out row;
4. records every exclusion that survives that split.

## Measured Result

The held-out check produced stable surviving exclusions.

```text
stable_survivor_count = 40
total_surviving_exclusion_rows = 266
total_falsified_exclusion_rows = 207
```

A stable survivor is a candidate exclusion that:

- was trained in all six deterministic splits;
- was not observed in any corresponding held-out band.

The result is positive evidence for the multiplication-map hypothesis because
some absences are not artifacts of a single full-corpus count. They persist
under repeated lower-band to upper-band tests.

## Split Table

| q ceiling | train rows | held-out rows | train exclusions | falsified exclusions | surviving exclusions |
|---:|---:|---:|---:|---:|---:|
| 360 | 1598 | 2236 | 98 | 58 | 40 |
| 400 | 1899 | 1935 | 79 | 39 | 40 |
| 420 | 2058 | 1776 | 76 | 36 | 40 |
| 450 | 2389 | 1445 | 66 | 26 | 40 |
| 480 | 2684 | 1150 | 78 | 25 | 53 |
| 500 | 2873 | 961 | 76 | 23 | 53 |

The early splits are stricter because the training band is smaller and the
held-out band is larger. The repeated `40` survivors across the first four
splits gives the first stable held-out exclusion surface.

## Stable Survivor Distribution

The `40` exclusions that survived all six splits are distributed across public
phase states as:

| public phase state | stable survivor count |
|---|---:|
| `o2_d4_odd|d<=4@late` | 9 |
| `o4_d4_odd|d<=4@early` | 7 |
| `o4_d4_odd|d<=4@late` | 6 |
| `o4_d4_even|d<=4@mid` | 5 |
| `o6_d4_even|d<=4@mid` | 4 |
| `o6_d4_odd|d<=4@late` | 4 |
| `o2_d4_odd|d<=4@early` | 2 |
| `o6_d4_odd|d<=4@mid` | 2 |
| `o4_d4_odd|d<=4@mid` | 1 |

Late public phase states and even public phase states remain the strongest
source of stable exclusions. That matches the first full-corpus signal.

## Falsification Result

The check also falsified many candidate exclusions.

This is useful. It separates full-corpus absences that fail under scale-forward
testing from absences that persist under held-out testing.

The preliminary full-corpus exclusion rule must therefore remain sidecar-only.
The stable survivor set is the next candidate surface, not a promoted rule.

## Machine-Readable Artifacts

```text
output/heldout_phase_exclusion_check/summary.json
output/heldout_phase_exclusion_check/split_summary_rows.jsonl
output/heldout_phase_exclusion_check/stable_survivor_rows.jsonl
output/heldout_phase_exclusion_check/surviving_exclusion_rows.jsonl
output/heldout_phase_exclusion_check/falsified_exclusion_rows.jsonl
```

## Boundary

This experiment uses known `(N, p, q)` triples to label and partition a research
corpus. It does not identify factors, does not close factor pairs, and does not
create a live PEDK inference rule.

The measured consequence is:

```text
phase-state gap compatibility has held-out survivor structure.
```

The unresolved target is to determine which stable survivor families preserve
under larger exact corpora and which reduce to finite-regime artifacts.
