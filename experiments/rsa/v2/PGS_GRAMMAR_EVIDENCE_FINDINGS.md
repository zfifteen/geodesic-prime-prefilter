# PGS Grammar Evidence Findings

## Status

The current grammar evidence pass is complete.

This is a measured PGS grammar result. It is not a proof, not a resolver, and
not an official RSA v2 inference rule.

## Strongest Finding

Solved semiprime rows reuse recursive grammar components from the deterministic
expanded surface, but they avoid the expanded surface's ordered lag-2 plus
lag-3 reduced words.

Compact form:

```text
inverse recursive grammar appears as component sharing with ordered-word
exclusion.
```

The grammar object that survived the evidence pass is the ordered combined
lag-2 plus lag-3 reduced word:

```text
outward_lag3 | outward_lag2 | inward_lag2 | inward_lag3
```

Single lag layers are not discriminating enough. Coarse low/higher class is
not discriminating enough. Full recursive class remains useful as component
sharing evidence, but the ordered reduced word is the measured exclusion
object.

## Evidence Surface

Primary solved surface:

```text
exact low-regime solved rows: 48 target rows
comparison scopes: global, public cell, public cell plus target side
expanded comparison surface: deterministic target-cell expansion
```

Fresh held-out surface:

```text
RSA-100 target rows: 2 target rows
comparison scopes: global, public cell, public cell plus target side
expanded comparison surface: deterministic target-cell expansion
```

The RSA-100 row is large-coordinate evidence. Its public context still contains
unresolved prior carriers on two public chambers, but its factor-side chambers
are exact closed target grammar rows.

## Measured Result

Primary solved surface, global scope:

```text
solved rows: 48
lag-2 component hits: 30
lag-3 component hits: 29
lag-2 plus lag-3 ordered-word hits: 0
full recursive reduced-word hits: 0
recursive class hits: 41
component-sharing word exclusions: 40
```

Primary solved surface, public-cell scope:

```text
solved rows: 48
lag-2 component hits: 14
lag-3 component hits: 11
lag-2 plus lag-3 ordered-word hits: 0
full recursive reduced-word hits: 0
recursive class hits: 24
component-sharing word exclusions: 22
```

Primary solved surface, public-cell plus target-side scope:

```text
solved rows: 48
lag-2 component hits: 10
lag-3 component hits: 5
lag-2 plus lag-3 ordered-word hits: 0
full recursive reduced-word hits: 0
recursive class hits: 17
component-sharing word exclusions: 15
```

Fresh RSA-100 surface, global scope:

```text
solved target rows: 2
lag-2 component hits: 2
lag-3 component hits: 1
lag-2 plus lag-3 ordered-word hits: 0
full recursive reduced-word hits: 0
recursive class hits: 2
component-sharing word exclusions: 2
```

Fresh RSA-100 surface, public-cell scope:

```text
solved target rows: 2
lag-2 component hits: 2
lag-3 component hits: 1
lag-2 plus lag-3 ordered-word hits: 0
full recursive reduced-word hits: 0
recursive class hits: 2
component-sharing word exclusions: 2
```

Fresh RSA-100 surface, public-cell plus target-side scope:

```text
solved target rows: 2
lag-2 component hits: 1
lag-3 component hits: 1
lag-2 plus lag-3 ordered-word hits: 0
full recursive reduced-word hits: 0
recursive class hits: 2
component-sharing word exclusions: 2
```

## Reproduction

From `experiments/rsa/v2`:

```bash
python3 grammar_compatibility_catalog.py --output-dir output/fresh_grammar_compatibility
python3 grammar_recursive_solved_surface_compare.py --compatibility-rows output/fresh_grammar_compatibility/compatibility_rows.jsonl --target-rows output/rsa_challenge_exact_grammar/target_grammar_rows.jsonl --expanded-recursive-rows output/grammar_recursive_target_catalog/recursive_target_rows.jsonl --solved-surface rsa_challenge --output-dir output/fresh_rsa_challenge_recursive_surface
python3 grammar_inverse_word_exclusion_probe.py --solved-recursive-rows output/fresh_rsa_challenge_recursive_surface/recursive_target_rows.jsonl --expanded-recursive-rows output/grammar_recursive_target_catalog/recursive_target_rows.jsonl --output-dir output/fresh_rsa_challenge_inverse_word_exclusion
```

Primary artifacts:

```text
output/grammar_inverse_word_exclusion/summary.json
output/fresh_rsa_challenge_inverse_word_exclusion/summary.json
output/fresh_rsa_challenge_recursive_surface/summary.json
output/fresh_grammar_compatibility/summary.json
```

## Interpretation

The inverse relation is not direct matching between public `N` grammar and
factor-side grammar. It is also not a simple low/high opposition.

The measured structure is:

```text
shared recursive components
+ excluded ordered reduced word
```

That gives the next PGS-native object to study:

```text
an exclusion family labeled by the combined lag-2 plus lag-3 reduced word
```

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

Known `p` and `q` values are downstream labels only. They identify where to
measure target-side grammar on solved surfaces. They do not enter public
inference.

## Next Work

The next valid grammar task is no longer to test fresh solved rows. That test
has been run and reproduced.

The next valid grammar task is to connect this exclusion word to the public
certificate side:

```text
PGSPG certificate
-> ordered commitment story
-> reciprocal transport
-> recursive lag-2 / lag-3 grammar projection
-> exclusion, survivor, or unresolved
```

This bridge is specified in `PGSMD_NEXT_EXPERIMENTS.md` as
`commitment_story_word_projection_v1`.

