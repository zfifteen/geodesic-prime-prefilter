# All-O6 Boundary Refinement, 601..5500

## Status

This is measured sidecar evidence for the PEDK gap-compatibility hypothesis.

The prior candidate rule was:

```text
Within the six target states, all-o6 is excluded from o2/o4 non-mid public states.
```

That rule is now invalidated.

The fresh falsifier is:

```text
case_id = small_semiprime_4583_4801
band = 4501_5000
N = 22002983
p = 4583
q = 4801
S(N) = o4_d4_odd|d<=4@late
exact_type = o4_d4_a10_d4_odd
factor_neighborhood_signature = all-o6
```

The broader hypothesis is strengthened, not weakened. The falsifier did not
erase the compatibility structure. It moved the boundary inward from a coarse
phase rule to a sharper public-state rule.

## Object

The downstream compatibility label is:

```text
F(p,q) = all-o6 factor-neighborhood signature
```

The public object is:

```text
S(N) = reduced_state(gap(N)) @ phase(N inside gap(N))
```

The tested public states are:

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

Fresh output directories:

```text
output/public_feature_all_o6_boundary_4501_5000/
output/public_feature_all_o6_boundary_5001_5500/
output/public_feature_all_o6_boundary_601_5500/
```

The cumulative output covers:

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
4501..5000
5001..5500
```

## Measured Result

Across factors `601..5500`:

```text
all_o6_compatible_state_count = 4
all_o6_not_observed_state_count = 2
all_o6_observation_count = 6
```

All-`o6` compatible states:

```text
o4_d4_even|d<=4@mid
o4_d4_odd|d<=4@late
o4_d4_odd|d<=4@mid
o6_d4_odd|d<=4@late
```

All-`o6` not-observed states:

```text
o2_d4_odd|d<=4@late
o4_d4_odd|d<=4@early
```

## Public Feature Table

```text
state                     rows  all-o6  status       median_pos  median_width  median_winner_offset
o2_d4_odd@late            894   0       not observed 812         30            2
o4_d4_even@mid            753   1       compatible   500         28            3
o4_d4_odd@early           1005  0       not observed 166         30            4
o4_d4_odd@late            784   1       compatible   823         30            4
o4_d4_odd@mid             3233  3       compatible   500         24            4
o6_d4_odd@late            653   1       compatible   791         24            6
```

## All-O6 Observation Rows

```text
small_semiprime_1823_1861
band = 1801_2200
S(N) = o4_d4_even|d<=4@mid
exact_type = o4_d4_a3_d4_even
width = 54
offsets = left 40, right 14
position_mpermille = 740

small_semiprime_3001_3331
band = 3001_3500
S(N) = o4_d4_odd|d<=4@mid
exact_type = o4_d4_a4_d4_odd
width = 46
offsets = left 18, right 28
position_mpermille = 391

small_semiprime_3301_3331
band = 3001_3500
S(N) = o4_d4_odd|d<=4@mid
exact_type = o4_d4_a10_d4_odd
width = 18
offsets = left 12, right 6
position_mpermille = 666

small_semiprime_4021_4261
band = 4001_4500
S(N) = o6_d4_odd|d<=4@late
exact_type = o6_d4_a4_d4_odd
width = 40
offsets = left 30, right 10
position_mpermille = 750

small_semiprime_4583_4801
band = 4501_5000
S(N) = o4_d4_odd|d<=4@late
exact_type = o4_d4_a10_d4_odd
width = 40
offsets = left 34, right 6
position_mpermille = 850

small_semiprime_5281_5303
band = 5001_5500
S(N) = o4_d4_odd|d<=4@mid
exact_type = o4_d4_a4_d4_odd
width = 10
offsets = left 4, right 6
position_mpermille = 400
```

## Interpretation

The invalidated rule was too coarse. `o4_d4_odd|d<=4@late` is compatible with
all-`o6` at exact subtype `o4_d4_a10_d4_odd`.

The surviving exclusion surface is:

```text
o2_d4_odd|d<=4@late
o4_d4_odd|d<=4@early
```

This is the current strongest measured all-`o6` exclusion surface in this
chain. It is sharper than the earlier phase-level rule because it keeps the
new compatible `o4` late subtype instead of forcing all late `o4` states into
one bucket.

The next public variable to examine is the exact subtype inside the reduced
public state, especially the `a` component in keys such as:

```text
o4_d4_a4_d4_odd
o4_d4_a10_d4_odd
```

## Next Testable Predicate

The next rule candidate is:

```text
Within the six target states, all-o6 is excluded from:
  o2_d4_odd|d<=4@late
  o4_d4_odd|d<=4@early
```

A direct falsification is:

```text
an all-o6 factor-neighborhood observation in either surviving state.
```

## Machine-Readable Artifacts

```text
output/public_feature_all_o6_boundary_4501_5000/summary.json
output/public_feature_all_o6_boundary_4501_5000/state_feature_rows.jsonl
output/public_feature_all_o6_boundary_4501_5000/all_o6_observation_rows.jsonl

output/public_feature_all_o6_boundary_5001_5500/summary.json
output/public_feature_all_o6_boundary_5001_5500/state_feature_rows.jsonl
output/public_feature_all_o6_boundary_5001_5500/all_o6_observation_rows.jsonl

output/public_feature_all_o6_boundary_601_5500/summary.json
output/public_feature_all_o6_boundary_601_5500/state_feature_rows.jsonl
output/public_feature_all_o6_boundary_601_5500/all_o6_observation_rows.jsonl
```

## Boundary

This is measured sidecar evidence. It is not a theorem, not live PEDK
inference, and not a factor resolver. The invalidated non-mid rule remains
invalidated. The surviving two-state exclusion surface is a measured candidate
for the next forward test.
