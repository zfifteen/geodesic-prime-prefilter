# Square-Tail Projection Graph Audit

## Status

Measured cascade audit. This is not a proof of the square-tail theorem.

## Finding

The current record root has a finite descending projection graph with no open
observed descendants.

For

```text
r = 424,171,123
```

the transitive least-factor projection graph has:

| Quantity | Value |
|---|---:|
| Nodes | `208` |
| Edges | `900` |
| Maximum depth | `6` |
| Sink nodes | `57` |
| Nondecreasing edges | `0` |
| Open cutoff nodes | `0` |
| Non-selected square nodes | `0` |

Every edge strictly decreases the root. Every observed node is closed by its
own dynamic cutoff and satisfies the selected-square condition.

The graph artifact is:

```text
research/04-bounded-compression/output/square_tail_projection_graph_424171123.json
```

The executable audit is:

```text
research/04-bounded-compression/scripts/square_tail_projection_graph.py
```

Run:

```text
python3 research/04-bounded-compression/scripts/square_tail_projection_graph.py \
  --root 424171123 \
  --output research/04-bounded-compression/output/square_tail_projection_graph_424171123.json
```

## Proof Boundary

This graph does not prove the parent theorem.

Strict descent is automatic because every least factor of `r^2 - 2m` is below
`r`. Descendant closure is measured on this record. The missing theorem is the
edge semantics:

```text
closed descendant states eliminate the hypothetical complete parent
obstruction word.
```

That implication is not present in the current proof. The graph audit narrows
the recursive route to a precise target:

```text
prove a deterministic descent law from complete parent obstruction words to
closed descendant states, or replace the route with a moving-cover
impossibility theorem.
```
