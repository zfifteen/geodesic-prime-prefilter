# Inverse Word Exclusion Finding

## Status

This is a measured grammar finding.

It is not a proof, not a resolver, and not an official RSA v2 inference rule.

## Finding

Solved semiprime target rows reuse recursive grammar pieces from the
deterministic expanded surface, but avoid the expanded surface's ordered
lag-2 + lag-3 reduced words.

Compact statement:

```text
inverse recursive grammar appears as component sharing with ordered-word
exclusion.
```

The inverse relation is not simple low/high opposition. It is not direct
matching between public `N` grammar and target-side grammar. The evidence points
to ordered recursive grammar words as the object that separates solved rows
from deterministic expansion rows.

## Reproduction Artifacts

Scripts:

```text
grammar_recursive_target_catalog.py
grammar_recursive_solved_surface_compare.py
grammar_inverse_word_exclusion_probe.py
```

Outputs:

```text
output/grammar_recursive_target_catalog/
output/grammar_recursive_solved_surface/
output/grammar_inverse_word_exclusion/
```

Primary summary:

```text
output/grammar_inverse_word_exclusion/summary.json
```

## Measured Result

Global scope:

```text
solved rows: 48
lag-2 hits: 30
lag-3 hits: 29
lag-2 + lag-3 ordered word hits: 0
full recursive reduced word hits: 0
recursive class hits: 41
component-sharing word exclusions: 40
```

Public-cell scope:

```text
solved rows: 48
lag-2 hits: 14
lag-3 hits: 11
lag-2 + lag-3 ordered word hits: 0
full recursive reduced word hits: 0
recursive class hits: 24
component-sharing word exclusions: 22
```

Public-cell plus target-side scope:

```text
solved rows: 48
lag-2 hits: 10
lag-3 hits: 5
lag-2 + lag-3 ordered word hits: 0
full recursive reduced word hits: 0
recursive class hits: 17
component-sharing word exclusions: 15
```

Fresh RSA-100 challenge target scope:

```text
solved target rows: 2
global lag-2 hits: 2
global lag-3 hits: 1
global lag-2 + lag-3 ordered word hits: 0
global full recursive reduced word hits: 0
global recursive class hits: 2
global component-sharing word exclusions: 2

public-cell lag-2 hits: 2
public-cell lag-3 hits: 1
public-cell lag-2 + lag-3 ordered word hits: 0
public-cell full recursive reduced word hits: 0
public-cell recursive class hits: 2
public-cell component-sharing word exclusions: 2

public-cell plus target-side lag-2 hits: 1
public-cell plus target-side lag-3 hits: 1
public-cell plus target-side lag-2 + lag-3 ordered word hits: 0
public-cell plus target-side full recursive reduced word hits: 0
public-cell plus target-side recursive class hits: 2
public-cell plus target-side component-sharing word exclusions: 2
```

Fresh output artifacts:

```text
output/fresh_grammar_compatibility/
output/fresh_rsa_challenge_recursive_surface/
output/fresh_rsa_challenge_inverse_word_exclusion/
```

## Interpretation

The solved rows share components and coarse recursive classes with the expanded
surface. They do not share the expanded surface's ordered reduced words.

The grammar object that matters is therefore not an isolated chamber, a single
lag layer, or a low/high class. The current evidence points to the ordered
combined lag-2 + lag-3 reduced grammar word.

## Boundary

Allowed role:

```text
grammar evidence for deriving future PGS compatibility or exclusion rules
```

Forbidden role:

```text
resolver
factor selector
product closure substitute
divisibility shortcut
audit inference
```

## Next Experiment

Use combined lag-2 + lag-3 reduced words as exclusion-family labels, then test
fresh solved rows for component sharing without ordered-word collision.

Decision rule for the next evidence pass:

```text
When a candidate target row shares lag-2 or lag-3 recursive pieces with an
excluded family but also repeats that family's combined lag-2 + lag-3 reduced
word, mark it grammar-incompatible for that family.
```

This rule is a hypothesis for testing. It is not yet a proved PGS law.
