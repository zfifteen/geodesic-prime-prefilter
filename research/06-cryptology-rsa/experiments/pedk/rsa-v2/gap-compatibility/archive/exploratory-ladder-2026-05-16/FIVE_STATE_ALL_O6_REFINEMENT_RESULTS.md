# Five-State All-O6 Refinement Results

## Status

This is the current strongest measured sidecar candidate rule for the PEDK
gap-compatibility hypothesis.

It is not a theorem. It is not a live PEDK inference rule. It is a refined
exclusion candidate derived after the exact six-state all-`o6` rule was
falsified in the fourth fresh band.

## Rule Object

The public object is:

```text
S(N) = reduced_state(gap(N)) @ phase(N inside gap(N))
```

The downstream factor-neighborhood object is:

```text
F(p,q) = unordered factor-neighborhood signature
```

The refined candidate rule is:

```text
For five public phase states, exclude the all-o6 factor-neighborhood signature.
```

Excluded signature:

```text
L=o6_higher_divisor_odd|d<=4|R=o6_higher_divisor_odd|d<=4
||
L=o6_higher_divisor_odd|d<=4|R=o6_higher_divisor_odd|d<=4
```

Five public phase states:

```text
o2_d4_odd|d<=4@late
o4_d4_odd|d<=4@early
o4_d4_odd|d<=4@late
o4_d4_odd|d<=4@mid
o6_d4_odd|d<=4@late
```

Removed public phase state:

```text
o4_d4_even|d<=4@mid
```

That state was removed because it produced the fourth-band falsification:

```text
small_semiprime_1823_1861
```

## Experiment

Script:

```text
five_state_all_o6_refinement_check.py
```

Inputs:

```text
output/symbolic_rule_forward_check/candidate_rule_rows.jsonl
output/all_o6_candidate_rule_check/summary.json
```

Output:

```text
output/five_state_all_o6_refinement_check/
```

Fresh test band:

```text
min_factor = 2201
max_factor = 2600
max_factor_ratio = 4/1
semiprime_triple_count = 1275
```

Falsification criterion:

```text
A row falsifies this candidate if S(N) is one of the five surviving public
phase states and F(p,q) is the all-o6 factor-neighborhood signature.
```

## Measured Result

The five-state refinement survived the fifth fresh band:

```text
tested_forward_row_count = 502
falsifying_forward_row_count = 0
candidate_status = survived_fresh_band
```

State support:

```text
o2_d4_odd|d<=4@late   support = 66,  falsifications = 0
o4_d4_odd|d<=4@early  support = 88,  falsifications = 0
o4_d4_odd|d<=4@late   support = 68,  falsifications = 0
o4_d4_odd|d<=4@mid    support = 224, falsifications = 0
o6_d4_odd|d<=4@late   support = 56,  falsifications = 0
```

The same refinement also survived the next fresh band:

```text
min_factor = 2601
max_factor = 3000
semiprime_triple_count = 1326
tested_forward_row_count = 517
falsifying_forward_row_count = 0
candidate_status = survived_fresh_band
```

## Evidence Chain

The rule-derivation path is:

```text
40 held-out-stable exclusions
27 forward-stable exclusions
14 state-local public-width-quantile survivors
6 all-o6 symbolic states
5 all-o6 refined states
```

Measured pressure:

```text
six-state all-o6 rule:
  survived factors 1401..1800
  falsified once in factors 1801..2200

five-state all-o6 refinement:
  survived factors 2201..2600
  survived factors 2601..3000
```

## Interpretation

The evidence supports the existence of compatibility and incompatibility
structure between the public composite gap state and factor-neighborhood gap
signatures.

The all-`o6` exclusion is not universal across the original six public phase
states. The even `o4` mid-phase state is compatible at least once with an
all-`o6` factor neighborhood. Removing that state produces a narrower rule
candidate that survives the next fresh band.

The current strongest candidate is:

```text
five-state all-o6 factor-neighborhood exclusion
```

## Machine-Readable Artifacts

```text
output/five_state_all_o6_refinement_check/summary.json
output/five_state_all_o6_refinement_check/candidate_rule_rows.jsonl
output/five_state_all_o6_refinement_check/falsification_rows.jsonl
output/five_state_all_o6_refinement_check/state_support_rows.jsonl
output/five_state_all_o6_refinement_check_2601_3000/summary.json
output/five_state_all_o6_refinement_check_2601_3000/candidate_rule_rows.jsonl
output/five_state_all_o6_refinement_check_2601_3000/falsification_rows.jsonl
output/five_state_all_o6_refinement_check_2601_3000/state_support_rows.jsonl
```

## Boundary

This is measured sidecar evidence. It does not locate `p` or `q`, does not
prove a theorem, and does not make the rule live PEDK inference.

The unresolved target is a mechanism: why these five public phase states
exclude the all-`o6` factor-neighborhood signature while
`o4_d4_even|d<=4@mid` does not.
