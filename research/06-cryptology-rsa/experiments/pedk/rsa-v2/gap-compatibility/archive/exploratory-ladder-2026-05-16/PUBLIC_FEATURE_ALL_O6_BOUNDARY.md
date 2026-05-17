# Public Feature All-O6 Boundary

## Status

This is measured sidecar evidence for the PEDK gap-compatibility hypothesis.

It compares public gap features for the states that have admitted the all-`o6`
factor-neighborhood signature against the states where all-`o6` has not yet
been observed.

## Object

The downstream compatibility label is:

```text
F(p,q) = all-o6 factor-neighborhood signature
```

The public object is:

```text
S(N) = reduced_state(gap(N)) @ phase(N inside gap(N))
```

The six target public states are:

```text
o2_d4_odd|d<=4@late
o4_d4_even|d<=4@mid
o4_d4_odd|d<=4@early
o4_d4_odd|d<=4@late
o4_d4_odd|d<=4@mid
o6_d4_odd|d<=4@late
```

## Experiment

Script:

```text
public_feature_all_o6_boundary.py
```

Output:

```text
output/public_feature_all_o6_boundary/
```

Bands:

```text
601..1000
1001..1400
1401..1800
1801..2200
2201..2600
2601..3000
3001..3500
3501..4000
4001..4500
```

## Measured Result

Across the six target states:

```text
all_o6_compatible_state_count = 3
all_o6_not_observed_state_count = 3
all_o6_observation_count = 4
```

All-`o6` compatible states:

```text
o4_d4_even|d<=4@mid
o4_d4_odd|d<=4@mid
o6_d4_odd|d<=4@late
```

All-`o6` not observed states:

```text
o2_d4_odd|d<=4@late
o4_d4_odd|d<=4@early
o4_d4_odd|d<=4@late
```

## Public Feature Table

```text
state                     status       rows  all-o6  median_pos  median_width  median_winner_offset
o2_d4_odd@late            not observed 730   0       814         30            2
o4_d4_even@mid            compatible   600   1       500         28            3
o4_d4_odd@early           not observed 792   0       166         30            4
o4_d4_odd@late            not observed 635   0       823         30            4
o4_d4_odd@mid             compatible   2642  2       500         24            4
o6_d4_odd@late            compatible   536   1       790         24            6
```

The state-level split is:

```text
compatible:
  mid-phase o4 states
  o6 first-open late state

not observed:
  o2/o4 non-mid states
```

## All-O6 Observation Rows

```text
small_semiprime_1823_1861
S(N) = o4_d4_even|d<=4@mid
exact_type = o4_d4_a3_d4_even

small_semiprime_3001_3331
S(N) = o4_d4_odd|d<=4@mid
exact_type = o4_d4_a4_d4_odd

small_semiprime_3301_3331
S(N) = o4_d4_odd|d<=4@mid
exact_type = o4_d4_a10_d4_odd

small_semiprime_4021_4261
S(N) = o6_d4_odd|d<=4@late
exact_type = o6_d4_a4_d4_odd
```

## Interpretation

The observed boundary is not parity alone:

```text
o4_d4_even|d<=4@mid and o4_d4_odd|d<=4@mid both admit all-o6.
```

It is not late phase alone:

```text
o2_d4_odd|d<=4@late and o4_d4_odd|d<=4@late have not admitted all-o6,
while o6_d4_odd|d<=4@late has.
```

It is not uniformity:

```text
all-o2 and all-o4 occur frequently in the target states.
```

The current public-feature boundary is:

```text
Within the six target states, all-o6 compatibility has appeared only in
mid-phase o4 states or the o6 first-open late state.
```

The surviving exclusion surface is:

```text
o2_d4_odd|d<=4@late
o4_d4_odd|d<=4@early
o4_d4_odd|d<=4@late
```

## Next Testable Predicate

The next rule candidate is:

```text
Within this target family, all-o6 is excluded from o2/o4 non-mid public states.
```

A direct falsification is:

```text
an all-o6 factor-neighborhood observation in:
  o2_d4_odd|d<=4@late
  o4_d4_odd|d<=4@early
  o4_d4_odd|d<=4@late
```

## Machine-Readable Artifacts

```text
output/public_feature_all_o6_boundary/summary.json
output/public_feature_all_o6_boundary/state_feature_rows.jsonl
output/public_feature_all_o6_boundary/state_band_support_rows.jsonl
output/public_feature_all_o6_boundary/all_o6_observation_rows.jsonl
```

## Boundary

This is measured sidecar evidence. The compatible and not-observed classes are
defined using downstream labels from known triples. The public features are
public, but the rule is not proved and is not live PEDK inference.
