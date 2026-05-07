# Grammar Evidence Status

## Purpose

This note records the active gap/chamber grammar evidence surface for known
`N,p,q` rows.

The goal is evidence gathering:

```text
known public N
-> public N neighboring chamber grammar
-> downstream known p/q neighboring chamber grammar labels
-> grammar correlation catalog
-> future PGS elimination experiments
```

The goal is not to resolve the decomposer from this artifact.

## Evidence Contract

Allowed fields:

```text
case_id
bits
N neighboring chamber reduced states
N neighboring chamber exact type keys when closed
p left/right chamber reduced states
p left/right chamber exact type keys when closed
q left/right chamber reduced states
q left/right chamber exact type keys when closed
orientation labels: p outward, p inward, q inward, q outward
explicit unresolved chamber state
explicit unresolved offsets
```

Forbidden inference fields:

```text
gcd
N % x
product closure
factor APIs
primality APIs as decomposer inference
random search
audit labels as public inference
```

Known factors in solved rows are downstream labels only. They identify where to
measure factor-side grammar. They do not enter public inference.

## Exact Low-Regime Catalog

Artifact:

```text
experiments/rsa/v2/output/grammar_evidence/exact_low_regime_grammar_rows.jsonl
```

Summary:

```text
case_count: 24
bit_range: 47..60
public N-containing higher-divisor rows: 0
target-side rows: 48
target-side higher-divisor rows: 10
outward higher-divisor rows: 8
inward higher-divisor rows: 2
outward fraction among higher-divisor target rows: 0.8
outward intrusion index: 4.0
```

Strongest measured finding on this surface:

```text
Every measured N-containing chamber is in d<=4 grammar, while higher-divisor
grammar appears on the factor-side rows and is outward-biased by 8 to 2.
```

This is measured evidence, not a theorem.

## RSA-100 Challenge Surface

Artifact:

```text
experiments/rsa/v2/output/rsa_challenge_exact_grammar/
```

Summary:

```text
case_id: rsa_100
bits: 330
public rows: 3
target rows: 4
public exact-closed rows: 1
public unresolved prior-carrier rows: 2
target exact-closed rows: 4
```

Exact-closed factor-side grammar:

```text
p_left:  o2_d4_a6_d4_odd
p_right: o2_d4_a35_d4_even
q_left:  o2_d4_a2_d4_odd
q_right: o2_d4_a8_d4_odd
```

Public N grammar rows:

```text
n_previous:   exact_closed, o4_d4_a34_d4_odd
n_containing: unresolved_prior_carrier, candidate o4_d4_a194_d4_odd
n_following:  unresolved_prior_carrier, candidate o4_d4_a44_d4_odd
```

The unresolved public rows are still evidence. They record the current
candidate grammar and the exact prior offsets that must be eliminated by
GWR/NLSC before the candidate becomes resolved public grammar.

Unresolved reason:

```text
requires_gwr_nlsc_prior_carrier_elimination
```

Open prior offsets:

```text
n_containing: 12, 18, 52, 78, 84, 102, 118, 174
n_following: 30
```

## Current Data Shape

The current catalog gives two useful layers:

```text
complete low-regime exact grammar
large-coordinate RSA-100 factor-side exact grammar
large-coordinate RSA-100 public grammar with explicit unresolved prior carriers
```

## Compatibility Catalog

Artifact:

```text
experiments/rsa/v2/output/grammar_compatibility/
```

Rows:

```text
compatibility_rows.jsonl
observed_compatibility_rows.jsonl
measured_absence_rows.jsonl
summary.json
```

Summary:

```text
case_count: 25
exact_low_regime rows: 24
rsa_challenge rows: 1
public unresolved context rows: 1
N context count: 24
observed compatibility rows: 100
measured absence rows: 644
outward higher-divisor rows: 8
inward higher-divisor rows: 2
outward fraction among higher-divisor target rows: 0.8
```

The compatibility rows normalize the evidence into this shape:

```text
N previous grammar
N containing grammar
N following grammar
p outward grammar
p inward grammar
q inward grammar
q outward grammar
```

The observed compatibility rows record measured co-occurrences between a public
`N` grammar context and an oriented factor-side grammar state.

The measured absence rows record states not seen for one measured public
context. These rows are not incompatibility proofs. They are review targets for
future PGS rules.

The next evidence task is to expand this catalog and derive PGS compatibility
or incompatibility rules from the measured co-occurrence and absence surfaces.

## Targeted Cell Expansion

Artifact:

```text
experiments/rsa/v2/output/grammar_cell_expansion/
```

Rows:

```text
expanded_compatibility_rows.jsonl
cell_summary_rows.jsonl
summary.json
```

Expansion method:

```text
fixed PGS prime ranges
fixed prime-pair offsets
deterministic semiprime labels
target public grammar cells
```

The expansion filled every selected target cell:

```text
target cells: 7
target rows per cell: 10
generated rows: 70
candidate rows examined: 297
underfilled cells: 0
```

Generated rows by bit size:

```text
40-bit: 16
47-bit: 19
54-bit: 19
60-bit: 16
```

The expansion surface changes the orientation balance:

```text
outward higher-divisor rows: 29
inward higher-divisor rows: 38
outward fraction: 0.43283582089552236
```

This does not erase the original solved-label pattern. It separates two
surfaces:

```text
solved-label compatibility surface: outward higher-divisor biased
target-cell deterministic expansion: inward/outward mixed
```

The next pattern pass should compare those two surfaces instead of merging them
without labels.

## Hidden Coordinate Split Scan

Artifact:

```text
experiments/rsa/v2/output/grammar_hidden_coordinate_scan/
```

Rows:

```text
split_group_rows.jsonl
feature_summary_rows.jsonl
summary.json
```

Measured result:

```text
source rows: 70
coarse cell groups: 7
coarse cell groups with both outward and inward higher-divisor grammar: 7
```

Exact public `N` grammar fields do not fully split the mixed cells. The
generated prime-pair separation coordinate changes the balance, but it also
leaves both-direction repeated groups.

Current strongest data-shape finding:

```text
The three public N chambers are not granular enough to determine factor-side
higher-divisor orientation on the expanded surface.
```

The next grammar object should be recursive oriented target grammar, not a
coarser public-cell count.

## Recursive Target-Side Grammar Catalog

Artifact:

```text
experiments/rsa/v2/output/grammar_recursive_target_catalog/
```

Rows:

```text
recursive_target_rows.jsonl
recursive_split_rows.jsonl
feature_summary_rows.jsonl
summary.json
```

Measured result:

```text
target-side recursive rows: 140

target direction classes:
  none:         82
  inward_only: 29
  outward_only:20
  both:         9

lag-2 class repeated groups:
  pure:  9
  mixed: 23

lag-2 reduced repeated groups:
  pure:  18
  mixed: 6

lag-2 reduced + lag-3 reduced repeated groups:
  pure:  16
  mixed: 0
```

The recursive pass confirms that lag-2 reduced grammar is a sharper object than
the public three-chamber cell or lag-2 low/higher class alone. Extending the
same reduced grammar view to lag-3 closes the remaining repeated-group
ambiguity on this expanded surface.

## Next Experiment Target

Apply the same recursive lag-3 target-side grammar measurement to the original
solved-label compatibility surface.

For each known downstream label, record:

```text
case_id
target_side
orientation
lag_minus_2 grammar
lag_minus_1 grammar
anchor grammar
lag_plus_1 grammar
lag_plus_2 grammar
public N previous / containing / following grammar
prime_pair_offset
prime_pair_offset_group
```

Purpose:

```text
Compare whether the original outward-biased rows share recursive reduced
signatures with the expanded rows, or whether the solved-label surface occupies
a distinct recursive grammar family.
```

This remains a grammar-evidence instrument. It must not use factorization,
`gcd`, divisibility by `N`, product closure, random search, or audit labels as
public inference.

## Solved-Surface Recursive Comparison

Artifact:

```text
experiments/rsa/v2/output/grammar_recursive_solved_surface/
```

Rows:

```text
recursive_target_rows.jsonl
recursive_split_rows.jsonl
feature_summary_rows.jsonl
signature_comparison_rows.jsonl
summary.json
```

Measured result:

```text
solved target-side recursive rows: 48
expanded target-side recursive rows: 140

solved target direction classes:
  none:         38
  outward_only: 8
  inward_only: 2

lag-2 reduced signature overlap:
  solved:   36
  expanded: 45
  overlap:  19

lag-3 reduced signature overlap:
  solved:   35
  expanded: 44
  overlap:  18

lag-2 + lag-3 reduced signature overlap:
  solved:   48
  expanded: 81
  overlap:   0

full recursive reduced signature overlap:
  solved:   48
  expanded: 82
  overlap:   0
```

Strongest current evidence statement:

```text
The original solved-label surface and the deterministic target-cell expansion
share coarse recursive grammar, but separate completely at combined lag-2 +
lag-3 reduced grammar on the measured rows.
```

Next Experiment Target:

```text
Use solved lag-2 + lag-3 reduced grammar signatures as family labels and test
fresh solved rows against those families before deriving exclusion rules.
```

## Inverse Word Exclusion Probe

Artifact:

```text
experiments/rsa/v2/output/grammar_inverse_word_exclusion/
```

Rows:

```text
inverse_word_rows.jsonl
direction_summary_rows.jsonl
summary.json
```

Measured result:

```text
global scope:
  solved rows: 48
  lag-2 hits: 30
  lag-3 hits: 29
  lag-2 + lag-3 word hits: 0
  full recursive reduced word hits: 0
  component-sharing word exclusions: 40

public-cell scope:
  solved rows: 48
  lag-2 hits: 14
  lag-3 hits: 11
  lag-2 + lag-3 word hits: 0
  full recursive reduced word hits: 0
  component-sharing word exclusions: 22

public-cell plus target-side scope:
  solved rows: 48
  lag-2 hits: 10
  lag-3 hits: 5
  lag-2 + lag-3 word hits: 0
  full recursive reduced word hits: 0
  component-sharing word exclusions: 15
```

Strongest current evidence statement:

```text
The inverse relation appears as component sharing with ordered-word exclusion.
Solved rows reuse recursive pieces from the expanded surface, but avoid the
expanded surface's ordered lag-2 + lag-3 reduced words.
```

Next Experiment Target:

```text
Use combined lag-2 + lag-3 reduced words as exclusion-family labels, then test
fresh solved rows for component sharing without ordered-word collision.
```
