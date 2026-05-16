# Public Grammar Factor Exclusion Pivot

## Status

This is measured sidecar evidence for the PEDK gap-compatibility hypothesis.

It compresses the `3741` absent cells from the multiplication map by grouping
factor words into residue multisets and winner-phase multisets under each
supported public grammar word.

## Object

The public side is:

```text
previous reduced state
containing exact type @ N phase
following reduced state
```

The factor side is compressed to:

```text
factor residue multiset
factor winner-phase multiset
```

Example factor classes:

```text
residue = o2:1|o4:2|o6:1
phase = mid:3|late:1
```

## Experiment

Script:

```text
public_grammar_factor_exclusion_pivot.py
```

Input:

```text
output/multiplication_map_law_surface_601_5500/
```

Output:

```text
output/public_grammar_factor_exclusion_pivot_601_5500/
```

## Measured Result

```text
factor_class_cell_count = 1644
candidate_class_exclusion_count = 531
supported_public_word_count = 23
```

Candidate exclusion counts by residue multiset:

```text
o2:4               89
o2:2|o6:2          48
o2:3|o6:1          48
o2:3|o4:1          43
o4:4               43
o2:1|o4:2|o6:1     39
o4:2|o6:2          36
o2:1|o4:1|o6:2     34
o2:2|o4:2          34
o4:1|o6:3          32
o2:2|o4:1|o6:1     24
o4:3|o6:1          23
o2:1|o4:3          22
o2:1|o6:3          16
```

## Highest-Support Candidate Classes

```text
public:
  prev=o2_d4_odd|d<=4
  containing=o2_d4_a2_d4_odd@early
  next=o4_d4_odd|d<=4

excluded factor class:
  residue = o2:1|o4:2|o6:1
  phase = mid:3|late:1

excluded_factor_word_count = 13
excluded_factor_support_total = 506
public_forward_row_count = 50
```

```text
public:
  prev=o4_higher_divisor_even|5<=d<=16
  containing=o2_d4_a2_d4_odd@mid
  next=o2_d4_odd|d<=4

excluded factor class:
  residue = o2:1|o4:2|o6:1
  phase = mid:3|late:1

excluded_factor_word_count = 13
excluded_factor_support_total = 506
public_forward_row_count = 52
```

```text
public:
  prev=o2_d4_odd|d<=4
  containing=o2_d4_a2_d4_odd@mid
  next=o6_d4_odd|d<=4

excluded factor class:
  residue = o2:2|o4:1|o6:1
  phase = mid:3|late:1

excluded_factor_word_count = 12
excluded_factor_support_total = 426
public_forward_row_count = 73
```

## Interpretation

The first broad-rule family is not the all-`o6` corner. The all-`o6` corner
remains important, but it is too sparse under the broad factor-word support
threshold used in the multiplication map.

The broad map's first visible rule family is:

```text
public grammar words with d4-odd local context exclude specific mixed-residue
factor classes whose winner-phase multiset is mid:3|late:1.
```

The repeated excluded phase multiset is:

```text
mid:3|late:1
```

That phase pattern appears in the top excluded classes across multiple public
grammar words. The next refinement should test whether the public-side
containing type `o2_d4_a2_d4_odd@early` imposes a stable exclusion on mixed
factor classes with three mid winners and one late winner.

## Next Testable Predicate

Candidate:

```text
If containing=o2_d4_a2_d4_odd@early and the public neighbors are d4-odd,
exclude factor classes with phase multiset mid:3|late:1 in the mixed-residue
families:
  o2:1|o4:2|o6:1
  o2:1|o4:1|o6:2
  o2:2|o4:2
```

A direct falsification is:

```text
a fresh public word satisfying the public predicate whose factor-neighborhood
word lands in one of the excluded residue/phase classes.
```

## Machine-Readable Artifacts

```text
output/public_grammar_factor_exclusion_pivot_601_5500/summary.json
output/public_grammar_factor_exclusion_pivot_601_5500/factor_class_pivot_rows.jsonl
output/public_grammar_factor_exclusion_pivot_601_5500/candidate_class_exclusion_rows.jsonl
```

## Boundary

This is measured sidecar evidence. It is not a theorem, not live PEDK
inference, and not a factor resolver. It is a compression table for candidate
rule extraction.
