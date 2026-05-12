# Square-Tail Dynamic-Tail Audit For Root 509 CRT Representative

## Status

Audit evidence. Not a proof.

## Finding

The first prime selected-square representative of the `509` CRT rough-cover
class closes in its own dynamic tail, not inside the modeled source window.

The representative root is

```text
89726961223544427015292389839
```

Its modeled source window ends at even offset `78`. Its actual previous prime
below the square occurs at even offset `338`, inside the dynamic cutoff `8889`.

| Quantity | Value |
|---|---:|
| Source root | `509` |
| Source `M` | `39` |
| Representative dynamic cutoff | `8889` |
| Representative `M` | `4444` |
| Dynamic-tail even offsets audited | `80..338` |
| Tail positions | `130` |
| Covered by source small carriers | `94` |
| Covered by source assigned large carriers | `20` |
| Covered by any source-modeled carrier | `98` |
| Covered by new repeat-capable carriers | `65` |
| Representative rough tail positions | `13` |
| Prime-valued tail positions | `1` |
| Prime-valued offset | `338` |

The representative's own rough tail offsets are:

```text
80, 114, 128, 132, 182, 194, 252, 260, 278, 300, 318, 332, 338
```

The only prime-valued row among those rough tail offsets is `338`.

## Boundary

This audit does not prove the infinite-tail theorem. It shows that the source
CRT cover does not explain the later closure. The closure appears in the
representative's own dynamic rough tail.

The live theorem target remains:

```text
every selected-square root has at least one prime-valued rough defect before
the dynamic cutoff.
```

The artifact is:

```text
research/04-bounded-compression/output/square_tail_dynamic_tail_audit_509.json
```

The executable audit is:

```text
research/04-bounded-compression/scripts/square_tail_dynamic_tail_audit.py
```
