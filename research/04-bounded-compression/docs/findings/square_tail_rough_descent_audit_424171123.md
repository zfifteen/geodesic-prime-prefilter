# Square-Tail Rough-Defect Descent Audit

## Status

Measured recursive-descent audit. This is not a proof of the square-tail
theorem.

## Finding

Every composite M-rough defect in the standing record descends to a smaller
root that is closed by its own prime-valued M-rough defect.

For

```text
r = 424,171,123
```

the parent rough-defect audit has:

| Quantity | Value |
|---|---:|
| Parent `M` | `395` |
| Parent M-rough defects | `65` |
| Parent prime-valued M-rough defects | `3` |
| Parent composite M-rough defects | `62` |
| Distinct composite least-factor children | `62` |
| Children with root smaller than parent | `62` |
| Children closed by prime-valued M-rough defect | `62` |

The largest child by `M` is:

```text
root = 159,673,649
M = 357
rough defects = 57
prime-valued rough defects = 21
```

The largest child by rough-defect count is:

```text
root = 108,562,759
M = 342
rough defects = 73
prime-valued rough defects = 17
```

## Audit Artifact

```text
research/04-bounded-compression/output/square_tail_rough_descent_audit_424171123.json
```

The executable audit is:

```text
research/04-bounded-compression/scripts/square_tail_rough_descent_audit.py
```

Run:

```text
python3 research/04-bounded-compression/scripts/square_tail_rough_descent_audit.py \
  --root 424171123 \
  --output research/04-bounded-compression/output/square_tail_rough_descent_audit_424171123.json
```

## Proof Boundary

This audit supports the recursive route but does not close it.

The missing implication is:

```text
closed rough-defect children eliminate the possibility that the parent has a
complete composite rough-defect set.
```

That implication is not proved by the current artifacts. The audit shows that
the measured descent has closed leaves; it does not prove that closed leaves
force parent closure.
