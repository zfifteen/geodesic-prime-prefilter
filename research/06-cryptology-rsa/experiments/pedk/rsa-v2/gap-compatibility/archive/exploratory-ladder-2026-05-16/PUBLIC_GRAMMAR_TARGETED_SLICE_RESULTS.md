# Public Grammar Targeted Slice Results

## Status

This is measured sidecar evidence for the PEDK gap-compatibility hypothesis.

It tests the top five public-grammar factor-class exclusions from the compressed
multiplication map on fresh factor bands.

## Object

Each candidate has the form:

```text
public grammar word -> excluded factor residue/phase class
```

The public grammar word records:

```text
previous reduced state
containing exact type @ phase of N
following reduced state
```

The factor class records:

```text
factor residue multiset
factor winner-phase multiset
```

## Experiment

Script:

```text
public_grammar_targeted_slice_check.py
```

Selected candidates:

```text
top 5 rows from:
output/public_grammar_factor_exclusion_pivot_601_5500/candidate_class_exclusion_rows.jsonl
```

Fresh bands:

```text
5501..6500
6501..7500
```

Combined output:

```text
output/public_grammar_targeted_slice_check_5501_7500/
```

## Combined Result

```text
candidate_count = 5
fresh_semiprime_count = 12564
survived_fresh_public_slice = 2
falsified_fresh_public_slice = 3
falsification_row_count = 8
```

## Surviving Candidates

### Rank 2

```text
public:
  prev = o4_higher_divisor_even|5<=d<=16
  containing = o2_d4_a2_d4_odd@mid
  next = o2_d4_odd|d<=4

excluded factor class:
  residue = o2:1|o4:2|o6:1
  phase = mid:3|late:1

fresh_public_slice_row_count = 23
fresh_falsification_row_count = 0
fresh_observed_factor_class_count = 19
```

### Rank 4

```text
public:
  prev = o2_d4_odd|d<=4
  containing = o2_d4_a2_d4_odd@early
  next = o4_d4_odd|d<=4

excluded factor class:
  residue = o2:1|o4:1|o6:2
  phase = mid:3|late:1

fresh_public_slice_row_count = 42
fresh_falsification_row_count = 0
fresh_observed_factor_class_count = 29
```

## Falsified Candidates

### Rank 1

```text
public:
  prev = o2_d4_odd|d<=4
  containing = o2_d4_a2_d4_odd@early
  next = o4_d4_odd|d<=4

excluded factor class:
  residue = o2:1|o4:2|o6:1
  phase = mid:3|late:1

fresh_public_slice_row_count = 42
fresh_falsification_row_count = 4
```

### Rank 3

```text
public:
  prev = o2_d4_odd|d<=4
  containing = o2_d4_a2_d4_odd@mid
  next = o6_d4_odd|d<=4

excluded factor class:
  residue = o2:2|o4:1|o6:1
  phase = mid:3|late:1

fresh_public_slice_row_count = 67
fresh_falsification_row_count = 1
```

### Rank 5

```text
public:
  prev = o4_d4_odd|d<=4
  containing = o2_d4_a2_d4_odd@early
  next = o2_d4_odd|d<=4

excluded factor class:
  residue = o2:1|o4:1|o6:2
  phase = mid:3|late:1

fresh_public_slice_row_count = 50
fresh_falsification_row_count = 3
```

## Interpretation

The targeted slice check confirms that compression was productive. It also
shows that high training support is not enough. Three of the top five
compressed exclusions falsified immediately in fresh public slices.

The surviving signal is narrower:

```text
specific public grammar word -> specific mixed-residue phase class
```

The repeated factor phase class remains:

```text
mid:3|late:1
```

but it is not excluded uniformly. Neighbor context and residue multiset both
matter.

## Next Testable Predicate

The next forward candidates are:

```text
Rank 2:
prev=o4_higher_divisor_even|5<=d<=16
containing=o2_d4_a2_d4_odd@mid
next=o2_d4_odd|d<=4
excludes residue o2:1|o4:2|o6:1 with phase mid:3|late:1

Rank 4:
prev=o2_d4_odd|d<=4
containing=o2_d4_a2_d4_odd@early
next=o4_d4_odd|d<=4
excludes residue o2:1|o4:1|o6:2 with phase mid:3|late:1
```

A direct falsification is:

```text
a fresh row in the matching public slice whose factor-neighborhood class
equals the excluded residue/phase class.
```

## Machine-Readable Artifacts

```text
output/public_grammar_targeted_slice_check_5501_6500/summary.json
output/public_grammar_targeted_slice_check_5501_6500/targeted_result_rows.jsonl
output/public_grammar_targeted_slice_check_5501_6500/falsification_rows.jsonl

output/public_grammar_targeted_slice_check_6501_7500/summary.json
output/public_grammar_targeted_slice_check_6501_7500/targeted_result_rows.jsonl
output/public_grammar_targeted_slice_check_6501_7500/falsification_rows.jsonl

output/public_grammar_targeted_slice_check_5501_7500/summary.json
output/public_grammar_targeted_slice_check_5501_7500/targeted_result_rows.jsonl
output/public_grammar_targeted_slice_check_5501_7500/falsification_rows.jsonl
```

## Boundary

This is measured sidecar evidence. It is not a theorem, not live PEDK
inference, and not a factor resolver. It is a fresh targeted falsification
check for candidate grammar exclusions.
