# Positive Signature Compression

## Status

This is measured sidecar evidence for the PEDK gap-compatibility hypothesis.

It compresses the `72` stable positive signatures from the five-state
positive map by their factor-side residue grammar.

## Object

Each stable positive signature has four factor-side gap residues:

```text
p-left, p-right, q-left, q-right
```

The compression records the multiset count of:

```text
o2, o4, o6
```

across those four positions.

## Experiment

Script:

```text
positive_signature_compression.py
```

Input:

```text
output/five_state_positive_signature_map/stable_positive_signature_rows.jsonl
```

Output:

```text
output/positive_signature_compression/
```

## Measured Result

The `72` stable positive signatures use `12` residue multisets.

The all-`o6` multiset is absent:

```text
all_o6_positive_signature_count = 0
all_positive_signatures_have_non_o6_residue = true
```

No exact factor-neighborhood signature appears in all five public phase states:

```text
all_state_intersection_signature_count = 0
```

Residue presence:

```text
signatures_with_o2_count = 67
signatures_with_o4_count = 62
signatures_with_o6_count = 57
```

Largest residue multisets:

```text
o2:2|o4:1|o6:1  stable_positive_signature_count = 16
o2:1|o4:2|o6:1  stable_positive_signature_count = 14
o2:1|o4:1|o6:2  stable_positive_signature_count = 13
o2:2|o4:0|o6:2  stable_positive_signature_count = 6
o2:3|o4:1|o6:0  stable_positive_signature_count = 6
o2:2|o4:2|o6:0  stable_positive_signature_count = 5
```

## Interpretation

The allowed side is not merely the complement of the all-`o6` exclusion. The
stable positive signatures concentrate in mixed-residue neighborhoods.

The clearest compact statement is:

```text
In the five refined public phase states, stable positive signatures always
contain at least one non-o6 factor-side residue.
```

The all-`o6` exclusion is therefore visible as a missing corner of a larger
mixed-residue compatibility surface.

The positive side is state-specific at exact-signature resolution. The common
structure is residue-level, not a single universal allowed signature shared by
all five public phase states.

## Machine-Readable Artifacts

```text
output/positive_signature_compression/summary.json
output/positive_signature_compression/positive_signature_residue_rows.jsonl
output/positive_signature_compression/residue_multiset_rows.jsonl
output/positive_signature_compression/state_residue_multiset_rows.jsonl
output/positive_signature_compression/all_state_intersection_signature_rows.jsonl
```

## Boundary

This is measured sidecar evidence. It is a grammar compression of downstream
factor-neighborhood labels, not a theorem and not live PEDK inference.

The unresolved target is to derive a PGS-native mechanism for why the stable
positive surface favors mixed residues and excludes the all-`o6` corner in the
five refined public phase states.
