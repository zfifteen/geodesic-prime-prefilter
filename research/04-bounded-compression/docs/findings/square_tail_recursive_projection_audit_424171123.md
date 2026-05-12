# Square-Tail Recursive Projection Audit

## Status

Measured route audit. This is not a proof of the square-tail theorem.

## Finding

Pointwise child projection does not prove parent closure.

For the current record root

```text
r = 424,171,123
```

the strongest projected child root is

```text
r' = 509.
```

The parent word contains `509` as a least-factor letter exactly once. The
child obstruction prefix for `509` has `23` entries, and the child
counterexample word would require `39` entries.

The child word also uses least factors that are absent from the parent word:

```text
83, 449
```

Therefore the direct-containment version of the recursive-collapse route is
invalidated on the current record. The surviving recursive target must be a
joint cascade theorem or a covering-impossibility theorem. It cannot be the
claim that a closed child projection, by itself, supplies the child word
inside the parent word.

## Audit Artifact

```text
research/04-bounded-compression/output/square_tail_recursive_projection_audit_424171123_509.json
```

The executable audit is:

```text
research/04-bounded-compression/scripts/square_tail_recursive_projection_audit.py
```

Run:

```text
python3 research/04-bounded-compression/scripts/square_tail_recursive_projection_audit.py \
  --parent-root 424171123 \
  --child-root 509 \
  --output research/04-bounded-compression/output/square_tail_recursive_projection_audit_424171123_509.json
```

## Proof Consequence

The next valid lemma cannot be:

```text
Every closed child projection directly contains the obstruction word needed to
close the parent.
```

The next valid lemma must have a stronger form:

```text
A complete parent obstruction word forces a global recursive cascade or an
impossible moving residue cover.
```

This keeps the square-tail proof target deterministic and exact. The remaining
problem is still the same theorem:

```text
D(r) = r^2 - P(r^2) <= max(64, ceil(0.5 * log(r^2)^2))
```

on the selected-square branch.
