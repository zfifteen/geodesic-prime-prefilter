# Symbolic Rule Forward Results

## Status

This is a measured sidecar rule-derivation result for the PEDK
gap-compatibility hypothesis.

It is not a theorem. It is not a live PEDK inference rule. It tests symbolic
candidate rule families derived from the `14` survivor surface.

## Experiment

Script:

```text
symbolic_rule_forward_check.py
```

Input:

```text
output/symbolic_survivor_compression/symbolic_survivor_rows.jsonl
```

Output:

```text
output/symbolic_rule_forward_check/
```

Fresh test band:

```text
min_factor = 1401
max_factor = 1800
max_factor_ratio = 4/1
semiprime_triple_count = 1540
```

## Candidate Rules Tested

### Narrow All-`o6` Rule

Candidate rule:

```text
For the six surviving public phase states, exclude the all-o6
factor-neighborhood signature.
```

Excluded signature:

```text
L=o6_higher_divisor_odd|d<=4|R=o6_higher_divisor_odd|d<=4
||
L=o6_higher_divisor_odd|d<=4|R=o6_higher_divisor_odd|d<=4
```

Public phase states:

```text
o2_d4_odd|d<=4@late
o4_d4_even|d<=4@mid
o4_d4_odd|d<=4@early
o4_d4_odd|d<=4@late
o4_d4_odd|d<=4@mid
o6_d4_odd|d<=4@late
```

Falsification criterion:

```text
A row falsifies this candidate if S(N) is one of the six public phase states
and F(p,q) is the all-o6 factor-neighborhood signature.
```

Measured result:

```text
tested_forward_row_count = 652
falsifying_forward_row_count = 0
candidate_status = survived_fresh_band
```

### Broad Two-`o6` Envelope

Candidate envelope:

```text
For the current survivor phase states, exclude any factor-neighborhood
signature with at least two o6 residues.
```

Measured result:

```text
tested_forward_row_count = 851
falsifying_forward_row_count = 143
candidate_status = falsified_in_fresh_band
```

This broad envelope is invalidated as a rule candidate.

## Measured Result

The symbolic forward check produced:

```text
candidate_rule_count = 2
survived_candidate_rule_count = 1
falsified_candidate_rule_count = 1
narrow_all_o6_falsifying_row_count = 0
broad_two_o6_falsifying_row_count = 143
```

The first compact symbolic rule candidate is therefore:

```text
all-o6 factor-neighborhood exclusion for six public phase states
```

## Interpretation

The work has moved from a list of candidate exclusions to a compact symbolic
rule candidate.

The broad observation that the survivor surface is `o6`-heavy is real, but the
rule "exclude all signatures with at least two `o6` residues" is too broad. The
narrow all-`o6` signature exclusion survived a third fresh factor band and now
has the strongest measured support.

## Machine-Readable Artifacts

```text
output/symbolic_rule_forward_check/summary.json
output/symbolic_rule_forward_check/candidate_rule_rows.jsonl
output/symbolic_rule_forward_check/falsification_rows.jsonl
output/symbolic_rule_forward_check/state_support_rows.jsonl
```

## Boundary

The symbolic rule is still sidecar-only. It is derived from downstream
factor-neighborhood labels and must not be used as live PEDK inference until it
survives larger fresh bands and its public application boundary is formalized.

The measured consequence is:

```text
the all-o6 factor-neighborhood exclusion survived 652 tested rows across six
public phase states in a third fresh band, while the broader two-o6 envelope was
falsified 143 times.
```

The unresolved target is to test the narrow all-`o6` rule on another fresh band
and then formalize it as a candidate exclusion rule with exact public input and
downstream-label boundary.
