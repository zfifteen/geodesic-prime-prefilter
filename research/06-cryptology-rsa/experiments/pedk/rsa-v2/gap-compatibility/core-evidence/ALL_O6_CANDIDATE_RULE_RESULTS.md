# All-O6 Candidate Rule Results

## Status

This is a measured sidecar rule-derivation result for the PEDK
gap-compatibility hypothesis.

It is not a theorem. It is not a live PEDK inference rule. It tests the compact
all-`o6` incompatibility candidate on a fourth fresh factor band.

## Object

The public object is the typed gap containing the composite `N`. Its state is
recorded as:

```text
S(N) = reduced_state(gap(N)) @ phase(N inside gap(N))
```

The downstream factor-neighborhood object is the unordered pair of typed gaps
touching `p` and `q`:

```text
F(p,q) = unordered factor-neighborhood signature
```

The candidate rule tested here is:

```text
For six public phase states, exclude the all-o6 factor-neighborhood signature.
```

Excluded signature:

```text
L=o6_higher_divisor_odd|d<=4|R=o6_higher_divisor_odd|d<=4
||
L=o6_higher_divisor_odd|d<=4|R=o6_higher_divisor_odd|d<=4
```

Six public phase states from the prior symbolic rule check:

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
all_o6_candidate_rule_check.py
```

Input:

```text
output/symbolic_rule_forward_check/candidate_rule_rows.jsonl
```

Output:

```text
output/all_o6_candidate_rule_check/
```

Fresh test band:

```text
min_factor = 1801
max_factor = 2200
max_factor_ratio = 4/1
semiprime_triple_count = 1176
```

Falsification criterion:

```text
A row falsifies the candidate if S(N) is one of the six public phase states
and F(p,q) is the all-o6 factor-neighborhood signature.
```

## Measured Result

The exact six-state rule was falsified once:

```text
tested_forward_row_count = 486
falsifying_forward_row_count = 1
candidate_status = falsified_in_fresh_band
```

Falsifying row:

```text
case_id = small_semiprime_1823_1861
N = 3392603
p = 1823
q = 1861
S(N) = o4_d4_even|d<=4@mid
F(p,q) = all-o6 factor-neighborhood signature
```

State-level result:

```text
survived_public_phase_state_count = 5
falsified_public_phase_state_count = 1
falsified_public_phase_states = o4_d4_even|d<=4@mid
```

The surviving five-state refinement is:

```text
o2_d4_odd|d<=4@late
o4_d4_odd|d<=4@early
o4_d4_odd|d<=4@late
o4_d4_odd|d<=4@mid
o6_d4_odd|d<=4@late
```

## Interpretation

The all-`o6` signal remains strong, but the six-state rule is too broad.

The fourth fresh band gives a sharper candidate:

```text
all-o6 factor-neighborhood exclusion for five public phase states
```

The invalidated part is concrete:

```text
o4_d4_even|d<=4@mid cannot remain in the all-o6 exclusion rule.
```

The current live sidecar state is therefore:

```text
six-state all-o6 rule: invalidated
five-state all-o6 refinement: candidate survivor, not yet promoted
```

## Machine-Readable Artifacts

```text
output/all_o6_candidate_rule_check/summary.json
output/all_o6_candidate_rule_check/candidate_rule_rows.jsonl
output/all_o6_candidate_rule_check/falsification_rows.jsonl
output/all_o6_candidate_rule_check/state_support_rows.jsonl
```

## Boundary

This result strengthens the multiplication-map hypothesis while narrowing the
rule boundary.

The evidence supports correlation between public composite gap state and
factor-neighborhood gap signature. It does not prove a theorem, does not locate
`p` or `q`, and does not make the rule live PEDK inference.

The next unresolved target is to test the five-state all-`o6` refinement on a
fresh band.
