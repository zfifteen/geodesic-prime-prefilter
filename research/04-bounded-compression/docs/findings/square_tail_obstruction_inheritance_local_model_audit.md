# Square-Tail Obstruction Inheritance Local-Model Carrier Audit

## Status

Invalidated proof route.

## Finding

The full-cutoff local CRT obstruction model does not force obstruction on its
assigned singleton carriers.

The model gives a locally consistent complete parent obstruction through the
representative cutoff. Its assigned singleton carriers are congruence carriers
for the modeled rough rows. They are not certified least factors of the
modeled row values. Every one of those assigned carriers is closed by at least
one prime-valued M-rough defect.

| Quantity | Value |
|---|---:|
| Source root | `509` |
| Parent rough defects in local model | `569` |
| Assigned singleton carriers | `569` |
| Assigned carriers with `O(ell)` | `0` |
| Closed assigned carriers | `569` |

## Boundary

The selection-free descent target cannot be proved from local congruence
consistency plus assigned carrier closure alone:

```text
local complete carrier cover at r
-> some assigned carrier ell also has O(ell)
```

is false for the full-cutoff local CRT model.

This does not refute obstruction inheritance for actual prime roots, because
actual `Child(r)` uses least factors of parent rough rows. The local CRT model
does not certify least-factor minimality above `M`. The remaining theorem must
use least-factor/global PGS structure, or it must prove direct impossibility of
`O(r)` for positive-row prime roots.

## Second Opinion

Grok response `cad9c1e1-0889-9eeb-8b74-feb21382ecd7` agreed that local
congruence structure alone does not force obstruction inheritance. The response
described the model as a counterexample to obstruction inheritance; the precise
statement is narrower. It is a counterexample to assigned-carrier obstruction
inheritance, not to the least-factor actual-prime-root theorem.

The artifact is:

```text
research/04-bounded-compression/output/square_tail_obstruction_inheritance_local_model_audit.json
```

The executable audit is:

```text
research/04-bounded-compression/scripts/square_tail_obstruction_inheritance_local_model_audit.py
```
