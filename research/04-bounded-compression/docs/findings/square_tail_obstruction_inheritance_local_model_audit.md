# Square-Tail Obstruction Inheritance Local-Model Audit

## Status

Invalidated proof route.

## Finding

The full-cutoff local CRT obstruction model does not force obstruction
inheritance.

The model gives a locally consistent complete parent obstruction through the
representative cutoff. Its assigned singleton carriers are the model's child
roots. Every one of those child roots is closed by at least one prime-valued
M-rough defect.

| Quantity | Value |
|---|---:|
| Source root | `509` |
| Parent rough defects in local model | `569` |
| Assigned child carriers | `569` |
| Children with `O(ell)` | `0` |
| Closed children | `569` |

## Boundary

The selection-free descent target cannot be proved from the obstruction word
and local congruence consistency alone:

```text
local complete obstruction at r
-> some child ell also has O(ell)
```

is false for the full-cutoff local CRT model.

The remaining theorem must use an actual prime-root/global PGS condition that
the local CRT model does not encode, or it must prove direct impossibility of
`O(r)` for positive-row prime roots.

## Second Opinion

Grok response `cad9c1e1-0889-9eeb-8b74-feb21382ecd7` agreed with this
boundary: local congruence structure alone does not force obstruction
inheritance. The response described the model as a counterexample to
obstruction inheritance; the precise statement is narrower. It is a
counterexample to local obstruction inheritance, not to the actual-prime-root
theorem.

The artifact is:

```text
research/04-bounded-compression/output/square_tail_obstruction_inheritance_local_model_audit.json
```

The executable audit is:

```text
research/04-bounded-compression/scripts/square_tail_obstruction_inheritance_local_model_audit.py
```
