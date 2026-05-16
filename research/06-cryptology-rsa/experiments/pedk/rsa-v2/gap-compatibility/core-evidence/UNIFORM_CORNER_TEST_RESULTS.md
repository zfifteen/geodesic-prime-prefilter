# Uniform Corner Test Results

## Status

This is measured sidecar evidence for the PEDK gap-compatibility hypothesis.

It tests a stronger abstraction suggested by the all-`o6` work: whether the
five refined public phase states reject every fully uniform factor-neighborhood
corner, not only the all-`o6` corner.

## Object

The tested public-state families are:

```text
five_state_survivor_family:
  o2_d4_odd|d<=4@late
  o4_d4_odd|d<=4@early
  o4_d4_odd|d<=4@late
  o4_d4_odd|d<=4@mid
  o6_d4_odd|d<=4@late

even_mid_exception_family:
  o4_d4_even|d<=4@mid
```

The tested factor-neighborhood predicate is:

```text
fully uniform = all four factor-side gap residues are identical
```

This includes:

```text
all-o2
all-o4
all-o6
```

## Experiment

Script:

```text
uniform_corner_test.py
```

Output:

```text
output/uniform_corner_test/
```

Fresh bands:

```text
3001..3500
3501..4000
```

## Measured Result

The broad missing-uniform-corner hypothesis is false:

```text
five_state_forward_row_count = 1410
five_state_uniform_observation_count = 95
five_state_uniform_corner_status = falsified_uniform_observation_present
```

The exception class also admits uniform signatures:

```text
exception_forward_row_count = 140
exception_uniform_observation_count = 11
exception_uniform_corner_status = exception_supported_uniform_observation_present
```

Uniform observations by group:

```text
five_state_survivor_family:
  all-o2 = 34
  all-o4 = 59
  all-o6 = 2

even_mid_exception_family:
  all-o2 = 7
  all-o4 = 4
  all-o6 = 0
```

## Consequence

The broad diversity-law form is invalidated:

```text
False: the five refined public phase states reject every fully uniform factor
neighborhood.
```

The five-state all-`o6` rule is also invalidated:

```text
False: all-o6 is excluded from all five refined public phase states.
```

The falsifying public phase state is:

```text
o4_d4_odd|d<=4@mid
```

Falsifying rows:

```text
case_id = small_semiprime_3001_3331
N = 9996331
p = 3001
q = 3331

case_id = small_semiprime_3301_3331
N = 10995631
p = 3301
q = 3331
```

Both rows have:

```text
S(N) = o4_d4_odd|d<=4@mid
F(p,q) = all-o6 factor-neighborhood signature
```

## Refined Candidate

The surviving all-`o6` exclusion surface is now four public phase states:

```text
o2_d4_odd|d<=4@late
o4_d4_odd|d<=4@early
o4_d4_odd|d<=4@late
o6_d4_odd|d<=4@late
```

In the two tested bands above `3000`, those four states had no all-`o6`
observations.

## Interpretation

The missing corner is not full uniformity. All-`o2` and all-`o4` occur many
times in the five-state family.

The sharper pattern is specific to the all-`o6` corner, and even that corner is
not excluded from every odd public state. The mid-phase `o4` state is now an
exception in both parity forms:

```text
o4_d4_even|d<=4@mid
o4_d4_odd|d<=4@mid
```

The candidate theorem target narrows again:

```text
some non-mid public phase states exclude the all-o6 factor-neighborhood corner.
```

## Machine-Readable Artifacts

```text
output/uniform_corner_test/summary.json
output/uniform_corner_test/group_band_summary_rows.jsonl
output/uniform_corner_test/uniform_observation_rows.jsonl
```

## Boundary

This is measured sidecar evidence. It invalidates an overbroad candidate rule
and sharpens the search target. It does not prove a theorem and does not make
PEDK inference live.
