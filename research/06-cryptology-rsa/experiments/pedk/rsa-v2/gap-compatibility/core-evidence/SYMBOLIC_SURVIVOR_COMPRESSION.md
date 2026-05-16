# Symbolic Survivor Compression

## Status

This is a measured sidecar compression of the current PEDK gap-compatibility
survivor surface.

It is not a theorem. It is not a live PEDK inference rule. It summarizes the
symbolic grammar shared by the `14` candidates that survived:

```text
held-out splits
fresh factor band 601..1000
public gap-width split
fresh factor band 1001..1400
state-local public width quantiles
```

## Experiment

Script:

```text
symbolic_survivor_compression.py
```

Input:

```text
output/public_width_quantile_stability_check/stable_quantile_survivor_rows.jsonl
```

Output:

```text
output/symbolic_survivor_compression/
```

## Measured Compression

The current `14`-survivor surface is `o6`-heavy.

```text
survivor_count = 14
minimum_o6_residue_count = 2
all_survivors_have_at_least_two_o6_residues = true
has_all_o6_factor_neighborhood_count = 10
both_factor_neighborhoods_touch_o6_count = 13
all_right_residues_o6_count = 11
all_o6_signature_count = 6
```

Every surviving excluded factor-neighborhood signature contains at least two
`o6` residues across the four factor-side gap positions.

The strongest repeated signature is the all-`o6` factor-neighborhood:

```text
L=o6_higher_divisor_odd|d<=4|R=o6_higher_divisor_odd|d<=4
||
L=o6_higher_divisor_odd|d<=4|R=o6_higher_divisor_odd|d<=4
```

This all-`o6` signature survives for six public phase states:

```text
o2_d4_odd|d<=4@late
o4_d4_even|d<=4@mid
o4_d4_odd|d<=4@early
o4_d4_odd|d<=4@late
o4_d4_odd|d<=4@mid
o6_d4_odd|d<=4@late
```

## Residue Multiset Distribution

| factor residue multiset | survivor count |
|---|---:|
| `o6,o6,o6,o6` | 6 |
| `o2,o2,o6,o6` | 2 |
| `o2,o4,o6,o6` | 2 |
| `o2,o6,o6,o6` | 2 |
| `o4,o4,o6,o6` | 1 |
| `o4,o6,o6,o6` | 1 |

No survivor has fewer than two `o6` factor residues.

## Candidate Rule Family

The current measured candidate family is:

```text
For the surviving public phase states, factor-neighborhood signatures with
strong o6 concentration are candidate-incompatible.
```

The narrowest high-support symbolic subfamily is:

```text
all-o6 factor-neighborhood signature excluded across six public phase states
```

The broader symbolic envelope is:

```text
at least two o6 residues in the four factor-side gap positions
```

The broader envelope is descriptive, not yet an exclusion rule. It contains all
current survivors but has not been tested as a complete rule against all
possible signatures.

## Machine-Readable Artifacts

```text
output/symbolic_survivor_compression/summary.json
output/symbolic_survivor_compression/symbolic_survivor_rows.jsonl
output/symbolic_survivor_compression/signature_phase_count_rows.jsonl
output/symbolic_survivor_compression/multiset_phase_count_rows.jsonl
```

## Boundary

This compression operates on downstream factor-neighborhood labels. It
identifies a candidate symbolic grammar for incompatibility, not a live PEDK
inference rule.

The measured consequence is:

```text
the strongest surviving incompatibility surface concentrates around o6-heavy
factor-neighborhood signatures.
```

The unresolved target is to test whether the all-`o6` subfamily and the broader
two-or-more-`o6` envelope survive as explicit symbolic rules on another fresh
band.
