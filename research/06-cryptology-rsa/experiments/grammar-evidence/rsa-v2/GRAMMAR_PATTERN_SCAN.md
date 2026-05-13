# Grammar Pattern Scan

## Surface

Input artifact:

```text
research/06-cryptology-rsa/experiments/rsa/v2/output/grammar_compatibility/compatibility_rows.jsonl
```

Measured rows:

```text
cases: 25
exact low-regime cases: 24
RSA-100 challenge cases: 1
```

Orientation convention:

```text
p_outward = p_left
p_inward  = p_right
q_inward  = q_left
q_outward = q_right
```

## Pattern 1: Public N-Containing Grammar Stays Low

Across the measured surface, the `N`-containing chamber never enters a
higher-divisor grammar state.

Observed `N`-containing states:

```text
o4_d4_odd|d<=4: 10
o2_d4_odd|d<=4: 9
o6_d4_odd|d<=4: 4
o2_d4_even|d<=4: 2
```

Observed higher-divisor `N`-containing rows:

```text
0 / 25
```

The public product chamber is therefore low-divisor grammar on this surface.

## Pattern 2: Higher-Divisor Factor Grammar Is Outward-Biased

Higher-divisor factor-side grammar appears 10 times.

By orientation:

```text
p_outward: 4
p_inward:  1
q_inward:  1
q_outward: 4
```

Grouped by direction:

```text
outward: 8
inward:  2
```

The outward fraction among higher-divisor target rows is:

```text
0.8
```

This is the strongest measured correlation in the current catalog.

## Pattern 3: Inward Higher-Divisor Grammar Is Concentrated

The only inward higher-divisor event occurs in one row:

```text
case_id: mid_50_anchor_2
N context:
  previous   = o2_higher_divisor_even|5<=d<=16
  containing = o4_d4_odd|d<=4
  following  = o4_d4_odd|d<=4

factor-side higher-divisor states:
  p_inward = o2_higher_divisor_odd|5<=d<=16
  q_inward = o2_higher_divisor_odd|5<=d<=16
```

This row is structurally different from the other higher-divisor target rows:
the public `N` previous chamber is already higher-divisor grammar.

Candidate pattern:

```text
Inward higher-divisor factor grammar appears only when public neighbor grammar
already contains a higher-divisor state on the previous side.
```

## Pattern 4: Public Neighbor Position Splits The Higher-Divisor Direction

Grouping by whether the public neighboring chambers are low or higher-divisor:

```text
N neighbors low:
  cases: 13
  outward higher: 5
  inward higher: 0

N following higher:
  cases: 8
  outward higher: 3
  inward higher: 0

N previous higher:
  cases: 4
  outward higher: 0
  inward higher: 2
```

Candidate pattern:

```text
When public higher-divisor grammar appears on the following side, factor-side
higher-divisor grammar remains outward.

When public higher-divisor grammar appears on the previous side, the only
measured inward higher-divisor event appears.
```

## Pattern 5: N-Containing First-Open Class Changes Higher-Divisor Placement

By `N`-containing state:

```text
o2_d4_even|d<=4:
  cases: 2
  outward higher: 0
  inward higher: 0

o2_d4_odd|d<=4:
  cases: 9
  outward higher: 3
  inward higher: 0

o4_d4_odd|d<=4:
  cases: 10
  outward higher: 2
  inward higher: 2

o6_d4_odd|d<=4:
  cases: 4
  outward higher: 3
  inward higher: 0
```

Candidate pattern:

```text
o6_d4_odd N-containing grammar is the most outward-active class on this
surface.

o4_d4_odd is the only N-containing class with inward higher-divisor events.
```

## Pattern 6: Repeated Public Context Does Not Force One Target Grammar

One public three-chamber context appears twice:

```text
o2_d4_odd|d<=4 | o2_d4_odd|d<=4 | o6_d4_odd|d<=4
```

Rows:

```text
mid_47_anchor_2:
  q_outward = o2_higher_divisor_even|17<=d<=64

mid_50_anchor_1:
  p_outward = o2_higher_divisor_even|17<=d<=64
```

The same public context carries the same higher-divisor family outward, but it
switches between the two outer sides.

Candidate pattern:

```text
The public three-chamber context may constrain orientation class and grammar
family without selecting which factor endpoint receives the outward event.
```

## Pattern 7: RSA-100 Matches The Low-Grammar Public Product Pattern

RSA-100 has:

```text
N previous   = o4_d4_odd|d<=4
N containing = o4_d4_odd|d<=4
N following  = o4_d4_odd|d<=4
```

Its factor-side grammar is also low-divisor:

```text
p_outward = o2_d4_odd|d<=4
p_inward  = o2_d4_even|d<=4
q_inward  = o2_d4_odd|d<=4
q_outward = o2_d4_odd|d<=4
```

RSA-100 adds a large-coordinate row consistent with the current low public
product pattern. It does not add a higher-divisor factor-side event.

## Candidate Correlations To Test Next

1. Public `N`-containing grammar remains low-divisor while factor-side grammar
   carries higher-divisor events.

2. Higher-divisor factor-side grammar is outward-biased.

3. Inward higher-divisor factor-side grammar requires a public previous-side
   higher-divisor neighbor.

4. Public following-side higher-divisor grammar is compatible with outward
   factor-side higher-divisor grammar, not inward higher-divisor grammar on the
   measured surface.

5. `o6_d4_odd` public containing grammar is strongly outward-active.

6. A public three-chamber context can constrain outward grammar family without
   deciding whether the event lands at `p_outward` or `q_outward`.

## Next Data Need

The next evidence pass should increase repeated public contexts.

The current catalog has:

```text
N context count: 24
case count: 25
```

Most public contexts occur once. To find stable compatibility patterns, the
next catalog should deliberately collect multiple examples for the same
coarse public context:

```text
N previous low/higher
N containing first-open class
N following low/higher
```

The highest-priority repeated cells are:

```text
N previous low, N containing o6_d4_odd, N following low
N previous low, N containing o4_d4_odd, N following higher
N previous higher, N containing o4_d4_odd, N following low
N previous low, N containing o2_d4_odd, N following low
```

## Grok Second-Opinion Pattern Review

Grok agreed that the strongest descriptive patterns are:

```text
N-containing grammar remains d<=4.
higher-divisor factor grammar is outward-biased at 8:2.
inward higher-divisor occurs only in the row where N-previous is higher.
N-following higher co-occurs with outward higher on the current surface.
o6_d4_odd N-containing has a 3/4 outward-higher rate.
```

Grok flagged two patterns to distrust:

```text
p_outward vs q_outward selection inside the repeated public context
RSA-100 as a general row
```

The reason is direct: the repeated public context has only two instances, and
RSA-100 has only one challenge row.

## Grok-Suggested Cross-Tabs

### N Triple Against Higher-Divisor Orientation

Rows with a higher-divisor factor-side state:

```text
o2_d4_odd | o2_d4_odd | o6_d4_odd
  cases: 2
  p_outward higher: 1
  q_outward higher: 1

o2_higher_divisor_even | o4_d4_odd | o4_d4_odd
  cases: 1
  p_inward higher: 1
  q_inward higher: 1

o4_d4_even | o2_d4_odd | o4_d4_odd
  cases: 1
  p_outward higher: 1

o4_d4_odd | o4_d4_odd | o6_higher_divisor_odd
  cases: 1
  p_outward higher: 1

o4_d4_odd | o6_d4_odd | o2_d4_odd
  cases: 1
  q_outward higher: 1

o6_d4_odd | o4_d4_odd | o2_higher_divisor_even
  cases: 1
  q_outward higher: 1

o6_d4_odd | o6_d4_odd | o2_higher_divisor_even
  cases: 1
  q_outward higher: 1

o6_d4_odd | o6_d4_odd | o6_d4_odd
  cases: 1
  p_outward higher: 1
```

### N-Previous Higher Rows

There are four rows where `N_previous` is higher-divisor grammar.

```text
mid_47_wall:
  N_previous = o6_d8_a3_higher_divisor_even
  factor-side higher states: none

mid_50_anchor_2:
  N_previous = o2_d8_a3_higher_divisor_even
  p_inward = o2_d8_a2_higher_divisor_odd
  q_inward = o2_d8_a2_higher_divisor_odd

mid_57_anchor_1:
  N_previous = o2_d64_a1_higher_divisor_even
  factor-side higher states: none

mid_57_anchor_2:
  N_previous = o2_d32_a1_higher_divisor_even
  factor-side higher states: none
```

The only inward higher-divisor row is also the only `N_previous` higher row
where the exact `N_previous` carrier has `d=8` and first-open `o2`.

Additional rows are needed in this exact cell:

```text
N_previous = o2_d8_higher_divisor_even
N_containing = o4_d4_odd
N_following = o4_d4_odd
```

## Targeted Cell Expansion Result

The grammar-cell expander filled the high-signal public cells with deterministic
PGS prime-pair labels.

Artifact:

```text
research/06-cryptology-rsa/experiments/rsa/v2/output/grammar_cell_expansion/
```

Filled cells:

```text
H|o4_d4_odd|L: 10
L|o2_d4_odd|H: 10
L|o2_d4_odd|L: 10
L|o4_d4_odd|H: 10
L|o4_d4_odd|L: 10
L|o6_d4_odd|H: 10
L|o6_d4_odd|L: 10
```

Bit spread:

```text
40-bit: 16
47-bit: 19
54-bit: 19
60-bit: 16
```

Expanded orientation counts:

```text
p_outward higher: 13
p_inward higher:  20
q_inward higher:  18
q_outward higher: 16

outward higher: 29
inward higher:  38
```

This expansion changes the first-pass reading. The outward-bias pattern is
strong on the original solved-label surface, but it does not automatically
hold on deterministic close-pair target-cell expansion.

The next pattern question is therefore sharper:

```text
Which public grammar cells preserve outward bias across surfaces, and which
cells flip or mix when the catalog is deliberately expanded?
```

Cell-level expansion counts:

```text
H|o4_d4_odd|L:
  outward higher: 5
  inward higher: 7

L|o2_d4_odd|H:
  outward higher: 5
  inward higher: 7

L|o2_d4_odd|L:
  outward higher: 3
  inward higher: 5

L|o4_d4_odd|H:
  outward higher: 5
  inward higher: 6

L|o4_d4_odd|L:
  outward higher: 4
  inward higher: 3

L|o6_d4_odd|H:
  outward higher: 4
  inward higher: 3

L|o6_d4_odd|L:
  outward higher: 3
  inward higher: 7
```

The most important correction is that the old preliminary rule
`o6_d4_odd is outward-active` is not stable on the expanded target-cell
surface. It should be downgraded to:

```text
o6_d4_odd was outward-active on the solved-label surface, but mixed on the
targeted deterministic expansion.
```

## Hidden Coordinate Split Scan

Artifact:

```text
research/06-cryptology-rsa/experiments/rsa/v2/output/grammar_hidden_coordinate_scan/
```

The hidden-coordinate scan tests whether the mixed expanded cells become
ordered when additional measured coordinates are attached.

Source rows:

```text
expanded rows: 70
coarse public cells: 7
```

Result:

```text
cell_key groups with both outward and inward higher-divisor grammar: 7 / 7
```

The coarse grammar cells are therefore too coarse. Each selected public cell
contains both outward and inward higher-divisor factor-side grammar.

Adding exact public grammar helps only partially:

```text
cell_key+n_previous_exact repeated groups:
  both_direction: 5
  inward_only:    2
  outward_only:   2

cell_key+n_following_exact repeated groups:
  both_direction: 5
  inward_only:    2
  no_higher:      1
  outward_only:   1

cell_key+n_previous_d+n_following_d repeated groups:
  both_direction: 7
  inward_only:    2
  no_higher:      2
```

Exact `N` grammar alone does not split the surface cleanly.

The generated prime-pair separation coordinate changes the orientation balance:

```text
small offsets:
  rows: 37
  outward higher: 14
  inward higher:  22

mid offsets:
  rows: 15
  outward higher: 8
  inward higher:  8

wide offsets:
  rows: 18
  outward higher: 7
  inward higher:  8
```

This is evidence that the factor-side grammar relation includes a separation
coordinate. It is not yet enough to resolve the mixed cells.

The next object to measure is recursive neighbor grammar around the oriented
factor-side chambers:

```text
p_outward lag-2 / p_outward lag-1 / p / p_inward lag+1 / p_inward lag+2
q_inward lag-2 / q_inward lag-1 / q / q_outward lag+1 / q_outward lag+2
```

The working interpretation is direct:

```text
When the visible public grammar cell is mixed, the missing state is outside the
three public N chambers. The next granular object is the recursive grammar
surrounding each oriented factor-side chamber.
```

## Recursive Target-Side Grammar Catalog

Artifact:

```text
research/06-cryptology-rsa/experiments/rsa/v2/output/grammar_recursive_target_catalog/
```

The recursive catalog measures two chambers outward and two chambers inward
from each known downstream target label in the expanded surface.

Rows:

```text
expanded source rows: 70
target-side recursive rows: 140
```

Target-local direction classes:

```text
none:         82
inward_only: 29
outward_only:20
both:         9
```

The important split is lag-2 grammar outside the immediate target-side chamber.
Class-only lag-2 grammar remains too coarse:

```text
cell_key + target_side + lag2_class_signature:
  repeated groups: 32
  pure groups:      9
  mixed groups:    23
```

Reduced lag-2 grammar is substantially sharper:

```text
cell_key + target_side + lag2_reduced_signature:
  repeated groups: 24
  pure groups:     18
  mixed groups:     6
```

This is the first strong evidence that recursive target-side grammar is the
right next object. The immediate chamber identifies the observed direction by
definition, but the lag-2 reduced grammar is outside that immediate observation
and still splits many repeated groups.

Example pure repeated lag-2 reduced groups:

```text
L|o2_d4_odd|H, p, lag2=o2_d4_odd | o4_d4_odd:
  rows: 4
  target direction: inward_only

H|o4_d4_odd|L, p, lag2=o2_d4_odd | o4_d4_odd:
  rows: 3
  target direction: inward_only

L|o4_d4_odd|L, p, lag2=o4_d4_odd | o6_d4_odd:
  rows: 2
  target direction: outward_only

L|o6_d4_odd|H, q, lag2=o2_d4_odd | o6_d4_odd:
  rows: 3
  target direction: none
```

Current pattern statement:

```text
The three public N chambers do not determine orientation on the expanded
surface. Adding recursive lag-2 reduced grammar around each oriented
factor-side target splits most repeated groups into pure direction classes.
```

Next refinement:

```text
Measure lag-3 or recursive GWR/NLSC neighbor grammar only for the six remaining
mixed repeated lag-2 reduced groups.
```

## Lag-3 Recursive Refinement

The recursive catalog now records the third chamber outward and inward from
each target-side label.

Measured split:

```text
cell_key + target_side + lag2_reduced_signature:
  repeated groups: 24
  pure groups:     18
  mixed groups:     6

cell_key + target_side + lag2_reduced_signature + lag3_reduced_signature:
  repeated groups: 16
  pure groups:     16
  mixed groups:     0
```

The six mixed lag-2 repeated groups separate when lag-3 reduced grammar is
attached. In this expanded surface, recursive reduced grammar through lag-3
eliminates the repeated-group ambiguity left by lag-2.

The six lag-2 mixed groups all split into singleton lag-3 refinements:

```text
H|o4_d4_odd|L, p, lag2=o2_d4_odd | o2_d4_odd
L|o2_d4_odd|H, q, lag2=o2_d4_odd | o6_d4_odd
L|o2_d4_odd|H, q, lag2=o4_d4_odd | o2_higher_divisor_even
L|o4_d4_odd|H, p, lag2=o4_d4_odd | o2_d4_odd
L|o4_d4_odd|H, q, lag2=o2_d4_odd | o2_d4_odd
L|o6_d4_odd|H, p, lag2=o2_d4_odd | o2_d4_odd
```

Current pattern statement:

```text
Orientation ambiguity in the expanded grammar surface is recursive. It is not
resolved by coarser public N cells, exact N chamber keys, separation class, or
lag-2 low/higher class. It is resolved on repeated groups by reduced recursive
grammar through lag-3.
```

Next evidence step:

```text
Apply the same lag-3 recursive target grammar measurement to the original
solved-label compatibility surface and compare whether the outward-biased rows
share the same recursive reduced signatures as the expanded rows.
```

## Solved-Surface Recursive Comparison

Artifact:

```text
research/06-cryptology-rsa/experiments/rsa/v2/output/grammar_recursive_solved_surface/
```

The original solved-label surface was measured with the same lag-3 recursive
target grammar instrument.

Rows:

```text
solved target-side recursive rows: 48
expanded target-side recursive rows: 140
```

Solved target-local direction classes:

```text
none:         38
outward_only: 8
inward_only: 2
```

Coarser signatures overlap between surfaces:

```text
lag-2 reduced signatures:
  solved signatures:   36
  expanded signatures: 45
  overlap:             19

lag-3 reduced signatures:
  solved signatures:   35
  expanded signatures: 44
  overlap:             18

recursive class signatures:
  solved signatures:   19
  expanded signatures: 28
  overlap:             13
```

The combined reduced recursive signatures separate the surfaces:

```text
lag-2 + lag-3 reduced signatures:
  solved signatures:   48
  expanded signatures: 81
  overlap:              0

full recursive reduced signatures:
  solved signatures:   48
  expanded signatures: 82
  overlap:              0
```

The outward-only solved rows also separate:

```text
solved outward-only rows: 8
solved outward-only lag-2 + lag-3 reduced signatures: 8
overlap with expanded lag-2 + lag-3 signatures: 0
```

Current pattern statement:

```text
The original outward-biased solved-label surface and the deterministic
target-cell expansion share coarse recursive classes, but they do not share
combined lag-2 + lag-3 reduced signatures. The two surfaces occupy distinct
recursive reduced grammar families at this granularity.
```

Next evidence step:

```text
Use the solved-surface lag-2 + lag-3 reduced signatures as grammar family
labels, then test fresh solved rows against those families before deriving any
compatibility or exclusion rule.
```

## Inverse Word Exclusion Probe

Artifact:

```text
research/06-cryptology-rsa/experiments/rsa/v2/output/grammar_inverse_word_exclusion/
```

The inverse probe tests whether solved rows share recursive pieces with the
expanded surface while excluding the expanded surface's ordered reduced words.

Global scope:

```text
solved rows: 48
lag-2 piece hits: 30
lag-3 piece hits: 29
lag-2 + lag-3 ordered word hits: 0
full recursive reduced word hits: 0
recursive class hits: 41
component-sharing word exclusions: 40
```

Public-cell scope:

```text
solved rows: 48
lag-2 piece hits: 14
lag-3 piece hits: 11
lag-2 + lag-3 ordered word hits: 0
full recursive reduced word hits: 0
recursive class hits: 24
component-sharing word exclusions: 22
```

Public-cell plus target-side scope:

```text
solved rows: 48
lag-2 piece hits: 10
lag-3 piece hits: 5
lag-2 + lag-3 ordered word hits: 0
full recursive reduced word hits: 0
recursive class hits: 17
component-sharing word exclusions: 15
```

Current inverse-pattern statement:

```text
The inverse relation is not a simple low/high opposition. It is component
sharing with ordered-word exclusion. Solved rows reuse recursive pieces and
coarse classes from the expansion surface, but avoid the expansion surface's
combined lag-2 + lag-3 reduced words.
```

Concrete decision rule for the next evidence pass:

```text
When a candidate target row shares lag-2 or lag-3 recursive pieces with an
excluded family but also repeats that family's combined lag-2 + lag-3 reduced
word, mark it grammar-incompatible for that family.
```
