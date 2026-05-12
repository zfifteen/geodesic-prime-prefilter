# Square-Tail Full-Cutoff CRT Model For Root 509 Representative

## Status

Invalidated proof route.

## Finding

The first prime selected-square representative of the `509` CRT rough-cover
class admits a local CRT obstruction model through its full dynamic cutoff.

The model preserves every repeat-capable residue class for the representative
root through

```text
M = 4444.
```

It then assigns one distinct singleton carrier greater than `M` to each rough
position. The CRT system is consistent and its residue is coprime to its
modulus.

| Quantity | Value |
|---|---:|
| Source root | `509` |
| Representative root | `89726961223544427015292389839` |
| `M` | `4444` |
| Repeat-capable prime carriers | `602` |
| Positions covered by repeat-capable carriers | `3875 / 4444` |
| Rough positions | `569` |
| Assigned singleton carriers | `569` |
| First singleton carrier | `4451` |
| Last singleton carrier | `14741` |
| CRT residue digits | `4136` |
| CRT modulus digits | `4136` |
| CRT residue coprime to modulus | `true` |
| Local model consistent | `true` |

The first rough offsets are:

```text
80, 114, 128, 132, 182, 194, 252, 260, 278, 300,
318, 332, 338, 344, 360, 362, 390, 402, 428, 444
```

The last rough offsets are:

```text
8582, 8592, 8594, 8598, 8624, 8640, 8658, 8672, 8682,
8690, 8700, 8708, 8730, 8738, 8760, 8774, 8780, 8784,
8828, 8868
```

## Boundary

This is not a square-tail counterexample. It is a local CRT model.

It rules out a broader congruence-only proof route:

```text
repeat-capable residues through the full dynamic cutoff
+ one singleton carrier per rough row
-> contradiction
```

No such contradiction exists at the local CRT level for this representative.
The missing theorem must use an ordered PGS condition that the local CRT model
does not encode.

The carrier comparison in

```text
research/04-bounded-compression/docs/findings/square_tail_model_actual_carrier_compare_509.md
```

records the exact separation: the model's singleton carriers do not match the
representative's actual least factors in the measured rough tail.

The artifact is:

```text
research/04-bounded-compression/output/square_tail_full_cutoff_crt_model_509.json
```

The executable model is:

```text
research/04-bounded-compression/scripts/square_tail_full_cutoff_crt_model.py
```
