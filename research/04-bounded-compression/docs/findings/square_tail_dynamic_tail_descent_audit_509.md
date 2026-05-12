# Square-Tail Dynamic-Tail Descent Audit For Root 509 CRT Representative

## Status

Audit evidence. Not a proof.

## Finding

The first prime selected-square representative of the `509` CRT rough-cover
class has `13` rough tail rows after the modeled source window. Twelve are
composite and one is prime.

Every composite rough tail row descends through its least factor to a smaller
selected-square child that is closed by its own dynamic cutoff.

| Quantity | Value |
|---|---:|
| Source root | `509` |
| Representative root | `89726961223544427015292389839` |
| Representative `M` | `4444` |
| Rough tail rows | `13` |
| Composite rough tail rows | `12` |
| Prime rough tail rows | `1` |
| Prime rough tail offset | `338` |
| Least-factor child projections | `12` |
| Child projections closed by cutoff | `12` |
| Child projections selected-square | `12` |
| Child closing primes covering inside representative `M` | `0` |

The composite rough-tail least factors are:

```text
6736351,
1714849,
665241324811967767,
7541,
1614712643,
13214687,
31249,
15277,
333497,
284521,
149969,
170450107
```

Their child offsets are:

```text
2, 14, 42, 38, 50, 32, 38, 8, 20, 18, 24, 80
```

## Boundary

This strengthens the recursive evidence but does not prove the transport law.
The current facts are:

1. each composite rough-tail row has a smaller selected-square child;
2. each such child is closed by its own dynamic cutoff;
3. the representative itself closes at the remaining prime-valued rough row.

The direct parent-cover interpretation is false for this representative. If
each child closing prime is treated as a possible carrier in the parent root,
none of the resulting parent residues lies inside the representative cutoff
window.

The missing theorem is still the parent-to-child implication:

```text
closed child rough-tail structure
-> parent rough-tail elimination
```

The artifact is:

```text
research/04-bounded-compression/output/square_tail_dynamic_tail_descent_audit_509.json
```

The executable audit is:

```text
research/04-bounded-compression/scripts/square_tail_dynamic_tail_descent_audit.py
```
