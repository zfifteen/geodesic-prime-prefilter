# GWR-Relative All-O6 Boundary

## Status

This is measured sidecar evidence for the PEDK gap-compatibility hypothesis.

The previous exact-subtype table showed that the public state must include the
exact type of the gap containing `N` and the phase of `N` inside that gap. This
table adds the local position of `N` relative to the selected integer inside
the same gap.

## Object

The containing gap has a left endpoint, a right endpoint, and a selected
integer inside the gap. The selected integer is the local GWR winner: the
leftmost minimum-divisor position chosen by the Prime Gap Structure rule.

For each semiprime row, define:

```text
gwr_signed_distance = n_offset_from_left - winner_offset
```

The public object is:

```text
S_gwr(N) = exact_type(gap(N)) @ phase(N inside gap(N)) @ gwr_signed_distance
```

The downstream compatibility label is:

```text
F(p,q) = all-o6 factor-neighborhood signature
```

## Experiment

Script:

```text
gwr_relative_all_o6_boundary.py
```

Output:

```text
output/gwr_relative_all_o6_boundary_601_5500/
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

Across the six all-`o6` observations:

```text
all_o6_distance_counts:
  0: 1
  2: 1
  14: 1
  24: 1
  26: 1
  37: 1

all_o6_side_counts:
  at_winner: 1
  after_winner: 5
```

The all-`o6` rows are:

```text
case_id                    state              exact_type           distance
small_semiprime_1823_1861  o4_even@mid        o4_d4_a3_d4_even     37
small_semiprime_3001_3331  o4_odd@mid         o4_d4_a4_d4_odd      14
small_semiprime_3301_3331  o4_odd@mid         o4_d4_a10_d4_odd     2
small_semiprime_4021_4261  o6_odd@late        o6_d4_a4_d4_odd      26
small_semiprime_4583_4801  o4_odd@late        o4_d4_a10_d4_odd     24
small_semiprime_5281_5303  o4_odd@mid         o4_d4_a4_d4_odd      0
```

## Key Contrast

The same exact subtype behaves differently at different phases:

```text
o4_d4_a4_d4_odd@early:
  distance 0   rows 576   all-o6 0
  distance 2   rows 121   all-o6 0
  distance 6   rows 46    all-o6 0
  distance 8   rows 18    all-o6 0

o4_d4_a4_d4_odd@mid:
  distance 0   rows 586   all-o6 1
  distance 14  rows 112   all-o6 1
```

The GWR-relative distance is not a replacement for phase. It is the next
coordinate in the public word. The compatibility object is the joint structure:

```text
exact_type(gap(N)) @ phase(N inside gap(N)) @ distance_from_GWR_winner
```

## Interpretation

The law is not visible as a one-dimensional threshold. Plain residue,
parity, exact subtype, phase, and GWR-relative distance each lose information
when separated.

The all-`o6` corner appears only at specific joint public words. The strongest
current exclusion cell remains:

```text
o4_d4_a4_d4_odd@early
```

with `770` rows and zero all-`o6` observations across factors `601..5500`.

The strongest local contrast is:

```text
o4_d4_a4_d4_odd@early@distance0  rows 576  all-o6 0
o4_d4_a4_d4_odd@mid@distance0    rows 586  all-o6 1
```

The same exact subtype and the same GWR-relative distance diverge by phase.
That is direct evidence that the compatibility law uses a grammar word, not an
isolated scalar.

## Next Testable Predicate

The next forward predicate is:

```text
all-o6 is excluded from o4_d4_a4_d4_odd@early
```

The stricter local predicate is:

```text
all-o6 is excluded from o4_d4_a4_d4_odd@early@distance0
```

A direct falsification is:

```text
an all-o6 factor-neighborhood observation in that exact public word.
```

## Machine-Readable Artifacts

```text
output/gwr_relative_all_o6_boundary_601_5500/summary.json
output/gwr_relative_all_o6_boundary_601_5500/gwr_relation_rows.jsonl
output/gwr_relative_all_o6_boundary_601_5500/gwr_distance_rows.jsonl
output/gwr_relative_all_o6_boundary_601_5500/all_o6_observation_rows.jsonl
```

## Boundary

This is measured sidecar evidence. It is not a theorem, not live PEDK
inference, and not a factor resolver. It identifies a sharper public grammar
coordinate for the next compatibility-law extraction pass.
