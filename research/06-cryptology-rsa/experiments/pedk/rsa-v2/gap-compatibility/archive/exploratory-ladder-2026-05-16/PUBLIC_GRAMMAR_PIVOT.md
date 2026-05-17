# Public Grammar Pivot

## Status

This is measured sidecar evidence for the PEDK gap-compatibility hypothesis.

It is the first compact pivot over the supported public grammar words in the
multiplication map.

## Object

Each public grammar word records:

```text
previous reduced gap state
containing exact type of gap(N)
phase of N inside gap(N)
GWR-relative distance distribution
following reduced gap state
```

Each row attaches the observed factor-neighborhood grammar on the compatible
side and the number of missing supported factor words on the incompatible side.

## Experiment

Script:

```text
public_grammar_pivot.py
```

Input:

```text
output/multiplication_map_law_surface_601_5500/
```

Output:

```text
output/public_grammar_pivot_601_5500/
```

## Measured Result

```text
pivot_public_word_count = 23
supported_factor_word_count = 198
candidate_exclusion_count = 3741
```

## Highest-Pressure Public Words

```text
public word:
  prev=o6_d4_odd|d<=4
  containing=o4_d4_a4_d4_odd@mid
  next=o4_d4_odd|d<=4

support = 69
observed_factor_word_count = 67
candidate_exclusions_covered = 174
all_o6_row_count = 0
uniform_factor_row_count = 0
top distances = 0:32, 6:10, 12:6, 2:4
```

```text
public word:
  prev=o2_d4_odd|d<=4
  containing=o2_d4_a2_d4_odd@early
  next=o6_d4_odd|d<=4

support = 52
observed_factor_word_count = 50
candidate_exclusions_covered = 173
all_o6_row_count = 0
uniform_factor_row_count = 3
top distances = 0:41, 4:5, 10:2, 12:2, 6:2
```

```text
public word:
  prev=o2_d4_odd|d<=4
  containing=o4_d4_a4_d4_odd@mid
  next=o6_d4_odd|d<=4

support = 54
observed_factor_word_count = 51
candidate_exclusions_covered = 173
all_o6_row_count = 0
uniform_factor_row_count = 3
top distances = 0:14, 2:12, 6:7, 8:5, 12:4
```

## Interpretation

The supported public words are not equal. Some public grammar words carry a
large exclusion load while still admitting many positive factor words.

That means the law is not simply:

```text
public word excludes almost everything
```

It is:

```text
public word selects compatible factor grammar classes and excludes others
```

The next compression must therefore group the missing factor words by their
factor-side grammar: residue multiset and winner-phase multiset.

## Machine-Readable Artifacts

```text
output/public_grammar_pivot_601_5500/summary.json
output/public_grammar_pivot_601_5500/public_grammar_pivot_rows.jsonl
```

## Boundary

This is measured sidecar evidence. It is not a theorem, not live PEDK
inference, and not a factor resolver.
