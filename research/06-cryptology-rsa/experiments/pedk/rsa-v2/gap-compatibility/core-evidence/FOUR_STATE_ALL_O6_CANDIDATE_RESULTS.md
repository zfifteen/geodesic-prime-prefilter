# Four-State All-O6 Candidate Results

## Status

This is measured sidecar evidence for the PEDK gap-compatibility hypothesis.

It tests the four-state all-`o6` candidate produced after the uniform-corner
test invalidated the five-state all-`o6` rule.

## Object

Candidate public phase states:

```text
o2_d4_odd|d<=4@late
o4_d4_odd|d<=4@early
o4_d4_odd|d<=4@late
o6_d4_odd|d<=4@late
```

Removed state:

```text
o4_d4_odd|d<=4@mid
```

Falsification criterion:

```text
A row falsifies this candidate if S(N) is one of the four public phase states
and F(p,q) is the all-o6 factor-neighborhood signature.
```

## Experiment

Script:

```text
four_state_all_o6_candidate_check.py
```

Output:

```text
output/four_state_all_o6_candidate_check/
```

Fresh band:

```text
4001..4500
```

## Measured Result

The four-state candidate is falsified:

```text
semiprime_triple_count = 1770
tested_forward_row_count = 317
falsifying_forward_row_count = 1
candidate_status = falsified_in_fresh_band
```

Falsified public phase state:

```text
o6_d4_odd|d<=4@late
```

Falsifying row:

```text
case_id = small_semiprime_4021_4261
N = 17133481
p = 4021
q = 4261
S(N) = o6_d4_odd|d<=4@late
F(p,q) = all-o6 factor-neighborhood signature
```

State support:

```text
o2_d4_odd|d<=4@late   support = 85, falsifications = 0
o4_d4_odd|d<=4@early  support = 84, falsifications = 0
o4_d4_odd|d<=4@late   support = 86, falsifications = 0
o6_d4_odd|d<=4@late   support = 62, falsifications = 1
```

## Refined Candidate

The surviving all-`o6` exclusion surface is now three public phase states:

```text
o2_d4_odd|d<=4@late
o4_d4_odd|d<=4@early
o4_d4_odd|d<=4@late
```

## Interpretation

The all-`o6` corner is not excluded by all late states and not excluded by all
odd states. The `o6` late state eventually admits the all-`o6` factor
neighborhood.

The current surviving surface is more specific:

```text
o2 late and o4 non-mid phase states
```

That is now the next candidate boundary to pressure.

## Machine-Readable Artifacts

```text
output/four_state_all_o6_candidate_check/summary.json
output/four_state_all_o6_candidate_check/candidate_rule_rows.jsonl
output/four_state_all_o6_candidate_check/falsification_rows.jsonl
output/four_state_all_o6_candidate_check/state_support_rows.jsonl
```

## Boundary

This is measured sidecar evidence. It invalidates another overbroad candidate
and sharpens the public-state boundary. It does not prove a theorem and does
not make PEDK inference live.
