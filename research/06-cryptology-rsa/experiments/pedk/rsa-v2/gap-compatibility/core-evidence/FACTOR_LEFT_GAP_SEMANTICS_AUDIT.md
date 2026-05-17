# Factor Left Gap Semantics Audit

## Finding

The current factor-left record is a two-endpoint bridge.

For a factor endpoint `p`, the stored left record does not describe only the
immediate interval from the previous endpoint to `p`. It describes the span from
the second previous endpoint to `p`. The selected point inside that stored span
is the immediate previous endpoint.

In symbols, if:

```text
u < v < p
```

are consecutive PGS endpoints, then the current stored factor-left record is:

```text
u -> p
```

and its selected point is:

```text
v
```

Therefore:

```text
stored left winner distance from factor = p - v
```

The `very_late` label in the shared-load reentry rows is not an abstract phase
feature. It records that the immediate previous endpoint is very close to the
factor endpoint.

## Measured Audit

The audit covers all enriched multiplication-map output bands currently present
under `core-evidence/output/`.

```text
factor-side records audited = 561444
stored left gap contains immediate previous endpoint = 561444
stored left winner is immediate previous endpoint = 561444
```

For the load-match reentry rows:

```text
load-match reentry factor-side records = 4
load-match reentry very_late left records = 2
very_late left winner is immediate previous endpoint = 2
factor minus immediate previous endpoint = 2: 2
```

## Consequence

The current proof target can be stated without phase vocabulary:

```text
first public load 4
and
right endpoint boundary 4
and
right-boundary reentry
    -> one replacement factor has immediate-left endpoint distance 2
```

Equivalently, the observed reentry lift goes through a factor endpoint whose
immediate predecessor is two units to the left.

This does not prove the law. It replaces a phase-bucket statement with a
literal endpoint-distance statement.

## Boundary

This audit is also a representation warning. The current factor-left field is
not the ordinary immediate left interval alone. It is a bridge that includes the
ordinary immediate left endpoint as its selected point.

Any proof or implementation using this field must treat it as:

```text
second-previous endpoint -> factor endpoint, selected at immediate previous endpoint
```

not as:

```text
immediate previous endpoint -> factor endpoint
```

## Reproduction

Run:

```text
python3 factor_left_gap_semantics_audit.py
```

Primary outputs:

```text
output/factor_left_gap_semantics_audit/summary.json
output/factor_left_gap_semantics_audit/audit_rows.jsonl
output/factor_left_gap_semantics_audit/load_match_reentry_rows.jsonl
```

The `output/` tree is ignored. The committed script is the reproducible
instrument.
