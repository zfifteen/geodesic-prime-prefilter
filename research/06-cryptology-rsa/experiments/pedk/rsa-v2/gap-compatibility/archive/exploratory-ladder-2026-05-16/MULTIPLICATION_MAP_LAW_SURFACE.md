# Multiplication Map Law Surface

## Status

This is measured sidecar evidence for the PEDK gap-compatibility hypothesis.

The object is the observed multiplication map from public gap words around `N`
to unordered factor-neighborhood words around `p` and `q`.

## Object

The public word records:

```text
previous reduced gap state
containing exact type @ phase of N
following reduced gap state
```

Example:

```text
prev=o2_d4_odd|d<=4
containing=o2_d4_a2_d4_odd@mid
next=o4_d4_odd|d<=4
```

The factor word records the unordered pair of factor endpoint neighborhoods,
with each side carrying reduced gap state and winner phase:

```text
L=<left factor gap reduced state>@<winner phase>
R=<right factor gap reduced state>@<winner phase>
||
L=<left factor gap reduced state>@<winner phase>
R=<right factor gap reduced state>@<winner phase>
```

This is the current table form of the multiplication map:

```text
S(N) -> F(p,q)
```

## Experiment

Script:

```text
multiplication_map_law_surface.py
```

Output:

```text
output/multiplication_map_law_surface_601_5500/
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

Support thresholds:

```text
min_public_support = 50
min_factor_support = 20
```

## Measured Result

```text
public_word_count = 5178
factor_word_count = 2048
observed_cell_count = 16710
supported_public_word_count = 23
supported_factor_word_count = 198
candidate_exclusion_count = 3741
```

## Interpretation

This is the first broad table where the rule surface becomes visible as a
compatibility grammar rather than as a single all-`o6` corner.

The table separates three things:

```text
public_word_rows.jsonl   public words and observed factor-word support
factor_word_rows.jsonl   globally observed factor words
map_cell_rows.jsonl      observed cells plus candidate exclusions
```

The candidate exclusions are not theorem claims. They are absent cells between
supported public words and supported factor words. They are the raw material
from which the factor-neighborhood compatibility and incompatibility rules
must be compressed.

## Next Compression Target

The next research step is to compress the `3741` candidate exclusions by shared
grammar components:

```text
containing exact type
N phase
GWR-relative distance
previous and following public reduced states
factor-side residue multiset
factor-side winner-phase multiset
```

The all-`o6` work has already shown how this compression behaves at one corner
of the map. The same compression should now be applied to the full factor-word
surface.

## Machine-Readable Artifacts

```text
output/multiplication_map_law_surface_601_5500/summary.json
output/multiplication_map_law_surface_601_5500/public_word_rows.jsonl
output/multiplication_map_law_surface_601_5500/factor_word_rows.jsonl
output/multiplication_map_law_surface_601_5500/map_cell_rows.jsonl
```

## Boundary

This is measured sidecar evidence. It is not a theorem, not live PEDK
inference, and not a factor resolver. It is the broad compatibility surface
from which candidate rules can now be derived and tested.
