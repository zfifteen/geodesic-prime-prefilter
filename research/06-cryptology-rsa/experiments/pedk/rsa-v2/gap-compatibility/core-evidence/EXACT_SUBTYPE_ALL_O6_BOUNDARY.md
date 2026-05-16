# Exact Subtype All-O6 Boundary

## Status

This is measured sidecar evidence for the PEDK gap-compatibility hypothesis.

The previous refinement showed that all-`o6` compatibility is not decided by
the reduced public phase state alone. This note splits the same public states
by the exact subtype of the gap containing `N`.

## Object

The downstream compatibility label is:

```text
F(p,q) = all-o6 factor-neighborhood signature
```

The public object is:

```text
S_exact(N) = exact_type(gap(N)) @ phase(N inside gap(N))
```

The exact type key records the public first-open residue, the local `a`
component, the divisor threshold family, and parity. For example:

```text
o4_d4_a4_d4_odd
o4_d4_a10_d4_odd
```

## Experiment

Script:

```text
exact_subtype_all_o6_boundary.py
```

Output:

```text
output/exact_subtype_all_o6_boundary_601_5500/
```

Bands:

```text
601..1000
1001..1400
1401..1800
1801..2200
2201..2600
2601..3000
3001..3500
3501..4000
4001..4500
4501..5000
5001..5500
```

## Measured Result

Across the six target public phase states:

```text
exact_subtype_cell_count = 51
all_o6_compatible_cell_count = 5
all_o6_not_observed_cell_count = 46
all_o6_observation_count = 6
```

All-`o6` compatible exact-subtype cells:

```text
state                   exact_type            rows  all-o6  rate_mpermille
o4_d4_even@mid          o4_d4_a3_d4_even      320   1       3
o4_d4_odd@late          o4_d4_a10_d4_odd      74    1       13
o4_d4_odd@mid           o4_d4_a10_d4_odd      210   1       4
o4_d4_odd@mid           o4_d4_a4_d4_odd       1884  2       1
o6_d4_odd@late          o6_d4_a4_d4_odd       117   1       8
```

The two surviving reduced-state exclusions break into these exact-subtype
cells:

```text
o2_d4_odd@late
  o2_d4_a2_d4_odd       544   all-o6 0
  o2_d4_a6_d4_odd       176   all-o6 0
  o2_d4_a8_d4_odd       66    all-o6 0
  o2_d4_a4_d4_odd       47    all-o6 0
  o2_d4_a12_d4_odd      35    all-o6 0
  o2_d4_a14_d4_odd      10    all-o6 0
  o2_d4_a10_d4_odd      8     all-o6 0
  o2_d4_a18_d4_odd      5     all-o6 0
  o2_d4_a16_d4_odd      3     all-o6 0

o4_d4_odd@early
  o4_d4_a4_d4_odd       770   all-o6 0
  o4_d4_a6_d4_odd       114   all-o6 0
  o4_d4_a2_d4_odd       98    all-o6 0
  o4_d4_a10_d4_odd      15    all-o6 0
  o4_d4_a8_d4_odd       6     all-o6 0
  o4_d4_a12_d4_odd      2     all-o6 0
```

## Interpretation

The exact subtype split exposes a phase-sensitive grammar rule candidate.

The same public exact subtype can change compatibility when the position of
`N` inside the containing gap changes:

```text
o4_d4_a4_d4_odd@mid    admits all-o6
o4_d4_a4_d4_odd@early  has not admitted all-o6 across 770 rows
```

The same is visible for `a10`:

```text
o4_d4_a10_d4_odd@mid   admits all-o6
o4_d4_a10_d4_odd@late  admits all-o6
o4_d4_a10_d4_odd@early has not admitted all-o6 across 15 rows
```

The compatibility map is therefore not just residue, parity, or exact subtype.
It is the joint public state:

```text
exact_type(gap(N)) @ phase(N inside gap(N))
```

That is the multiplication map object in sharper form.

## Next Testable Predicate

The current strongest exact-subtype test is:

```text
all-o6 is excluded from o4_d4_a4_d4_odd@early
```

The broad two-state survivor remains:

```text
all-o6 is excluded from:
  o2_d4_odd|d<=4@late
  o4_d4_odd|d<=4@early
```

A direct falsification of the strongest exact-subtype candidate is:

```text
an all-o6 factor-neighborhood observation in o4_d4_a4_d4_odd@early.
```

## Machine-Readable Artifacts

```text
output/exact_subtype_all_o6_boundary_601_5500/summary.json
output/exact_subtype_all_o6_boundary_601_5500/exact_subtype_rows.jsonl
output/exact_subtype_all_o6_boundary_601_5500/all_o6_observation_rows.jsonl
```

## Boundary

This is measured sidecar evidence. It is not a theorem, not live PEDK
inference, and not a factor resolver. The strongest current object is a
candidate exclusion surface for the next forward band.
