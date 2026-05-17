# Simple Endpoint Exclusion Rule

## Rule

The current PGS-native exclusion rule is:

```text
Given a public at-winner composite-gap word W,
and a directed endpoint-pair cell E around the two factor endpoints,
exclude E when:

1. E is absent for W across the prior measured bands,
2. E has sufficient prior support as an endpoint-pair cell,
3. the maximum right-following endpoint residue of E is o4.
```

In compact form:

```text
public_at_winner(W)
and prior_absent(W, E)
and supported(E)
and max(right_residue(E)) = o4
    -> exclude E
```

This is an endpoint-space exclusion rule. It does not claim that every true
factor pair under `public_at_winner` has `max(right_residue)=o4`. Actual
factor observations still include other right-residue maxima. The rule applies
to candidate endpoint-pair cells that are already absent under the public word;
the invariant identifies the stable carrier of those exclusions.

## Definitions

For each factor endpoint, take the prime gap immediately to its right. Record
the first-open residue of that right-following gap as one of:

```text
o2, o4, o6
```

Rank them by their wheel order:

```text
o2 = 1
o4 = 2
o6 = 3
```

For the two factor endpoints together:

```text
right_residue_max(E) =
    max(rank(p_right_residue), rank(q_right_residue))
```

The simple invariant is:

```text
right_residue_max(E) = rank(o4)
```

The endpoint-pair cell reaches the middle right-following residue and does not
reach the high right-following residue.

Equivalently:

```text
right_boundary_balance(E) = middle_o4_balance
```

with the two off-balance states:

```text
max=o2 -> shortfall_below_o4
max=o6 -> overshoot_above_o4
```

## Measured Status

Across five strict-forward windows:

```text
21001..23000
23001..25000
25001..27000
27001..30000
30001..32000
```

the rule excludes:

```text
excluded_endpoint_cell_count = 37834
exact_falsifications = 0
```

The complement is not clean:

```text
max(right_residue)=o2 -> 2 / 11352 exact-pair falsifications
max(right_residue)=o6 -> 24 / 4882 exact-pair falsifications
```

Public-locality check:

```text
public_containing_exact_type_count = 9
right_residue_max_o4_falsified_type_count = 0
full_public_word_testable_count = 143
right_residue_max_o4_falsified_public_word_count = 0
```

The unchanged rule also survived the first fresh extension window:

```text
fresh_window = 30001..32000
fresh_testable_endpoint_cells = 7216
fresh_exact_falsifications = 0
```

## Interpretation

The public selected position of `N` does not merely correlate with a loose
factor-neighborhood label. It filters factor endpoint space by a directed
boundary condition.

The right-following side is the side reached by moving outward from each
factor endpoint. Under the public at-winner condition, the stable excluded
endpoint cells are exactly the cells whose right-following residue maximum
lands on the middle residue. Too low (`o2`) and too high (`o6`) both leave the
zero-falsification exclusion surface.

This is the current simple invariant candidate beneath the measured PEDK gap
compatibility signal.

The mechanism is stated directly in:

```text
PUBLIC_SELECTED_POSITION_FILTER_MECHANISM.md
```

## Reproduction

Run:

```text
python3 simple_invariant_probe.py
```

Primary rule output:

```text
output/simple_invariant_probe/excluded_endpoint_cell_rows.jsonl
```
