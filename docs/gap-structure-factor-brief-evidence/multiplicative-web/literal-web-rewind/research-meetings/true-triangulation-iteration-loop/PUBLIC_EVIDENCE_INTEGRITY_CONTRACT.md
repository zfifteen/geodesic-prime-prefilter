# Public Evidence Integrity Contract

This contract controls semiprime factor-recovery and scale runs in this folder.

The recovery claim is admissible only when a public artifact emits a factor
distance from `N` alone before any private audit reads the hidden factors.

## Required Order

1. Create public input containing `N` only.
2. Run an `N`-only public nomination program.
3. Freeze `public_output.jsonl` and `public_manifest.json` with SHA-256 hashes.
4. Unlock private audit only after the public freeze record exists.
5. Run the fixed canonical membership checker.
6. Use only the canonical checker's `status.json` for recovery language.

## Allowed Status Labels

- `recovered`: the frozen public output emitted one of the hidden factor
  distances.
- `missed`: the frozen public output did not emit either hidden factor
  distance.
- `unresolved`: the public program did not produce an admissible output.
- `invalid`: private factor information influenced public inference.

`contained_only` is an audit-side classification only. It is not recovery
evidence and cannot headline a scale claim.

## Private-Factor Quarantine

After a public freeze exists for a given `N`, any touch of hidden factors or
derived hidden distances is allowed only through the fixed canonical
membership checker.

Forbidden inside a recovery run after public freeze, regardless of filename or
purpose label:

- private rank studies;
- private score computations;
- containment measurements;
- band-position measurements;
- radius diagnostics using hidden factors;
- private-factor visualizations;
- sidecar files based on hidden factor ranks;
- summaries based on hidden factor ranks.

Any private-factor touch outside the canonical checker requires:

```text
POST_FREEZE_VIOLATION: private factor touch outside canonical membership checker
EXECUTION: aborted
SUMMARY_ALLOWED: false
```

## Canonical Checker Rule

The canonical checker may only:

1. load emitted public distances;
2. load hidden audit factors;
3. evaluate membership of each hidden factor in the emitted public distance set;
4. write `recovered` or `missed`.

It must not rank, score, sort, compare bands, compute containment intervals, or
call public scoring functions after hidden factors are available.
